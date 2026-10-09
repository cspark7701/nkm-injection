"""Publication lifecycle regressions use temporary source and result trees."""
import json
from pathlib import Path
import subprocess

import pytest

from nkm_injection.results_schema import (
    initialize_publication_manifest, validate_publication_manifest,
)
from nkm_injection.publication_build import build_publication_pdf


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            if p.is_file() else None for p in root.rglob('*')}


@pytest.mark.parametrize('fault', ['none', 'missing_baseline', 'empty_baseline',
                                  'bad_digest', 'missing_artifact', 'malformed_artifact'])
def test_validation_is_strict_and_read_only(publication_case, fault):
    root, manifest = publication_case()
    baseline = root / manifest.input_hash_manifest
    artifact = root / manifest.injection_run / 'injection_metrics_summary.json'
    if fault == 'missing_baseline':
        baseline.unlink()
    elif fault == 'empty_baseline':
        baseline.write_text('{}')
    elif fault == 'bad_digest':
        data = json.loads(baseline.read_text())
        data['By.txt'] = '0' * 64
        baseline.write_text(json.dumps(data))
    elif fault == 'missing_artifact':
        artifact.unlink()
    elif fault == 'malformed_artifact':
        artifact.write_text('{invalid')
    before = snapshot(root)
    report = validate_publication_manifest(manifest, root)
    assert report['valid'] == (fault == 'none')
    assert bool(report['verified_runs']) == report['valid']
    if report['valid']:
        assert len(report['upstream_artifacts']['artifacts']) == 7
    assert snapshot(root) == before
    with pytest.raises(ValueError, match='read-only'):
        validate_publication_manifest(manifest, root, create_if_missing=True)
    assert snapshot(root) == before


def test_explicit_initialization_does_not_validate_empty_runs(publication_case):
    root, manifest = publication_case()
    import shutil
    shutil.rmtree(root / 'results')
    report = initialize_publication_manifest(manifest, root)
    assert report['baseline_created']
    assert len(report['created_run_directories']) == 6
    assert not report['stage_artifacts_verified']
    before = snapshot(root)
    assert not validate_publication_manifest(manifest, root)['valid']
    assert snapshot(root) == before
    assert not initialize_publication_manifest(manifest, root)['baseline_created']
    (root / 'By.txt').write_text('changed')
    before = snapshot(root)
    with pytest.raises(ValueError, match='Hash mismatch'):
        initialize_publication_manifest(manifest, root)
    assert snapshot(root) == before


def test_missing_inputs_cannot_initialize(publication_case):
    root, manifest = publication_case()
    (root / manifest.input_hash_manifest).unlink()
    (root / 'By.txt').unlink()
    before = snapshot(root)
    with pytest.raises(FileNotFoundError, match='missing scientific inputs'):
        initialize_publication_manifest(manifest, root)
    assert snapshot(root) == before


@pytest.mark.parametrize('failed_step', [1, 2, 3, 4, None, 'missing_pdf', 'missing_tool'])
def test_pdf_commands_and_fresh_artifact_determine_success(tmp_path, monkeypatch, failed_step):
    source = tmp_path / 'manuscript'
    source.mkdir()
    (source / 'paper.tex').write_text('manuscript')
    (source / 'paper.pdf').write_bytes(b'stale PDF')
    (source / 'reference.pdf').write_bytes(b'reference figure')
    (source / 'paper.aux').write_text('stale auxiliary')
    tables = tmp_path / 'tables'
    tables.mkdir()
    (tables / 'table.tex').write_text('new table')
    run = tmp_path / 'run'
    run.mkdir()
    before = snapshot(source)
    calls = []
    def execute(command, cwd, stdout, stderr, check):
        calls.append(command)
        assert Path(cwd) == run / 'build'
        assert not (Path(cwd) / 'paper.aux').exists()
        if failed_step == 'missing_tool':
            raise FileNotFoundError('tool missing')
        stdout.write('command diagnostics\n')
        if failed_step != 'missing_pdf':
            (Path(cwd) / 'paper.pdf').write_bytes(b'new PDF')
        return subprocess.CompletedProcess(command, 1 if len(calls) == failed_step else 0)
    monkeypatch.setattr('nkm_injection.publication_build.subprocess.run', execute)
    report = build_publication_pdf(source, run, [], tables)
    assert (report['status'] == 'completed') == (failed_step is None)
    assert (run / 'paper.pdf').exists() == (failed_step is None)
    assert len(calls) == (failed_step if isinstance(failed_step, int) else
                          1 if failed_step == 'missing_tool' else 4)
    assert json.loads((run / 'pdf_build.json').read_text()) == report
    assert all(Path(record['log_path']).is_file() for record in report['commands'])
    assert 'paper.pdf' not in report['input_sha256']
    assert (run / 'build/reference.pdf').read_bytes() == b'reference figure'
    assert (run / 'build/table.tex').read_text() == 'new table'
    assert snapshot(source) == before


