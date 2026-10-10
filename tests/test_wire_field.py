"""Exact filament NKM field: agreement with the RADIA kick map, curl-free kicks and tracker limits."""
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.injection_study import InjectionStudyConfig, KickModelEvaluator, _apply_kick
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.wire_field import FilamentNKMField, FilamentNKMKicker, brho_T_m, segment_field

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def kmap():
    return NKMKickMap2D(ROOT / "kickmap_file.txt")


def test_infinite_wire_limit():
    a, b = np.array([[0.0, 0.0, -1e3]]), np.array([[0.0, 0.0, 1e3]])
    bf = segment_field(np.array([[0.01, 0.0, 0.0]]), a, b, 100.0)[0]
    assert bf[1] == pytest.approx(2e-7 * 100.0 / 0.01, rel=1e-6) and abs(bf[0]) < 1e-15


def test_line_integrals_reproduce_both_map_components(kmap):
    x = np.array([-0.0085, -0.009, 0.004, -0.005, 0.0, 0.02])
    y = np.array([0.0, 0.002, 0.004, -0.003, 0.0, -0.015])
    ibx, iby = FilamentNKMField().line_integrals(x, y, s_max_m=5.0)
    kx, ky = kmap.evaluate_kicks(x, y)
    br = brho_T_m(4e9)
    assert np.max(np.abs(iby / br - kx)) < 1e-9   # rad
    assert np.max(np.abs(ibx / br - ky)) < 1e-9   # map stores +∫Bx/Bρ (non-physical vertical sign)


def test_physical_kicks_are_curl_free(kmap):
    ev = KickModelEvaluator("fieldmap", InjectionStudyConfig(), kmap, -0.009, interpolation="cubic")
    h = 1e-4
    for x, y in ((-0.009, 0.002), (-0.002, 0.001), (-0.012, 0.003), (0.003, -0.008)):  # ≥ 3 mm from wires
        dkx_dy = (ev.kicks(np.array([x]), np.array([y + h]))[0] - ev.kicks(np.array([x]), np.array([y - h]))[0]) / (2 * h)
        dky_dx = (ev.kicks(np.array([x + h]), np.array([y]))[1] - ev.kicks(np.array([x - h]), np.array([y]))[1]) / (2 * h)
        assert dkx_dy[0] == pytest.approx(dky_dx[0], rel=1e-2, abs=1e-6)  # spline-limited


def test_tracker_zero_field_is_exact_drift_identity():
    cfg = InjectionStudyConfig(field_scale=0.0)
    beam = np.zeros((6, 3)); beam[0] = [-0.009, 0.0, 0.002]; beam[1] = [4e-3, 0.0, -1e-3]; beam[4] = [0, 1e-3, -2e-3]
    out = beam.copy()
    _apply_kick(out, FilamentNKMKicker(cfg, n_slices=40), 0.0)
    assert np.max(np.abs(out[:4] - beam[:4])) < 1e-15  # transverse identity (path length ct may change)


def test_tracker_converges_and_matches_thin_on_straight_line(kmap):
    cfg = InjectionStudyConfig(field_scale=1.0)
    # a particle with zero slope sees the straight-line integral, so the thick and thin kicks nearly agree
    beam = np.zeros((6, 1)); beam[0] = -0.0085
    a, b = beam.copy(), beam.copy()
    _apply_kick(a, FilamentNKMKicker(cfg, n_slices=320), 0.0)
    _apply_kick(b, FilamentNKMKicker(cfg, n_slices=640), 0.0)
    assert abs(a[1, 0] - b[1, 0]) < 1e-8
    kx, _ = kmap.evaluate_kicks(np.array([-0.0085]), np.array([0.0]))
    assert abs(b[1, 0] - kx[0]) < 0.02 * abs(kx[0])  # differs only by the bending inside the magnet
    assert b[1, 0] < 0  # P = +1: negative kick at x < 0


def test_kick_is_canonical_and_lost_near_wires():
    cfg = InjectionStudyConfig(field_scale=1.0)
    b0 = np.zeros((6, 2)); b0[0] = -0.0085; b0[4] = [0.0, 1e-3]
    _apply_kick(b0, FilamentNKMKicker(cfg, n_slices=320), 0.0)
    assert abs(b0[1, 0] - b0[1, 1]) < 1e-3 * abs(b0[1, 0])  # no 1/(1+δ) on the canonical kick
    w = np.zeros((6, 1)); w[0] = 0.0053; w[2] = 0.0053
    assert FilamentNKMKicker(cfg, n_slices=40).apply(w, 0.0).all()


def test_exact_field_kicks_are_curl_free():
    f, h = FilamentNKMField(), 1e-5
    for x, y in ((-0.009, 0.002), (0.003, -0.008)):
        # physical pair (∫By, −∫Bx): ∂(∫By)/∂y = ∂(−∫Bx)/∂x
        d1 = (f.line_integrals([x], [y + h])[1] - f.line_integrals([x], [y - h])[1]) / (2 * h)
        d2 = -(f.line_integrals([x + h], [y])[0] - f.line_integrals([x - h], [y])[0]) / (2 * h)
        assert d1[0] == pytest.approx(d2[0], rel=1e-5)  # quadrature + finite-difference limited
