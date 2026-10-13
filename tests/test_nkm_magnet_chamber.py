"""Round-3 in-magnet NKM chamber: wire clearance, kicker and control loss checks (units: m, rad)."""
import numpy as np
import pytest

from nkm_injection.chamber import NKM_CONDUCTOR_ALLOWANCE_M, ChamberProfile, nkm_chamber_half_height
from nkm_injection.injection_study import InjectionStudyConfig, _apply_kick
from nkm_injection.wire_field import CalibratedControl, FilamentGeometry, FilamentNKMKicker


def test_maximum_half_height_leaves_allowance_below_inner_wires():
    g = FilamentGeometry()
    assert nkm_chamber_half_height(g) == pytest.approx(g.y1_m - NKM_CONDUCTOR_ALLOWANCE_M)
    ChamberProfile(nkm_magnet_half_x_m=0.016, nkm_magnet_half_y_m=nkm_chamber_half_height(g)).validate_against_wires(g)


def test_round2_assumed_straight_chamber_cannot_be_the_magnet_chamber():
    with pytest.raises(ValueError, match="reaches wire"):
        ChamberProfile(nkm_magnet_half_x_m=0.030, nkm_magnet_half_y_m=0.015).validate_against_wires(FilamentGeometry())


def test_partial_in_magnet_chamber_is_rejected():
    with pytest.raises(ValueError):
        ChamberProfile(nkm_magnet_half_x_m=0.016).validate()


def _beam(y):
    b = np.zeros((6, 2))
    b[0] = -0.0086
    b[2] = y
    return b


def test_kicker_chamber_removes_only_particles_outside_the_flat_aperture():
    cfg = InjectionStudyConfig(field_scale=0.0)
    inside, outside = _beam([0.0, 0.0]), _beam([0.001, 0.0045])
    kick = FilamentNKMKicker(cfg, n_slices=40, chamber_half_x_m=0.016, chamber_half_y_m=0.0038)
    assert not kick.apply(inside, 0.0).any()
    assert kick.apply(outside, 0.0).tolist() == [False, True]


def test_default_kicker_keeps_round2_conductor_rule():
    cfg = InjectionStudyConfig(field_scale=0.0)
    assert not FilamentNKMKicker(cfg, n_slices=40).apply(_beam([0.001, 0.0045]), 0.0).any()


def test_control_sees_the_same_chamber_at_the_magnet_centre():
    cfg = InjectionStudyConfig()
    ctrl = CalibratedControl("dipole", -4.8e-3, 0.0, -0.0086, chamber_half_x_m=0.016, chamber_half_y_m=0.0038)
    b = _beam([0.0, 0.0045])
    _, out = _apply_kick(b, ctrl, cfg.closed_orbit_x_m)
    assert out.tolist() == [False, True]
    with pytest.raises(ValueError):
        CalibratedControl("dipole", 0.0, 0.0, 0.0, chamber_half_y_m=0.004)


def test_ring_magnet_halves_carry_the_in_magnet_chamber():
    import at
    from nkm_injection.chamber import apply_chamber
    r = at.Lattice([at.Drift("NKM_H2", 0.2625), at.Drift("LH1", 1.0), at.Drift("NKM_H1", 0.2625)], energy=4e9)
    ch, meta = apply_chamber(r, ChamberProfile(ivu_count=0, nkm_magnet_half_x_m=0.016, nkm_magnet_half_y_m=0.0038))
    assert list(ch[0].RApertures) == [-0.016, 0.016, -0.0038, 0.0038]
    assert list(ch[1].RApertures) == [-0.03, 0.03, -0.015, 0.015]
    assert {m["region"] for m in meta["assignments"] if m["family"].startswith("NKM_H")} == {"nkm_magnet_chamber"}
    ch0, _ = apply_chamber(r, ChamberProfile(ivu_count=0))
    assert list(ch0[0].RApertures) == [-0.03, 0.03, -0.015, 0.015]
