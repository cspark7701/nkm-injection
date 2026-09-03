# Milestone 77 — Task 13: Structure Convergence and Dynamic Acceptance Return Types

## Executive Summary

Task 13 establishes strongly typed, structured return dataclasses across the multi-turn injection convergence and acceptance analysis framework in `src/nkm_injection/convergence_study.py`. Previously loose dictionary structures returned by `particle_count_convergence_scan`, `turn_count_convergence_scan`, `compute_injection_acceptance`, and `run_ensemble_study` have been replaced with validated dataclasses (`ConvergenceScanResult`, `AcceptanceResult`, `EnsembleStudyResult`) inheriting from `SerializableConfigMixin`. These dataclasses provide full serialization, pandas DataFrame conversion, statistical summary helpers, execution time profiling, and sequence/dict indexing backward compatibility.

---

## Key Achievements

### 1. Created Strongly Typed Return Dataclasses
- **Location**: [`src/nkm_injection/convergence_study.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/convergence_study.py)
- **Dataclasses**:
  - `ConvergenceScanResult(SerializableConfigMixin)`:
    - Attributes: `scan_parameter`, `scan_values`, `efficiencies`, `survived_counts`, `cpu_times_s`, `final_emittance_x`, `final_emittance_y`, `records`, `metadata`.
    - Statistical methods: `mean_efficiency()`, `std_efficiency()`.
    - Export: `to_dataframe()` generating tabular pandas DataFrames with scan parameters, efficiencies, survived counts, and execution times.
    - Backward compatibility: Implements `__len__`, `__iter__`, and `__getitem__` supporting both positional integer/slice access and legacy string keys (`"efficiencies"`, `"survived"`, `"n_particles"`, `"n_turns"`).
  - `AcceptanceResult(SerializableConfigMixin)`:
    - Attributes: `x_grid_m`, `survival_fraction_grid`, `x_offsets_mm`, `acceptance_area_m_rad`, `xp_grid_rad`, `records`, `metadata`.
    - Acceptance helper: `acceptance_window_mm(threshold=0.9)` computing physical acceptance boundaries where capture efficiency meets the specified threshold.
    - Export: `to_dataframe()` creating structured pandas DataFrames.
    - Backward compatibility: Implements `__len__`, `__iter__`, and `__getitem__`.
  - `EnsembleStudyResult(SerializableConfigMixin)`:
    - Attributes: `label`, `kicker_model`, `tier`, `capture_efficiency_ci`, `per_seed_results`, `mean_stored_perturbation`, `first_loss_distribution`, `metadata`.
    - Dict-like interface: Implements `__getitem__`, `__contains__`, `get`, `keys`, `values`, `items`.
    - Export: `to_dataframe()` converting per-seed results to tabular form.

### 2. Refactored Convergence Study Signatures and Time Profiling
- Updated `particle_count_convergence_scan(...) -> ConvergenceScanResult`:
  - Added per-step runtime measurement using `time.perf_counter()`.
  - Recorded final emittance metrics and surviving particle counts.
- Updated `turn_count_convergence_scan(...) -> ConvergenceScanResult`:
  - Added per-step runtime measurement and emittance tracking.
- Updated `compute_injection_acceptance(...) -> AcceptanceResult`:
  - Added numerical trapezoidal integration of acceptance area over $x$.
- Updated `run_ensemble_study(...) -> EnsembleStudyResult`:
  - Returned structured `EnsembleStudyResult` instance.

### 3. Integrated Scripts and Package Exports
- Updated [`scripts/run_multiturn_injection.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_multiturn_injection.py) to save results using native `.save()` methods.
- Exported `ConvergenceScanResult`, `AcceptanceResult`, and `EnsembleStudyResult` in [`src/nkm_injection/__init__.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/__init__.py).

### 4. Expanded Test Suite
- **Location**: [`tests/test_convergence_study.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_convergence_study.py)
- **Tests Added**:
  - `test_convergence_scan_result_methods_and_df`: Verified statistical helpers, sequence iteration, dict access, DataFrame schema, and serialization round-trip.
  - `test_acceptance_result_methods_and_df`: Verified acceptance window computation, array properties, DataFrame schema, and JSON serialization.
  - `test_ensemble_study_result_methods_and_df`: Verified dict compatibility, CI extraction, DataFrame generation, and serialization.

---

## Verification & Status

- **Unit Test Suite**: 190/190 passing tests (+3 new tests added).
- **Protected Files Integrity**: Unchanged and verified against SHA-256 baseline.
