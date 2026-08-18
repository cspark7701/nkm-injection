"""
Unit, Integration, and Physics-Level Tests for BTS & NKM Error Modeling and Robustness

Consolidates basic error configuration tests and Task 08 physical error model validation.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm.bts_lattice import BTSConfig
from src.nkm.errors import (
    ErrorBudgetConfig,
    sample_error_ensemble,
    apply_sample_errors,
    evaluate_monte_carlo_robustness,
    compute_error_sensitivity_ranking
)
from src.nkm.robust_optimization import (
    evaluate_robustness_statistics,
    compute_one_at_a_time_sensitivity,
    nominal_vs_robust_comparison
)


@pytest.fixture
def nominal_bts_config():
    return BTSConfig(
        k_q11=0.47419899, k_q12=-1.70822248, k_q13=1.33402498,
        k_q21=-1.05419705, k_q22=1.63861169, k_q23=-0.98192641,
        k_q31=1.08602944, k_q32=-1.67069631, k_q33=0.92706350
    )


@pytest.fixture
def target_twiss():
    return {
        'beta': [2.336495, 4.256241],
        'alpha': [-0.016335, 0.017772],
        'dispersion': [0.080868, 0.047472, 0.0, 0.0]
    }


def test_error_budget_config():
    """Test default error budget configuration values."""
    config = ErrorBudgetConfig()
    assert config.quad_k_rel_std == 1e-3
    assert config.quad_dx_std_m == 1e-4
    assert config.nkm_scale_std == 5e-3


def test_sample_error_ensemble_reproducibility():
    """Test reproducible Monte Carlo error sampling."""
    config = ErrorBudgetConfig()
    samples1 = sample_error_ensemble(config, n_samples=50, seed=42)
    samples2 = sample_error_ensemble(config, n_samples=50, seed=42)

    assert len(samples1) == 50
    assert samples1[0]["quad_k_err"] == samples2[0]["quad_k_err"]
    assert samples1[10]["booster_x_m"] == samples2[10]["booster_x_m"]


def test_apply_sample_errors(nominal_bts_config):
    """Test applying an error realization to an AT lattice."""
    samples = sample_error_ensemble(n_samples=5, seed=42)
    s = samples[0]
    lattice, init_twiss = apply_sample_errors(nominal_bts_config, s)

    assert len(lattice) > 0
    q11 = [e for e in lattice if e.FamName == 'q11'][0]
    assert hasattr(q11, 'T1')
    assert hasattr(q11, 'R1')
    assert q11.T1.shape == (6,)
    assert q11.R1.shape == (6, 6)


def test_quadrupole_roll_symplectic_structure():
    """Verify that quadrupole roll transformation is 6D symplectic."""
    nominal = BTSConfig()
    sample = sample_error_ensemble(n_samples=1)[0]
    roll_angle = 0.05  # 50 mrad
    sample["quad_roll_rad"] = [roll_angle] * 9

    lattice, _ = apply_sample_errors(nominal, sample)
    q11 = [e for e in lattice if e.FamName == 'q11'][0]

    cos_r = np.cos(roll_angle)
    sin_r = np.sin(roll_angle)

    # Check both positions and momenta are rotated
    assert q11.R1[0, 0] == pytest.approx(cos_r)
    assert q11.R1[0, 2] == pytest.approx(sin_r)
    assert q11.R1[1, 1] == pytest.approx(cos_r)
    assert q11.R1[1, 3] == pytest.approx(sin_r)
    assert q11.R1[2, 0] == pytest.approx(-sin_r)
    assert q11.R1[2, 2] == pytest.approx(cos_r)
    assert q11.R1[3, 1] == pytest.approx(-sin_r)
    assert q11.R1[3, 3] == pytest.approx(cos_r)

    # Symplectic matrix J in 6D: [ [0, 1], [-1, 0] ] blocks
    J = np.zeros((6, 6))
    for i in range(3):
        J[2*i, 2*i + 1] = 1.0
        J[2*i + 1, 2*i] = -1.0

    # Symplecticity condition: R * J * R.T == J
    r1_sym = q11.R1 @ J @ q11.R1.T
    np.testing.assert_allclose(r1_sym, J, atol=1e-14)

    r2_sym = q11.R2 @ J @ q11.R2.T
    np.testing.assert_allclose(r2_sym, J, atol=1e-14)


def test_monte_carlo_robustness_execution(nominal_bts_config, target_twiss):
    """Test Monte Carlo robustness evaluator on a small ensemble."""
    res = evaluate_monte_carlo_robustness(nominal_bts_config, target_twiss, n_samples=20, seed=42)

    assert res["n_samples"] == 20
    assert "mismatch_x" in res
    assert "p50" in res["mismatch_x"]
    assert "p95" in res["mismatch_x"]
    assert res["mismatch_x"]["mean"] > 0.0
    assert res["mismatch_y"]["mean"] > 0.0


def test_no_duplicate_booster_fields():
    config = ErrorBudgetConfig()
    samples = sample_error_ensemble(config, n_samples=1)
    sample = samples[0]
    assert "booster_x_jitter_m" not in sample
    assert "booster_dx_m" not in sample
    assert "booster_x_m" in sample
    assert "booster_xp_rad" in sample


def test_nkm_timing_sampled():
    config = ErrorBudgetConfig()
    samples = sample_error_ensemble(config, n_samples=1)
    assert "nkm_timing_mrad" in samples[0]


def test_apply_sample_errors_dict_structure():
    nominal = BTSConfig()
    sample = sample_error_ensemble(n_samples=1)[0]
    sample["booster_x_m"] = 0.001
    sample["booster_xp_rad"] = 0.002
    sample["nkm_scale_err"] = 0.01
    sample["ring_co_x_m"] = 0.003
    
    lat, twiss = apply_sample_errors(nominal, sample)
    
    assert "centroid_offset" in twiss
    assert twiss["centroid_offset"][0] == 0.001
    assert twiss["centroid_offset"][1] == 0.002
    
    assert "nkm_errors" in twiss
    assert "scale_err" in twiss["nkm_errors"]
    assert "dx_m" in twiss["nkm_errors"]
    assert "timing_mrad" in twiss["nkm_errors"]
    
    assert "ring_errors" in twiss
    assert "co_x_m" in twiss["ring_errors"]
    assert "septum_x_m" in twiss["ring_errors"]


def test_energy_rigidity_correction():
    nominal = BTSConfig(energy_eV=4.0e9, k_q11=1.0)
    sample = sample_error_ensemble(n_samples=1)[0]
    for k in sample:
        if isinstance(sample[k], list):
            sample[k] = [0.0]*len(sample[k])
        elif isinstance(sample[k], (float, int)):
            sample[k] = 0.0
    
    sample["energy_dp_p"] = 0.01
    sample["quad_k_err"] = [0.0]*9
    
    lat, twiss = apply_sample_errors(nominal, sample)
    
    assert lat.energy == pytest.approx(4.0e9 * 1.01)
    
    q11 = [elem for elem in lat if elem.FamName == "q11"][0]
    expected_k = 1.0 / 1.01
    assert q11.PolynomB[1] == pytest.approx(expected_k)


def test_evaluate_robustness_statistics_keys():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    samples = sample_error_ensemble(n_samples=10, seed=42)
    stats = evaluate_robustness_statistics(nominal, target_twiss, samples)
    
    assert "stored_beam_kick_mrad" in stats
    assert "convergence_check" in stats
    assert "failure_modes" in stats


def test_oat_sensitivity_includes_new_sources():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    rankings = compute_one_at_a_time_sensitivity(nominal, target_twiss, n_samples=5, seed=42)
    
    labels = list(rankings.keys())
    assert any("NKM Horizontal Alignment" in l for l in labels)
    assert any("Ring Closed-Orbit" in l for l in labels)
    assert any("Septum Position" in l for l in labels)


def test_nominal_vs_robust_comparison():
    nominal = BTSConfig()
    robust = BTSConfig(k_q11=0.5)
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    samples = sample_error_ensemble(n_samples=10, seed=42)
    
    comp = nominal_vs_robust_comparison(nominal, robust, target_twiss, samples)
    assert "nominal_stats" in comp
    assert "robust_stats" in comp
    assert "improvement_mismatch_x_p95" in comp
    assert "improvement_mismatch_y_p95" in comp


def test_stored_beam_kick_perturbation():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    
    # 1. On-axis stored beam (x_co = 0, dx_nkm = 0) -> zero kick
    s_zero = sample_error_ensemble(n_samples=1)[0]
    for k in s_zero:
        if isinstance(s_zero[k], float): s_zero[k] = 0.0
    s_zero["ring_co_x_m"] = 0.0
    s_zero["nkm_dx_m"] = 0.0
    s_zero["nkm_scale_err"] = 0.0
    stats_zero = evaluate_robustness_statistics(nominal, target_twiss, [s_zero])
    assert stats_zero["stored_beam_kick_mrad"]["p50"] == pytest.approx(0.0, abs=1e-6)
    
    # 2. Offset stored beam (x_co = 1 mm) -> non-zero deflection scaled by scale_err
    s1 = s_zero.copy()
    s1["ring_co_x_m"] = 0.001
    s1["nkm_scale_err"] = 0.0
    
    s2 = s1.copy()
    s2["nkm_scale_err"] = 0.1
    
    stats1 = evaluate_robustness_statistics(nominal, target_twiss, [s1])
    stats2 = evaluate_robustness_statistics(nominal, target_twiss, [s2])
    
    assert stats1["stored_beam_kick_mrad"]["p50"] > 0.0
    assert stats2["stored_beam_kick_mrad"]["p50"] == pytest.approx(stats1["stored_beam_kick_mrad"]["p50"] * 1.1, rel=1e-3)


def test_common_random_numbers():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    
    s1 = sample_error_ensemble(n_samples=10, seed=123)
    s2 = sample_error_ensemble(n_samples=10, seed=123)
    
    stats1 = evaluate_robustness_statistics(nominal, target_twiss, s1)
    stats2 = evaluate_robustness_statistics(nominal, target_twiss, s2)
    
    assert stats1["mismatch_x"]["p50"] == stats2["mismatch_x"]["p50"]
    assert stats1["failure_probability"] == stats2["failure_probability"]
