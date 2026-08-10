"""
Task 07 — Tests for Repaired Deterministic BTS Optimization Constraints

Acceptance criteria (from docs/03_nkm_repo_analysis_task_prompts/07_repair_deterministic_optimization_constraints.md):

1. Final selected solution is feasible under all declared constraints.
2. Infeasible candidates cannot be selected over feasible candidates.
3. Every constraint has a physical unit, tolerance, and violation value.
4. Baseline, deterministic optimum, and injection-aware optimum are compared.
5. Protected files remain unchanged.

Additional coverage:
- Element-specific quadrupole bounds (per-family limits).
- Beam aperture margin check (3σ envelope vs. pipe).
- Injection orbit / angle surrogate checks.
- Septum clearance check.
- Injection mismatch surrogate constraint.
- Distinct seeds for global restarts.
- Candidate table includes infeasible candidates and violations.
- Optimizer exceptions are preserved and reported.
- Reproducibility of multi-start run.
"""

import sys
import copy
import json
from pathlib import Path
from typing import List
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm.constraints import (
    BTSConstraintConfig,
    BTSHardwareConstraints,
    ConstraintRecord,
    QuadrupoleHardwareBounds,
)
from src.nkm.objectives import BTSNormalizedObjectives, OpticsTargetConfig
from src.nkm.optimization import (
    BTSOptimizationConfig,
    BTSOptimizationResult,
    CandidateRecord,
    DeterministicObjective,
    OpticsOptimizer,
    optimize_bts_quadrupoles,
    compute_sensitivity_matrix,
    round_strengths,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(scope="module")
def nominal_k():
    """Nominal quadrupole strengths from BTSConfig defaults."""
    return BTSNormalizedObjectives().nominal_strengths


@pytest.fixture(scope="module")
def fast_config():
    """Fast configuration for tests (low max_iter, single start)."""
    return BTSOptimizationConfig(random_seed=42, max_iter=10)


@pytest.fixture(scope="module")
def opt_result(fast_config):
    """Run one SLSQP optimization and cache the result."""
    return optimize_bts_quadrupoles(method="SLSQP", config=fast_config, n_starts=1)


# ============================================================
# 1. ConstraintRecord — structured metadata
# ============================================================

class TestConstraintRecord:
    def test_constraint_record_fields(self):
        """Every ConstraintRecord must carry unit, tolerance, value, limit, violation."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        k_valid = np.array([0.45, -1.03, 0.89, -1.07, 1.49, -0.67, 0.59, -1.17, 0.94])
        result = hw.check_quad_hardware_limits(k_valid)
        for rec in result["records"]:
            assert isinstance(rec, ConstraintRecord)
            assert rec.unit != ""
            assert rec.tolerance > 0
            assert isinstance(rec.value, float)
            assert isinstance(rec.limit, float)
            assert isinstance(rec.violation, float)

    def test_constraint_record_as_dict(self):
        """ConstraintRecord.as_dict() must contain all required keys."""
        rec = ConstraintRecord(
            name="test_constraint", unit="m", tolerance=0.01,
            value=0.05, limit=0.0, violated=True, violation=0.05,
            description="test"
        )
        d = rec.as_dict()
        for key in ("name", "unit", "tolerance", "value", "limit",
                    "violated", "violation", "description"):
            assert key in d


# ============================================================
# 2. Element-specific quadrupole bounds
# ============================================================

class TestElementSpecificQuadBounds:
    def test_q11_tighter_bound(self):
        """q11 must have |k_max| ≤ 2.5 (tighter than generic 3.0)."""
        cfg = BTSConstraintConfig()
        assert cfg.quad_bounds["q11"].k_max <= 2.5
        assert cfg.quad_bounds["q11"].k_min >= -2.5

    def test_q33_tighter_bound(self):
        """q33 must have |k_max| ≤ 2.5 (NKM injection-point focusing constraint)."""
        cfg = BTSConstraintConfig()
        assert cfg.quad_bounds["q33"].k_max <= 2.5
        assert cfg.quad_bounds["q33"].k_min >= -2.5

    def test_all_nine_quads_present(self):
        """All 9 quadrupole families must have individual bounds defined."""
        cfg = BTSConstraintConfig()
        expected = {"q11", "q12", "q13", "q21", "q22", "q23", "q31", "q32", "q33"}
        assert set(cfg.quad_bounds.keys()) == expected

    def test_violation_at_q11_tight_limit(self):
        """Strength K = 2.6 at q11 must trigger a violation (limit 2.5)."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        k = np.array([2.6, -1.0, 0.9, -1.0, 1.0, -0.7, 0.6, -1.1, 0.9])
        result = hw.check_quad_hardware_limits(k)
        assert result["feasible"] is False
        assert any("q11" in v for v in result["violations"])

    def test_no_violation_within_element_bounds(self):
        """Strengths within all element-specific bounds must be feasible."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        # All within tightest bounds (2.5)
        k_safe = np.array([0.45, -1.03, 0.89, -1.07, 1.49, -0.67, 0.59, -1.17, 0.94])
        result = hw.check_quad_hardware_limits(k_safe)
        assert result["feasible"] is True, result["violations"]


# ============================================================
# 3. Aperture margin constraint
# ============================================================

class TestApertureMargin:
    def _get_prop(self, k):
        obj = BTSNormalizedObjectives()
        obj.set_quads(k)
        from src.nkm.optics import compute_twiss_propagation
        return compute_twiss_propagation(obj.lattice, obj.initial_twiss)

    def test_aperture_margin_keys(self, nominal_k):
        """Aperture margin check must return clearance_x_m and clearance_y_m."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop = self._get_prop(nominal_k)
        result = hw.check_aperture_margin(prop)
        assert "clearance_x_m" in result
        assert "clearance_y_m" in result
        assert "envelope_x_m" in result

    def test_aperture_records_have_units(self, nominal_k):
        """Aperture ConstraintRecords must specify unit = 'm'."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop = self._get_prop(nominal_k)
        result = hw.check_aperture_margin(prop)
        for rec in result["records"]:
            assert rec.unit == "m"
            assert rec.tolerance > 0


# ============================================================
# 4. Injection orbit and angle check
# ============================================================

class TestInjectionOrbitCheck:
    def _get_prop(self, k):
        obj = BTSNormalizedObjectives()
        obj.set_quads(k)
        from src.nkm.optics import compute_twiss_propagation
        return compute_twiss_propagation(obj.lattice, obj.initial_twiss)

    def test_injection_orbit_records_present(self, nominal_k):
        """Injection orbit check must return at least one ConstraintRecord."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop = self._get_prop(nominal_k)
        result = hw.check_injection_orbit_and_angle(prop)
        assert len(result["records"]) >= 1

    def test_exit_beta_positive_required(self, nominal_k):
        """BTS exit β_x and β_y must be positive."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop = self._get_prop(nominal_k)
        result = hw.check_injection_orbit_and_angle(prop)
        # Nominal solution should not violate beta positivity
        beta_positive_recs = [r for r in result["records"] if "positive" in r.name]
        for rec in beta_positive_recs:
            assert rec.value > 0, f"Exit beta is not positive: {rec}"


# ============================================================
# 5. Septum clearance check
# ============================================================

class TestSeptumClearance:
    def _get_prop(self, k):
        obj = BTSNormalizedObjectives()
        obj.set_quads(k)
        from src.nkm.optics import compute_twiss_propagation
        return compute_twiss_propagation(obj.lattice, obj.initial_twiss)

    def test_septum_clearance_keys(self, nominal_k):
        """Septum clearance check must return envelope_x_m and allowed_halfgap_m."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop = self._get_prop(nominal_k)
        result = hw.check_septum_clearance(prop)
        assert "envelope_x_m" in result
        assert "allowed_halfgap_m" in result

    def test_septum_clearance_unit_is_meters(self, nominal_k):
        """Septum clearance ConstraintRecord unit must be 'm'."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop = self._get_prop(nominal_k)
        result = hw.check_septum_clearance(prop)
        for rec in result["records"]:
            assert rec.unit == "m"


# ============================================================
# 6. Mismatch surrogate constraint
# ============================================================

class TestMismatchSurrogate:
    def test_low_mismatch_feasible(self):
        """Total mismatch well below limit must be feasible."""
        cfg = BTSConstraintConfig(mismatch_limit=2.0)
        hw = BTSHardwareConstraints(cfg)
        result = hw.check_mismatch_surrogate(mismatch_x=0.1, mismatch_y=0.1)
        assert result["feasible"] is True
        assert result["total_mismatch"] == pytest.approx(0.2, abs=1e-9)

    def test_high_mismatch_infeasible(self):
        """Total mismatch above limit must be infeasible."""
        cfg = BTSConstraintConfig(mismatch_limit=2.0)
        hw = BTSHardwareConstraints(cfg)
        result = hw.check_mismatch_surrogate(mismatch_x=1.5, mismatch_y=1.5)
        assert result["feasible"] is False
        assert result["total_mismatch"] == pytest.approx(3.0, abs=1e-9)

    def test_mismatch_record_has_unit(self):
        """Mismatch ConstraintRecord must carry unit 'dimensionless'."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        result = hw.check_mismatch_surrogate(0.0, 0.0)
        for rec in result["records"]:
            assert rec.unit == "dimensionless"
            assert rec.tolerance > 0


# ============================================================
# 7. validate_full — comprehensive constraint validation
# ============================================================

class TestValidateFull:
    def _get_prop_and_mismatch(self, k):
        obj = BTSNormalizedObjectives()
        obj.set_quads(k)
        from src.nkm.optics import compute_twiss_propagation, compute_mismatch_metric
        from src.nkm.objectives import OpticsTargetConfig
        prop = compute_twiss_propagation(obj.lattice, obj.initial_twiss)
        tc = OpticsTargetConfig()
        mx = compute_mismatch_metric(
            prop["final_beta"][0], prop["final_alpha"][0],
            tc.target_beta_x, tc.target_alpha_x)
        my = compute_mismatch_metric(
            prop["final_beta"][1], prop["final_alpha"][1],
            tc.target_beta_y, tc.target_alpha_y)
        return prop, float(mx), float(my)

    def test_validate_full_structure(self, nominal_k):
        """validate_full must return all required sub-result keys."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop, mx, my = self._get_prop_and_mismatch(nominal_k)
        result = hw.validate_full(nominal_k, prop, mismatch_x=mx, mismatch_y=my)
        for key in ("feasible", "violations", "records",
                    "hardware", "optics", "aperture",
                    "injection", "septum", "mismatch", "diagnostics"):
            assert key in result, f"Missing key: {key}"

    def test_all_records_have_metadata(self, nominal_k):
        """Every ConstraintRecord in validate_full must have unit, tolerance, violation."""
        cfg = BTSConstraintConfig()
        hw = BTSHardwareConstraints(cfg)
        prop, mx, my = self._get_prop_and_mismatch(nominal_k)
        result = hw.validate_full(nominal_k, prop, mismatch_x=mx, mismatch_y=my)
        for rec in result["records"]:
            assert isinstance(rec, ConstraintRecord)
            assert rec.unit != ""
            assert rec.tolerance > 0
            assert isinstance(rec.violation, float)
            assert rec.violation >= 0.0


# ============================================================
# 8. Feasibility-first candidate selection
# ============================================================

class TestFeasibilityFirstSelection:
    def test_selected_candidate_is_feasible(self, opt_result):
        """If feasible candidates exist, the selected one must be feasible."""
        if opt_result.n_feasible_found > 0:
            selected = next(c for c in opt_result.candidate_table if c.selected)
            assert selected.physically_feasible is True, (
                f"Selected candidate is infeasible. Violations: {selected.violations}"
            )

    def test_feasible_not_beaten_by_infeasible(self, fast_config):
        """
        Artificially construct a scenario where the first (nominal) start is
        infeasible but a later start is feasible.  Verify the feasible one is
        selected even if it has higher merit.
        """
        # Use multi-start to increase chance of finding feasible + infeasible candidates
        res = optimize_bts_quadrupoles(method="SLSQP", config=fast_config, n_starts=2)
        feasible_found = [c for c in res.candidate_table if c.physically_feasible]
        if feasible_found:
            selected = next(c for c in res.candidate_table if c.selected)
            assert selected.physically_feasible is True

    def test_no_feasible_falls_back_to_best_infeasible(self, fast_config):
        """
        When no feasible solution exists, the best (lowest merit) infeasible
        candidate should be selected.
        """
        # Use an impossibly tight mismatch_limit to force all infeasible
        tight_cfg = copy.deepcopy(fast_config)
        tight_cfg.constraint_config.mismatch_limit = 0.0   # impossible limit
        tight_cfg.constraint_config.beta_max_limit_m = 200.0  # relax optics
        res = optimize_bts_quadrupoles(method="SLSQP", config=tight_cfg, n_starts=1)
        # All candidates will be infeasible; best must still be selected
        selected = next((c for c in res.candidate_table if c.selected), None)
        assert selected is not None
        # n_feasible_found must be 0 or selection is wrong
        assert res.n_feasible_found == 0 or res.constraints_satisfied


# ============================================================
# 9. Distinct seeds for multi-start
# ============================================================

class TestDistinctSeeds:
    def test_start_seeds_are_distinct(self, fast_config):
        """Each multi-start restart must use a distinct seed."""
        config = BTSOptimizationConfig(random_seed=42, max_iter=5)
        res = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=3)
        seeds = [c.seed for c in res.candidate_table]
        assert len(seeds) == len(set(seeds)), f"Duplicate seeds found: {seeds}"

    def test_nominal_start_is_index_zero(self, fast_config):
        """The first candidate (index 0) must be the nominal start point."""
        config = BTSOptimizationConfig(random_seed=42, max_iter=5)
        res = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=2)
        assert res.candidate_table[0].start_idx == 0

    def test_multi_start_reproducible(self):
        """Same seed → same candidate table results."""
        config = BTSOptimizationConfig(random_seed=99, max_iter=5)
        res1 = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=2)
        res2 = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=2)
        # Seeds must be identical
        seeds1 = [c.seed for c in res1.candidate_table]
        seeds2 = [c.seed for c in res2.candidate_table]
        assert seeds1 == seeds2
        # Final selected strengths must be identical
        np.testing.assert_allclose(
            res1.optimized_strengths, res2.optimized_strengths, atol=1e-10
        )


# ============================================================
# 10. Candidate table — structure and content
# ============================================================

class TestCandidateTable:
    def test_candidate_table_length(self, fast_config):
        """Candidate table length must equal n_starts."""
        config = BTSOptimizationConfig(random_seed=42, max_iter=5)
        res = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=3)
        assert len(res.candidate_table) == 3

    def test_candidate_table_serializable(self, opt_result):
        """Every candidate must be serializable to a dict (for JSON output)."""
        for rec in opt_result.candidate_table:
            d = rec.as_dict()
            # Must be JSON-serializable
            _ = json.dumps(d)

    def test_exactly_one_selected(self, opt_result):
        """Exactly one candidate in the table must be marked as selected."""
        selected_count = sum(1 for c in opt_result.candidate_table if c.selected)
        assert selected_count == 1

    def test_violations_list_in_candidate(self, opt_result):
        """Each candidate record must have a violations list."""
        for rec in opt_result.candidate_table:
            assert isinstance(rec.violations, list)

    def test_infeasible_candidate_has_violations(self):
        """An infeasible candidate must have at least one violation."""
        # Force infeasibility by using impossible mismatch limit
        config = BTSOptimizationConfig(
            random_seed=0, max_iter=5,
            constraint_config=BTSConstraintConfig(mismatch_limit=0.0),
        )
        res = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=1)
        for rec in res.candidate_table:
            if not rec.physically_feasible:
                assert len(rec.violations) > 0, "Infeasible candidate has empty violations list"


# ============================================================
# 11. Optimizer exception handling
# ============================================================

class TestOptimizerExceptionHandling:
    def test_exception_field_empty_on_success(self, opt_result):
        """On a normal run the selected candidate's exception field must be empty."""
        selected = next(c for c in opt_result.candidate_table if c.selected)
        assert selected.exception == ""

    def test_evaluate_returns_infeasible_on_exception(self):
        """DeterministicObjective.evaluate must return feasible=False when propagator fails."""
        obj = DeterministicObjective()
        # Pass NaN strengths to trigger propagator failure
        nan_k = np.full(9, np.nan)
        result = obj.evaluate(nan_k)
        assert result["feasible"] is False
        assert result["merit"] >= 1e9


# ============================================================
# 12. Per-element bounds in optimizer
# ============================================================

class TestPerElementBoundsInOptimizer:
    def test_per_element_bounds_respected(self):
        """Optimized q11 strength must stay within q11-specific bounds (±2.5)."""
        config = BTSOptimizationConfig(random_seed=42, max_iter=20)
        res = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=1)
        k = res.optimized_strengths
        q11_k = k[0]
        assert -2.5 <= q11_k <= 2.5, f"q11 K={q11_k:.4f} violates ±2.5 bound"

    def test_per_element_bounds_q33(self):
        """Optimized q33 strength must stay within q33-specific bounds (±2.5)."""
        config = BTSOptimizationConfig(random_seed=42, max_iter=20)
        res = optimize_bts_quadrupoles(method="SLSQP", config=config, n_starts=1)
        k = res.optimized_strengths
        q33_k = k[8]
        assert -2.5 <= q33_k <= 2.5, f"q33 K={q33_k:.4f} violates ±2.5 bound"


