#!/usr/bin/env python3
"""E8 — physical synthesis: capture against the margin between the ring's dynamic aperture and the injected amplitude.

For every E6 selection candidate (x_inj, S, matched x') the injected centroid's betatron amplitude at the NKM centre is
computed from its state just after the 3-D magnet, A = sqrt(x^2 + (alpha x + beta x')^2) with the NKM optics of each
corrected ring. The margin is |first unstable negative launch| (E5, septum only, 500 turns) minus A. Capture of each
candidate on each corrected ring (E6 selection bunch: same particles, chamber, no injection errors) is paired with that
margin. A logistic fit of capture versus margin tests whether that margin organizes capture (it is reported even when
it does not). Ring-level correlates of validated capture at the selected point (residual beta-beat, orbit, NKM closed
orbit, chromaticity, DA edges) are tabulated with Spearman coefficients for the NKM and the dipole control.
Deterministic inputs plus finite-particle capture fractions; no new tracking. Units: m, rad.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.wire_field import FilamentNKMKicker
from run_operating_window_3d import LEVER, centroid_exit


def logistic(m, m50, width):
    return 1.0 / (1.0 + np.exp(-(m - m50) / width))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--selection", type=Path, required=True)
    p.add_argument("--ring-dir", type=Path, required=True)
    p.add_argument("--targets", type=float, nargs="+", default=[0.8, 0.9])
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(argv)
    if a.output.exists():
        raise SystemExit("output exists")
    sel = json.loads(a.selection.read_text())
    rings = {f"seed{r['seed']}": r for r in json.loads((a.ring_dir / "corrected_ring_summary.json").read_text())["rows"]}
    points = []
    for cand in sel["candidates"]:
        cfg = InjectionStudyConfig.from_dict(cand["config"])
        x, px = centroid_exit(cfg, FilamentNKMKicker(cfg, n_slices=640), cfg.injection_xp_rad)
        for label, capture in cand["per_ring"].items():
            ring = label.split("|")[0]
            r = rings[ring]; beta, alpha = r["optics_after"]["nkm_beta_m"][0], r["optics_after"]["nkm_alpha"][0]
            co = r["closed_orbit_at_nkm_m"][0]
            xr = x - co
            amp = float(np.hypot(xr, alpha * xr + beta * px))
            da = abs(r["first_unstable_negative_m"])
            points.append({"candidate": cand["label"], "ring": ring, "blade_m": cand["blade_m"], "amplitude_m": amp,
                           "da_edge_m": da, "margin_m": da - amp, "capture": capture})
    m = np.array([q["margin_m"] for q in points]); c = np.array([q["capture"] for q in points])
    (m50, width), cov = curve_fit(logistic, m, c, p0=[0.0, 2e-4], bounds=([-5e-3, 1e-6], [5e-3, 5e-3]))
    required = {f"{t:g}": float(m50 + width * np.log(t / (1 - t))) for t in a.targets}
    rho = float(np.corrcoef(np.argsort(np.argsort(m)), np.argsort(np.argsort(c)))[0, 1])
    out = {"points": points, "fit": {"model": "capture = 1/(1+exp(-(margin-m50)/width))", "m50_m": float(m50),
                                     "width_m": float(width), "cov": np.asarray(cov).tolist()},
           "required_margin_m": required, "spearman_margin_capture": rho, "n_points": len(points),
           "lever_m": LEVER, "scope": "E6 selection bunches (100 particles per ring, seed 3001), corrected rings, chamber, no injection errors",
           "units": "m; capture fractions"}
    val = sel["validation"]["selected_b2"]; table = []
    for label, r in rings.items():
        o = r["optics_after"]
        table.append({"ring": label, "nkm": val[f"{label}|fieldmap_3d"], "dipole": val.get(f"{label}|dipole"),
                      "beta_beat_rms": max(o["beta_beat_rms"]), "orbit_x_m": r["orbit_rms_relative_to_references_m"][0],
                      "orbit_y_m": r["orbit_rms_relative_to_references_m"][1], "co_nkm_x_m": r["closed_orbit_at_nkm_m"][0],
                      "chrom_x": o["chromaticities"][0], "chrom_y": o["chromaticities"][1],
                      "da_neg_m": abs(r["first_unstable_negative_m"]), "da_pos_m": r["first_unstable_positive_m"]})
    corr = {}
    for key in ("beta_beat_rms", "orbit_x_m", "orbit_y_m", "co_nkm_x_m", "chrom_x", "chrom_y", "da_neg_m", "da_pos_m"):
        for model in ("nkm", "dipole"):
            r_s, pv = spearmanr([t[model] for t in table], [t[key] for t in table])
            corr[f"{model}|{key}"] = {"rho": float(r_s), "p": float(pv)}
    out["ring_level"] = {"rows": table, "spearman": corr, "n_rings": len(table),
                         "scope": "selected point, fresh 2 x 500-particle validation, no injection errors"}
    a.output.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print("points", len(points), "m50 %.2f mm width %.2f mm" % (1e3 * m50, 1e3 * width), "required",
          {k: round(1e3 * v, 2) for k, v in required.items()}, "spearman %.2f" % rho)


if __name__ == "__main__":
    main()
