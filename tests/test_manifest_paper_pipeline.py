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

from src.nkm_injection.results_schema import (
    PublicationManifest,
    validate_publication_manifest,
    compute_input_data_hashes
)
from src.nkm_injection.paper import run_paper_pipeline


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

    summary = run_paper_pipeline(repo_root=REPO_ROOT, run_id="test_manifest_run", manifest=manifest, compile_pdf=False)
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


# ===========================================================================
# Task 11 — SerializableConfigMixin & Validation Tests
# ===========================================================================

from src.nkm_injection import (
    SerializableConfigMixin,
    BTSConfig,
    StorageRingInjectionConfig,
    BTSMOGAConfig,
    ErrorBudgetConfig,
    OpticsTargetConfig,
    BTSConstraintConfig,
    QuadrupoleHardwareBounds,
)
from src.nkm_injection.optimization import BTSOptimizationConfig


def test_serializable_config_mixin_roundtrips(tmp_path):
    """Verify to_dict/from_dict, to_json/from_json, save/load for all config dataclasses."""
    configs = [
        BTSConfig(),
        StorageRingInjectionConfig(),
        BTSMOGAConfig(),
        ErrorBudgetConfig(),
        OpticsTargetConfig(),
        PublicationManifest(),
        BTSOptimizationConfig(),
        BTSConstraintConfig(),
        QuadrupoleHardwareBounds("q11", k_min=-2.5, k_max=2.5),
    ]

    for cfg in configs:
        cls = cfg.__class__
        # 1. to_dict -> from_dict
        d = cfg.to_dict()
        assert isinstance(d, dict)
        reconstructed_from_dict = cls.from_dict(d)
        assert isinstance(reconstructed_from_dict, cls)

        # 2. to_json -> from_json
        j = cfg.to_json()
        assert isinstance(j, str)
        reconstructed_from_json = cls.from_json(j)
        assert isinstance(reconstructed_from_json, cls)

        # 3. save -> load
        filepath = tmp_path / f"{cls.__name__}.json"
        cfg.save(filepath)
        assert filepath.is_file()
        loaded = cls.load(filepath)
        assert isinstance(loaded, cls)


def test_serializable_config_mixin_extra_keys_ignored():
    """Verify that unknown extra keys in dictionary/JSON do not cause failures."""
    data = {
        "energy_eV": 4.0e9,
        "unexpected_new_field": 12345,
        "another_unknown_key": "some_string",
    }
    bts_cfg = BTSConfig.from_dict(data)
    assert bts_cfg.energy_eV == 4.0e9
    assert not hasattr(bts_cfg, "unexpected_new_field")


def test_serializable_config_nested_roundtrip(tmp_path):
    """Verify complex nested dataclass serialization (BTSMOGAConfig -> BTSOptimizationConfig -> OpticsTargetConfig)."""
    moga_cfg = BTSMOGAConfig(
        pop_size=50,
        n_gen=25,
        seed=123,
        quad_bounds=(-2.8, 2.8),
    )
    # Mutate a nested value to verify deep round-trip preservation
    moga_cfg.bts_opt_config.max_iter = 77
    moga_cfg.bts_opt_config.target_config.target_beta_x = 3.5

    saved_path = tmp_path / "nested_moga.json"
    moga_cfg.save(saved_path)

    loaded = BTSMOGAConfig.load(saved_path)
    assert loaded.pop_size == 50
    assert loaded.n_gen == 25
    assert loaded.seed == 123
    assert loaded.quad_bounds == (-2.8, 2.8)
    assert loaded.bts_opt_config.max_iter == 77
    assert loaded.bts_opt_config.target_config.target_beta_x == 3.5


def test_validation_guards_catch_invalid_values():
    """Verify that validation guards raise ValueError on non-physical configuration values."""
    # 1. BTSConfig: negative energy
    with pytest.raises(ValueError, match="energy_eV must be positive"):
        BTSConfig.from_dict({"energy_eV": -1.0})

    # 2. StorageRingInjectionConfig: negative length or beta
    with pytest.raises(ValueError, match="nkm_length_m must be positive"):
        StorageRingInjectionConfig.from_dict({"nkm_length_m": -0.5})

    # 3. BTSMOGAConfig: inverted quad bounds
    with pytest.raises(ValueError, match="quad_bounds must be a valid"):
        BTSMOGAConfig.from_dict({"quad_bounds": [3.0, -3.0]})

    # 4. ErrorBudgetConfig: negative tolerance std
    with pytest.raises(ValueError, match="cannot be negative"):
        ErrorBudgetConfig.from_dict({"quad_k_rel_std": -0.01})

    # 5. OpticsTargetConfig: negative normalization sigma
    with pytest.raises(ValueError, match="must be positive"):
        OpticsTargetConfig.from_dict({"sigma_beta_x": -0.05})

    # 6. QuadrupoleHardwareBounds: k_min >= k_max
    with pytest.raises(ValueError, match="must be less than k_max"):
        QuadrupoleHardwareBounds.from_dict({"name": "q11", "k_min": 3.0, "k_max": -3.0})

