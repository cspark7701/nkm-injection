"""Contract tests for the journal-campaign drivers."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.injection_study import InjectionStudyConfig, prepare_ring
from nkm_injection.kickmap import NKMKickMap2D

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S6 = _load("run_injection_operating_region")


def test_s6_parser_requires_selection_and_matched_angle():
    with pytest.raises(SystemExit):
        S6.parse_args(["--study-config", "c.json", "--output-dir", "x"])
    cfg = InjectionStudyConfig()
    kmap = NKMKickMap2D(ROOT / "kickmap_file.txt")
    xp = S6.matched_angle(cfg, kmap, -0.020)
    assert S6.matched_angle(cfg, kmap, -0.020, 0.9) != pytest.approx(xp)
    lever = cfg.septum_to_nkm_drift_m + S6.NKM_HALF_LENGTH_M
    xc = -0.020 + lever * xp
    kick = kmap.evaluate_kicks(np.array([xc]), np.array([0.0]))[0][0]
    assert xp > 0 and abs(xp + kick) < 1e-12  # angle cancelled at the NKM centre (P = +1)
    assert -0.012 < xc < -0.004


def test_s6_jobs_are_paired_and_cover_groups(tmp_path):
    args = S6.parse_args(["--study-config", "c.json", "--optimization-summary", "o.json", "--output-dir", str(tmp_path),
                          "--x-offset-mm", "-21", "-20", "--xp-offset-mrad", "-0.5", "0", "--field-scale", "0.95", "1.0",
                          "--seeds", "42", "123"])
    cfg = InjectionStudyConfig()
    kmap = NKMKickMap2D(ROOT / "kickmap_file.txt")
    bts = {"bts_config": {}, "initial_twiss": {}}
    jobs, xmatch = S6.build_jobs(args, cfg, kmap, ROOT, tmp_path, bts, bts)
    groups = [j["group"] for j in jobs]
    assert groups.count("map") == 8 and groups.count("linmap") == 8
    assert groups.count("replicate") == 2 and groups.count("bts") == 2
    centre = [j for j in jobs if j["group"] == "map" and j["xp_offset_rad"] == 0.0]
    assert all(j["models"] == ["fieldmap", "off", "dipole", "linear"] for j in centre)  # paired controls
    assert len(xmatch) == 4
    only = S6.parse_args(["--study-config", "c.json", "--optimization-summary", "o.json", "--output-dir", str(tmp_path),
                          "--stages", "replicate", "--seeds", "1", "2", "3"])
    jobs2, _ = S6.build_jobs(only, cfg, kmap, ROOT, tmp_path, bts, bts)
    assert {j["group"] for j in jobs2} == {"replicate", "bts"} and len(jobs2) == 6


def test_centroid_amplitude_zero_for_on_axis(tmp_path):
    ring = prepare_ring(InjectionStudyConfig(), ROOT, tmp_path)
    cfg = InjectionStudyConfig(injection_x_m=0.0, injection_xp_rad=0.0)
    amp, xc, xp = S6.centroid_amplitude(ring, cfg, lambda x: 0.0)
    assert amp == 0.0 and xc == 0.0 and xp == 0.0
