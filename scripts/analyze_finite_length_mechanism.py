#!/usr/bin/env python3
"""C2 — Mechanism of the thin/finite-length difference (reviewer tasks R1-03, R2-1c).

Single-centroid analysis at the operating point (no ring tracking). The horizontal kick profile K(x) is the
straight-line integrated kick of the RADIA map (bicubic, y = 0). Four models are compared, each at its own matched
injection angle (zero centroid angle after the magnet):

* ``thin``      — K(x_c) applied at the magnet centre (kick-map model);
* ``straight``  — kick density K(x)/L distributed over L but sampled on the undeflected straight line (path-slope
                  averaging only);
* ``bent``      — the same density sampled on the self-consistent deflected trajectory (uniform-profile finite
                  magnet; equals the 1-D thick model);
* ``3d``        — exact filament field (wire_field.FilamentNKMKicker), all field components and fringes.

Outputs: matched angles, Courant–Snyder amplitude of the kicked centroid at the NKM centre against septum angle and
position errors, the trajectory and local kick density inside the magnet, the sagitta K L/8, and a magnet-length
scan of the ``bent`` model at fixed integrated kick (L = 0.2–1.0 m). Units: m, rad; amplitudes in m.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from nkm_injection.injection_study import InjectionStudyConfig, KickModelEvaluator, _apply_kick
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.stage_cli import input_hashes
from nkm_injection.wire_field import FilamentNKMKicker

REPO = Path(__file__).resolve().parent.parent
BETA_X, ALPHA_X = 16.27, -0.145  # ring optics at the NKM centre (physics_model.md)


def amplitude(x, xp):
    g = (1 + ALPHA_X ** 2) / BETA_X
    return float(np.sqrt(BETA_X * (g * x * x + 2 * ALPHA_X * x * xp + BETA_X * xp * xp)))


class Models:
    def __init__(self, cfg, root, n_slices=640):
        self.cfg, self.lever = cfg, cfg.septum_to_nkm_drift_m + 0.2625
        ev = KickModelEvaluator("fieldmap", cfg, NKMKickMap2D(root / cfg.kickmap_path), cfg.nkm_entry_x_m,
                                interpolation="cubic")
        self.K = lambda x: float(ev.kicks(np.array([x]), np.array([0.0]))[0][0])
        self.k3 = FilamentNKMKicker(cfg, n_slices=n_slices)

    def exit(self, model, xp, dx=0.0, length=0.525, n=400, record=False):
        """Centroid (x, x') at the NKM centre after the kick, for septum angle xp and position error dx."""
        xc = self.cfg.injection_x_m + dx + self.lever * xp
        if model == "thin":
            return xc, xp + self.K(xc)
        if model == "3d":
            b = np.zeros((6, 1)); b[0] = xc; b[1] = xp
            _apply_kick(b, self.k3, self.cfg.closed_orbit_x_m)
            return float(b[0, 0]), float(b[1, 0])
        x, p, ds, path = xc - 0.5 * length * xp, xp, length / n, []
        for i in range(n):
            s = -0.5 * length + (i + 0.5) * ds
            x += 0.5 * ds * p
            xs = xc + s * xp if model == "straight" else x
            k = self.K(xs) / length
            if record:
                path.append((s, xs, k))
            p += k * ds
            x += 0.5 * ds * p
        out = (x - 0.5 * length * p, p)
        return (out, path) if record else out

    def matched(self, model, **kw):
        """Inner (largest) root of the exit angle in [xp0 − 2.5 mrad, xp0 + 1 mrad]; None if there is none."""
        f = lambda xp: self.exit(model, xp, **kw)[1]
        grid = self.cfg.injection_xp_rad + np.linspace(-2.5e-3, 1e-3, 71)
        vals = [f(x) for x in grid]
        roots = [brentq(f, grid[i], grid[i + 1], xtol=1e-12) for i in range(len(grid) - 1)
                 if np.sign(vals[i]) != np.sign(vals[i + 1])]
        return max(roots) if roots else None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(argv)
    if a.output.exists():
        raise SystemExit("output exists; choose a new path")
    cfg = InjectionStudyConfig.load(a.study_config)
    m = Models(cfg, a.repo_root)
    models = ("thin", "straight", "bent", "3d")
    matched = {k: m.matched(k) for k in models}
    dxp = np.round(np.arange(-0.6, 0.6001, 0.05), 3) * 1e-3
    dx = np.round(np.arange(-1.0, 1.0001, 0.1), 2) * 1e-3
    out = {"study_config": cfg.to_dict(), "optics_at_nkm": {"beta_x_m": BETA_X, "alpha_x": ALPHA_X},
           "input_sha256": input_hashes(a.repo_root, ("kickmap_file.txt",)),
           "matched_angle_rad": matched, "angle_error_rad": dxp.tolist(), "position_error_m": dx.tolist(),
           "amplitude_vs_angle_m": {k: [amplitude(*m.exit(k, matched[k] + d)) for d in dxp] for k in models},
           "amplitude_vs_position_m": {k: [amplitude(*m.exit(k, matched[k], dx=d)) for d in dx] for k in models}}
    k_nom = m.K(cfg.injection_x_m + m.lever * matched["thin"])
    out["sagitta_m"] = {"definition": "|K| L / 8 for a uniformly distributed kick", "value": abs(k_nom) * 0.525 / 8}
    traj = {}
    for d in (-3e-4, 0.0, 3e-4):
        for model in ("straight", "bent"):
            _, path = m.exit(model, matched["bent"] + d, record=True)
            traj[f"{model}_{d * 1e3:+.1f}mrad"] = [[float(s), float(x), float(k)] for s, x, k in path[::8]]
    out["trajectories_s_x_kickdensity"] = traj
    xs = np.linspace(-0.0115, -0.0065, 101)
    out["kick_profile"] = {"x_m": xs.tolist(), "kick_rad": [m.K(x) for x in xs]}
    scan = {}
    for length in (0.2, 0.35, 0.525, 0.75, 1.0):
        xm = m.matched("bent", length=length)
        if xm is None:
            scan[f"{length:.3f}"] = {"matched_angle_rad": None, "sagitta_m": abs(k_nom) * length / 8}
            continue
        amps = [amplitude(*m.exit("bent", xm + d, length=length)) for d in (-3e-4, 0.0, 3e-4)]
        scan[f"{length:.3f}"] = {"matched_angle_rad": xm, "amp_minus03_m": amps[0], "amp_nominal_m": amps[1],
                                 "amp_plus03_m": amps[2], "sagitta_m": abs(k_nom) * length / 8}
    out["length_scan_bent_fixed_integral"] = scan
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"matched_mrad": {k: v * 1e3 for k, v in matched.items()}, "sagitta_mm": out["sagitta_m"]["value"] * 1e3,
                      "length_scan": {k: {kk: (None if vv is None else round(vv * 1e3, 3)) for kk, vv in v.items()} for k, v in scan.items()}}, indent=1))


if __name__ == "__main__":
    main()