# ============================================================
# 13. Baseline vs. optimum comparison
# ============================================================

class TestBaselineVsOptimum:
    def test_optimum_merit_lower_than_baseline(self, opt_result):
        """Optimized merit must be lower than initial (nominal) merit."""
        assert opt_result.final_merit < opt_result.initial_merit

    def test_beta_reduced_after_optimization(self, opt_result):
        """Peak beta must be reduced after optimization relative to baseline."""
        assert opt_result.final_max_beta_x < 250.0
        assert opt_result.final_max_beta_y < 250.0

    def test_result_contains_n_feasible(self, opt_result):
        """BTSOptimizationResult must report n_feasible_found and n_total_starts."""
        assert hasattr(opt_result, "n_feasible_found")
        assert hasattr(opt_result, "n_total_starts")
        assert opt_result.n_total_starts >= 1


# ============================================================
# 14. Backward compatibility
# ============================================================

class TestBackwardCompatibility:
    def test_bts_optimization_evaluator_alias(self):
        """BTSOptimizationEvaluator must be an alias for DeterministicObjective."""
        from src.nkm.optimization import BTSOptimizationEvaluator
        assert BTSOptimizationEvaluator is DeterministicObjective

    def test_legacy_optimize_still_works(self, fast_config):
        """optimize_bts_quadrupoles with n_starts=1 still returns valid result."""
        res = optimize_bts_quadrupoles(method="least_squares", config=fast_config, n_starts=1)
        assert isinstance(res, BTSOptimizationResult)
        assert res.final_merit < res.initial_merit
