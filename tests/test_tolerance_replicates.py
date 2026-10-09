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


T5 = _load("analyze_tolerance_replicates")


def test_tolerance_postprocessing_bounds():
    x = np.sort(np.random.default_rng(0).normal(size=20001))
    lo, hi = T5.order_statistic_ci(x, 0.5, 0.95)
    assert lo < np.median(x) < hi and hi - lo < 0.05
    fb = T5.failure_bounds(0, 20000)
    assert fb["one_sided_95_upper_zero_failure"] == pytest.approx(1 - 0.05 ** (1 / 20000))
    assert fb["clopper_pearson"][0] == 0.0 and 1e-4 < fb["clopper_pearson"][1] < 2e-4
