#!/usr/bin/env python3
"""S7 — Combined-error injection capture robustness with coupled BTS tracking (Task 006).

For each error realization (ErrorBudgetConfig, fixed seed) the booster beam is perturbed
(centroid jitter, Twiss mismatch, emittance and energy-spread variation, mean energy offset),
tracked through the perturbed selected BTS (quadrupole gradient/offset/roll errors, dipole field
errors), placed at the septum (septum position error moves the blade and the injected centroid),
kicked by the NKM (field scale, alignment, additive timing kick error) and tracked natively for
n_turns around a ring with a closed-orbit offset at the NKM. All kick models of one realization
see the identical beam (paired). Out of scope: quadrupole longitudinal placement, power-supply
quantisation, ring optics errors (documented in physics_model.md section 7).

Energy errors are applied as a momentum offset of the tracked particles (chromatic tracking through
the nominal-field BTS), not by rescaling magnet strengths. Units: m, rad, eV, dimensionless delta.
Uncertainty: realizations are the resampling unit (cluster bootstrap); particles within a realization
are not treated as independent error samples.
"""
import argparse
import copy
import datetime
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from nkm_injection.concurrency import parallel_map
from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble, apply_sample_errors
from nkm_injection.injection_study import (
    InjectionStudyConfig, KickModelEvaluator, cached_ring, injected_beam_at_septum, track_injection,
    stored_beam_response, booster_beam, track_bts, beam_moments, wilson_interval, KICK_MODELS)
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.bts_lattice import BTSConfig
from nkm_injection.optics import compute_mismatch_metric
from nkm_injection.stage_cli import add_source_argument, source_root, input_hashes

REPO = Path(__file__).resolve().parent.parent


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True, help="Operating point (InjectionStudyConfig)")
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--error-config", type=Path, required=True)
    p.add_argument("--error-scale", type=float, default=1.0, help="Multiplies every error sigma (stress tests)")
    p.add_argument("--tracking-backend", choices=("element", "map"), default="element")
    p.add_argument("--kicker-models", nargs="+", choices=KICK_MODELS, default=["fieldmap", "dipole"])
    p.add_argument("--samples", type=int, default=50)
    p.add_argument("--particles", type=int, default=200)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--include-zero-error", action="store_true", help="Add realization -1 with all errors zero")
    p.add_argument("--correct-static-orbit", action="store_true",
                   help="Ideal steering at the septum exit: remove the static trajectory of the perturbed BTS "
                        "(reference particle on the design orbit); booster centroid/energy jitter are kept")
    p.add_argument("--bootstrap-count", type=int, default=10000)
    p.add_argument("--bootstrap-seed", type=int, default=1729)
    p.add_argument("--capture-threshold", type=float, default=0.9)
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--output-dir", type=Path, required=True)
    add_source_argument(p)
    return p.parse_args(argv)


def zero_sample(template):
    z = copy.deepcopy(template)
    for k, v in z.items():
        if k != "sample_id":
            z[k] = [0.0] * len(v) if isinstance(v, list) else 0.0
    z["sample_id"] = -1
    return z


def scale_sample(sample, factor):
    s = copy.deepcopy(sample)
    for k, v in s.items():
        if k != "sample_id":
            s[k] = [x * factor for x in v] if isinstance(v, list) else v * factor
    return s


