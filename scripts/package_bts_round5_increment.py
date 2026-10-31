#!/usr/bin/env python3
"""Package the round-five BTS referee increment and verify it against the round-three attachment.

The increment overlays the round-three attachment like the round-four increment, and carries the
current sources and PDFs, the evidence ledger, the round-3/4/5 code and tests, and the selected
round-4 and round-5 stage outputs. Verification extracts the round-three attachment and this
increment into a new directory and runs the evidence audit there with an isolated interpreter.
"""
import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('package_bts_round4_increment', ROOT / 'scripts/package_bts_round4_increment.py')
base = importlib.util.module_from_spec(_spec)
sys.modules['package_bts_round4_increment'] = base
_spec.loader.exec_module(base)

R5 = 'results/bts_round5_campaign_20261031'
base.SELECTED = base.SELECTED + [f'{R5}/{stage}' for stage in ('final_test_b', 'layouts_b', 'edge_study')]
base.TREES = ['docs/paper_bts', 'src/nkm_injection'] + base.SELECTED
base.FILES = base.FILES + ['scripts/run_bts_round5.py', 'scripts/export_bts_round5_assets.py',
                           'scripts/package_bts_round5_increment.py']
base.ARCHIVES = base.ARCHIVES + [f'docs/exec-plans/completed/{p.name}' for p in
                                 sorted((ROOT / 'docs/exec-plans/completed').glob('2[89][0-9]_r5_bts_*.md'))]


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--verify-dir', type=Path, required=True)
    a = p.parse_args()
    base.verify(base.package(a.output_dir), a.verify_dir)


if __name__ == '__main__':
    main()
