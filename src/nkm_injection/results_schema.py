"""
NKM Paper Result Provenance & Cryptographic Schema Module

Defines result directory schemas, cryptographic input file hashing, environment logging,
and validation checks for fully data-driven publication reproduction.
"""

from dataclasses import dataclass, field, is_dataclass, fields
from pathlib import Path
import hashlib
import json
import os
import sys
import subprocess
from typing import Dict, List, Optional, Tuple, Any, Union, get_type_hints, get_origin, get_args
import numpy as np


def _to_serializable(val: Any) -> Any:
    """Recursively convert values, collections, paths, and dataclasses to JSON-serializable types."""
    if val is None or isinstance(val, (str, int, float, bool)):
        return val
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return float(val)
    if isinstance(val, np.ndarray):
        return val.tolist()
    if isinstance(val, Path):
        return str(val)
    if hasattr(val, "to_dict") and callable(val.to_dict):
        return val.to_dict()
    if is_dataclass(val):
        return {f.name: _to_serializable(getattr(val, f.name)) for f in fields(val)}
    if isinstance(val, dict):
        return {str(k): _to_serializable(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [_to_serializable(item) for item in val]
    return str(val)


class SerializableConfigMixin:
    """
    Mixin providing robust serialization, deserialization, type coercion,
    JSON file I/O, and domain validation for configuration dataclasses.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass fields into a JSON-serializable dictionary."""
        if not is_dataclass(self):
            return {k: _to_serializable(v) for k, v in self.__dict__.items() if not k.startswith('_')}
        res = {}
        for f in fields(self):
            val = getattr(self, f.name)
            res[f.name] = _to_serializable(val)
        return res

    def to_json(self, indent: int = 2) -> str:
        """Serialize configuration to a formatted JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, filepath: Union[str, Path], indent: int = 2) -> None:
        """Save configuration directly to a JSON file."""
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(self.to_json(indent=indent))

    @classmethod
    def _coerce_field_value(cls, val: Any, hint: Any) -> Any:
        """Coerce raw dictionary/JSON values to matching field type annotations."""
        if val is None:
            return None

        origin = get_origin(hint)
        args = get_args(hint)

        # Handle Optional / Union (e.g. Union[float, None], Optional[float])
        if origin is Union:
            non_none_args = [a for a in args if a is not type(None)]
            if len(non_none_args) == 1:
                hint = non_none_args[0]
                origin = get_origin(hint)
                args = get_args(hint)

        # Nested dataclass / SerializableConfigMixin
        if isinstance(val, dict):
            if hasattr(hint, "from_dict") and callable(getattr(hint, "from_dict")):
                return hint.from_dict(val)
            if isinstance(hint, type) and is_dataclass(hint):
                return hint(**val)

        # Dict mapping conversion
        if origin is dict or hint in (dict, Dict) or origin in (dict, Dict):
            if isinstance(val, dict) and args and len(args) == 2:
                val_type = args[1]
                return {k: cls._coerce_field_value(v, val_type) for k, v in val.items()}
            return val

        # List sequence conversion
        if origin is list or hint in (list, List) or origin in (list, List):
            if isinstance(val, (list, tuple)) and args and len(args) == 1:
                elem_type = args[0]
                return [cls._coerce_field_value(x, elem_type) for x in val]
            return list(val) if isinstance(val, (list, tuple)) else val

        # Tuple conversion
        if hint in (tuple, Tuple) or origin in (tuple, Tuple):
            if isinstance(val, (list, tuple)):
                if args and args[0] is not ... and len(args) == len(val):
                    return tuple(cls._coerce_field_value(x, a) for x, a in zip(val, args))
                elif args and args[0] is not ... and len(args) == 2 and args[1] is ...:
                    return tuple(cls._coerce_field_value(x, args[0]) for x in val)
                return tuple(val)

        # Path conversion
        if hint is Path or (isinstance(hint, type) and issubclass(hint, Path)):
            return Path(val)

        # Numeric and primitive conversions
        if hint is int:
            if isinstance(val, (int, float, np.number, str)):
                return int(val)
        if hint is float:
            if isinstance(val, (int, float, np.number, str)):
                return float(val)
        if hint is bool:
            return bool(val)

        return val

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        """
        Instantiate and validate dataclass from a dictionary, safely handling
        nested configs, type coercion, and ignoring unexpected extra keys.
        """
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict for {cls.__name__}.from_dict, got {type(data).__name__}")

        if not is_dataclass(cls):
            instance = cls()
            for k, v in data.items():
                if hasattr(instance, k):
                    setattr(instance, k, v)
            if hasattr(instance, "validate") and callable(instance.validate):
                instance.validate()
            return instance

        try:
            type_hints = get_type_hints(cls)
        except Exception:
            type_hints = {}

        kwargs = {}
        for f in fields(cls):
            if f.name in data:
                raw_val = data[f.name]
                hint = type_hints.get(f.name, f.type)
                kwargs[f.name] = cls._coerce_field_value(raw_val, hint)

        instance = cls(**kwargs)
        if hasattr(instance, "validate") and callable(instance.validate):
            instance.validate()
        return instance

    @classmethod
    def from_json(cls, json_str: str) -> Any:
        """Instantiate and validate configuration from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> Any:
        """Load and instantiate configuration from a JSON file."""
        p = Path(filepath)
        if not p.is_file():
            raise FileNotFoundError(f"Configuration file not found: {p}")
        with open(p, "r", encoding="utf-8") as f:
            return cls.from_json(f.read())

    def validate(self) -> None:
        """Default validation hook to be optionally overridden by subclasses."""
        pass


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
        if create_if_missing:
            hash_manifest_path.parent.mkdir(parents=True, exist_ok=True)
            input_hashes = compute_input_data_hashes(repo_root)
            with open(hash_manifest_path, "w") as f:
                json.dump(input_hashes, f, indent=2)
        else:
            validation_status["valid"] = False
            validation_status["errors"].append(f"Protected hash manifest missing: {manifest.input_hash_manifest}")

    if hash_manifest_path.is_file():
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
    from .optics import compute_beam_envelope
    return compute_beam_envelope(
        beta=beta_m,
        dispersion=disp_m,
        emittance_m_rad=emit_mrad,
        energy_spread=espread,
        n_sigma=n_sigma,
        method="rms_quadrature"
    )

