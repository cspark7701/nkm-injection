#!/usr/bin/env python3
"""Round-five BTS stages (R5-BTS tasks). SI units; new output directory per stage.

Stages:
  final_test   second-test realizations rerun with shared reading noise, including a duplicate setting (R5-BTS-01/02)
  layouts      steering layouts with shared reading noise and an angle-weighted layout (R5-BTS-01/06)
  edge_study   lower phase-advance edge versus the exit dispersion target (R5-BTS-05)
"""
import argparse
import hashlib
import importlib.util
import json
from multiprocessing import Pool
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import minimize

from nkm_injection.bts_journal import LOWER, SCALES, UPPER, lattice_for
from nkm_injection.bts_round2 import nominal_observables, spatial_profile
from nkm_injection import bts_round3 as r3
from nkm_injection import bts_round4 as r4

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'docs/paper_bts'
PROTOCOL = json.loads((PAPER / 'round5_protocol.json').read_text())
R4_CAMPAIGN = ROOT / 'results/bts_round4_campaign_20261030'
_spec = importlib.util.spec_from_file_location('run_bts_round4', ROOT / 'scripts/run_bts_round4.py')
R4 = importlib.util.module_from_spec(_spec)
sys.modules['run_bts_round4'] = R4  # worker processes look pickled functions up by module name
_spec.loader.exec_module(R4)
SOURCES = R4.SOURCES + ['scripts/run_bts_round5.py', 'docs/paper_bts/round5_protocol.json']
save, interval = R4.save, R4.interval


