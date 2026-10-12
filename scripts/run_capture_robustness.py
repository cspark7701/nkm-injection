#!/usr/bin/env python3
"""S7 — Combined-error injection capture robustness with coupled BTS tracking (Task 006).

For each error realization (ErrorBudgetConfig, fixed seed) the booster beam is perturbed
(centroid jitter, Twiss mismatch, emittance and energy-spread variation, mean energy offset),
tracked through the perturbed selected BTS (quadrupole gradient/offset/roll errors, dipole field
errors), placed at the septum (septum position error moves the blade and the injected centroid),
kicked by the NKM (field scale, alignment, additive timing kick error) and tracked natively for
n_turns around a ring with a closed-orbit offset at the NKM. All kick models of one realization
see the identical beam (paired). Optional saved corrected-ring scenarios include distributed
ring errors. Out of scope: quadrupole longitudinal placement, power-supply quantisation,
and the independent scalar ring-beta error field.

Energy errors are applied as a momentum offset of the tracked particles (chromatic tracking through
the nominal-field BTS), not by rescaling magnet strengths. Units: m, rad, eV, dimensionless delta.
Uncertainty: realizations are the resampling unit (cluster bootstrap); particles within a realization
are not treated as independent error samples.
"""
import argparse
import copy
import datetime
import hashlib
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from nkm_injection.concurrency import parallel_map
from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble, apply_sample_errors
from nkm_injection.injection_study import (
    InjectionStudyConfig, KickModelEvaluator, cached_ring, injected_beam_at_septum, track_injection,
    stored_beam_response, booster_beam, track_bts, beam_moments, wilson_interval, KICK_MODELS, ThickNKMKicker)
from nkm_injection.fieldmap import load_1d_fieldmap
from nkm_injection.wire_field import CalibratedControl, FilamentNKMKicker, calibrate_controls
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.bts_lattice import BTSConfig
from nkm_injection.optics import compute_mismatch_metric
from nkm_injection.steering import subtract_static_horizontal_reference
from nkm_injection.injection_timing import apply_injection_shot_errors
from nkm_injection.chamber import ChamberProfile, apply_chamber
from nkm_injection.ring_error_scenario import refresh_prepared_ring
from nkm_injection.stage_cli import add_source_argument, source_root, input_hashes

