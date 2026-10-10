#!/usr/bin/env python3
"""C1 — Kicker-model validation (consolidated revision task C1; reviewer tasks R1-02, R2-1, R2-14).

1. Exact filament field (``nkm_injection.wire_field``) against the RADIA kick map on the grid nodes.
2. Slice and field-span convergence of the 3-D sliced tracker at the operating point.
3. Momentum (δ) and vertical-offset sensitivity; centroid response to septum position/angle errors for the thin
   map, the 1-D uniform-profile thick model and the 3-D model.
4. Paired capture at the operating point (identical coupled-BTS bunches, native ring tracking): thin map with the
   physical vertical sign, thin map with the legacy sign, 3-D model at the thin-matched angle and at its own
   re-matched angle.
Units: m, rad. Output: one JSON in a new directory.
"""
import argparse
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from nkm_injection.concurrency import parallel_map
from nkm_injection.fieldmap import load_1d_fieldmap
from nkm_injection.injection_study import (InjectionStudyConfig, KickModelEvaluator, ThickNKMKicker, _apply_kick,
                                           booster_beam, cached_ring, injected_beam_at_septum, track_bts,
                                           track_injection, wilson_interval)
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.stage_cli import input_hashes
from nkm_injection.wire_field import FilamentNKMField, FilamentNKMKicker, brho_T_m

REPO = Path(__file__).resolve().parent.parent
LEVER = 2.0 + 0.2625  # septum exit to NKM centre (m)


def make_kicker(case, cfg, root, n_slices):
    if case in ("thin", "thin_legacy"):
        return KickModelEvaluator("fieldmap", cfg, NKMKickMap2D(root / cfg.kickmap_path), cfg.nkm_entry_x_m,
                                  vertical_sign=-1.0 if case == "thin" else 1.0)
    if case == "thick1d":
        return ThickNKMKicker(cfg, *load_1d_fieldmap(root / "By.txt"))
    return FilamentNKMKicker(cfg, n_slices=n_slices, vertical_kick=not case.endswith("_novert"))


def exit_state(cfg, kicker, dx=0.0, dxp=0.0, y=0.0, delta=0.0, xp=None):
    xp = cfg.injection_xp_rad if xp is None else xp
    b = np.zeros((6, 1)); b[0] = cfg.injection_x_m + dx + LEVER * (xp + dxp); b[1] = xp + dxp; b[2] = y; b[4] = delta
    _apply_kick(b, kicker, cfg.closed_orbit_x_m)
    return b[:, 0]


def matched_angle(cfg, kicker):
    return brentq(lambda xp: exit_state(cfg, kicker, xp=xp)[1], cfg.injection_xp_rad - 1e-3,
                  cfg.injection_xp_rad + 1e-3, xtol=1e-12)


def map_agreement(root, stride):
    km = NKMKickMap2D(root / "kickmap_file.txt")
    f = FilamentNKMField()
    xg = km.x_grid[::stride]
    X, Y = np.meshgrid(xg, xg); X, Y = X.ravel(), Y.ravel()
    w = f.geometry.wire_positions()
    dist = np.min(np.hypot(X[:, None] - w[None, :, 0], Y[:, None] - w[None, :, 1]), axis=1)
    sel = (np.abs(X) <= 0.03) & (np.abs(Y) <= 0.03) & (dist >= 1.5e-3)
    X, Y = X[sel], Y[sel]
    ibx, iby = f.line_integrals(X, Y, s_max_m=5.0)
    kx, ky = km.evaluate_kicks(X, Y)
    br = brho_T_m(4e9)
    out = {"n_nodes": int(len(X)), "region": "|x|,|y| <= 30 mm, >= 1.5 mm from wires, every %d-th node" % stride}
    for name, a, b in (("kx_vs_int_By", kx, iby / br), ("ky_vs_int_Bx", ky, ibx / br), ("ky_vs_minus_int_Bx", ky, -ibx / br)):
        r = a - b
        out[name] = {"max_abs_rad": float(np.max(np.abs(r))), "rms_rad": float(np.sqrt(np.mean(r ** 2))),
                     "max_rel": float(np.max(np.abs(r)) / np.max(np.abs(a)))}
    return out


