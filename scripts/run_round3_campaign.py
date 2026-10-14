#!/usr/bin/env python3
"""E7 — the single round-3 robustness rerun: joint ensembles, jitter curve, analysis and matched tuning.

Inputs fixed by earlier round-3 tasks: the in-magnet NKM chamber (E4, ``--chamber-config``), the corrected ring
population (E5, ``--corrected-ring-dir``) and the re-selected operating point (E6, ``--study-config``). The error budget
is the round-2 budget (unchanged). Populations are unchanged from round 2: three seeds x 50 joint realizations,
200 particles, 500 native turns; jitter levels on the seed-42 realizations. Outputs under ``--campaign`` with prefix e7.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--campaign', type=Path, required=True)
    p.add_argument('--study-config', type=Path, required=True)
    p.add_argument('--optimization-summary', type=Path, required=True)
    p.add_argument('--chamber-config', type=Path, required=True)
    p.add_argument('--corrected-ring-dir', type=Path, required=True)
    p.add_argument('--error-budget', type=Path, required=True)
    p.add_argument('--x-max-m', type=float, required=True, help='septum-clearance bound for tuning (from E6)')
    p.add_argument('--workers', type=int, default=8)
    a = p.parse_args(); root = a.campaign; root.mkdir(parents=True, exist_ok=True)
    ring = json.loads((a.corrected_ring_dir / 'corrected_ring_summary.json').read_text())
    if len(ring['seeds']) != 10: raise SystemExit('E5 ring population incomplete')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MPLBACKEND='Agg')

    def run(script, args, log):
        command = [sys.executable, 'scripts/' + script, *map(str, args)]
        print('Running', script, log, flush=True)
        with (root / log).open('a') as handle:
            subprocess.run(command, env=env, stdout=handle, stderr=subprocess.STDOUT, check=True)

    variants = root / 'e7_input_variants'; variants.mkdir(exist_ok=True)
    common = ['--study-config', a.study_config, '--optimization-summary', a.optimization_summary,
              '--chamber-config', a.chamber_config, '--corrected-ring-dir', a.corrected_ring_dir,
              '--kicker-models', 'fieldmap_3d', 'dipole', '--control-reference', '3d', '--timing-model', 'scale',
              '--correct-static-orbit', '--samples', '50', '--particles', '200', '--turns', '500',
              '--workers', a.workers, '--capture-threshold', '.8', '--resume']
    for seed in (42, 123, 777):
        run('run_capture_robustness.py', common + ['--seed', seed, '--error-config', a.error_budget,
                                                   '--output-dir', root / f'e7_seed{seed}'], f'e7_seed{seed}.log')
    original = json.loads(a.error_budget.read_text())
    for label, sx, sxp in (('0', 0, 0), ('0.25', .25, .25), ('0.5', .5, .5), ('0.75', .75, .75), ('x_only', 1, 0), ('xp_only', 0, 1)):
        values = dict(original); values['booster_x_jitter_std_m'] *= sx; values['booster_xp_jitter_std_rad'] *= sxp
        path = variants / f'jitter_{label}.json'
        if path.exists() and json.loads(path.read_text()) != values: raise SystemExit('Existing jitter budget changed')
        path.write_text(json.dumps(values, indent=2) + '\n')
        run('run_capture_robustness.py', common + ['--seed', '42', '--error-config', path,
                                                   '--output-dir', root / f'e7_jitter_{label}'], f'e7_jitter_{label}.log')
    if not (root / 'e7_final_statistics.json').exists():
        run('analyze_round2_robustness.py', ['--campaign', root, '--prefix', 'e7',
                                             '--output', root / 'e7_final_statistics.json'], 'e7_analysis.log')
    run('run_round3_tuning.py', ['--full-ensemble', root / 'e7_seed42', '--zero-ensemble', root / 'e7_jitter_0',
                                 '--quarter-ensemble', root / 'e7_jitter_0.25', '--x-max-m', a.x_max_m,
                                 '--output-dir', root / 'e7_tuning', '--workers', a.workers, '--resume'], 'e7_tuning.log')
    print('E7 numerical campaign complete', flush=True)


if __name__ == '__main__':
    main()
