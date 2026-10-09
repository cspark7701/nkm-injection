#!/usr/bin/env python3
"""Empirical effective-coverage audit of ErrorBudgetConfig (Task 002).

Each sampled field is set to +3 sigma alone (others zero) in the selected optimized
BTS configuration; the tolerance-study observables are recomputed through the same
code path (apply_sample_errors -> compute_twiss_propagation -> mismatch; stored kick).
A field is 'effective' for an observable if it changes it by more than 1e-12.
Units: m, rad, dimensionless mismatch; stored kick in mrad.
"""
import json, sys, copy
from dataclasses import fields
from pathlib import Path
import numpy as np
from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble, apply_sample_errors
from nkm_injection.optics import compute_twiss_propagation, compute_mismatch_metric
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.kickmap import NKMKickMap2D

import argparse
ap = argparse.ArgumentParser(description="Audit effective ErrorBudgetConfig coverage (+3 sigma, one at a time)")
ap.add_argument("--repo-root", type=Path, required=True)
ap.add_argument("--source-run", type=Path, required=True, help="Run containing optimization/bts_optimization_summary.json")
ap.add_argument("--error-config", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True, help="New JSON output path")
args = ap.parse_args()
root, src = args.repo_root, args.source_run
if args.output.exists():
    raise SystemExit("Output exists; choose a new path")
sel = load_optimization_handoff(src / "optimization/bts_optimization_summary.json")
cfg = ErrorBudgetConfig.from_dict(json.loads(args.error_config.read_text()))
kmap = NKMKickMap2D(root / "kickmap_file.txt")
zero = sample_error_ensemble(cfg, 1, 0)[0]
for k, v in zero.items():
    if k != "sample_id":
        zero[k] = [0.0] * len(v) if isinstance(v, list) else 0.0

def observe(sample):
    lat, tw = apply_sample_errors(sel.bts, sample, initial_twiss=sel.initial_twiss)
    p = compute_twiss_propagation(lat, tw)
    t = sel.target_twiss
    mx = compute_mismatch_metric(p["final_beta"][0], p["final_alpha"][0], t["beta"][0], t["alpha"][0])
    my = compute_mismatch_metric(p["final_beta"][1], p["final_alpha"][1], t["beta"][1], t["alpha"][1])
    net = sample["ring_co_x_m"] - sample["nkm_dx_m"]
    kick = abs(kmap.evaluate_kicks(np.array([net]))[0][0]) * (1 + sample["nkm_scale_err"]) * 1e3
    return {"mismatch_x": mx, "mismatch_y": my, "max_beta_x": p["max_beta_x"], "max_beta_y": p["max_beta_y"],
            "stored_kick_mrad": float(kick)}

ref = observe(zero)
sample_map = {  # sampled key -> ErrorBudgetConfig sigma field
    "quad_k_err": "quad_k_rel_std", "dipole_b_err": "dipole_b_rel_std", "booster_x_m": "booster_x_jitter_std_m",
    "booster_xp_rad": "booster_xp_jitter_std_rad", "quad_dx_m": "quad_dx_std_m", "quad_dy_m": "quad_dy_std_m",
    "quad_roll_rad": "quad_roll_std_rad", "quad_ds_m": "quad_ds_std_m", "energy_dp_p": "energy_dp_p_std",
    "beta_mismatch_x": "beta_mismatch_rel_std", "beta_mismatch_y": "beta_mismatch_rel_std",
    "nkm_scale_err": "nkm_scale_std", "nkm_dx_m": "nkm_dx_std_m", "nkm_timing_mrad": "nkm_timing_std_mrad",
    "ring_co_x_m": "ring_co_x_std_m", "septum_x_m": "septum_x_std_m"}
rows = []
for key, sig_name in sample_map.items():
    s = copy.deepcopy(zero); sig = getattr(cfg, sig_name)
    s[key] = [3 * sig] * len(zero[key]) if isinstance(zero[key], list) else 3 * sig
    obs = observe(s)
    eff = {k: bool(abs(obs[k] - ref[k]) > 1e-12) for k in obs}
    rows.append({"sample_key": key, "config_field": sig_name, "sigma": sig, "perturbation": "+3 sigma",
                 "effective_on": [k for k, e in eff.items() if e],
                 "delta": {k: obs[k] - ref[k] for k in obs}})
sampled = set(sample_map.values())
unsampled = [f.name for f in fields(ErrorBudgetConfig) if f.name not in sampled]
out = {"reference": ref, "rows": rows, "config_fields_never_sampled": unsampled,
       "capture_observable_in_tolerance_study": False}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(out, indent=2) + "\n")
for r in rows: print(f"{r['sample_key']:18s} {r['config_field']:26s} -> {r['effective_on']}")
print("never sampled:", unsampled)
