#!/usr/bin/env python3
"""C3 — Operating window with the exact 3-D finite-length NKM (reviewer tasks R1-04, R2-2, R2-9).

Stages (each writes ``<stage>_raw.json`` into the output directory):

* ``grid``       matched-point grid over septum position x_inj and field scale S; the injection angle is the inner
                 root of zero centroid angle after the 3-D magnet. Selection rule (declared before the run): the
                 point with the largest 95 % Wilson lower bound on capture.
* ``angle``      capture against the angle offset from the matched angle at one point (default step 0.1 mrad).
* ``position``   capture against the septum position offset at the matched angle.
* ``acceptance`` single-particle survival map in septum phase space (x, x') at δ = 0, y = 0 (500 turns).
* ``validate``   fresh bunches (seeds not used for selection) at one point for the 3-D NKM, dipole and linear
                 controls calibrated to the 3-D response of the nominal centroid, and the kicker off.

All stages use the coupled matched-BTS bunch (except ``acceptance``) and native element-by-element ring tracking.
Units: m, rad (CLI in mm and mrad).
"""
import argparse
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import (InjectionStudyConfig, _apply_kick, beam_moments, booster_beam, cached_ring,
                                           injected_beam_at_septum, track_bts, track_injection, wilson_interval)
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.stage_cli import input_hashes
from nkm_injection.wire_field import CalibratedControl, FilamentNKMKicker, calibrate_controls

REPO = Path(__file__).resolve().parent.parent
LEVER = 2.0 + 0.2625


def centroid_exit(cfg, kicker, xp, dx=0.0):
    b = np.zeros((6, 1)); b[0] = cfg.injection_x_m + dx + LEVER * xp; b[1] = xp
    _apply_kick(b, kicker, cfg.closed_orbit_x_m)
    return float(b[0, 0]), float(b[1, 0])


def matched_angle_3d(cfg, n_slices):
    """Inner (largest) root x' in [0, 15] mrad of zero centroid angle after the 3-D magnet; None if absent."""
    k = FilamentNKMKicker(cfg, n_slices=n_slices)
    f = lambda xp: centroid_exit(cfg, k, xp)[1]
    grid = np.linspace(2e-3, 9e-3, 141)
    vals = [f(v) for v in grid]
    roots = [brentq(f, grid[i], grid[i + 1], xtol=1e-12) for i in range(len(grid) - 1)
             if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] < 0]
    return max(roots) if roots else None


def run_bunch(job):
    t0 = time.perf_counter()
    root = Path(job["repo_root"])
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    lat = create_bts_lattice(BTSConfig.from_dict(job["bts"]["bts_config"]))
    exit_beam = track_bts(lat, booster_beam(job["bts"]["initial_twiss"], cfg.injected_beam, job["particles"], job["seed"]))
    beam = injected_beam_at_septum(cfg, ring, job["seed"], bts_exit_beam=exit_beam)
    out = {k: job[k] for k in ("stage", "label", "seed")}
    out.update({"x_inj_m": cfg.injection_x_m, "xp_inj_rad": cfg.injection_xp_rad, "field_scale": cfg.field_scale,
                "xp_offset_rad": job.get("xp_offset_rad", 0.0), "dx_offset_m": job.get("dx_offset_m", 0.0),
                "nkm_offset_m": job.get("nkm_offset_m", 0.0), "emit_x_m_rad": cfg.injected_beam.emit_x_m_rad,
                "injected_moments": beam_moments(beam), "bts_lost": int(np.sum(~np.isfinite(exit_beam[0]))), "models": {}})
    for model in job["models"]:
        if model == "fieldmap_3d":
            kicker = FilamentNKMKicker(cfg, n_slices=job["n_slices"])
        else:
            kicker = CalibratedControl(model, *job["calibration"])
        res = track_injection(cfg, ring, kicker, beam, "element", n_turns=job["turns"])
        lo, hi = wilson_interval(res["captured"], res["n_particles"])
        out["models"][model] = {"captured": res["captured"], "n": res["n_particles"], "capture": res["capture_fraction"],
                                "ci95": [lo, hi], "loss_causes": res["loss_causes"], "alive_mask": res["alive_mask"],
                                "first_loss_turn": res["first_loss_turn"]}
    out["runtime_s"] = time.perf_counter() - t0
    return out


