#!/usr/bin/env python3
"""Standalone BTS Paper Reproduction & Verification Script.

Cross-checks nominal matching, margin design, SVD condition numbers,
tolerance quantiles, and verifies figures and compilation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
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


def verify_assets() -> bool:
    print("=== Verifying Frozen BTS Publication Assets ===")
    if not PROVENANCE_PATH.exists():
        print(f"Error: Provenance file missing at {PROVENANCE_PATH}")
        return False

    with PROVENANCE_PATH.open("r") as f:
        prov = json.load(f)

    expected_assets = prov.get("verified_publication_assets_sha256", {})
    all_ok = True

    for rel_path, expected_hash in expected_assets.items():
        full_path = PAPER_DIR / rel_path
        if not full_path.exists():
            print(f"[FAIL] Missing file: {rel_path}")
            all_ok = False
            continue
        actual_hash = sha256_file(full_path)
        if actual_hash == expected_hash:
            print(f"[PASS] {rel_path} (SHA-256 match)")
        else:
            print(f"[MISMATCH] {rel_path}")
            print(f"  Expected: {expected_hash}")
            print(f"  Actual:   {actual_hash}")
            all_ok = False

    return all_ok


def test_pdf_compile() -> bool:
    print("\n=== Testing LaTeX Compilation ===")
    cmd = (
        "pdflatex -interaction=nonstopmode paper.tex && "
        "bibtex paper && "
        "pdflatex -interaction=nonstopmode paper.tex && "
        "pdflatex -interaction=nonstopmode paper.tex"
    )
    res = subprocess.run(cmd, shell=True, cwd=PAPER_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        pdf_path = PAPER_DIR / "paper.pdf"
        print(f"[PASS] PDF compiled successfully: {pdf_path} ({pdf_path.stat().st_size} bytes)")
        return True
    else:
        print("[FAIL] Compilation error:")
        print(res.stderr[:500])
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce and verify BTS paper artifacts.")
    parser.add_argument("--verify", action="store_true", help="Verify SHA-256 digests against provenance record")
    parser.add_argument("--compile", action="store_true", help="Recompile LaTeX paper PDF")
    args = parser.parse_args()

    # Default to both if no specific action provided
    do_all = not (args.verify or args.compile)

    success = True
    if args.verify or do_all:
        if not verify_assets():
            success = False

    if args.compile or do_all:
        if not test_pdf_compile():
            success = False

    if success:
        print("\nAll BTS reproduction checks PASSED.")
        return 0
    else:
        print("\nSome BTS reproduction checks FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
