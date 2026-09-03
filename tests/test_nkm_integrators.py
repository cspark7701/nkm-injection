"""
Unit tests for Symplectic Split and Lorentz RK4 integrators (Task 03)
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.integrators import SymplecticSplitIntegrator, LorentzRK4Integrator
from src.nkm_injection.tracking import (
    track_nkm_thick_symplectic,
    track_nkm_thick_rk4,
    track_nkm_thin_kick,
    track_nkm_symplectic,
    track_nkm_rk4
)
from src.nkm_injection.units import compute_rigidity, ELECTRON_CHARGE_C


def test_zero_field_limit():
    """Zero magnetic field should reduce to a pure drift of length L."""
    def zero_field(x, y, z):
        return np.zeros_like(x), np.zeros_like(x)

    beam_in = np.zeros((6, 2))
    beam_in[0, 0] = -0.010  # x = -10 mm
    beam_in[1, 0] = 0.001   # xp = 1 mrad
    beam_in[2, 1] = 0.005   # y = 5 mm
    beam_in[3, 1] = -0.002  # yp = -2 mrad

    length_m = 0.525

    # Symplectic split tracker
    beam_sym = track_nkm_thick_symplectic(beam_in, zero_field, length_m=length_m, n_slices=20)
    # RK4 tracker
    beam_rk4 = track_nkm_thick_rk4(beam_in, zero_field, length_m=length_m, n_slices=20)

    # Pure drift x_out = x_in + xp * L, xp_out = xp_in
    np.testing.assert_allclose(beam_sym[0, :], beam_in[0, :] + beam_in[1, :] * length_m, atol=1e-12)
    np.testing.assert_allclose(beam_sym[1, :], beam_in[1, :], atol=1e-12)
    np.testing.assert_allclose(beam_sym[2, :], beam_in[2, :] + beam_in[3, :] * length_m, atol=1e-12)
    np.testing.assert_allclose(beam_sym[3, :], beam_in[3, :], atol=1e-12)

    np.testing.assert_allclose(beam_rk4[0, :], beam_in[0, :] + beam_in[1, :] * length_m, atol=1e-12)
    np.testing.assert_allclose(beam_rk4[1, :], beam_in[1, :], atol=1e-12)


def test_uniform_field_limit():
    """Uniform dipole field By = B0 gives constant deflection rate Delta xp = - B0 * L / B_rho for electrons."""
    B0 = 0.146  # 0.146 T
    def uniform_field(x, y, z):
        return np.full_like(x, B0), np.zeros_like(x)

    length_m = 0.525
    energy_GeV = 4.0
    brho = compute_rigidity(energy_GeV * 1e9, ELECTRON_CHARGE_C)
    expected_kick_rad = - B0 * length_m / brho  # ~ -0.005747 rad

    beam_in = np.zeros((6, 1))

    beam_sym = track_nkm_thick_symplectic(beam_in, uniform_field, length_m=length_m, n_slices=100, energy_GeV=energy_GeV)
    beam_rk4 = track_nkm_thick_rk4(beam_in, uniform_field, length_m=length_m, n_slices=100, energy_GeV=energy_GeV)

    assert pytest.approx(beam_sym[1, 0], rel=1e-4) == expected_kick_rad
    assert pytest.approx(beam_rk4[1, 0], rel=1e-4) == expected_kick_rad


def test_slice_convergence():
    """Check convergence of exit position and angle as slice count increases."""
    def nkm_model_field(x, y, z):
        # Model NKM B_y(x) profile
        by = 0.146 * np.exp(-((x + 0.010)/0.015)**2)
        bx = np.zeros_like(x)
        return by, bx

    beam_in = np.zeros((6, 1))
    beam_in[0, 0] = -0.010  # -10 mm offset

    slice_counts = [10, 20, 40, 80, 160]
    exit_xp = []

    for n in slice_counts:
        out = track_nkm_thick_symplectic(beam_in, nkm_model_field, length_m=0.525, n_slices=n)
        exit_xp.append(out[1, 0])

    ref_xp = exit_xp[-1]
    errors = [abs(xp - ref_xp) for xp in exit_xp]

    # Error must decrease monotonically with slice refinement
    assert errors[-2] < errors[0]
    assert errors[-1] < 1e-7


def test_two_plane_thin_thick_kick_agreement():
    """Verify two-plane (Bx, By) thin-kick vs. thick-integrator agreement for a uniform field."""
    B0x = 0.05  # T
    B0y = 0.146 # T
    length_m = 0.525
    energy_GeV = 4.0
    brho = compute_rigidity(energy_GeV * 1e9, ELECTRON_CHARGE_C)

    def uniform_2d_field(x, y, z):
        return np.full_like(x, B0y), np.full_like(x, B0x)

    # Electron: Delta x' = - B0y * L / B_rho, Delta y' = + B0x * L / B_rho
    exp_dxp = - B0y * length_m / brho
    exp_dyp = + B0x * length_m / brho

    beam_in = np.zeros((6, 1))

    beam_sym = track_nkm_thick_symplectic(beam_in, uniform_2d_field, length_m=length_m, n_slices=100, energy_GeV=energy_GeV)
    beam_rk4 = track_nkm_thick_rk4(beam_in, uniform_2d_field, length_m=length_m, n_slices=100, energy_GeV=energy_GeV)

    assert pytest.approx(beam_sym[1, 0], rel=1e-4) == exp_dxp
    assert pytest.approx(beam_sym[3, 0], rel=1e-4) == exp_dyp

    assert pytest.approx(beam_rk4[1, 0], rel=1e-4) == exp_dxp
    assert pytest.approx(beam_rk4[3, 0], rel=1e-4) == exp_dyp


def test_track_nkm_symplectic_alias_and_legacy_rk4():
    """Verify track_nkm_symplectic and track_nkm_rk4 tracking wrappers."""
    beam_in = np.zeros((6, 1))
    beam_in[0, 0] = -0.016

    def field_2d(x, y, z):
        return np.full_like(x, 0.146), np.zeros_like(x)

    def field_1d(x):
        return np.full_like(x, 0.146)

    # 1. track_nkm_symplectic alias
    out_sym = track_nkm_symplectic(beam_in.copy(), field_2d, length_m=0.525, n_slices=40)
    out_thick_sym = track_nkm_thick_symplectic(beam_in.copy(), field_2d, length_m=0.525, n_slices=40)
    np.testing.assert_allclose(out_sym, out_thick_sym)

    # 2. track_nkm_rk4 legacy wrapper
    out_rk4 = track_nkm_rk4(beam_in.copy(), field_1d, length_m=0.525, n_steps=40)
    np.testing.assert_allclose(out_rk4, out_thick_sym)


# ---------------------------------------------------------------------------
# Task 14 — Protocol and Mock Evaluator Tests
# ---------------------------------------------------------------------------

from src.nkm_injection.units import (
    FieldMap3DProtocol,
    KickerEvaluatorProtocol,
    ZeroFieldMap3D,
    UniformFieldMap3D,
    LinearGradientFieldMap3D,
    KickMapMetadata
)
from src.nkm_injection.storage_ring_injection import (
    OffKickerEvaluator,
    IdealKickerEvaluator,
    LinearKickerEvaluator,
    StorageRingInjectionConfig,
    get_kicker_evaluator
)
from src.nkm_injection.kickmap import NKMKickMap2D


def test_field_map_3d_protocol_and_mock_evaluators():
    """Verify that mock field maps conform to FieldMap3DProtocol and track accurately."""
    x = np.array([-0.010, 0.0, 0.010])
    y = np.array([0.0, 0.005, -0.005])

    # 1. ZeroFieldMap3D
    zero_map = ZeroFieldMap3D()
    assert isinstance(zero_map, FieldMap3DProtocol)
    by, bx = zero_map(x, y, z=0.1)
    np.testing.assert_allclose(by, 0.0)
    np.testing.assert_allclose(bx, 0.0)

    # 2. UniformFieldMap3D
    unif_map = UniformFieldMap3D(by_T=0.146, bx_T=-0.05)
    assert isinstance(unif_map, FieldMap3DProtocol)
    by, bx = unif_map(x, y, z=0.2)
    np.testing.assert_allclose(by, 0.146)
    np.testing.assert_allclose(bx, -0.05)

    # 3. LinearGradientFieldMap3D
    grad_map = LinearGradientFieldMap3D(gradient_T_per_m=2.5)
    assert isinstance(grad_map, FieldMap3DProtocol)
    by, bx = grad_map(x, y, z=0.0)
    np.testing.assert_allclose(by, 2.5 * x)
    np.testing.assert_allclose(bx, 2.5 * y)

    # 4. Direct tracking with mock field map instance in SymplecticSplitIntegrator
    beam_in = np.zeros((6, 1))
    beam_in[0, 0] = -0.010
    integrator = SymplecticSplitIntegrator(unif_map, length_m=0.525, n_slices=20, energy_GeV=4.0)
    beam_out = integrator.track(beam_in)
    assert abs(beam_out[1, 0]) > 0.0


def test_kicker_evaluator_protocols():
    """Verify that all 4 kicker models produce evaluators conforming to KickerEvaluatorProtocol."""
    cfg = StorageRingInjectionConfig()

    # 1. Off model
    eval_off, meta_off = get_kicker_evaluator("off", config=cfg)
    assert isinstance(eval_off, KickerEvaluatorProtocol)
    assert eval_off.model_type == "off"
    kx, ky = eval_off.evaluate_kicks(np.array([-0.016, 0.0]))
    np.testing.assert_allclose(kx, 0.0)
    np.testing.assert_allclose(ky, 0.0)

    # 2. Ideal model
    eval_ideal, meta_ideal = get_kicker_evaluator("ideal", config=cfg)
    assert isinstance(eval_ideal, KickerEvaluatorProtocol)
    assert eval_ideal.model_type == "ideal"
    kx, ky = eval_ideal.evaluate_kicks(np.array([-0.016, 0.0]))
    assert abs(kx[0]) > 0.0
    np.testing.assert_allclose(ky, 0.0)

    # 3. Linear model
    eval_linear, meta_linear = get_kicker_evaluator("linear", config=cfg)
    assert isinstance(eval_linear, KickerEvaluatorProtocol)
    assert eval_linear.model_type == "linear"
    kx, ky = eval_linear.evaluate_kicks(np.array([-0.016, 0.0]))
    assert abs(kx[0]) > 0.0
    np.testing.assert_allclose(ky, 0.0)

    # 4. Fieldmap model (mocked metadata or loaded from file)
    kmap_path = REPO_ROOT / "kickmap_file.txt"
    if kmap_path.is_file():
        kmap = NKMKickMap2D(kmap_path)
        assert isinstance(kmap, KickerEvaluatorProtocol)
        assert kmap.model_type == "fieldmap"
        eval_fmap, meta_fmap = get_kicker_evaluator("fieldmap", config=cfg, kickmap_obj=kmap)
        assert isinstance(eval_fmap, KickerEvaluatorProtocol)
        kx, ky = eval_fmap.evaluate_kicks(np.array([-0.016, 0.0]))
        assert abs(kx[0]) > 0.0



