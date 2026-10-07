"""Isolated selected-run artifacts for publication integration tests."""
import json
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def publication_case(tmp_path):
    """Build complete run bundles without simulations or repository result writes."""
    from src.nkm_injection.bts_lattice import BTSConfig
    from src.nkm_injection.constraints import BTSConstraintConfig
    from src.nkm_injection.objectives import OpticsTargetConfig
    from src.nkm_injection.results_schema import PublicationManifest, compute_input_data_hashes

    def build(name='selected', delta=0.0):
        root = tmp_path / name
        root.mkdir()
        for filename in ('By.txt', 'kickmap_file.txt', 'K4GSR_HBIv4-1.mat',
                         'nkm_field.xlsx', 'nkm_field_expanded.xlsx'):
            (root / filename).write_bytes(b'synthetic hash-only input ' + filename.encode())
        manifest = PublicationManifest(**{stage: f'results/{stage}' for stage in (
            'field_validation_run', 'tracking_convergence_run', 'bts_optimization_run',
            'injection_run', 'tolerance_run', 'moga_run')})
        def save(stage, name, value):
            path = root / getattr(manifest, stage) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value))
        bts = BTSConfig(ap1_limit=0.02 + delta * 0.001)
        target = OpticsTargetConfig(target_beta_x=2.4 + delta)
        constraints = BTSConstraintConfig(emit_x_m=1e-7 * (1 + delta))
        strengths = bts.quad_strengths_list
        strengths[0] += delta
        save('bts_optimization_run', 'config.json', {
            'publication_input_schema_version': 1,
            'bts_config': bts.to_dict(), 'target_config': target.to_dict(),
            'constraint_config': constraints.to_dict(), 'quad_bounds_global': [-3.0, 3.0]})
        save('bts_optimization_run', 'bts_optimization_summary.json', {
            'success': True, 'constraints_satisfied': True,
            'optimized_strengths_raw': strengths, 'final_mismatch_x': 0.01 + delta,
            'final_mismatch_y': 0.02 + delta})
        save('field_validation_run', 'fieldmap_validation_metrics.json', {
            '1d_fieldmap_validation': {'valid': True, 'peak_by_T': 0.15 + delta,
                                       'odd_symmetry_residual_T': 1e-11},
            '2d_kickmap_validation': {'grid_interpolation_max_err': 0.0,
                                     'lorentz_kick_test': {'sign_verified': True}}})
        save('tracking_convergence_run', 'tracking_convergence_summary.json', {
            'recommended_production_slices': 40,
            'results': [{'n_slices': n, 'ref_xp_exit_mrad': -5.4 + delta + 1/n,
                         'inj_survival_fraction': 1.0} for n in (10, 40, 80)]})
        save('injection_run', 'injection_metrics_summary.json', [{
            'kicker_model': 'fieldmap', 'n_particles': 100, 'n_turns': 10, 'n_seeds': 3,
            'capture_mean': 0.9 + delta * 0.1, 'capture_ci_lo': 0.85,
            'capture_ci_hi': 0.99, 'capture_ci_level': 0.95,
            'stored_centroid_osc_mm': 0.006 + delta}])
        save('tolerance_run', 'publication_tolerances_summary.json', {
            'n_samples': 100, 'robustness_statistics': {
                'n_samples': 100, 'failure_probability': 0.01 + delta,
                'mismatch_x': {'p50_median': 0.001 + delta},
                'mismatch_y': {'p50_median': 0.002 + delta}}})
        save('moga_run', 'multi_seed_moga_summary.json', {
            'seeds': [42], 'seed_metrics': {'seed_42': {'success': True,
            'feasible_fraction': 1.0, 'pareto_count': 20 + int(delta * 10)}}})
        path = root / manifest.input_hash_manifest
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(compute_input_data_hashes(root)))
        return root, manifest
    return build
