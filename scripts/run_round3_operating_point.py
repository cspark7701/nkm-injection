#!/usr/bin/env python3
"""E6 — re-select the operating point for the design beam on the corrected-ring population and NKM chamber.

Declared before any run:

* **Clearance rule.** The injected centroid at the septum exit keeps ``--clearance-sigma`` (default 3) rms beam
  widths of the design beam (sigma_x from the BTS-exit beam, including dispersion) from the blade's outer face:
  x_inj <= septum_edge - thickness - n sigma_x. Two blades: 2 mm (study geometry, primary) and 1 mm (KLS baseline
  thin septum, alternative).
* **Knobs.** x_inj at the clearance limit and 0.25, 0.5 and 1.0 mm further out; S in {0.80, ..., 1.00}; x' is the
  inner matched root of the 3-D magnet (zero centroid angle after the magnet) for each (x_inj, S).
* **Objective.** Tenth percentile of capture over the corrected rings (primary) and mean (tie-break), with the declared
  chamber including the flat NKM chamber. Selection bunch: ``--selection-particles`` (100) per ring, seed 3001,
  500 turns, NKM only.
* **Validation.** Selected points and the round-2 point on fresh 2 x 500-particle bunches (seeds 1001/1002) on the
  ideal ring and every corrected ring; the paired dipole control at the primary (2 mm blade) point.

Units: m, rad; capture fractions.
"""
import argparse
from dataclasses import asdict, replace
import json
import math
from pathlib import Path

import at
import numpy as np

from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.chamber import ChamberProfile, apply_chamber
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig, booster_beam, cached_ring, track_bts
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.ring_error_scenario import refresh_prepared_ring
from nkm_injection.wire_field import calibrate_controls
from run_operating_window_3d import LEVER, matched_angle_3d
from run_round2_chamber import run_capture_case


def septum_sigma_x(cfg, sel, particles=20000, seed=77):
    """rms horizontal width (m) of the design beam at the BTS exit (septum), from transported particles."""
    bts = create_bts_lattice(BTSConfig.from_dict(sel.bts.to_dict()))
    beam = track_bts(bts, booster_beam(sel.initial_twiss, cfg.injected_beam, particles, seed))
    return float(np.nanstd(beam[0]))


def ring_population(base, profile, cfg, ring_dir):
    rings = {}
    lattice, _ = apply_chamber(base.ring_c, profile, cfg.septum_edge_x_m)
    rings["ideal"] = refresh_prepared_ring(base, lattice)
    summary = json.loads((ring_dir / "corrected_ring_summary.json").read_text())
    for s in summary["seeds"]:
        lattice, _ = apply_chamber(at.load_mat(ring_dir / f"seed{s}.mat"), profile, cfg.septum_edge_x_m)
        rings[f"seed{s}"] = refresh_prepared_ring(base, lattice)
    return rings


def jobs_for(cfg, rings, ring_labels, sel, profile, calibration, label, seeds, particles, models, chunk):
    return [{"config": cfg.to_dict(), "ring": rings[r], "seed": seed, "bts": sel.bts.to_dict(),
             "initial_twiss": sel.initial_twiss, "particles": particles, "turns": 500, "model": model,
             "calibration": calibration, "ring_label": r, "profile_label": label, "chamber": asdict(profile),
             "kicker_chamber": profile.kicker_kwargs(), "chunk": (lo, min(particles, lo + chunk))}
            for r in ring_labels for seed in seeds for model in models for lo in range(0, particles, chunk)]


def fractions(rows, label):
    out = {}
    for r in rows:
        if r["profile"] != label:
            continue
        k = (r["ring"], r["model"]); v = out.setdefault(k, [0, 0]); v[0] += r["captured"]; v[1] += r["n_particles"]
    return {f"{k[0]}|{k[1]}": v[0] / v[1] for k, v in out.items()}


