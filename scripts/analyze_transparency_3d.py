#!/usr/bin/env python3
"""C7 — Stored-beam transparency from the exact 3-D field (reviewer tasks R1-07, R2-8).

Deterministic analysis: straight-line kicks of the exact filament field averaged over the Gaussian
  stored beam with tensor Gauss–Hermite quadrature (no sampling noise). For horizontal and vertical NKM–orbit
  offsets: centroid kicks, centroid amplitudes A_u = β_u |⟨Δu'⟩| in units of σ_u, rms kick spreads and filamented
  emittance growth in both planes. Also the near-axis multipole expansion of K(x, 0), the interpolation error of the
  bilinear/bicubic kick map, and the Monte Carlo standard error of the earlier 10⁵-particle estimate.
The tracked multi-turn check is in ``scripts/track_stored_beam_3d.py``.

Stored beam at the NKM centre: horizontal emittance, energy spread and Twiss from the ring model; the vertical
emittance is a declared assumption (``--emit-y-ratio`` × ε_x; the uncoupled model has ε_y ≈ 0). Units: m, rad.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np

from nkm_injection.injection_study import InjectionStudyConfig, KickModelEvaluator, cached_ring
from nkm_injection.kickmap import NKMKickMap2D
from nkm_injection.stage_cli import input_hashes
from nkm_injection.wire_field import FilamentNKMField, brho_T_m

REPO = Path(__file__).resolve().parent.parent


def beam_optics(ring, emit_y_ratio):
    bx, ax = ring.twiss_x
    by, ay = ring.twiss_y
    ex = ring.emit_x_m_rad
    ey = emit_y_ratio * ex
    return {"beta_x": bx, "alpha_x": ax, "beta_y": by, "alpha_y": ay, "emit_x": ex, "emit_y": ey,
            "sigma_x": float(np.sqrt(ex * bx)), "sigma_y": float(np.sqrt(ey * by))}


def gh_nodes(n):
    t, w = np.polynomial.hermite_e.hermegauss(n)  # probabilists' Hermite: weight exp(-t²/2)
    return t, w / w.sum()


def response(kick_fn, opt, dx, dy, n=40):
    """Deterministic beam averages for the NKM offset (dx, dy) relative to the stored orbit."""
    t, w = gh_nodes(n)
    X, Y = np.meshgrid(t * opt["sigma_x"], t * opt["sigma_y"], indexing="ij")
    W = np.outer(w, w)
    kx, ky = kick_fn(X.ravel() - dx, Y.ravel() - dy)
    kx, ky, W = kx.reshape(X.shape), ky.reshape(X.shape), W
    out = {}
    for plane, u, k, beta, alpha, emit, sig in (("x", X, kx, opt["beta_x"], opt["alpha_x"], opt["emit_x"], opt["sigma_x"]),
                                                 ("y", Y, ky, opt["beta_y"], opt["alpha_y"], opt["emit_y"], opt["sigma_y"])):
        gamma = (1 + alpha ** 2) / beta
        kbar = float(np.sum(W * k))
        var = float(np.sum(W * (k - kbar) ** 2))
        # <J> after the kick about the new centroid; x' | x is Gaussian with mean −α x/β and variance ε/β
        m = -alpha * u / beta + (k - kbar)
        jmean = float(np.sum(W * (gamma * u ** 2 + 2 * alpha * u * m + beta * (m ** 2 + emit / beta))))
        out[plane] = {"mean_kick_rad": kbar, "rms_kick_spread_rad": float(np.sqrt(var)),
                      "centroid_amplitude_m": beta * abs(kbar), "amplitude_over_sigma": beta * abs(kbar) / sig if sig > 0 else None,
                      "filamented_emittance_growth": jmean / 2 / emit - 1.0 if emit > 0 else None}
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--emit-y-ratio", type=float, default=0.1, help="Assumed ε_y/ε_x of the stored beam")
    p.add_argument("--offsets-mm", nargs="+", type=float, default=[0.0, 0.05, 0.1, 0.2, 0.3, 0.5])
    p.add_argument("--gh-nodes", type=int, default=40)
    p.add_argument("--repo-root", type=Path, default=REPO)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(argv)
    if a.output.exists():
        raise SystemExit("output exists")
    t0 = time.time()
    cfg = InjectionStudyConfig.load(a.study_config)
    import tempfile
    ring = cached_ring(cfg, a.repo_root, Path(tempfile.mkdtemp()))
    opt = beam_optics(ring, a.emit_y_ratio)
    f = FilamentNKMField()
    g = cfg.kicker_polarity * cfg.field_scale / brho_T_m(cfg.energy_eV)

    def exact(x, y):
        ibx, iby = f.line_integrals(np.asarray(x), np.asarray(y), s_max_m=5.0)
        return g * iby, -g * ibx

    km = NKMKickMap2D(a.repo_root / cfg.kickmap_path)
    maps = {interp: KickModelEvaluator("fieldmap", cfg, km, cfg.nkm_entry_x_m, interpolation=interp) for interp in ("linear", "cubic")}
    out = {"study_config": cfg.to_dict(), "optics": opt, "emit_y_assumption": f"emit_y = {a.emit_y_ratio} emit_x",
           "input_sha256": input_hashes(a.repo_root, ("kickmap_file.txt", cfg.ring_source)), "gh_nodes": a.gh_nodes}
    rows = []
    for d in a.offsets_mm:
        r = {"dx_m": d * 1e-3, "dy_m": 0.0, "exact": response(exact, opt, d * 1e-3, 0.0, a.gh_nodes)}
        for interp, ev in maps.items():
            r[f"map_{interp}"] = response(lambda x, y, ev=ev: ev.kicks(x, y), opt, d * 1e-3, 0.0, a.gh_nodes)
        rows.append(r)
    for d in (0.1, 0.2):
        rows.append({"dx_m": 0.0, "dy_m": d * 1e-3, "exact": response(exact, opt, 0.0, d * 1e-3, a.gh_nodes)})
    out["offset_response"] = rows
    # quadrature convergence at 0.2 mm
    out["gh_convergence_dx0.2mm"] = {n: response(exact, opt, 2e-4, 0.0, n)["x"]["amplitude_over_sigma"] for n in (20, 30, 40, 60)}
    # near-axis multipoles of the exact kick K(x, 0) and K(0, y)
    xs = np.linspace(-2e-3, 2e-3, 81)
    kx_line, _ = exact(xs, np.zeros_like(xs))
    coeff = np.polynomial.polynomial.polyfit(xs, kx_line, 7)
    resid = kx_line - np.polynomial.polynomial.polyval(xs, coeff)
    out["near_axis_fit"] = {"range_m": 2e-3, "coefficients_rad_per_m^k": coeff.tolist(), "max_residual_rad": float(np.max(np.abs(resid))),
                            "note": "K(x,0) = sum c_k x^k; by the mirror symmetry of the four loops the even coefficients vanish"}
    xb = np.linspace(-0.25e-3, 0.25e-3, 11)
    out["map_interpolation_error_near_axis"] = {
        interp: float(np.max(np.abs(ev.kicks(xb, np.zeros_like(xb))[0] - exact(xb, np.zeros_like(xb))[0]))) for interp, ev in maps.items()}
    k0 = rows[0]["exact"]["x"]
    out["monte_carlo_standard_error_1e5"] = {
        "sem_mean_kick_rad": k0["rms_kick_spread_rad"] / np.sqrt(1e5),
        "sem_amplitude_over_sigma": opt["beta_x"] * k0["rms_kick_spread_rad"] / np.sqrt(1e5) / opt["sigma_x"],
        "note": "standard error of a 1e5-particle sample mean of the kick for the aligned beam"}
    out["runtime_s"] = time.time() - t0
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2) + "\n")
    for r in rows:
        e = r["exact"]
        print(f"dx={r['dx_m']*1e3:.2f} dy={r['dy_m']*1e3:.2f}  Ax/sx={e['x']['amplitude_over_sigma']:.3e} Ay/sy={e['y']['amplitude_over_sigma']}"
              f"  dex={e['x']['filamented_emittance_growth']:.2e} dey={e['y']['filamented_emittance_growth']:.2e}"
              + (f"  map_lin={r['map_linear']['x']['amplitude_over_sigma']:.3e} map_cub={r['map_cubic']['x']['amplitude_over_sigma']:.3e}" if 'map_linear' in r else ""))
    print(json.dumps({k: out[k] for k in ("gh_convergence_dx0.2mm", "map_interpolation_error_near_axis", "monte_carlo_standard_error_1e5")}, indent=1))
    print("near-axis coeffs", np.array(coeff))


if __name__ == "__main__":
    main()
