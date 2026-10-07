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


# Preserve the established public import while separating configuration from provenance.
from .configuration import SerializableConfigMixin


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
class PublicationManifest(SerializableConfigMixin):
    """Publication manifest container linking validated simulation run outputs."""
    field_validation_run: str = "results/field_validation/run_01"
    tracking_convergence_run: str = "results/tracking_convergence/run_01"
    bts_optimization_run: str = "results/bts_publication_optimization/run_01"
    injection_run: str = "results/multiturn_injection/run_01"
    tolerance_run: str = "results/publication_tolerances/run_01"
    moga_run: str = "results/publication_moga/run_01"
    input_hash_manifest: str = "results/baseline/protected_files_manifest.json"
    git_commit: str = ""


def _check_publication_hashes(manifest, root):
    """Read and verify a complete scientific baseline without changing files."""
    path = root / manifest.input_hash_manifest
    if not path.is_file():
        raise ValueError(f"Protected hash manifest missing: {manifest.input_hash_manifest}")
    def pairs(items):
        data = {}
        for key, value in items:
            if key in data:
                raise ValueError(f"Duplicate baseline entry: {key}")
            data[key] = value
        return data
    expected = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)
    current = compute_input_data_hashes(root)
    if not isinstance(expected, dict) or not set(current).issubset(expected):
        raise ValueError('Hash baseline must include every required scientific input')
    for name, digest in expected.items():
        source = (root / name).resolve()
        if Path(name).is_absolute() or not source.is_relative_to(root):
            raise ValueError(f'Invalid relative baseline path: {name}')
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError(f'Invalid SHA-256 baseline for {name}')
        if compute_file_hash(source) != digest:
            raise ValueError(f'Hash mismatch for protected file {name}')
    return current


def _publication_runs(manifest):
    return {name: getattr(manifest, name) for name in (
        'field_validation_run', 'tracking_convergence_run', 'bts_optimization_run',
        'injection_run', 'tolerance_run', 'moga_run')}


def initialize_publication_manifest(manifest: PublicationManifest, repo_root: Path) -> Dict[str, Any]:
    """Explicitly create missing run directories/baseline; never rebase existing hashes.

    Initialization records present source bytes, not scientific validation or
    stage completion. Units and source data are unchanged.
    """
    root = Path(repo_root).resolve()
    hashes = compute_input_data_hashes(root)
    if 'MISSING' in hashes.values():
        raise FileNotFoundError('Cannot initialize with missing scientific inputs')
    baseline = root / manifest.input_hash_manifest
    if baseline.exists():
        _check_publication_hashes(manifest, root)
    runs = _publication_runs(manifest)
    for name, relative in runs.items():
        path = root / relative
        if path.exists() and not path.is_dir():
            raise ValueError(f'Result run is not a directory: {name}: {relative}')
    created = []
    for relative in runs.values():
        path = root / relative
        if not path.exists():
            path.mkdir(parents=True)
            created.append(str(path))
    baseline_created = not baseline.exists()
    if baseline_created:
        baseline.parent.mkdir(parents=True, exist_ok=True)
        with baseline.open('x', encoding='utf-8') as handle:
            json.dump(hashes, handle, indent=2, allow_nan=False)
    return {'status': 'initialized', 'created_run_directories': created,
            'baseline_created': baseline_created, 'baseline_path': str(baseline),
            'stage_artifacts_verified': False}


def validate_publication_manifest(manifest: PublicationManifest,
                                  repo_root: Path,
                                  create_if_missing: bool = False) -> Dict[str, Any]:
    """Read-only verification of hashes and every required selected stage artifact.

    Legacy create_if_missing=True is rejected; call explicit initialization.
    Failed validation never establishes a new baseline or verifies empty runs.
    """
    if create_if_missing:
        raise ValueError('Validation is read-only; use initialize_publication_manifest explicitly')
    root = Path(repo_root).resolve()
    status = {'valid': False, 'errors': [], 'warnings': [], 'verified_runs': {},
              'upstream_artifacts': {}}
    try:
        _check_publication_hashes(manifest, root)
    except (OSError, ValueError, TypeError) as error:
        status['errors'].append(str(error))
    runs = _publication_runs(manifest)
    for name, relative in runs.items():
        if not (root / relative).is_dir():
            status['errors'].append(f'Required result run directory missing for {name}: {relative}')
    if not status['errors']:
        try:
            from .publication_inputs import load_publication_inputs
            inputs = load_publication_inputs(manifest, root)
            status['upstream_artifacts'] = inputs.provenance()
        except (OSError, ValueError, TypeError, KeyError) as error:
            status['errors'].append(str(error))
    if not status['errors']:
        status['valid'] = True
        status['verified_runs'] = runs
    return status


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
    from .optics import compute_beam_envelope
    return compute_beam_envelope(
        beta=beta_m,
        dispersion=disp_m,
        emittance_m_rad=emit_mrad,
        energy_spread=espread,
        n_sigma=n_sigma,
        method="rms_quadrature"
    )

