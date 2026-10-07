"""Synthetic estimands and boundary counts, independent of expensive tracking."""
import json
import numpy as np
import pytest

from nkm_injection.statistics import (StatisticalPolicy, bootstrap_interval,
    check_prefix_stability, summarize_observations, summarize_robustness_results)
from nkm_injection.convergence_study import bootstrap_capture_ci
from nkm_injection import robust_optimization as robust
from nkm_injection.bts_lattice import BTSConfig


def outcome(value, status='valid'):
    return {'mx': value, 'my': value, 'bx_max': 10., 'by_max': 12.,
            'stored_kick_mrad': 0.1, 'eff': .9, 'failed': status == 'infeasible',
            'outcome': {'status': status, 'identity': {'sample_id': value},
                        'physical_failure_reasons': ['beta_exceeded'] if status == 'infeasible' else []}}


@pytest.mark.parametrize('count', [0, 9, 10, 49, 50, 99, 100, 150])
def test_exact_required_prefix_sizes(count):
    result = summarize_robustness_results([outcome(1.) for _ in range(count)],
                                        StatisticalPolicy(bootstrap_count=10))
    check = result['convergence_check']
    assert check['available_valid_samples'] == count
    if count < 100:
        assert check['status'] == 'insufficient_evidence'
        assert check['converged'] is None
        assert check['absolute_difference'] is None
        assert check['N_50_to_100_diff'] is None
    else:
        assert check['status'] == 'within_tolerance'
        assert check['converged'] is True
        assert check['absolute_difference'] == 0
    if count == 0:
        assert result['failure_probability'] is None
        assert result['feasible_fraction'] is None
        assert result['mismatch_x']['p50'] is None
        assert result['mismatch_x']['bootstrap_ci_median'] == [None, None]
    json.dumps(result, allow_nan=False)


def test_custom_prefix_sizes_threshold_and_larger_samples():
    policy = StatisticalPolicy(convergence_sizes=(2, 4), convergence_tolerance=.5)
    result = check_prefix_stability([0., 0., 1., 1., 100., 200.], policy)
    assert result['prefix_estimates'] == [0., .5]
    assert result['absolute_difference'] == .5
    assert result['converged'] is False  # strict less-than convention
    assert result['status'] == 'outside_tolerance'
    assert 'N_50_to_100_diff' not in result
    assert check_prefix_stability([0, 0, 1], policy)['status'] == 'insufficient_evidence'


def test_invalid_samples_excluded_and_physical_failures_retained():
    records = [outcome(1.), outcome(3., 'infeasible'), outcome(1e9, 'invalid')]
    policy = StatisticalPolicy(bootstrap_count=20, convergence_sizes=(1, 2))
    result = summarize_robustness_results(records, policy, capture_enabled=True)
    assert result['n_valid_evaluations'] == 2
    assert result['n_invalid_evaluations'] == 1
    assert result['n_physical_failures'] == 1
    assert result['n_physically_feasible'] == 1
    assert result['mismatch_x']['p50'] == 2
    assert result['failure_probability'] == .5
    assert result['feasible_fraction'] == pytest.approx(1/3)
    assert result['failure_modes']['beta_exceeded'] == 1
    assert result['convergence_check']['status'] == 'blocked_invalid_evaluations'
    assert result['convergence_check']['converged'] is None
    with pytest.raises(ValueError, match='invalid_sample_policy=raise'):
        summarize_robustness_results(records, StatisticalPolicy(invalid_sample_policy='raise'))
    all_bad = summarize_robustness_results([outcome(None, 'invalid')], policy)
    assert all_bad['mismatch_x']['mean'] is None
    assert all_bad['failure_probability'] is None


def test_known_distribution_and_deterministic_bootstrap():
    values = np.arange(1, 10, dtype=float)
    summary = summarize_observations(values)
    assert summary['mean'] == 5.
    assert summary['p50'] == 5.
    assert summary['p95'] == pytest.approx(8.6, abs=1e-14)
    result = bootstrap_interval(values, estimator='median', count=20, seed=17, ci_level=.8)
    assert result == bootstrap_interval(values, estimator='median', count=20, seed=17, ci_level=.8)
    # Independent reference resampling of the selected estimator.
    rng = np.random.default_rng(17)
    medians = [np.median(rng.choice(values, len(values), replace=True)) for _ in range(20)]
    expected = np.percentile(medians, [10., 90.])
    np.testing.assert_allclose([result['ci_lo'], result['ci_hi']], expected, atol=1e-14, rtol=0)
    assert result['settings']['estimator'] == 'median'
    constant = bootstrap_interval([3., 3., 3.], estimator='mean', count=10)
    assert constant['estimate'] == constant['ci_lo'] == constant['ci_hi'] == 3.
    singleton = bootstrap_interval([3.], estimator='median', count=10)
    assert singleton['status'] == 'descriptive_only'


def test_all_statistical_settings_saved_and_correct_aliases():
    policy = StatisticalPolicy(bootstrap_count=23, bootstrap_seed=11, ci_level=.8,
                               convergence_sizes=(2, 3), convergence_tolerance=.2)
    result = summarize_robustness_results([outcome(1), outcome(2), outcome(3)], policy)
    restored = StatisticalPolicy.from_dict({k: result['statistical_settings'][k] for k in policy.to_dict()})
    assert restored == policy
    settings = result['mismatch_x']['bootstrap']['settings']
    assert settings['count'] == 23 and settings['seed'] == 11 and settings['ci_level'] == .8
    assert 'bootstrap_95ci_median' not in result['mismatch_x']
    assert result['convergence_check']['sample_sizes'] == [2, 3]
    assert result['statistical_settings']['summary_std_ddof'] == 0
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize('kwargs', [{'bootstrap_count': 0}, {'bootstrap_count': 1.5},
    {'bootstrap_seed': -1}, {'bootstrap_seed': True}, {'ci_level': 0}, {'ci_level': 1},
    {'ci_level': np.nan}, {'convergence_sizes': (50, 50)}, {'convergence_sizes': (100, 50)},
    {'convergence_sizes': (0, 10)}, {'convergence_tolerance': -1},
    {'convergence_tolerance': np.inf}, {'invalid_sample_policy': 'penalty'}])
