#!/usr/bin/env python3
"""F6 — septum dispersion budget and the scope of the thin-map accuracy result (round 4).

1. Dispersion at the septum exit (the injected beam of the adopted model): within-bunch betatron and dispersive
   contributions to the rms size and divergence, and the shot-to-shot centroid terms of the 0.1 % energy jitter.
2. Thin-map accuracy along the *production* matched trajectory at each F1 candidate point, compared with the
   synthetic diagnostic launch of the eta fit (centroid at the kick extremum with momentum opposite to the kick,
   y = 1 mm, y' = 0.2 mrad). Thin map: straight-line integrated filament kick at the centroid's position at the
   magnet centre; reference: exact 640-slice filament tracking; sliced vector map: 1280 slices. Midplane (y = 0)
   and y = 1 mm launches.
3. The companion BTS study's dispersion-free exit as an alternative (identity only; no ring capture is claimed).
Units: m, rad.
"""
import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.sliced_vector_map import integrated_filament_kicks, sliced_vector_map
from nkm_injection.wire_field import FilamentGeometry, FilamentNKMKicker

LEVER = 2.0 + 0.2625
JITTER_DELTA = 1e-3


def dispersion_budget(cfg):
    b = cfg.injected_beam
    gamma = (1 + b.alpha_x ** 2) / b.beta_x_m
    return {'D_m': b.disp_x_m, 'Dp': b.disp_px, 'sigma_delta': b.energy_spread,
            'betatron_size_m': float(np.sqrt(b.emit_x_m_rad * b.beta_x_m)),
            'dispersive_size_m': float(abs(b.disp_x_m) * b.energy_spread),
            'betatron_divergence_rad': float(np.sqrt(b.emit_x_m_rad * gamma)),
            'dispersive_divergence_rad': float(abs(b.disp_px) * b.energy_spread),
            'total_divergence_rad': float(np.hypot(np.sqrt(b.emit_x_m_rad * gamma), b.disp_px * b.energy_spread)),
            'shot_energy_jitter': JITTER_DELTA,
            'shot_angle_rad': float(abs(b.disp_px) * JITTER_DELTA), 'shot_position_m': float(abs(b.disp_x_m) * JITTER_DELTA)}


def accuracy(cfg, y0=0.0, yp0=0.0):
    """Thin, sliced and exact exit momenta for a centroid launched at the magnet centre (straight-line chord)."""
    g = FilamentGeometry()
    x_c = cfg.injection_x_m + LEVER * cfg.injection_xp_rad
    b = np.array([x_c, cfg.injection_xp_rad, y0, yp0, 0.0, 0.0])
    thin = b.copy()
    kx, ky = integrated_filament_kicks(b[0], b[2], g, scale=cfg.field_scale)
    thin[1] += float(kx)
    thin[3] += float(ky)
    full = b[:, None].copy()
    lost = FilamentNKMKicker(cfg, n_slices=640).apply(full, 0.0)
    if lost.any():
        raise RuntimeError('production centroid lost')
    sliced = sliced_vector_map(b, g, scale=cfg.field_scale, slices=1280)
    return {'centroid_at_centre_m': float(x_c), 'launch_y_m': y0, 'launch_yp_rad': yp0,
            'thin_minus_3d': (thin - full[:, 0]).tolist(), 'sliced_minus_3d': (sliced - full[:, 0]).tolist(),
            'exit_px_3d_rad': float(full[1, 0])}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise SystemExit('output exists')
    pts = json.loads((ROOT / 'results/journal_campaign_05/points/points.json').read_text())['points']
    rows = {}
    for name, point in pts.items():
        cfg = InjectionStudyConfig.load(ROOT / point['config'])
        rows[name] = {'config': point['config'], 'field_scale': cfg.field_scale,
                      'midplane': accuracy(cfg), 'offplane_1mm': accuracy(cfg, 1e-3, 2e-4)}
    current = InjectionStudyConfig.load(ROOT / pts['current']['config'])
    bts_exit = json.loads((ROOT / 'docs/paper_bts/generated/round3_exit.json').read_text())
    result = {'units': 'm, rad', 'dispersion_budget': dispersion_budget(current), 'production_accuracy': rows,
              'synthetic_launch': 'eta fit (round 3): centroid at the kick extremum, momentum opposite to the kick, y = 1 mm, '
                                  "y' = 0.2 mrad, S = 0.85 family scan; production launches above are the matched trajectories",
              'companion_dispersion_free_exit': {'source': 'docs/paper_bts/generated/round3_exit.json',
                                                 'pool': bts_exit['dispersion_free_pool'],
                                                 'best_mu_x_deg': bts_exit['dispersion_free_best']['mu_x_deg'],
                                                 'best_exit_jitter_xp_rad': bts_exit['dispersion_free_best']['exit_jitter_xp_rad'],
                                                 'scope': 'BTS-only analytic result on the unchanged BTS lattice; not imported into NKM capture'}}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['dispersion_budget']))
    for n, r in rows.items():
        print(n, 'thin-3d px (mid, off) urad', round(r['midplane']['thin_minus_3d'][1] * 1e6, 2), round(r['offplane_1mm']['thin_minus_3d'][1] * 1e6, 2),
              'py off', round(r['offplane_1mm']['thin_minus_3d'][3] * 1e6, 2), 'sliced px', f"{r['midplane']['sliced_minus_3d'][1]:.1e}")


if __name__ == '__main__':
    main()
