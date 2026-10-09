#!/usr/bin/env python3
"""Task 006 — Pool S7 capture ensembles and rank error sources against per-realization capture.

Reads one or more ``capture_robustness_raw.json`` files (independent seeds) and reports:
* pooled per-realization capture statistics (realization = resampling unit, cluster bootstrap);
* seed-to-seed comparison of the mean capture;
* Spearman rank correlation between capture and each sampled error (absolute value for symmetric
  errors) and the BTS-exit centroid angle/position, with permutation-free asymptotic p-values.
Units: m, rad (reported mm, mrad); capture as a fraction.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import stats

SCALARS = ("booster_x_m", "booster_xp_rad", "energy_dp_p", "beta_mismatch_x", "beta_mismatch_y", "nkm_scale_err",
           "nkm_dx_m", "nkm_timing_mrad", "ring_co_x_m", "septum_x_m", "dipole_b_err")
VECTORS = ("quad_k_err", "quad_dx_m", "quad_dy_m", "quad_roll_rad")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--raw", nargs="+", type=Path, required=True)
    p.add_argument("--model", default="fieldmap")
    p.add_argument("--stored-model", default=None,
                   help="Kick model for the bicubic stored-beam recompute (default: --model; use fieldmap for fieldmap_thick)")
    p.add_argument("--bootstrap-count", type=int, default=10000)
    p.add_argument("--bootstrap-seed", type=int, default=1729)
    p.add_argument("--threshold", type=float, default=0.9)
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    p.add_argument("--stored-samples", type=int, default=20000,
                   help="Equilibrium sample size for the recomputed (bicubic) stored-beam response")
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(argv)
    if a.output.exists():
        raise SystemExit("Output exists; choose a new path")
    rows, per_seed, inputs, stored = [], {}, {}, []
    from dataclasses import replace
    import tempfile
    from nkm_injection.injection_study import InjectionStudyConfig, KickModelEvaluator, prepare_ring, stored_beam_response
    from nkm_injection.kickmap import NKMKickMap2D
    tmp = tempfile.TemporaryDirectory()
    ring_cache = {}
    for path in a.raw:
        raw = path.read_bytes()
        inputs[str(path)] = hashlib.sha256(raw).hexdigest()
        d = json.loads(raw)
        seed = d["cli"]["seed"]
        samples = {}
        from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble
        err = ErrorBudgetConfig.from_dict(d["error_config"])
        for s in sample_error_ensemble(err, d["cli"]["samples"], seed):
            samples[s["sample_id"]] = s
        caps = []
        for r in d["realizations"]:
            if r["sample_id"] < 0 or a.model not in r["models"]:
                continue
            s = samples[r["sample_id"]]
            feat = {k: abs(s[k]) * d["error_scale"] for k in SCALARS}
            for k in VECTORS:
                feat[f"rms_{k}"] = float(np.sqrt(np.mean(np.square(s[k])))) * d["error_scale"]
            ex = r["bts_exit"]
            feat["abs_exit_centroid_x_m"] = abs(ex.get("centroid_x_m", np.nan))
            feat["abs_exit_centroid_xp_rad"] = abs(ex.get("centroid_xp_rad", np.nan))
            feat["exit_mismatch_x"] = r["bts_exit_mismatch"].get("mismatch_x", np.nan)
            c = r["models"][a.model]["capture_fraction"]
            rows.append((c, feat)); caps.append(c)
            # Recompute the stored-beam response with the bicubic map (same configuration logic as S7).
            cfg0 = InjectionStudyConfig.from_dict(d["study_config"])
            if "ring" not in ring_cache:
                ring_cache["ring"] = prepare_ring(cfg0, a.repo_root, Path(tmp.name))
                ring_cache["kmap"] = NKMKickMap2D(a.repo_root / cfg0.kickmap_path)
            sc = d["error_scale"]
            cfg = replace(cfg0, field_scale=cfg0.field_scale * (1 + sc * s["nkm_scale_err"]),
                          nkm_dx_m=cfg0.nkm_dx_m + sc * s["nkm_dx_m"],
                          kick_offset_rad=cfg0.kick_offset_rad + sc * s["nkm_timing_mrad"] * 1e-3,
                          closed_orbit_x_m=cfg0.closed_orbit_x_m + sc * s["ring_co_x_m"])
            kick = KickModelEvaluator(a.stored_model or a.model, cfg, ring_cache["kmap"], cfg0.nkm_entry_x_m)
            sr = stored_beam_response(cfg, ring_cache["ring"], kick, n=a.stored_samples, seed=11, interpolation="cubic")
            stored.append({"seed": seed, "sample_id": r["sample_id"], "amplitude_over_sigma_cubic": sr["amplitude_over_sigma"],
                           "amplitude_over_sigma_linear_recorded": r["models"][a.model].get("stored", {}).get("amplitude_over_sigma"),
                           "filamented_emittance_growth_cubic": sr["filamented_emittance_growth"],
                           "magnet_frame_offset_m": cfg.closed_orbit_x_m - cfg.nkm_dx_m})
        per_seed[str(seed)] = {"n": len(caps), "mean": float(np.mean(caps)), "median": float(np.median(caps)),
                               "error_scale": d["error_scale"]}
    cap = np.array([r[0] for r in rows])
    rng = np.random.default_rng(a.bootstrap_seed)
    boot = cap[rng.integers(0, len(cap), size=(a.bootstrap_count, len(cap)))].mean(axis=1)
    k = int(np.sum(cap >= a.threshold))
    ranking = []
    for name in rows[0][1]:
        x = np.array([r[1][name] for r in rows], float)
        ok = np.isfinite(x)
        if np.ptp(x[ok]) == 0:
            continue
        rho, pv = stats.spearmanr(x[ok], cap[ok])
        ranking.append({"variable": name, "spearman_rho": float(rho), "p_value": float(pv)})
    ranking.sort(key=lambda r: r["spearman_rho"])
    out = {"inputs_sha256": inputs, "model": a.model, "stored_model": a.stored_model or a.model, "n_realizations": int(len(cap)),
           "pooled": {"mean": float(cap.mean()), "mean_ci95": [float(np.quantile(boot, .025)), float(np.quantile(boot, .975))],
                      "median": float(np.median(cap)), "p05": float(np.quantile(cap, .05)), "min": float(cap.min()),
                      "fraction_above_threshold": k / len(cap), "threshold": a.threshold},
           "per_seed": per_seed, "spearman_ranking": ranking,
           "stored_beam_cubic": {
               "amplitude_over_sigma": {q: float(np.quantile([x["amplitude_over_sigma_cubic"] for x in stored], v))
                                        for q, v in (("median", .5), ("p95", .95), ("max", 1.0))},
               "amplitude_over_sigma_linear_recorded": {q: float(np.quantile([x["amplitude_over_sigma_linear_recorded"] for x in stored
                                                                             if x["amplitude_over_sigma_linear_recorded"] is not None], v))
                                                        for q, v in (("median", .5), ("p95", .95), ("max", 1.0))} if any(
                   x["amplitude_over_sigma_linear_recorded"] is not None for x in stored) else None,
               "emittance_growth": {q: float(np.quantile([x["filamented_emittance_growth_cubic"] for x in stored], v))
                                    for q, v in (("median", .5), ("p95", .95), ("max", 1.0))},
               "per_realization": stored},
           "note": "Negative rho: larger error magnitude associated with lower capture. Correlation is not causation; errors are sampled independently."}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"pooled": out["pooled"], "per_seed": per_seed, "top": ranking[:5],
                      "stored": {k: v for k, v in out["stored_beam_cubic"].items() if k != "per_realization"}}, indent=1))


if __name__ == "__main__":
    main()
