#!/usr/bin/env python3
"""F2 — paired error-class ablation at zero booster jitter (round 4).

Ensembles (50 seed-42 realizations each, identical particles and corrected-ring identities):
all-off, the full zero-jitter budget (E7 ``e7_jitter_0``), each class alone and each class omitted.
Estimands, per model (3-D NKM, dipole control) and for the paired NKM-minus-dipole gap:
  ensemble means;
  alone effect   = alone_c  - all_off   (the class acting by itself);
  omitted effect = full     - omit_c    (the class's contribution in the presence of all others);
  non-additivity = (full - all_off) - sum_c alone effect_c.
Intervals: central 95 % percentile bootstrap over realizations (10 000 resamples, seed 1729), pointwise.
Post hoc (labelled exploratory): the septum-exit state left by the class with the largest effect, compared with
all-off, and its Spearman association with capture within that class-alone ensemble.
Units: capture fractions (reported in percentage points by the note); m, rad for the exit state.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = json.loads((ROOT / 'docs/paper/round4_protocol.json').read_text())
C5 = ROOT / PROTOCOL['campaign']
MODELS = ('fieldmap_3d', 'dipole')


def classes():
    return [c for c in PROTOCOL['error_classes'] if c not in ('not_applied', 'disabling_rule')]


def load(folder):
    raw = json.loads((folder / 'capture_robustness_raw.json').read_text())
    return {r['sample_id']: r for r in raw['realizations'] if r['sample_id'] >= 0}


def vector(ens, model, ids):
    if model == 'gap':
        return np.array([ens[i]['models']['fieldmap_3d']['capture_fraction'] - ens[i]['models']['dipole']['capture_fraction'] for i in ids])
    return np.array([ens[i]['models'][model]['capture_fraction'] for i in ids])


def bootstrap(values, seed=1729, count=10000):
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boot = v[rng.integers(0, len(v), (count, len(v)))].mean(1)
    return {'mean': float(v.mean()), 'ci95': np.quantile(boot, [.025, .975]).tolist()}


def check_pairing(ensembles):
    ref = ensembles['full']
    ids = sorted(ref)
    for name, ens in ensembles.items():
        if sorted(ens) != ids:
            raise ValueError('Unpaired realization set: ' + name)
        for i in ids:
            if (ens[i]['beam_seed'], ens[i]['ring_error_seed']) != (ref[i]['beam_seed'], ref[i]['ring_error_seed']):
                raise ValueError('Particles or ring identity differ: ' + name)
    return ids


def analyse(ensembles):
    ids = check_pairing(ensembles)
    out = {'n_realizations': len(ids), 'ensembles': {}, 'alone_effect': {}, 'omitted_effect': {}, 'non_additivity': {}}
    for name, ens in ensembles.items():
        out['ensembles'][name] = {m: {**bootstrap(vector(ens, m, ids)), 'zero_fraction': float(np.mean(vector(ens, m, ids) == 0))}
                                  if m != 'gap' else bootstrap(vector(ens, m, ids)) for m in MODELS + ('gap',)}
    for c in classes():
        out['alone_effect'][c] = {m: bootstrap(vector(ensembles[f'alone_{c}'], m, ids) - vector(ensembles['all_off'], m, ids))
                                  for m in MODELS + ('gap',)}
        out['omitted_effect'][c] = {m: bootstrap(vector(ensembles['full'], m, ids) - vector(ensembles[f'omit_{c}'], m, ids))
                                    for m in MODELS + ('gap',)}
    for m in MODELS + ('gap',):
        total = vector(ensembles['full'], m, ids) - vector(ensembles['all_off'], m, ids)
        alone = sum(vector(ensembles[f'alone_{c}'], m, ids) - vector(ensembles['all_off'], m, ids) for c in classes())
        out['non_additivity'][m] = {'total_effect': bootstrap(total), 'sum_of_alone': bootstrap(alone),
                                    'difference': bootstrap(total - alone)}
    return out


EXIT_KEYS = ('centroid_x_m', 'centroid_xp_rad', 'centroid_y_m', 'centroid_yp_rad', 'beta_x_m', 'beta_y_m', 'disp_x_m', 'disp_px')


def exit_state(ensembles, name, ids):
    """Exit-state spread (all-off vs the named alone ensemble) and Spearman associations of |state| with capture."""
    alone, off = ensembles[name], ensembles['all_off']
    state = {k: {'all_off': [float(np.mean([off[i]['bts_exit'][k] for i in ids])), float(np.std([off[i]['bts_exit'][k] for i in ids]))],
                 name: [float(np.mean([alone[i]['bts_exit'][k] for i in ids])), float(np.std([alone[i]['bts_exit'][k] for i in ids]))]}
             for k in EXIT_KEYS}
    assoc = {}
    for k in EXIT_KEYS:
        v = np.abs([alone[i]['bts_exit'][k] for i in ids])
        assoc[k] = {m: dict(zip(('rho', 'p'), map(float, spearmanr(v, vector(alone, m, ids))))) for m in MODELS}
    return {'ensemble': name, 'mean_std': state, 'spearman_abs_vs_capture': assoc,
            'scope': 'post hoc, exploratory, unadjusted; association within one ensemble, not a causal decomposition'}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('output exists')
    ensembles = {'all_off': load(C5 / 'f2_all_off'), 'full': load(ROOT / PROTOCOL['references']['full_zero_jitter'])}
    for c in classes():
        ensembles[f'alone_{c}'] = load(C5 / f'f2_alone_{c}')
        ensembles[f'omit_{c}'] = load(C5 / f'f2_omit_{c}')
    result = {'protocol': 'docs/paper/round4_protocol.json', 'classes': {c: PROTOCOL['error_classes'][c] for c in classes()},
              'interval': 'central 95 % percentile bootstrap over the 50 paired realizations, 10 000 resamples, seed 1729; pointwise',
              **analyse(ensembles)}
    largest = min(classes(), key=lambda c: result['alone_effect'][c]['fieldmap_3d']['mean'])
    result['exit_state_post_hoc'] = exit_state(ensembles, f'alone_{largest}', sorted(ensembles['full']))
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    e = result['ensembles']
    print('all-off', {m: round(100 * e['all_off'][m]['mean'], 1) for m in MODELS + ('gap',)},
          'full', {m: round(100 * e['full'][m]['mean'], 1) for m in MODELS + ('gap',)})
    for c in classes():
        al, om = result['alone_effect'][c], result['omitted_effect'][c]
        print(f"{c:22s} alone NKM {100 * al['fieldmap_3d']['mean']:+6.1f} dip {100 * al['dipole']['mean']:+6.1f} gap {100 * al['gap']['mean']:+6.1f} | "
              f"omitted NKM {100 * om['fieldmap_3d']['mean']:+6.1f} dip {100 * om['dipole']['mean']:+6.1f} gap {100 * om['gap']['mean']:+6.1f}")
    x = result['exit_state_post_hoc']
    print(x['ensemble'], {k: round(v[x['ensemble']][1], 7) for k, v in x['mean_std'].items()},
          {k: round(v['fieldmap_3d']['rho'], 2) for k, v in x['spearman_abs_vs_capture'].items()})
    print('non-additivity', {m: round(100 * v['difference']['mean'], 1) for m, v in result['non_additivity'].items()})


if __name__ == '__main__':
    main()
