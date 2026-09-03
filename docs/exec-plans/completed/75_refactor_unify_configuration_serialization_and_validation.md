# Milestone 75 — Task 11: Unify Configuration Serialization and Validation Framework

## Executive Summary

Task 11 establishes a unified, robust, type-safe serialization, deserialization, and domain validation architecture across the `nkm_injection` package. A reusable `SerializableConfigMixin` was created and adopted by all core configuration classes, standardizing JSON round-trip serialization, file I/O (`.to_dict()`, `.to_json()`, `.save()`, `.from_dict()`, `.from_json()`, `.load()`), nested dataclass translation, unknown key tolerance, and physical domain validation guards.

---

## Key Achievements

### 1. Created `SerializableConfigMixin` Base Framework
- **Location**: [`src/nkm_injection/results_schema.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/results_schema.py)
- **Features**:
  - `to_dict()`: Recursively converts dataclass instances, nested dataclasses, dictionaries, tuples, `pathlib.Path` objects, NumPy scalars (`np.integer`, `np.floating`), and NumPy arrays (`.tolist()`) to clean Python dicts.
  - `to_json(indent=2)`: Serializes config state to formatted JSON strings.
  - `save(filepath)`: Saves JSON output to disk, automatically creating parent directories.
  - `from_dict(data)`: Constructs and type-coerces configuration instances from raw dictionaries, gracefully ignoring unexpected extra fields, converting sequences to typed `Tuple`/`List`, mapping nested dictionaries to child dataclasses (e.g. `BTSOptimizationConfig`, `QuadrupoleHardwareBounds`), and executing validation guards.
  - `from_json(json_str)`: Deserializes directly from JSON strings.
  - `load(filepath)`: Loads and parses configuration files from disk with `FileNotFoundError` checks.
  - `validate()`: Domain validation hook executed upon construction or deserialization.

### 2. Integrated Framework Across Configuration Dataclasses
Inherited `SerializableConfigMixin` and added domain constraint validation methods to all configuration classes:

| Configuration Dataclass | Source Module | Domain Validation Guards |
| :--- | :--- | :--- |
| [`PublicationManifest`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/results_schema.py) | `src/nkm_injection/results_schema.py` | Validates upstream run directories and SHA-256 data hashes |
| [`BTSConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/bts_lattice.py) | `src/nkm_injection/bts_lattice.py` | `energy_eV > 0`, non-negative magnet/drift lengths, positive apertures |
| [`StorageRingInjectionConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/storage_ring_injection.py) | `src/nkm_injection/storage_ring_injection.py` | `energy_eV > 0`, `nkm_length_m > 0`, positive emittances, Twiss betas |
| [`BTSMOGAConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/moga.py) | `src/nkm_injection/moga.py` | `pop_size > 0`, `n_gen > 0`, `quad_bounds[0] < quad_bounds[1]`, nested configs |
| [`ErrorBudgetConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/errors.py) | `src/nkm_injection/errors.py` | Non-negative standard deviations across all 5 uncertainty categories |
| [`OpticsTargetConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/objectives.py) | `src/nkm_injection/objectives.py` | Positive target/initial Twiss betas, positive normalization scales |
| [`BTSOptimizationConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/optimization.py) | `src/nkm_injection/optimization.py` | `max_iter > 0`, valid quad bounds, nested target & constraint configs |
| [`BTSConstraintConfig`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/constraints.py) | `src/nkm_injection/constraints.py` | `energy_eV > 0`, positive envelope limits, valid per-element quad bounds |
| [`QuadrupoleHardwareBounds`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/constraints.py) | `src/nkm_injection/constraints.py` | `k_min < k_max`, `r_bore_m > 0`, `b_pole_max_T > 0` |

### 3. Expanded Test Suite
- **Location**: [`tests/test_manifest_paper_pipeline.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_manifest_paper_pipeline.py)
- **Tests Added**:
  - `test_serializable_config_mixin_roundtrips`: Validated 100% round-trip fidelity (`to_dict` -> `from_dict`, `to_json` -> `from_json`, `save` -> `load`) for all 9 configuration dataclasses.
  - `test_serializable_config_mixin_extra_keys_ignored`: Verified backward/forward compatibility when extra or unknown keys exist in input dictionaries/JSON files.
  - `test_serializable_config_nested_roundtrip`: Verified multi-level nested serialization and deserialization (e.g., `BTSMOGAConfig` -> `BTSOptimizationConfig` -> `OpticsTargetConfig`).
  - `test_validation_guards_catch_invalid_values`: Verified `ValueError` triggering on negative energies, inverted quadrupole bounds, negative error tolerances, non-positive optical normalizations, and non-physical aperture limits.

---

## Verification & Status

- **Unit Test Suite**: 181 passing tests (4 new tests added).
- **Protected Files Integrity**: Unchanged and verified against SHA-256 baseline.
- **Package Exports**: Exported `SerializableConfigMixin` and configuration classes via [`src/nkm_injection/__init__.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/__init__.py).
