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


S5 = _load("run_tracking_backend_validation")


def test_s5_parser_contract():
    a = S5.parse_args(["--study-config", "c.json", "--optimization-summary", "o.json", "--backends", "map", "element",
                       "--kicker-models", "off", "fieldmap", "dipole", "linear", "--particles", "1000", "10000",
                       "--turns", "100", "1000", "--seeds", "42", "123", "--workers", "2", "--output-dir", "x"])
    assert a.backends == ["map", "element"] and a.particles == [1000, 10000] and a.seeds == [42, 123]
    with pytest.raises(SystemExit):
        S5.parse_args(["--study-config", "c.json", "--output-dir", "x", "--kicker-models", "ideal"])


def test_s5_job_matrix(tmp_path):
    args = S5.parse_args(["--study-config", "c.json", "--output-dir", str(tmp_path), "--particles", "200", "1000",
                          "--turns", "100", "500", "2000", "--seeds", "42", "123", "777"])
    jobs = S5.build_jobs(args, InjectionStudyConfig(), ROOT, tmp_path, None)
    kinds = [j["kind"] for j in jobs]
    assert kinds.count("da_x_delta") == 7 and kinds.count("da_x_xp") == 13
    inj = [j for j in jobs if j["kind"] == "injection"]
    # 4 models x 2 backends, fieldmap with 3 seeds -> 2*(3+1+1+1) = 12, +1 particle conv, +1 turn conv, +1 chamber
    assert len(inj) == 15
    assert {j["label"] for j in jobs if j["kind"] == "stored_paired"} == {"stored_fieldmap", "stored_off", "stored_uniform_1urad"}
