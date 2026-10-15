#!/usr/bin/env python3
"""Round-three BTS stages for Reviewer 2 (R2B-01 to R2B-06). SI units; new output directory per stage.

Stages:
  apertures    element-wise aperture model: nominal clearances, active restriction, parametric sweeps (R2B-01)
  phase        multistart matching pools: reachable phase advances and the jitter-transfer trade-off (R2B-04/05)
  steering     uncorrected versus corrected machines, reference and low-beta settings (R2B-03)
  robust       loss-based design, frozen before testing (R2B-04)
  test         fresh corrected machines for reference, low beta and robust settings (R2B-04)
  exit         exit divergence budget and the dispersion-free exit target (R2B-05)
  sensitivity  roll and energy-jitter levels, analytic loss and clearance (R2B-06)
"""
import argparse
from collections import Counter
import hashlib
import json
from multiprocessing import Pool
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.optimize import least_squares, minimize
from scipy.stats import norm
import at

from nkm_injection.bts_journal import JournalBeam, LOWER, SCALES, TARGET, UPPER, draw_static, lattice_for
from nkm_injection.bts_round2 import nominal_observables, spatial_profile
from nkm_injection import bts_round3 as r3

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'docs/paper_bts'
PROTOCOL = json.loads((PAPER / 'round3_protocol.json').read_text())
SOURCES = ['src/nkm_injection/bts_round3.py', 'src/nkm_injection/bts_round2.py', 'src/nkm_injection/bts_journal.py',
           'scripts/run_bts_round3.py', 'docs/paper_bts/round3_protocol.json']


