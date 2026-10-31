#!/usr/bin/env python3
"""Package the current BTS revision and verify its documented audits after extraction.

The round-seven implementation answers the filename-round-five checklists.
This creates local evidence files only; it performs no external delivery.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_bts_round5_increment', ROOT / 'scripts/package_bts_round5_increment.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
base = previous.base
base.FILES += ['scripts/audit_bts_round6_revision.py', 'scripts/audit_bts_round7_shot_losses.py',
               'scripts/package_bts_round7_increment.py', 'tests/test_bts_round2.py',
               'tests/test_bts_evidence_audit.py', 'tests/test_bts_journal.py',
               'tests/test_bts_lattice.py', 'tests/test_bts_figure_reference.py']
base.ARCHIVES = [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'docs/exec-plans/completed').glob('*.md'))]


def package(output):
    output.mkdir(parents=True, exist_ok=False)
    paths = sorted(set(base.members()))
    inventory = {str(p.relative_to(ROOT)): base.sha256(p) for p in paths}
    record = {'base_archive_sha256': base.sha256(base.BASE), 'files': inventory}
    (output / 'ROUND7_SHA256.json').write_text(json.dumps(record, indent=2) + '\n')
    (output / 'ROUND7_README.md').write_text(
        '# Current BTS referee increment\n\n'
        'Extract the round-three base attachment, then this increment into the same root.\n'
        'This is implementation round seven, answering the renamed review-round-five task lists.\n'
        'Use the project environment and run the round-six audit and round-seven shot-loss audit\n'
        'with fresh output directories; see docs/paper_bts/round7_reproduction.md.\n'
        'The base digest and exact increment inventory are in ROUND7_SHA256.json.\n'
        'This local package does not imply author approval, journal delivery or a public deposit.\n')
    archive = output / 'bts_referee_round7_increment.tar.gz'
    with tarfile.open(archive, 'w:gz') as tar:
        for p in paths:
            tar.add(p, arcname='bts_referee_attachment/' + str(p.relative_to(ROOT)))
        for name in ('ROUND7_README.md', 'ROUND7_SHA256.json'):
            tar.add(output / name, arcname='bts_referee_attachment/' + name)
    (output / 'increment_sha256.txt').write_text(base.sha256(archive) + '  ' + archive.name + '\n')
    print('Packaged', len(paths), 'files:', archive, flush=True)
    return archive


def verify(archive, workdir):
    workdir.mkdir(parents=True, exist_ok=False)
    for source in (base.BASE, archive):
        with tarfile.open(source) as tar:
            tar.extractall(workdir, filter='data')
    root = workdir / 'bts_referee_attachment'
    record = json.loads((root / 'ROUND7_SHA256.json').read_text())
    assert record['base_archive_sha256'] == base.sha256(base.BASE)
    bad = [name for name, digest in record['files'].items() if base.sha256(root / name) != digest]
    if bad:
        raise ValueError('Increment inventory mismatch: ' + repr(bad[:5]))
    # -I plus an explicitly selected extracted scripts directory prevents imports
    # from the live checkout, including package_bts_revision's local audit helper.
    runner = ('import runpy,sys;from pathlib import Path;'
              'p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));'
              'sys.argv=sys.argv[1:];runpy.run_path(str(p),run_name="__main__")')
    jobs = [
        ('evidence', 'audit_bts_evidence.py', []),
        ('assets', 'package_bts_revision.py', ['--verify']),
        ('round6', 'audit_bts_round6_revision.py', ['--output-dir', str(root / 'results/new_extracted_round6_checks')]),
        ('round7', 'audit_bts_round7_shot_losses.py', ['--output-dir', str(root / 'results/new_extracted_round7_checks')]),
    ]
    checks = {}
    for label, name, arguments in jobs:
        result = subprocess.run([sys.executable, '-I', '-c', runner, str(root / 'scripts' / name), *arguments],
                                cwd=root, capture_output=True, text=True)
        (workdir / (label + '_audit.txt')).write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(label + ' extracted check failed: ' + result.stderr)
        checks[label] = {'returncode': result.returncode, 'stdout': result.stdout.strip()}
    for exported, generated in [('generated/round6_checks.json', 'results/new_extracted_round6_checks/round6_checks.json'),
                                ('generated/round7_shot_losses.json', 'results/new_extracted_round7_checks/shot_loss_diagnostic.json')]:
        assert json.loads((root / 'docs/paper_bts' / exported).read_text()) == json.loads((root / generated).read_text())
    checks['inventory_files'] = len(record['files'])
    checks['archive_sha256'] = base.sha256(archive)
    checks['postprocessing_matches_selected_records'] = True
    (workdir / 'verification.json').write_text(json.dumps(checks, indent=2) + '\n')
    print('Extracted inventory, evidence, assets and both post-processing audits verified.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--verify-dir', type=Path, required=True)
    args = parser.parse_args()
    verify(package(args.output_dir.resolve()), args.verify_dir.resolve())


if __name__ == '__main__':
    main()
