"""Selected-run publication contracts, data sensitivity and source immutability."""
import hashlib
import json

import numpy as np
import pytest

from nkm_injection.publication_inputs import load_publication_inputs
from nkm_injection.paper import run_paper_pipeline, generate_paper_tables


def test_selected_manifest_changes_tables_and_figure_data(publication_case, monkeypatch):
    from matplotlib.axes import Axes
    plotted_apertures = []
    axhline = Axes.axhline
    def capture_aperture(self, y=0, *args, **kwargs):
        plotted_apertures.append(y)
        return axhline(self, y, *args, **kwargs)
    monkeypatch.setattr(Axes, 'axhline', capture_aperture)
    outputs = []
    for name, delta in [('first', 0.0), ('second', 0.2)]:
        root, manifest = publication_case(name, delta)
        upstream = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
        summary = run_paper_pipeline(root, name, manifest=manifest, create_if_missing=False)
        output = root / 'results/paper' / name
        assert summary['tables_count'] == 7
        assert summary['figures_count'] == 4
        assert all(p.read_bytes() == raw for p, raw in upstream.items())
        provenance = json.loads((output / 'upstream_artifacts.json').read_text())
        assert len(provenance['artifacts']) == 7
        for artifact in provenance['artifacts'].values():
            from pathlib import Path
            assert hashlib.sha256(Path(artifact['path']).read_bytes()).hexdigest() == artifact['sha256']
        data = json.loads((output / 'figures/figure_data.json').read_text())
        assert data['strengths_m_inv2'][0] == pytest.approx(0.448572 + delta, abs=1e-12)
        assert data['injection'][0]['capture'] == pytest.approx(0.9 + delta * 0.1, abs=1e-12)
        assert data['tolerance']['mismatch_x_median'] == pytest.approx(0.001 + delta, abs=1e-12)
        assert data['moga'][0]['pareto_count'] == 20 + int(delta * 10)
        assert data['convergence'][0]['reference_xp_rad'] == pytest.approx((-5.4 + delta + 0.1) * 1e-3, abs=1e-12)
        assert data['source'] == 'Selected optimized run'
        assert plotted_apertures[-2:] == pytest.approx([20.0 + delta, -20.0 - delta], abs=1e-12)
        tables = {p.name: p.read_text() for p in (output / 'tables').glob('*.md')}
        assert f'{0.448572 + delta:+.4f}' in tables['table2_quad_strengths.md']
        assert '[-2.5000, +2.5000]' in tables['table2_quad_strengths.md']
        assert f'{2.4 + delta:.4f}' in tables['table3_optics_comparison.md']
        assert f'{0.9 + delta * 0.1:.6f}' in tables['table4_injection.md']
        assert f'{0.01 + delta:.6f}' in tables['table5_tolerances.md']
        assert str(20 + int(delta * 10)) in tables['table6_moga.md']
        assert f'{0.15 + delta:.8g}' in tables['table7_validation.md']
        outputs.append((tables, data))
    for name in outputs[0][0]:
        assert outputs[0][0][name] != outputs[1][0][name]
    assert not np.allclose(outputs[0][1]['beta_m'], outputs[1][1]['beta_m'], rtol=1e-8, atol=1e-10)
    assert not np.allclose(outputs[0][1]['envelope_x_m'], outputs[1][1]['envelope_x_m'], rtol=1e-8, atol=1e-10)


@pytest.mark.parametrize('stage,filename', [
    ('field_validation_run', 'fieldmap_validation_metrics.json'),
    ('tracking_convergence_run', 'tracking_convergence_summary.json'),
    ('bts_optimization_run', 'config.json'),
    ('bts_optimization_run', 'bts_optimization_summary.json'),
    ('injection_run', 'injection_metrics_summary.json'),
    ('tolerance_run', 'publication_tolerances_summary.json'),
    ('moga_run', 'multi_seed_moga_summary.json')])
def test_missing_artifact_rejected(publication_case, stage, filename):
    root, manifest = publication_case()
    (root / getattr(manifest, stage) / filename).unlink()
    with pytest.raises(ValueError, match=filename.replace('.', r'\.')):
        run_paper_pipeline(root, 'missing', manifest=manifest, create_if_missing=False)
    assert not (root / 'results/paper/missing').exists()


