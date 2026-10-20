#!/usr/bin/env python3
"""F4 — signed and physical associations, zero-capture summaries and two-model jitter rows (round 4).

Exploratory, not causal (the causal contrasts are F2). Inputs are the E7 full-budget ensembles (seeds 42, 123,
777; 150 joint realizations) and the paired seed-42 jitter ensembles; no new tracking.

Predictors (signed):
  booster x [m], booster x' [rad], mean energy offset [1], NKM-minus-orbit offset (nkm_dx - ring_co) [m],
  NKM amplitude error [1], septum position [m], septum strength [1], entrance beta mismatch x [1];
  physical: betatron amplitude of the centroid just after each kicker [m^1/2] (normalised with the drawn ring's
  NKM Twiss), computed from the realization's septum-exit centroid, every shot error and the kicker itself
  (3-D filament NKM, or the calibrated dipole control) -- the same geometry as the tracking.
Responses: NKM capture, dipole capture and their paired difference.
Statistics: Spearman rank correlation with the asymptotic two-sided p, Holm-adjusted within each response.
Interval convention: central 95 % percentile bootstrap over realizations (10 000 resamples, seed 1729); a
one-sided test at its lower endpoint is a conservative 97.5 % bound.
"""
import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
from nkm_injection.chamber import ChamberProfile
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.injection_timing import apply_injection_shot_errors
from nkm_injection.wire_field import CalibratedControl, FilamentNKMKicker

E7 = ROOT / 'results/journal_campaign_04'
LEVER = 2.0 + 0.2625
SIGNED = ('booster_x_m', 'booster_xp_rad', 'energy_dp_p', 'nkm_minus_orbit_m', 'nkm_scale_err', 'septum_x_m',
          'septum_strength_rel', 'beta_mismatch_x')


def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(p) - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def interval(values, seed=1729, count=10000):
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boot = v[rng.integers(0, len(v), (count, len(v)))].mean(1)
    return {'mean': float(v.mean()), 'ci95': np.quantile(boot, [.025, .975]).tolist()}


def ring_twiss():
    rows = json.loads((E7 / 'e5_corrected_ring/corrected_ring_summary.json').read_text())['rows']
    return {r['seed']: (r['optics_after']['nkm_beta_m'][0], r['optics_after']['nkm_alpha'][0]) for r in rows}


def post_kick_amplitudes(job, realization, twiss):
    """Centroid betatron amplitude [m^1/2] just after the NKM and after the dipole control."""
    cfg0 = InjectionStudyConfig.from_dict(job['config'])
    s = job['sample']
    timing_rel = s['nkm_timing_mrad'] * 1e-3 / abs(cfg0.injection_xp_rad)
    cfg = replace(cfg0, septum_edge_x_m=cfg0.septum_edge_x_m + s['septum_x_m'],
                  injection_x_m=cfg0.injection_x_m + s['septum_x_m'],
                  field_scale=cfg0.field_scale * (1 + s['nkm_scale_err'] + timing_rel),
                  nkm_dx_m=cfg0.nkm_dx_m + s['nkm_dx_m'], closed_orbit_x_m=cfg0.closed_orbit_x_m + s['ring_co_x_m'])
    ex = realization['bts_exit']
    b = np.zeros((6, 1))
    b[0] = cfg.injection_x_m - cfg.closed_orbit_x_m + ex['centroid_x_m']
    b[1] = cfg.injection_xp_rad + ex['centroid_xp_rad']
    b[4] = ex['delta_mean']
    scale = apply_injection_shot_errors(b, s, septum_angle_rad=job.get('septum_angle_mrad', 10.) * 1e-3,
                                        rf_frequency_hz=job['rf_frequency_hz'], pulse_duration_s=job['pulse_duration_us'] * 1e-6)
    cfg = replace(cfg, field_scale=cfg.field_scale * scale)
    b[0] += LEVER * b[1] / (1 + b[4])
    kch = ChamberProfile(**job['chamber']).kicker_kwargs() if job.get('chamber') else {}
    calib = job['calibration_3d']
    rel = cfg.field_scale / cfg0.field_scale
    beta, alpha = twiss[realization['ring_error_seed']]
    out = {}
    for model, kicker in (('fieldmap_3d', FilamentNKMKicker(cfg, n_slices=job.get('slices_3d', 640), **kch)),
                          ('dipole', CalibratedControl('dipole', calib[0] * rel + cfg.kick_offset_rad, calib[1] * rel, calib[2], **kch))):
        c = b.copy()
        if hasattr(kicker, 'apply'):
            kicker.apply(c, cfg.closed_orbit_x_m)
        else:
            from nkm_injection.injection_study import _apply_kick
            _apply_kick(c, kicker, cfg.closed_orbit_x_m)
        x, xp = float(c[0, 0]), float(c[1, 0])
        out[model] = {'amplitude_sqrt_m': float(np.hypot(x, alpha * x + beta * xp) / np.sqrt(beta)),
                      'x_m': x, 'xp_rad': xp}
    return out


