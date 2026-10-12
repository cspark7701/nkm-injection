#!/usr/bin/env python3
"""C7 — Tracked multi-turn stored-beam response to one passage through the 3-D NKM (R1-07, R2-8).

The same Gaussian stored beam (ring equilibrium ε_x, σ_δ and Twiss at the NKM centre; ε_y = ratio × ε_x) is tracked
natively for ``--turns`` turns twice: unperturbed, and after one passage through the exact 3-D magnet with the given
horizontal NKM–orbit offset. The turn-by-turn centroid difference (paired particles; sampling noise largely cancels)
gives the tracked residual oscillation amplitude; the rms emittance difference at the last turn gives the tracked
emittance change. Compared with the deterministic single-pass estimate of ``analyze_transparency_3d.py``. Units: m, rad.
"""
import argparse
import json
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig, cached_ring
from nkm_injection.wire_field import FilamentNKMKicker

REPO = Path(__file__).resolve().parent.parent


def stored_beam(ring, n, seed, emit_y_ratio):
    rng = np.random.default_rng(seed)
    b = np.zeros((6, n))
    for i, ((bet, alp), em) in enumerate(((ring.twiss_x, ring.emit_x_m_rad), (ring.twiss_y, emit_y_ratio * ring.emit_x_m_rad))):
        u = np.sqrt(em * bet) * rng.standard_normal(n)
        b[2 * i] = u
        b[2 * i + 1] = -alp * u / bet + np.sqrt(em / bet) * rng.standard_normal(n)
    b[4] = ring.energy_spread * rng.standard_normal(n)
    b[5] = ring.bunch_length_m * rng.standard_normal(n)
    return b + np.asarray(ring.orbit6)[:, None]


def rms_emit(u, up):
    u, up = u - u.mean(), up - up.mean()
    return float(np.sqrt(np.mean(u * u) * np.mean(up * up) - np.mean(u * up) ** 2))


def run(job):
    t0 = time.perf_counter()
    root = Path(job["repo_root"])
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    b = stored_beam(ring, job["particles"], job["seed"], job["emit_y_ratio"])
    kicked = b.copy()
    FilamentNKMKicker(replace(cfg, nkm_dx_m=job["dx_m"], closed_orbit_x_m=0.0), n_slices=job["n_slices"]).apply(kicked, 0.0)
    res = {}
    for lab, beam in (("ref", b), ("kicked", kicked)):
        out, _, info = ring.ring_c.track(beam.copy(), nturns=job["turns"], refpts=[len(ring.ring_c)], losses=True)
        res[lab] = (np.asarray(out)[:, :, 0, :], int(np.sum(info["loss_map"]["islost"])))
    (r, lr), (k, lk) = res["ref"], res["kicked"]
    dcx = np.nanmean(k[0], axis=0) - np.nanmean(r[0], axis=0)
    dcy = np.nanmean(k[2], axis=0) - np.nanmean(r[2], axis=0)
    bx = ring.twiss_x[0]; by = ring.twiss_y[0]
    sigx = np.sqrt(ring.emit_x_m_rad * bx); sigy = np.sqrt(job["emit_y_ratio"] * ring.emit_x_m_rad * by)
    first = slice(0, min(50, job["turns"]))  # before decoherence
    return {"dx_m": job["dx_m"], "seed": job["seed"], "particles": job["particles"], "turns": job["turns"],
            "lost_ref": lr, "lost_kicked": lk,
            "centroid_x_amplitude_first50_m": float(np.max(np.abs(dcx[first]))),
            "centroid_y_amplitude_first50_m": float(np.max(np.abs(dcy[first]))),
            "centroid_y_amplitude_over_sigma": float(np.max(np.abs(dcy[first])) / sigy),
            "amplitude_observation_turns": [1, min(50, job["turns"])],
            "emittance_observation_turn": job["turns"],
            "centroid_x_amplitude_over_sigma": float(np.max(np.abs(dcx[first])) / sigx),
            "centroid_x_last_turns_rms_m": float(np.sqrt(np.mean(dcx[-50:] ** 2))),
            "emit_x_ratio_last": rms_emit(k[0, :, -1], k[1, :, -1]) / rms_emit(r[0, :, -1], r[1, :, -1]),
            "emit_y_ratio_last": rms_emit(k[2, :, -1], k[3, :, -1]) / rms_emit(r[2, :, -1], r[3, :, -1]),
            "sigma_x_m": float(sigx), "sigma_y_m": float(sigy), "runtime_s": time.perf_counter() - t0}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--offsets-mm", nargs="+", type=float, default=[0.0, 0.2, 0.5])
    p.add_argument("--seeds", nargs="+", type=int, default=[11, 12])
    p.add_argument("--particles", type=int, default=500)
    p.add_argument("--turns", type=int, default=1000)
    p.add_argument("--emit-y-ratio", type=float, default=0.1)
    p.add_argument("--n-slices", type=int, default=640)
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(argv)
    if a.output.exists():
        raise SystemExit("output exists")
    cfg = InjectionStudyConfig.load(a.study_config)
    work = a.output.parent / "_lattice"
    cached_ring(cfg, a.repo_root, work)
    jobs = [{"repo_root": str(a.repo_root), "work_dir": str(work), "config": cfg.to_dict(), "dx_m": d * 1e-3, "seed": s,
             "particles": a.particles, "turns": a.turns, "emit_y_ratio": a.emit_y_ratio, "n_slices": a.n_slices}
            for d in a.offsets_mm for s in a.seeds]
    t0 = time.time()
    rows = parallel_map(run, jobs, n_workers=a.workers, desc="C7 tracked")
    a.output.write_text(json.dumps({"study_config": cfg.to_dict(), "cli": {k: str(v) for k, v in vars(a).items()},
                                    "rows": rows, "runtime_s": time.time() - t0}, indent=2) + "\n")
    for r in rows:
        print(f"dx={r['dx_m']*1e3:.1f} seed={r['seed']} A/sigma={r['centroid_x_amplitude_over_sigma']:.3e} "
              f"emit_x ratio={r['emit_x_ratio_last']:.5f} lost {r['lost_ref']}/{r['lost_kicked']}")


if __name__ == "__main__":
    main()
