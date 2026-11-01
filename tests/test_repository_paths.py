"""Historical evidence paths survive the NKM manuscript directory rename."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from nkm_injection.repository_paths import manuscript_path


@pytest.mark.parametrize('requested,present', [('paper', 'paper_nkm'), ('paper_nkm', 'paper')])
def test_manifest_path_resolves_in_checkout_and_old_attachment(tmp_path, requested, present):
    actual = tmp_path / 'docs' / present / 'config.json'
    actual.parent.mkdir(parents=True)
    actual.write_text('{"units": "m"}')
    assert manuscript_path(tmp_path, f'docs/{requested}/config.json') == actual
    assert manuscript_path(tmp_path, tmp_path/'docs'/requested/'config.json') == actual


def test_existing_path_wins_and_unrelated_prefix_is_never_redirected(tmp_path):
    for folder in ('paper', 'paper_nkm'):
        p = tmp_path/'docs'/folder/'input.json'
        p.parent.mkdir(parents=True)
        p.write_text(folder)
    assert manuscript_path(tmp_path, 'docs/paper/input.json').read_text() == 'paper'
    assert manuscript_path(tmp_path, 'docs/paper_bts/input.json') == tmp_path/'docs/paper_bts/input.json'
    assert manuscript_path(tmp_path, 'elsewhere/docs/paper/input.json') == tmp_path/'elsewhere/docs/paper/input.json'


def test_migrated_evidence_still_rejects_hash_mismatch(tmp_path):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location('migration_builder', root/'scripts/build_journal_figures.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual = tmp_path/'docs/paper_nkm/config.json'
    actual.parent.mkdir(parents=True)
    actual.write_text('{"value": 1}')
    manifest = tmp_path/'manifest.json'
    manifest.write_text(json.dumps({'artifacts': {'config': 'docs/paper/config.json'},
                                    'sha256': {'config': hashlib.sha256(actual.read_bytes()).hexdigest()}}))
    builder = module.Builder(manifest, tmp_path, tmp_path/'output')
    assert builder.load('config') == {'value': 1}
    actual.write_text('{"value": 2}')
    with pytest.raises(SystemExit, match='SHA-256 mismatch'):
        builder.load('config')
