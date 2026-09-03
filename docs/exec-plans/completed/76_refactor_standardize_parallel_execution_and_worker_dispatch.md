# Milestone 76 — Task 12: Standardize Parallel Execution and Worker Dispatch Utility

## Executive Summary

Task 12 establishes a unified, robust, OpenMP/C-safe multiprocessing and worker dispatch architecture across the `nkm_injection` package and analysis scripts. A dedicated concurrency utility module (`src/nkm_injection/concurrency.py`) was created, providing `parallel_map` with automatic `forkserver`/`spawn` process context resolution, deterministic independent worker seed generation (`generate_worker_seeds`), CPU worker count resolution (`resolve_workers`), and graceful sequential fallback. Standard CLI argument parsing (`-w, --workers`) was aligned across all production and analysis scripts.

---

## Key Achievements

### 1. Created Dedicated Concurrency Utility Module
- **Location**: [`src/nkm_injection/concurrency.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/concurrency.py)
- **Features**:
  - `parallel_map(func, items, n_workers=1, chunksize=1, desc=None)`: Dispatches items across worker processes using `ProcessPoolExecutor` with safe multiprocessing context (`forkserver` or `spawn`) to prevent OpenMP/pyAT fork deadlocks. Preserves input sequence ordering in results. Executes synchronously in main process when `n_workers <= 1` or `len(items) <= 1`.
  - `resolve_workers(workers)`: Normalizes user-supplied worker counts to positive integers, defaulting to `max(1, os.cpu_count() - 1)` when unspecified or non-positive.
  - `generate_worker_seeds(base_seed, n_items)`: Generates deterministic, distinct pseudo-random seeds per worker sample to avoid RNG seed collisions across child processes.
  - Contextual exception wrapping: Cleanly wraps worker-level exceptions with item index and task description.

### 2. Integrated Parallel Dispatch Across Core Modules
- **Robust Optimization & Statistical Tolerance Scans**:
  - Refactored `evaluate_robustness_statistics` and `compute_one_at_a_time_sensitivity` in [`src/nkm_injection/robust_optimization.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/robust_optimization.py) to accept `n_workers: Optional[int] = 1` and dispatch sample evaluations via `parallel_map`.
  - Updated legacy wrappers in [`src/nkm_injection/errors.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/errors.py) (`evaluate_monte_carlo_robustness`, `compute_error_sensitivity_ranking`) to propagate worker count.
- **Multi-Turn Injection Convergence & Ensemble Studies**:
  - Refactored `run_ensemble_study` in [`src/nkm_injection/convergence_study.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/convergence_study.py) to accept `n_workers: Optional[int] = 1` and parallelize tracking across independent seed realizations.
- **Paper Reproduction Pipeline**:
  - Updated `run_paper_pipeline` in [`src/nkm_injection/paper.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/paper.py) to support `workers: Optional[int] = None`.

### 3. Standardized CLI Arguments Across Analysis & Production Scripts
- Aligned `-w, --workers` across:
  - [`scripts/run_tolerance_study.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_tolerance_study.py)
  - [`scripts/run_publication_tolerances.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_publication_tolerances.py)
  - [`scripts/run_multiturn_injection.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_multiturn_injection.py)
  - [`scripts/reproduce_paper.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/reproduce_paper.py)
  - [`scripts/run_bts_moga.py`](file:///home/cspark/Work/projects/nkm-injection/scripts/run_bts_moga.py)

### 4. Expanded Test Suite
- **Location**: [`tests/test_optimization.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_optimization.py)
- **Tests Added**:
  - `test_resolve_workers`: Verified default and explicit CPU core allocation limits.
  - `test_generate_worker_seeds`: Verified deterministic generation and strict uniqueness of per-worker random seeds.
  - `test_parallel_map_sequential_and_parallel`: Verified that `parallel_map` produces identical, ordered results with $N=1$ and $N=2$ workers, and handles edge cases (empty list, single item).
  - `test_parallel_map_exception_propagation`: Verified clean exception trapping and context reporting.
  - `test_evaluate_robustness_statistics_parallel_consistency`: Verified exact numerical agreement of Monte Carlo statistics between sequential and 2-worker parallel execution.
  - `test_compute_oat_sensitivity_parallel_consistency`: Verified exact numerical agreement and category ordering for OAT sensitivity scans between sequential and parallel execution.

---

## Verification & Status

- **Unit Test Suite**: 187/187 tests passing.
- **Protected Files Integrity**: Verified unchanged against SHA-256 baseline.
- **Package Exports**: Exported `parallel_map`, `resolve_workers`, and `generate_worker_seeds` in [`src/nkm_injection/__init__.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/__init__.py).
