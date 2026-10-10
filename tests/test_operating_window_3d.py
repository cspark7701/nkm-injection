"""C3 driver helpers: matched angle with the 3-D NKM and calibrated controls (no ring tracking)."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.injection_study import InjectionStudyConfig, _apply_kick
from nkm_injection.wire_field import FilamentNKMKicker

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ow3d", ROOT / "scripts" / "run_operating_window_3d.py")
OW = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OW)


def test_matched_angle_zeroes_exit_angle_and_controls_reproduce_it():
    cfg = InjectionStudyConfig(injection_x_m=-0.020, field_scale=0.85)
    xm = OW.matched_angle_3d(cfg, 320)
    assert 4.4e-3 < xm < 4.9e-3
    c = InjectionStudyConfig(injection_x_m=-0.020, field_scale=0.85, injection_xp_rad=xm)
    assert abs(OW.centroid_exit(c, FilamentNKMKicker(c, n_slices=320), xm)[1]) < 1e-10
    k0, k1, xref = OW.calibrate_controls(c, 320)
    for model in ("dipole", "linear"):
        b = np.zeros((6, 1)); b[0] = xref; b[1] = xm
        _apply_kick(b, OW.CalibratedControl(model, k0, k1, xref), 0.0)
        assert abs(b[1, 0]) < 1e-12  # nominal centroid leaves with zero angle, as for the NKM
    lin = OW.CalibratedControl("linear", k0, k1, xref)
    kx, ky = lin.kicks(np.array([xref + 1e-4]), np.array([1e-4]))
    assert kx[0] - k0 == pytest.approx(k1 * 1e-4) and ky[0] == pytest.approx(-k1 * 1e-4)  # curl-free partner
