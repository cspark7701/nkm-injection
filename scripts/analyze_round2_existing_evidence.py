#!/usr/bin/env python3
"""D2: hash-verified survival, paired jitter and Holm-adjusted partial correlations."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble
from nkm_injection.injection_study import wilson_interval
from nkm_injection.revision_statistics import capture_by_id, paired_capture_difference, holm_adjust
from analyze_capture_robustness import SCALARS, VECTORS, partial_spearman


def analyze(manifest, root):
    m = json.loads(Path(manifest).read_text())
    used = {}

    def load(key):
        path = root / m['artifacts'][key]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != m['sha256'][key]:
            raise ValueError(f'Hash mismatch: {key}')
        used[key] = {'path': str(path), 'sha256': digest}
        return json.loads(data)

    lt = load('c4_longturn')
    rows = lt['rows']
    turns = {r['turns'] for r in rows}
    if len(turns) != 1:
        raise ValueError('Long-turn durations differ')
    n, k = sum(r['n'] for r in rows), sum(r['captured'] for r in rows)
    survival = {'turns': turns.pop(), 'n': n, 'captured': k, 'fraction': k / n,
                'ci95_wilson': list(wilson_interval(k, n)), 'seeds': sorted({r['seed'] for r in rows}),
                'interval_unit': 'particle; conditional on the two generated bunches'}
    jitter = {}
    correlations = {}
    for prefix in ('c6', 'c6c'):
        ref_raw = load(f'{prefix}_raw_0')
        reference = capture_by_id(ref_raw)
        for level in ('0', '0.25', '0.5', '0.75', '1', 'x_only', 'xp_only'):
            key = f'{prefix}_raw_{level}'
            if level == '1':
                key = 'c5c_raw_42' if prefix == 'c6c' else 'c5_raw_42'
            raw = load(key)
            if raw['cli']['seed'] != ref_raw['cli']['seed']:
                raise ValueError('Paired studies must have the same ensemble seed')
            jitter[f'{prefix}_{level}'] = paired_capture_difference(reference, capture_by_id(raw))
    for prefix in ('c5', 'c5c'):
        caps, features = [], []
        for seed in (42, 123, 777):
            d = load(f'{prefix}_raw_{seed}')
            samples = {s['sample_id']: s for s in sample_error_ensemble(
                ErrorBudgetConfig.from_dict(d['error_config']), d['cli']['samples'], seed)}
            for i, cap in capture_by_id(d).items():
                s = samples[i]
                feature = {key: abs(s[key]) * d['error_scale'] for key in SCALARS}
                feature.update({f'rms_{key}': float(np.sqrt(np.mean(np.square(s[key])))) * d['error_scale']
                                for key in VECTORS})
                caps.append(cap); features.append(feature)
        selected = {key: np.array([f[key] for f in features]) for key in features[0]
                    if np.ptp([f[key] for f in features]) > 0}
        stats = partial_spearman(selected, caps)
        adjusted = holm_adjust([s['p_value'] for s in stats])
        for s, q in zip(stats, adjusted):
            s['p_holm'] = float(q)
        correlations[prefix] = {'n_realizations': len(caps), 'family_size': len(stats), 'rows': stats,
                               'interpretation': 'model-conditioned association; not causation'}
    return {'survival': survival, 'paired_jitter': jitter, 'partial_correlations': correlations,
            'inputs': used, 'units': 'capture fractions; angles rad; positions m',
            'equivalence_margin': '1 percentage point declared for sensitivity; not a proven allocation'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, default=Path('docs/paper/revision_manifest.json'))
    p.add_argument('--repo-root', type=Path, default=Path.cwd())
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('Output exists; choose a new path')
    out = analyze(a.manifest, a.repo_root)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'survival': out['survival'], 'quarter': out['paired_jitter']['c6c_0.25']}, indent=2))


if __name__ == '__main__':
    main()
