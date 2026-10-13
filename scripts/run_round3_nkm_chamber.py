#!/usr/bin/env python3
"""E4 — capture sensitivity to the flat in-magnet NKM chamber (ideal ring, design beam, fixed operating point).

The arc, centre-bend, IVU and injection-straight apertures are the round-2 reference profile. Only the flat chamber
inside the magnet (half-width ``--half-x-mm``, half-heights ``--half-y-mm``) is varied; ``none`` repeats the round-2
conductor-exclusion model. Each case tracks the 3-D NKM and the paired dipole control on two 500-particle bunches
(seeds 1001/1002) for 500 native turns. Units: m, rad; capture fractions.
"""
import argparse
import importlib.util
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

from nkm_injection.chamber import ChamberProfile, apply_chamber
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig, cached_ring, wilson_interval
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.ring_error_scenario import refresh_prepared_ring
from nkm_injection.wire_field import FilamentGeometry, calibrate_controls

_spec = importlib.util.spec_from_file_location("run_round2_chamber", Path(__file__).resolve().parent / "run_round2_chamber.py")
_d6 = importlib.util.module_from_spec(_spec)
sys.modules["run_round2_chamber"] = _d6  # workers unpickle run_capture_case by module name
_spec.loader.exec_module(_d6)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--optimization-summary", type=Path, required=True)
    p.add_argument("--chamber-config", type=Path, required=True, help="round-3 chamber JSON (ChamberProfile fields)")
    p.add_argument("--half-x-mm", type=float, default=16.0)
    p.add_argument("--half-y-mm", nargs="+", default=["none", "3.0", "3.4", "3.8", "4.3"])
    p.add_argument("--particles", type=int, default=500)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--chunk", type=int, default=100)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args(argv)
    out = a.output_dir
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    out.mkdir(parents=True)
    cfg = InjectionStudyConfig.load(a.study_config)
    sel = load_optimization_handoff(a.optimization_summary)
    reference = ChamberProfile(**{k: v for k, v in json.loads(a.chamber_config.read_text()).items()
                                  if not k.startswith("nkm_magnet")})
    base = cached_ring(cfg, Path.cwd(), out / "_lattice")
    calibration = calibrate_controls(cfg)
    geometry = FilamentGeometry()
    rows = []
    for label in a.half_y_mm:
        if label == "none":
            profile = reference
        else:
            profile = replace(reference, nkm_magnet_half_x_m=a.half_x_mm * 1e-3, nkm_magnet_half_y_m=float(label) * 1e-3)
            allowance = 1.5e-3 if float(label) <= 3.8 else 1.0e-3
            profile.validate_against_wires(geometry, allowance_m=allowance)
        # The in-magnet chamber acts on the injection pass (kicker) and on every later turn (ring NKM_H1/NKM_H2).
        chamber, assignment = apply_chamber(base.ring_c, profile, cfg.septum_edge_x_m)
        ring = refresh_prepared_ring(base, chamber)
        jobs = [{"config": cfg.to_dict(), "ring": ring, "seed": seed, "bts": sel.bts.to_dict(),
                 "initial_twiss": sel.initial_twiss, "particles": a.particles, "turns": a.turns, "model": model,
                 "calibration": calibration, "ring_label": "ideal", "profile_label": f"nkm_y{label}",
                 "chamber": asdict(profile), "kicker_chamber": profile.kicker_kwargs(),
                 "chunk": (lo, min(a.particles, lo + a.chunk))}
                for seed in (1001, 1002) for model in ("fieldmap_3d", "dipole") for lo in range(0, a.particles, a.chunk)]
        case = parallel_map(_d6.run_capture_case, jobs, n_workers=a.workers, desc=f"E4 nkm_y{label}")
        (out / f"nkm_y{label}.json").write_text(json.dumps({"rows": case}, indent=2, allow_nan=False) + "\n")
        rows.extend(case)
    summary = {}
    for r in rows:
        key = (r["profile"], r["model"])
        s = summary.setdefault(key, {"captured": 0, "n": 0, "magnet_losses": 0})
        s["captured"] += r["captured"]; s["n"] += r["n_particles"]
        s["magnet_losses"] += r["loss_causes"].get("outside_field_map", 0)
    table = [{"profile": k[0], "model": k[1], **v, "capture": v["captured"] / v["n"],
              "ci95": list(wilson_interval(v["captured"], v["n"]))} for k, v in sorted(summary.items())]
    for t in table:
        print(t["profile"], t["model"], round(100 * t["capture"], 1), "magnet losses", t["magnet_losses"])
    (out / "nkm_chamber_scan.json").write_text(json.dumps({
        "rows": rows, "summary": table, "half_x_m": a.half_x_mm * 1e-3, "study_config": cfg.to_dict(),
        "reference_chamber": asdict(reference), "assignment": assignment,
        "allowance": "1.5 mm (Sun et al. 2020) for half-heights <= 3.8 mm; 1.0 mm for the optimistic 4.3 mm bound",
        "statistical_unit": "particle (Wilson)", "turns": a.turns, "seeds": [1001, 1002],
        "observation": "NKM centre", "loss_definition": "native AT loss, septum, or in-magnet chamber/conductor"},
        indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
