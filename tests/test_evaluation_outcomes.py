"""Scientific infeasibility must be distinguishable from missing evaluation data."""
import json
from pathlib import Path
from unittest.mock import patch

import at
import numpy as np
import pytest

from nkm_injection import objectives as objective_module
from nkm_injection import optimization as optimization_module
from nkm_injection import robust_optimization as robust
from nkm_injection.bts_lattice import BTSConfig
from nkm_injection.concurrency import parallel_map
from nkm_injection.errors import sample_error_ensemble
from nkm_injection.evaluation import EvaluationExecutionError
from nkm_injection.objectives import BTSNormalizedObjectives, OpticsTargetConfig
from nkm_injection.storage_ring_injection import track_element_resolved_injection

TARGET = {"beta": [2.336495, 4.256241], "alpha": [-.016335, .017772]}
MAP = Path(__file__).resolve().parents[1] / 'kickmap_file.txt'


def good_prop():
    return {"final_beta": TARGET['beta'], "final_alpha": TARGET['alpha'],
            "final_dispersion": [0., 0., 0., 0.], "max_beta_x": 10., "max_beta_y": 10.}


def numerical_worker(args):
    """Inject a known numerical error inside each spawned worker."""
    with patch.object(robust, 'compute_twiss_propagation', side_effect=np.linalg.LinAlgError('singular optics')):
        return robust._eval_single_robustness_sample(args)


def unexpected_capture(*args):
    raise TypeError('broken capture callback')


@pytest.mark.parametrize('workers', [1, 2])
def test_missing_map_is_a_contextual_error_never_linear(tmp_path, workers):
    samples = sample_error_ensemble(n_samples=2, seed=42)
    samples[0]['sample_id'] = 'missing-map-17'
    with pytest.raises(RuntimeError, match="Sample 'missing-map-17'.*fieldmap.*model_setup.*FileNotFoundError") as error:
        robust.evaluate_robustness_statistics(BTSConfig(), TARGET, samples,
            n_workers=workers, kickmap_path=tmp_path/'missing.txt')
    assert error.value.__cause__ is not None


@pytest.mark.parametrize('workers', [1, 2])
def test_domain_failures_have_null_metrics_and_identical_sample_identity(workers):
    samples = sample_error_ensemble(n_samples=2, seed=42)
    for index, sample in enumerate(samples):
        sample['sample_id'] = f'domain-{index}'
        sample['ring_co_x_m'] = 1.0
    stats = robust.evaluate_robustness_statistics(BTSConfig(), TARGET, samples, n_workers=workers)
    assert stats['n_invalid_evaluations'] == 2
    assert stats['n_valid_evaluations'] == 0
    assert stats['invalid_evaluation_fraction'] == 1
    assert stats['failure_probability'] is None
    assert stats['feasible_fraction'] == 0
    assert stats['mismatch_x']['p50'] is None
    assert stats['failure_modes'] == {'beta_exceeded': 0, 'mismatch_exceeded': 0, 'capture_failed': 0}
    for index, result in enumerate(stats['sample_results']):
        outcome = result['outcome']
        assert outcome['status'] == 'invalid'
        assert outcome['identity']['sample_id'] == f'domain-{index}'
        assert outcome['exception']['type'] == 'OutOfDomainError'
        assert outcome['exception']['phase'] == 'stored_beam_kick'
        assert outcome['model_provenance']['kicker_model'] == 'fieldmap'
        assert len(outcome['model_provenance']['map_sha256']) == 64
        assert result['mx'] is None and result['stored_kick_mrad'] is None
        assert not result['failed']
    json.dumps(stats, allow_nan=False)


@pytest.mark.parametrize('workers', [1, 2])
def test_failed_optics_has_numeric_diagnostic_in_serial_and_parallel(workers):
    samples = sample_error_ensemble(n_samples=2, seed=42)
    args = [(BTSConfig(), s, TARGET, None, 'fieldmap', MAP) for s in samples]
    results = parallel_map(numerical_worker, args, n_workers=workers)
    for index, result in enumerate(results):
        assert result['outcome']['identity']['sample_id'] == index
        assert result['outcome']['status'] == 'invalid'
        assert result['outcome']['exception'] == {'type': 'LinAlgError', 'message': 'singular optics', 'phase': 'optics'}
        assert result['failure_mode'] is None