def redo_dipole(a):
    path = a.redo_validation; payload = json.loads(path.read_text())
    cfg0 = InjectionStudyConfig.load(a.study_config); sel = load_optimization_handoff(a.optimization_summary)
    profile = ChamberProfile(**json.loads(a.chamber_config.read_text()))
    base = cached_ring(cfg0, Path.cwd(), path.parent / "_lattice")
    rings = ring_population(base, profile, cfg0, a.ring_dir)
    cfg = InjectionStudyConfig.from_dict(json.loads((path.parent / "operating_point_selected_b2.json").read_text()))
    rows = parallel_map(run_capture_case, jobs_for(cfg, rings, list(rings), sel, profile, calibrate_controls(cfg),
                                                   "selected_b2", (1001, 1002), 500, ("dipole",), 100),
                        n_workers=a.workers, desc="E6 dipole revalidation")
    kept = [r for r in payload["validation_rows"] if not (r["profile"] == "selected_b2" and r["model"] == "dipole")]
    payload["superseded_dipole_rows"] = [r for r in payload["validation_rows"] if r["profile"] == "selected_b2" and r["model"] == "dipole"]
    payload["validation_rows"] = kept + rows
    payload["validation"] = {label: fractions(payload["validation_rows"], label) for label in payload["validation"]}
    payload["control_calibration"] = "dipole control calibrated to the 3-D centroid response at the validated point"
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    print("selected_b2 dipole", {k: round(v, 3) for k, v in payload["validation"]["selected_b2"].items() if k.endswith("dipole")})


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--chamber-config", type=Path, required=True)
    p.add_argument("--ring-dir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--clearance-sigma", type=float, default=3.0)
    p.add_argument("--scales", nargs="+", type=float, default=[0.80, 0.85, 0.90, 0.95, 1.00])
    p.add_argument("--steps-mm", nargs="+", type=float, default=[0.0, 0.25, 0.5, 1.0])
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--n-slices", type=int, default=640)
    p.add_argument("--selection-particles", type=int, default=100)
    p.add_argument("--redo-validation", type=Path, default=None,
                   help="existing operating_point_selection.json: recompute only the selected_b2 dipole validation with the "
                        "control calibrated at that point, and write it back (fix for runs before per-point calibration)")
    a = p.parse_args(argv)
    if a.redo_validation:
        return redo_dipole(a)
    out = a.output_dir
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    out.mkdir(parents=True)
    cfg0 = InjectionStudyConfig.load(a.study_config); sel = load_optimization_handoff(a.optimization_summary)
    profile = ChamberProfile(**json.loads(a.chamber_config.read_text()))
    base = cached_ring(cfg0, Path.cwd(), out / "_lattice")
    rings = ring_population(base, profile, cfg0, a.ring_dir)
    corrected = [k for k in rings if k != "ideal"]
    sigma = septum_sigma_x(cfg0, sel)
    candidates, skipped = [], []
    for blade in (0.002, 0.001):
        x_max = cfg0.septum_edge_x_m - blade - a.clearance_sigma * sigma
        for step in a.steps_mm:
            for s in a.scales:
                c = replace(cfg0, septum_thickness_m=blade, injection_x_m=round(x_max - step * 1e-3, 7), field_scale=s)
                xp = matched_angle_3d(c, a.n_slices)
                centroid = None if xp is None else c.injection_x_m + LEVER * xp
                if xp is None or abs(centroid) > 0.012:
                    skipped.append({"blade_m": blade, "x_inj_m": c.injection_x_m, "S": s,
                                    "reason": "no inner matched root" if xp is None else "centroid outside DA"})
                    continue
                candidates.append({"label": f"b{blade*1e3:g}_x{c.injection_x_m*1e3:.3f}_S{s:.2f}", "blade_m": blade,
                                   "config": replace(c, injection_xp_rad=xp), "centroid_m": centroid})
    print("sigma_x at septum", sigma, "candidates", len(candidates), "skipped", len(skipped), flush=True)
    calibration = calibrate_controls(cfg0)
    selection_rows = []
    for cand in candidates:
        rows = parallel_map(run_capture_case, jobs_for(cand["config"], rings, corrected, sel, profile, calibration,
                                                       cand["label"], (3001,), a.selection_particles, ("fieldmap_3d",), 100),
                            n_workers=a.workers, desc=f"E6 select {cand['label']}")
        caps = np.array([v for v in fractions(rows, cand["label"]).values()])
        cand.update({"p10": float(np.quantile(caps, 0.1)), "mean": float(caps.mean()), "per_ring": fractions(rows, cand["label"])})
        selection_rows.extend(rows)
        print(cand["label"], "p10 %.3f mean %.3f" % (cand["p10"], cand["mean"]), flush=True)
        (out / "selection_partial.json").write_text(json.dumps(
            [{k: (v.to_dict() if k == "config" else v) for k, v in c.items()} for c in candidates if "p10" in c], indent=2) + "\n")
    selected = {}
    for blade in (0.002, 0.001):
        pool = [c for c in candidates if c["blade_m"] == blade]
        if pool:
            selected[blade] = max(pool, key=lambda c: (c["p10"], c["mean"]))
    points = {"round2": cfg0, **{f"selected_b{b*1e3:g}": c["config"] for b, c in selected.items()}}
    validation_rows = []
    for label, cfg in points.items():
        models = ("fieldmap_3d", "dipole") if label == "selected_b2" else ("fieldmap_3d",)  # paired control at the primary
        # The controls are calibrated to the 3-D centroid response at each validated point, not at the round-2 point.
        validation_rows.extend(parallel_map(run_capture_case, jobs_for(cfg, rings, list(rings), sel, profile, calibrate_controls(cfg),
                                                                       label, (1001, 1002), 500, models, 100),
                                            n_workers=a.workers, desc=f"E6 validate {label}"))
    validation = {label: fractions(validation_rows, label) for label in points}
    for label, cfg in points.items():
        (out / f"operating_point_{label}.json").write_text(json.dumps(cfg.to_dict(), indent=2) + "\n")
    payload = {"sigma_x_septum_m": sigma, "clearance_sigma": a.clearance_sigma,
               "candidates": [{k: (v.to_dict() if k == "config" else v) for k, v in c.items()} for c in candidates],
               "skipped": skipped, "selected": {f"{b*1e3:g}mm": c["label"] for b, c in selected.items()},
               "primary": "selected_b2", "validation": validation, "validation_rows": validation_rows,
               "selection_rows": selection_rows, "chamber": asdict(profile), "rings": list(rings),
               "objective": f"p10 of capture over corrected rings (primary), mean (tie-break); {a.selection_particles} particles per ring, seed 3001",
               "statistical_unit": "particle within ring; ring for population descriptors", "turns": 500}
    (out / "operating_point_selection.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
