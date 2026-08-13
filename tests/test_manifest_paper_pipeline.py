"""
Task 10 — Manifest Validation and Paper Pipeline Tests

Verifies PublicationManifest schema validation, error stopping on missing or corrupted inputs/runs,
and reproduce_paper CLI integration.
"""

import sys
import json
import pytest
from pathlib import Path
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm.results_schema import (
    PublicationManifest,
    validate_publication_manifest,
    compute_input_data_hashes
)
from src.nkm.paper import run_paper_pipeline


def test_publication_manifest_load_save(tmp_path):
    manifest = PublicationManifest(git_commit="test_commit_123")
    manifest_file = tmp_path / "test_manifest.json"
    manifest.save(manifest_file)

    assert manifest_file.is_file()

    loaded = PublicationManifest.load(manifest_file)
    assert loaded.git_commit == "test_commit_123"
    assert loaded.field_validation_run == "results/field_validation/run_01"


def test_validate_publication_manifest_success():
    manifest = PublicationManifest(
        field_validation_run="results/field_validation",
        tracking_convergence_run="results/tracking_convergence",
        bts_optimization_run="results/baseline",
        injection_run="results/multiturn_injection",
        tolerance_run="results/baseline",
        moga_run="results/baseline",
        input_hash_manifest="results/baseline/protected_files_manifest.json"
    )

    val = validate_publication_manifest(manifest, REPO_ROOT)
    assert val["valid"] is True
    assert len(val["errors"]) == 0
    assert len(val["verified_runs"]) == 6


def test_validate_publication_manifest_missing_run():
    manifest = PublicationManifest(
        field_validation_run="results/non_existent_run_directory_xyz"
    )

    val = validate_publication_manifest(manifest, REPO_ROOT, create_if_missing=False)
    assert val["valid"] is False
    assert any("non_existent_run_directory_xyz" in err for err in val["errors"])


def test_run_paper_pipeline_manifest_execution(tmp_path):
    manifest = PublicationManifest(
        field_validation_run="results/field_validation",
        tracking_convergence_run="results/tracking_convergence",
        bts_optimization_run="results/baseline",
        injection_run="results/multiturn_injection",
        tolerance_run="results/baseline",
        moga_run="results/baseline",
        input_hash_manifest="results/baseline/protected_files_manifest.json"
    )

    summary = run_paper_pipeline(repo_root=REPO_ROOT, run_id="test_manifest_run", manifest=manifest)
    assert summary["manifest_valid"] is True
    assert summary["input_hashes_verified"] is True
    assert summary["tables_count"] >= 2
    assert summary["figures_count"] >= 2


def test_run_paper_pipeline_fails_on_invalid_manifest():
    manifest = PublicationManifest(
        field_validation_run="results/missing_directory_123"
    )

    with pytest.raises(ValueError, match="Publication manifest validation failed"):
        run_paper_pipeline(repo_root=REPO_ROOT, run_id="test_invalid_run", manifest=manifest, create_if_missing=False)
