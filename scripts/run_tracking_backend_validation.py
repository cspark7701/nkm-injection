#!/usr/bin/env python3
"""S5 — Tracking backend and numerical validation for the NKM injection model (Task 003).

Compares native element-by-element AT tracking ("element") with the linear one-turn-map backend
("map") on identical (paired) beams, maps the dynamic aperture at the NKM centre, checks limiting
cases, particle/turn convergence and the stored-beam response, and records chamber-aperture
sensitivity. All inputs are read-only; all outputs go to a new --output-dir.

Units: m, rad, eV; DA amplitudes reported in mm. Capture intervals are 95 % Wilson intervals.
"""
import argparse
import datetime
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import (
    InjectionStudyConfig, KickModelEvaluator, cached_ring, injected_beam_at_septum, track_injection,
    stored_beam_at_nkm, stored_beam_response, booster_beam, track_bts, beam_moments, wilson_interval, KICK_MODELS)
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.bts_lattice import create_bts_lattice
from nkm_injection.stage_cli import add_source_argument, source_root, input_hashes

REPO = Path(__file__).resolve().parent.parent


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--optimization-summary", type=Path, default=None,
                   help="Selected BTS optimisation; when given, the injected beam is tracked through it")
    p.add_argument("--backends", nargs="+", choices=("element", "map"), default=["element", "map"])
    p.add_argument("--kicker-models", nargs="+", choices=KICK_MODELS, default=list(KICK_MODELS))
    p.add_argument("--particles", nargs="+", type=int, default=[200, 1000])
    p.add_argument("--turns", nargs="+", type=int, default=[100, 500, 2000])
    p.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 777])
    p.add_argument("--da-turns", type=int, default=500)
    p.add_argument("--chamber-half-x-mm", type=float, default=12.0, help="Sensitivity case chamber half aperture")
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--output-dir", type=Path, required=True)
    add_source_argument(p)
    return p.parse_args(argv)


# ---------------------------------------------------------------------------
# Worker (top level for process pools)
# ---------------------------------------------------------------------------

def _context(job):
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, Path(job["repo_root"]), Path(job["work_dir"]))
    kmap = NKMKickMap2D(Path(job["repo_root"]) / cfg.kickmap_path)
    return cfg, ring, kmap


def _injected(job, cfg, ring, n, seed):
    if job.get("bts") is None:
        return injected_beam_at_septum(cfg, ring, seed, n=n)
    from nkm_injection.bts_lattice import BTSConfig
    bts = job["bts"]
    lat = create_bts_lattice(BTSConfig.from_dict(bts["bts_config"]))
    exit_beam = track_bts(lat, booster_beam(bts["initial_twiss"], cfg.injected_beam, n, seed))
    return injected_beam_at_septum(cfg, ring, seed, bts_exit_beam=exit_beam)


