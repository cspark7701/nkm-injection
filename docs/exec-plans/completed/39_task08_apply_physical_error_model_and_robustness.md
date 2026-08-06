# Milestone 39 — Task 08: Apply Physical Error Model and Robustness Analysis

**Source task prompt**: `docs/03_nkm_repo_analysis_task_prompts/08_apply_physical_error_model_and_robustness.md`  
**Status**: COMPLETED  
**Date**: 2026-08-07

---

## Objective

Ensure every declared uncertainty source in the error budget is physically applied to the correct subsystem, affects expected observables, and contributes to multi-metric robustness analysis.

---

## Problem Addressed

- Removed duplicate booster extraction position jitter draws (`booster_x_jitter_m` and `booster_dx_m`) that caused triple counting of initial centroid jitter.
- Corrected quadrupole gradient perturbations to include beam rigidity scaling from energy error $\Delta p / p$, ensuring physical consistency between magnet field error and beam energy deviation.
- Structured output of `apply_sample_errors()` to explicitly return `centroid_offset`, `nkm_errors`, and `ring_errors` dictionaries so injection tracking and closed-orbit perturbations can consume them directly.
- Expanded robustness evaluation to track stored beam disturbance (`stored_beam_kick_mrad`), capture efficiency, failure mode classifications (`beta_exceeded`, `mismatch_exceeded`, `capture_failed`), and Monte Carlo sample size convergence.
- Expanded One-At-A-Time (OAT) sensitivity rankings to include all 5 physical error categories (optics, orbit/alignment, beam, NKM, storage ring).

---

## Files Changed

| File | Description |
| :--- | :--- |
| `src/nkm/errors.py` | Audited error sampling, eliminated duplicate fields, added `nkm_timing_mrad`, applied rigidity scaling to quadrupole strengths, and added structured error sub-dicts to `apply_sample_errors()`. |
| `src/nkm/robust_optimization.py` | Added stored beam kick calculation, capture efficiency evaluation support, failure mode counters, Monte Carlo sample size convergence metric, and `nominal_vs_robust_comparison()` function. |
| `scripts/run_publication_tolerances.py` | Updated script execution to include convergence checks, failure modes, and full 5-category OAT sensitivity rankings. |
| `tests/test_task08_error_model.py` | **New** — Comprehensive test suite covering sampling purity, rigidity scaling, structured outputs, failure modes, convergence checks, and common random number comparison. |

---

## Verification & Acceptance Criteria

1. **Error Model Audit**:
   - `sample_error_ensemble()` generates clean single-draw samples per uncertainty.
   - `apply_sample_errors()` correctly isolates optics, orbit, NKM, and ring error parameters.
2. **Observable Responses**:
   - Energy deviation affects beam rigidity and magnet strength scaling.
   - NKM field scale and alignment perturbations measurably alter kick dynamics and stored beam kick metrics.
3. **Robustness & Convergence**:
   - Statistical evaluations output percentiles (p50, p68, p95, p99), bootstrap confidence intervals, failure mode breakdown, and Monte Carlo convergence indicators.
4. **Test Suite**:
   - Passed all 18 unit & integration tests (`tests/test_task08_error_model.py`, `tests/test_error_model.py`, `tests/test_optimization.py`).
5. **Protected Files**:
   - All protected source files (`NKM_radia.ipynb`, `storage_ring.ipynb`, spreadsheets, etc.) remained untouched.