def test_policy_validation(kwargs):
    with pytest.raises(ValueError):
        StatisticalPolicy(**kwargs).validate()


@pytest.mark.parametrize('values', [[np.nan], [np.inf], [[1., 2.]]])
def test_nonfinite_and_wrong_shaped_observations_rejected(values):
    with pytest.raises(ValueError):
        bootstrap_interval(values, estimator='mean')


def test_capture_estimand_seed_settings_and_empty_samples():
    result = bootstrap_capture_ci([20, 80, 80], 100, n_bootstrap=30, ci_level=.8, bootstrap_seed=7)
    assert result == bootstrap_capture_ci([20, 80, 80], 100, n_bootstrap=30, ci_level=.8, bootstrap_seed=7)
    assert result['mean'] == pytest.approx(.6, abs=1e-14)
    assert result['bootstrap_settings']['estimator'] == 'mean'
    assert result['bootstrap_settings']['seed'] == 7
    assert result['bootstrap_settings']['resampling_unit'] == 'seed_run'
    empty = bootstrap_capture_ci([], 100, n_bootstrap=10)
    assert empty['status'] == 'insufficient_evidence'
    assert empty['mean'] is empty['ci_lo'] is empty['ci_hi'] is None
    single = bootstrap_capture_ci([80], 100, n_bootstrap=10)
    assert single['status'] == 'descriptive_only'
    assert single['std'] == 0.
    # External generator state, rather than a fabricated seed, is recorded.
    rng = np.random.default_rng(9)
    external = bootstrap_capture_ci([20, 80], 100, n_bootstrap=10, rng=rng)
    settings = external['bootstrap_settings']
    assert settings['seed'] is None
    replay = np.random.default_rng()
    replay.bit_generator.state = settings['rng_state_before']
    assert external == bootstrap_capture_ci([20, 80], 100, n_bootstrap=10, rng=replay)
    json.dumps(external, allow_nan=False)


@pytest.mark.parametrize('counts,denominator', [([1.5], 10), ([11], 10), ([-1], 10),
    ([True], 10), ([np.nan], 10), ([1], 0)])
def test_capture_count_validation(counts, denominator):
    with pytest.raises(ValueError):
        bootstrap_capture_ci(counts, denominator)


def test_empty_robustness_evaluation_has_explicit_evidence_status():
    result = robust.evaluate_robustness_statistics(BTSConfig(), {'beta': [10, 5], 'alpha': [0, 0]}, [], kicker_model='off')
    assert result['n_samples'] == 0
    assert result['convergence_check']['status'] == 'insufficient_evidence'
    assert result['statistical_settings']['bootstrap_seed'] == 42
    json.dumps(result, allow_nan=False)


def test_cli_saves_selected_policy_and_does_not_print_false_zero(tmp_path, monkeypatch, capsys):
    from scripts import run_publication_tolerances as cli
    captured = []
    def evaluate(*args, **kwargs):
        policy = kwargs['statistical_policy']
        captured.append(policy)
        return summarize_robustness_results([outcome(.01), outcome(.02), outcome(.03)], policy)
    monkeypatch.setattr(cli, 'evaluate_robustness_statistics', evaluate)
    monkeypatch.setattr(cli, 'sample_error_ensemble', lambda *args, **kwargs: [])
    monkeypatch.setattr(cli, 'compute_one_at_a_time_sensitivity', lambda *args, **kwargs: {})
    output = tmp_path / 'selected-policy'
    cli.main(['--reference', '--output-dir', str(output), '--samples', '3',
              '--bootstrap-count', '17', '--bootstrap-seed', '11', '--ci-level', '.8',
              '--convergence-sizes', '2', '4', '--convergence-tolerance', '.02'])
    result = json.loads((output / 'publication_tolerances_summary.json').read_text())
    assert result['statistical_policy'] == captured[0].to_dict()
    assert result['sampling']['bootstrap'] == {'seed': 11, 'replicates': 17, 'ci_level': .8,
                                               'estimator': 'median_mismatch_x'}
    assert result['robustness_statistics']['convergence_check']['converged'] is None
    printed = capsys.readouterr().out
    assert 'insufficient_evidence' in printed and 'Absolute difference: None' in printed


def test_cli_raise_policy_archives_invalid_settings_and_diagnostics(tmp_path, monkeypatch):
    from scripts import run_publication_tolerances as cli
    def evaluate(*args, **kwargs):
        return summarize_robustness_results([outcome(None, 'invalid')], kwargs['statistical_policy'])
    monkeypatch.setattr(cli, 'evaluate_robustness_statistics', evaluate)
    monkeypatch.setattr(cli, 'sample_error_ensemble', lambda *args, **kwargs: [])
    output = tmp_path / 'invalid-policy'
    with pytest.raises(RuntimeError, match='Invalid evaluations'):
        cli.main(['--reference', '--output-dir', str(output), '--invalid-sample-policy', 'raise'])
    saved = json.loads((output / 'publication_tolerances_summary.json').read_text())
    assert saved['statistical_policy']['invalid_sample_policy'] == 'raise'
    stats = saved['robustness_statistics']
    assert stats['statistical_settings']['invalid_sample_policy'] == 'raise'
    assert stats['n_invalid_evaluations'] == 1
    assert stats['convergence_check']['converged'] is None
