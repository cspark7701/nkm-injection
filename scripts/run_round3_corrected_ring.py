#!/usr/bin/env python3
"""E5 — corrected ring-error population with BPM references, converged orbit and optics correction.

Same error draws as round 2 (``apply_errors`` with seeds 5501–5510 and the same staged ten-step ramp), so the ring
identities are preserved. The correction chain per seed:

1. BPM readings referenced to the adjacent quadrupole centre (beam-based alignment) with a declared Gaussian residual
   ``--bba-residual-um`` per plane;
2. converged truncated-SVD orbit correction with the 120 HVC correctors (stop when the larger-plane rms improves by
   less than 1 % per iteration);
3. beta-beat and dispersion correction with individual quadrupole gradients (Gauss–Newton, fixed Jacobian);
4. bounded Q11/Q12 tune correction to the ideal tunes, then a final converged orbit correction.

No skew correctors exist in the lattice, so coupling is not corrected (stated). Native 6-D DA: one particle per
0.5 mm in x over ±16 mm, 500 turns, septum aperture only (the chamber enters in the capture studies). Units: m, rad.
"""
import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import time

import at
import numpy as np

from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig, cached_ring
from nkm_injection.ring_error_scenario import (RingErrorScenario, apply_errors, bpm_orbit, bpm_reference_offsets,
                                               correct_optics, correct_orbit_converged, correct_tunes, response_matrix)


def _optics_summary(lin, bpms, beta0, disp0, nkm_index=0):
    _, _, l = lin.get_optics(refpts=bpms)
    bb = (l.beta - beta0) / beta0
    _, _, ln = lin.get_optics(refpts=[nkm_index])
    return {"beta_beat_rms": [float(bb[:, 0].std()), float(bb[:, 1].std())],
            "beta_beat_max": [float(np.abs(bb[:, 0]).max()), float(np.abs(bb[:, 1]).max())],
            "dispersion_rms_m": float(np.sqrt(np.mean((l.dispersion[:, 0] - disp0) ** 2))),
            "nkm_beta_m": [float(ln.beta[0, 0]), float(ln.beta[0, 1])], "nkm_alpha": [float(ln.alpha[0, 0]), float(ln.alpha[0, 1])],
            "tunes": [float(v) for v in lin.get_tune()[:2]], "chromaticities": [float(v) for v in lin.get_chrom()[:2]]}


