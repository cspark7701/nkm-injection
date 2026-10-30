#!/usr/bin/env python3
"""Package the round-four BTS referee increment and verify it against the round-three attachment.

The increment overlays the round-three attachment (results/bts_referee_attachment_20261020):
current article and supplement sources and PDFs, evidence ledger, round-4 protocol and
reproduction guide, the round-3/4 sources and tests, the selected round-4 stage outputs and
the R4-BTS-03 comparison. Verification extracts both archives into a new directory and runs
the evidence audit there with an isolated interpreter.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/bts_referee_attachment_20261020/bts_referee_attachment.tar.gz'
CAMPAIGN = 'results/bts_round4_campaign_20261030'
SELECTED = [f'{CAMPAIGN}/{stage}' for stage in ('jitter_b', 'blade_b', 'phase_scan_b', 'final_test_b', 'layouts_b')]
FILES = ['results/bts_round4_r403_exact_20261030/comparison.json',
         'scripts/run_bts_round3.py', 'scripts/run_bts_round4.py', 'scripts/export_bts_round3_assets.py',
         'scripts/export_bts_round4_assets.py', 'scripts/export_bts_at_figures.py', 'scripts/audit_bts_evidence.py',
         'scripts/compare_bts_round3_campaigns.py', 'scripts/package_bts_revision.py', 'scripts/package_bts_round4_increment.py',
         'tests/test_bts_round3.py', 'tests/test_bts_round4.py']
TREES = ['docs/paper_bts', 'src/nkm_injection'] + SELECTED
ARCHIVES = [f'docs/exec-plans/completed/{n}' for n in sorted(p.name for p in (ROOT / 'docs/exec-plans/completed').glob('2[67][0-9]_r4_bts_*.md'))]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def members():
    paths = [ROOT / f for f in FILES + ARCHIVES]
    for tree in TREES:
        paths += [p for p in sorted((ROOT / tree).rglob('*')) if p.is_file() and '__pycache__' not in p.parts
                  and p.suffix not in ('.aux', '.log', '.out', '.blg')]
    return paths


def package(output):
    output.mkdir(parents=True, exist_ok=False)
    paths = members()
    inventory = {str(p.relative_to(ROOT)): sha256(p) for p in paths}
    readme = ('# BTS round-4 referee increment\n\nExtract the round-3 attachment (SHA-256 ' + sha256(BASE) + '), then this\n'
              'increment over it. Run `python -I scripts/audit_bts_evidence.py --root <extracted>/bts_referee_attachment`.\n'
              'See docs/paper_bts/round4_reproduction.md. Not a public deposit.\n')
    (output / 'ROUND4_README.md').write_text(readme)
    (output / 'ROUND4_SHA256.json').write_text(json.dumps(inventory, indent=1) + '\n')
    archive = output / 'bts_referee_round4_increment.tar.gz'
    with tarfile.open(archive, 'w:gz') as tar:
        for p in paths:
            tar.add(p, arcname='bts_referee_attachment/' + str(p.relative_to(ROOT)))
        for name in ('ROUND4_README.md', 'ROUND4_SHA256.json'):
            tar.add(output / name, arcname='bts_referee_attachment/' + name)
    (output / 'increment_sha256.txt').write_text(f'{sha256(archive)}  {archive.name}\n')
    print(archive, len(paths), 'files', sha256(archive))
    return archive


def verify(archive, workdir):
    workdir.mkdir(parents=True, exist_ok=False)
    for source in (BASE, archive):
        with tarfile.open(source) as tar:
            tar.extractall(workdir, filter='data')
    root = workdir / 'bts_referee_attachment'
    inventory = json.loads((root / 'ROUND4_SHA256.json').read_text())
    bad = [name for name, digest in inventory.items() if sha256(root / name) != digest]
    if bad:
        raise ValueError(f'Increment inventory mismatch: {bad[:5]}')
    result = subprocess.run([sys.executable, '-I', str(root / 'scripts/audit_bts_evidence.py'), '--root', str(root)],
                            capture_output=True, text=True, cwd=workdir)
    if result.returncode:
        raise RuntimeError(result.stderr)
    print('Extracted audit:', result.stdout.strip().split(':')[-1].count(',') + 1, 'claims verified')


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--verify-dir', type=Path, required=True)
    a = p.parse_args()
    verify(package(a.output_dir), a.verify_dir)


if __name__ == '__main__':
    main()
