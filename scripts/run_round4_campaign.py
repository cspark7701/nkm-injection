#!/usr/bin/env python3
"""Round-4 (F1-F3) campaign driver: reproduction check, point candidates, error-class ablation, point test and
vertical-steering sensitivity.

Everything follows ``docs/paper/round4_protocol.json``, declared before any run. Ensembles reuse the E7 command
line (``run_capture_robustness.py``) with only the error configuration or the study configuration changed, so
particle seeds, ring identities and every non-disabled error draw stay paired with E7.

Stages:
  reproduce   bitwise reproduction of E7 realization 0 (zero jitter) with the current code      (F1)
  points      earlier and extremum-centred point configurations with root and clearance checks (F1)
  ablation    all-off, each class alone and each class omitted, zero booster jitter            (F2)
  points_test earlier and extremum-centred points at zero-jitter and full budgets              (F3)
  vertical    two-plane ideal static steering at the current point, zero-jitter and full budgets (sensitivity)

Units: m, rad; capture fractions.
"""
import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
PROTOCOL = json.loads((ROOT / 'docs/paper/round4_protocol.json').read_text())
CAMPAIGN = ROOT / PROTOCOL['campaign']
CLEARANCE_LIMIT_M = -0.018478063  # 3 sigma_x (E6) from the 2 mm blade's outer face


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def budgets():
    zero = json.loads((ROOT / PROTOCOL['budgets']['zero_jitter']).read_text())
    full = json.loads((ROOT / 'results/journal_campaign_03/error_budget.json').read_text())
    return zero, full


def class_config(base, disabled):
    """Error configuration with the listed classes disabled (standard deviations zero)."""
    cfg = dict(base)
    for name in disabled:
        for key in PROTOCOL['error_classes'][name]:
            cfg[key] = 0.0
    return cfg


def ablation_configs():
    zero, _ = budgets()
    classes = [c for c in PROTOCOL['error_classes'] if c not in ('not_applied', 'disabling_rule')]
    configs = {'all_off': class_config(zero, classes)}
    for c in classes:
        configs[f'alone_{c}'] = class_config(zero, [d for d in classes if d != c])
        configs[f'omit_{c}'] = class_config(zero, [c])
    return configs, classes


def common_args(study_config):
    p = PROTOCOL['adopted_model']
    return ['--study-config', study_config, '--optimization-summary', ROOT / p['optimization_summary'],
            '--chamber-config', ROOT / p['chamber_config'], '--corrected-ring-dir', ROOT / p['corrected_ring_dir'],
            '--kicker-models', 'fieldmap_3d', 'dipole', '--control-reference', '3d', '--timing-model', 'scale',
            '--correct-static-orbit', '--samples', '50', '--particles', '200', '--turns', '500', '--seed', '42',
            '--capture-threshold', '.8', '--resume']


def run_ensemble(name, study_config, error_config, workers, extra=()):
    out = CAMPAIGN / name
    if (out / 'capture_robustness_raw.json').exists():
        print('exists', name, flush=True)
        return
    variants = CAMPAIGN / 'inputs'
    variants.mkdir(parents=True, exist_ok=True)
    path = variants / f'{name}.json'
    if path.exists() and json.loads(path.read_text()) != error_config:
        raise SystemExit('Existing error configuration changed: ' + name)
    path.write_text(json.dumps(error_config, indent=2) + '\n')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg')
    args = [sys.executable, str(ROOT / 'scripts/run_capture_robustness.py'), *map(str, common_args(study_config)),
            '--error-config', str(path), '--output-dir', str(out), '--workers', str(workers), *extra]
    print('Running', name, flush=True)
    with (CAMPAIGN / f'{name}.log').open('a') as log:
        subprocess.run(args, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, cwd=ROOT)


