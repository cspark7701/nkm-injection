#!/usr/bin/env python3
"""
Task 03 — Thick-Element NKM Tracking Convergence Study Script

Evaluates tracking convergence across slice counts N_slices = [10, 20, 40, 80, 160]
for reference particle trajectories, beam centroids, RMS sizes, projected emittances,
loss fractions, and stored beam perturbations.
"""

import argparse
import json
import datetime
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent

from nkm_injection.units import compute_rigidity
from nkm_injection.fieldmap import NKMFieldMap1D, load_1d_fieldmap
from nkm_injection.beam import generate_6d_beam, compute_beam_statistics
from nkm_injection.tracking import track_nkm_thick_symplectic, track_nkm_thick_rk4


from nkm_injection.stage_cli import add_source_argument, source_root, stage_output, input_hashes, check_seed

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="NKM slicing convergence (sequential)")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument('--tier', choices=('smoke', 'pilot', 'production'), default='production')
    add_source_argument(parser)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    root = source_root(args, repo_root)
    check_seed(args.seed)
    hashes = input_hashes(root, ("By.txt",))
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = stage_output(args, root, 'tracking_convergence')
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== NKM Thick-Element Tracking Convergence Study ===")
    print(f"Output directory: {output_dir}")

    # Load 1D field map By.txt
    by_path = root / "By.txt"
    x_by, by_vals = load_1d_fieldmap(by_path)
    fmap = NKMFieldMap1D(x_by, by_vals)

    def field_fn(x, y, z):
        by = fmap.evaluate(x)
        bx = np.zeros_like(x)
        return by, bx

    slice_counts = [10, 20, 40] if args.tier == 'smoke' else [10, 20, 40, 80, 160]
    n_particles = {'smoke': 16, 'pilot': 100, 'production': 1000}[args.tier]
    length_m = 0.525
    energy_GeV = 4.0

    # 1. Single reference particle at nominal injection offset x = -16.0 mm
    ref_in = np.zeros((6, 1))
    ref_in[0, 0] = -0.016

    # 2. Injected beam distribution (1000 particles)
    beam_inj_in = generate_6d_beam(
        n_particles=n_particles,
        beta_x=10.0, alpha_x=0.0, emit_x=1e-7,
        beta_y=5.0, alpha_y=0.0, emit_y=1e-8,
        x_offset=-0.016,
        seed=args.seed
    )

    # 3. Stored beam reference at x = 0.0 mm
    stored_in = np.zeros((6, 1))

    results_by_slice = []

    for i, n_slices in enumerate(slice_counts):
        if i > 0:
            print()
        # Track reference injected particle
        ref_out = track_nkm_thick_symplectic(ref_in, field_fn, length_m=length_m, n_slices=n_slices, energy_GeV=energy_GeV)
        ref_x_exit_mm = float(ref_out[0, 0] * 1e3)
        ref_xp_exit_mrad = float(ref_out[1, 0] * 1e3)

        # Track injected beam distribution
        beam_inj_out = track_nkm_thick_symplectic(beam_inj_in, field_fn, length_m=length_m, n_slices=n_slices, energy_GeV=energy_GeV)
        inj_stats = compute_beam_statistics(beam_inj_out)

        # Track stored beam reference
        stored_out = track_nkm_thick_symplectic(stored_in, field_fn, length_m=length_m, n_slices=n_slices, energy_GeV=energy_GeV)
        stored_kick_mrad = float(stored_out[1, 0] * 1e3)

        res = {
            "n_slices": n_slices,
            "ref_x_exit_mm": ref_x_exit_mm,
            "ref_xp_exit_mrad": ref_xp_exit_mrad,
            "inj_centroid_x_mm": inj_stats["centroid"]["x_mm"],
            "inj_centroid_xp_mrad": inj_stats["centroid"]["xp_mrad"],
            "inj_rms_x_mm": inj_stats["std_dev"]["sigma_x_mm"],
            "inj_emitt_x_mrad": inj_stats["emittance_x_mrad"],
            "inj_survival_fraction": inj_stats["survival_fraction"],
            "stored_kick_mrad": stored_kick_mrad
        }
        results_by_slice.append(res)
        print(f"N_slices={n_slices:3d}: Exit xp={ref_xp_exit_mrad:8.5f} mrad | Stored kick={stored_kick_mrad:8.5e} mrad")

    summary_output = {
        "timestamp": timestamp,
        "seed": args.seed,
        "tier": args.tier,
        "n_particles": n_particles,
        "distribution": {"beta_x_m": 10., "alpha_x": 0., "emit_x_m_rad": 1e-7,
                         "beta_y_m": 5., "alpha_y": 0., "emit_y_m_rad": 1e-8,
                         "energy_spread": 1.1e-3, "bunch_length_m": .0134, "x_offset_m": -.016},
        "energy_eV": energy_GeV*1e9, "length_m": length_m,
        "input_sha256": hashes,
        "observation_point": "NKM exit",
        "recommended_slices_policy": "configured production standard; not inferred from smoke results",
        "execution_mode": "sequential",
        "slice_counts": slice_counts,
        "results": results_by_slice,
        "recommended_production_slices": 40
    }

    json_path = output_dir / "tracking_convergence_summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary_output, f, indent=2)
    print(f"Saved summary JSON: {json_path}")


if __name__ == "__main__":
    main()