def run_job(job):
    t0 = time.perf_counter()
    cfg, ring, kmap = _context(job)
    kind = job["kind"]
    out = {"kind": kind, "label": job["label"]}
    if kind in ("da_x_delta", "da_x_xp"):
        pts = np.asarray(job["points"], dtype=float)  # columns: x, xp, delta
        beam = np.tile(ring.orbit6[:, None], (1, len(pts)))
        beam[0] += pts[:, 0]; beam[1] += pts[:, 1]; beam[2] += 1e-5; beam[4] += pts[:, 2]
        _, _, info = ring.ring_c.track(beam, nturns=job["turns"], refpts=None, losses=True, in_place=True)
        lost = np.asarray(info["loss_map"]["islost"], dtype=bool)
        out.update(points=pts.tolist(), survived=(~lost).tolist(),
                   loss_turn=np.where(lost, info["loss_map"]["turn"], -1).tolist(), turns=job["turns"])
    elif kind == "injection":
        x_ref = cfg.nkm_entry_x_m
        kicker = KickModelEvaluator(job["model"], cfg, None if job["model"] == "off" else kmap, x_ref)
        beam = _injected(job, cfg, ring, job["particles"], job["seed"])
        res = track_injection(cfg, ring, kicker, beam, job["backend"], n_turns=job["turns"])
        lo, hi = wilson_interval(res["captured"], res["n_particles"])
        out.update({k: res[k] for k in ("backend", "kick_model", "n_particles", "n_turns", "captured",
                                        "capture_fraction", "loss_causes", "first_loss_turn")},
                   capture_ci95=[lo, hi], seed=job["seed"], model=job["model"], chamber=cfg.chamber_half_x_m,
                   injected_moments_at_septum=beam_moments(beam))
    elif kind == "stored_paired":
        beam0 = stored_beam_at_nkm(cfg, ring, job["particles"], job["seed"])
        kicker = KickModelEvaluator(job["model"], cfg, kmap, cfg.nkm_entry_x_m)
        kicked = beam0.copy()
        kx, ky = kicker.kicks(kicked[0] + cfg.closed_orbit_x_m, kicked[2])
        kicked[1] += kx; kicked[3] += ky
        refpts = [0]
        r_ref = ring.ring_c.track(beam0.copy(), nturns=job["turns"], refpts=refpts)[0][:, :, 0, :]
        r_kick = ring.ring_c.track(kicked, nturns=job["turns"], refpts=refpts)[0][:, :, 0, :]
        dc = np.nanmean(r_kick[0] - r_ref[0], axis=0)  # paired centroid difference per turn (m)
        resp = stored_beam_response(cfg, ring, kicker)
        out.update(model=job["model"], turns=job["turns"], particles=job["particles"],
                   tracked_max_centroid_diff_m=float(np.nanmax(np.abs(dc))),
                   analytic_centroid_amplitude_m=resp["centroid_amplitude_m"],
                   analytic=resp, survivors_kicked=int(np.isfinite(r_kick[0, :, -1]).sum()))
    elif kind == "limits":
        # (a) small-amplitude linear regime: element vs map residual after n turns with zero kick
        pts = np.array([[1e-4, 0, 0], [5e-4, 0, 0], [1e-3, 0, 0], [0, 1e-5, 0]])
        beam = np.tile(ring.orbit6[:, None], (1, len(pts)))
        beam[0] += pts[:, 0]; beam[1] += pts[:, 1]
        res = {}
        for n in job["turns_list"]:
            el = beam.copy(); ring.ring_c.track(el, nturns=n, refpts=None, in_place=True)
            mp = beam - ring.orbit6[:, None]
            for _ in range(n):
                mp = ring.m66 @ mp
            mp = mp + ring.orbit6[:, None]
            res[str(n)] = {"amplitudes_m": pts[:, 0].tolist(),
                           "abs_dx_m": np.abs(el[0] - mp[0]).tolist(), "abs_dxp_rad": np.abs(el[1] - mp[1]).tolist(),
                           "rel_dx": (np.abs(el[0] - mp[0]) / np.maximum(np.abs(mp[0] - ring.orbit6[0]), 1e-12)).tolist()}
        # (b) zero field scale equals kicker off exactly (element backend, same beam)
        beam_i = _injected(job, cfg, ring, 50, 5)
        zero = replace(cfg, field_scale=0.0)
        a = track_injection(zero, ring, KickModelEvaluator("fieldmap", zero, kmap, cfg.nkm_entry_x_m), beam_i, "element", n_turns=20)
        b = track_injection(cfg, ring, KickModelEvaluator("off", cfg, None, cfg.nkm_entry_x_m), beam_i, "element", n_turns=20)
        out.update(small_amplitude=res, zero_scale_equals_off=bool(a["alive_mask"] == b["alive_mask"] and
                   np.allclose(np.asarray(a["final_coordinates"], float), np.asarray(b["final_coordinates"], float),
                               equal_nan=True, atol=0.0, rtol=0.0)))
    out["runtime_s"] = time.perf_counter() - t0
    return out


# ---------------------------------------------------------------------------
# Job construction and summary
# ---------------------------------------------------------------------------

