"""Tests for the journal-campaign injection model (units: m, rad, eV)."""
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.injection_study import (
    InjectionStudyConfig, KickModelEvaluator, prepare_ring, injected_beam_at_septum,
    track_injection, stored_beam_response, KICK_MODELS)
from nkm_injection.kickmap import NKMKickMap2D

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def kickmap():
    return NKMKickMap2D(ROOT / "kickmap_file.txt")


@pytest.fixture(scope="module")
def ring(tmp_path_factory):
    return prepare_ring(InjectionStudyConfig(), ROOT, tmp_path_factory.mktemp("ring"))


def test_config_round_trip_and_example(tmp_path):
    cfg = InjectionStudyConfig(field_scale=1.05, chamber_half_x_m=0.012)
    cfg.save(tmp_path / "c.json")
    assert InjectionStudyConfig.load(tmp_path / "c.json") == cfg
    assert InjectionStudyConfig.load(ROOT / "config/injection_study_v1.json") == InjectionStudyConfig()


@pytest.mark.parametrize("kwargs", [{"kicker_polarity": 0}, {"n_turns": 0}, {"schema_version": 2},
                                    {"septum_edge_x_m": 0.01}, {"chamber_half_x_m": -1.0}])
def test_config_rejects_invalid(kwargs):
    with pytest.raises(ValueError):
        InjectionStudyConfig(**kwargs).validate()


def test_polarity_and_calibrated_controls(kickmap):
    cfg = InjectionStudyConfig()
    x_ref = -0.0085
    fm = KickModelEvaluator("fieldmap", cfg, kickmap, x_ref)
    kx_ref = fm.kicks(np.array([x_ref]), np.array([0.0]))[0][0]
    assert kx_ref == pytest.approx(-5.749065e-3, abs=1e-8)  # stored map value, P = +1
    flipped = KickModelEvaluator("fieldmap", InjectionStudyConfig(kicker_polarity=-1), kickmap, x_ref)
    assert flipped.kicks(np.array([x_ref]), np.array([0.0]))[0][0] == pytest.approx(-kx_ref, abs=1e-15)
    dip = KickModelEvaluator("dipole", cfg, kickmap, x_ref)
    lin = KickModelEvaluator("linear", cfg, kickmap, x_ref)
    xs = np.array([x_ref, 0.0])
    assert np.allclose(dip.kicks(xs, np.zeros(2))[0], kx_ref, atol=1e-15)
    assert lin.kicks(np.array([x_ref]), np.zeros(1))[0][0] == pytest.approx(kx_ref, abs=1e-15)
    assert np.all(KickModelEvaluator("off", cfg, None, x_ref).kicks(xs, np.zeros(2))[0] == 0)
    assert abs(fm.kicks(np.array([0.0]), np.array([0.0]))[0][0]) < 1e-12
    assert not fm.in_domain(np.array([0.06]), np.array([0.0]))[0]
    with pytest.raises(ValueError):
        KickModelEvaluator("ideal", cfg, kickmap, x_ref)


def test_ring_layout_and_optics(ring):
    assert ring.ring_c[ring.septum_index].FamName == "NKMUPRING"
    assert ring.circumference_m == pytest.approx(799.29698, abs=1e-5)
    assert ring.twiss_x[0] == pytest.approx(16.274, abs=1e-3)
    assert 5e-11 < ring.emit_x_m_rad < 7e-11


def test_septum_creation_and_zero_kick_backends_agree_near_axis(ring, kickmap):
    cfg = InjectionStudyConfig(injection_x_m=-0.0175, injection_xp_rad=0.0)
    beam = np.zeros((6, 3))
    beam[0] = [-0.0175, -0.0190, -0.0195]  # first lies on the stored side of the blade outer face
    beam[4] += ring.orbit6[4]; beam[5] += ring.orbit6[5]
    off = KickModelEvaluator("off", cfg, None, -0.01)
    res = track_injection(cfg, ring, off, beam, "map", n_turns=3)
    assert res["loss_causes"]["septum_creation"] == 1
    # Small-amplitude particle: native and linear backends agree after a few turns.
    small = np.zeros((6, 1)); small[0] = -0.0185; small[1] = 0.0055
    small[4] += ring.orbit6[4]; small[5] += ring.orbit6[5]
    fm = KickModelEvaluator("fieldmap", InjectionStudyConfig(), kickmap, -0.0065)
    a = track_injection(InjectionStudyConfig(), ring, fm, small, "element", n_turns=3)
    b = track_injection(InjectionStudyConfig(), ring, fm, small, "map", n_turns=3)
    assert a["captured"] == b["captured"] == 1


