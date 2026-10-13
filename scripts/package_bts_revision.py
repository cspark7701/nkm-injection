#!/usr/bin/env python3
"""Build an isolated BTS PDF or prepare a portable selected-evidence attachment."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
from audit_bts_evidence import sha256

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'docs/paper_bts'


def build_pdf(output):
    output.mkdir(parents=True,exist_ok=False)
    for name in ['paper.tex','paper.bib']:shutil.copy2(PAPER/name,output/name)
    for name in ['generated','figures']:shutil.copytree(PAPER/name,output/name)
    commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','paper.tex'],['bibtex','paper'],['pdflatex','-interaction=nonstopmode','-halt-on-error','paper.tex'],['pdflatex','-interaction=nonstopmode','-halt-on-error','paper.tex']]
    for i,command in enumerate(commands):
        result=subprocess.run(command,cwd=output,text=True,capture_output=True)
        (output/f'build_{i}.txt').write_text(result.stdout+result.stderr)
        if result.returncode:raise RuntimeError(f'Build failed: {command}; see {output}')
    log=(output/'paper.log').read_text()
    problems=[line for line in log.splitlines() if any(s in line for s in ['LaTeX Warning','Overfull','Underfull','undefined','Missing character'])]
    if problems:raise ValueError('Layout/reference warnings: '+repr(problems))
    info=subprocess.check_output(['pdfinfo',str(output/'paper.pdf')],text=True)
    (output/'pdfinfo.txt').write_text(info)
    return output/'paper.pdf'


def verify():
    record=json.loads((PAPER/'revision_selection.json').read_text())
    for name,digest in record['final_assets_sha256'].items():
        if sha256(PAPER/name)!=digest:raise ValueError('Final asset mismatch: '+name)
    print('Final manuscript/asset hashes verified.')


def package(output,campaign):
    verify();output.mkdir(parents=True,exist_ok=False);bundle=output/'attachment';bundle.mkdir()
    for name in ['pyproject.toml','README.md','AGENTS.md']:
        shutil.copy2(ROOT/name,bundle/name)
    for name in ['src','scripts','tests']:
        shutil.copytree(ROOT/name,bundle/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.egg-info'))
    shutil.copytree(PAPER,bundle/'docs/paper_bts')
    archive_dir=bundle/'docs/exec-plans/completed';archive_dir.mkdir(parents=True)
    for archive in (ROOT/'docs/exec-plans/completed').glob('*_r1_bts_*.md'):shutil.copy2(archive,archive_dir/archive.name)
    # The NKM manuscript remains separate; only the source-labelled author inputs
    # used by this study are included, without changing the original file.
    answers=bundle/'docs/paper/dependent_answers.md';answers.parent.mkdir(parents=True)
    shutil.copy2(ROOT/'docs/paper/dependent_answers.md',answers)
    manifest=json.loads((PAPER/'evidence_manifest.json').read_text())
    for artifact in manifest['artifacts']:
        target=bundle/artifact['path'];target.parent.mkdir(parents=True,exist_ok=True)
        if sha256(ROOT/artifact['path'])!=artifact['sha256']:raise ValueError('Scientific artifact mismatch')
        shutil.copy2(ROOT/artifact['path'],target)
    shutil.copytree(campaign,bundle/campaign.relative_to(ROOT))
    # Freeze the exact driver/module/config bytes that generated each stage,
    # including uncommitted working-file identity recorded in the stage output.
    stage_commits={'validation':'c1e1f91','matching':'3eba7e3','response':'3cb4ff9','comparison':'b83ae5c'}
    for label,commit in stage_commits.items():
        destination=bundle/'generating_source'/label
        for name in ['src/nkm_injection/bts_journal.py','scripts/run_bts_journal_revision.py','docs/paper_bts/journal_config.json']:
            target=destination/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT))
        candidates=list((campaign/('validation_02' if label=='validation' else label)).glob('*.json'))
        metadata=next(json.loads(path.read_text())['environment'] for path in candidates if 'environment' in json.loads(path.read_text()))
        for name,digest in metadata['source_sha256'].items():
            if sha256(destination/name)!=digest:raise ValueError('Generating source mismatch: '+label+'/'+name)
    snapshots=bundle/'generating_source/statistics/scripts';snapshots.mkdir(parents=True,exist_ok=True)
    for name in ['audit_bts_statistics.py','analyze_tolerance_replicates.py']:shutil.copy2(ROOT/'scripts'/name,snapshots/name)
    stats=json.loads((campaign/'statistics_final/historical_statistics.json').read_text())
    for name,digest in stats['environment']['source_sha256'].items():
        if sha256(bundle/'generating_source/statistics'/name)!=digest:raise ValueError('Statistics generating source mismatch')
    (bundle/'SOURCE_IDENTITY.json').write_text(json.dumps({'packaging_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'identity':'Exact source-file hashes and generating snapshots distinguish working source changes from commit checkpoints.'},indent=2)+'\n')
    (bundle/'REPRODUCE.md').write_text('''# BTS referee attachment

All paths are relative to this extracted root. Historical absolute paths are preserved solely as original metadata; the audit resolves selected data by relative artifact paths.

Use Python 3.11.9 with the recorded pyAT 0.7.2.dev26+g4701d48c.d20260831, NumPy 2.4.6 and SciPy 1.17.1 (plus matplotlib and pytest). Install this package with `python -m pip install -e . --no-deps` in that environment. Other versions require repeating the checks rather than assuming bitwise reproduction.

Run:

```bash
python scripts/audit_bts_evidence.py
python scripts/audit_bts_statistics.py --output-dir results/new_reproduction/statistics
python scripts/run_bts_journal_revision.py --stage validation --output-dir results/new_reproduction/validation
python scripts/run_bts_journal_revision.py --stage matching --output-dir results/new_reproduction/matching
python scripts/run_bts_journal_revision.py --stage response --output-dir results/new_reproduction/response
python scripts/run_bts_journal_revision.py --stage comparison --output-dir results/new_reproduction/comparison
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/new_reproduction/pdf
python -m pytest tests/test_bts_journal.py tests/test_bts_lattice.py tests/test_bts_evidence_audit.py -q
```

Never reuse an existing output directory. The historical 550000 observations are supplied, not regenerated from an unverified historical environment. Their distributions and intervals are numerically reconstructed. New stages can be rerun with source/environment identity recorded. Earlier exact stage driver/module/config snapshots are in `generating_source/`; current sources include the same numerical stages. All scientific inputs and raw outputs are in the attachment; no external personal result directory is needed.

Manuscript publication hashes and selected artifact pointers are in docs/paper_bts/. Compare new results with the installed numerical summaries at the declared tolerances. Inspect the original report and point-by-point response there. Funding, competing interests, final author approval and actual reviewer delivery remain author actions. This local package is not a public deposition or journal acceptance.
''')
    files={str(path.relative_to(bundle)):sha256(path) for path in sorted(bundle.rglob('*')) if path.is_file()}
    (bundle/'SHA256.json').write_text(json.dumps(files,indent=2)+'\n')
    archive=output/'bts_referee_attachment.tar.gz'
    with tarfile.open(archive,'w:gz',compresslevel=3) as tar:tar.add(bundle,arcname='bts_referee_attachment')
    (output/'attachment_sha256.txt').write_text(sha256(archive)+'  '+archive.name+'\n')
    print(archive)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir',type=Path);parser.add_argument('--package-dir',type=Path)
    parser.add_argument('--campaign-dir',type=Path,default=ROOT/'results/bts_journal_campaign_r1_20261013')
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    if args.verify:verify()
    if args.build_dir:print(build_pdf(args.build_dir))
    if args.package_dir:package(args.package_dir,args.campaign_dir.resolve())
    if not (args.verify or args.build_dir or args.package_dir):parser.error('Select --verify, --build-dir or --package-dir')


if __name__=='__main__':main()