def test_cli_validation_and_initialization(publication_case, monkeypatch):
    from scripts import reproduce_paper as cli
    root, manifest = publication_case()
    path = root / 'manifest.json'
    manifest.save(path)
    monkeypatch.setattr(cli, 'repo_root', root)
    before = snapshot(root)
    cli.main(['--manifest', str(path), '--validate-only'])
    assert snapshot(root) == before
    baseline = root / manifest.input_hash_manifest
    baseline.unlink()
    before = snapshot(root)
    with pytest.raises(SystemExit) as exc:
        cli.main(['--manifest', str(path), '--validate-only'])
    assert exc.value.code == 1
    assert snapshot(root) == before
    cli.main(['--manifest', str(path), '--initialize'])
    assert baseline.is_file()
    with pytest.raises(FileNotFoundError):
        cli.main(['--manifest', str(root / 'missing.json'), '--validate-only'])


def test_cli_reports_requested_pdf_failure(monkeypatch, capsys):
    from scripts import reproduce_paper as cli
    monkeypatch.setattr(cli, 'run_paper_pipeline', lambda **kw: {
        'pdf_compiled': False, 'pdf_build': {'error': 'bibtex exited with code 1'}})
    with pytest.raises(SystemExit) as exc:
        cli.main([])
    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert 'bibtex exited with code 1' in output
    assert 'Completed Successfully' not in output


def test_default_pipeline_build_is_isolated(publication_case, monkeypatch):
    from nkm_injection.paper import run_paper_pipeline
    root, manifest = publication_case()
    source = root / 'docs/jinst-paper'
    source.mkdir(parents=True)
    (source / 'paper.tex').write_text('manuscript')
    (source / 'paper.pdf').write_bytes(b'stale')
    before = snapshot(source)
    monkeypatch.setattr('nkm_injection.paper.generate_paper_tables', lambda *a, **kw: {})
    monkeypatch.setattr('nkm_injection.paper.generate_paper_figures', lambda *a, **kw: [])
    def execute(command, cwd, **kwargs):
        assert Path(cwd) == root / 'results/paper/isolated/build'
        (Path(cwd) / 'paper.pdf').write_bytes(b'new')
        return subprocess.CompletedProcess(command, 0)
    monkeypatch.setattr('nkm_injection.publication_build.subprocess.run', execute)
    summary = run_paper_pipeline(root, 'isolated', manifest=manifest, compile_pdf=True)
    assert summary['pdf_compiled']
    assert Path(summary['pdf_path']).read_bytes() == b'new'
    assert snapshot(source) == before
    before = snapshot(root)
    with pytest.raises(ValueError, match='new or empty'):
        run_paper_pipeline(root, 'isolated', manifest=manifest)
    assert snapshot(root) == before


@pytest.mark.parametrize('destination', ['selected_run', 'manuscript', 'occupied'])
def test_pipeline_rejects_output_collisions(publication_case, destination):
    from nkm_injection.paper import run_paper_pipeline
    root, manifest = publication_case()
    output = root / {'selected_run': manifest.injection_run,
                     'manuscript': 'docs/jinst-paper', 'occupied': 'old_output'}[destination]
    output.mkdir(parents=True, exist_ok=True)
    (output / 'existing.txt').write_text('preserve')
    before = snapshot(root)
    with pytest.raises(ValueError, match='separate|new or empty'):
        run_paper_pipeline(root, 'collision', manifest=manifest, output_dir=output)
    assert snapshot(root) == before