@pytest.mark.parametrize('stage,filename,mutate,error', [
    ('field_validation_run', 'fieldmap_validation_metrics.json',
     lambda x: x['1d_fieldmap_validation'].update(peak_by_T=float('nan')), 'finite'),
    ('field_validation_run', 'fieldmap_validation_metrics.json',
     lambda x: x['2d_kickmap_validation']['lorentz_kick_test'].update(sign_verified=False), 'sign'),
    ('tracking_convergence_run', 'tracking_convergence_summary.json',
     lambda x: x['results'][1].update(n_slices=10), 'unique'),
    ('bts_optimization_run', 'config.json', lambda x: x.pop('target_config'), 'target_config'),
    ('bts_optimization_run', 'config.json', lambda x: x.update(publication_input_schema_version=2), 'unsupported'),
    ('bts_optimization_run', 'config.json', lambda x: x['bts_config'].pop('energy_eV'), 'incomplete'),
    ('bts_optimization_run', 'bts_optimization_summary.json',
     lambda x: x.update(optimized_strengths_raw=[0.0]), 'nine'),
    ('bts_optimization_run', 'bts_optimization_summary.json',
     lambda x: x.update(constraints_satisfied=False), 'feasible'),
    ('bts_optimization_run', 'bts_optimization_summary.json',
     lambda x: x.update(final_mismatch_x=-1e-3), '>='),
    ('injection_run', 'injection_metrics_summary.json',
     lambda x: x[0].update(capture_mean=1.1), '<='),
    ('injection_run', 'injection_metrics_summary.json',
     lambda x: x[0].update(capture_ci_lo=0.95), 'confidence'),
    ('injection_run', 'injection_metrics_summary.json',
     lambda x: x[0].update(stored_centroid_osc_mm=float('inf')), 'finite'),
    ('tolerance_run', 'publication_tolerances_summary.json',
     lambda x: x['robustness_statistics']['mismatch_x'].pop('p50_median'), 'p50_median'),
    ('moga_run', 'multi_seed_moga_summary.json',
     lambda x: x['seed_metrics']['seed_42'].update(pareto_count=1.5), 'integer')])
def test_malformed_metrics_rejected(publication_case, stage, filename, mutate, error):
    root, manifest = publication_case()
    path = root / getattr(manifest, stage) / filename
    data = json.loads(path.read_text())
    mutate(data)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match=error):
        load_publication_inputs(manifest, root)


def test_no_survivors_remains_unavailable(publication_case):
    root, manifest = publication_case()
    path = root / manifest.injection_run / 'injection_metrics_summary.json'
    data = json.loads(path.read_text())
    data[0].update(capture_mean=0.0, capture_ci_lo=0.0, capture_ci_hi=0.0,
                   stored_centroid_osc_mm=float('nan'))
    path.write_text(json.dumps(data))
    inputs = load_publication_inputs(manifest, root)
    assert inputs.injection[0].stored_oscillation_m is None
    tables = generate_paper_tables(root, root / 'results/tables', inputs)
    assert 'Unavailable (no survivors)' in tables['table4']


def test_reference_generation_is_labelled(tmp_path):
    tables = generate_paper_tables(tmp_path, tmp_path / 'reference')
    assert all('Nominal reference' in value for value in tables.values())


def test_mismatch_roundoff_has_explicit_tolerance(publication_case):
    root, manifest = publication_case()
    path = root / manifest.bts_optimization_run / 'bts_optimization_summary.json'
    data = json.loads(path.read_text())
    data['final_mismatch_x'] = -2e-16
    path.write_text(json.dumps(data))
    inputs = load_publication_inputs(manifest, root)
    assert inputs.optimization.mismatch_x == 0.0
    assert inputs.provenance()['validation_tolerances']['mismatch_roundoff'] == 1e-12


def test_pipeline_in_fresh_python_process(publication_case):
    import subprocess
    import sys
    from pathlib import Path
    root, manifest = publication_case()
    manifest_path = root / 'manifest.json'
    manifest.save(manifest_path)
    code = """
import sys
from pathlib import Path
from nkm_injection.paper import run_paper_pipeline
summary = run_paper_pipeline(Path(sys.argv[1]), 'fresh_process',
                             manifest=Path(sys.argv[2]), create_if_missing=False)
assert summary['tables_count'] == 7
assert summary['figures_count'] == 4
"""
    completed = subprocess.run([sys.executable, '-c', code, str(root), str(manifest_path)],
                               cwd=Path(__file__).resolve().parent.parent,
                               capture_output=True, text=True, timeout=60)
    assert completed.returncode == 0, completed.stderr
    assert (root / 'results/paper/fresh_process/upstream_artifacts.json').is_file()


def test_stored_beam_absence_is_independent_of_injected_capture(publication_case):
    root, manifest = publication_case()
    path = root / manifest.injection_run / 'injection_metrics_summary.json'
    data = json.loads(path.read_text())
    data[0].update(capture_mean=.8, capture_ci_lo=.7, capture_ci_hi=.9,
                   stored_centroid_osc_mm=None)
    path.write_text(json.dumps(data, allow_nan=False))
    inputs = load_publication_inputs(manifest, root)
    assert inputs.injection[0].capture == .8
    assert inputs.injection[0].stored_oscillation_m is None
