"""Descriptive statistics and explicit prefix-stability policies; no physics units change."""
from dataclasses import dataclass
from typing import Literal, Tuple
import copy

import numpy as np

from .configuration import SerializableConfigMixin, _to_serializable
from .tracking_contracts import positive_count, finite_scalar


class InvalidStatisticalSamplesError(ValueError):
    """Rejected invalid ensemble with diagnostics available for archival."""
    def __init__(self, summary):
        self.summary = summary
        super().__init__(f"{summary['n_invalid_evaluations']} invalid evaluations; invalid_sample_policy=raise")


@dataclass
class StatisticalPolicy(SerializableConfigMixin):
    """Robustness settings; median mismatch tolerance is dimensionless.

    Excluded computations never count as physical failures and block stability
    claims. ``raise`` rejects a summary containing any invalid evaluation.
    """
    bootstrap_count: int = 1000
    bootstrap_seed: int = 42
    ci_level: float = 0.95
    convergence_sizes: Tuple[int, int] = (50, 100)
    convergence_tolerance: float = 0.05
    invalid_sample_policy: Literal['exclude', 'raise'] = 'exclude'

    def validate(self):
        validate_bootstrap_settings(self.bootstrap_count, self.bootstrap_seed, self.ci_level)
        if len(self.convergence_sizes) != 2:
            raise ValueError('convergence_sizes must contain two distinct increasing counts')
        small, large = [positive_count(n, 'convergence size') for n in self.convergence_sizes]
        if small >= large:
            raise ValueError('convergence_sizes must contain two distinct increasing counts')
        finite_scalar(self.convergence_tolerance, 'convergence_tolerance', minimum=0)
        if self.invalid_sample_policy not in ('exclude', 'raise'):
            raise ValueError('invalid_sample_policy must be exclude or raise')


def validate_bootstrap_settings(count, seed, ci_level):
    positive_count(count, 'bootstrap_count')
    if isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)) or seed < 0:
        raise ValueError('bootstrap_seed must be a nonnegative integer')
    finite_scalar(ci_level, 'ci_level')
    if not 0 < ci_level < 1:
        raise ValueError('ci_level must be between zero and one')


def finite_observations(values):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError('statistical observations must be a finite 1-D array')
    return values


def bootstrap_interval(values, *, estimator, count=1000, seed=42, ci_level=.95, rng=None):
    """Percentile interval by resampling observations; estimator is mean or median.

    This measures variability of the selected estimand across observations. It
    does not establish numerical convergence or compensate for excluded data.
    """
    validate_bootstrap_settings(count, seed, ci_level)
    values = finite_observations(values)
    if estimator not in ('mean', 'median'):
        raise ValueError('estimator must be mean or median')
    if rng is not None and not isinstance(rng, np.random.Generator):
        raise TypeError('rng must be a NumPy Generator')
    generator = np.random.default_rng(seed) if rng is None else rng
    settings = {'estimator': estimator, 'count': int(count), 'seed': int(seed) if rng is None else None,
                'ci_level': float(ci_level), 'method': 'percentile', 'quantile_method': 'linear',
                'resampling_unit': 'observation', 'bit_generator': type(generator.bit_generator).__name__}
    if rng is not None:
        settings['rng_state_before'] = _to_serializable(copy.deepcopy(generator.bit_generator.state))
    if not values.size:
        return {'estimate': None, 'ci_lo': None, 'ci_hi': None, 'status': 'insufficient_evidence',
                'n_observations': 0, 'settings': settings}
    statistic = np.mean if estimator == 'mean' else np.median
    # Keep draws sequential to preserve existing deterministic seed semantics.
    replicates = [statistic(generator.choice(values, size=values.size, replace=True)) for _ in range(count)]
    alpha = (1-ci_level)/2
    lo, hi = np.percentile(replicates, [100*alpha, 100*(1-alpha)])
    return {'estimate': float(statistic(values)), 'ci_lo': float(lo), 'ci_hi': float(hi),
            'status': 'descriptive_only' if values.size == 1 else 'estimated',
            'n_observations': int(values.size), 'settings': settings}


def summarize_observations(values):
    """Finite descriptive percentiles, mean and population std in input units."""
    values = finite_observations(values)
    keys = ('p50', 'p50_median', 'p68', 'p95', 'p99', 'mean', 'std', 'max')
    if not values.size:
        return dict.fromkeys(keys)
    p50, p68, p95, p99 = np.percentile(values, [50, 68, 95, 99])
    return dict(zip(keys, map(float, (p50, p50, p68, p95, p99, np.mean(values), np.std(values), np.max(values)))))