def run_capture(job):
    t0 = time.perf_counter()
    root = Path(job["repo_root"])
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    lat = create_bts_lattice(BTSConfig.from_dict(job["bts"]["bts_config"]))
    exit_beam = track_bts(lat, booster_beam(job["bts"]["initial_twiss"], cfg.injected_beam, job["particles"], job["seed"]))
    beam = injected_beam_at_septum(cfg, ring, job["seed"], bts_exit_beam=exit_beam)
    res = track_injection(cfg, ring, make_kicker(job["case"], cfg, root, job["n_slices"]), beam, "element", n_turns=job["turns"])
    lo, hi = wilson_interval(res["captured"], res["n_particles"])
    return {"case": job["case"], "seed": job["seed"], "xp_inj_rad": cfg.injection_xp_rad, "captured": res["captured"],
            "n": res["n_particles"], "capture": res["capture_fraction"], "ci95": [lo, hi], "loss_causes": res["loss_causes"],
            "alive_mask": res["alive_mask"], "runtime_s": time.perf_counter() - t0}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 777, 2025])
    p.add_argument("--particles", type=int, default=500)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--n-slices", type=int, default=640)
    p.add_argument("--map-stride", type=int, default=2)
    p.add_argument("--skip-capture", action="store_true")
    p.add_argument("--cases", nargs="+", default=["thin", "thin_legacy", "fieldmap_3d", "fieldmap_3d_rematched"],
                   help="Capture cases; *_rematched use the 3-D matched angle; *_novert suppress the 3-D vertical kick "
                        "(diagnostic); thick1d uses its own re-matched angle")
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args(argv)
    out = a.output_dir.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    cfg = InjectionStudyConfig.load(a.study_config)
    root = a.repo_root
    t0 = time.time()
    summary = {"study_config": cfg.to_dict(), "n_slices": a.n_slices,
               "input_sha256": input_hashes(root, ("By.txt", "kickmap_file.txt", cfg.ring_source)),
               "map_agreement": map_agreement(root, a.map_stride)}
    conv = []
    for n in (80, 160, 320, 640, 1280):
        for span in (0.45, 0.8):
            s = exit_state(cfg, FilamentNKMKicker(cfg, n_slices=n, s_span_m=span))
            conv.append({"n_slices": n, "s_span_m": span, "x_m": float(s[0]), "px_rad": float(s[1])})
    ref = conv[-1]
    for c in conv:
        c["dpx_vs_finest_rad"] = c["px_rad"] - ref["px_rad"]
    summary["convergence"] = conv
    k3 = FilamentNKMKicker(cfg, n_slices=a.n_slices)
    kicks = {c: make_kicker(c, cfg, root, a.n_slices) for c in ("thin", "thin_legacy", "thick1d", "fieldmap_3d")}
    summary["delta_sensitivity"] = {f"{d:+.0e}": {"px_rad": float(exit_state(cfg, k3, delta=d)[1])} for d in (-3e-3, 0.0, 3e-3)}
    resp = {}
    for c, k in kicks.items():
        rows = {}
        for lab, kw in (("nominal", {}), ("dx+0.5mm", {"dx": 5e-4}), ("dx-0.5mm", {"dx": -5e-4}), ("dxp+0.3mrad", {"dxp": 3e-4}),
                        ("dxp-0.3mrad", {"dxp": -3e-4}), ("y+1mm", {"y": 1e-3})):
            s = exit_state(cfg, k, **kw)
            rows[lab] = {"x_m": float(s[0]), "px_rad": float(s[1]), "y_m": float(s[2]), "py_rad": float(s[3])}
        resp[c] = rows
    summary["centroid_response"] = resp
    xp3 = matched_angle(cfg, k3)
    summary["matched_angle_rad"] = {"thin": cfg.injection_xp_rad, "fieldmap_3d": xp3,
                                    "thick1d": matched_angle(cfg, kicks["thick1d"])}
    if not a.skip_capture:
        sel = load_optimization_handoff(a.optimization_summary)
        bts = {"bts_config": sel.bts.to_dict(), "initial_twiss": sel.initial_twiss}
        work = out / "_lattice"
        cached_ring(cfg, root, work)
        base = {"repo_root": str(root), "work_dir": str(work), "bts": bts, "particles": a.particles, "turns": a.turns,
                "n_slices": a.n_slices}
        jobs = []
        for seed in a.seeds:
            for case in a.cases:
                xp = xp3 if "rematched" in case else (summary["matched_angle_rad"]["thick1d"] if case == "thick1d" else None)
                c = cfg if xp is None else replace(cfg, injection_xp_rad=xp)
                jobs.append({**base, "case": case, "seed": seed, "config": c.to_dict()})
        rows = parallel_map(run_capture, jobs, n_workers=a.workers, desc="C1 capture")
        summary["capture_rows"] = rows
        summary["capture_means"] = {c: float(np.mean([r["capture"] for r in rows if r["case"] == c])) for c in a.cases}
    summary["runtime_s"] = time.time() - t0
    (out / "kicker_model_validation.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("map_agreement", "matched_angle_rad")}, indent=1))
    print(json.dumps(summary.get("capture_means"), indent=1))


if __name__ == "__main__":
    main()
