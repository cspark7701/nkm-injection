#!/usr/bin/env python3
"""Audit paired round-5 jitter jobs and summarize capture fractions (m, rad inputs)."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODELS = ('fieldmap_3d', 'dipole')


def interval(values, count=10000, seed=1729):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or not len(values) or not np.all(np.isfinite(values)):
        raise ValueError('Finite nonempty realization vector required')
    rng = np.random.default_rng(seed)
    resamples = values[rng.integers(0, len(values), (count, len(values)))].mean(axis=1)
    return {'mean': float(values.mean()), 'ci95': np.quantile(resamples, [.025, .975]).tolist()}


def validate_jobs(reference, jobs, scale):
    """Reject changed physics, particles or non-jitter draws; allow only x/xp scaling."""
    ref = {j['sample']['sample_id']: j for j in reference}
    current = {j['sample']['sample_id']: j for j in jobs}
    if len(current) != len(jobs) or set(ref) != set(current):
        raise ValueError('Unpaired or duplicate realization IDs')
    scientific_keys = ('config', 'bts_config', 'initial_twiss', 'target_twiss', 'models', 'backend',
                       'thick_slices', 'particles', 'turns', 'correct_static_orbit', 'slices_3d',
                       'timing_model', 'calibration_3d', 'septum_angle_mrad', 'rf_frequency_hz',
                       'pulse_duration_us', 'chamber', 'static_steering_planes', 'extra', 'beam_seed',
                       'ring_error_seed', 'corrected_ring_path')
    jitter_keys = ('booster_x_m', 'booster_xp_rad')
    for i, job in current.items():
        for key in scientific_keys:
            if job[key] != ref[i][key]:
                raise ValueError(f'Changed paired job field: {i} {key}')
        for key, value in job['sample'].items():
            if key in jitter_keys:
                if not np.isclose(value, ref[i]['sample'][key] * scale, rtol=1e-14, atol=1e-18):
                    raise ValueError(f'Jitter scale differs: {i} {key}')
            elif value != ref[i]['sample'][key]:
                raise ValueError(f'Non-jitter draw differs: {i} {key}')
    return sorted(current)


def summarize(vectors, baseline, count=10000, seed=1729, margin=.01):
    output = {}
    for name in MODELS:
        values = np.asarray(vectors[name], float)
        output[name] = {**interval(values, count, seed), 'zero_fraction': float(np.mean(values == 0)),
                        'jitter_cost': interval(values - baseline[name], count, seed)}
    gap = np.asarray(vectors[MODELS[0]]) - vectors[MODELS[1]]
    base_gap = np.asarray(baseline[MODELS[0]]) - baseline[MODELS[1]]
    output['gap'] = interval(gap, count, seed)
    output['gap_change'] = interval(gap - base_gap, count, seed)
    output['nkm_noninferior_to_zero_jitter'] = bool(output[MODELS[0]]['jitter_cost']['ci95'][0] > -margin)
    return output


def analyze(root=ROOT):
    protocol_path = root / 'docs/paper/round5_protocol.json'
    protocol = json.loads(protocol_path.read_text())
    campaign = root / protocol['campaign']
    preparation = json.loads((campaign / 'preparation.json').read_text())
    folders = {float(k): root / v for k, v in protocol['endpoints'].items()}
    folders.update({float(k): root / v['output'] for k, v in preparation['variants'].items()})
    load = lambda path: json.loads(path.read_text())
    ref = load(folders[1.] / 'checkpoint_inputs.json')['jobs']
    ensembles, identities = {}, {}
    for scale in protocol['scales']:
        folder = folders[float(scale)]
        spec = load(folder / 'checkpoint_inputs.json')
        ids = validate_jobs(ref, spec['jobs'], float(scale))
        raw = load(folder / 'capture_robustness_raw.json')
        rows = {r['sample_id']: r for r in raw['realizations'] if r['sample_id'] >= 0}
        if sorted(rows) != ids or len(ids) != protocol['samples']:
            raise ValueError('Raw realization identities differ')
        for job in spec['jobs']:
            row = rows[job['sample']['sample_id']]
            if (row['beam_seed'], row['ring_error_seed']) != (job['beam_seed'], job['ring_error_seed']):
                raise ValueError('Raw metadata differs from checkpoint')
            for model in MODELS:
                m = row['models'][model]
                causes = m['loss_causes']
                lost = sum(causes[k] for k in ('upstream', 'septum_creation', 'injection_segment', 'outside_field_map', 'ring'))
                if m['n'] != protocol['particles'] or lost + m['captured'] != m['n']:
                    raise ValueError('Particle/loss accounting mismatch')
        ensembles[float(scale)] = {m: np.array([rows[i]['models'][m]['capture_fraction'] for i in ids]) for m in MODELS}
        for name in ('capture_robustness_raw.json', 'checkpoint_inputs.json'):
            path = folder / name
            identities[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    rows = [{'scale': float(s), **summarize(ensembles[float(s)], ensembles[0.],
             protocol['bootstrap_count'], protocol['bootstrap_seed'], protocol['margin_fraction'])} for s in protocol['scales']]
    passing = [r['scale'] for r in rows if r['scale'] > 0 and r['nkm_noninferior_to_zero_jitter']]
    return {'protocol': str(protocol_path.relative_to(root)), 'n_realizations': protocol['samples'],
            'particles_per_realization': protocol['particles'], 'turns': protocol['turns'],
            'steering': protocol['steering'], 'interval_scope': protocol['test'], 'rows': rows,
            'largest_passing_nonzero_tested_scale': max(passing) if passing else None,
            'input_sha256': identities, 'pairing_verified': True,
            'interpretation': 'Pointwise realization intervals conditional on ten rings; no continuous threshold or hardware tolerance.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repo-root', type=Path, default=ROOT, help='Evidence root for portable saved-output reanalysis')
    args = parser.parse_args()
    result = analyze(args.repo_root.resolve())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        print(row['scale'], {m: round(100 * row[m]['mean'], 2) for m in MODELS},
              'gap', row['gap'], 'loss-test pass', row['nkm_noninferior_to_zero_jitter'])
