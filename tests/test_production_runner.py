"""Production routing and failure behavior without full production simulations."""
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from nkm_injection.production import ProductionRunConfig, production_stages, run_production, REQUIRED_INPUTS
from nkm_injection.paper import run_paper_pipeline
from nkm_injection.results_schema import PublicationManifest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def production_case(publication_case):
    root, selected = publication_case()
    (root / selected.injection_run / 'config.json').write_text(json.dumps({'tier': 'production'}))
    for filename in REQUIRED_INPUTS:
        if not (root / filename).exists():
            (root / filename).write_text('{}')
    (root / 'scripts').mkdir()
    config = ProductionRunConfig(repo_root=root, output_dir=root / 'results/new production', workers=2)
    for stage in production_stages(config):
        script = Path(stage.command[2])
        shutil.copy2(REPO_ROOT / 'scripts' / script.name, script)
    sources = {'baseline': root / selected.input_hash_manifest,
               'fieldmap': root / selected.field_validation_run,
               'convergence': root / selected.tracking_convergence_run,
               'multiturn': root / selected.injection_run,
               'optimization': root / selected.bts_optimization_run,
               'tolerances': root / selected.tolerance_run,
               'moga': root / selected.moga_run}
    def execute(stage):
        if stage.name == 'summary':
            manifest_path = Path(stage.command[stage.command.index('--manifest') + 1])
            assert manifest_path.is_file()
            run_paper_pipeline(root, manifest=manifest_path, output_dir=stage.output_dir,
                               create_if_missing=False, compile_pdf=False)
        else:
            for artifact in stage.expected_artifacts:
                source = sources[stage.name]
                if source.is_dir():
                    source = source / artifact
                shutil.copy2(source, stage.output_dir / artifact)
    return root, config, execute


def test_routing_workers_and_manifest(production_case):
    root, config, execute = production_case
    before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
    seen = []
    def spy(stage):
        seen.append(stage)
        assert stage.output_dir.is_relative_to(config.output_dir)
        assert stage.command[stage.command.index('--output-dir') + 1] == str(stage.output_dir)
        if stage.name in ('multiturn', 'tolerances'):
            assert stage.command[stage.command.index('--workers') + 1] == '2'
        else:
            assert '--workers' not in stage.command
            assert stage.execution_mode == 'sequential'
        execute(stage)
    report = run_production(config, executor=spy)
    assert report['status'] == 'completed'
    assert len(seen) == 8
    manifest = PublicationManifest.load(config.output_dir / 'publication_manifest.json')
    for field in ('field_validation_run', 'tracking_convergence_run', 'bts_optimization_run',
                  'injection_run', 'tolerance_run', 'moga_run', 'input_hash_manifest'):
        assert Path(getattr(manifest, field)).is_relative_to(config.output_dir)
    tolerance = next(s for s in seen if s.name == 'tolerances')
    assert tolerance.command[tolerance.command.index('--optimization-summary') + 1] == str(
        config.output_dir / 'optimization/bts_optimization_summary.json')
    assert (config.output_dir / 'summary/figures/figure_data.json').is_file()
    assert not (root / 'results/paper').exists()
    assert all(p.read_bytes() == value for p, value in before.items())
    assert json.loads((config.output_dir / 'production_config.json').read_text())['resolved_workers'] == 2


def test_dry_run_has_no_writes_or_executor_calls(production_case, capsys):
    root, config, _ = production_case
    before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
    def forbidden(stage):
        pytest.fail('dry run must not execute stages')
    report = run_production(config, dry_run=True, executor=forbidden)
    assert report['status'] == 'planned'
    assert not config.output_dir.exists()
    assert {p: p.read_bytes() for p in root.rglob('*') if p.is_file()} == before
    assert 'sequential' in capsys.readouterr().out


@pytest.mark.parametrize('setting,value', [('workers', 0), ('workers', -1), ('workers', True),
    ('seed', -1), ('tolerance_samples', 0), ('tier', 'invalid')])
def test_invalid_arguments_are_read_only(production_case, setting, value):
    _, config, _ = production_case
    setattr(config, setting, value)
    with pytest.raises(ValueError):
        run_production(config, dry_run=True)
    assert not config.output_dir.exists()


def test_missing_input_and_bad_script_are_read_only(production_case):
    root, config, _ = production_case
    source = root / 'K4GSR_HBIv4-1.mat'
    raw = source.read_bytes()
    source.unlink()
    with pytest.raises(FileNotFoundError, match='K4GSR'):
        run_production(config, dry_run=True)
    source.write_bytes(raw)
    (root / 'scripts/run_tracking_convergence.py').write_text('invalid syntax !')
    with pytest.raises(SyntaxError):
        run_production(config, dry_run=True)
    assert not config.output_dir.exists()


