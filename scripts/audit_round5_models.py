#!/usr/bin/env python3
"""Compare NKM/BTS nominal models and jitter units; lengths m, angles rad, K m^-2."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from nkm_injection.bts_journal import JournalBeam, QUADS, lattice_for
from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice

ROOT = Path(__file__).resolve().parents[1]


def audit(root=ROOT):
    def read(name):
        return json.loads((root / name).read_text())
    endpoint = read('results/journal_campaign_05/f2v_xy_zero/checkpoint_inputs.json')
    job = endpoint['jobs'][0]
    config = BTSConfig.from_dict(job['bts_config'])
    reference = read('docs/paper_bts/generated/round2_designs.json')['designs']['baseline']['nominal']['reference']['strengths_m_minus2']
    nkm = create_bts_lattice(config)
    bts = lattice_for(reference)
    get_k = lambda lat: [float(next(e.K for e in lat if e.FamName == q)) for q in QUADS]
    if not np.array_equal(get_k(nkm), reference):
        raise ValueError('Nominal quadrupole strengths differ')
    sequence = lambda lat: [(e.FamName, float(e.Length), float(getattr(e, 'BendingAngle', 0))) for e in lat]
    if sequence(nkm) != sequence(bts):
        raise ValueError('Element sequence, length or nominal bend differs')
    cov = JournalBeam().covariance()
    raw = read('results/journal_campaign_04/e7_seed42/capture_robustness_raw.json')
    fractions = read('docs/paper_bts/generated/round5.json')['macros']
    post = read('results/journal_campaign_05/f2_ablation.json')['exit_state_post_hoc']['mean_std']
    nkm_mean = np.array([post[k]['alone_bts_magnets'][0] for k in ('centroid_y_m','centroid_yp_rad')])
    nkm_std = np.array([post[k]['alone_bts_magnets'][1] for k in ('centroid_y_m','centroid_yp_rad')])
    nkm_rms = np.sqrt(nkm_mean**2+nkm_std**2)
    bts_ref = next(r['designs']['reference'] for r in
        read('results/bts_round4_campaign_20261030/jitter_b/jitter.json')['rows'] if r['scale']==0)
    bts_mean = np.array(bts_ref['mean_exit_centroid_m_rad'][2:])
    bts_rms = np.array(bts_ref['exit_centroid_rms_m_rad'][2:])
    bts_std = np.sqrt(bts_rms**2-bts_mean**2)
    sources = ['src/nkm_injection/errors.py', 'src/nkm_injection/bts_journal.py',
               'scripts/run_capture_robustness.py', 'scripts/run_bts_round3.py',
               'docs/paper_bts/generated/round2_designs.json',
               'results/journal_campaign_05/f2v_xy_zero/checkpoint_inputs.json',
               'results/journal_campaign_05/f2_ablation.json',
               'results/bts_round4_campaign_20261030/jitter_b/jitter.json']
    return {
        'units': {'length': 'm', 'angle': 'rad', 'quadrupole_strength': 'm^-2'},
        'nominal_strengths_identical': True, 'element_sequence_and_bends_identical': True,
        'strengths_m_minus2': dict(zip(QUADS, get_k(nkm))),
        'nkm_integration_steps': sorted({int(e.NumIntSteps) for e in nkm if hasattr(e, 'NumIntSteps')}),
        'bts_integration_steps': sorted({int(e.NumIntSteps) for e in bts if hasattr(e, 'NumIntSteps')}),
        'entrance_twiss': job['initial_twiss'],
        'nominal_entrance_sigma_x_m': float(np.sqrt(cov[0, 0])),
        'nominal_entrance_sigma_xp_rad': float(np.sqrt(cov[1, 1])),
        'jitter_in_nominal_rms_sizes': [float(.0005 / np.sqrt(cov[0, 0])), float(.0002 / np.sqrt(cov[1, 1]))],
        'nkm_population': {'realizations': 50, 'seed': 42, 'particles': 200,
                           'centroid': 'finite-particle septum-exit beam moments; horizontal reference translation'},
        'bts_population': {'machines': 200, 'shots_per_machine': 3,
                           'centroid': 'analytic propagated centroid; fitted existing-dipole steering'},
        'vertical_values': {'nkm_mean_m_rad': nkm_mean.tolist(), 'nkm_population_std_m_rad': nkm_std.tolist(),
                            'nkm_rms_m_rad': nkm_rms.tolist(), 'nkm_quoted_statistic': 'population standard deviation',
                            'bts_mean_m_rad': bts_mean.tolist(), 'bts_population_std_m_rad': bts_std.tolist(),
                            'bts_rms_m_rad': bts_rms.tolist(), 'bts_quoted_statistic': 'root mean square'},
        'error_difference': {'nkm_dipole': 'one common relative draw shared by all bending elements',
                             'bts_dipole': 'independent relative draw per bending element',
                             'shared_rms': raw['error_config']['dipole_b_rel_std'],
                             'quadrupoles': 'independent gradient, x/y offset and roll with common declared rms levels'},
        'other_differences': ['aperture checks and steering implementation differ',
                              'NKM adds emittance/spread and other shot fluctuations; populations/streams are distinct',
                              'NKM finite-particle centroid versus BTS analytic centroid statistic'],
        'vertical_hardware': 'No vertical corrector in either modeled line; future hardware unspecified.',
        'interpretation': 'Same nominal setting and rms levels do not make these identical stochastic models; no sampling-only attribution.',
        'source_sha256': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sources},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        json.dump(audit(), stream, indent=2)
        stream.write('\n')