def serial(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    raise TypeError(type(x).__name__)


def save(path, data):
    path.write_text(json.dumps(data, indent=2, default=serial, allow_nan=False) + '\n')


def environment():
    return {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__, 'pyat': at.__version__,
            'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}}


def settings():
    """Frozen round-2 reference and refined low-beta strengths [m^-2]."""
    designs = json.loads((PAPER / 'generated/round2_designs.json').read_text())['designs']['baseline']['nominal']
    low = json.loads((PAPER / 'generated/round2_spatial.json').read_text())['refined_low_beta']['strengths_m_minus2']
    return {'reference': np.array(designs['reference']['strengths_m_minus2']), 'low_beta': np.array(low)}


def model_from_protocol(overrides=None):
    a = PROTOCOL['aperture_model']
    model = {'pipe_radius': a['pipe_radius_m'], 'quad_bore_radius': a['quad_bore_radius_m'],
             'kicker_half': tuple(a['kicker_half_m']), 'dipole_half': tuple(a['dipole_half_m']),
             'septum_in_half': tuple(a['septum_in_half_m']), 'septum_ex_blade': a['septum_ex_blade_m'],
             'septum_ex_outer': a['septum_ex_outer_m'], 'septum_ex_half_y': a['septum_ex_half_y_m'],
             'slices_quad': a['slices_quad'], 'slices_bend': a['slices_bend']}
    model.update(overrides or {})
    return model


def interval(delta, seed, count=10000):
    rng = np.random.default_rng(seed)
    delta = np.asarray(delta, dtype=float)
    means = delta[rng.integers(0, len(delta), (count, len(delta)))].mean(1)
    return {'mean': float(delta.mean()), 'ci95': np.quantile(means, [.025, .975]).tolist()}


# --------------------------------------------------------------------------- apertures (R2B-01)
def apertures(output):
    beam, model = JournalBeam(), model_from_protocol()
    result = {'environment': environment(), 'model': model, 'units': 'm', 'designs': {}, 'sweeps': []}
    result['sagitta_m'] = r3.bend_sagitta(lattice_for(settings()['reference']))
    for name, k in settings().items():
        line = r3.elementwise_lattice(k, model=model)
        record = r3.clearance_and_loss(line, np.zeros(5), beam.covariance())
        families = {}
        for row in record['rows']:
            key = row['name'] + ('_x' if row['plane'] == 0 else '_y')
            families[key] = min(families.get(key, np.inf), row['clearance_m'])
        interior = {k_: v for k_, v in families.items() if not k_.startswith(('sept', 'blade', 'kext'))}
        result['designs'][name] = {'strengths_m_minus2': k, 'minimum_m': record['minimum_m'], 'active': record['active'],
                                   'family_minimum_m': families, 'interior_minimum_m': min(interior.values()),
                                   'interior_active': min(interior, key=interior.get), 'profile': record['rows'],
                                   'apertures': r3.aperture_table(line)}
    for key, values in PROTOCOL['aperture_sweeps'].items():
        for v in values:
            override = {'dipole_half_gap_m': {'dipole_half': (model['dipole_half'][0], v)},
                        'septum_in_half_x_m': {'septum_in_half': (v, model['septum_in_half'][1])},
                        'septum_ex_blade_m': {'septum_ex_blade': v}}[key]
            for name, k in settings().items():
                record = r3.clearance_and_loss(r3.elementwise_lattice(k, model=model_from_protocol(override)), np.zeros(5), beam.covariance())
                result['sweeps'].append({'parameter': key, 'value_m': v, 'design': name, 'minimum_m': record['minimum_m'],
                                         'active': record['active']})
    save(output / 'apertures.json', result)
    print(json.dumps({n: (round(d['minimum_m'] * 1e3, 3), d['active'], d['interior_active'], round(d['interior_minimum_m'] * 1e3, 3))
                      for n, d in result['designs'].items()}))


# --------------------------------------------------------------------------- phase (R2B-04/05)
def _residual(k, target):
    return (nominal_observables(lattice_for(k)) - target) / SCALES


def _multistart(job):
    seed, starts, target = job
    rng, out = np.random.default_rng(seed), []
    for _ in range(starts):
        r = least_squares(_residual, rng.uniform(LOWER, UPPER), args=(target,), bounds=(LOWER, UPPER),
                          xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=3000)
        if np.max(np.abs(_residual(r.x, target))) < 1e-4:
            out.append(r.x)
    return out


def _tradeoff(k):
    """Shot-averaged blade loss and exit jitter of a matched setting (error-free line)."""
    lat = lattice_for(k)
    mux, muy = r3.phase_advance(lat)
    loss = r3.shot_averaged_loss(r3.elementwise_lattice(k, model=model_from_protocol(), correctors=False))
    jit = r3.jitter_transfer(mux)
    peaks = spatial_profile(lat, 16)['peak_beta_m']
    return {'strengths_m_minus2': k, 'mu_x_deg': np.degrees(mux), 'mu_y_deg': np.degrees(muy),
            'loss_max': loss['loss_lower'], 'loss_union': loss['loss_union'], 'active': loss['active'],
            'exit_jitter_x_m': float(np.sqrt(jit[0, 0])), 'exit_jitter_xp_rad': float(np.sqrt(jit[1, 1])),
            'peak_beta_m': peaks}


def phase(output, workers):
    m = PROTOCOL['multistart']
    pools = {}
    for label, seeds, starts, target in [('configured', m['seeds'], m['starts_per_seed'], np.array(PROTOCOL['exit_targets']['configured'])),
                                         ('dispersion_free', m['dispersion_free_seeds'], m['dispersion_free_starts_per_seed'],
                                          np.array(PROTOCOL['exit_targets']['dispersion_free']))]:
        with Pool(workers) as pool:
            found = [k for chunk in pool.map(_multistart, [(s, starts, target) for s in seeds]) for k in chunk]
        if label == 'configured':
            with Pool(workers) as pool:
                rows = pool.map(_tradeoff, found)
        else:
            rows = []
            for k in found:
                mux, muy = r3.phase_advance(lattice_for(k))
                rows.append({'strengths_m_minus2': k, 'mu_x_deg': np.degrees(mux), 'mu_y_deg': np.degrees(muy),
                             'peak_beta_m': spatial_profile(lattice_for(k), 16)['peak_beta_m']})
        pools[label] = {'starts': len(seeds) * starts, 'solutions': len(found), 'rows': rows,
                        'mu_x_range_deg': [min(r['mu_x_deg'] for r in rows), max(r['mu_x_deg'] for r in rows)] if rows else None}
    curve = []
    for mu in np.radians(np.arange(0.0, 360.5, 1.0)):
        jit = r3.jitter_transfer(mu)
        curve.append({'mu_x_deg': float(np.degrees(mu)), 'exit_jitter_x_m': float(np.sqrt(jit[0, 0])),
                      'exit_jitter_xp_rad': float(np.sqrt(jit[1, 1]))})
    save(output / 'phase.json', {'environment': environment(), 'pools': pools, 'analytic_curve': curve,
                                 'scope': 'Bounded multistart, not a proof of global reachability; jitter transfer for matched ends.'})
    print({k: (v['solutions'], v['mu_x_range_deg']) for k, v in pools.items()})


# --------------------------------------------------------------------------- campaigns (R2B-03/04/06)
def _machine(job):
    """Evaluate one static machine and its shots for every design and variant."""
    (machine, designs, variants, seeds, shots, particles, track, error_scale, jitter) = job
    beam, model = JournalBeam(), model_from_protocol()
    static_rng = np.random.default_rng([seeds['static'], machine])
    shot_rng = np.random.default_rng([seeds['shot'], machine])
    particle_rng = np.random.default_rng([seeds['particle'], machine]) if track else None
    errors = draw_static(static_rng, lattice_for(next(iter(designs.values()))))
    errors['roll'] = errors['roll'] * error_scale.get('roll', 1.0)
    lines = {}
    layouts = {'declared': {}, 'amended': {'corrector_before': r3.AMENDED_CORRECTORS, 'monitor_before': r3.AMENDED_MONITORS}}
    for name, k in designs.items():
        built = {}
        for layout, kwargs in layouts.items():
            nominal = r3.elementwise_lattice(k, None, model, **kwargs)
            response = r3.response_matrix(nominal)
            # Same BPM error draw per monitor position for both layouts (the extra monitor is drawn last).
            draws = np.random.default_rng([seeds['bpm'], machine, list(designs).index(name)]).normal(
                0, PROTOCOL['steering']['bpm_error_m'], (12, 2))
            bpm_errors = draws[:len(response[1])]
            built[layout] = (r3.elementwise_lattice(k, errors, model, **kwargs), response, bpm_errors)
        for variant in variants:
            if variant == 'uncorrected':
                line, response, _ = built['declared']
                lines[(name, variant)] = (line, np.zeros(2 * len(response[2])))
            else:
                line, response, bpm_errors = built['declared' if variant == 'corrected' else 'amended']
                lines[(name, variant)] = r3.correct_trajectory(line, response, bpm_errors, PROTOCOL['steering'])
    shot_rows = []
    table = {key: r3.aperture_table(line) for key, (line, _) in lines.items()}
    for shot in range(shots):
        factors = 1 + shot_rng.normal(0, .05, 2)
        dx, px, dp = shot_rng.normal(0, [jitter['x_m'], jitter['xp_rad'], jitter['delta']])
        centroid = np.array([dx + .2762 * dp, px - .0657 * dp, 0, 0, dp])
        cov = beam.covariance(factors)
        sample = None
        if track:
            sample = particle_rng.multivariate_normal(np.zeros(6), cov, particles).T
            sample[:5] += centroid[:, None]
        row = {'shot': shot, 'centroid': centroid, 'beta_factors': factors, 'results': {}}
        for (name, variant), (line, kicks) in lines.items():
            rec = r3.clearance_and_loss(line, centroid, cov, table=table[(name, variant)])
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
            row['results'].setdefault(name, {})[variant] = entry
        shot_rows.append(row)
    return {'machine': machine, 'static_errors': errors, 'shots': shot_rows}


def campaign(designs, variants, config, track, workers, error_scale=None, jitter=None):
    seeds = {'static': config['static_seed'], 'shot': config['shot_seed'], 'particle': config.get('particle_seed', 0),
             'bpm': config['bpm_seed']}
    jitter = {**r3.JITTER, **(jitter or {})}
    jobs = [(m, designs, variants, seeds, config['shots_per_machine'], config.get('particles_per_shot', 0), track,
             error_scale or {}, jitter) for m in range(config['machines'])]
    with Pool(workers) as pool:
        return pool.map(_machine, jobs, chunksize=1)


def summarise(raw, designs, variants, reference, seed, track):
    out = {}
    for variant in variants:
        base = np.array([np.mean([s['results'][reference][variant]['clearance_m'] for s in m['shots']]) for m in raw])
        for name in designs:
            values = np.array([np.mean([s['results'][name][variant]['clearance_m'] for s in m['shots']]) for m in raw])
            shots = [s['results'][name][variant] for m in raw for s in m['shots']]
            exit_x = np.array([s['exit_centroid'][0] for s in shots])
            exit_xp = np.array([s['exit_centroid'][1] for s in shots])
            entry = {'mean_clearance_m': float(values.mean()), 'paired_vs_reference_m': interval(values - base, seed),
                     'predicted_loss_max_mean': float(np.mean([s['loss_max'] for s in shots])),
                     'predicted_loss_union_mean': float(np.mean([s['loss_union'] for s in shots])),
                     'active': dict(Counter(s['active'][0] + ('_x' if s['active'][1] == 0 else '_y') for s in shots)),
                     'exit_centroid_rms_m_rad': [float(np.sqrt(np.mean(exit_x ** 2))), float(np.sqrt(np.mean(exit_xp ** 2)))],
                     'kick_rms_rad': float(np.mean([s['kick_rms_rad'] for s in shots]))}
            if track:
                lost = np.array([s['lost'] for s in shots])
                n = len(shots) * raw[0]['shots'][0].get('particles', 1)
                blocks = [any(s['results'][name][variant]['lost'] for s in m['shots']) for m in raw]
                first = Counter()
                for s in shots:
                    first.update(s['first_losses'])
                machine_loss = np.array([np.mean([s['results'][name][variant]['lost'] for s in m['shots']]) for m in raw])
                machine_pred = np.array([np.mean([s['results'][name][variant]['loss_max'] for s in m['shots']]) for m in raw])
                entry.update({'lost_particles': int(lost.sum()), 'loss_blocks': int(sum(blocks)), 'first_loss_families': dict(first),
                              'machine_loss_per_shot_mean': interval(machine_loss, seed), 'machine_predicted_max_per_shot': float(machine_pred.mean())})
            out.setdefault(variant, {})[name] = entry
    return out


def steering(output, workers):
    config = PROTOCOL['steering_campaign']
    designs = {k: v for k, v in settings().items() if k in config['designs']}
    raw = campaign(designs, config['variants'], config, True, workers)
    summary = summarise(raw, designs, config['variants'], 'reference', config['bootstrap_seed'], True)
    particles = config['particles_per_shot']
    for variant in summary.values():
        for entry in variant.values():
            entry['observed_loss_fraction'] = entry['lost_particles'] / (config['machines'] * config['shots_per_machine'] * particles)
            entry['predicted_loss_max_particles'] = entry['predicted_loss_max_mean'] * config['machines'] * config['shots_per_machine'] * particles
    # Corrected minus uncorrected, per design, paired by machine.
    effect = {}
    for variant in ('corrected', 'amended'):
        for name in designs:
            a = np.array([np.mean([s['results'][name][variant]['clearance_m'] for s in m['shots']]) for m in raw])
            b = np.array([np.mean([s['results'][name]['uncorrected']['clearance_m'] for s in m['shots']]) for m in raw])
            effect.setdefault(variant, {})[name] = interval(a - b, config['bootstrap_seed'])
    save(output / 'raw_machines.json', raw)
    save(output / 'steering.json', {'environment': environment(), 'protocol': config, 'summary': summary,
                                    'corrected_minus_uncorrected_m': effect,
                                    'interval_scope': 'pointwise 95 % machine-cluster percentile bootstrap'})
    print(json.dumps({v: {n: (round(e['mean_clearance_m'] * 1e3, 3), e['lost_particles'], round(e['predicted_loss_max_particles']),
                             [round(x * 1e3, 3) for x in e['exit_centroid_rms_m_rad']]) for n, e in d.items()} for v, d in summary.items()}))


def _robust_objective(k):
    loss = r3.shot_averaged_loss(r3.elementwise_lattice(k, model=model_from_protocol(), correctors=False))
    return float(np.log10(max(loss['loss_lower'], 1e-300)))


def robust(output, phase_file):
    pool = json.loads(phase_file.read_text())['pools']['configured']['rows']
    best_pool = min(pool, key=lambda r: r['loss_max'])
    target = np.array(PROTOCOL['exit_targets']['configured'])
    starts = {**settings(), 'pool_best': np.array(best_pool['strengths_m_minus2'])}
    candidates = []
    for label, start in starts.items():
        res = minimize(_robust_objective, start, method='SLSQP', bounds=list(zip(LOWER, UPPER)),
                       constraints=[{'type': 'eq', 'fun': lambda k: _residual(k, target)},
                                    {'type': 'ineq', 'fun': lambda k: 60 - spatial_profile(lattice_for(k), 16)['peak_beta_m'][0]}],
                       options={'maxiter': 200, 'ftol': 1e-10})
        feasible = bool(np.max(np.abs(_residual(res.x, target))) < 1e-3 and spatial_profile(lattice_for(res.x), 64)['peak_beta_m'][0] < 60.02)
        candidates.append({'start': label, 'strengths_m_minus2': res.x, 'objective_log10': res.fun, 'success': bool(res.success),
                           'feasible': feasible, 'iterations': res.nit, 'termination': str(res.message),
                           'mu_x_deg': np.degrees(r3.phase_advance(lattice_for(res.x))[0])})
    valid = [c for c in candidates if c['feasible']]
    best = min(valid, key=lambda c: c['objective_log10'])
    designs = {**{n: _tradeoff(k) for n, k in settings().items()}, 'robust': _tradeoff(np.array(best['strengths_m_minus2']))}
    save(output / 'robust.json', {'environment': environment(), 'objective': PROTOCOL['robust_design']['objective'],
                                  'bounds': list(zip(LOWER, UPPER)), 'candidates': candidates, 'selected_start': best['start'],
                                  'designs': designs, 'frozen_before_test': True})
    print({n: (round(d['mu_x_deg'], 2), d['loss_max'], round(d['exit_jitter_x_m'] * 1e3, 3), round(d['exit_jitter_xp_rad'] * 1e3, 3))
           for n, d in designs.items()}, best['start'])


def test(output, workers, robust_file):
    config = PROTOCOL['test_campaign']
    frozen = json.loads(robust_file.read_text())['designs']
    designs = {n: np.array(frozen[n]['strengths_m_minus2']) for n in config['designs']}
    raw = campaign(designs, [config['variant']], config, True, workers)
    summary = summarise(raw, designs, [config['variant']], 'reference', config['bootstrap_seed'], True)
    n = config['machines'] * config['shots_per_machine'] * config['particles_per_shot']
    for entry in summary[config['variant']].values():
        entry['observed_loss_fraction'] = entry['lost_particles'] / n
        entry['predicted_loss_max_particles'] = entry['predicted_loss_max_mean'] * n
    paired = {}
    variant = config['variant']
    for name in designs:
        a = np.array([np.mean([s['results'][name][variant]['lost'] for s in m['shots']]) for m in raw])
        b = np.array([np.mean([s['results']['reference'][variant]['lost'] for s in m['shots']]) for m in raw])
        paired[name] = interval((a - b) / config['particles_per_shot'], config['bootstrap_seed'])
    save(output / 'raw_machines.json', raw)
    save(output / 'test.json', {'environment': environment(), 'protocol': config, 'frozen_sha256': hashlib.sha256(robust_file.read_bytes()).hexdigest(),
                                'summary': summary, 'paired_loss_fraction_vs_reference': paired,
                                'interval_scope': 'pointwise 95 % machine-cluster percentile bootstrap'})
    print(json.dumps({k: (e['lost_particles'], round(e['predicted_loss_max_particles']), round(e['mean_clearance_m'] * 1e3, 3),
                          [round(x * 1e3, 3) for x in e['exit_centroid_rms_m_rad']]) for k, e in summary[config['variant']].items()}),
          {k: v['mean'] for k, v in paired.items()})


# --------------------------------------------------------------------------- exit (R2B-05)
def exit_stage(output, phase_file):
    beam, ex = JournalBeam(), r3.EXIT_TWISS
    gamma = (1 + ex['alpha_x'] ** 2) / ex['beta_x']
    budget = {'betatron_divergence_rad': float(np.sqrt(beam.emit_x_m_rad * gamma)),
              'dispersive_divergence_rad': float(abs(ex['disp_px']) * beam.sigma_delta),
              'betatron_size_m': float(np.sqrt(beam.emit_x_m_rad * ex['beta_x'])),
              'dispersive_size_m': float(abs(ex['disp_x']) * beam.sigma_delta),
              'energy_jitter_angle_rad': float(abs(ex['disp_px']) * r3.JITTER['delta']),
              'energy_jitter_position_m': float(abs(ex['disp_x']) * r3.JITTER['delta'])}
    budget['total_divergence_rad'] = float(np.hypot(budget['betatron_divergence_rad'], budget['dispersive_divergence_rad']))
    pools = json.loads(phase_file.read_text())['pools']
    free = pools['dispersion_free']['rows']
    feasible = [r for r in free if r['peak_beta_m'][0] < 60 and r['peak_beta_m'][1] < 60]
    rows = []
    for label, d, dp, pool in [('configured', ex['disp_x'], ex['disp_px'], pools['configured']['rows']),
                               ('dispersion_free', 0.0, 0.0, feasible)]:
        mus = np.radians([r['mu_x_deg'] for r in pool])
        for mu in (mus.min(), mus.max()):
            jit = r3.jitter_transfer(mu)
            jit_d = jit.copy()
            jit_d -= r3.JITTER['delta'] ** 2 * np.outer([ex['disp_x'], ex['disp_px']], [ex['disp_x'], ex['disp_px']])
            jit_d += r3.JITTER['delta'] ** 2 * np.outer([d, dp], [d, dp])
            sigma_beam = np.sqrt(beam.emit_x_m_rad * ex['beta_x'] + (d * beam.sigma_delta) ** 2)
            blade = PROTOCOL['aperture_model']['septum_ex_blade_m']
            rows.append({'target': label, 'mu_x_deg': float(np.degrees(mu)), 'exit_jitter_x_m': float(np.sqrt(jit_d[0, 0])),
                         'exit_jitter_xp_rad': float(np.sqrt(jit_d[1, 1])),
                         'beam_divergence_rad': float(np.sqrt(beam.emit_x_m_rad * gamma + (dp * beam.sigma_delta) ** 2)),
                         'blade_loss_at_exit': float(norm.sf(blade / np.sqrt(sigma_beam ** 2 + jit_d[0, 0])))})
    save(output / 'exit.json', {'environment': environment(), 'budget': budget, 'companion_identity': 'm4 target equals the companion NKM injected_beam (beta_x 2.336495 m, D 80.868 mm, D\' 47.472 mrad)',
                                'dispersion_free_pool': {'solutions': len(free), 'within_60m': len(feasible),
                                                         'mu_x_range_deg': [min(r['mu_x_deg'] for r in feasible), max(r['mu_x_deg'] for r in feasible)] if feasible else None,
                                                         'min_peak_beta_m': min(max(r['peak_beta_m']) for r in free) if free else None},
                                'extremes': rows})
    print(json.dumps(budget), json.dumps(rows))


# --------------------------------------------------------------------------- sensitivity (R2B-06)
def sensitivity(output, workers, robust_file):
    config = PROTOCOL['sensitivity']
    frozen = json.loads(robust_file.read_text())['designs']
    designs = {n: np.array(frozen[n]['strengths_m_minus2']) for n in ('reference', 'low_beta', 'robust')}
    rows = []
    for roll in config['roll_rad']:
        for energy in config['energy_jitter']:
            raw = campaign(designs, ['amended'], config, False, workers, {'roll': roll / 5e-4}, {'delta': energy})
            summary = summarise(raw, designs, ['amended'], 'reference', 93005, False)['amended']
            rows.append({'roll_rad': roll, 'energy_jitter': energy,
                         'designs': {n: {'predicted_loss_max_mean': e['predicted_loss_max_mean'], 'mean_clearance_m': e['mean_clearance_m'],
                                         'paired_clearance_vs_reference_m': e['paired_vs_reference_m'],
                                         'exit_centroid_rms_m_rad': e['exit_centroid_rms_m_rad'], 'active': e['active']}
                                     for n, e in summary.items()}})
            print(roll, energy, {n: (round(e['predicted_loss_max_mean'], 5), round(e['mean_clearance_m'] * 1e3, 3)) for n, e in summary.items()}, flush=True)
    save(output / 'sensitivity.json', {'environment': environment(), 'protocol': config, 'rows': rows})


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--stage', required=True, choices=['apertures', 'phase', 'steering', 'robust', 'test', 'exit', 'sensitivity'])
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--phase-file', type=Path)
    p.add_argument('--robust-file', type=Path)
    p.add_argument('--workers', type=int, default=8)
    a = p.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=False)
    save(a.output_dir / 'configuration.json', {'stage': a.stage, 'protocol': PROTOCOL, 'environment': environment(),
                                               'phase_file': str(a.phase_file) if a.phase_file else None,
                                               'robust_file': str(a.robust_file) if a.robust_file else None})
    if a.stage == 'apertures':
        apertures(a.output_dir)
    elif a.stage == 'phase':
        phase(a.output_dir, a.workers)
    elif a.stage == 'steering':
        steering(a.output_dir, a.workers)
    elif a.stage == 'robust':
        robust(a.output_dir, a.phase_file)
    elif a.stage == 'test':
        test(a.output_dir, a.workers, a.robust_file)
    elif a.stage == 'exit':
        exit_stage(a.output_dir, a.phase_file)
    else:
        sensitivity(a.output_dir, a.workers, a.robust_file)


if __name__ == '__main__':
    main()