def environment():
    env = R4.environment()
    env['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    return env


def frozen():
    """Frozen strengths [m^-2]: round-2/3 settings, the round-4 edge and dispersion-free settings, and a duplicate."""
    scan = json.loads((R4_CAMPAIGN / 'phase_scan_b/phase_scan.json').read_text())
    edges = [e for e in scan['edges'] if e['target'] == 'configured' and e['direction'] == 'min' and e['success'] and e['matched']]
    extra = {'edge_best': np.array(min(edges, key=lambda e: e['mu_x_deg'])['strengths_m_minus2']),
             'free_best': np.array(scan['chosen']['free_best']['strengths_m_minus2'])}
    table = R4.frozen_designs(['reference', 'low_beta', 'robust'], extra)
    table.update(extra)
    table['robust_copy'] = table['robust'].copy()
    return table


def gain(raw, numerator, denominator, layout, seed, count=10000):
    """Ratio of population means of the jitter-integrated loss, with a paired realization bootstrap."""
    a = np.array([m['jitter_integrated_loss'][numerator][layout] for m in raw])
    b = np.array([m['jitter_integrated_loss'][denominator][layout] for m in raw])
    rng = np.random.default_rng(seed)
    ids = rng.integers(0, len(a), (count, len(a)))
    num, den = a[ids].mean(1), b[ids].mean(1)
    valid = den > 0
    ratios = num[valid] / den[valid]
    return {'estimate': float(a.mean() / b.mean()), 'ci95': np.quantile(ratios, [.025, .975]).tolist(),
            'numerator_mean': float(a.mean()), 'denominator_mean': float(b.mean()),
            'resamples': count, 'zero_denominator_resamples': int((~valid).sum())}


def validation(summary, n_particles):
    """Tracked counts against Gaussian predictions conditional on the sampled shots, with Poisson deviations."""
    out = {}
    for name, e in summary.items():
        expected = e['predicted_loss_max_mean'] * n_particles
        observed = e['lost_particles']
        out[name] = {'observed_count': observed, 'conditional_expected_count': expected,
                     'integrated_expected_count': e['jitter_integrated_loss_mean'] * n_particles,
                     'relative_difference': (observed - expected) / observed if observed else None,
                     'poisson_z': (observed - expected) / np.sqrt(expected) if expected > 0 else None}
    return out


def final_test(output, workers):
    config = PROTOCOL['final_test']
    designs = {n: frozen()[n] for n in config['designs']}
    raw = R4.campaign(designs, ['full'], config, True, workers)
    summary = R4.summarise(raw, designs, ['full'], 'reference', config['bootstrap_seed'], config['particles_per_shot'])['full']
    n = config['machines'] * config['shots_per_machine'] * config['particles_per_shot']
    duplicate = all(s['results']['robust']['full'] == s['results']['robust_copy']['full'] for m in raw for s in m['shots']) and \
        all(m['jitter_integrated_loss']['robust']['full'] == m['jitter_integrated_loss']['robust_copy']['full'] for m in raw)
    gains = {name: gain(raw, 'reference', name, 'full', config['bootstrap_seed']) for name in ('edge_best', 'robust', 'low_beta', 'free_best')}
    save(output / 'raw_machines.json', raw)
    save(output / 'final_test.json', {'environment': environment(), 'protocol': config, 'estimator': PROTOCOL['estimator'],
                                      'summary': summary, 'gain_vs_reference': gains, 'validation': validation(summary, n),
                                      'duplicate_identical': bool(duplicate),
                                      'interval_scope': 'pointwise 95 % realization-cluster percentile bootstrap'})
    print('duplicate identical:', duplicate)
    for k, g in gains.items():
        print(k, round(g['estimate'], 3), [round(x, 3) for x in g['ci95']])
    for k, e in summary.items():
        print(k, e['lost_particles'], round(100 * e['observed_loss_fraction'], 4), round(100 * e['predicted_loss_max_mean'], 4),
              round(100 * e['jitter_integrated_loss_mean'], 4), e['paired_tracked_vs_reference'])


def layouts(output, workers):
    config = PROTOCOL['steering_layouts']
    designs = {n: frozen()[n] for n in config['designs']}
    raw = R4.campaign(designs, config['layouts'], config, True, workers)
    summary = R4.summarise(raw, designs, config['layouts'], 'reference', config['bootstrap_seed'], config['particles_per_shot'])
    gains = {layout: gain(raw, 'reference', 'edge_best', layout, config['bootstrap_seed']) for layout in config['layouts']}
    save(output / 'raw_machines.json', raw)
    save(output / 'layouts.json', {'environment': environment(), 'protocol': config, 'summary': summary,
                                   'gain_vs_reference': gains,
                                   'interval_scope': 'pointwise 95 % realization-cluster percentile bootstrap'})
    for layout, d in summary.items():
        print(layout, {k: (round(100 * e['observed_loss_fraction'], 3), [round(1e3 * x, 3) for x in e['exit_centroid_rms_m_rad']])
                       for k, e in d.items()}, round(gains[layout]['estimate'], 2))


def _edge(job):
    label, d, dp, start = job
    target = np.array([2.336495, 4.256241, -0.016335, 0.017772, d, dp])
    residual = lambda k: (nominal_observables(lattice_for(k)) - target) / SCALES
    peak = lambda k: 60.0 - np.array(spatial_profile(lattice_for(k), 16)['peak_beta_m'])
    res = minimize(lambda k: r3.phase_advance(lattice_for(k))[0], np.asarray(start), method='SLSQP', bounds=list(zip(LOWER, UPPER)),
                   constraints=[{'type': 'eq', 'fun': residual}, {'type': 'ineq', 'fun': peak}],
                   options={'maxiter': 300, 'ftol': 1e-12})
    k = res.x
    peaks = spatial_profile(lattice_for(k), 16)['peak_beta_m']
    return {'D_m': d, 'Dp': dp, 'start': label, 'mu_x_deg': float(np.degrees(r3.phase_advance(lattice_for(k))[0])),
            'matched': bool(np.max(np.abs(residual(k))) < 1e-3), 'success': bool(res.success), 'iterations': int(res.nit),
            'termination': str(res.message), 'peak_beta_m': peaks, 'peak_beta_active': [bool(p > 59.99) for p in peaks],
            'active_bounds': r4.active_bounds(k, LOWER, UPPER, 1e-5), 'strengths_m_minus2': k}


def edge_study(output, workers):
    targets = [(0.080868, 0.047472), (0.080868, 0.032), (0.080868, 0.016), (0.080868, 0.0), (0.0, 0.047472), (0.0, 0.0)]
    table = frozen()
    starts = {'configured_edge': table['edge_best'], 'dispersion_free_best': table['free_best'], 'robust': table['robust']}
    jobs = [(label, d, dp, k) for d, dp in targets for label, k in starts.items()]
    with Pool(workers) as pool:
        rows = pool.map(_edge, jobs, chunksize=1)
    best = {}
    for d, dp in targets:
        found = [r for r in rows if r['D_m'] == d and r['Dp'] == dp and r['matched']]
        best[f'{d}_{dp}'] = min(found, key=lambda r: r['mu_x_deg']) if found else None
    save(output / 'edge_study.json', {'environment': environment(), 'protocol': PROTOCOL['edge_study'], 'rows': rows, 'lowest': best})
    for key, r in best.items():
        print(key, None if r is None else (round(r['mu_x_deg'], 2), r['success'], r['active_bounds'], r['peak_beta_active']))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--stage', required=True, choices=['final_test', 'layouts', 'edge_study'])
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--workers', type=int, default=8)
    a = p.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=False)
    save(a.output_dir / 'configuration.json', {'stage': a.stage, 'protocol': PROTOCOL, 'environment': environment()})
    {'final_test': final_test, 'layouts': layouts, 'edge_study': edge_study}[a.stage](a.output_dir, a.workers)


if __name__ == '__main__':
    main()