REPO = Path(__file__).resolve().parent.parent
# "fieldmap_thick": drift-kick-drift NKM through the By.txt profile (Task 011 review); no stored-beam response
# is recorded for it (the transparency study uses the bicubic kick map).
# "fieldmap_3d": exact 3-D filament field (wire_field.FilamentNKMKicker), principal model after revision task C1.
S7_MODELS = tuple(KICK_MODELS) + ("fieldmap_thick", "fieldmap_3d")
NO_STORED = ("off", "fieldmap_thick", "fieldmap_3d")  # stored-beam response computed separately (task C7)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True, help="Operating point (InjectionStudyConfig)")
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--error-config", type=Path, required=True)
    p.add_argument("--error-scale", type=float, default=1.0, help="Multiplies every error sigma (stress tests)")
    p.add_argument("--tracking-backend", choices=("element", "map"), default="element")
    p.add_argument("--kicker-models", nargs="+", choices=S7_MODELS, default=["fieldmap", "dipole"])
    p.add_argument("--thick-slices", type=int, default=160, help="Slices for the fieldmap_thick model")
    p.add_argument("--slices-3d", type=int, default=640, help="Slices for the fieldmap_3d model")
    p.add_argument("--control-reference", choices=("thin", "3d"), default="thin",
                   help="Calibrate dipole/linear controls to the thin map (legacy) or to the 3-D response of the nominal centroid")
    p.add_argument("--timing-model", choices=("additive", "scale"), default="additive",
                   help="NKM timing error as an additive dipole kick (legacy) or as an equivalent field-scale error "
                        "(same kick change for the nominal injected centroid, zero on axis)")
    p.add_argument("--samples", type=int, default=50)
    p.add_argument("--particles", type=int, default=200)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--include-zero-error", action="store_true", help="Add realization -1 with all errors zero")
    p.add_argument("--correct-static-orbit", action="store_true",
                   help="Ideal steering at the septum exit: remove the static trajectory of the perturbed BTS "
                        "(reference particle on the design orbit); booster centroid/energy jitter are kept")
    p.add_argument("--septum-angle-mrad", type=float, default=10.)
    p.add_argument("--rf-frequency-hz", type=float, default=499593472.8240743)
    p.add_argument("--pulse-duration-us", type=float, default=5.3)
    p.add_argument("--chamber-config", type=Path, default=None)
    p.add_argument("--corrected-ring-dir", type=Path, default=None,
                   help="D5 scenario ensemble; draw a saved corrected ring independently for each realization")
    p.add_argument("--bootstrap-count", type=int, default=10000)
    p.add_argument("--bootstrap-seed", type=int, default=1729)
    p.add_argument("--capture-threshold", type=float, default=0.9)
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--resume", action="store_true", help="Resume only checkpoints with identical inputs and code")
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
    if job.get("corrected_ring_path") or job.get("chamber"):
        import at
        lattice=at.load_mat(job["corrected_ring_path"]) if job.get("corrected_ring_path") else ring.ring_c
        if job.get("chamber"):
            lattice,_=apply_chamber(lattice,ChamberProfile(**job["chamber"]),cfg0.septum_edge_x_m)
        ring=refresh_prepared_ring(ring,lattice)
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
        static = subtract_static_horizontal_reference(exit_beam, ref)
    exit_mom = beam_moments(exit_beam)
    # timing error: additive dipole kick (legacy) or the field-scale change giving the same kick change for the
    # nominal injected centroid, whose kick magnitude equals the matched angle |x'_inj| (zero on the stored-beam axis)
    timing_kick = s["nkm_timing_mrad"] * 1e-3
    if job.get("timing_model", "additive") == "scale":
        timing_rel, timing_add = timing_kick / abs(cfg0.injection_xp_rad), 0.0
    else:
        timing_rel, timing_add = 0.0, timing_kick
    cfg = replace(cfg0,
                  septum_edge_x_m=cfg0.septum_edge_x_m + s["septum_x_m"],
                  injection_x_m=cfg0.injection_x_m + s["septum_x_m"],
                  field_scale=cfg0.field_scale * (1 + s["nkm_scale_err"] + timing_rel),
                  nkm_dx_m=cfg0.nkm_dx_m + s["nkm_dx_m"],
                  kick_offset_rad=cfg0.kick_offset_rad + timing_add,
                  closed_orbit_x_m=cfg0.closed_orbit_x_m + s["ring_co_x_m"])
    if s["septum_x_m"] != 0.0:
        # Move the physical return aperture with the same blade displacement
        # used for beam creation. Do not mutate the cached nominal lattice.
        ring=replace(ring,ring_c=ring.ring_c.deepcopy())
        ring.ring_c[ring.septum_index].RApertures[0]=cfg.septum_edge_x_m
    beam = injected_beam_at_septum(cfg, ring, job["beam_seed"], bts_exit_beam=exit_beam)
    timing_scale = apply_injection_shot_errors(beam, s,
        septum_angle_rad=job.get("septum_angle_mrad", 10.)*1e-3,
        rf_frequency_hz=job.get("rf_frequency_hz", 499593472.8240743),
        pulse_duration_s=job.get("pulse_duration_us", 5.3)*1e-6)
    cfg = replace(cfg, field_scale=cfg.field_scale*timing_scale)
    tgt = job["target_twiss"]
    mism = {}
    if exit_mom.get("beta_x_m"):
        mism = {"mismatch_x": compute_mismatch_metric(exit_mom["beta_x_m"], exit_mom["alpha_x"], tgt["beta"][0], tgt["alpha"][0]),
                "mismatch_y": compute_mismatch_metric(exit_mom["beta_y_m"], exit_mom["alpha_y"], tgt["beta"][1], tgt["alpha"][1])}
    out = {"sample_id": s["sample_id"], "beam_seed": job["beam_seed"], "bts_exit": exit_mom, "bts_exit_mismatch": mism,
           "static_orbit_corrected_m_rad": static,
           "bts_lost": int(np.sum(~np.isfinite(exit_beam[0]))), "models": {}}
    out["ring_error_seed"]=job.get("ring_error_seed")
    x_ref = cfg0.nkm_entry_x_m  # controls stay calibrated at the nominal point (no error knowledge)
    calib = job.get("calibration_3d")
    for model in job["models"]:
        if model == "fieldmap_3d":
            kicker = FilamentNKMKicker(cfg, n_slices=job.get("slices_3d", 640))
        elif model in ("dipole", "linear") and calib is not None:
            relative_scale=cfg.field_scale/cfg0.field_scale
            kicker = CalibratedControl(model, calib[0]*relative_scale+cfg.kick_offset_rad,
                                       calib[1]*relative_scale, calib[2])
        elif model == "fieldmap_thick":
            kicker = ThickNKMKicker(cfg, *load_1d_fieldmap(root / "By.txt"), n_slices=job.get("thick_slices", 160))
        else:
            kicker = KickModelEvaluator(model, cfg, None if model == "off" else kmap, x_ref)
        res = track_injection(cfg, ring, kicker, beam, job["backend"], n_turns=job["turns"])
        entry = {"captured": res["captured"], "n": res["n_particles"], "capture_fraction": res["capture_fraction"],
                 "loss_causes": res["loss_causes"],
                 "loss_turn_histogram": np.bincount(np.asarray([t for t in res["first_loss_turn"] if t >= 0], int),
                                                    minlength=1).tolist()}
        if model not in NO_STORED:
            sr = stored_beam_response(cfg, ring, kicker, n=20000, seed=11)
            entry["stored"] = {k: sr[k] for k in ("mean_kick_x_rad", "centroid_amplitude_m", "amplitude_over_sigma",
                                                  "filamented_emittance_growth")}
        out["models"][model] = entry
    out["runtime_s"] = time.perf_counter() - t0
    if job.get("checkpoint"):
        path=Path(job["checkpoint"])
        temporary=path.with_suffix(".tmp")
        temporary.write_text(json.dumps(out, allow_nan=False)+"\n")
        temporary.replace(path)
    return out