def test_incomplete_baseline_identifies_missing_input_and_selected_path(publication_case):
    root, manifest = publication_case()
    path = root / manifest.input_hash_manifest
    data = json.loads(path.read_text())
    del data['K4GSR_HBIv4-1.mat']
    path.write_text(json.dumps(data))
    before = snapshot(root)
    report = validate_publication_manifest(manifest, root)
    assert not report['valid']
    assert 'missing: K4GSR_HBIv4-1.mat' in report['errors'][0]
    assert str(path) in report['errors'][0]
    assert '--input-hash-manifest' in report['errors'][0]
    assert snapshot(root) == before


@pytest.mark.parametrize('absolute', [False, True])
def test_explicit_complete_baseline_override_generates_paper(publication_case, absolute):
    from scripts import reproduce_paper as cli
    root, manifest = publication_case()
    old = root / manifest.input_hash_manifest
    complete = root / 'results/new baseline/protected_files_manifest.json'
    complete.parent.mkdir()
    complete.write_bytes(old.read_bytes())
    incomplete = json.loads(old.read_text()); del incomplete['K4GSR_HBIv4-1.mat']
    old.write_text(json.dumps(incomplete))
    selected = root / 'selected.json'; manifest.save(selected)
    before = snapshot(root)
    override = complete if absolute else complete.relative_to(root)
    args = ['--repo-root', str(root), '--manifest', str(selected),
            '--input-hash-manifest', str(override)]
    cli.main(args + ['--validate-only'])
    assert snapshot(root) == before
    output = root / 'results/new paper'
    cli.main(args + ['--no-pdf', '--output-dir', str(output)])
    saved = json.loads((output / 'publication_manifest.json').read_text())
    assert saved['input_hash_manifest'] == str(override)
    metrics = json.loads((output / 'metrics.json').read_text())
    assert metrics['input_hashes_verified'] and metrics['manifest_valid']
    assert metrics['tables_count'] == 7 and metrics['figures_count'] == 4
    assert all(snapshot(root)[p] == value for p, value in before.items())


def test_baseline_override_does_not_accept_mismatched_hashes(publication_case):
    from scripts import reproduce_paper as cli
    root, manifest = publication_case()
    selected = root / 'selected.json'; manifest.save(selected)
    baseline = root / 'bad baseline.json'
    data = json.loads((root / manifest.input_hash_manifest).read_text()); data['By.txt'] = '0' * 64
    baseline.write_text(json.dumps(data))
    before = snapshot(root)
    with pytest.raises(SystemExit) as error:
        cli.main(['--repo-root', str(root), '--manifest', str(selected), '--validate-only',
                  '--input-hash-manifest', str(baseline)])
    assert error.value.code == 1
    assert snapshot(root) == before


def test_generation_reports_missing_selected_manifest(tmp_path, capsys):
    from scripts import reproduce_paper as cli
    output = tmp_path / 'publication'
    with pytest.raises(SystemExit) as error:
        cli.main(['--manifest', str(tmp_path / 'missing.json'), '--no-pdf',
                  '--output-dir', str(output)])
    assert error.value.code == 1
    assert '[ERROR] Paper reproduction pipeline failed:' in capsys.readouterr().out
    assert not output.exists()


def test_bundled_manifest_selects_versioned_complete_baseline():
    from nkm_injection.results_schema import PublicationManifest, compute_input_data_hashes
    root = Path(__file__).resolve().parents[1]
    manifest = PublicationManifest.load(root / 'config/publication_manifest.json')
    baseline = root / manifest.input_hash_manifest
    assert baseline.parent == root / 'config'
    assert json.loads(baseline.read_text()) == compute_input_data_hashes(root)
