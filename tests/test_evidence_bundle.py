"""Frozen evidence must reject unsafe paths and uncommitted source snapshots."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


def builder():
    path = Path(__file__).resolve().parents[1] / 'scripts/build_evidence_bundle.py'
    spec = importlib.util.spec_from_file_location('evidence_bundle', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('artifact', ['../outside.json', '/tmp/outside.json'])
def test_bundle_rejects_paths_outside_evidence_tree(tmp_path, artifact):
    module = builder()
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'artifacts': {'outside': artifact}}))
    with pytest.raises(SystemExit, match='repository-relative'):
        module.main(['--manifest', str(manifest), '--output-dir', str(tmp_path / 'bundle')])
    assert not (tmp_path / 'outside.json').exists()


def test_bundle_cannot_freeze_dirty_code(tmp_path, monkeypatch):
    module = builder()
    monkeypatch.setattr(module, 'REPO', tmp_path)
    monkeypatch.setattr(module, 'INPUTS', ())
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'artifacts': {}}))
    calls = []

    def git(command, **kwargs):
        calls.append(command)
        if command[1] == 'rev-parse':
            return SimpleNamespace(stdout='abc123\n')
        if command[1] == 'status':
            return SimpleNamespace(stdout=' M scripts/build_revision_figures.py\n')
        pytest.fail('Dirty source must be rejected before git archive')

    monkeypatch.setattr(module.subprocess, 'run', git)
    with pytest.raises(SystemExit, match='Commit the source'):
        module.main(['--manifest', str(manifest), '--output-dir', str(tmp_path / 'bundle')])
    assert len(calls) == 2