def build_jobs(args, cfg, root, work_dir, bts):
    base = {"config": cfg.to_dict(), "repo_root": str(root), "work_dir": str(work_dir), "bts": bts}
    jobs = []
    xs = np.round(np.arange(-20.0, 20.01, 1.0) * 1e-3, 6)
    deltas = [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03]
    pts = [(x, 0.0, d) for d in deltas for x in xs]
    for i in range(0, len(pts), 41):
        jobs.append({**base, "kind": "da_x_delta", "label": f"da_x_delta_{i // 41}", "points": pts[i:i + 41], "turns": args.da_turns})
    xps = np.round(np.arange(-1.5, 1.51, 0.25) * 1e-3, 6)
    pts = [(x, xp, 0.0) for xp in xps for x in xs]
    for i in range(0, len(pts), 41):
        jobs.append({**base, "kind": "da_x_xp", "label": f"da_x_xp_{i // 41}", "points": pts[i:i + 41], "turns": args.da_turns})
    p0, t_main = min(args.particles), sorted(args.turns)[len(args.turns) // 2]
    for model in args.kicker_models:
        for backend in args.backends:
            for seed in (args.seeds if model == "fieldmap" else args.seeds[:1]):
                jobs.append({**base, "kind": "injection", "label": f"inj_{model}_{backend}_p{p0}_t{t_main}_s{seed}",
                             "model": model, "backend": backend, "particles": p0, "turns": t_main, "seed": seed})
    for n in sorted(args.particles)[1:]:  # particle convergence (fieldmap, element, first seed)
        jobs.append({**base, "kind": "injection", "label": f"conv_particles_{n}", "model": "fieldmap",
                     "backend": "element", "particles": n, "turns": t_main, "seed": args.seeds[0]})
    t_max = max(args.turns)  # turn convergence: one long run; loss-turn distribution gives all shorter N
    jobs.append({**base, "kind": "injection", "label": f"conv_turns_{t_max}", "model": "fieldmap",
                 "backend": "element", "particles": p0, "turns": t_max, "seed": args.seeds[0]})
    chamber = replace(cfg, chamber_half_x_m=args.chamber_half_x_mm * 1e-3, chamber_half_y_m=args.chamber_half_x_mm * 0.5e-3)
    jobs.append({**base, "config": chamber.to_dict(), "work_dir": str(work_dir / "chamber"), "kind": "injection",
                 "label": f"chamber_{args.chamber_half_x_mm:g}mm", "model": "fieldmap", "backend": "element",
                 "particles": p0, "turns": t_main, "seed": args.seeds[0]})
    for model in ("fieldmap", "off"):
        jobs.append({**base, "kind": "stored_paired", "label": f"stored_{model}", "model": model,
                     "particles": 100, "turns": 200, "seed": 11})
    uniform = replace(cfg, field_scale=0.0, kick_offset_rad=1.0e-6)  # 1 urad uniform kick: analytic check
    jobs.append({**base, "config": uniform.to_dict(), "kind": "stored_paired", "label": "stored_uniform_1urad",
                 "model": "fieldmap", "particles": 100, "turns": 200, "seed": 11})
    jobs.append({**base, "kind": "limits", "label": "limits", "turns_list": [1, 10, 100]})
    return jobs


def summarise(results, args, cfg):
    by = {r["label"]: r for r in results}
    da = {}
    for kind in ("da_x_delta", "da_x_xp"):
        pts, surv = [], []
        for r in results:
            if r["kind"] == kind:
                pts += r["points"]; surv += r["survived"]
        pts, surv = np.asarray(pts), np.asarray(surv, bool)
        if kind == "da_x_delta":
            table = {}
            for d in np.unique(pts[:, 2]):
                sel = pts[:, 2] == d
                xs, ok = pts[sel, 0], surv[sel]
                neg = xs[(xs < 0)][::-1]; pos = xs[xs > 0]
                def edge(cands):
                    last = 0.0
                    for x in cands:
                        if not ok[xs == x][0]:
                            break
                        last = x
                    return last
                table[f"{d:+.2f}"] = {"x_min_stable_mm": edge(neg) * 1e3, "x_max_stable_mm": edge(pos) * 1e3}
            da[kind] = table
        else:
            da[kind] = {"n_points": int(len(pts)), "n_survived": int(surv.sum())}
    inj = {k: {kk: v[kk] for kk in ("model", "backend", "seed", "n_particles", "n_turns", "captured",
                                     "capture_fraction", "capture_ci95", "loss_causes")}
           for k, v in by.items() if v["kind"] == "injection"}
    paired = []
    for model in args.kicker_models:
        for seed in args.seeds:
            e = by.get(f"inj_{model}_element_p{min(args.particles)}_t{sorted(args.turns)[len(args.turns) // 2]}_s{seed}")
            m = by.get(f"inj_{model}_map_p{min(args.particles)}_t{sorted(args.turns)[len(args.turns) // 2]}_s{seed}")
            if e and m:
                ae, am = np.asarray(e["first_loss_turn"]) < 0, np.asarray(m["first_loss_turn"]) < 0
                paired.append({"model": model, "seed": seed, "element_capture": e["capture_fraction"],
                               "map_capture": m["capture_fraction"],
                               "capture_difference": m["capture_fraction"] - e["capture_fraction"],
                               "discordant_particles": int(np.sum(ae != am))})
    long = by[f"conv_turns_{max(args.turns)}"]
    flt = np.asarray(long["first_loss_turn"])
    turn_curve = {str(t): float(np.mean((flt < 0) | (flt >= t))) for t in sorted(set(args.turns + [50, 200, 1000]))
                  if t <= max(args.turns)}
    return {"dynamic_aperture": da, "injection_runs": inj, "paired_backend_comparison": paired,
            "turn_convergence_capture": turn_curve,
            "stored_beam": {k: {kk: by[k][kk] for kk in ("model", "tracked_max_centroid_diff_m",
                                                          "analytic_centroid_amplitude_m", "survivors_kicked")}
                            for k in by if by[k]["kind"] == "stored_paired"},
            "limits": {"small_amplitude": by["limits"]["small_amplitude"],
                       "zero_scale_equals_off": by["limits"]["zero_scale_equals_off"]}}


def main(argv=None):
    args = parse_args(argv)
    root = source_root(args, REPO)
    out = args.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    cfg = InjectionStudyConfig.load(args.study_config)
    cfg.validate()
    bts = None
    if args.optimization_summary is not None:
        sel = load_optimization_handoff(args.optimization_summary)
        bts = {"bts_config": sel.bts.to_dict(), "initial_twiss": sel.initial_twiss}
    out.mkdir(parents=True, exist_ok=True)
    work = out / "_lattice"
    cached_ring(cfg, root, work)  # generate the run-local lattice once before dispatch
    jobs = build_jobs(args, cfg, root, work, bts)
    print(f"S5: {len(jobs)} jobs, workers={args.workers}", flush=True)
    t0 = time.time()
    results = parallel_map(run_job, jobs, n_workers=args.workers, desc="S5 backend validation")
    summary = summarise(results, args, cfg)
    meta = {"timestamp": datetime.datetime.now().isoformat(), "study_config": cfg.to_dict(),
            "study_config_path": str(args.study_config), "optimization_summary": str(args.optimization_summary),
            "injected_beam_source": "coupled BTS tracking" if bts else "Gaussian at septum exit",
            "input_sha256": input_hashes(root, (cfg.ring_source, cfg.kickmap_path)),
            "cli": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
            "runtime_s": time.time() - t0, "n_jobs": len(jobs),
            "definitions": {"capture": "alive after n_turns of native (or map) tracking from the septum exit",
                            "ci": "95% Wilson score interval over particles",
                            "da_edge": "largest |x| on a 1 mm grid with all smaller grid points stable for da_turns"}}
    (out / "backend_validation_raw.json").write_text(json.dumps(results, indent=1, allow_nan=False) + "\n")
    (out / "backend_validation_summary.json").write_text(json.dumps({**meta, **summary}, indent=2, allow_nan=False) + "\n")
    print(json.dumps(summary["dynamic_aperture"], indent=1))
    print(json.dumps(summary["paired_backend_comparison"], indent=1))
    print("turn convergence:", summary["turn_convergence_capture"])
    print(f"Done in {time.time() - t0:.0f} s -> {out}")


if __name__ == "__main__":
    main()