def correct_seed(job):
    t0 = time.time()
    base_ring = job["base_ring"]; seed = job["seed"]; cfg = job["scenario"]
    bpms, correctors, quads = job["bpms"], job["correctors"], job["quads"]
    response, beta0, disp0, target = job["response"], job["beta0"], job["disp0"], job["target_tunes"]
    commissioning = []; previous = np.zeros((len(correctors), 2))
    for fraction in np.linspace(.1, 1., 10):
        stage = replace(cfg, **{k: getattr(cfg, k) * fraction for k in
                                ("girder_offset_std_m", "magnet_offset_std_m", "roll_std_rad", "gradient_rel_std",
                                 "sextupole_rel_std", "skew_quad_relative_std")})
        lattice, errors = apply_errors(base_ring, seed, stage); lin = lattice.disable_6d(copy=True)
        for j, index in enumerate(correctors):
            lin[index].KickAngle = previous[j].copy()
        offsets = bpm_reference_offsets(lin, errors, bpms, job["bba_residual_m"], seed)
        step = correct_orbit_converged(lin, bpms, correctors, response, offsets, cfg)
        commissioning.append({"error_fraction": float(fraction), "correction": step})
        previous = np.array([lin[index].KickAngle for index in correctors])
    before = _optics_summary(lin, bpms, beta0, disp0)
    optics = correct_optics(lin, bpms, quads, beta0, disp0)
    orbit_after_optics = correct_orbit_converged(lin, bpms, correctors, response, offsets, cfg)
    qf = lin.get_uint32_index("Q11"); qd = lin.get_uint32_index("Q12")
    tune = correct_tunes(lin, [qf, qd], target, tolerance=cfg.tune_tolerance)
    final_orbit = correct_orbit_converged(lin, bpms, correctors, response, offsets, cfg)
    after = _optics_summary(lin, bpms, beta0, disp0)
    for dst, src in zip(lattice, lin):
        if hasattr(src, "KickAngle"): dst.KickAngle = src.KickAngle.copy()
        if hasattr(src, "PolynomB"): dst.PolynomB = src.PolynomB.copy()
    orbit6, _ = lattice.find_orbit6()
    raw = bpm_orbit(lin, bpms); n = len(bpms)
    xs = np.arange(-16., 16.01, .5) * 1e-3
    b = np.zeros((6, len(xs))); b[0] = xs; b += orbit6[:, None]
    _, _, loss = lattice.track(b, nturns=job["turns"], losses=True, in_place=True)
    alive = ~np.asarray(loss["loss_map"]["islost"], bool)
    neg = xs[(xs < 0) & ~alive]; pos = xs[(xs > 0) & ~alive]
    first_neg = float(neg.max()) if len(neg) else None; first_pos = float(pos.min()) if len(pos) else None
    at.save_mat(lattice, job["out"] / f"seed{seed}.mat")
    row = {"seed": seed, "scenario": asdict(cfg), "bba_residual_m": job["bba_residual_m"],
           "commissioning": commissioning, "optics_before": before, "optics_correction": optics,
           "orbit_after_optics": orbit_after_optics, "tune_correction": tune, "final_orbit": final_orbit,
           "optics_after": after,
           "orbit_rms_relative_to_references_m": [final_orbit["history"][-1]["rms_x_m"], final_orbit["history"][-1]["rms_y_m"]],
           "orbit_rms_relative_to_design_axis_m": [float(np.sqrt(np.mean(raw[:n] ** 2))), float(np.sqrt(np.mean(raw[n:] ** 2)))],
           "closed_orbit_at_nkm_m": [float(orbit6[0]), float(orbit6[2])],
           "tune_residual": (np.asarray(after["tunes"]) - target).tolist(),
           "da_x_m": xs.tolist(), "da_alive": alive.tolist(), "first_unstable_negative_m": first_neg,
           "first_unstable_positive_m": first_pos, "turns": job["turns"],
           "feasible": bool(not final_orbit["saturated"] and tune["feasible"]),
           "coupling_correction": "none (no skew correctors in the lattice)",
           "loss_definition": "native AT loss before final turn; septum aperture only",
           "observation": "NKM centre", "runtime_s": time.time() - t0}
    (job["out"] / f"seed{seed}.json").write_text(json.dumps(row, indent=2, allow_nan=False) + "\n")
    print(seed, "orbit ref %.1f/%.1f um" % tuple(1e6 * np.asarray(row["orbit_rms_relative_to_references_m"])),
          "beat %.1f/%.1f %%" % tuple(100 * np.asarray(after["beta_beat_rms"])), "DA", first_neg, first_pos, flush=True)
    return row


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--study-config", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--seeds", nargs="+", type=int, default=list(range(5501, 5511)))
    p.add_argument("--bba-residual-um", type=float, default=10.0)
    p.add_argument("--turns", type=int, default=500)
    p.add_argument("--workers", type=int, default=5)
    a = p.parse_args(argv)
    out = a.output_dir
    if out.exists() and any(out.iterdir()):
        raise SystemExit("--output-dir must be new or empty")
    out.mkdir(parents=True)
    base = cached_ring(InjectionStudyConfig.load(a.study_config), Path.cwd(), out / "_lattice")
    ideal = base.ring_c.disable_6d(copy=True)
    bpms = np.array([i for i, e in enumerate(ideal) if "BPM" in e.FamName])
    correctors = np.array([i for i, e in enumerate(ideal) if isinstance(e, at.Corrector)])
    quads = np.array([i for i, e in enumerate(ideal) if isinstance(e, at.Quadrupole)])
    if len(correctors) != 120 or len(bpms) == 0:
        raise RuntimeError("Expected 120 HVC correctors and BPM markers")
    _, _, l0 = ideal.get_optics(refpts=bpms)
    print("Building coupled numerical orbit response", flush=True)
    response = response_matrix(ideal, bpms, correctors); np.save(out / "response.npy", response)
    jobs = [{"base_ring": base.ring_c, "seed": s, "scenario": RingErrorScenario(), "bpms": bpms,
             "correctors": correctors, "quads": quads, "response": response, "beta0": l0.beta.copy(),
             "disp0": l0.dispersion[:, 0].copy(), "target_tunes": np.asarray(ideal.get_tune())[:2],
             "bba_residual_m": a.bba_residual_um * 1e-6, "turns": a.turns, "out": out} for s in a.seeds]
    rows = parallel_map(correct_seed, jobs, n_workers=a.workers, desc="E5 seeds")
    summary = {"rows": rows, "seeds": a.seeds, "source_sha256": hashlib.sha256(Path("K4GSR_HBIv4-1.mat").read_bytes()).hexdigest(),
               "bpm_count": int(len(bpms)), "corrector_count": int(len(correctors)), "quadrupole_count": int(len(quads)),
               "bba_residual_m": a.bba_residual_um * 1e-6, "passed": all(r["feasible"] for r in rows),
               "scope": "selected error/correction scenario with BPM references, orbit, optics and tune correction; "
                        "no coupling correction; not an as-built KLS prediction"}
    (out / "corrected_ring_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