def records():
    twiss = ring_twiss()
    rows = []
    for seed in (42, 123, 777):
        folder = E7 / f'e7_seed{seed}'
        raw = {r['sample_id']: r for r in json.loads((folder / 'capture_robustness_raw.json').read_text())['realizations']}
        for job in json.loads((folder / 'checkpoint_inputs.json').read_text())['jobs']:
            s = job['sample']
            r = raw[s['sample_id']]
            amp = post_kick_amplitudes(job, r, twiss)
            rows.append({'seed': seed, 'sample_id': s['sample_id'], 'ring': r['ring_error_seed'],
                         'nkm': r['models']['fieldmap_3d']['capture_fraction'], 'dipole': r['models']['dipole']['capture_fraction'],
                         'booster_x_m': s['booster_x_m'], 'booster_xp_rad': s['booster_xp_rad'], 'energy_dp_p': s['energy_dp_p'],
                         'nkm_minus_orbit_m': s['nkm_dx_m'] - s['ring_co_x_m'], 'nkm_scale_err': s['nkm_scale_err'],
                         'septum_x_m': s['septum_x_m'], 'septum_strength_rel': s['septum_strength_rel'],
                         'beta_mismatch_x': s['beta_mismatch_x'],
                         'amp_nkm': amp['fieldmap_3d']['amplitude_sqrt_m'], 'amp_dipole': amp['dipole']['amplitude_sqrt_m'],
                         'xp_after_nkm': amp['fieldmap_3d']['xp_rad'], 'xp_after_dipole': amp['dipole']['xp_rad']})
    return rows


def associations(rows):
    out = {}
    responses = {'nkm': [r['nkm'] for r in rows], 'dipole': [r['dipole'] for r in rows],
                 'difference': [r['nkm'] - r['dipole'] for r in rows]}
    predictors = {k: [r[k] for r in rows] for k in SIGNED}
    predictors['amplitude_after_nkm'] = [r['amp_nkm'] for r in rows]
    predictors['amplitude_after_dipole'] = [r['amp_dipole'] for r in rows]
    predictors['amplitude_difference'] = [r['amp_nkm'] - r['amp_dipole'] for r in rows]
    for name, y in responses.items():
        table = []
        for k, x in predictors.items():
            rho, p = spearmanr(x, y)
            table.append({'predictor': k, 'rho': float(rho), 'p': float(p)})
        for t, q in zip(table, holm([t['p'] for t in table])):
            t['p_holm'] = float(q)
        out[name] = table
    return out


def zero_capture(values):
    v = np.asarray(values, float)
    nz = v[v > 0]
    return {'n': int(len(v)), 'zero_fraction': float(np.mean(v == 0)), 'mean': float(v.mean()),
            'conditional_mean_nonzero': float(nz.mean()) if len(nz) else None}


def jitter_rows():
    """Paired seed-42 jitter ensembles for both models (differences from zero jitter)."""
    def load(name):
        return {r['sample_id']: r for r in json.loads((E7 / name / 'capture_robustness_raw.json').read_text())['realizations']}
    ref = load('e7_jitter_0')
    rows = {}
    for label, folder in (('0', 'e7_jitter_0'), ('0.25', 'e7_jitter_0.25'), ('0.5', 'e7_jitter_0.5'),
                          ('0.75', 'e7_jitter_0.75'), ('1', 'e7_seed42'), ('x_only', 'e7_jitter_x_only'),
                          ('xp_only', 'e7_jitter_xp_only')):
        cur = load(folder)
        ids = sorted(i for i in cur if i >= 0)
        row = {}
        for model in ('fieldmap_3d', 'dipole'):
            v = [cur[i]['models'][model]['capture_fraction'] for i in ids]
            d = [cur[i]['models'][model]['capture_fraction'] - ref[i]['models'][model]['capture_fraction'] for i in ids]
            row[model] = {'mean': float(np.mean(v)), **{'zero_fraction': zero_capture(v)['zero_fraction']},
                          'difference_from_zero': interval(d)}
        g = [cur[i]['models']['fieldmap_3d']['capture_fraction'] - cur[i]['models']['dipole']['capture_fraction'] for i in ids]
        row['gap'] = interval(g)
        rows[label] = row
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('output exists')
    rows = records()
    result = {'scope': 'Exploratory associations on 150 full-budget E7 realizations; not causal (see F2).',
              'interval_convention': 'central 95 % percentile bootstrap over realizations, 10 000 resamples, seed 1729; '
                                     'a one-sided test at its lower endpoint is a conservative 97.5 % bound',
              'multiplicity': 'Holm within each response over the listed predictors',
              'records': rows, 'associations': associations(rows),
              'zero_capture': {'nkm': zero_capture([r['nkm'] for r in rows]), 'dipole': zero_capture([r['dipole'] for r in rows])},
              'jitter_rows': jitter_rows()}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    for name, table in result['associations'].items():
        print(name, [(t['predictor'], round(t['rho'], 2), f"{t['p_holm']:.1e}") for t in sorted(table, key=lambda t: t['p'])[:5]])
    print(result['zero_capture'])
    print({k: (round(v['fieldmap_3d']['mean'], 3), round(v['dipole']['mean'], 3), round(v['gap']['mean'], 3)) for k, v in result['jitter_rows'].items()})


if __name__ == '__main__':
    main()
