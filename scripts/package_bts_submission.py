#!/usr/bin/env python3
"""Package BTS manuscript sources into a self-contained submission tarball.

Verifies SHA-256 digests and tests isolated compilation.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = REPO_ROOT / "docs" / "paper_bts"
OUTPUT_DIR = REPO_ROOT / "results" / "bts_submission"

MANIFEST_FILES = [
    "paper.tex",
    "paper.bib",
    "generated/archived_results.tex",
    "draft_provenance.json",
    "figures/fig1_bts_layout.pdf",
    "figures/fig2_svd_knobs.pdf",
    "figures/fig3_margin_tradeoff.pdf",
    "figures/fig4_tolerance_curves.pdf",
    "figures/fig5_heldout_transmission.pdf",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_submission_bundle() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tarball_path = OUTPUT_DIR / "bts_jkps_submission.tar.gz"

    print("Checking files to package...")
    checksums = {}
    for rel_path in MANIFEST_FILES:
        full_path = PAPER_DIR / rel_path
        if not full_path.exists():
            raise FileNotFoundError(f"Missing required file: {full_path}")
        csum = sha256_file(full_path)
        checksums[rel_path] = csum
        print(f"  {rel_path}: {csum[:16]}...")

    with tarfile.open(tarball_path, "w:gz") as tar:
        for rel_path in MANIFEST_FILES:
            full_path = PAPER_DIR / rel_path
            tar.add(full_path, arcname=rel_path)

    tar_sha = sha256_file(tarball_path)
    print(f"\nBundle created: {tarball_path}")
    print(f"SHA-256: {tar_sha}")

    # Verify extraction and compilation in isolated temp directory
    test_dir = OUTPUT_DIR / "isolated_build_test"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True)

    print("\nExtracting to isolated test directory and compiling...")
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(path=test_dir)

    cmd = (
        "pdflatex -interaction=nonstopmode paper.tex && "
        "bibtex paper && "
        "pdflatex -interaction=nonstopmode paper.tex && "
        "pdflatex -interaction=nonstopmode paper.tex"
    )
    res = subprocess.run(cmd, shell=True, cwd=test_dir, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr)
        raise RuntimeError("Isolated PDF build failed!")

    compiled_pdf = test_dir / "paper.pdf"
    if not compiled_pdf.exists():
        raise RuntimeError("paper.pdf was not produced in isolated build!")

    print(f"Isolated build SUCCESS: {compiled_pdf} ({compiled_pdf.stat().st_size} bytes)")
    
    # Save bundle manifest
    manifest_info = {
        "tarball": str(tarball_path),
        "tarball_sha256": tar_sha,
        "files": checksums,
        "isolated_build_status": "SUCCESS"
    }
    with (OUTPUT_DIR / "bundle_manifest.json").open("w") as f:
        json.dump(manifest_info, f, indent=2)

    return tarball_path


if __name__ == "__main__":
    build_submission_bundle()
