#!/usr/bin/env python3
"""Round-four BTS stages (consolidated R4-BTS tasks). SI units; new output directory per stage.

Stages:
  jitter      booster betatron-jitter level sweep, analytic loss on steered realizations (R4-BTS-01)
  blade       blade-distance sweep at two jitter levels, analytic loss (R4-BTS-02)
  phase_scan  constrained phase-advance scan and edge search for both exit targets (R4-BTS-05)
  layouts     steering with reduced monitors and series-powered bends, tracked (R4-BTS-10)
  final_test  fresh tracked test of the frozen settings, including scan_best and free_best (R4-BTS-05/12)
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares, minimize
import at

from nkm_injection.bts_journal import JournalBeam, LOWER, SCALES, UPPER, draw_static, independent_maps, lattice_for
from nkm_injection.bts_round2 import spatial_profile
from nkm_injection.optics import DEFAULT_BTS_ENTRANCE_TWISS
from nkm_injection import bts_round3 as r3
from nkm_injection import bts_round4 as r4

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'docs/paper_bts'
PROTOCOL = json.loads((PAPER / 'round4_protocol.json').read_text())
R3_PROTOCOL = json.loads((PAPER / 'round3_protocol.json').read_text())
R3_CAMPAIGN = ROOT / 'results/bts_journal_campaign_r3b_20261015'
_spec = importlib.util.spec_from_file_location('run_bts_round3', ROOT / 'scripts/run_bts_round3.py')
R3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R3)
SOURCES = ['src/nkm_injection/bts_round3.py', 'src/nkm_injection/bts_round4.py', 'src/nkm_injection/bts_journal.py',
           'scripts/run_bts_round3.py', 'scripts/run_bts_round4.py', 'docs/paper_bts/round3_protocol.json',
           'docs/paper_bts/round4_protocol.json']
save, interval, model_from_protocol = R3.save, R3.interval, R3.model_from_protocol


def environment():
    env = R3.environment()
    env['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    return env


def frozen_designs(names, extra=None):
    """Frozen strengths [m^-2] by name: round-2 reference/low beta, round-3 robust, round-4 scan settings."""
    robust = json.loads((R3_CAMPAIGN / 'robust/robust.json').read_text())['designs']
    table = {n: np.array(robust[n]['strengths_m_minus2']) for n in ('reference', 'low_beta', 'robust')}
    table.update(extra or {})
    return {n: table[n] for n in names}


# --------------------------------------------------------------------------- machines
def _machine(job):
    """One static error realization and its shots for every design and steering layout."""
    (machine, designs, layouts, seeds, shots, particles, track, jitter, model_override) = job
    beam, model = JournalBeam(), model_from_protocol(model_override)
    tw = DEFAULT_BTS_ENTRANCE_TWISS
    static_rng = np.random.default_rng([seeds['static'], machine])
    shot_rng = np.random.default_rng([seeds['shot'], machine])
    particle_rng = np.random.default_rng([seeds['particle'], machine]) if track else None
    errors = draw_static(static_rng, lattice_for(next(iter(designs.values()))))
    lines = {}
    for d_index, (name, k) in enumerate(designs.items()):
        machine_line = r3.aperture_lattice(k, errors, model)
        model_line = r3.aperture_lattice(k, None, model)
        candidates = r4.layout_monitors(model_line, r4.LAYOUTS['full'])
        reading_error = dict(zip(candidates, np.random.default_rng([seeds['bpm'], machine, d_index]).normal(
            0, R3_PROTOCOL['steering']['bpm_error_m'], len(candidates))))
        for layout in layouts:
            if layout == 'uncorrected':
                lines[(name, layout)] = (machine_line, np.zeros(1))
                continue
            response = r4.layout_response(model_line, r4.LAYOUTS[layout])
            bpm = np.array([reading_error[p] for p in response[1]])
            lines[(name, layout)] = r4.correct_with_layout(machine_line, response, bpm, R3_PROTOCOL['steering'])
    table = {key: r3.aperture_table(line) for key, (line, _) in lines.items()}
    # Exact average over Gaussian entrance jitter on each steered line, without shot sampling.
    total = beam.covariance()[:5, :5] + r3.entrance_jitter_covariance(jitter)
    integrated = {key: r3.clearance_and_loss(line, np.zeros(5), total, table=table[key])['loss_lower']
                  for key, (line, _) in lines.items()}
    rows = []
    for shot in range(shots):
        factors = 1 + shot_rng.normal(0, .05, 2)
        dx, px, dp = shot_rng.normal(0, [jitter['x_m'], jitter['xp_rad'], jitter['delta']])
        centroid = np.array([dx + tw.disp_x * dp, px + tw.disp_px * dp, 0, 0, dp])
        cov = beam.covariance(factors)
        sample = None
        if track:
            sample = particle_rng.multivariate_normal(np.zeros(6), cov, particles).T
            sample[:5] += centroid[:, None]
        row = {'shot': shot, 'centroid': centroid, 'results': {}}
        for (name, layout), (line, kicks) in lines.items():
            rec = r3.clearance_and_loss(line, centroid, cov, table=table[(name, layout)])
            entry = {'clearance_m': rec['minimum_m'], 'active': rec['active'], 'loss_max': rec['loss_lower'],
                     'loss_union': rec['loss_union'], 'exit_centroid': rec['exit_centroid'][:4],
                     'kick_rms_rad': float(np.sqrt(np.mean(np.square(kicks))))}
            if track:
                out = at.lattice_track(line, np.array(sample, order='F'), nturns=1, refpts=np.arange(len(line) + 1))[0][:, :, :, 0]
                lost = ~np.isfinite(out[0, :, -1])
                first = Counter()
                for p in np.flatnonzero(lost):
                    first[line[int(np.flatnonzero(~np.isfinite(out[0, p]))[0]) - 1].FamName] += 1
                entry.update({'lost': int(lost.sum()), 'first_losses': dict(first)})
            row['results'].setdefault(name, {})[layout] = entry
        rows.append(row)
    return {'machine': machine, 'shots': rows,
            'jitter_integrated_loss': {name: {layout: integrated[(name, layout)] for (n, layout) in lines if n == name}
                                       for name in designs}}


def campaign(designs, layouts, config, track, workers, jitter=None, model_override=None):
    seeds = {'static': config['static_seed'], 'shot': config['shot_seed'], 'particle': config.get('particle_seed', 0),
             'bpm': config['bpm_seed']}
    jitter = {**r3.JITTER, **(jitter or {})}
    jobs = [(m, designs, layouts, seeds, config['shots_per_machine'], config.get('particles_per_shot', 0), track,
             jitter, model_override) for m in range(config['machines'])]
    with Pool(workers) as pool:
        return pool.map(_machine, jobs, chunksize=1)


def summarise(raw, designs, layouts, reference, seed, particles=0):
    """Per layout and design: clearance, loss predictions, exit centroids (x, x', y, y') and tracked losses."""
    out = {}
    for layout in layouts:
        for name in designs:
            shots = [s['results'][name][layout] for m in raw for s in m['shots']]
            exits = np.array([s['exit_centroid'] for s in shots])
            per = lambda key, d=name: np.array([np.mean([s['results'][d][layout][key] for s in m['shots']]) for m in raw])
            entry = {'mean_clearance_m': float(np.mean([s['clearance_m'] for s in shots])),
                     'mean_exit_centroid_m_rad': exits.mean(0).tolist(),
                     'exit_centroid_rms_m_rad': np.sqrt(np.mean(exits ** 2, 0)).tolist(),
                     'predicted_loss_max_mean': float(np.mean([s['loss_max'] for s in shots])),
                     'predicted_loss_union_mean': float(np.mean([s['loss_union'] for s in shots])),
                     'paired_predicted_vs_reference': interval(per('loss_max') - per('loss_max', reference), seed),
                     'jitter_integrated_loss_mean': float(np.mean([m['jitter_integrated_loss'][name][layout] for m in raw])),
                     'kick_rms_rad': float(np.mean([s['kick_rms_rad'] for s in shots])),
                     'active': dict(Counter(s['active'][0] + ('_x' if s['active'][1] == 0 else '_y') for s in shots))}
            if particles:
                lost = per('lost') / particles
                first = Counter()
                for s in shots:
                    first.update(s['first_losses'])
                entry.update({'lost_particles': int(sum(s['lost'] for s in shots)),
                              'observed_loss_fraction': float(np.mean([s['lost'] for s in shots]) / particles),
                              'loss_blocks': int(sum(any(s['results'][name][layout]['lost'] for s in m['shots']) for m in raw)),
                              'first_loss_families': dict(first),
                              'paired_tracked_vs_reference': interval(lost - per('lost', reference) / particles, seed)})
            out.setdefault(layout, {})[name] = entry
    return out


# --------------------------------------------------------------------------- jitter (R4-BTS-01)
def error_free_loss(k, jitter, model_override=None):
    return r3.shot_averaged_loss(r3.aperture_lattice(k, model=model_from_protocol(model_override)), jitter=jitter)['loss_lower']


def jitter_stage(output, workers):
    config = PROTOCOL['jitter']
    designs = frozen_designs(config['designs'])
    rows = []
    for scale in config['scales']:
        jitter = {'x_m': r3.JITTER['x_m'] * scale, 'xp_rad': r3.JITTER['xp_rad'] * scale}
        raw = campaign(designs, ['full'], config, False, workers, jitter)
        summary = summarise(raw, designs, ['full'], 'reference', config['bootstrap_seed'])['full']
        rows.append({'scale': scale, 'jitter': jitter,
                     'designs': {n: {**summary[n], 'error_free_loss': error_free_loss(k, jitter),
                                     'exit_jitter_m_rad': np.sqrt(np.diag(r3.jitter_transfer(r3.phase_advance(lattice_for(k))[0], jitter))).tolist()}
                                 for n, k in designs.items()}})
        print(scale, {n: (f"{e['predicted_loss_max_mean']:.3e}", f"{e['jitter_integrated_loss_mean']:.3e}", f"{e['error_free_loss']:.3e}")
                      for n, e in rows[-1]['designs'].items()}, flush=True)
    beam = JournalBeam()
    tw = DEFAULT_BTS_ENTRANCE_TWISS
    units = {'m1_beam_size_m': float(np.sqrt(beam.covariance()[0, 0])), 'm1_beam_divergence_rad': float(np.sqrt(beam.covariance()[1, 1])),
             'm4_beam_size_m': r3.boundary_sigma(r3.EXIT_TWISS['beta_x'], beam.emit_x_m_rad, r3.EXIT_TWISS['disp_x'], beam.sigma_delta),
             'centroid_action_over_emittance': float(((1 + tw.alpha_x ** 2) / tw.beta_x * r3.JITTER['x_m'] ** 2
                                                      + tw.beta_x * r3.JITTER['xp_rad'] ** 2) / beam.emit_x_m_rad)}
    save(output / 'jitter.json', {'environment': environment(), 'protocol': config, 'beam_units': units, 'rows': rows})


# --------------------------------------------------------------------------- blade (R4-BTS-02)
def blade_stage(output, workers):
    config, jconfig = PROTOCOL['blade'], PROTOCOL['jitter']
    designs = frozen_designs(config['designs'])
    rows = []
    for scale in config['jitter_scales']:
        jitter = {'x_m': r3.JITTER['x_m'] * scale, 'xp_rad': r3.JITTER['xp_rad'] * scale}
        for d_b in config['blade_distance_m']:
            override = {'septum_ex_blade': d_b}
            raw = campaign(designs, ['full'], jconfig, False, workers, jitter, override)
            summary = summarise(raw, designs, ['full'], 'reference', jconfig['bootstrap_seed'])['full']
            rows.append({'jitter_scale': scale, 'blade_distance_m': d_b,
                         'designs': {n: {'steered_loss': summary[n]['predicted_loss_max_mean'],
                                         'jitter_integrated_loss': summary[n]['jitter_integrated_loss_mean'],
                                         'error_free_loss': error_free_loss(k, jitter, override),
                                         'mean_clearance_m': summary[n]['mean_clearance_m']} for n, k in designs.items()}})
            print(scale, d_b, {n: (f"{e['steered_loss']:.3e}", f"{e['jitter_integrated_loss']:.3e}") for n, e in rows[-1]['designs'].items()}, flush=True)
    tolerance = {}
    for scale in config['jitter_scales']:
        for name in designs:
            pts = [(r['blade_distance_m'], r['designs'][name]['jitter_integrated_loss']) for r in rows if r['jitter_scale'] == scale]
            tolerance.setdefault(str(scale), {})[name] = _crossing(pts, config['tolerance_loss'])
    save(output / 'blade.json', {'environment': environment(), 'protocol': config, 'rows': rows,
                                 'distance_for_tolerance_m': tolerance})
    print(tolerance)


def _crossing(points, level):
    """Smallest blade distance [m] at which the loss falls to ``level``, log-linear interpolation; None if outside."""
    points = sorted(points)
    if points[0][1] <= level:
        return {'distance_m': points[0][0], 'bound': 'at or below the smallest swept distance'}
    for (d0, p0), (d1, p1) in zip(points, points[1:]):
        if p1 <= level < p0:
            if p1 <= 0:
                return {'distance_m': d1, 'bound': 'upper'}
            f = (np.log(level) - np.log(p0)) / (np.log(p1) - np.log(p0))
            return {'distance_m': float(d0 + f * (d1 - d0)), 'bound': 'interpolated'}
    return {'distance_m': None, 'bound': 'above the largest swept distance'}


# --------------------------------------------------------------------------- phase scan (R4-BTS-05)
def _scan_point(job):
    label, mu_deg, starts, target = job
    mu, found = np.radians(mu_deg), []
    for start in starts:
        res = least_squares(r4.phase_residual, np.asarray(start), args=(target, SCALES, mu), bounds=(LOWER, UPPER),
                            xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=3000)
        if np.max(np.abs(r4.phase_residual(res.x, target, SCALES, mu))) < 1e-4:
            found.append(res.x)
    if not found:
        return {'target': label, 'mu_x_deg': mu_deg, 'matched': 0}
    rows = []
    for k in found:
        peaks = spatial_profile(lattice_for(k), 16)['peak_beta_m']
        rows.append((max(peaks), k, peaks))
    best_peak, k, peaks = min(rows, key=lambda r: r[0])
    m = independent_maps(lattice_for(k))[0][-1]
    jit = m @ r3.entrance_jitter_covariance() @ m.T
    return {'target': label, 'mu_x_deg': mu_deg, 'matched': len(found), 'strengths_m_minus2': k, 'peak_beta_m': peaks,
            'feasible': bool(best_peak <= 60.0), 'active_bounds': r4.active_bounds(k, LOWER, UPPER),
            'loss_max': error_free_loss(k, None), 'exit_jitter_x_m': float(np.sqrt(jit[0, 0])),
            'exit_jitter_xp_rad': float(np.sqrt(jit[1, 1]))}


def _edge(job):
    label, sign, start, target = job
    peak = lambda k: 60.0 - np.array(spatial_profile(lattice_for(k), 16)['peak_beta_m'])
    res = minimize(lambda k: sign * r3.phase_advance(lattice_for(k))[0], np.asarray(start), method='SLSQP',
                   bounds=list(zip(LOWER, UPPER)),
                   constraints=[{'type': 'eq', 'fun': lambda k: R3._residual(k, target)}, {'type': 'ineq', 'fun': peak}],
                   options={'maxiter': 300, 'ftol': 1e-12})
    k = res.x
    residual = float(np.max(np.abs(R3._residual(k, target))))
    peaks = spatial_profile(lattice_for(k), 16)['peak_beta_m']
    return {'target': label, 'direction': 'min' if sign > 0 else 'max', 'mu_x_deg': float(np.degrees(r3.phase_advance(lattice_for(k))[0])),
            'matched': residual < 1e-3, 'max_scaled_residual': residual, 'strengths_m_minus2': k, 'peak_beta_m': peaks,
            'active_bounds': r4.active_bounds(k, LOWER, UPPER, 1e-5), 'peak_beta_active': [bool(p > 59.99) for p in peaks],
            'iterations': int(res.nit), 'termination': str(res.message), 'success': bool(res.success)}


def phase_scan(output, workers):
    config = PROTOCOL['phase_scan']
    pools = json.loads((R3_CAMPAIGN / 'phase/phase.json').read_text())['pools']
    rng = np.random.default_rng(config['random_seed'])
    targets = {k: np.array(v) for k, v in R3_PROTOCOL['exit_targets'].items()}
    jobs, edge_jobs = [], []
    for label, (lo, hi, step) in config['grid_deg'].items():
        pool = pools[label]['rows']
        for mu in np.arange(lo, hi + 0.5 * step, step):
            near = sorted(pool, key=lambda r: abs(r['mu_x_deg'] - mu))[:6]
            starts = [np.array(r['strengths_m_minus2']) for r in near] + [rng.uniform(LOWER, UPPER) for _ in range(10)]
            jobs.append((label, float(mu), starts, targets[label]))
        ordered = sorted(pool, key=lambda r: r['mu_x_deg'])
        edge_jobs += [(label, 1.0, np.array(r['strengths_m_minus2']), targets[label]) for r in ordered[:5]]
        edge_jobs += [(label, -1.0, np.array(r['strengths_m_minus2']), targets[label]) for r in ordered[-5:]]
    with Pool(workers) as pool:
        rows = pool.map(_scan_point, jobs, chunksize=1)
        edges = pool.map(_edge, edge_jobs, chunksize=1)
    chosen = {}
    for label, key in (('configured', 'scan_best'), ('dispersion_free', 'free_best')):
        feasible = [r for r in rows if r['target'] == label and r.get('feasible')]
        chosen[key] = min(feasible, key=lambda r: r['loss_max'])
    save(output / 'phase_scan.json', {'environment': environment(), 'protocol': config, 'rows': rows, 'edges': edges,
                                      'chosen': chosen, 'frozen_before_test': True})
    for label in config['grid_deg']:
        ok = [r['mu_x_deg'] for r in rows if r['target'] == label and r['matched']]
        print(label, 'matched grid range', (min(ok), max(ok)) if ok else None)
    for e in edges:
        print(e['target'], e['direction'], round(e['mu_x_deg'], 2), e['matched'], e['active_bounds'], e['peak_beta_active'])
    print({k: (v['mu_x_deg'], v['loss_max'], v['peak_beta_m']) for k, v in chosen.items()})


# --------------------------------------------------------------------------- layouts (R4-BTS-10)
def layouts_stage(output, workers):
    config = PROTOCOL['steering_layouts']
    designs = frozen_designs(config['designs'])
    raw = campaign(designs, config['layouts'], config, True, workers)
    summary = summarise(raw, designs, config['layouts'], 'reference', config['bootstrap_seed'], config['particles_per_shot'])
    r3_row = json.loads((R3_CAMPAIGN / 'steering/steering.json').read_text())['summary']['corrected']['reference']
    check = {'round3_lost_particles': r3_row['lost_particles'], 'full_lost_particles': summary['full']['reference']['lost_particles'],
             'round3_predicted': r3_row['predicted_loss_max_mean'], 'full_predicted': summary['full']['reference']['predicted_loss_max_mean']}
    save(output / 'raw_machines.json', raw)
    save(output / 'layouts.json', {'environment': environment(), 'protocol': config, 'summary': summary,
                                   'reproduction_check': check, 'interval_scope': 'pointwise 95 % realization-cluster percentile bootstrap'})
    print(json.dumps(check))
    for layout, d in summary.items():
        print(layout, {n: (round(e['observed_loss_fraction'] * 100, 3), [round(x * 1e3, 3) for x in e['exit_centroid_rms_m_rad']])
                       for n, e in d.items()})


# --------------------------------------------------------------------------- final test (R4-BTS-05/12)
def final_test(output, workers, scan_file):
    config = PROTOCOL['final_test']
    chosen = json.loads(scan_file.read_text())['chosen']
    designs = frozen_designs(config['designs'], {k: np.array(v['strengths_m_minus2']) for k, v in chosen.items()})
    raw = campaign(designs, ['full'], config, True, workers)
    summary = summarise(raw, designs, ['full'], 'reference', config['bootstrap_seed'], config['particles_per_shot'])['full']
    save(output / 'raw_machines.json', raw)
    save(output / 'final_test.json', {'environment': environment(), 'protocol': config,
                                      'scan_sha256': hashlib.sha256(scan_file.read_bytes()).hexdigest(),
                                      'summary': summary, 'interval_scope': 'pointwise 95 % realization-cluster percentile bootstrap'})
    for n, e in summary.items():
        print(n, round(e['observed_loss_fraction'] * 100, 3), round(e['predicted_loss_max_mean'] * 100, 3),
              e['paired_tracked_vs_reference'], e['first_loss_families'])


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--stage', required=True, choices=['jitter', 'blade', 'phase_scan', 'layouts', 'final_test'])
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--scan-file', type=Path)
    p.add_argument('--workers', type=int, default=8)
    a = p.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=False)
    save(a.output_dir / 'configuration.json', {'stage': a.stage, 'protocol': PROTOCOL, 'environment': environment(),
                                               'scan_file': str(a.scan_file) if a.scan_file else None})
    {'jitter': lambda: jitter_stage(a.output_dir, a.workers), 'blade': lambda: blade_stage(a.output_dir, a.workers),
     'phase_scan': lambda: phase_scan(a.output_dir, a.workers), 'layouts': lambda: layouts_stage(a.output_dir, a.workers),
     'final_test': lambda: final_test(a.output_dir, a.workers, a.scan_file)}[a.stage]()


if __name__ == '__main__':
    main()
