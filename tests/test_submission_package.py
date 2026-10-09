"""Tests for the submission package builder helpers (no LaTeX run)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bsp", ROOT / "scripts" / "build_submission_package.py")
BSP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BSP)


def test_referenced_figures_exist_and_are_generated():
    figs = BSP.referenced_figures((BSP.PAPER / "paper.tex").read_text())
    assert len(figs) == 7
    assert all(f.startswith("generated/figures/") and (BSP.PAPER / f).is_file() for f in figs)


def test_supplement_files_exist():
    assert all((BSP.PAPER / r).is_file() for r in BSP.SUPPLEMENT)


def test_log_gate_patterns():
    assert BSP.BAD_LOG.search("LaTeX Warning: Reference `x' on page 1 undefined")
    assert BSP.BAD_LOG.search("Overfull \\hbox (3pt too wide)")
    assert not BSP.BAD_LOG.search("Output written on paper.pdf (10 pages, 1 bytes).")
