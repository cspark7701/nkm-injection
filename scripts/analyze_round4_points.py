#!/usr/bin/env python3
"""F3 — paired comparison of the current, earlier and extremum-centred points (round 4).

Each point is evaluated at the zero-jitter and full budgets on the same 50 seed-42 realizations, particles and
corrected rings; the dipole control is recalibrated at each point. The current point uses the bitwise-reproduced E7
ensembles. The decision rule is the one declared in docs/paper/round4_protocol.json:
  a candidate replaces the current point only if its full-budget NKM mean exceeds the current one with a paired
  central 95 % interval excluding zero, and its zero-jitter NKM mean is not lower by more than the 1-point declared
  margin (lower endpoint of the paired interval above -0.01; a conservative 97.5 % one-sided bound).
Units: capture fractions.
"""
import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = json.loads((ROOT / 'docs/paper/round4_protocol.json').read_text())
C5 = ROOT / PROTOCOL['campaign']
MARGIN = 0.01


def load(folder):
    raw = json.loads((folder / 'capture_robustness_raw.json').read_text())
    return {r['sample_id']: r for r in raw['realizations'] if r['sample_id'] >= 0}


def bootstrap(values, seed=1729, count=10000):
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boot = v[rng.integers(0, len(v), (count, len(v)))].mean(1)
    return {'mean': float(v.mean()), 'ci95': np.quantile(boot, [.025, .975]).tolist()}


def vec(ens, model, ids):
    if model == 'gap':
        return np.array([ens[i]['models']['fieldmap_3d']['capture_fraction'] - ens[i]['models']['dipole']['capture_fraction'] for i in ids])
    return np.array([ens[i]['models'][model]['capture_fraction'] for i in ids])


def meets_rule(full, zero, margin=MARGIN):
    """Declared F3 rule on paired NKM differences (candidate - current): full-budget gain with a central 95 %
    interval above zero, and a zero-jitter loss no larger than ``margin`` (lower endpoint above -margin)."""
    return bool(full['ci95'][0] > 0 and zero['ci95'][0] > -margin)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('output exists')
    data = {'current': {'zero': load(ROOT / PROTOCOL['references']['full_zero_jitter']),
                        'full': load(ROOT / PROTOCOL['references']['full_budget'])}}
    for point in ('earlier', 'extremum'):
        data[point] = {b: load(C5 / f'f3_{point}_{b}') for b in ('zero', 'full')}
    ids = sorted(data['current']['zero'])
    for point, budgets in data.items():
        for b, ens in budgets.items():
            ref = data['current'][b]
            if sorted(ens) != ids or any((ens[i]['beam_seed'], ens[i]['ring_error_seed']) != (ref[i]['beam_seed'], ref[i]['ring_error_seed']) for i in ids):
                raise ValueError(f'Unpaired ensemble {point}/{b}')
    points = json.loads((C5 / 'points/points.json').read_text())['points']
    result = {'points': points, 'margin': MARGIN, 'decision_rule': PROTOCOL['f3_points']['decision_rule'], 'by_point': {}}
    for point, budgets in data.items():
        entry = {}
        for b, ens in budgets.items():
            entry[b] = {m: {**bootstrap(vec(ens, m, ids)), 'zero_fraction': float(np.mean(vec(ens, m, ids) == 0))} if m != 'gap'
                        else bootstrap(vec(ens, m, ids)) for m in ('fieldmap_3d', 'dipole', 'gap')}
            if point != 'current':
                entry[b]['paired_vs_current'] = {m: bootstrap(vec(ens, m, ids) - vec(data['current'][b], m, ids))
                                                 for m in ('fieldmap_3d', 'dipole', 'gap')}
        if point != 'current':
            full = entry['full']['paired_vs_current']['fieldmap_3d']
            zero = entry['zero']['paired_vs_current']['fieldmap_3d']
            entry['meets_rule'] = meets_rule(full, zero)
        result['by_point'][point] = entry
    winners = [p for p in ('earlier', 'extremum') if result['by_point'][p]['meets_rule']]
    best = max(winners, key=lambda p: result['by_point'][p]['full']['paired_vs_current']['fieldmap_3d']['mean']) if winners else None
    result['decision'] = {'adopted_point': best or 'current', 'candidates_meeting_rule': winners,
                          'note': 'Evaluated on the seed-42 population; a change is a selection on that population, not a held-out optimum.'}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    for point, e in result['by_point'].items():
        print(point, {b: (round(100 * e[b]['fieldmap_3d']['mean'], 1), round(100 * e[b]['dipole']['mean'], 1), round(100 * e[b]['gap']['mean'], 1))
                      for b in ('zero', 'full')}, e.get('meets_rule'))
    print('decision', result['decision'])


if __name__ == '__main__':
    main()