def test_existing_output_is_never_overwritten(production_case):
    _, config, _ = production_case
    config.output_dir.mkdir()
    sentinel = config.output_dir / 'keep.txt'
    sentinel.write_text('keep')
    with pytest.raises(ValueError, match='already exists'):
        run_production(config)
    assert sentinel.read_text() == 'keep'


@pytest.mark.parametrize('failure', ['exception', 'missing_artifact', 'invalid_publication_inputs'])
def test_failure_stops_later_stages(production_case, failure):
    _, config, execute = production_case
    visited = []
    def fail(stage):
        visited.append(stage.name)
        if stage.name == 'fieldmap' and failure == 'exception':
            raise RuntimeError('injected child failure')
        if stage.name == 'fieldmap' and failure == 'missing_artifact':
            return
        execute(stage)
        if stage.name == 'optimization' and failure == 'invalid_publication_inputs':
            (stage.output_dir / 'bts_optimization_summary.json').write_text('{}')
    with pytest.raises(RuntimeError, match='Production stopped'):
        run_production(config, executor=fail)
    assert 'summary' not in visited
    assert not (config.output_dir / 'publication_manifest.json').exists()
    if failure != 'invalid_publication_inputs':
        assert visited == ['baseline', 'fieldmap']
    report = json.loads((config.output_dir / 'production_status.json').read_text())
    assert report['status'] == 'failed'
    assert report['failed_stage'] == ('summary' if failure == 'invalid_publication_inputs' else 'fieldmap')


def test_stage_cli_contracts():
    config = ProductionRunConfig(repo_root=REPO_ROOT, output_dir=Path('/tmp/not-created-contract'), workers=3)
    for stage in production_stages(config):
        module = importlib.import_module('scripts.' + Path(stage.command[2]).stem)
        args = module.parse_args(list(stage.command[3:]))
        assert args.output_dir == stage.output_dir
        if stage.name in ('multiturn', 'tolerances'):
            assert args.workers == 3