def run_acceptance(job):
    """Single particles from the septum exit through the 3-D NKM and the ring; returns survival flags."""
    root = Path(job["repo_root"])
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    pts = np.asarray(job["points"])
    beam = np.zeros((6, len(pts)))
    beam[0], beam[1] = pts[:, 0], pts[:, 1]
    beam[4] += ring.orbit6[4]
    res = track_injection(cfg, ring, FilamentNKMKicker(cfg, n_slices=job["n_slices"]), beam, "element", n_turns=job["turns"])
    return {"points": pts.tolist(), "alive": res["alive_mask"], "first_loss_turn": res["first_loss_turn"]}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True, help="Base configuration (beam, ring, geometry)")
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--stages", nargs="+", choices=("grid", "angle", "position", "acceptance", "validate", "nkm_offset", "emittance"),
                   required=True)
    p.add_argument("--nkm-offsets-mm", nargs="+", type=float, default=[-0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6],
                   help="NKM horizontal offset from the stored orbit (no re-tuning of the injection angle)")
    p.add_argument("--emittances-nm", nargs="+", type=float, default=[25.0, 50.0, 100.0, 150.0, 200.0],
                   help="Injected horizontal geometric emittance at booster extraction")
    p.add_argument("--x-inj-mm", nargs="+", type=float, default=[-19.5, -20.0, -20.5, -21.0, -21.5, -22.0])
    p.add_argument("--field-scale", nargs="+", type=float, default=[0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1])
    p.add_argument("--point", nargs=2, type=float, metavar=("X_INJ_MM", "S"), help="Point for angle/position/acceptance/validate")
    p.add_argument("--angle-offsets-mrad", nargs="+", type=float, default=list(np.round(np.arange(-1.0, 1.0001, 0.1), 2)))
    p.add_argument("--position-offsets-mm", nargs="+", type=float, default=list(np.round(np.arange(-1.0, 1.0001, 0.2), 2)))
    p.add_argument("--acceptance-grid", nargs=6, type=float, default=[-23.0, -17.9, 52, 3.0, 6.5, 71],
                   metavar=("X0_MM", "X1_MM", "NX", "XP0_MRAD", "XP1_MRAD", "NXP"))
    p.add_argument("--grid-seed", type=int, default=42)
    p.add_argument("--scan-seeds", nargs="+", type=int, default=[42])
    p.add_argument("--validate-seeds", nargs="+", type=int, default=[1001, 1002, 1003, 1004])
    p.add_argument("--particles", type=int, default=200)
    p.add_argument("--scan-particles", type=int, default=500)
    p.add_argument("--validate-particles", type=int, default=500)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--n-slices", type=int, default=640)
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args(argv)
    out = a.output_dir.resolve(); out.mkdir(parents=True, exist_ok=True)
    cfg0 = InjectionStudyConfig.load(a.study_config)
    sel = load_optimization_handoff(a.optimization_summary)
    bts = {"bts_config": sel.bts.to_dict(), "initial_twiss": sel.initial_twiss}
    work = out / "_lattice"
    cached_ring(cfg0, a.repo_root, work)
    base = {"repo_root": str(a.repo_root), "work_dir": str(work), "bts": bts, "turns": a.turns, "n_slices": a.n_slices}
    meta = {"base_config": cfg0.to_dict(), "cli": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(a).items()},
            "input_sha256": input_hashes(a.repo_root, ("kickmap_file.txt", cfg0.ring_source)),
            "kicker": "wire_field.FilamentNKMKicker (exact 3-D filament field)", "loss_definition":
            "not alive after the last turn (septum creation, conductor/domain inside magnet, native AT ring loss)"}

    def point_cfg(x_mm, s):
        c = replace(cfg0, injection_x_m=x_mm * 1e-3, field_scale=s)
        xm = matched_angle_3d(c, a.n_slices)
        return None if xm is None else replace(c, injection_xp_rad=xm)

    for stage in a.stages:
        if (out / f"{stage}_raw.json").exists():
            raise SystemExit(f"{stage}_raw.json exists in the output directory")
        t0 = time.time()
        jobs = []
        if stage == "grid":
            skipped = []
            for x in a.x_inj_mm:
                for s in a.field_scale:
                    c = point_cfg(x, s)
                    xc = None if c is None else c.injection_x_m + LEVER * c.injection_xp_rad
                    if c is None or abs(xc) > 0.012:
                        skipped.append({"x_inj_mm": x, "S": s, "reason": "no inner matched root" if c is None else "centroid outside DA"})
                        continue
                    jobs.append({**base, "stage": stage, "label": f"x{x}_S{s}", "seed": a.grid_seed, "particles": a.particles,
                                 "config": c.to_dict(), "models": ["fieldmap_3d"]})
            rows = parallel_map(run_bunch, jobs, n_workers=a.workers, desc="C3 grid")
            payload = {"skipped": skipped, "rows": rows}
        else:
            if a.point is None:
                raise SystemExit("--point X_INJ_MM S is required for this stage")
            c = point_cfg(*a.point)
            if c is None:
                raise SystemExit("no matched angle at --point")
            calib = calibrate_controls(c, a.n_slices)
            if stage == "angle":
                for seed in a.scan_seeds:
                    for off in a.angle_offsets_mrad:
                        jobs.append({**base, "stage": stage, "label": f"off{off:+.2f}", "seed": seed, "particles": a.scan_particles,
                                     "xp_offset_rad": off * 1e-3, "models": ["fieldmap_3d"],
                                     "config": replace(c, injection_xp_rad=c.injection_xp_rad + off * 1e-3).to_dict()})
            elif stage == "position":
                for seed in a.scan_seeds:
                    for off in a.position_offsets_mm:
                        jobs.append({**base, "stage": stage, "label": f"dx{off:+.2f}", "seed": seed, "particles": a.scan_particles,
                                     "dx_offset_m": off * 1e-3, "models": ["fieldmap_3d"],
                                     "config": replace(c, injection_x_m=c.injection_x_m + off * 1e-3,
                                                       septum_edge_x_m=c.septum_edge_x_m).to_dict()})
            elif stage == "nkm_offset":
                for seed in a.scan_seeds:
                    for off in a.nkm_offsets_mm:
                        jobs.append({**base, "stage": stage, "label": f"nkm{off:+.2f}", "seed": seed, "particles": a.scan_particles,
                                     "nkm_offset_m": off * 1e-3, "models": ["fieldmap_3d"],
                                     "config": replace(c, nkm_dx_m=c.nkm_dx_m + off * 1e-3).to_dict()})
            elif stage == "emittance":
                for seed in a.scan_seeds:
                    for em in a.emittances_nm:
                        ib = replace(c.injected_beam, emit_x_m_rad=em * 1e-9)
                        jobs.append({**base, "stage": stage, "label": f"emit{em:g}", "seed": seed, "particles": a.scan_particles,
                                     "emit_x_m_rad": em * 1e-9, "models": ["fieldmap_3d"],
                                     "config": replace(c, injected_beam=ib).to_dict()})
            elif stage == "validate":
                for seed in a.validate_seeds:
                    jobs.append({**base, "stage": stage, "label": "validate", "seed": seed, "particles": a.validate_particles,
                                 "models": ["fieldmap_3d", "dipole", "linear", "off"], "calibration": list(calib),
                                 "config": c.to_dict()})
            if stage == "acceptance":
                x0, x1, nx, p0, p1, npp = a.acceptance_grid
                X, P = np.meshgrid(np.linspace(x0, x1, int(nx)) * 1e-3, np.linspace(p0, p1, int(npp)) * 1e-3)
                pts = np.column_stack([X.ravel(), P.ravel()])
                chunks = np.array_split(pts, max(1, a.workers * 3))
                parts = parallel_map(run_acceptance, [{**base, "config": c.to_dict(), "points": ch.tolist()} for ch in chunks],
                                     n_workers=a.workers, desc="C3 acceptance")
                payload = {"point_config": c.to_dict(), "points": sum((q["points"] for q in parts), []),
                           "alive": sum((q["alive"] for q in parts), []),
                           "first_loss_turn": sum((q["first_loss_turn"] for q in parts), [])}
            else:
                rows = parallel_map(run_bunch, jobs, n_workers=a.workers, desc=f"C3 {stage}")
                payload = {"point_config": c.to_dict(), "calibration_k0_k1_xref": list(calib), "rows": rows}
        payload.update(meta); payload["stage"] = stage; payload["runtime_s"] = time.time() - t0
        (out / f"{stage}_raw.json").write_text(json.dumps(payload) + "\n")
        print(f"[{stage}] done in {payload['runtime_s']:.0f} s", flush=True)


if __name__ == "__main__":
    main()
