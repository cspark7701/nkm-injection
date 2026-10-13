#!/usr/bin/env python3
"""E6 follow-up — the per-point studies at the re-selected operating point, so the manuscript uses one point.

Sequence (each stage reuses the round-2 driver, now with the in-magnet NKM chamber):

1. ``e6_window``      angle/position window on the ideal ring with the round-3 chamber (``run_round2_window.py``);
2. ``e6_edge_offsets.json``   interpolated 80 % angle edges (``round2_reporting.window_bounds``);
3. ``e6_trajectory.json``     independent DOP853 trajectory check at the new nominal point and edges;
4. ``e6_validation``  native/affine backends at 500 turns, nominal 4000-turn survival, the two angular edges and the
   degraded corrected ring (lowest validated capture in the E6 selection output) to 4000 turns;
5. ``e6_chamber_{ideal,corrected}``  declared chamber study (ideal and corrected rings, open/closed IVUs, rectangular arc scan).

Units: m, rad.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from round2_reporting import window_bounds


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--campaign', type=Path, required=True)
    p.add_argument('--study-config', type=Path, required=True, help='selected operating point (E6)')
    p.add_argument('--selection', type=Path, required=True, help='E6 operating_point_selection.json')
    p.add_argument('--optimization-summary', type=Path, required=True)
    p.add_argument('--chamber-config', type=Path, required=True)
    p.add_argument('--ring-dir', type=Path, required=True)
    p.add_argument('--workers', type=int, default=8)
    a = p.parse_args(); root = a.campaign
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg')
    chamber = json.loads(a.chamber_config.read_text())

    def run(script, args, log):
        print('Running', script, flush=True)
        with (root / log).open('a') as handle:
            subprocess.run([sys.executable, 'scripts/' + script, *map(str, args)], env=env, stdout=handle,
                           stderr=subprocess.STDOUT, check=True)

    common = ['--study-config', a.study_config, '--optimization-summary', a.optimization_summary]
    if not (root / 'e6_window' / 'window_summary.json').exists():
        run('run_round2_window.py', common + ['--chamber-config', a.chamber_config, '--output-dir', root / 'e6_window',
                                              '--workers', a.workers, '--resume'], 'e6_window.log')
    window = json.loads((root / 'e6_window' / 'window_summary.json').read_text())
    edges = list(window_bounds(window['rows'], 'angle'))
    sources = {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((root / 'e6_window').glob('angle_*.json'))}
    (root / 'e6_edge_offsets.json').write_text(json.dumps({'edge_offsets_mrad': edges, 'source_sha256': sources}, indent=2) + '\n')
    if not (root / 'e6_trajectory.json').exists():
        run('validate_round2_trajectory.py', ['--study-config', a.study_config, '--edge-offsets-mrad', *edges,
                                              '--output', root / 'e6_trajectory.json'], 'e6_trajectory.log')
    selection = json.loads(a.selection.read_text())
    label = 'selected_b2'
    per_ring = {k.split('|')[0]: v for k, v in selection['validation'][label].items()
                if k.endswith('|fieldmap_3d') and not k.startswith('ideal')}
    degraded = min(per_ring, key=per_ring.get)
    if not (root / 'e6_validation' / 'validation_summary.json').exists():
        run('run_round2_validation.py', common + ['--chamber-config', a.chamber_config,
                                                  '--degraded-ring', a.ring_dir / f'{degraded}.mat',
                                                  '--edge-offsets-mrad', *edges, '--output-dir', root / 'e6_validation',
                                                  '--workers', a.workers, '--resume'], 'e6_validation.log')
    for scope in ('ideal', 'corrected'):
        if not (root / f'e6_chamber_{scope}' / 'chamber_summary.json').exists():
            run('run_round2_chamber.py', common + ['--corrected-dir', a.ring_dir, '--ring-scope', scope,
                                                   '--output-dir', root / f'e6_chamber_{scope}', '--workers', a.workers,
                                                   '--resume', '--nkm-magnet-half-mm', 1e3 * chamber['nkm_magnet_half_x_m'],
                                                   1e3 * chamber['nkm_magnet_half_y_m']], f'e6_chamber_{scope}.log')
    print('E6 point studies complete; degraded ring', degraded, flush=True)


if __name__ == '__main__':
    main()