def test_stored_beam_response_controls(ring, kickmap):
    cfg = InjectionStudyConfig()
    r_fm = stored_beam_response(cfg, ring, KickModelEvaluator("fieldmap", cfg, kickmap, cfg.nkm_entry_x_m), n=20000)
    r_dp = stored_beam_response(cfg, ring, KickModelEvaluator("dipole", cfg, kickmap, cfg.nkm_entry_x_m), n=20000)
    assert r_fm["amplitude_over_sigma"] < 1e-2
    assert r_dp["amplitude_over_sigma"] > 100
    assert r_dp["centroid_amplitude_m"] == pytest.approx(ring.twiss_x[0] * abs(r_dp["mean_kick_x_rad"]), rel=1e-12)


def test_cubic_interpolation_matches_nodes_and_cubic_law(kickmap):
    cfg = InjectionStudyConfig()
    lin = KickModelEvaluator("fieldmap", cfg, kickmap, -0.009)
    cub = KickModelEvaluator("fieldmap", cfg, kickmap, -0.009, interpolation="cubic")
    nodes = kickmap.x_grid[::5]
    assert np.allclose(lin.kicks(nodes, np.zeros_like(nodes))[0], cub.kicks(nodes, np.zeros_like(nodes))[0], atol=1e-15, rtol=0)
    c = cub.kicks(np.array([1e-3]), np.zeros(1))[0][0] / 1e-9  # cubic coefficient from the 1 mm node
    x = np.array([1e-4, 2e-4, 3e-4])
    assert np.allclose(cub.kicks(x, np.zeros(3))[0], c * x ** 3, rtol=0.01)
    assert np.all(lin.kicks(x, np.zeros(3))[0] > 2 * c * x ** 3)  # bilinear overstates near the axis
    with pytest.raises(ValueError):
        KickModelEvaluator("fieldmap", cfg, kickmap, -0.009, interpolation="quadratic")


def test_thick_nkm_kicker_limits_and_sign(kickmap):
    from nkm_injection.fieldmap import load_1d_fieldmap
    from nkm_injection.injection_study import ThickNKMKicker, _apply_kick
    x, by = load_1d_fieldmap(ROOT / "By.txt")
    beam = np.zeros((6, 3)); beam[0] = [-0.009, 0.0, 0.002]; beam[1] = [1e-3, 0.0, -2e-3]
    zero = beam.copy()
    _apply_kick(zero, ThickNKMKicker(InjectionStudyConfig(field_scale=0.0), x, by), 0.0)
    assert np.max(np.abs(zero - beam)) < 1e-15  # zero field: back-drift and forward drift cancel exactly
    thick, thin = beam.copy(), beam.copy()
    cfg = InjectionStudyConfig()
    _apply_kick(thick, ThickNKMKicker(cfg, x, by, n_slices=160), 0.0)
    _apply_kick(thin, KickModelEvaluator("fieldmap", cfg, kickmap, -0.009), 0.0)
    assert np.sign(thick[1, 0] - beam[1, 0]) == np.sign(thin[1, 0] - beam[1, 0]) == -1.0  # P = +1 at x < 0
    assert abs((thick[1, 0] - thin[1, 0])) < 2e-4  # thin-lens error bounded (rad) at the kick peak region
    far = beam.copy(); far[0] = 0.06
    lost = ThickNKMKicker(cfg, x, by).apply(far, 0.0)
    assert lost.all() and np.isnan(far[0]).all()  # outside the profile: lost, never extrapolated
