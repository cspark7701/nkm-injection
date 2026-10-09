"""Tests for the journal figure/macro builder helpers and manifest hash enforcement."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bjf", ROOT / "scripts" / "build_journal_figures.py")
BJF = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BJF)


def test_number_formatting():
    assert BJF.tex_sci(5.19e-6) == r"$5\times10^{-6}$"
    assert BJF.tex_sci(3.714e-5, 2) == r"$3.7\times10^{-5}$"
    assert BJF.sci_label(2502.7) == "2503" and BJF.sci_label(0.104) == "0.1" and BJF.sci_label(5.2e-6) == "5e-6"


def test_manifest_hash_mismatch_is_rejected(tmp_path):
    art = tmp_path / "a.json"
    art.write_text(json.dumps({"x": 1}))
    manifest = tmp_path / "m.json"
    manifest.write_text(json.dumps({"artifacts": {"a": str(art)}, "sha256": {"a": "0" * 64}}))
    b = BJF.Builder(manifest, ROOT, tmp_path / "out")
    with pytest.raises(SystemExit):
        b.load("a")
    manifest.write_text(json.dumps({"artifacts": {"a": str(art)}, "sha256": {}}))
    assert BJF.Builder(manifest, ROOT, tmp_path / "out").load("a") == {"x": 1}


def test_installed_macros_cover_manuscript():
    import re
    tex = (ROOT / "docs/jinst-paper/paper.tex").read_text()
    macros = (ROOT / "docs/jinst-paper/generated/journal_macros.tex").read_text()
    defined = set(re.findall(r"\\newcommand\{\\(\w+)\}", macros))
    used = set(re.findall(r"\\((?:DAx|Kick|Prov|Op|Rep|Baseline|Rob|Tol|Stored)\w*)", tex))
    assert used <= defined, used - defined