def run_realization(job):
    t0 = time.perf_counter()
    cfg0 = InjectionStudyConfig.from_dict(job["config"])
    root = Path(job["repo_root"])
    ring = cached_ring(cfg0, root, Path(job["work_dir"]))
    kmap = NKMKickMap2D(root / cfg0.kickmap_path)
    s, extra = job["sample"], job["extra"]
    bts = BTSConfig.from_dict(job["bts_config"])
    optics_sample = dict(s, energy_dp_p=0.0)  # energy offset applied to the particles instead
    lattice, tw = apply_sample_errors(bts, optics_sample, initial_twiss=job["initial_twiss"])
    for elem in lattice:  # dipole field error: relative change of the bending field
        if hasattr(elem, "BendingAngle") and elem.Length > 0 and s["dipole_b_err"] != 0.0:
            pb = np.array(getattr(elem, "PolynomB", np.zeros(4)), dtype=float)
            pb[0] += s["dipole_b_err"] * elem.BendingAngle / elem.Length
            elem.PolynomB = pb
            elem.MaxOrder = max(int(getattr(elem, "MaxOrder", 0)), len(pb) - 1)
    beam_cfg = replace(cfg0.injected_beam,
                       emit_x_m_rad=cfg0.injected_beam.emit_x_m_rad * max(1e-3, 1 + extra["emit_rel"]),
                       emit_y_m_rad=cfg0.injected_beam.emit_y_m_rad * max(1e-3, 1 + extra["emit_rel"]),
                       energy_spread=max(1e-6, cfg0.injected_beam.energy_spread + extra["espread_abs"]))
    centroid = np.array([s["booster_x_m"], s["booster_xp_rad"], 0.0, 0.0, s["energy_dp_p"], 0.0])
    exit_beam = track_bts(lattice, booster_beam(tw, beam_cfg, job["particles"], job["beam_seed"], centroid=centroid))
    static = None
    if job.get("correct_static_orbit"):
        ref = track_bts(lattice, np.zeros((6, 1)))  # static trajectory of the perturbed line (no jitter)
        static = [float(ref[0, 0]), float(ref[1, 0])]
        exit_beam[0] -= ref[0, 0]
        exit_beam[1] -= ref[1, 0]
    exit_mom = beam_moments(exit_beam)
    cfg = replace(cfg0,
                  septum_edge_x_m=cfg0.septum_edge_x_m + s["septum_x_m"],
                  injection_x_m=cfg0.injection_x_m + s["septum_x_m"],
                  field_scale=cfg0.field_scale * (1 + s["nkm_scale_err"]),
                  nkm_dx_m=cfg0.nkm_dx_m + s["nkm_dx_m"],
                  kick_offset_rad=cfg0.kick_offset_rad + s["nkm_timing_mrad"] * 1e-3,
                  closed_orbit_x_m=cfg0.closed_orbit_x_m + s["ring_co_x_m"])
    beam = injected_beam_at_septum(cfg, ring, job["beam_seed"], bts_exit_beam=exit_beam)
    tgt = job["target_twiss"]
    mism = {}
    if exit_mom.get("beta_x_m"):
        mism = {"mismatch_x": compute_mismatch_metric(exit_mom["beta_x_m"], exit_mom["alpha_x"], tgt["beta"][0], tgt["alpha"][0]),
                "mismatch_y": compute_mismatch_metric(exit_mom["beta_y_m"], exit_mom["alpha_y"], tgt["beta"][1], tgt["alpha"][1])}
    out = {"sample_id": s["sample_id"], "beam_seed": job["beam_seed"], "bts_exit": exit_mom, "bts_exit_mismatch": mism,
           "static_orbit_corrected_m_rad": static,
           "bts_lost": int(np.sum(~np.isfinite(exit_beam[0]))), "models": {}}
    x_ref = cfg0.nkm_entry_x_m  # controls stay calibrated at the nominal point (no error knowledge)
    for model in job["models"]:
        kicker = KickModelEvaluator(model, cfg, None if model == "off" else kmap, x_ref)
        res = track_injection(cfg, ring, kicker, beam, job["backend"], n_turns=job["turns"])
        entry = {"captured": res["captured"], "n": res["n_particles"], "capture_fraction": res["capture_fraction"],
                 "loss_causes": res["loss_causes"],
                 "loss_turn_histogram": np.bincount(np.asarray([t for t in res["first_loss_turn"] if t >= 0], int),
                                                    minlength=1).tolist()}
        if model != "off":
            sr = stored_beam_response(cfg, ring, kicker, n=20000, seed=11)
            entry["stored"] = {k: sr[k] for k in ("mean_kick_x_rad", "centroid_amplitude_m", "amplitude_over_sigma",
                                                  "filamented_emittance_growth")}
        out["models"][model] = entry
    out["runtime_s"] = time.perf_counter() - t0
    return out


def cluster_stats(values, seed, count, threshold):
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boot = v[rng.integers(0, len(v), size=(count, len(v)))].mean(axis=1)
    k = int(np.sum(v >= threshold))
    return {"n_realizations": int(len(v)), "mean_capture": float(v.mean()), "median_capture": float(np.median(v)),
            "min_capture": float(v.min()), "p05_capture": float(np.quantile(v, 0.05)),
            "mean_ci95_cluster_bootstrap": [float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))],
            "fraction_realizations_above_threshold": k / len(v), "threshold": threshold,
            "fraction_above_wilson95": list(wilson_interval(k, len(v)))}