def reproduce():
    """Rerun realization 0 of e7_jitter_0 with the current code and compare it field by field."""
    import run_capture_robustness as rc
    ref_dir = ROOT / PROTOCOL['references']['full_zero_jitter']
    spec = json.loads((ref_dir / 'checkpoint_inputs.json').read_text())
    job = dict(next(j for j in spec['jobs'] if j['sample']['sample_id'] == 0))
    job['checkpoint'] = None
    job['work_dir'] = str(CAMPAIGN / 'reproduce_lattice')
    new = rc.run_realization(job)
    old = json.loads((ref_dir / 'realization_0.json').read_text())
    same = {m: new['models'][m] == old['models'][m] for m in old['models']}
    result = {'reference': str(ref_dir / 'realization_0.json'), 'identical_models': same,
              'identical_bts_exit': new['bts_exit'] == old['bts_exit'],
              'captures': {m: [old['models'][m]['capture_fraction'], new['models'][m]['capture_fraction']] for m in old['models']}}
    (CAMPAIGN / 'f1_reproduction.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    if not all(same.values()) or not result['identical_bts_exit']:
        raise SystemExit('E7 realization 0 is not reproduced bitwise')


def points():
    from nkm_injection.injection_study import InjectionStudyConfig
    from nkm_injection.kickmap import NKMKickMap2D
    from run_operating_window_3d import LEVER, matched_angle_3d
    current_path = ROOT / PROTOCOL['adopted_model']['study_config_current']
    current = InjectionStudyConfig.load(current_path)
    earlier = InjectionStudyConfig.load(ROOT / 'results/journal_campaign_04/e6_operating_point/operating_point_round2.json')
    kmap = NKMKickMap2D(ROOT / current.kickmap_path)
    kick = lambda x: float(np.ravel(kmap.evaluate_kick(x, 0.0))[0])
    x_ext = float(minimize_scalar(lambda x: -abs(kick(x)), bounds=(-12e-3, -5e-3), method='bounded',
                                  options={'xatol': 1e-9}).x)

    def centroid(x):
        xp = matched_angle_3d(replace(current, injection_x_m=x), 640)
        return np.nan if xp is None else x + LEVER * xp

    x_inj = brentq(lambda x: centroid(x) - x_ext, -0.0207, -0.0209, xtol=1e-10)
    xp = matched_angle_3d(replace(current, injection_x_m=x_inj), 640)
    extremum = replace(current, injection_x_m=float(x_inj), injection_xp_rad=float(xp))
    earlier_xp = matched_angle_3d(earlier, 640)
    rows = {}
    out = CAMPAIGN / 'points'
    out.mkdir(parents=True, exist_ok=True)
    for name, cfg in (('current', current), ('earlier', earlier), ('extremum', extremum)):
        root = matched_angle_3d(cfg, 640)
        rows[name] = {'injection_x_m': cfg.injection_x_m, 'field_scale': cfg.field_scale,
                      'injection_xp_rad': cfg.injection_xp_rad, 'matched_root_rad': root,
                      'root_reproduced': bool(root is not None and abs(root - cfg.injection_xp_rad) < 1e-9),
                      'centroid_at_nkm_m': cfg.injection_x_m + LEVER * cfg.injection_xp_rad,
                      'septum_clearance_ok': bool(cfg.injection_x_m <= CLEARANCE_LIMIT_M + 1e-12)}
        if name != 'current':
            path = out / f'{name}.json'
            cfg.save(path) if hasattr(cfg, 'save') else path.write_text(json.dumps(cfg.to_dict(), indent=2) + '\n')
            rows[name]['config'] = str(path.relative_to(ROOT))
            rows[name]['config_sha256'] = sha(path)
    rows['current']['config'] = str(current_path.relative_to(ROOT))
    result = {'kick_extremum_x_m': x_ext, 'kick_extremum_rad': kick(x_ext), 'clearance_limit_m': CLEARANCE_LIMIT_M,
              'earlier_root_check_rad': earlier_xp, 'points': rows}
    (out / 'points.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=1))
    if not all(r['root_reproduced'] and r['septum_clearance_ok'] for r in rows.values()):
        raise SystemExit('A candidate point fails its root or clearance check')


def ablation(workers):
    configs, _ = ablation_configs()
    current = ROOT / PROTOCOL['adopted_model']['study_config_current']
    for name, cfg in configs.items():
        run_ensemble(f'f2_{name}', current, cfg, workers)


def points_test(workers):
    zero, full = budgets()
    pts = json.loads((CAMPAIGN / 'points/points.json').read_text())['points']
    for point in ('earlier', 'extremum'):
        for label, cfg in (('zero', zero), ('full', full)):
            run_ensemble(f'f3_{point}_{label}', ROOT / pts[point]['config'], cfg, workers)


def vertical(workers):
    """Declared sensitivity: ideal static steering in both planes at the current point (round4_protocol.json)."""
    zero, full = budgets()
    current = ROOT / PROTOCOL['adopted_model']['study_config_current']
    for label, cfg in (('zero', zero), ('full', full)):
        run_ensemble(f'f2v_xy_{label}', current, cfg, workers, extra=('--static-steering-planes', 'xy'))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--stage', required=True, choices=['reproduce', 'points', 'ablation', 'points_test', 'vertical'])
    p.add_argument('--workers', type=int, default=8)
    a = p.parse_args()
    CAMPAIGN.mkdir(parents=True, exist_ok=True)
    {'reproduce': reproduce, 'points': points, 'ablation': lambda: ablation(a.workers),
     'points_test': lambda: points_test(a.workers), 'vertical': lambda: vertical(a.workers)}[a.stage]()


if __name__ == '__main__':
    main()
