#!/usr/bin/env python3
"""E7 — capture-based tuning with matched knobs and held-out, shot-perturbed validation.

Knobs per static machine: septum position x_inj (bounded above by the declared septum-clearance limit), an angle trim
about the 3-D matched angle of the current (x_inj, S), and the field scale S. The matched angle is recomputed for every
trial, so moving x_inj does not mismatch the trajectory. Search: repeated strict-improvement coordinate sweeps
(``iterated_coordinate_search``, at most ``--max-sweeps``), 100 fresh training particles with all shot errors zero.
Held-out validation restores the joint shot errors at zero and quarter booster jitter on the paired 200-particle
samples. The fraction of machines whose optimum lies on a bound is reported. Units: m, rad.
"""
import argparse
import copy
import functools
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.injection_tuning import iterated_coordinate_search
from run_capture_robustness import cluster_stats, run_realization
from run_operating_window_3d import matched_angle_3d

SHOT_KEYS = ('booster_x_m', 'booster_xp_rad', 'energy_dp_p', 'nkm_scale_err',
             'nkm_timing_mrad', 'septum_strength_rel', 'rf_phase_rad', 'arrival_time_s')


@functools.lru_cache(maxsize=512)
def _matched(config_json, x_inj, scale):
    cfg = replace(InjectionStudyConfig.from_dict(json.loads(config_json)), injection_x_m=x_inj, field_scale=scale)
    return matched_angle_3d(cfg, 640)