def main(argv=None):
    args = parse_args(argv)
    root = source_root(args, REPO)
    out = args.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    cfg = InjectionStudyConfig.load(args.study_config)
    cfg.validate()
    sel = load_optimization_handoff(args.optimization_summary)
    err = ErrorBudgetConfig.load(args.error_config)
    samples = [scale_sample(x, args.error_scale) for x in sample_error_ensemble(err, args.samples, args.seed)]
    rng_extra = np.random.default_rng([args.seed, 9001])  # separate stream: emittance / energy-spread variation
    extras = [{"emit_rel": float(rng_extra.normal(0, err.emittance_rel_std * args.error_scale)),
               "espread_abs": float(rng_extra.normal(0, err.espread_std * args.error_scale))} for _ in samples]
    if args.include_zero_error:
        samples.insert(0, zero_sample(samples[0]))
        extras.insert(0, {"emit_rel": 0.0, "espread_abs": 0.0})
    out.mkdir(parents=True)
    work = out / "_lattice"
    cached_ring(cfg, root, work)
    base = {"config": cfg.to_dict(), "repo_root": str(root), "work_dir": str(work), "bts_config": sel.bts.to_dict(),
            "initial_twiss": sel.initial_twiss, "target_twiss": sel.target_twiss, "models": args.kicker_models,
            "backend": args.tracking_backend, "particles": args.particles, "turns": args.turns,
            "correct_static_orbit": args.correct_static_orbit}
    jobs = [{**base, "sample": s, "extra": e, "beam_seed": int(args.seed * 100003 + max(s["sample_id"], -1) + 1)}
            for s, e in zip(samples, extras)]
    print(f"S7: {len(jobs)} realizations x {len(args.kicker_models)} models, workers={args.workers}", flush=True)
    t0 = time.time()
    results = parallel_map(run_realization, jobs, n_workers=args.workers, desc="S7 capture robustness")
    stats_by_model = {}
    for m in args.kicker_models:
        caps = [r["models"][m]["capture_fraction"] for r in results if r["sample_id"] >= 0]
        st = cluster_stats(caps, args.bootstrap_seed, args.bootstrap_count, args.capture_threshold)
        st["pooled_particles_capture"] = float(sum(r["models"][m]["captured"] for r in results if r["sample_id"] >= 0)
                                               / sum(r["models"][m]["n"] for r in results if r["sample_id"] >= 0))
        if m != "off":
            amp = [r["models"][m]["stored"]["amplitude_over_sigma"] for r in results if r["sample_id"] >= 0]
            st["stored_amp_over_sigma"] = {"median": float(np.median(amp)), "p95": float(np.quantile(amp, 0.95)),
                                           "max": float(np.max(amp))}
        stats_by_model[m] = st
    paired = None
    if "fieldmap" in args.kicker_models and "dipole" in args.kicker_models:
        d = np.array([r["models"]["fieldmap"]["capture_fraction"] - r["models"]["dipole"]["capture_fraction"]
                      for r in results if r["sample_id"] >= 0])
        rng = np.random.default_rng(args.bootstrap_seed)
        boot = d[rng.integers(0, len(d), size=(args.bootstrap_count, len(d)))].mean(axis=1)
        paired = {"mean_difference_fieldmap_minus_dipole": float(d.mean()),
                  "ci95": [float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))]}
    meta = {"timestamp": datetime.datetime.now().isoformat(), "study_config": cfg.to_dict(),
            "error_config": err.to_dict(), "error_scale": args.error_scale, "optimization_source": sel.source,
            "input_sha256": input_hashes(root, (cfg.ring_source, cfg.kickmap_path)),
            "cli": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
            "static_orbit_correction": "ideal steering at septum exit" if args.correct_static_orbit else None,
            "runtime_s": time.time() - t0, "out_of_scope_errors": ["quad_ds_std_m", "ps_quantization_std", "ring_beta_rel_std"],
            "resampling_unit": "error realization (cluster bootstrap); particle statistics within realizations"}
    zero = next((r for r in results if r["sample_id"] == -1), None)
    summary = {**meta, "statistics": stats_by_model, "paired_difference": paired,
               "zero_error_realization": None if zero is None else {m: zero["models"][m]["capture_fraction"] for m in args.kicker_models}}
    (out / "capture_robustness_raw.json").write_text(json.dumps({**meta, "realizations": results}, allow_nan=False) + "\n")
    (out / "capture_robustness_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"statistics": stats_by_model, "paired": paired, "zero": summary["zero_error_realization"]}, indent=1))
    print(f"Done in {time.time() - t0:.0f} s -> {out}")


if __name__ == "__main__":
    main()
