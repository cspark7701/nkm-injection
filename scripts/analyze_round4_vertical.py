#!/usr/bin/env python3
"""Round-4 sensitivity — ideal static steering in both planes at the current point.

Declared in ``docs/paper/round4_protocol.json`` (``vertical_steering_sensitivity``) before the runs. Each two-plane
ensemble is paired with its production (horizontal-only steering) reference on the same 50 seed-42 realizations,
particles and corrected rings:
  f2v_xy_zero  vs  e7_jitter_0  (zero booster jitter)
  f2v_xy_full  vs  e7_seed42    (full budget)
Estimands: per model mean capture and zero-capture fraction; paired (xy minus x-only) changes for the 3-D NKM, the
dipole control and their gap. Intervals: central 95 % percentile bootstrap over realizations (10 000 resamples,
seed 1729). Sensitivity only; the production steering remains the headline model. Units: capture fractions; m, rad.
"""
import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from analyze_round4_ablation import bootstrap, check_pairing, load, vector  # noqa: E402

PROTOCOL = json.loads((ROOT / 'docs/paper/round4_protocol.json').read_text())
C5 = ROOT / PROTOCOL['campaign']
PAIRS = {'zero': ('f2v_xy_zero', 'results/journal_campaign_04/e7_jitter_0'),
         'full': ('f2v_xy_full', 'results/journal_campaign_04/e7_seed42')}
MODELS = ('fieldmap_3d', 'dipole', 'gap')


def summary(ens, ids):
    out = {}
    for m in MODELS:
        v = vector(ens, m, ids)
        out[m] = bootstrap(v) if m == 'gap' else {**bootstrap(v), 'zero_fraction': float(np.mean(v == 0))}
    return out


def exit_rms(ens, ids, key):
    return float(np.sqrt(np.mean([ens[i]['bts_exit'][key] ** 2 for i in ids])))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('output exists')
    result = {'protocol': 'docs/paper/round4_protocol.json#vertical_steering_sensitivity', 'budgets': {}}
    for budget, (name, ref_path) in PAIRS.items():
        xy, x = load(C5 / name), load(ROOT / ref_path)
        ids = check_pairing({'full': x, 'xy': xy})
        result['budgets'][budget] = {
            'ensembles': {'x_only': ref_path, 'xy': str((C5 / name).relative_to(ROOT))},
            'n_realizations': len(ids),
            'x_only': summary(x, ids), 'xy': summary(xy, ids),
            'paired_xy_minus_x': {m: bootstrap(vector(xy, m, ids) - vector(x, m, ids)) for m in MODELS},
            'exit_centroid_rms': {s: {k: exit_rms(e, ids, k) for k in ('centroid_y_m', 'centroid_yp_rad')}
                                  for s, e in (('x_only', x), ('xy', xy))}}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    for b, r in result['budgets'].items():
        f = lambda d: f"{100 * d['mean']:+.1f} [{100 * d['ci95'][0]:+.1f}, {100 * d['ci95'][1]:+.1f}]"
        print(b, 'x-only', {m: round(100 * r['x_only'][m]['mean'], 1) for m in MODELS},
              'xy', {m: round(100 * r['xy'][m]['mean'], 1) for m in MODELS})
        print('   paired', {m: f(v) for m, v in r['paired_xy_minus_x'].items()},
              'zero-capture', {s: (r[s]['fieldmap_3d']['zero_fraction'], r[s]['dipole']['zero_fraction']) for s in ('x_only', 'xy')},
              'exit y rms', r['exit_centroid_rms'])


if __name__ == '__main__':
    main()
