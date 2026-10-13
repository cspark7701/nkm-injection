import importlib.util
import json
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location('audit_bts_evidence',Path(__file__).parents[1]/'scripts/audit_bts_evidence.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)


def test_evidence_audit_detects_missing_keys_and_changed_digest(tmp_path):
    file=tmp_path/'result.json';file.write_text(json.dumps({'value':2}))
    artifact={'path':file.name,'sha256':audit.sha256(file),'bytes':file.stat().st_size}
    manifest={'artifacts':[artifact],'claims':[{'id':'BC','artifact':file.name,'pointer':'/value','expected':2}]}
    assert audit.audit(tmp_path,manifest)==['BC']
    manifest['claims'][0]['pointer']='/absent'
    with pytest.raises(KeyError):audit.audit(tmp_path,manifest)
    file.write_text('{"value":3}')
    with pytest.raises(ValueError,match='identity mismatch'):audit.audit(tmp_path,manifest)


def test_pointer_escaped_tokens_and_arrays():
    assert audit.resolve({'a/b':[{'~key':7}]},'/a~1b/0/~0key')==7
    with pytest.raises(ValueError):audit.resolve({},'wrong')
