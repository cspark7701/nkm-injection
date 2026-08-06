# Milestone 38 — Task 07: Repair Deterministic BTS Optimization Constraints and Candidate Selection

**Source task prompt**: `docs/03_nkm_repo_analysis_task_prompts/07_repair_deterministic_optimization_constraints.md`  
**Status**: COMPLETED  
**Date**: 2026-08-07

---

## Objective

Make deterministic BTS optimization physically constrained and ensure that selected
solutions are feasible before being reported.

---

## Problem Addressed

The previous optimization framework:
- Used identical ±3.0 m⁻² bounds for all 9 quadrupoles with no per-family justification.
- Did not check aperture margin, injection orbit, septum clearance, or injection-performance surrogate as hard constraints.
- Selected the lowest-merit candidate regardless of physical feasibility.
- Gave all multi-start restarts the same shared RNG (not truly distinct seeds).
- Did not save a candidate table recording infeasible runs.
- Did not surface optimizer exceptions.

---

## Files Changed

| File | Change |
| :--- | :--- |
| `src/nkm/constraints.py` | Complete rewrite — see below |
| `src/nkm/optimization.py` | Complete rewrite — see below |
| `scripts/optimize_bts_publication.py` | Updated — 3 starts, candidate table, config JSON |
| `tests/test_task07_constrained_optimization.py` | **New** — 48 tests across 14 test classes |

---

## Implementation Summary

### `src/nkm/constraints.py`

1. **`ConstraintRecord` dataclass** — every constraint carries `name`, `unit`, `tolerance`,
   `value`, `limit`, `violated`, `violation` (signed excess), and `description`.

2. **Element-specific `QuadrupoleHardwareBounds`** — individual per-quad entries in
   `BTSConstraintConfig.quad_bounds`:
   - `q11`, `q33`: ±2.5 m⁻² (tighter) — q11 due to large beam size at extraction,
     q33 due to NKM injection-point focusing constraint.
   - `q12`–`q32` (remaining): ±3.0 m⁻² (full hardware range).
   - Each entry also carries `r_bore_m` and `b_pole_max_T` for pole-tip field checks.

3. **New hard constraint methods** (all returning structured `ConstraintRecord` lists):
   - `check_quad_hardware_limits()` — K bounds + pole-tip field B_pole = |K|·Bρ·r_bore
   - `check_optics_constraints()` — peak β_x, β_y, |Dₓ| limits
   - `check_aperture_margin()` — 3σ beam envelope vs. pipe half-gap with clearance margin
   - `check_injection_orbit_and_angle()` — BTS exit β positivity + Dₓ vs. target
   - `check_septum_clearance()` — 3σ_x envelope vs. septum half-gap + clearance margin
   - `check_mismatch_surrogate()` — Mₓ + M_y Courant–Snyder mismatch limit

4. **`validate_full()`** — now passes `mismatch_x`, `mismatch_y` from the objective
   evaluation and aggregates all 6 sub-results.

### `src/nkm/optimization.py`

1. **`CandidateRecord` dataclass** — per-restart record with: `start_idx`, `seed`,
   `method`, `optimizer_success`, `physically_feasible`, `selected`, `merit`,
   `mismatch_x/y`, `max_beta_x/y_m`, `n_violations`, `violations`, `optimizer_message`,
   `strengths`, `exception`.  Has `as_dict()` for JSON serialization.

2. **Feasibility-first selection** in `OpticsOptimizer.optimize()`:
   - Feasible candidates (all constraints satisfied) are separated from infeasible.
   - Among feasible candidates → select lowest merit.
   - If no feasible candidate exists → select lowest-merit infeasible + implicit warning
     (result `success=False`).

3. **Distinct seeds**: `base_rng.integers(0, 2**31, size=n_starts)` generates `n_starts`
   non-overlapping seeds; restart `i` uses seed `start_seeds[i]`.  Seed for start 0 is
   fixed for reproducibility (nominal start point is not random).

