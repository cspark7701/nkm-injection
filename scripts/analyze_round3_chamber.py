#!/usr/bin/env python3
"""E4 — normalised vertical/horizontal apertures (half-aperture / sqrt(beta)) of every declared chamber region.

Uses the ideal ring with the round-3 chamber profile (linear optics, 4-D). The in-magnet NKM chamber is evaluated with
the optics at the NKM centre. Output: ``aperture_normalisation.json`` (mm m^-1/2). Units: m.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from nkm_injection.chamber import ChamberProfile, apply_chamber
from nkm_injection.injection_study import InjectionStudyConfig, cached_ring


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--chamber-config", type=Path, required=True)
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(argv)
    cfg = InjectionStudyConfig.load(a.study_config)
    c = json.loads(a.chamber_config.read_text())
    profile = ChamberProfile(**c)
    base = cached_ring(cfg, Path.cwd(), a.work_dir)
    ch, meta = apply_chamber(base.ring_c, profile, cfg.septum_edge_x_m)
    lin = ch.disable_6d(copy=True)
    _, _, ld = lin.get_optics(refpts=range(len(lin)))
    regions = {}
    for item in meta["assignments"]:
        i = item["index"]
        r = regions.setdefault(item["region"], {"normalised_y": np.inf, "normalised_x": np.inf, "beta_y_max_m": 0.0})
        r["normalised_y"] = min(r["normalised_y"], 1e3 * item["half_y_m"] / np.sqrt(ld.beta[i, 1]))
        r["normalised_x"] = min(r["normalised_x"], 1e3 * item["half_x_m"] / np.sqrt(ld.beta[i, 0]))
        r["beta_y_max_m"] = max(r["beta_y_max_m"], float(ld.beta[i, 1]))
    bx, by = float(ld.beta[0, 0]), float(ld.beta[0, 1])
    regions["nkm_magnet_chamber"] = {"normalised_y": 1e3 * profile.nkm_magnet_half_y_m / np.sqrt(by),
                                     "normalised_x": 1e3 * profile.nkm_magnet_half_x_m / np.sqrt(bx),
                                     "beta_y_max_m": by}
    closed_ivu = {"normalised_y": 1e3 * 0.0025 / np.sqrt(regions["ivu_3m_segment"]["beta_y_max_m"])}
    out = {"regions": regions, "closed_ivu_stress": closed_ivu, "nkm_beta_m": [bx, by], "chamber": c,
           "units": "mm m^-1/2 (half-aperture / sqrt(beta)); minimum over the region's elements",
           "optics": "ideal ring, linear 4-D"}
    a.output.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    for k, v in regions.items():
        print(k, round(v["normalised_y"], 2), round(v["normalised_x"], 2))


if __name__ == "__main__":
    main()
