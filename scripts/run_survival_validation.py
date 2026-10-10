#!/usr/bin/env python3
"""C4 — Survival and acceptance validation at the final operating point (R1-06, R2-3, R2-4, R2-12).

Stages (each writes ``<stage>_raw.json``):

* ``particles``    capture of one large bunch (default 2000 particles, split over workers) against the 500-particle
                   validation bunches (precision of the capture estimate).
* ``longturn``     bunches tracked for ``--long-turns`` (default 4000 ≈ one horizontal damping time); first-loss turns.
* ``aperture``     uniform rectangular chamber aperture ±a × ±b at every ring element (parameterised sensitivity;
                   the actual chamber is not specified in the lattice).
* ``ring_errors``  seeded random relative gradient errors on quadrupoles and strength errors on sextupoles (no
                   misalignments, hence no closed-orbit distortion and no correction); for each seed: linear tunes,
                   on-momentum horizontal DA at the NKM and capture. A bounded sensitivity, not a corrected-machine
                   model.

The injected bunch is the coupled matched-BTS bunch; the kicker is the exact 3-D NKM. Units: m, rad.
"""
import argparse
import copy
import json
import time
from pathlib import Path

import numpy as np

from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import (InjectionStudyConfig, booster_beam, cached_ring, injected_beam_at_septum,
                                           track_bts, track_injection, wilson_interval)
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.stage_cli import input_hashes
from nkm_injection.wire_field import FilamentNKMKicker

REPO = Path(__file__).resolve().parent.parent


def _beam(job, cfg, ring):
    lat = create_bts_lattice(BTSConfig.from_dict(job["bts"]["bts_config"]))
    exit_beam = track_bts(lat, booster_beam(job["bts"]["initial_twiss"], cfg.injected_beam, job["particles"], job["seed"]))
    beam = injected_beam_at_septum(cfg, ring, job["seed"], bts_exit_beam=exit_beam)
    lo, hi = job.get("slice", (0, beam.shape[1]))
    return beam[:, lo:hi]


def apply_ring_errors(ring, seed, quad_rel, sext_rel):
    """Deep-copied PreparedRing with seeded relative errors on PolynomB[1] (quadrupoles) and PolynomB[2] (sextupoles)."""
    r = copy.deepcopy(ring)
    rng = np.random.default_rng([int(seed), 4242])
    nq = ns = 0
    for e in r.ring_c:
        pb = getattr(e, "PolynomB", None)
        if pb is None or getattr(e, "Length", 0.0) <= 0:
            continue
        pb = np.array(pb, float)
        cls = type(e).__name__
        if cls == "Quadrupole" and len(pb) > 1 and pb[1] != 0:
            pb[1] *= 1 + rng.normal(0, quad_rel); nq += 1
        elif cls == "Sextupole" and len(pb) > 2 and pb[2] != 0:
            pb[2] *= 1 + rng.normal(0, sext_rel); ns += 1
        else:
            continue
        e.PolynomB = pb
    return r, nq, ns


def ring_diagnostics(ring, turns):
    lin = ring.ring_c.disable_6d(copy=True)
    tunes = [float(v) for v in lin.get_tune()[:2]]
    xs = np.arange(-16.0, 16.01, 0.5) * 1e-3
    b = np.zeros((6, len(xs))); b[0] = xs; b += np.asarray(ring.orbit6)[:, None]
    _, _, info = ring.ring_c.track(b, nturns=turns, losses=True, in_place=True)
    ok = ~np.asarray(info["loss_map"]["islost"], bool)
    neg = xs[(xs < 0)][::-1]; pos = xs[xs > 0]
    da_neg = next((float(x) for x, k in zip(neg, ok[xs < 0][::-1]) if not k), None)
    da_pos = next((float(x) for x, k in zip(pos, ok[xs > 0]) if not k), None)
    return {"tunes": tunes, "first_unstable_x_neg_m": da_neg, "first_unstable_x_pos_m": da_pos, "da_grid_m": 5e-4}


def run_job(job):
    t0 = time.perf_counter()
    root = Path(job["repo_root"])
    cfg = InjectionStudyConfig.from_dict(job["config"])
    ring = cached_ring(cfg, root, Path(job["work_dir"]))
    out = {k: job[k] for k in ("stage", "label", "seed") if k in job}
    if job.get("ring_error_seed") is not None:
        ring, nq, ns = apply_ring_errors(ring, job["ring_error_seed"], job["quad_rel"], job["sext_rel"])
        out.update({"ring_error_seed": job["ring_error_seed"], "quad_rel": job["quad_rel"], "sext_rel": job["sext_rel"],
                    "n_quads": nq, "n_sexts": ns, "ring": ring_diagnostics(ring, job["turns"])})
    beam = _beam(job, cfg, ring)
    kicker = FilamentNKMKicker(cfg, n_slices=job["n_slices"], vertical_kick=not job.get("no_vertical_kick", False))
    res = track_injection(cfg, ring, kicker, beam, "element", n_turns=job["turns"])
    out.update({"n": res["n_particles"], "captured": res["captured"], "loss_causes": res["loss_causes"],
                "first_loss_turn": res["first_loss_turn"], "turns": job["turns"],
                "chamber_half_x_m": cfg.chamber_half_x_m, "chamber_half_y_m": cfg.chamber_half_y_m,
                "runtime_s": time.perf_counter() - t0})
    return out


