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


S7 = _load("run_capture_robustness")


def test_s7_parser_and_sample_helpers():
    a = S7.parse_args(["--study-config", "c.json", "--optimization-summary", "o.json", "--error-config", "e.json",
                       "--output-dir", "x", "--samples", "100", "--particles", "2000", "--turns", "1000", "--seed", "123"])
    assert a.kicker_models == ["fieldmap", "dipole"] and a.samples == 100 and a.error_scale == 1.0
    from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble
    s = sample_error_ensemble(ErrorBudgetConfig(), 1, 3)[0]
    z = S7.zero_sample(s)
    assert z["sample_id"] == -1 and all((v == 0.0) or (isinstance(v, list) and not any(v))
                                        for k, v in z.items() if k != "sample_id")
    d = S7.scale_sample(s, 3.0)
    assert d["booster_x_m"] == pytest.approx(3 * s["booster_x_m"]) and d["quad_k_err"][0] == pytest.approx(3 * s["quad_k_err"][0])


def test_s7_cluster_statistics():
    st = S7.cluster_stats([1.0, 0.95, 0.85, 1.0], seed=1, count=500, threshold=0.9)
    assert st["mean_capture"] == pytest.approx(0.95) and st["fraction_realizations_above_threshold"] == 0.75
    lo, hi = st["mean_ci95_cluster_bootstrap"]
    assert 0.85 <= lo <= 0.95 <= hi <= 1.0


A7 = _load("analyze_capture_robustness")


def test_s7_and_analysis_end_to_end(tmp_path):
    """Tiny real S7 run (2 realizations + zero-error, 8 particles, 3 turns) and its pooled analysis."""
    from nkm_injection.errors import ErrorBudgetConfig
    err = tmp_path / "err.json"
    ErrorBudgetConfig().save(err)
    out = tmp_path / "s7"
    S7.main(["--study-config", str(ROOT / "config/injection_study_v1.json"),
             "--optimization-summary", str(ROOT / "tests/fixtures/s7_optimization/bts_optimization_summary.json"),
             "--error-config", str(err), "--samples", "2", "--particles", "8", "--turns", "3",
             "--include-zero-error", "--bootstrap-count", "50", "--workers", "1", "--repo-root", str(ROOT),
             "--output-dir", str(out)])
    summary = json.loads((out / "capture_robustness_summary.json").read_text())
    assert summary["statistics"]["fieldmap"]["n_realizations"] == 2
    assert summary["zero_error_realization"]["fieldmap"] is not None
    res = tmp_path / "analysis.json"
    A7.main(["--raw", str(out / "capture_robustness_raw.json"), "--bootstrap-count", "50", "--stored-samples", "2000",
             "--repo-root", str(ROOT), "--output", str(res)])
    a = json.loads(res.read_text())
    assert a["n_realizations"] == 2 and len(a["stored_beam_cubic"]["per_realization"]) == 2
    assert all(np.isfinite(r["amplitude_over_sigma_cubic"]) for r in a["stored_beam_cubic"]["per_realization"])
    with pytest.raises(SystemExit):
        A7.main(["--raw", str(out / "capture_robustness_raw.json"), "--output", str(res)])  # never overwrite