@pytest.mark.parametrize('workers', [1, 2])
def test_unexpected_worker_error_propagates_with_sample_and_phase(workers):
    samples = sample_error_ensemble(n_samples=2, seed=42)
    with pytest.raises(RuntimeError, match="Sample 0.*fieldmap.*capture.*TypeError.*broken capture"):
        robust.evaluate_robustness_statistics(BTSConfig(), TARGET, samples,
            capture_efficiency_fn=unexpected_capture, n_workers=workers)


def test_aggregation_separates_invalid_from_physical_infeasibility(monkeypatch):
    samples = sample_error_ensemble(n_samples=4, seed=42)
    samples[2]['ring_co_x_m'] = 1.0
    monkeypatch.setattr(robust, 'apply_sample_errors', lambda config, s: (s['sample_id'], {}))
    def prop(sample_id, twiss):
        if sample_id == 3:
            raise FloatingPointError('failed optics')
        result = good_prop()
        if sample_id == 1:
            result['max_beta_x'] = 100.
            result['final_alpha'] = [10., 10.]
        return result
    monkeypatch.setattr(robust, 'compute_twiss_propagation', prop)
    stats = robust.evaluate_robustness_statistics(BTSConfig(), TARGET, samples)
    assert stats['n_valid_evaluations'] == 2
    assert stats['n_invalid_evaluations'] == 2
    assert stats['failure_probability'] == .5
    assert stats['feasible_fraction'] == .25
    assert stats['failure_modes']['beta_exceeded'] == 1
    assert stats['failure_modes']['mismatch_exceeded'] == 1
    assert [r['outcome']['status'] for r in stats['sample_results']] == ['valid', 'infeasible', 'invalid', 'invalid']
    assert stats['max_beta_x_m']['p50'] == 55.
    assert stats['convergence_check']['status'] == 'blocked_invalid_evaluations'
    assert stats['convergence_check']['converged'] is None
    json.dumps(stats, allow_nan=False)


@pytest.mark.parametrize('model', ['off', 'ideal', 'linear'])
def test_alternate_model_requires_explicit_selection_and_is_disclosed(tmp_path, model):
    samples = sample_error_ensemble(n_samples=1, seed=42)
    stats = robust.evaluate_robustness_statistics(BTSConfig(), TARGET, samples,
        kicker_model=model, kickmap_path=tmp_path/'missing.txt')
    provenance = stats['sample_results'][0]['outcome']['model_provenance']
    assert provenance['kicker_model'] == model
    assert provenance['map_path'] is None
    assert 'map_sha256' not in provenance
    assert stats['n_invalid_evaluations'] == 0


@pytest.mark.parametrize('error', [FloatingPointError('unstable'), np.linalg.LinAlgError('singular')])
def test_normalized_penalty_has_candidate_context(monkeypatch, error):
    obj = BTSNormalizedObjectives()
    monkeypatch.setattr(objective_module, 'compute_twiss_propagation', lambda *args: (_ for _ in ()).throw(error))
    np.testing.assert_array_equal(obj.compute_residual_vector(obj.nominal_strengths), np.full(6, 1e4))
    assert obj.last_outcome.status == 'invalid'
    assert obj.last_outcome.exception['message'] == str(error)
    assert obj.last_outcome.identity['strengths_m_minus2'] == obj.nominal_strengths.tolist()


@pytest.mark.parametrize('error', [TypeError('bug'), KeyError('missing key'), ValueError('bad config'), RuntimeError('bug'), at.AtError('ambiguous backend error')])
def test_unexpected_objective_and_optimizer_errors_propagate(monkeypatch, error):
    obj = BTSNormalizedObjectives()
    def fail(*args):
        raise error
    monkeypatch.setattr(objective_module, 'compute_twiss_propagation', fail)
    with pytest.raises(type(error)):
        obj.compute_residual_vector(obj.nominal_strengths)
    assert obj.last_outcome is None
    monkeypatch.setattr(optimization_module, 'compute_twiss_propagation', fail)
    deterministic = optimization_module.DeterministicObjective()
    with pytest.raises(type(error)):
        deterministic.evaluate(deterministic.nominal_strengths)
    with pytest.raises(type(error)):
        optimization_module.optimize_bts_quadrupoles(config=optimization_module.BTSOptimizationConfig(max_iter=2))