def summarise(rows, key):
    groups = {}
    for r in rows:
        groups.setdefault(r[key], []).append(r)
    out = {}
    for k, rs in groups.items():
        n = sum(r["n"] for r in rs); c = sum(r["captured"] for r in rs)
        lo, hi = wilson_interval(c, n)
        causes = {}
        for r in rs:
            for kk, vv in r["loss_causes"].items():
                causes[kk] = causes.get(kk, 0) + vv
        out[str(k)] = {"n": n, "captured": c, "capture": c / n, "ci95": [lo, hi], "loss_causes": causes,
                       "reconciles": n == c + causes.get("septum_creation", 0) + causes.get("outside_field_map", 0) + causes.get("ring", 0)}
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True, help="Final operating point (3-D matched)")
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--stages", nargs="+", choices=("particles", "longturn", "aperture", "ring_errors"), required=True)
    p.add_argument("--big-particles", type=int, default=2000)
    p.add_argument("--big-seed", type=int, default=5001)
    p.add_argument("--long-seeds", nargs="+", type=int, default=[1001, 1002])
    p.add_argument("--long-particles", type=int, default=500)
    p.add_argument("--long-turns", type=int, default=4000)
    p.add_argument("--chunk", type=int, default=100, help="Particles per job when a bunch is split")
    p.add_argument("--apertures-mm", nargs="+", type=float, default=[15.0, 12.0, 11.0, 10.0])
    p.add_argument("--aperture-half-y-mm", type=float, default=5.0)
    p.add_argument("--aperture-seeds", nargs="+", type=int, default=[1001, 1002])
    p.add_argument("--ring-error-seeds", type=int, default=10)
    p.add_argument("--ring-error-levels", nargs="+", type=float, default=[5e-4, 1e-3], help="Quadrupole relative σ")
    p.add_argument("--sext-rel", type=float, default=1e-3)
    p.add_argument("--particles", type=int, default=500)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--n-slices", type=int, default=640)
    p.add_argument("--no-vertical-kick", action="store_true", help="Diagnostic: suppress the NKM vertical kick")
    p.add_argument("--workers", "-w", type=int, default=1)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args(argv)
    out = a.output_dir.resolve(); out.mkdir(parents=True, exist_ok=True)
    cfg = InjectionStudyConfig.load(a.study_config)
    sel = load_optimization_handoff(a.optimization_summary)
    bts = {"bts_config": sel.bts.to_dict(), "initial_twiss": sel.initial_twiss}
    work = out / "_lattice"
    cached_ring(cfg, a.repo_root, work)
    base = {"repo_root": str(a.repo_root), "work_dir": str(work), "bts": bts, "n_slices": a.n_slices,
            "no_vertical_kick": a.no_vertical_kick}
    meta = {"study_config": cfg.to_dict(), "cli": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(a).items()},
            "input_sha256": input_hashes(a.repo_root, ("kickmap_file.txt", cfg.ring_source)),
            "kicker": "wire_field.FilamentNKMKicker", "loss_definition":
            "not alive after the last turn; categories reconcile with the particle count"}

    def split(stage, label, seed, n, turns, config=cfg, **extra):
        return [{**base, "stage": stage, "label": label, "seed": seed, "particles": n, "turns": turns,
                 "slice": (lo, min(n, lo + a.chunk)), "config": config.to_dict(), **extra} for lo in range(0, n, a.chunk)]

    for stage in a.stages:
        if (out / f"{stage}_raw.json").exists():
            raise SystemExit(f"{stage}_raw.json exists")
        t0 = time.time()
        if stage == "particles":
            jobs = split(stage, f"n{a.big_particles}", a.big_seed, a.big_particles, a.turns)
            key = "label"
        elif stage == "longturn":
            jobs = sum((split(stage, f"seed{s}", s, a.long_particles, a.long_turns) for s in a.long_seeds), [])
            key = "label"
        elif stage == "aperture":
            from dataclasses import replace
            jobs = []
            for ax in a.apertures_mm:
                c = replace(cfg, chamber_half_x_m=ax * 1e-3, chamber_half_y_m=a.aperture_half_y_mm * 1e-3)
                for s in a.aperture_seeds:
                    jobs.append({**base, "stage": stage, "label": f"{ax:g}mm", "seed": s, "particles": a.particles,
                                 "turns": a.turns, "config": c.to_dict()})
            key = "label"
        else:
            jobs = []
            for q in a.ring_error_levels:
                for k in range(a.ring_error_seeds):
                    jobs.append({**base, "stage": stage, "label": f"q{q:g}_s{a.sext_rel:g}_seed{k}", "seed": 1001,
                                 "particles": a.particles, "turns": a.turns, "config": cfg.to_dict(),
                                 "ring_error_seed": k, "quad_rel": q, "sext_rel": a.sext_rel})
            key = "label"
        rows = parallel_map(run_job, jobs, n_workers=a.workers, desc=f"C4 {stage}")
        payload = {**meta, "stage": stage, "rows": rows, "summary": summarise(rows, key), "runtime_s": time.time() - t0}
        (out / f"{stage}_raw.json").write_text(json.dumps(payload) + "\n")
        print(f"[{stage}] done in {payload['runtime_s']:.0f} s", flush=True)


if __name__ == "__main__":
    main()
