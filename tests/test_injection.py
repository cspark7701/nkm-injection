"""
Unit and Integration Tests for Milestone 5 NKM Injection Tracking & Beam Dynamics
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.beam import (
    generate_6d_beam,
    compute_beam_centroid,
    compute_projected_emittance,
    compute_beam_statistics
)
from src.nkm_injection.kickmap import NKMKickMap2D
from src.nkm_injection.tracking import track_nkm_thin_kick, track_nkm_rk4
from src.nkm_injection.injection import simulate_nkm_models


@pytest.fixture
def kickmap():
    p = REPO_ROOT / "kickmap_file.txt"
    assert p.is_file(), f"kickmap_file.txt missing at {p}"
    return NKMKickMap2D(p)


def test_generate_6d_beam():
    """Test 6D beam generation and statistics."""
    beam = generate_6d_beam(
        n_particles=500,
        beta_x=7.56, alpha_x=1.52, emit_x=10.89e-9,
        beta_y=12.27, alpha_y=-1.65, emit_y=10.89e-9,
        x_offset=-5.7e-3, xp_offset=3.0e-3, seed=42
    )
    assert beam.shape == (6, 500)
    centroid = compute_beam_centroid(beam)
    assert pytest.approx(centroid[0], abs=1e-4) == -5.7e-3
    assert pytest.approx(centroid[1], abs=1e-4) == 3.0e-3
    
    stats = compute_beam_statistics(beam)
    assert stats["survival_fraction"] == 1.0
    assert stats["total_particles"] == 500


def test_thin_kick_limiting_cases(kickmap):
    """Test zero field limiting case and scaling proportionality."""
    beam = generate_6d_beam(
        n_particles=100,
        beta_x=2.33, alpha_x=0.0, emit_x=10.89e-9,
        beta_y=4.25, alpha_y=0.0, emit_y=10.89e-9,
        x_offset=-5.7e-3, seed=42
    )
    
    # 1. Zero field scale -> zero kick
    b_zero = track_nkm_thin_kick(beam, kickmap.evaluate, scale_factor=0.0)
    c_in = compute_beam_centroid(beam)
    c_zero = compute_beam_centroid(b_zero)
    # xp change should be 0 (except drift effect on x)
    assert pytest.approx(c_zero[1], abs=1e-9) == c_in[1]
    
    # 2. Scaled kick -> proportional kick
    b_half = track_nkm_thin_kick(beam, kickmap.evaluate, scale_factor=0.5)
    b_full = track_nkm_thin_kick(beam, kickmap.evaluate, scale_factor=1.0)
    
    kick_half = compute_beam_centroid(b_half)[1] - c_in[1]
    kick_full = compute_beam_centroid(b_full)[1] - c_in[1]
    
    assert pytest.approx(kick_full, rel=1e-3) == 2.0 * kick_half


def test_rk4_tracking_consistency():
    """Test RK4 step integration consistency."""
    beam = generate_6d_beam(
        n_particles=50,
        beta_x=7.56, alpha_x=1.52, emit_x=10.89e-9,
        beta_y=12.27, alpha_y=-1.65, emit_y=10.89e-9,
        x_offset=-5.7e-3, seed=42
    )
    
    def constant_field(x):
        return np.full_like(x, 0.146)  # 0.146 T constant field
        
    b_rk4 = track_nkm_rk4(beam, constant_field, length_m=0.525, n_steps=20)
    c_in = compute_beam_centroid(beam)
    c_rk4 = compute_beam_centroid(b_rk4)
    
    expected_kick_rad = - (0.146 * 0.525) / (4.0e9 / 299792458.0)
    actual_kick_rad = c_rk4[1] - c_in[1]
    assert pytest.approx(actual_kick_rad, abs=1e-4) == expected_kick_rad


def test_injection_four_models_comparison(kickmap):
    """Test 4-model injection tracking pipeline (off, ideal, linear, fieldmap)."""
    circ_beam = generate_6d_beam(
        n_particles=200, beta_x=2.33, alpha_x=0.0, emit_x=10.89e-9,
        beta_y=4.25, alpha_y=0.0, emit_y=10.89e-9, x_offset=0.0, seed=42
    )
    inj_beam = generate_6d_beam(
        n_particles=200, beta_x=7.56, alpha_x=1.52, emit_x=10.89e-9,
        beta_y=12.27, alpha_y=-1.65, emit_y=10.89e-9, x_offset=-5.7e-3, seed=42
    )
    
    sim_res = simulate_nkm_models(inj_beam, circ_beam, kickmap)
    models = sim_res["models"]
    perf = sim_res["performance_metrics"]
    
    # 1. Verify all 4 models exist in output
    assert "nkm_off" in models
    assert "nkm_ideal" in models
    assert "nkm_linear" in models
    assert "nkm_fieldmap" in models
    
    # 2. Verify stored beam perturbation:
    # - Ideal dipole kicker perturbs stored beam (> 0.1 mrad)
    # - Fieldmap NKM protects stored beam (< 0.01 mrad)
    ideal_circ_kick = models["nkm_ideal"]["circulating_stats"]["centroid"]["xp_mrad"]
    fieldmap_circ_kick = models["nkm_fieldmap"]["circulating_stats"]["centroid"]["xp_mrad"]
    
    assert abs(ideal_circ_kick) > 0.1
    assert abs(fieldmap_circ_kick) < 0.01
    
    # 3. Verify performance metrics
    assert perf["injected_survival_fraction"] == 1.0
    assert perf["circulating_survival_fraction"] == 1.0
    assert perf["stored_beam_kick_mrad"] < 0.01
    assert perf["beam_separation_mm"] > 0.0