def test_shell_adapter_from_other_directory(tmp_path):
    output = tmp_path / 'dry run with spaces'
    env = os.environ.copy()
    env['NKM_PYTHON'] = sys.executable
    done = subprocess.run(['bash', str(REPO_ROOT / 'scripts/run_full_production_simulation.sh'),
                           '--dry-run', '--workers', '2', '--output-dir', str(output), '--no-color'],
                          cwd=tmp_path, env=env, capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    assert 'Production planned' in done.stdout
    assert not output.exists()
    assert '--optimization-summary' in done.stdout


def test_notebook_in_clean_process():
    notebook = json.loads((REPO_ROOT / 'notebooks/04_full_production_simulation.ipynb').read_text())
    code = '\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code')
    code += '\nassert report["status"] == "planned"\nassert not config.output_dir.exists()\n'
    result = subprocess.run([sys.executable, '-B', '-c', code], cwd=REPO_ROOT / 'notebooks',
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('script,artifact', [
    ('inventory_protected_hashes.py', 'protected_files_manifest.json'),
    ('validate_nkm_fieldmap.py', 'fieldmap_validation_metrics.json'),
    ('run_tracking_convergence.py', 'tracking_convergence_summary.json')])
def test_small_stages_write_to_explicit_directory(tmp_path, script, artifact):
    output = tmp_path / 'output'
    result = subprocess.run([sys.executable, '-B', str(REPO_ROOT / 'scripts' / script),
                             '--output-dir', str(output)], cwd=tmp_path,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    data = json.loads((output / artifact).read_text())
    if script == 'inventory_protected_hashes.py':
        assert len(data['K4GSR_HBIv4-1.mat']) == 64


def test_subprocess_failure_reports_log(tmp_path):
    from nkm_injection.production import ProductionStage, _execute
    config = ProductionRunConfig(output_dir=tmp_path / 'failed', verbose=False)
    (config.output_dir / 'logs').mkdir(parents=True)
    stage = ProductionStage('child', 'Failing child',
        (sys.executable, '-c', "print('diagnostic'); raise SystemExit(7)"), config.output_dir, ())
    with pytest.raises(RuntimeError, match='status 7'):
        _execute(stage, config)
    assert 'diagnostic' in (config.output_dir / 'logs/child.log').read_text()


def test_tolerance_receives_current_strengths_targets_and_workers(publication_case, tmp_path, monkeypatch):
    import scripts.run_publication_tolerances as cli
    root, manifest = publication_case(delta=0.2)
    summary_path = root / manifest.bts_optimization_run / 'bts_optimization_summary.json'
    calls = []
    def evaluate(bts, target, samples, n_workers, **kwargs):
        calls.append((bts.quad_strengths_list, target, n_workers))
        metric = {'p50_median': 0.01, 'p68': 0.02, 'p95': 0.03, 'p99': 0.04,
                  'bootstrap_95ci_median': [0.005, 0.015]}
        return {'failure_probability': 0.0, 'mismatch_x': metric, 'mismatch_y': metric}
    monkeypatch.setattr(cli, 'evaluate_robustness_statistics', evaluate)
    monkeypatch.setattr(cli, 'sample_error_ensemble', lambda *args, **kwargs: [])
    monkeypatch.setattr(cli, 'compute_one_at_a_time_sensitivity', lambda *args, **kwargs: {})
    output = tmp_path / 'tolerance output'
    cli.main(['--optimization-summary', str(summary_path), '--output-dir', str(output), '--workers', '3'])
    assert calls[0][0][0] == pytest.approx(0.648572, abs=1e-12)
    assert calls[0][1]['beta'][0] == pytest.approx(2.6, abs=1e-12)
    assert calls[0][2] == 3
    saved = json.loads((output / 'publication_tolerances_summary.json').read_text())
    assert saved['optimization_source']['path'] == str(summary_path.resolve())


def test_injection_lattice_path_is_local(tmp_path, monkeypatch):
    import scripts.run_multiturn_injection as cli
    seen = []
    def stop_after_configuration(config):
        seen.append(config.mat_filename)
        raise RuntimeError('configuration checked')
    monkeypatch.setattr(cli, 'load_storage_ring_injection_lattice', stop_after_configuration)
    with pytest.raises(RuntimeError, match='configuration checked'):
        cli.main(['--tier', 'smoke', '--output-dir', str(tmp_path)])
    assert Path(seen[0]) == tmp_path / 'storage_ring_lattice_nkm.mat'


def test_moga_lattice_configuration_is_forwarded(tmp_path, monkeypatch):
    from types import SimpleNamespace
    import scripts.run_publication_moga as cli
    seen = []
    result = SimpleNamespace(success=True, representative_solutions={}, feasible_fraction=1.0,
                             pareto_x=[], history_hypervolume=[], runtime_seconds=0.0)
    monkeypatch.setattr(cli, 'run_bts_moga', lambda cfg: result)
    monkeypatch.setattr(cli, 'reevaluate_pareto_finalists',
                        lambda res, **kwargs: seen.append(kwargs['ring_config']))
    monkeypatch.setattr(cli, 'save_moga_results_json', lambda *args: None)
    cli.main(['--output-dir', str(tmp_path)])
    assert len(seen) == 5
    assert all(Path(cfg.mat_filename) == tmp_path / 'storage_ring_lattice_nkm.mat' for cfg in seen)


def test_pdf_build_cannot_write_to_manuscript_sources(publication_case, tmp_path, monkeypatch):
    import nkm_injection.paper as paper
    root, manifest = publication_case()
    source = root / 'docs/jinst-paper'
    (source / 'figures').mkdir(parents=True)
    (source / 'paper.tex').write_text('mock manuscript')
    (source / 'paper.pdf').write_bytes(b'old compiled PDF')
    (source / 'figures/reference.pdf').write_bytes(b'reference figure')
    before = {p: p.read_bytes() for p in source.rglob('*') if p.is_file()}
    output = tmp_path / 'custom publication'
    commands = []
    monkeypatch.setattr(shutil, 'which', lambda name: '/bin/true')
    def compile_fake(cmd, cwd, **kwargs):
        commands.append((cmd, cwd))
        assert Path(cwd).is_relative_to(output)
        assert (Path(cwd) / 'figures/reference.pdf').is_file()
        (Path(cwd) / 'paper.pdf').write_bytes(b'new compiled PDF')
        return subprocess.CompletedProcess(cmd, 0)
    monkeypatch.setattr(subprocess, 'run', compile_fake)
    summary = paper.run_paper_pipeline(root, manifest=manifest, output_dir=output, compile_pdf=True,
                                       create_if_missing=False)
    assert summary['pdf_compiled']
    assert commands
    assert (output / 'paper.pdf').read_bytes() == b'new compiled PDF'
    assert all(p.read_bytes() == raw for p, raw in before.items())
