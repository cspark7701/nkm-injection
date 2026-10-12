#!/usr/bin/env python3
"""D3 independent ODE check, slice/span convergence and documented accuracy gate."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.trajectory_reference import integrate_reference
from nkm_injection.wire_field import FilamentNKMKicker


def validate(config,edge_offsets_rad=(-.00030,.00044)):
    if not np.isfinite(edge_offsets_rad).all() or not edge_offsets_rad[0]<0<edge_offsets_rad[1]:
        raise ValueError('Window edges must bracket the nominal angle')
    cases = [('nominal', 0., 0., 0., 0.), ('lower_window', edge_offsets_rad[0], 0., 0., 0.),
             ('upper_window', edge_offsets_rad[1], 0., 0., 0.), ('vertical_position', 0., .001, 0., 0.),
             ('vertical_angle', 0., 0., .0002, 0.), ('vertical_both', 0., .001, .0002, 0.),
             ('delta_minus', 0., .001, .0002, -.002), ('delta_plus', 0., .001, .0002, .002)]
    rows = []
    # 1% of the measured 0.74 mrad window; 1% of a 0.1-sigma stored-beam response.
    sigma_x = np.sqrt(61.6e-12 * 16.27)
    sigma_y = np.sqrt(61.6e-12 * .1 * 5.60)
    position_limit = min(sigma_x, sigma_y) * .001
    momentum_limit = min(7.4e-6, sigma_x * .001 / 16.27, sigma_y * .001 / 5.60)
    for label, dpx, y, py, delta in cases:
        px = (config.injection_xp_rad + dpx) * (1 + delta)
        b = np.array([config.injection_x_m + 2.2625 * (config.injection_xp_rad + dpx),
                      px, y, py * (1 + delta), delta, 0.])
        ref = integrate_reference(config, b)
        tight = integrate_reference(config, b, rtol=2e-12, atol=2e-14)
        slices = []
        for n in (160, 320, 640, 1280):
            beam = b[:, None].copy()
            lost = FilamentNKMKicker(config, n_slices=n).apply(beam, config.closed_orbit_x_m)
            if lost.any():
                raise RuntimeError(f'Validation particle lost: {label}')
            slices.append({'n_slices': n, 'exit': beam[:, 0].tolist(),
                           'minus_reference': (beam[:, 0] - ref).tolist()})
        span = []
        for s in (.45, .65, .9):
            u = integrate_reference(config, b, span_m=s)
            beam = b[:, None].copy()
            FilamentNKMKicker(config, n_slices=int(round(640*s/.45)), s_span_m=s).apply(beam, config.closed_orbit_x_m)
            span.append({'span_m': s, 'reference_exit': u.tolist(), 'slice_minus_reference': (beam[:, 0]-u).tolist(),
                         'reference_minus_default_span': (u-ref).tolist()})
        err = np.asarray(slices[2]['minus_reference'])[:4]
        rows.append({'case': label, 'initial': b.tolist(), 'reference_exit': ref.tolist(),
                     'solver_refinement_difference': (tight-ref).tolist(), 'slices': slices, 'spans': span,
                     'slice_gate': bool(np.max(np.abs(err[[0,2]])) < position_limit and
                                        np.max(np.abs(err[[1,3]])) < momentum_limit)})
    return {'config': config.to_dict(), 'solver': 'DOP853', 'rtol': 2e-11, 'atol': 2e-13, 'max_step_m': .01,
            'coordinates': ['x_m','px_rad','y_m','py_rad','delta','ct_m'], 'cases': rows,
            'position_limit_m': position_limit, 'momentum_limit_rad': momentum_limit,
            'gate_basis': '1% of 0.1 sigma using beta_x/y=16.27/5.60 m and emittance 61.6/6.16 pm rad',
            'passed': all(r['slice_gate'] for r in rows),
            'scope': 'numerical check of stated paraxial equations; same field, independent integrator'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-config', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--edge-offsets-mrad',type=float,nargs=2,default=[-.30,.44])
    a=p.parse_args()
    if a.output.exists(): raise SystemExit('Output exists')
    out=validate(InjectionStudyConfig.load(a.study_config),np.asarray(a.edge_offsets_mrad)*1e-3)
    out['edge_offsets_mrad']=a.edge_offsets_mrad
    out['config_sha256']=hashlib.sha256(a.study_config.read_bytes()).hexdigest()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    for row in out['cases']:
        print(row['case'],row['slices'][2]['minus_reference'][:4],row['slice_gate'])
    if not out['passed']: raise SystemExit('D3 slice gate failed; fix numerical integration before reruns')


if __name__=='__main__': main()
