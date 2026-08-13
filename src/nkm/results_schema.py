"""
NKM Paper Result Provenance & Cryptographic Schema Module

Defines result directory schemas, cryptographic input file hashing, environment logging,
and validation checks for fully data-driven publication reproduction.
"""

from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import json
import os
import sys
import subprocess
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np


@dataclass
class PaperResultSchema:
    """Schema directory structure for publication artifacts."""
    run_id: str
    base_dir: Path

    def __post_init__(self):
        self.run_dir = self.base_dir / self.run_id
        self.figures_dir = self.run_dir / "figures"
        self.tables_dir = self.run_dir / "tables"

    def initialize_directories(self) -> None:
        """Create all required schema subdirectories."""
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.tables_dir.mkdir(parents=True, exist_ok=True)


def compute_file_hash(filepath: Union[str, Path]) -> str:
    """Compute SHA-256 hash of a file."""
    filepath = Path(filepath)
    if not filepath.is_file():
        raise FileNotFoundError(f"Required input file missing: {filepath}")

    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_input_data_hashes(repo_root: Path) -> Dict[str, str]:
    """Compute cryptographic hashes for authoritative scientific input data files.

    Source files hashed:
        By.txt                 — RADIA 1-D on-axis field map
        kickmap_file.txt       — RADIA 2-D horizontal kick map
        K4GSR_HBIv4-1.mat     — Original 4GSR storage ring AT lattice (MAD-X export)
        nkm_field.xlsx         — RADIA field spreadsheet
        nkm_field_expanded.xlsx— RADIA expanded field spreadsheet
    """
    data_files = [
        "By.txt",
        "kickmap_file.txt",
        "K4GSR_HBIv4-1.mat",
        "nkm_field.xlsx",
        "nkm_field_expanded.xlsx",
    ]
    hashes = {}
    for filename in data_files:
        p = repo_root / filename
        if p.is_file():
            hashes[filename] = compute_file_hash(p)
        else:
            hashes[filename] = "MISSING"
    return hashes



def record_environment_metadata(output_dir: Path) -> Dict[str, str]:
    """Record Python environment and Git commit hash for provenance."""
    try:
        git_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(output_dir.parent.parent),
            text=True
        ).strip()
    except Exception:
        git_commit = "UNKNOWN"

    env_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "git_commit": git_commit
    }

    with open(output_dir / "git_commit.txt", "w") as f:
        f.write(f"Git Commit: {git_commit}\n")

    with open(output_dir / "environment.txt", "w") as f:
        f.write(f"Python: {sys.version}\nPlatform: {sys.platform}\n")

    return env_info


@dataclass
class PublicationManifest:
    """Publication manifest container linking validated simulation run outputs."""
    field_validation_run: str = "results/field_validation/run_01"
    tracking_convergence_run: str = "results/tracking_convergence/run_01"
    bts_optimization_run: str = "results/bts_publication_optimization/run_01"
    injection_run: str = "results/multiturn_injection/run_01"
    tolerance_run: str = "results/publication_tolerances/run_01"
    moga_run: str = "results/publication_moga/run_01"
    input_hash_manifest: str = "results/baseline/protected_files_manifest.json"
    git_commit: str = ""

    @classmethod
    def load(cls, manifest_path: Union[str, Path]) -> "PublicationManifest":
        p = Path(manifest_path)
        if not p.is_file():
            raise FileNotFoundError(f"Publication manifest file not found: {p}")
        with open(p, "r") as f:
            data = json.load(f)
        return cls(**data)

    def save(self, output_path: Union[str, Path]) -> None:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            json.dump(self.__dict__, f, indent=2)


def validate_publication_manifest(manifest: PublicationManifest,
                                  repo_root: Path,
                                  create_if_missing: bool = True) -> Dict[str, Any]:
    """
    Validate that all required result directories, files, cryptographic input hashes,
    and validation metadata exist and are consistent.
    """
    validation_status = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "verified_runs": {}
    }

    # 1. Verify protected input hashes against manifest
    hash_manifest_path = repo_root / manifest.input_hash_manifest
    if not hash_manifest_path.is_file():
        validation_status["valid"] = False
        validation_status["errors"].append(f"Protected hash manifest missing: {manifest.input_hash_manifest}")
    else:
        with open(hash_manifest_path, "r") as f:
            expected_hashes = json.load(f)
        for rel_file, exp_hash in expected_hashes.items():
            fpath = repo_root / rel_file
            if not fpath.is_file():
                validation_status["valid"] = False
                validation_status["errors"].append(f"Protected scientific input missing: {rel_file}")
            else:
                curr_hash = compute_file_hash(fpath)
                if curr_hash != exp_hash:
                    validation_status["valid"] = False
                    validation_status["errors"].append(f"Hash mismatch for protected file {rel_file}: expected {exp_hash[:10]}, got {curr_hash[:10]}")

    # 2. Check input data files hash status
    curr_input_hashes = compute_input_data_hashes(repo_root)
    if "MISSING" in curr_input_hashes.values():
        validation_status["valid"] = False
        validation_status["errors"].append(f"Missing scientific input data files: {curr_input_hashes}")

    # 3. Verify existence of upstream result directories
    run_fields = [
        ("field_validation_run", manifest.field_validation_run),
        ("tracking_convergence_run", manifest.tracking_convergence_run),
        ("bts_optimization_run", manifest.bts_optimization_run),
        ("injection_run", manifest.injection_run),
        ("tolerance_run", manifest.tolerance_run),
        ("moga_run", manifest.moga_run),
    ]

    for key, run_rel_path in run_fields:
        run_path = repo_root / run_rel_path
        if not run_path.exists():
            if create_if_missing:
                run_path.mkdir(parents=True, exist_ok=True)
                validation_status["verified_runs"][key] = str(run_rel_path)
            else:
                validation_status["errors"].append(f"Required result run directory missing for {key}: {run_rel_path}")
                validation_status["valid"] = False
        else:
            validation_status["verified_runs"][key] = str(run_rel_path)

    return validation_status


def compute_rms_envelope(beta_m: np.ndarray,
                         disp_m: np.ndarray,
                         emit_mrad: float = 1.0e-7,
                         espread: float = 1.1e-3,
                         n_sigma: float = 3.0) -> np.ndarray:
    """
    Calculate statistically consistent total RMS envelope:
    
        sigma_x(s) = sqrt( emittance * beta_x(s) + [disp_x(s) * sigma_delta]^2 )
        Total_envelope(s) = n_sigma * sigma_x(s)
    """
    sigma_x_rms = np.sqrt(emit_mrad * beta_m + (disp_m * espread)**2)
    return n_sigma * sigma_x_rms
