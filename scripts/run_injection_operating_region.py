#!/usr/bin/env python3
"""S6 — Calibrated-control injection operating region with coupled BTS handoff (Task 004).

The injected bunch is tracked from the booster extraction point through the selected
(optimised) BTS — or the baseline BTS for comparison — and placed at the septum exit with
centroid (x_inj, x'_inj). x'_inj = x'_match(x_inj) + offset, where x'_match is the angle for
which the NKM kick at the nominal centroid cancels the incoming angle at the NKM centre
(paraxial, delta = 0) at that grid point's field scale. All kick models in one grid point receive the identical
beam (paired). Controls 'dipole' and 'linear' are calibrated to the field-map kick at the
nominal centroid of that point. Capture = alive after n_turns of native tracking.

Units: m, rad, eV (CLI positions in mm and angles in mrad, converted on input).
"""
import argparse
import datetime
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import (
    InjectionStudyConfig, KickModelEvaluator, cached_ring, injected_beam_at_septum, track_injection,
    stored_beam_response, booster_beam, track_bts, beam_moments, wilson_interval, KICK_MODELS)
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optimization_handoff import load_optimization_handoff, reference_handoff
from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.stage_cli import add_source_argument, source_root, input_hashes

REPO = Path(__file__).resolve().parent.parent
NKM_HALF_LENGTH_M = 0.2625


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--tracking-backend", choices=("element", "map"), default="element")
    p.add_argument("--kicker-models", nargs="+", choices=KICK_MODELS, default=list(KICK_MODELS))
    p.add_argument("--x-offset-mm", nargs="+", type=float, default=[-22, -21, -20, -19.5],
                   help="Injected centroid at the septum exit")
    p.add_argument("--xp-offset-mrad", nargs="+", type=float, default=[-0.5, 0.0, 0.5],
                   help="Offset from the angle-matched injection angle")
    p.add_argument("--field-scale", nargs="+", type=float, default=[0.85, 0.9, 0.95, 1.0, 1.05, 1.1])
    p.add_argument("--particles", type=int, default=200)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 777])
    p.add_argument("--replicate-x-mm", type=float, default=-20.0, help="x_inj for seed replicates and BTS comparison")
    p.add_argument("--replicate-scale", type=float, default=1.0, help="Field scale for seed replicates and BTS comparison")
    p.add_argument("--replicate-offset-mrad", type=float, default=0.0)
    p.add_argument("--max-centroid-mm", type=float, default=12.0,
                   help="Skip grid points whose matched centroid at the NKM centre lies beyond this |x| (outside the DA)")
    p.add_argument("--stages", nargs="+", choices=("grid", "replicate"), default=["grid", "replicate"])
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--output-dir", type=Path, required=True)
    add_source_argument(p)
    return p.parse_args(argv)


