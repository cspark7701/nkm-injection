#!/usr/bin/env python3
"""Run the declared round-5 paired two-plane jitter scan; units m, rad, eV."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / 'docs/paper/round5_protocol.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare():
    protocol = json.loads(PROTOCOL.read_text())
    for path, digest in protocol['core_input_sha256'].items():
        # These are version snapshots, not tracking inputs. Prose edits may proceed during tracking.
        if path in ('docs/paper/paper.tex', 'docs/paper/paper.pdf'):
            continue
        if sha(ROOT / path) != digest:
            raise ValueError('Frozen input/source changed: ' + path)
    import run_capture_robustness as tracker
    if 'nkm_injection.bts_round3' in sys.modules:
        raise ValueError('Previously unrelated BTS module is now imported by NKM tracking')
    checks = {}
    for scale, folder in protocol['endpoints'].items():
        spec = json.loads((ROOT / folder / 'checkpoint_inputs.json').read_text())
        changed = [path for path, digest in spec['hashes'].items() if sha(path) != digest]
        # This module belongs to the separate BTS manuscript and is not imported above.
        unrelated = str(ROOT / 'src/nkm_injection/bts_round3.py')
        if any(path != unrelated for path in changed):
            raise ValueError('Endpoint tracking dependency changed: ' + repr(changed))
        if any(j['static_steering_planes'] != 'xy' or j['particles'] != 200 or j['turns'] != 500
               for j in spec['jobs']):
            raise ValueError('Endpoint steering/count configuration differs')
        checks[scale] = {'path': folder, 'raw_sha256': sha(ROOT / folder / 'capture_robustness_raw.json'),
                         'unrelated_changed_not_imported': changed}
    return protocol, checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError('Positive worker count required')
    protocol, checks = prepare()
    campaign = ROOT / protocol['campaign']
    campaign.mkdir(parents=True, exist_ok=True)
    inputs = campaign / 'inputs'
    inputs.mkdir(exist_ok=True)
    base = json.loads((ROOT / 'results/journal_campaign_03/error_budget.json').read_text())
    record = {'protocol_sha256': sha(PROTOCOL), 'endpoint_reuse': checks, 'variants': {}}
    for scale in protocol['new_scales']:
        cfg = dict(base)
        cfg['booster_x_jitter_std_m'] = base['booster_x_jitter_std_m'] * scale
        cfg['booster_xp_jitter_std_rad'] = base['booster_xp_jitter_std_rad'] * scale
        label = str(scale).replace('.', 'p')
        path = inputs / ('jitter_' + label + '.json')
        text = json.dumps(cfg, indent=2) + '\n'
        if path.exists() and path.read_text() != text:
            raise ValueError('Input configuration differs: ' + str(path))
        if not path.exists():
            path.write_text(text)
        record['variants'][str(scale)] = {'config': str(path.relative_to(ROOT)), 'sha256': sha(path),
                                          'output': str((campaign / ('g2_xy_' + label)).relative_to(ROOT))}
    recpath = campaign / 'preparation.json'
    if recpath.exists() and json.loads(recpath.read_text()) != record:
        raise ValueError('Preparation identity differs')
    if not recpath.exists():
        recpath.write_text(json.dumps(record, indent=2) + '\n')
    if args.prepare_only:
        print(json.dumps(record, indent=2))
        return
    model = protocol['adopted_model']
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg')
    for scale, variant in record['variants'].items():
        output = ROOT / variant['output']
        if output.exists() and not args.resume:
            raise ValueError('Output exists; use --resume for strictly validated checkpoints')
        command = [sys.executable, str(ROOT / 'scripts/run_capture_robustness.py'),
                   '--study-config', str(ROOT / model['study_config_current']),
                   '--optimization-summary', str(ROOT / model['optimization_summary']),
                   '--chamber-config', str(ROOT / model['chamber_config']),
                   '--corrected-ring-dir', str(ROOT / model['corrected_ring_dir']),
                   '--error-config', str(ROOT / variant['config']), '--output-dir', str(output),
                   '--kicker-models', 'fieldmap_3d', 'dipole', '--control-reference', '3d',
                   '--timing-model', 'scale', '--correct-static-orbit', '--static-steering-planes', 'xy',
                   '--samples', '50', '--particles', '200', '--turns', '500', '--seed', '42',
                   '--capture-threshold', '.8', '--bootstrap-count', '10000', '--bootstrap-seed', '1729',
                   '--workers', str(args.workers)]
        if args.resume:
            command.append('--resume')
        print('Running paired two-plane scale', scale, flush=True)
        with (campaign / ('g2_scale_' + scale + '.log')).open('a') as log:
            subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        print('Completed scale', scale, flush=True)


if __name__ == '__main__':
    main()
