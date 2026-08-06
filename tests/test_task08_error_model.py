import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm.errors import ErrorBudgetConfig, sample_error_ensemble, apply_sample_errors
from src.nkm.robust_optimization import evaluate_robustness_statistics, compute_one_at_a_time_sensitivity, nominal_vs_robust_comparison
from src.nkm.bts_lattice import BTSConfig

def test_task08_no_duplicate_booster_fields():
    config = ErrorBudgetConfig()
    samples = sample_error_ensemble(config, n_samples=1)
    sample = samples[0]
    assert "booster_x_jitter_m" not in sample
    assert "booster_dx_m" not in sample
    assert "booster_x_m" in sample
    assert "booster_xp_rad" in sample

def test_task08_nkm_timing_sampled():
    config = ErrorBudgetConfig()
    samples = sample_error_ensemble(config, n_samples=1)
    assert "nkm_timing_mrad" in samples[0]

def test_task08_apply_sample_errors_dict_structure():
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

def test_task08_energy_rigidity_correction():
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

def test_task08_evaluate_robustness_statistics_keys():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    samples = sample_error_ensemble(n_samples=10, seed=42)
    stats = evaluate_robustness_statistics(nominal, target_twiss, samples)
    
    assert "stored_beam_kick_mrad" in stats
    assert "convergence_check" in stats
    assert "failure_modes" in stats

def test_task08_oat_sensitivity_includes_new_sources():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    rankings = compute_one_at_a_time_sensitivity(nominal, target_twiss, n_samples=5, seed=42)
    
    labels = list(rankings.keys())
    assert any("NKM Horizontal Alignment" in l for l in labels)
    assert any("Ring Closed-Orbit" in l for l in labels)
    assert any("Septum Position" in l for l in labels)

def test_task08_nominal_vs_robust_comparison():
    nominal = BTSConfig()
    robust = BTSConfig(k_q11=0.5)
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    samples = sample_error_ensemble(n_samples=10, seed=42)
    
    comp = nominal_vs_robust_comparison(nominal, robust, target_twiss, samples)
    assert "nominal_stats" in comp
    assert "robust_stats" in comp
    assert "improvement_mismatch_x_p95" in comp
    assert "improvement_mismatch_y_p95" in comp

def test_task08_stored_beam_kick_perturbation():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    
    s1 = sample_error_ensemble(n_samples=1)[0]
    for k in s1:
        if isinstance(s1[k], float): s1[k] = 0.0
    s1["ring_co_x_m"] = 0.001
    s1["nkm_scale_err"] = 0.0
    
    s2 = s1.copy()
    s2["nkm_scale_err"] = 0.1
    
    stats1 = evaluate_robustness_statistics(nominal, target_twiss, [s1])
    stats2 = evaluate_robustness_statistics(nominal, target_twiss, [s2])
    
    assert stats1["stored_beam_kick_mrad"]["p50"] == 0.0
    assert stats2["stored_beam_kick_mrad"]["p50"] > 0.0

def test_task08_common_random_numbers():
    nominal = BTSConfig()
    target_twiss = {"beta": [2.336, 4.256], "alpha": [-0.016, 0.017]}
    
    s1 = sample_error_ensemble(n_samples=10, seed=123)
    s2 = sample_error_ensemble(n_samples=10, seed=123)
    
    stats1 = evaluate_robustness_statistics(nominal, target_twiss, s1)
    stats2 = evaluate_robustness_statistics(nominal, target_twiss, s2)
    
    assert stats1["mismatch_x"]["p50"] == stats2["mismatch_x"]["p50"]
    assert stats1["failure_probability"] == stats2["failure_probability"]
