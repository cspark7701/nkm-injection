"""Local checks must work without ignored production artifacts or remote services."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_github_actions.sh'


def invoke(script, args, cwd, temporary):
    env = os.environ.copy()
    env.update(NKM_PYTHON=sys.executable, TMPDIR=str(temporary),
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    return subprocess.run(['bash', str(script), *args], cwd=cwd, env=env,
                          text=True, capture_output=True, timeout=120)


@pytest.mark.parametrize('workflow', ['all', 'ci', 'paper', 'release'])
def test_dry_run_has_no_artifacts_and_uses_selected_interpreter(tmp_path, workflow):
    done = invoke(SCRIPT, ['--dry-run', '--workflow', workflow], tmp_path, tmp_path)
    assert done.returncode == 0, done.stderr
    assert sys.executable in done.stdout
    assert not list(tmp_path.iterdir())
    assert 'scripts/reproduce_paper.py --no-pdf' not in done.stdout
    assert ('complete temporary manifests' in done.stdout) == (workflow != 'ci')


@pytest.mark.parametrize('args', [['--workflow'], ['--workflow', 'invalid'], ['--unknown']])
def test_invalid_options_fail_before_writing(tmp_path, args):
    done = invoke(SCRIPT, args, tmp_path, tmp_path)
    assert done.returncode != 0
    assert done.stderr
    assert not list(tmp_path.iterdir())


def test_quiet_failure_displays_diagnostics_and_keeps_log(tmp_path):
    interpreter = tmp_path / 'failing python'
    interpreter.write_text('#!/bin/sh\necho "intentional child failure" >&2\nexit 23\n')
    interpreter.chmod(0o755)
    env = os.environ.copy()
    env.update(NKM_PYTHON=str(interpreter), TMPDIR=str(tmp_path))
    done = subprocess.run(['bash', str(SCRIPT), '--quiet'], env=env, text=True,
                          capture_output=True, timeout=30)
    assert done.returncode != 0
    assert 'intentional child failure' in done.stderr
    directories = list(tmp_path.glob('nkm-local-actions.*'))
    assert len(directories) == 1
    assert 'intentional child failure' in (directories[0] / 'check_1.log').read_text()


def test_fast_checks_pass_from_checkout_without_results(tmp_path):
    checkout = tmp_path / 'clean checkout'; checkout.mkdir()
    for name in ('scripts', 'tests', 'config', '.github'):
        shutil.copytree(ROOT / name, checkout / name,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ('By.txt', 'kickmap_file.txt', 'K4GSR_HBIv4-1.mat', 'nkm_field.xlsx',
                 'nkm_field_expanded.xlsx', 'NKM_radia.ipynb', 'NKM_radia_y=0.ipynb',
                 'nlk.py', 'storage_ring.ipynb'):
        shutil.copy2(ROOT / name, checkout / name)
    temporary = tmp_path / 'temporary'; temporary.mkdir()
    before = {p: p.read_bytes() for p in checkout.rglob('*') if p.is_file()}
    done = invoke(checkout / 'scripts/check_github_actions.sh', ['--fast', '--quiet'],
                  checkout, temporary)
    assert done.returncode == 0, done.stdout + done.stderr
    assert 'All selected local workflow checks completed' in done.stdout
    assert not (checkout / 'results').exists()
    assert not (checkout / 'storage_ring_lattice_nkm.mat').exists()
    assert not list(temporary.iterdir())
    assert {p: p.read_bytes() for p in checkout.rglob('*') if p.is_file()} == before
