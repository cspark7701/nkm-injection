"""
Unit and Integration Tests for Milestone 4 BTS Deterministic Optimization
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.optimization import (
    BTSOptimizationConfig,
    BTSOptimizationEvaluator,
    DeterministicObjective,
    OpticsOptimizer,
    optimize_bts_quadrupoles,
    compute_sensitivity_matrix
)
from src.nkm_injection.robust_optimization import RobustMonteCarloObjective


@pytest.fixture
def opt_config():
    return BTSOptimizationConfig(random_seed=42)


@pytest.fixture
def evaluator(opt_config):
    return BTSOptimizationEvaluator(opt_config)


def test_optimization_evaluator_baseline(evaluator):
    """Test evaluator output on nominal baseline quadrupole strengths."""
    initial_k = evaluator.nominal_strengths
    res = evaluator.evaluate(initial_k)
    
    # Baseline lattice exceeds beta_max limit (beta_y_max = 242.6m > 60m), so feasible is False
    assert res["feasible"] is False
    assert res["merit"] > 1e5  # High baseline merit due to mismatch
    assert pytest.approx(res["mismatch_x"], abs=1e-2) == 8.67
    assert pytest.approx(res["mismatch_y"], abs=1e-2) == 28.61


def test_bts_optimization_slsqp(opt_config):
    """Test SLSQP optimization run and check merit reduction and constraint compliance."""
    res = optimize_bts_quadrupoles(method="SLSQP", config=opt_config, n_starts=1)
    
    assert res.success is True
    assert res.final_merit < res.initial_merit
    assert res.final_max_beta_x <= 60.0
    assert res.final_max_beta_y <= 60.0
    assert np.all(res.optimized_strengths >= -5.0)
    assert np.all(res.optimized_strengths <= 5.0)


def test_sensitivity_matrix(evaluator):
    """Test sensitivity matrix calculation and shape."""
    initial_k = evaluator.nominal_strengths
    sens = compute_sensitivity_matrix(initial_k)
    
    assert sens["jacobian_matrix"].shape == (6, 9)
    assert len(sens["observable_names"]) == 6
    assert len(sens["quad_names"]) == 9
    assert np.any(np.abs(sens["jacobian_matrix"]) > 1e-3)


def test_optimization_reproducibility(opt_config):
    """Verify that optimization with fixed seed is reproducible."""
    res1 = optimize_bts_quadrupoles(method="SLSQP", config=opt_config, n_starts=1)
    res2 = optimize_bts_quadrupoles(method="SLSQP", config=opt_config, n_starts=1)
    
    assert np.allclose(res1.optimized_strengths, res2.optimized_strengths, atol=1e-6)
    assert pytest.approx(res1.final_merit, abs=1e-6) == res2.final_merit


def test_optics_optimizer_strategy_pattern(opt_config):
    """Verify OpticsOptimizer execution with DeterministicObjective and RobustMonteCarloObjective."""
    det_obj = DeterministicObjective(opt_config)
    optimizer_det = OpticsOptimizer(objective=det_obj, config=opt_config)
    res_det = optimizer_det.optimize(method="SLSQP", n_starts=1)

    assert res_det.success is True
    assert res_det.final_merit < res_det.initial_merit

    # Verify RobustMonteCarloObjective strategy instantiation & evaluation
    robust_obj = RobustMonteCarloObjective(opt_config, n_samples=5, seed=42)
    robust_eval = robust_obj.evaluate(res_det.optimized_strengths)
    assert "robust_stats" in robust_eval
    assert "mismatch_x" in robust_eval


# ===========================================================================
# Task 12 — Concurrency & Worker Dispatch Tests
# ===========================================================================

from src.nkm_injection.concurrency import (
    parallel_map,
    resolve_workers,
    generate_worker_seeds,
    _sample_square,
    _failing_worker
)
from src.nkm_injection.bts_lattice import BTSConfig
from src.nkm_injection.errors import sample_error_ensemble
from src.nkm_injection.robust_optimization import (
    evaluate_robustness_statistics,
    compute_one_at_a_time_sensitivity,
)


def test_resolve_workers():
    """Verify worker resolution defaults and positive integers."""
    assert resolve_workers(1) == 1
    assert resolve_workers(4) == 4
    assert resolve_workers(None) >= 1
    assert resolve_workers(0) >= 1
    assert resolve_workers(-5) >= 1


def test_generate_worker_seeds():
    """Verify deterministic distinct seed generation."""
    seeds = generate_worker_seeds(42, 10)
    assert len(seeds) == 10
    assert len(set(seeds)) == 10  # All unique
    # Determinism
    seeds_again = generate_worker_seeds(42, 10)
    assert seeds == seeds_again


def test_parallel_map_sequential_and_parallel():
    """Verify parallel_map produces identical, ordered results with 1 vs 2 workers."""
    items = list(range(12))
    res_seq = parallel_map(_sample_square, items, n_workers=1)
    res_par = parallel_map(_sample_square, items, n_workers=2)

    assert res_seq == [x * x for x in items]
    assert res_par == res_seq

    # Edge cases: empty list, single item
    assert parallel_map(_sample_square, [], n_workers=2) == []
    assert parallel_map(_sample_square, [5], n_workers=2) == [25]


def test_parallel_map_exception_propagation():
    """Verify clean exception propagation from worker processes."""
    items = [1, 2, -3, 4]
    with pytest.raises(RuntimeError, match=r"failed"):
        parallel_map(_failing_worker, items, n_workers=2)


def test_evaluate_robustness_statistics_parallel_consistency():
    """Verify evaluate_robustness_statistics gives identical results in parallel (n_workers=2) vs sequential."""
    bts_cfg = BTSConfig()
    target_twiss = {"beta": [2.336495, 4.256241], "alpha": [-0.016335, 0.017772]}
    samples = sample_error_ensemble(n_samples=5, seed=42)

    stats_seq = evaluate_robustness_statistics(bts_cfg, target_twiss, samples, n_workers=1)
    stats_par = evaluate_robustness_statistics(bts_cfg, target_twiss, samples, n_workers=2)

    assert pytest.approx(stats_seq["mismatch_x"]["p50"]) == stats_par["mismatch_x"]["p50"]
    assert pytest.approx(stats_seq["mismatch_y"]["p50"]) == stats_par["mismatch_y"]["p50"]
    assert stats_seq["feasible_fraction"] == stats_par["feasible_fraction"]


def test_compute_oat_sensitivity_parallel_consistency():
    """Verify compute_one_at_a_time_sensitivity gives identical results in parallel vs sequential."""
    bts_cfg = BTSConfig()
    target_twiss = {"beta": [2.336495, 4.256241], "alpha": [-0.016335, 0.017772]}

    rankings_seq = compute_one_at_a_time_sensitivity(bts_cfg, target_twiss, n_samples=3, seed=42, n_workers=1)
    rankings_par = compute_one_at_a_time_sensitivity(bts_cfg, target_twiss, n_samples=3, seed=42, n_workers=2)

    assert list(rankings_seq.keys()) == list(rankings_par.keys())
    for k in rankings_seq:
        assert pytest.approx(rankings_seq[k], abs=1e-9) == rankings_par[k]



