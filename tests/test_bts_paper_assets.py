"""Regression and integrity test suite for BTS paper assets.

Validates that all figures, LaTeX files, compiled PDF, and verification manifests
exist, match their audited cryptographic digests, and satisfy formatting constraints.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = REPO_ROOT / "docs" / "paper_bts"
PROVENANCE_PATH = PAPER_DIR / "draft_provenance.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def test_provenance_file_exists():
    assert PROVENANCE_PATH.exists(), f"Provenance file not found at {PROVENANCE_PATH}"
    with PROVENANCE_PATH.open("r") as f:
        data = json.load(f)
    assert data.get("status") == "completed publication package; Tasks B01-B12 verified"
    assert "verified_publication_assets_sha256" in data


def test_paper_pdf_integrity():
    pdf_path = PAPER_DIR / "paper.pdf"
    assert pdf_path.exists(), "paper.pdf is missing"
    assert pdf_path.stat().st_size > 100000, "paper.pdf file size is suspiciously small"


def test_all_five_figures_exist():
    for i in range(1, 6):
        pdf_name = f"figures/fig{i}_*.pdf"
        matching = list(PAPER_DIR.glob(pdf_name))
        assert len(matching) == 1, f"Expected exactly one matching file for {pdf_name}, found {matching}"
        assert matching[0].stat().st_size > 5000, f"Figure {matching[0]} appears empty or corrupt"


def test_sha256_matches_provenance():
    with PROVENANCE_PATH.open("r") as f:
        prov = json.load(f)

    assets = prov["verified_publication_assets_sha256"]
    for rel_path, expected_hash in assets.items():
        target = PAPER_DIR / rel_path
        assert target.exists(), f"Asset {rel_path} declared in provenance is missing on disk"
        actual_hash = sha256_file(target)
        assert actual_hash == expected_hash, (
            f"Digest mismatch for {rel_path}: expected {expected_hash}, got {actual_hash}"
        )


def test_archived_latex_macros_present():
    macro_file = PAPER_DIR / "generated" / "archived_results.tex"
    assert macro_file.exists()
    content = macro_file.read_text()
    assert r"\newcommand{\BtsPeakX}{31.4368}" in content
    assert r"\newcommand{\BtsPeakY}{50.7459}" in content
    assert r"\newcommand{\BtsMedianX}{0.00208629}" in content
