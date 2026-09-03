"""
Unit and integration tests for fully data-driven paper pipeline (Task 08)
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.results_schema import (
    PaperResultSchema,
    compute_file_hash,
    compute_input_data_hashes,
    compute_rms_envelope
)
from src.nkm_injection.paper import (
    run_paper_pipeline,
    set_publication_style,
    PUBLICATION_COLORS
)


def test_input_data_hashes():
    hashes = compute_input_data_hashes(REPO_ROOT)

    assert "By.txt" in hashes
    assert "kickmap_file.txt" in hashes
    assert "K4GSR_HBIv4-1.mat" in hashes
    assert len(hashes["By.txt"]) == 64  # SHA-256 hex string length


def test_rms_envelope_formula():
    beta_m = np.array([10.0, 20.0])
    disp_m = np.array([0.1, 0.2])
    emit_mrad = 1e-7
    espread = 1.1e-3

    env_3sig = compute_rms_envelope(beta_m, disp_m, emit_mrad=emit_mrad, espread=espread, n_sigma=3.0)

    # Expected rms: sqrt( 1e-7 * 10 + (0.1 * 1.1e-3)^2 ) = sqrt( 1e-6 + 1.21e-8 ) = sqrt(1.0121e-6)
    expected_rms_0 = np.sqrt(emit_mrad * 10.0 + (0.1 * espread)**2)
    assert env_3sig[0] == pytest.approx(3.0 * expected_rms_0, rel=1e-6)


def test_paper_pipeline_execution(tmp_path):
    schema = PaperResultSchema(run_id="test_run", base_dir=tmp_path)
    schema.initialize_directories()

    assert schema.figures_dir.is_dir()
    assert schema.tables_dir.is_dir()

    summary = run_paper_pipeline(repo_root=REPO_ROOT, run_id="test_run_pipeline", compile_pdf=False)
    assert summary["input_hashes_verified"] is True
    assert summary["tables_count"] >= 2
    assert summary["figures_count"] >= 2


def test_set_publication_style():
    """Verify set_publication_style configures matplotlib rc_params and color palette."""
    params = set_publication_style(font_size=11, dpi=300)
    assert params["font.size"] == 11
    assert params["figure.dpi"] == 300

    assert "beta_x" in PUBLICATION_COLORS
    assert "beta_y" in PUBLICATION_COLORS
    assert "dispersion" in PUBLICATION_COLORS


# ---------------------------------------------------------------------------
# Task 16 — LaTeX Table and Macro Builder Tests
# ---------------------------------------------------------------------------

from src.nkm_injection.paper import (
    escape_latex,
    format_scientific,
    format_uncertainty,
    LaTeXTableBuilder,
    LaTeXMacroBuilder
)


def test_escape_latex():
    """Verify special LaTeX character escaping while preserving math mode."""
    raw = "Beta_x error of 5% in beam #1 & #2 with $\\beta_x = 10.5$"
    escaped = escape_latex(raw)
    assert "\\%" in escaped
    assert "\\_" in escaped
    assert "\\&" in escaped
    assert "\\#" in escaped
    assert "$\\beta_x = 10.5$" in escaped  # Math block preserved intact


def test_format_scientific_and_uncertainty():
    """Verify scientific notation and uncertainty string formatting."""
    assert format_scientific(0.0) == "0"
    assert format_scientific(12) == "12"
    assert format_scientific(3.14159, precision=2) == "3.14"
    assert "10^{-5}" in format_scientific(1.23e-5, precision=2)
    assert "10^{6}" in format_scientific(4.5e6, precision=1)

    unc_str = format_uncertainty(1.234, 0.056, precision=2)
    assert unc_str == "$1.23 \\pm 0.06$"


def test_latex_table_builder(tmp_path):
    """Verify LaTeXTableBuilder row addition, validation, rendering, and disk output."""
    builder = LaTeXTableBuilder(
        caption="Sample Optical Parameters",
        label="tab:sample_optics",
        columns=["Parameter", "Value", "Unit"],
        alignment="lcl"
    )
    builder.add_row("$\\beta_x$", 13.626, "m")
    builder.add_row(["$\\alpha_x$", -2.046, "-"])

    # Column length mismatch validation
    with pytest.raises(ValueError, match="does not match column count"):
        builder.add_row("Extra", 1.0, "m", "Unexpected")

    latex_str = builder.render_latex()
    assert "\\begin{table}" in latex_str
    assert "\\toprule" in latex_str
    assert "\\midrule" in latex_str
    assert "\\bottomrule" in latex_str
    assert "\\label{tab:sample_optics}" in latex_str
    assert "13.626" in latex_str

    md_str = builder.render_markdown()
    assert "# Sample Optical Parameters" in md_str
    assert "| Parameter | Value | Unit |" in md_str

    # Save to disk
    tex_file = builder.save(tmp_path / "table.tex")
    md_file = builder.save(tmp_path / "table.md")
    assert tex_file.is_file()
    assert md_file.is_file()


def test_latex_macro_builder(tmp_path):
    """Verify LaTeXMacroBuilder declaration rendering and disk output."""
    builder = LaTeXMacroBuilder()
    builder.add("beam_energy_GeV", 4.0, precision=1, unit="GeV")
    builder.add("\\bts_length", 27.812, precision=3, unit="m")
    builder.add("kicker_type", "Nonlinear")

    rendered = builder.render()
    assert "\\newcommand{\\beamenergyGeV}{4.0\\,\\text{GeV}}" in rendered
    assert "\\newcommand{\\btslength}{27.812\\,\\text{m}}" in rendered
    assert "\\newcommand{\\kickertype}{Nonlinear}" in rendered

    macro_file = builder.save(tmp_path / "paper_macros.tex")
    assert macro_file.is_file()