def tune_machine(task):
    source = task['source']; identifier = source['sample']['sample_id']; base = copy.deepcopy(source)
    base.pop('checkpoint', None); base['models'] = ['fieldmap_3d']; base['particles'] = 100
    base['beam_seed'] = source['beam_seed'] + 100000000
    base['extra'] = {'emit_rel': 0., 'espread_abs': 0.}
    for key in SHOT_KEYS: base['sample'][key] = 0.
    cfg_json = json.dumps(base['config'], sort_keys=True)
    x0, s0 = base['config']['injection_x_m'], base['config']['field_scale']
    trim0 = base['config']['injection_xp_rad'] - _matched(cfg_json, x0, s0)

    def config_for(knobs):
        x, trim, s = (float(v) for v in knobs)
        xm = _matched(cfg_json, round(x, 9), round(s, 9))
        return None if xm is None else {'injection_x_m': x, 'injection_xp_rad': xm + trim, 'field_scale': s}

    def evaluate(knobs):
        update = config_for(knobs)
        if update is None:
            return 0.0
        job = copy.deepcopy(base); job['config'].update(update)
        return run_realization(job)['models']['fieldmap_3d']['capture_fraction']

    b = task['bounds']
    search = iterated_coordinate_search(evaluate, [x0, trim0, s0], b, task['steps'], max_sweeps=task['max_sweeps'],
                                        seed=base['beam_seed'])
    tuned = config_for(search['knobs'])
    heldout = []
    for scale in (0., .25):
        job = copy.deepcopy(source); job.pop('checkpoint', None); job['models'] = ['fieldmap_3d']
        job['sample']['booster_x_m'] *= scale; job['sample']['booster_xp_rad'] *= scale
        job['config'].update(tuned)
        result = run_realization(job)
        original = task['untuned'][str(scale)]
        assert original['beam_seed'] == result['beam_seed'] and original['ring_error_seed'] == result['ring_error_seed']
        heldout.append({'jitter_scale': scale, 'untuned': original, 'tuned': result})
    row = {'sample_id': identifier, 'training': search, 'tuned_config': tuned, 'heldout': heldout}
    path = Path(task['checkpoint']); temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(row, indent=2, allow_nan=False) + '\n'); temporary.replace(path)
    print('tuned realization', identifier, 'training capture', search['training_capture'], 'at bound', search['at_bound'], flush=True)
    return row


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--full-ensemble', type=Path, required=True)
    p.add_argument('--zero-ensemble', type=Path, required=True)
    p.add_argument('--quarter-ensemble', type=Path, required=True)
    p.add_argument('--x-max-m', type=float, required=True, help='septum-clearance upper bound on x_inj (m)')
    p.add_argument('--x-range-m', type=float, default=1.5e-3)
    p.add_argument('--trim-range-rad', type=float, default=0.5e-3)
    p.add_argument('--scale-range', type=float, nargs=2, default=[0.75, 1.05])
    p.add_argument('--steps', type=float, nargs=3, default=[0.25e-3, 0.1e-3, 0.025])
    p.add_argument('--max-sweeps', type=int, default=4)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--workers', type=int, default=8)
    p.add_argument('--resume', action='store_true')
    a = p.parse_args(); out = a.output_dir
    if out.exists() and any(out.iterdir()) and not a.resume: raise SystemExit('Output must be new')
    out.mkdir(parents=True, exist_ok=True)
    spec = json.loads((a.full_ensemble / 'checkpoint_inputs.json').read_text())
    jobs = [j for j in spec['jobs'] if j['sample']['sample_id'] >= 0]
    if len(jobs) != 50: raise ValueError('E7 tuning requires 50 machines')
    references = {str(scale): {r['sample_id']: r for r in json.loads((path / 'capture_robustness_raw.json').read_text())['realizations']}
                  for scale, path in ((0., a.zero_ensemble), (.25, a.quarter_ensemble))}
    bounds = [[a.x_max_m - a.x_range_m, a.x_max_m], [-a.trim_range_rad, a.trim_range_rad], list(a.scale_range)]
    signature = json.loads(json.dumps({'source': spec, 'references': references, 'bounds': bounds, 'steps': a.steps,
                                       'max_sweeps': a.max_sweeps,
                                       'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                       'search_sha256': hashlib.sha256(Path('src/nkm_injection/injection_tuning.py').read_bytes()).hexdigest()}))
    signature_path = out / 'tuning_inputs.json'
    if signature_path.exists() and json.loads(signature_path.read_text()) != signature: raise SystemExit('Tuning inputs changed')
    signature_path.write_text(json.dumps(signature, indent=2) + '\n')
    rows = []; tasks = []
    for job in jobs:
        identifier = job['sample']['sample_id']; path = out / f'tuning_{identifier}.json'
        if a.resume and path.exists(): rows.append(json.loads(path.read_text())); continue
        tasks.append({'source': job, 'untuned': {s: ref[identifier] for s, ref in references.items()}, 'checkpoint': str(path),
                      'bounds': bounds, 'steps': a.steps, 'max_sweeps': a.max_sweeps})
    rows += parallel_map(tune_machine, tasks, n_workers=a.workers, desc='E7 matched tuning')
    rows.sort(key=lambda r: r['sample_id']); statistics = {}
    for scale in (0., .25):
        pairs = [next(h for h in r['heldout'] if h['jitter_scale'] == scale) for r in rows]
        before = np.array([h['untuned']['models']['fieldmap_3d']['capture_fraction'] for h in pairs])
        after = np.array([h['tuned']['models']['fieldmap_3d']['capture_fraction'] for h in pairs]); diff = after - before
        rng = np.random.default_rng(1729); boot = diff[rng.integers(0, len(diff), (10000, len(diff)))].mean(axis=1)
        statistics[str(scale)] = {'untuned': cluster_stats(before, 1729, 10000, .8), 'tuned': cluster_stats(after, 1729, 10000, .8),
                                  'paired_gain': float(diff.mean()), 'gain_ci95': np.quantile(boot, [.025, .975]).tolist()}
    at_bound = np.array([r['training']['at_bound'] for r in rows])
    result = {'rows': rows, 'statistics': statistics, 'training_particles': 100, 'heldout_particles': jobs[0]['particles'],
              'bounds': bounds, 'steps': a.steps, 'max_sweeps': a.max_sweeps,
              'boundary_fraction': {'x_inj': float(at_bound[:, 0].mean()), 'angle_trim': float(at_bound[:, 1].mean()),
                                    'field_scale': float(at_bound[:, 2].mean()), 'any': float(at_bound.any(axis=1).mean())},
              'evaluations_per_machine': [len(r['training']['evaluations']) for r in rows],
              'training_scope': 'static-machine errors only; independent training particles; all shot errors zero',
              'validation_scope': 'same held-out particles and joint error draws as zero/quarter-jitter ensembles',
              'optimizer': 'iterated strict-improvement coordinate sweeps with re-matched angle; declared sweep budget',
              'bootstrap': {'unit': 'joint realization', 'seed': 1729, 'count': 10000},
              'units': 'x m, canonical angle trim rad, field scale dimensionless'}
    (out / 'tuning_summary.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__': main()
