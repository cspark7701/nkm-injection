#!/usr/bin/env python3
"""Task 011 review check — thin versus thick NKM at the operating point (native ring tracking).

Uses the same booster bunches as the S6 replicate stage (seeds, particles, coupled matched BTS) and tracks
(a) the thin kick-map model (reproduction), (b) a thick drift-kick-drift NKM through the By.txt profile at the
same injection angle, and (c) the thick NKM with the injection angle re-matched so that the nominal centroid
leaves the NKM with zero angle. Units: m, rad. Capture with 95 % Wilson intervals.
"""
import argparse
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import (InjectionStudyConfig, KickModelEvaluator, ThickNKMKicker, cached_ring,
                                           injected_beam_at_septum, track_injection, booster_beam, track_bts,
                                           wilson_interval, _apply_kick)
from nkm_injection.fieldmap import load_1d_fieldmap
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.stage_cli import input_hashes

REPO = Path(__file__).resolve().parent.parent
LEVER = 2.0 + 0.2625


def rematched_angle(cfg, thick):
    def f(xp):
        b = np.zeros((6, 1)); b[0] = cfg.injection_x_m + LEVER * xp; b[1] = xp
        _apply_kick(b, thick, cfg.closed_orbit_x_m)
        return b[1, 0]
    return brentq(f, cfg.injection_xp_rad - 1e-3, cfg.injection_xp_rad + 1e-3, xtol=1e-12)


def run(job):
    t0 = time.perf_counter()
    root = Path(job["repo_root"])
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    lat = create_bts_lattice(BTSConfig.from_dict(job["bts"]["bts_config"]))
    exit_beam = track_bts(lat, booster_beam(job["bts"]["initial_twiss"], cfg.injected_beam, job["particles"], job["seed"]))
    if job["case"] == "thin":
        kicker = KickModelEvaluator("fieldmap", cfg, NKMKickMap2D(root / cfg.kickmap_path), cfg.nkm_entry_x_m)
    else:
        x, by = load_1d_fieldmap(root / "By.txt")
        kicker = ThickNKMKicker(cfg, x, by, n_slices=job["n_slices"])
    beam = injected_beam_at_septum(cfg, ring, job["seed"], bts_exit_beam=exit_beam)
    res = track_injection(cfg, ring, kicker, beam, "element", n_turns=job["turns"])
    lo, hi = wilson_interval(res["captured"], res["n_particles"])
    return {"case": job["case"], "seed": job["seed"], "xp_inj_rad": cfg.injection_xp_rad, "captured": res["captured"],
            "n": res["n_particles"], "capture": res["capture_fraction"], "ci95": [lo, hi], "loss_causes": res["loss_causes"],
            "runtime_s": time.perf_counter() - t0}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 777, 2025])
    p.add_argument("--particles", type=int, default=500)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--n-slices", type=int, default=160)
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args(argv)
    out = a.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    cfg = InjectionStudyConfig.load(a.study_config)
    sel = load_optimization_handoff(a.optimization_summary)
    bts = {"bts_config": sel.bts.to_dict(), "initial_twiss": sel.initial_twiss}
    x, by = load_1d_fieldmap(a.repo_root / "By.txt")
    xp_re = rematched_angle(cfg, ThickNKMKicker(cfg, x, by, n_slices=a.n_slices))
    out.mkdir(parents=True)
    work = out / "_lattice"
    cached_ring(cfg, a.repo_root, work)
    base = {"repo_root": str(a.repo_root), "work_dir": str(work), "bts": bts, "particles": a.particles,
            "turns": a.turns, "n_slices": a.n_slices}
    jobs = []
    for seed in a.seeds:
        jobs.append({**base, "case": "thin", "seed": seed, "config": cfg.to_dict()})
        jobs.append({**base, "case": "thick_same_angle", "seed": seed, "config": cfg.to_dict()})
        jobs.append({**base, "case": "thick_rematched", "seed": seed,
                     "config": replace(cfg, injection_xp_rad=xp_re).to_dict()})
    t0 = time.time()
    rows = parallel_map(run, jobs, n_workers=a.workers, desc="thick NKM check")
    summary = {"study_config": cfg.to_dict(), "rematched_xp_rad": xp_re, "thin_xp_rad": cfg.injection_xp_rad,
               "n_slices": a.n_slices, "input_sha256": input_hashes(a.repo_root, ("By.txt", "kickmap_file.txt", cfg.ring_source)),
               "runtime_s": time.time() - t0, "rows": rows,
               "means": {c: float(np.mean([r["capture"] for r in rows if r["case"] == c]))
                         for c in ("thin", "thick_same_angle", "thick_rematched")}}
    (out / "thick_nkm_check.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"means": summary["means"], "rematched_xp_mrad": xp_re * 1e3}, indent=1))


if __name__ == "__main__":
    main()
