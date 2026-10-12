"""Round-2 evidence statistics. Capture and differences are fractions, not percent."""
import numpy as np


def holm_adjust(pvalues):
    """Holm family-wise adjusted p-values, preserving input order."""
    p = np.asarray(pvalues, dtype=float)
    if p.ndim != 1 or not np.isfinite(p).all() or np.any((p < 0) | (p > 1)):
        raise ValueError('p-values must be a finite vector in [0, 1]')
    order = np.argsort(p)
    out = np.empty_like(p)
    out[order] = np.minimum(1, np.maximum.accumulate(p[order] * np.arange(len(p), 0, -1)))
    return out


def capture_by_id(raw, model='fieldmap_3d'):
    """Read non-reference realizations, rejecting duplicates and invalid captures."""
    out = {}
    for row in raw['realizations']:
        i = row['sample_id']
        if i < 0:
            continue
        if i in out:
            raise ValueError('Duplicate realization ID')
        value = row['models'][model]['capture_fraction']
        if not np.isfinite(value) or not 0 <= value <= 1:
            raise ValueError('Invalid capture fraction')
        out[i] = float(value)
    if not out:
        raise ValueError('No non-reference realizations')
    return out


def paired_capture_difference(reference, comparison, *, seed=1729, count=10000, loss_margin=0.01):
    """Comparison minus reference; percentile bootstrap resamples paired realization IDs.

    ``loss_margin`` is a declared engineering tolerance in capture fraction. The
    noninferiority flag requires the lower 95% endpoint above minus that margin.
    """
    if set(reference) != set(comparison) or not reference:
        raise ValueError('Paired studies must have identical nonempty realization IDs')
    if not isinstance(count, int) or count < 1 or not np.isfinite(loss_margin) or loss_margin <= 0:
        raise ValueError('Invalid bootstrap count or loss margin')
    ids = sorted(reference)
    d = np.array([comparison[i] - reference[i] for i in ids], dtype=float)
    if not np.isfinite(d).all():
        raise ValueError('Nonfinite paired difference')
    rng = np.random.default_rng(seed)
    boot = d[rng.integers(0, len(d), size=(count, len(d)))].mean(axis=1)
    ci = np.quantile(boot, [0.025, 0.975])
    values = np.array([comparison[i] for i in ids])
    return {'n_pairs': len(d), 'mean_difference': float(d.mean()), 'ci95': ci.tolist(),
            'bootstrap_seed': seed, 'bootstrap_count': count, 'method': 'paired percentile bootstrap',
            'resampling_unit': 'error realization', 'loss_margin': loss_margin,
            'noninferior_at_declared_margin': bool(ci[0] > -loss_margin),
            'mean': float(values.mean()), 'median': float(np.median(values)),
            'p10': float(np.quantile(values, .1)), 'fraction_ge_80pct': float(np.mean(values >= .8))}