def cluster_stats(values, seed, count, threshold):
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boot = v[rng.integers(0, len(v), size=(count, len(v)))].mean(axis=1)
    k = int(np.sum(v >= threshold))
    return {"n_realizations": int(len(v)), "mean_capture": float(v.mean()), "median_capture": float(np.median(v)),
            "min_capture": float(v.min()), "p05_capture": float(np.quantile(v, 0.05)),
            "p10_capture": float(np.quantile(v, 0.10)),
            "mean_ci95_cluster_bootstrap": [float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))],
            "fraction_realizations_above_threshold": k / len(v), "threshold": threshold,
            "fraction_above_wilson95": list(wilson_interval(k, len(v)))}


def main(argv=None):
    args = parse_args(argv)
    root = source_root(args, REPO)
    out = args.output_dir.resolve()
    if out.exists() and any(out.iterdir()) and not args.resume:
        raise SystemExit("--output-dir must be new or empty")
    cfg = InjectionStudyConfig.load(args.study_config)
    cfg.validate()
    sel = load_optimization_handoff(args.optimization_summary)
    err = ErrorBudgetConfig.load(args.error_config)
    samples = [scale_sample(x, args.error_scale) for x in sample_error_ensemble(err, args.samples, args.seed)]
    chamber=json.loads(args.chamber_config.read_text()) if args.chamber_config else None
    ring_seeds=None
    if args.corrected_ring_dir:
        ring_summary=json.loads((args.corrected_ring_dir/"corrected_ring_summary.json").read_text())
        if not ring_summary["passed"]:raise ValueError("D5 correction gate has not passed")
        ring_seeds=ring_summary["seeds"]
    rng_extra = np.random.default_rng([args.seed, 9001])  # separate stream: emittance / energy-spread variation
    extras = [{"emit_rel": float(rng_extra.normal(0, err.emittance_rel_std * args.error_scale)),
               "espread_abs": float(rng_extra.normal(0, err.espread_std * args.error_scale))} for _ in samples]
    if args.include_zero_error:
        samples.insert(0, zero_sample(samples[0]))
        extras.insert(0, {"emit_rel": 0.0, "espread_abs": 0.0})
    out.mkdir(parents=True, exist_ok=True)
    work = out / "_lattice"
    cached_ring(cfg, root, work)
    base = {"config": cfg.to_dict(), "repo_root": str(root), "work_dir": str(work), "bts_config": sel.bts.to_dict(),
            "initial_twiss": sel.initial_twiss, "target_twiss": sel.target_twiss, "models": args.kicker_models,
            "backend": args.tracking_backend, "thick_slices": args.thick_slices, "particles": args.particles, "turns": args.turns,
            "correct_static_orbit": args.correct_static_orbit, "slices_3d": args.slices_3d, "timing_model": args.timing_model,
            "calibration_3d": list(calibrate_controls(cfg, args.slices_3d)) if args.control_reference == "3d" else None,
            "septum_angle_mrad": args.septum_angle_mrad, "rf_frequency_hz": args.rf_frequency_hz,
            "pulse_duration_us": args.pulse_duration_us}
    base["chamber"]=chamber
    jobs = [{**base, "sample": s, "extra": e, "beam_seed": int(args.seed * 100003 + max(s["sample_id"], -1) + 1)}
            for s, e in zip(samples, extras)]
    if ring_seeds:
        for job in jobs:
            if job["sample"]["sample_id"]<0:continue  # zero-error reference uses the ideal ring
            ring_rng=np.random.default_rng([args.seed,5505,job["sample"]["sample_id"]])
            seed=int(ring_rng.choice(ring_seeds))
            job["ring_error_seed"]=seed
            job["corrected_ring_path"]=str(args.corrected_ring_dir/f"seed{seed}.mat")
    # Completed realizations survive interruption. Reject stale checkpoints
    # whenever an input, source module, or scientific option has changed.
    paths=[args.study_config,args.error_config,args.optimization_summary,
           args.optimization_summary.parent/"config.json",root/cfg.ring_source,root/cfg.kickmap_path]
    if args.chamber_config:paths.append(args.chamber_config)
    if ring_seeds:paths.extend(Path(j["corrected_ring_path"]) for j in jobs if "corrected_ring_path" in j)
    paths.extend((REPO/"src/nkm_injection").glob("*.py"))
    paths.append(Path(__file__))
    signature={"jobs":jobs,"hashes":{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
               "analysis":{"bootstrap_seed":args.bootstrap_seed,"bootstrap_count":args.bootstrap_count,
                           "capture_threshold":args.capture_threshold}}
    spec=out/"checkpoint_inputs.json"
    if spec.exists():
        if json.loads(spec.read_text())!=signature:raise SystemExit("Checkpoint inputs or code changed; use a new output directory")
    else:
        if args.resume and any(out.glob("realization_*.json")):raise SystemExit("Missing checkpoint input specification")
        spec.write_text(json.dumps(signature,indent=2,allow_nan=False)+"\n")
    completed=[];pending=[]
    for job in jobs:
        checkpoint=out/f"realization_{job['sample']['sample_id']}.json"
        job["checkpoint"]=str(checkpoint)
        if args.resume and checkpoint.exists():completed.append(json.loads(checkpoint.read_text()))
        else:pending.append(job)
    if not pending and (out/"capture_robustness_raw.json").exists() and (out/"capture_robustness_summary.json").exists():
        print(f"Validated completed ensemble -> {out}",flush=True)
        return
    print(f"S7: {len(jobs)} realizations x {len(args.kicker_models)} models, workers={args.workers}", flush=True)
    t0 = time.time()
    results = completed+parallel_map(run_realization, pending, n_workers=args.workers, desc="S7 capture robustness")
    results.sort(key=lambda r:r["sample_id"])
    stats_by_model = {}
    for m in args.kicker_models:
        caps = [r["models"][m]["capture_fraction"] for r in results if r["sample_id"] >= 0]
        st = cluster_stats(caps, args.bootstrap_seed, args.bootstrap_count, args.capture_threshold)
        st["pooled_particles_capture"] = float(sum(r["models"][m]["captured"] for r in results if r["sample_id"] >= 0)
                                               / sum(r["models"][m]["n"] for r in results if r["sample_id"] >= 0))
        if m not in NO_STORED:
            amp = [r["models"][m]["stored"]["amplitude_over_sigma"] for r in results if r["sample_id"] >= 0]
            st["stored_amp_over_sigma"] = {"median": float(np.median(amp)), "p95": float(np.quantile(amp, 0.95)),
                                           "max": float(np.max(amp))}
        stats_by_model[m] = st
    paired = None
    primary = args.kicker_models[0]
    if primary != "dipole" and "dipole" in args.kicker_models:
        d = np.array([r["models"][primary]["capture_fraction"] - r["models"]["dipole"]["capture_fraction"]
                      for r in results if r["sample_id"] >= 0])
        rng = np.random.default_rng(args.bootstrap_seed)
        boot = d[rng.integers(0, len(d), size=(args.bootstrap_count, len(d)))].mean(axis=1)
        paired = {"primary_model": primary, f"mean_difference_{primary}_minus_dipole": float(d.mean()),
                  "mean_difference_fieldmap_minus_dipole" if primary == "fieldmap" else "mean_difference_primary_minus_dipole": float(d.mean()),
                  "ci95": [float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))]}
    meta = {"timestamp": datetime.datetime.now().isoformat(), "study_config": cfg.to_dict(),
            "error_config": err.to_dict(), "error_scale": args.error_scale, "optimization_source": sel.source,
            "input_sha256": input_hashes(root, (cfg.ring_source, cfg.kickmap_path)),
            "cli": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
            "static_orbit_correction": "ideal steering at septum exit" if args.correct_static_orbit else None,
            "runtime_s": time.time() - t0, "out_of_scope_errors": ["quad_ds_std_m", "ps_quantization_std", "ring_beta_rel_std"],
            "resampling_unit": "error realization (cluster bootstrap); particle statistics within realizations"}
    meta["chamber"]=chamber
    meta["ring_population"]=ring_seeds
    meta["ring_resampling_scope"]="joint draws conditional on this finite saved ring population" if ring_seeds else "ideal ring"
    zero = next((r for r in results if r["sample_id"] == -1), None)
    summary = {**meta, "statistics": stats_by_model, "paired_difference": paired,
               "zero_error_realization": None if zero is None else {m: zero["models"][m]["capture_fraction"] for m in args.kicker_models}}
    (out / "capture_robustness_raw.json").write_text(json.dumps({**meta, "realizations": results}, allow_nan=False) + "\n")
    (out / "capture_robustness_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"statistics": stats_by_model, "paired": paired, "zero": summary["zero_error_realization"]}, indent=1))
    print(f"Done in {time.time() - t0:.0f} s -> {out}")


if __name__ == "__main__":
    main()