def test_nonfinite_outputs_are_invalid_and_configuration_is_rejected(monkeypatch):
    obj = BTSNormalizedObjectives()
    result = good_prop(); result['final_beta'] = [np.nan, 1.]
    monkeypatch.setattr(objective_module, 'compute_twiss_propagation', lambda *args: result)
    obj.compute_residual_vector(obj.nominal_strengths)
    assert obj.last_outcome.exception['type'] == 'NumericalEvaluationError'
    with pytest.raises(ValueError, match='nine'):
        obj.compute_residual_vector([1, 2])
    with pytest.raises(ValueError, match='finite'):
        BTSNormalizedObjectives(OpticsTargetConfig(sigma_beta_x=np.nan))


class MissingPositionsRing(list):
    def get_s_pos(self):
        raise NotImplementedError('positions unavailable')


def test_unknown_loss_position_is_null_and_error_is_preserved():
    ring = MissingPositionsRing([at.Drift('DRIFT', 1.)])
    beam = np.zeros((6, 1)); beam[0] = .1
    result = track_element_resolved_injection(beam, ring, n_turns=1, kicker_model='off')
    assert result.loss_log[0]['s_position_m'] is None
    assert result.loss_log[0]['element_index'] == 0
    assert not result.metadata['loss_positions_complete']
    assert result.metadata['loss_position_exception']['type'] == 'NotImplementedError'


def test_unexpected_loss_position_error_propagates():
    class BrokenRing(list):
        def get_s_pos(self):
            raise TypeError('broken lattice')
    with pytest.raises(TypeError, match='broken lattice'):
        track_element_resolved_injection(np.zeros((6, 1)), BrokenRing(), kicker_model='off')


def test_publication_rejects_incomplete_tolerance_evaluations(publication_case):
    from nkm_injection.publication_inputs import load_publication_inputs
    root, manifest = publication_case('invalid-evaluations')
    path = root / manifest.tolerance_run / 'publication_tolerances_summary.json'
    raw = json.loads(path.read_text())
    raw['robustness_statistics']['n_invalid_evaluations'] = 1
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match='zero invalid evaluations'):
        load_publication_inputs(manifest, root)


def test_invalid_candidate_outcome_is_saved_with_start_identity(monkeypatch):
    def fail(*args):
        raise FloatingPointError('numerical propagation failed')
    monkeypatch.setattr(objective_module, 'compute_twiss_propagation', fail)
    monkeypatch.setattr(optimization_module, 'compute_twiss_propagation', fail)
    result = optimization_module.optimize_bts_quadrupoles(
        config=optimization_module.BTSOptimizationConfig(max_iter=2))
    record = result.candidate_table[0].as_dict()
    assert not record['physically_feasible']
    assert record['evaluation_outcome']['status'] == 'invalid'
    assert record['evaluation_outcome']['identity']['start_idx'] == 0
    assert record['evaluation_outcome']['identity']['seed'] == record['seed']
    assert record['evaluation_outcome']['exception']['type'] == 'FloatingPointError'


def test_tolerance_cli_saves_invalid_diagnostics_and_stops(tmp_path, monkeypatch):
    from scripts import run_publication_tolerances as cli
    samples = sample_error_ensemble(n_samples=1, seed=42)
    samples[0]['ring_co_x_m'] = 1.
    stats = robust.evaluate_robustness_statistics(BTSConfig(), TARGET, samples)
    def evaluate(*args, **kwargs):
        assert kwargs['kicker_model'] == 'off'
        return stats
    monkeypatch.setattr(cli, 'repo_root', tmp_path)
    monkeypatch.setattr(cli, 'evaluate_robustness_statistics', evaluate)
    monkeypatch.setattr(cli, 'compute_one_at_a_time_sensitivity', lambda *a, **k: pytest.fail('OAT must not run on invalid ensemble'))
    output = tmp_path / 'results/new_results'
    with pytest.raises(RuntimeError, match=r'Invalid evaluations for samples \[0\]'):
        cli.main(['--reference', '--samples', '1', '--output-dir', str(output), '--kicker-model', 'off'])
    raw = json.loads((output/'publication_tolerances_summary.json').read_text())
    assert raw['robustness_statistics']['sample_results'][0]['outcome']['exception']['type'] == 'OutOfDomainError'
    assert raw['sensitivity_ranking'] == {}


def test_invalid_candidate_diagnostic_serializes_nonfinite_identity_as_null():
    obj = optimization_module.DeterministicObjective()
    result = obj.evaluate(np.full(9, np.nan))
    assert result['outcome']['identity']['strengths_m_minus2'] == [None] * 9
    json.dumps(result['outcome'], allow_nan=False)