def check_prefix_stability(values, policy, *, n_invalid=0):
    """Compare ordered median prefixes only when both exact sizes are available."""
    policy.validate()
    values = finite_observations(values)
    small, large = policy.convergence_sizes
    result = {'status': 'insufficient_evidence', 'converged': None,
              'estimand': 'median_mismatch_x', 'method': 'ordered_prefix_stability',
              'sample_sizes': [int(small), int(large)], 'available_valid_samples': int(values.size),
              'n_invalid_evaluations': int(n_invalid), 'tolerance': policy.convergence_tolerance,
              'comparison': 'absolute_difference < tolerance', 'absolute_difference': None,
              'prefix_estimates': None}
    if (small, large) == (50, 100):
        result['N_50_to_100_diff'] = None
    if n_invalid:
        result['status'] = 'blocked_invalid_evaluations'
    elif values.size >= large:
        estimates = [float(np.median(values[:n])) for n in (small, large)]
        difference = abs(estimates[1]-estimates[0])
        result.update(prefix_estimates=estimates, absolute_difference=difference,
                      converged=bool(difference < policy.convergence_tolerance),
                      status='within_tolerance' if difference < policy.convergence_tolerance else 'outside_tolerance')
        if (small, large) == (50, 100):
            result['N_50_to_100_diff'] = difference
    return result


def summarize_robustness_results(results, policy=None, *, capture_enabled=False):
    """Summarize computed outcomes; invalid penalties never enter observations."""
    policy = policy or StatisticalPolicy()
    policy.validate()
    if any(r['outcome']['status'] not in ('valid', 'infeasible', 'invalid') for r in results):
        raise ValueError('unknown evaluation outcome status')
    valid = [r for r in results if r['outcome']['status'] != 'invalid']
    n_total, n_valid = len(results), len(valid)
    n_invalid = n_total-n_valid
    failures = [r for r in valid if r['outcome']['status'] == 'infeasible']
    failure_modes = dict.fromkeys(('beta_exceeded', 'mismatch_exceeded', 'capture_failed'), 0)
    for r in failures:
        for reason in r['outcome']['physical_failure_reasons']:
            failure_modes[reason] = failure_modes.get(reason, 0)+1
    mx = [r['mx'] for r in valid]
    interval = bootstrap_interval(mx, estimator='median', count=policy.bootstrap_count,
                                  seed=policy.bootstrap_seed, ci_level=policy.ci_level)
    summaries = {name: summarize_observations([r[key] for r in valid]) for name, key in (
        ('mismatch_x', 'mx'), ('mismatch_y', 'my'), ('max_beta_x_m', 'bx_max'),
        ('max_beta_y_m', 'by_max'), ('stored_beam_kick_mrad', 'stored_kick_mrad'))}
    summaries['mismatch_x']['bootstrap_ci_median'] = [interval['ci_lo'], interval['ci_hi']]
    # Preserve the old alias only at its actual confidence level.
    if policy.ci_level == .95:
        summaries['mismatch_x']['bootstrap_95ci_median'] = [interval['ci_lo'], interval['ci_hi']]
    summaries['mismatch_x']['bootstrap'] = interval
    summaries['capture_efficiency'] = summarize_observations([r['eff'] for r in valid]) if capture_enabled else {}
    summary = {**summaries, 'n_samples': n_total, 'n_valid_evaluations': n_valid,
            'n_invalid_evaluations': n_invalid, 'n_physical_failures': len(failures),
            'n_physically_feasible': n_valid-len(failures),
            'invalid_evaluation_fraction': n_invalid/n_total if n_total else None,
            'feasible_fraction': (n_valid-len(failures))/n_total if n_total else None,
            'failure_probability': len(failures)/n_valid if n_valid else None,
            'failure_modes': failure_modes, 'sample_results': results,
            'statistical_settings': {**policy.to_dict(), 'summary_std_ddof': 0,
                'percentile_method': 'linear', 'failure_probability_denominator': 'valid_evaluations',
                'feasible_fraction_denominator': 'requested_evaluations'},
            'convergence_check': check_prefix_stability(mx, policy, n_invalid=n_invalid)}

    if n_invalid and policy.invalid_sample_policy == 'raise':
        raise InvalidStatisticalSamplesError(summary)
    return summary
