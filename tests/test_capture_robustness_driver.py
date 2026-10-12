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


def test_s7_and_analysis_end_to_end(tmp_path, monkeypatch):
    """Tiny real S7 run (2 realizations + zero-error, 8 particles, 3 turns) and its pooled analysis."""
    from nkm_injection.errors import ErrorBudgetConfig
    err = tmp_path / "err.json"
    ErrorBudgetConfig().save(err)
    out = tmp_path / "s7"
    argv=["--study-config", str(ROOT / "config/injection_study_v1.json"),
             "--optimization-summary", str(ROOT / "tests/fixtures/s7_optimization/bts_optimization_summary.json"),
             "--error-config", str(err), "--samples", "2", "--particles", "8", "--turns", "3",
             "--include-zero-error", "--bootstrap-count", "50", "--workers", "1", "--repo-root", str(ROOT),
             "--output-dir", str(out)]
    S7.main(argv)
    summary = json.loads((out / "capture_robustness_summary.json").read_text())
    assert summary["statistics"]["fieldmap"]["n_realizations"] == 2
    assert summary["zero_error_realization"]["fieldmap"] is not None
    def unexpected_rerun(job):
        raise AssertionError("Completed realizations must be read from checkpoints")
    monkeypatch.setattr(S7,"run_realization",unexpected_rerun)
    S7.main(argv+["--resume"])
    resumed=json.loads((out/"capture_robustness_summary.json").read_text())
    assert resumed["statistics"]==summary["statistics"]
    raw=json.loads((out/"capture_robustness_raw.json").read_text())
    for row in raw["realizations"]:
        for model in row["models"].values():
            causes=model["loss_causes"]
            assert model["captured"]+sum(causes[k] for k in
                ("upstream","septum_creation","injection_segment","outside_field_map","ring"))==model["n"]
    res = tmp_path / "analysis.json"
    A7.main(["--raw", str(out / "capture_robustness_raw.json"), "--bootstrap-count", "50", "--stored-samples", "2000",
             "--repo-root", str(ROOT), "--output", str(res)])
    a = json.loads(res.read_text())
    assert a["n_realizations"] == 2 and len(a["stored_beam_cubic"]["per_realization"]) == 2
    assert all(np.isfinite(r["amplitude_over_sigma_cubic"]) for r in a["stored_beam_cubic"]["per_realization"])
    with pytest.raises(SystemExit):
        A7.main(["--raw", str(out / "capture_robustness_raw.json"), "--output", str(res)])  # never overwrite


def test_s7_accepts_thick_model():
    a = S7.parse_args(["--study-config", "c.json", "--optimization-summary", "o.json", "--error-config", "e.json",
                       "--output-dir", "out", "--kicker-models", "fieldmap_thick", "--thick-slices", "80"])
    assert a.kicker_models == ["fieldmap_thick"] and a.thick_slices == 80
    assert "fieldmap_thick" in S7.S7_MODELS and set(S7.S7_MODELS) > {"off", "fieldmap", "dipole", "linear"}


def test_s7_revision_options():
    a = S7.parse_args(["--study-config", "c.json", "--optimization-summary", "o.json", "--error-config", "e.json",
                       "--output-dir", "out", "--kicker-models", "fieldmap_3d", "dipole", "--control-reference", "3d",
                       "--timing-model", "scale", "--slices-3d", "320"])
    assert a.kicker_models == ["fieldmap_3d", "dipole"] and a.control_reference == "3d" and a.timing_model == "scale"
    assert "fieldmap_3d" in S7.NO_STORED


def test_partial_spearman_separates_confounded_driver():
    """y depends on x1 only; x2 is correlated with x1 and x3 is independent noise."""
    mod = _load("analyze_capture_robustness")
    rng = np.random.default_rng(3)
    x1 = rng.normal(size=400)
    x2 = x1 + 0.5 * rng.normal(size=400)
    x3 = rng.normal(size=400)
    y = -x1 + 0.3 * rng.normal(size=400)
    res = {r["variable"]: r for r in mod.partial_spearman({"x1": x1, "x2": x2, "x3": x3}, y)}
    assert res["x1"]["partial_spearman_rho"] < -0.8 and res["x1"]["p_value"] < 1e-10
    assert abs(res["x2"]["partial_spearman_rho"]) < 0.15
    assert abs(res["x3"]["partial_spearman_rho"]) < 0.15
