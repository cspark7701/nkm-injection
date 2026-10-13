#!/usr/bin/env python3
"""E9 — simultaneous wire-placement and loop-current errors, and the septum-leakage allowance.

Wire Monte Carlo: every one of the eight longitudinal wires is displaced by independent Gaussian (x, y) offsets of rms
``sigma_wire`` (10, 25, 50 um); loop currents receive independent relative errors of rms ``sigma_current`` (0 for
series powering, 1e-4 and 1e-3 for independent loops). For each draw the on-axis integrated kick (exact filament
kernel, infinite span) gives the stored-beam centroid amplitude A/sigma = |k| beta / sigma in each plane, at the NKM
optics and the stored equilibrium emittances (eps_y = ratio x eps_x). Deterministic seeds; 4000 draws per case.

Septum leakage: the dipole kick that keeps the stored-beam centroid at 0.1 sigma_x at the septum location is
0.1 sqrt(eps_x / beta_x); the corresponding uniform leakage field over the thin-septum length is compared with the
published 3.3 G value at the baseline bumped orbit (Hahn et al. 2024). Units: m, rad, T.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from nkm_injection.injection_study import InjectionStudyConfig, cached_ring
from nkm_injection.sliced_vector_map import integrated_filament_kicks
from nkm_injection.wire_field import FilamentGeometry, brho_T_m


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--draws", type=int, default=4000)
    p.add_argument("--septum-length-m", type=float, default=0.4)
    p.add_argument("--published-leakage-T", type=float, default=3.3e-4)
    a = p.parse_args(argv)
    if a.output.exists():
        raise SystemExit("output exists")
    cfg = InjectionStudyConfig.load(a.study_config)
    ring = cached_ring(cfg, Path.cwd(), a.output.parent / "_e9_lattice")
    g = FilamentGeometry()
    betas = np.array([ring.twiss_x[0], ring.twiss_y[0]])
    emits = np.array([ring.emit_x_m_rad, ring.emit_x_m_rad * cfg.stored_vertical_emittance_ratio])
    sigmas = np.sqrt(betas * emits)
    cases = []
    for sw in (10e-6, 25e-6, 50e-6):
        for sc, label in ((0.0, "series"), (1e-4, "independent 1e-4"), (1e-3, "independent 1e-3")):
            rng = np.random.default_rng([int(sw * 1e7), int(sc * 1e6), 9101])
            amps = np.empty((a.draws, 2))
            for i in range(a.draws):
                kx, ky = integrated_filament_kicks(0.0, 0.0, g, cfg.energy_eV, cfg.field_scale, cfg.kicker_polarity,
                                                   wire_offsets_m=rng.normal(0, sw, (8, 2)),
                                                   loop_current_relative=rng.normal(0, sc, 4))
                amps[i] = np.abs([float(kx), float(ky)]) * betas / sigmas
            q = lambda c, f: float(np.quantile(amps[:, c], f))
            cases.append({"sigma_wire_m": sw, "loop_powering": label, "sigma_current_relative": sc,
                          "Ax_over_sigma": {"median": q(0, .5), "p90": q(0, .9)},
                          "Ay_over_sigma": {"median": q(1, .5), "p90": q(1, .9)},
                          "fraction_both_below_0p1": float(np.mean((amps[:, 0] <= .1) & (amps[:, 1] <= .1)))})
            print(sw, label, cases[-1]["Ax_over_sigma"], cases[-1]["Ay_over_sigma"], cases[-1]["fraction_both_below_0p1"])
    # Septum leakage allowance at the septum location of the prepared ring.
    lin = ring.ring_c.disable_6d(copy=True)
    _, _, ls = lin.get_optics(refpts=[ring.septum_index])
    beta_s = float(ls.beta[0, 0])
    allowed_kick = 0.1 * np.sqrt(ring.emit_x_m_rad / beta_s)
    allowed_field = allowed_kick * brho_T_m(cfg.energy_eV) / a.septum_length_m
    out = {"cases": cases, "draws": a.draws, "beta_x_y_m": betas.tolist(), "sigma_x_y_m": sigmas.tolist(),
           "emittances_m_rad": emits.tolist(), "criterion": "centroid amplitude A/sigma per plane; 0.1 reference",
           "septum": {"beta_x_m": beta_s, "allowed_kick_rad": float(allowed_kick), "allowed_field_T": float(allowed_field),
                      "septum_length_m": a.septum_length_m, "published_leakage_T": a.published_leakage_T,
                      "required_reduction_factor": float(a.published_leakage_T / allowed_field),
                      "note": "published value is at the baseline bumped orbit, ~5 mm from the blade; the NKM-scheme "
                              "stored orbit is ~16 mm from it, so the required reduction is a reference, not a prediction"},
           "units": "m, rad, T", "study_config": cfg.to_dict()}
    a.output.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print("septum beta_x %.2f m allowed kick %.2e rad field %.2e T factor %.0f" %
          (beta_s, allowed_kick, allowed_field, a.published_leakage_T / allowed_field))


if __name__ == "__main__":
    main()
