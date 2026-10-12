"""Tests for the submission package builder helpers (no LaTeX run)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bsp", ROOT / "scripts" / "build_submission_package.py")
BSP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BSP)


def test_referenced_figures_exist_and_are_generated():
    figs = BSP.referenced_figures((BSP.PAPER / "paper.tex").read_text())
    assert len(figs) >= 8
    assert all(f.startswith("generated/figures/") and (BSP.PAPER / f).is_file() for f in figs)


def test_supplement_files_exist():
    assert all((BSP.PAPER / r).is_file() for r in BSP.SUPPLEMENT)


def test_log_gate_patterns():
    assert BSP.BAD_LOG.search("LaTeX Warning: Reference `x' on page 1 undefined")
    assert BSP.BAD_LOG.search("Overfull \\hbox (3pt too wide)")
    assert not BSP.BAD_LOG.search("Output written on paper.pdf (10 pages, 1 bytes).")


def test_staged_sources_include_shared_two_column_entry(tmp_path):
    files = BSP.stage_sources(tmp_path)
    assert "paper_twocolumn.tex" in files
    wrapper = (tmp_path / "paper_twocolumn.tex").read_text()
    assert r"\input{paper.tex}" in wrapper
    assert (tmp_path / "generated/journal_macros.tex").read_bytes() == (BSP.PAPER / "generated/journal_macros.tex").read_bytes()
    assert all((tmp_path / rel).is_file() for rel in files)


def test_initial_latex_failure_stops_before_bibtex(tmp_path, monkeypatch):
    from types import SimpleNamespace
    import pytest

    calls = []
    def fail(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=1, stdout="! Failed front matter")
    monkeypatch.setattr(BSP.subprocess, "run", fail)
    with pytest.raises(SystemExit, match="initial LaTeX build failed"):
        BSP.compile_paper(tmp_path)
    assert len(calls) == 1
    assert calls[0][0] == "pdflatex"


def test_two_column_compilation_uses_its_own_job(tmp_path, monkeypatch):
    from types import SimpleNamespace
    calls = []
    def run(command, **kwargs):
        calls.append(command)
        if command[0] == "pdflatex":
            (tmp_path / "paper_twocolumn.log").write_text("Output written on paper_twocolumn.pdf (14 pages, 10 bytes).")
        return SimpleNamespace(returncode=0, stdout="")
    monkeypatch.setattr(BSP.subprocess, "run", run)
    assert BSP.compile_paper(tmp_path, "paper_twocolumn.tex") == 14
    assert ("bibtex", "paper_twocolumn") in calls
    assert all(c[-1] == "paper_twocolumn.tex" for c in calls if c[0] == "pdflatex")


def test_unplaceable_float_fails_the_layout_gate():
    assert BSP.BAD_LOG.search("LaTeX Warning: A float is stuck (cannot be placed)")
    assert BSP.BAD_LOG.search("LaTeX Warning: Float too large for page")


def test_native_aps_control_notice_keeps_real_bibliography_warnings():
    notice = "Warning--jnrlst (dependency: not reversed) set 1"
    assert BSP.bibliography_warnings(notice) == []
    warning = "Warning--I didn't find a database entry for missing"
    assert BSP.bibliography_warnings(notice + "\n" + warning) == [warning]