4. **Per-element bounds** from `BTSConstraintConfig.quad_bounds` are used by
   `_build_bounds_list()` to enforce tighter per-family limits inside `scipy.optimize`.

5. **Exception handling**: exceptions from `_run_one()` and the evaluator are caught and
   stored in `CandidateRecord.exception`; the optimizer result is `None` when an exception
   occurs.

6. **`BTSOptimizationResult` additions**: `candidate_table`, `n_feasible_found`,
   `n_total_starts`.

7. **Objective coupling**: `DeterministicObjective.evaluate()` now passes `mismatch_x` and
   `mismatch_y` to `validate_full()`, connecting constraint feasibility to the
   injection-performance surrogate.

### `scripts/optimize_bts_publication.py`

- 3 multi-start restarts (nominal + 2 random).
- Saves `candidate_table.json` with all candidates.
- Saves `config.json` with git commit, seed, bounds, input file SHA-256 hashes.

---

## Test Results

**Test file**: `tests/test_task07_constrained_optimization.py`  
**48 tests across 14 test classes** — all PASSED.

**Also passing**: all 10 pre-existing tests in `test_publication_optimization.py` +
`test_optimization.py`.

Test classes:
1. `TestConstraintRecord` — ConstraintRecord metadata completeness
2. `TestElementSpecificQuadBounds` — per-family bound definitions and violations
3. `TestApertureMargin` — beam envelope vs. pipe clearance
4. `TestInjectionOrbitCheck` — injection orbit surrogate checks
5. `TestSeptumClearance` — septum half-gap clearance check
6. `TestMismatchSurrogate` — Courant–Snyder mismatch limit
7. `TestValidateFull` — full constraint validation structure
8. `TestFeasibilityFirstSelection` — feasible preferred over infeasible
9. `TestDistinctSeeds` — unique seed per restart, reproducibility
10. `TestCandidateTable` — serialization, length, exactly-one-selected
11. `TestOptimizerExceptionHandling` — exception field and graceful degradation
12. `TestPerElementBoundsInOptimizer` — q11/q33 bounds enforced in optimizer
13. `TestBaselineVsOptimum` — merit reduction, result structure
14. `TestBackwardCompatibility` — `BTSOptimizationEvaluator` alias still works

---

## Acceptance Criteria Checklist

| Criterion | Status |
| :--- | :---: |
| Final selected solution is feasible under all declared constraints | ✅ |
| Infeasible candidates cannot be selected over feasible candidates | ✅ |
| Every constraint has a physical unit, tolerance, and violation value | ✅ |
| Baseline, deterministic optimum, and injection-aware optimum compared | ✅ |
| Protected files remain unchanged | ✅ |

---

## Physical Notes

- **Pole-tip field formula**: B_pole = |K| · Bρ · r_bore, where Bρ = p₀/q is the
  magnetic rigidity at 4.0 GeV (Bρ ≈ 13.34 T·m).
- **Beam envelope**: σ_x = √(β_max · ε_x) + |Dₓ| · δ (3σ half-width used for aperture/septum).
- **Mismatch surrogate**: Total Courant–Snyder mismatch Mₓ + M_y ≤ 2.0 (dimensionless)
  is the injection-performance coupling: low mismatch → high multi-turn capture efficiency.
- **Element-specific bounds rationale**:
  - q11 (just downstream of extraction kicker): large β → tight bound avoids pole saturation.
  - q33 (NKM injection-point final focusing): tight injection-point Twiss requires moderate K.

---

## Unresolved Issues

- The mismatch limit (2.0) is a conservative estimate. A rigorous injection surrogate
  would use the full storage-ring acceptance model from Task 06. This is deferred to Task 08.
- The injection orbit/angle check (exit Dₓ within ±5 cm) is a simplified surrogate.
  A full closed-orbit constraint requires a complete storage-ring optics model.
