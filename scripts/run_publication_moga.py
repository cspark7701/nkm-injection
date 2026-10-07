#!/usr/bin/env python3
"""
Task 07 — Publication MOGA Pareto Optimization & Multi-Seed Reproducibility Script

Runs multi-seed NSGA-II Pareto optimizations across 5 independent seeds,
enforces strict physical feasibility, evaluates hypervolume convergence histories,
computes Pareto-front and knee-point variability, and archives JSON/CSV results under
results/publication_moga/run_<timestamp>/.
"""

import argparse
import json
import datetime
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent

from nkm_injection.moga import (
    reevaluate_pareto_finalists,
    BTSMOGAConfig,
    run_bts_moga,
    save_moga_results_json
)


from nkm_injection.stage_cli import add_source_argument, source_root, stage_output, input_hashes, check_seed

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Multi-seed publication MOGA (sequential)")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--tier", choices=("smoke", "pilot", "production"), default="production")
    parser.add_argument("--seed", type=int, default=42)
    add_source_argument(parser)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    root = source_root(args, repo_root)
    check_seed(args.seed)
    hashes = input_hashes(root, ("K4GSR_HBIv4-1.mat", "kickmap_file.txt"))
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = stage_output(args, root, 'publication_moga')
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== NKM Publication MOGA Pareto Optimization ===")
    print(f"Output directory: {output_dir}")

    from nkm_injection.storage_ring_injection import StorageRingInjectionConfig, load_storage_ring_injection_lattice
    ring_config = StorageRingInjectionConfig(
        mat_filename=str(output_dir.resolve() / "storage_ring_lattice_nkm.mat"))
    load_storage_ring_injection_lattice(ring_config, source_mat_path=root / "K4GSR_HBIv4-1.mat")
    presets = {"smoke": ([42], 4, 2, 16, 1), "pilot": ([42, 101, 202], 20, 10, 100, 2),
               "production": ([42, 101, 202, 303, 404], 40, 20, 1000, 2)}
    base_seeds, pop_size, n_gen, n_particles, n_mc_seeds = presets[args.tier]
    seeds = [args.seed + value - 42 for value in base_seeds]
    multi_seed_results = {}
    knee_quad_strengths = []

    for i, seed in enumerate(seeds):
        if i > 0:
            print()
        cfg = BTSMOGAConfig(pop_size=pop_size, n_gen=n_gen, seed=seed)
        print(f"--- Running Seed {seed} ---")
        res = run_bts_moga(cfg)

        seed_dir = output_dir / f"seed_{seed}"
        if res.success:
            reevaluate_pareto_finalists(res, n_particles=n_particles, n_mc_seeds=n_mc_seeds, ring_config=ring_config, seed=args.seed)
        save_moga_results_json(res, seed_dir)

        print(f"Seed {seed}: Success={res.success}, Feasible Fraction={res.feasible_fraction*100:.1f}%, Pareto Count={len(res.pareto_x)}")
        if res.success and "knee_point" in res.representative_solutions:
            knee = res.representative_solutions["knee_point"]
            knee_quad_strengths.append(knee["strengths_array"])
            print(f"  Knee Point Mismatch={knee['total_mismatch']:.4f}, Envelope Risk={knee['envelope_risk']:.2f} m")

        multi_seed_results[f"seed_{seed}"] = {
            "success": res.success,
            "feasible_fraction": res.feasible_fraction,
            "pareto_count": len(res.pareto_x),
            "final_hypervolume": res.history_hypervolume[-1] if res.history_hypervolume else 0.0,
            "runtime_seconds": res.runtime_seconds
        }

    if knee_quad_strengths:
        knee_arr = np.array(knee_quad_strengths)
        knee_std = float(np.mean(np.std(knee_arr, axis=0)))
    else:
        knee_std = None

    print(f"\nKnee Point Quad Strength Standard Deviation across seeds: {knee_std if knee_std is not None else 'unavailable'}")

    summary_file = output_dir / "multi_seed_moga_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "seeds": seeds,
            "tier": args.tier,
            "input_sha256": hashes,
            "workload": {"pop_size": pop_size, "n_gen": n_gen, "finalist_particles": n_particles,
                         "finalist_mc_seeds": n_mc_seeds, "finalist_turns": 10, "kicker_model": "ideal"},
            "storage_ring_config": ring_config.to_dict(),
            "seed_metrics": multi_seed_results,
            "knee_count": len(knee_quad_strengths),
            "knee_quad_std": knee_std
        }, f, indent=2, allow_nan=False)
    print(f"Saved multi-seed summary: {summary_file}")


if __name__ == "__main__":
    main()