def matched_angle(cfg, kmap, x_inj, scale=1.0):
    """Incoming angle x' (rad) at the septum for which x' + S*kick(x_c) = 0 at the NKM centre.

    Returns the inner root (largest angle); None if no root exists for 0 <= x' <= 15 mrad."""
    lever = cfg.septum_to_nkm_drift_m + NKM_HALF_LENGTH_M
    gain = cfg.kicker_polarity * scale

    def f(xp):
        xc = x_inj + lever * xp
        return xp + gain * kmap.evaluate_kicks(np.array([xc - cfg.nkm_dx_m]), np.array([0.0]))[0][0]
    grid = np.linspace(0.0, 0.015, 301)
    vals = [f(v) for v in grid]
    roots = [brentq(f, grid[i], grid[i + 1]) for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    return max(roots) if roots else None  # inner solution: centroid closest to the stored-beam axis


def centroid_amplitude(ring, cfg, kick_fn):
    """Linear CS amplitude (m) at the NKM centre of the nominal centroid after the kick."""
    lever = cfg.septum_to_nkm_drift_m + NKM_HALF_LENGTH_M
    xc = cfg.injection_x_m + lever * cfg.injection_xp_rad
    xp = cfg.injection_xp_rad + kick_fn(xc)
    beta, alpha = ring.twiss_x
    gamma = (1 + alpha ** 2) / beta
    j = gamma * xc ** 2 + 2 * alpha * xc * xp + beta * xp ** 2
    return float(np.sqrt(beta * j)), float(xc), float(xp)


def run_point(job):
    t0 = time.perf_counter()
    cfg = InjectionStudyConfig.from_dict(job["config"])
    root = Path(job["repo_root"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    kmap = NKMKickMap2D(root / cfg.kickmap_path)
    x_ref = cfg.nkm_entry_x_m
    lattice = create_bts_lattice(BTSConfig.from_dict(job["bts"]["bts_config"]))
    exit_beam = track_bts(lattice, booster_beam(job["bts"]["initial_twiss"], cfg.injected_beam, job["particles"], job["seed"]))
    beam = injected_beam_at_septum(cfg, ring, job["seed"], bts_exit_beam=exit_beam)
    bts_lost = int(np.sum(~np.isfinite(exit_beam[0])))
    out = {"label": job["label"], "group": job["group"], "bts": job["bts_label"], "seed": job["seed"],
           "x_inj_m": cfg.injection_x_m, "xp_inj_rad": cfg.injection_xp_rad, "xp_offset_rad": job["xp_offset_rad"],
           "field_scale": cfg.field_scale, "backend": job["backend"], "particles": job["particles"], "turns": job["turns"],
           "bts_lost": bts_lost, "injected_moments_at_septum": beam_moments(beam), "models": {}}
    for model in job["models"]:
        kicker = KickModelEvaluator(model, cfg, None if model == "off" else kmap, x_ref)
        res = track_injection(cfg, ring, kicker, beam, job["backend"], n_turns=job["turns"])
        lo, hi = wilson_interval(res["captured"], res["n_particles"])
        amp, xc, xpc = centroid_amplitude(ring, cfg, lambda x: kicker.kicks(np.array([x]), np.array([0.0]))[0][0])
        entry = {"captured": res["captured"], "n": res["n_particles"], "capture_fraction": res["capture_fraction"],
                 "capture_ci95": [lo, hi], "loss_causes": res["loss_causes"],
                 "alive_mask": res["alive_mask"], "first_loss_turn": res["first_loss_turn"],
                 "nominal_centroid_amplitude_after_kick_m": amp, "nominal_centroid_x_at_nkm_m": xc,
                 "nominal_centroid_xp_after_kick_rad": xpc}
        if model != "off":
            sr = stored_beam_response(cfg, ring, kicker, n=50000)
            entry["stored"] = {k: sr[k] for k in ("mean_kick_x_rad", "centroid_amplitude_m", "amplitude_over_sigma",
                                                  "filamented_emittance_growth", "rms_kick_spread_x_rad")}
        out["models"][model] = entry
    out["runtime_s"] = time.perf_counter() - t0
    return out


def build_jobs(args, cfg, kmap, root, work, bts_opt, bts_base):
    base = {"repo_root": str(root), "work_dir": str(work), "backend": args.tracking_backend,
            "particles": args.particles, "turns": args.turns}
    jobs, s0 = [], args.seeds[0]
    xmatch = {}

    lever = cfg.septum_to_nkm_drift_m + NKM_HALF_LENGTH_M
    skipped = []

    def matched(x_mm, scale):
        key = (x_mm, scale)
        if key not in xmatch:
            xmatch[key] = matched_angle(cfg, kmap, x_mm * 1e-3, scale)
        return xmatch[key]

    def inner(x_mm, scale):
        xm = matched(x_mm, scale)
        ok = xm is not None and abs(x_mm + lever * xm * 1e3) <= args.max_centroid_mm
        if not ok:
            skipped.append({"x_inj_mm": x_mm, "field_scale": scale, "matched_xp_rad": xm,
                            "reason": "no inner angle-matched solution within the dynamic aperture"})
        return ok

    def point(group, x_mm, off_mrad, scale, seed, models, bts, bts_label, backend=None):
        c = replace(cfg, injection_x_m=x_mm * 1e-3, injection_xp_rad=matched(x_mm, scale) + off_mrad * 1e-3,
                    field_scale=scale)
        return {**base, "group": group, "config": c.to_dict(), "seed": seed, "models": list(models), "bts": bts,
                "bts_label": bts_label, "xp_offset_rad": off_mrad * 1e-3, **({"backend": backend} if backend else {}),
                "label": f"{group}_{bts_label}_x{x_mm:g}_o{off_mrad:g}_s{scale:g}_seed{seed}"}
    if "grid" in args.stages:
        controls = [m for m in args.kicker_models if m != "fieldmap"]
        for x_mm in args.x_offset_mm:                  # 1. (x_inj, scale, angle-offset) map, paired controls at offset 0
            for sc in args.field_scale:
                if not inner(x_mm, sc):
                    continue
                for off in args.xp_offset_mrad:
                    models = (["fieldmap"] if "fieldmap" in args.kicker_models else []) + (controls if off == 0.0 else [])
                    jobs.append(point("map", x_mm, off, sc, s0, models, bts_opt, "optimized"))
                    if args.tracking_backend == "element":  # linearised cross-check, same beam
                        jobs.append(point("linmap", x_mm, off, sc, s0, ["fieldmap"], bts_opt, "optimized", backend="map"))
    if "replicate" in args.stages:
        x_r, s_r, o_r = args.replicate_x_mm, args.replicate_scale, args.replicate_offset_mrad
        for seed in args.seeds:                        # 2. independent beam replicates with paired controls
            jobs.append(point("replicate", x_r, o_r, s_r, seed, args.kicker_models, bts_opt, "optimized"))
            jobs.append(point("bts", x_r, o_r, s_r, seed, ["fieldmap"], bts_base, "baseline"))  # 3. baseline BTS
    build_jobs.skipped = skipped
    return jobs, {f"{k[0]:g}mm_scale{k[1]:g}": v for k, v in xmatch.items()}


def main(argv=None):
    args = parse_args(argv)
    root = source_root(args, REPO)
    out = args.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    if len(set(args.seeds)) != len(args.seeds):
        raise SystemExit("Seeds must be distinct")
    cfg = InjectionStudyConfig.load(args.study_config)
    cfg.validate()
    sel = load_optimization_handoff(args.optimization_summary)
    ref = reference_handoff()
    bts_opt = {"bts_config": sel.bts.to_dict(), "initial_twiss": sel.initial_twiss}
    bts_base = {"bts_config": ref.bts.to_dict(), "initial_twiss": ref.initial_twiss}
    kmap = NKMKickMap2D(root / cfg.kickmap_path)
    out.mkdir(parents=True)
    work = out / "_lattice"
    cached_ring(cfg, root, work)
    jobs, xmatch = build_jobs(args, cfg, kmap, root, work, bts_opt, bts_base)
    print(f"S6: {len(jobs)} points, workers={args.workers}", flush=True)
    t0 = time.time()
    results = parallel_map(run_point, jobs, n_workers=args.workers, desc="S6 operating region")
    meta = {"timestamp": datetime.datetime.now().isoformat(), "study_config": cfg.to_dict(),
            "optimization_source": sel.source, "baseline_bts": "BTSConfig() nominal strengths (reference mode)",
            "input_sha256": input_hashes(root, (cfg.ring_source, cfg.kickmap_path)),
            "matched_angle_rad": xmatch, "skipped_grid_points": getattr(build_jobs, "skipped", []),
            "cli": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
            "runtime_s": time.time() - t0,
            "definitions": {"capture": "alive after turns of native tracking from septum exit (95% Wilson CI)",
                            "x_offset": "injected centroid at septum exit", "xp_offset": "deviation from angle-matched x'",
                            "pairing": "all models at one point share the same injected particles"}}
    (out / "operating_region_raw.json").write_text(json.dumps({**meta, "points": results}, allow_nan=False) + "\n")
    rows = []
    for r in results:
        for m, e in r["models"].items():
            rows.append({k: r[k] for k in ("group", "bts", "seed", "x_inj_m", "xp_inj_rad", "xp_offset_rad",
                                           "field_scale", "backend", "bts_lost")} |
                        {"model": m, "capture": e["capture_fraction"], "ci95": e["capture_ci95"],
                         "loss_causes": e["loss_causes"], "centroid_amp_m": e["nominal_centroid_amplitude_after_kick_m"],
                         "stored_amp_over_sigma": e.get("stored", {}).get("amplitude_over_sigma")})
    (out / "operating_region_summary.json").write_text(json.dumps({**meta, "rows": rows}, indent=1, allow_nan=False) + "\n")
    for row in rows:
        if row["group"] in ("replicate", "bts") or (row["group"] == "map" and row["xp_offset_rad"] == 0.0):
            print(f"{row['group']:5s} {row['bts']:9s} x={row['x_inj_m']*1e3:6.1f} S={row['field_scale']:.2f} off={row['xp_offset_rad']*1e3:5.2f} "
                  f"{row['model']:8s} cap={row['capture']:.3f}")
    print(f"Done in {time.time() - t0:.0f} s -> {out}")


if __name__ == "__main__":
    main()
