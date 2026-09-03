#!/usr/bin/env python3
"""
Task 06 — Publication Error Model & Tolerance Budget Simulation Script

Runs Monte Carlo ensemble simulations across 5 physical error categories,
evaluates percentiles (p50, p68, p95, p99), computes bootstrap confidence intervals,
ranks dominant error contributors via OAT sensitivity scans, and outputs JSON metrics under
results/publication_tolerances/run_<timestamp>/.
"""

import argparse
import sys
import json
import datetime
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.nkm_injection.bts_lattice import BTSConfig
from src.nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble
from src.nkm_injection.robust_optimization import (
    evaluate_robustness_statistics,
    compute_one_at_a_time_sensitivity
)


def parse_args():
    parser = argparse.ArgumentParser(description="Publication Error Model & Tolerance Budget Simulation")
    parser.add_argument("-w", "--workers", type=int, default=None,
                        help="Number of parallel CPU worker cores.")
    parser.add_argument("--samples", type=int, default=100,
                        help="Number of Monte Carlo error samples.")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility.")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Override output directory path.")
    return parser.parse_args()


def main():
    args = parse_args()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir or (repo_root / "results" / "publication_tolerances" / f"run_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== NKM Publication Error Model & Tolerance Budget ===")
    print(f"Output directory: {output_dir}")

    config = ErrorBudgetConfig()
    
    # Check for optimized BTS quadrupole strengths from Step 5
    opt_runs = sorted((repo_root / "results" / "bts_publication_optimization").glob("run_*/bts_optimization_summary.json"))
    if opt_runs:
        with open(opt_runs[-1]) as f:
            opt_data = json.load(f)
        k_opt = opt_data.get("optimized_strengths_raw", None)
        if k_opt and len(k_opt) >= 9:
            nominal_bts = BTSConfig(
                k_q11=k_opt[0], k_q12=k_opt[1], k_q13=k_opt[2],
                k_q21=k_opt[3], k_q22=k_opt[4], k_q23=k_opt[5],
                k_q31=k_opt[6], k_q32=k_opt[7], k_q33=k_opt[8]
            )
        else:
            nominal_bts = BTSConfig()
    else:
        nominal_bts = BTSConfig()

    target_twiss = {"beta": [2.336495, 4.256241], "alpha": [-0.016335, 0.017772]}

    # 1. Fast Monte Carlo Ensemble
    n_samples = args.samples
    print(f"\nSampling Monte Carlo ensemble (N={n_samples}, workers={args.workers})...\n")
    samples = sample_error_ensemble(config, n_samples=n_samples, seed=args.seed)

    stats = evaluate_robustness_statistics(nominal_bts, target_twiss, samples, n_workers=args.workers)

    print("\n--- Monte Carlo Robustness Percentiles ---\n")
    print(f"Failure Probability: {stats['failure_probability']*100:.1f}%")
    print(f"Horizontal Mismatch Mx: p50={stats['mismatch_x']['p50_median']:.4f}, p68={stats['mismatch_x']['p68']:.4f}, p95={stats['mismatch_x']['p95']:.4f}, p99={stats['mismatch_x']['p99']:.4f}")
    print(f"Vertical Mismatch My:   p50={stats['mismatch_y']['p50_median']:.4f}, p68={stats['mismatch_y']['p68']:.4f}, p95={stats['mismatch_y']['p95']:.4f}, p99={stats['mismatch_y']['p99']:.4f}")
    print(f"Bootstrap 95% CI for Median Mx: [{stats['mismatch_x']['bootstrap_95ci_median'][0]:.4f}, {stats['mismatch_x']['bootstrap_95ci_median'][1]:.4f}]")
    print(f"\n--- Failure Modes ---\n")
    for fm, count in stats.get("failure_modes", {}).items():
        print(f"  {fm}: {count}")
    print(f"\n--- MC Convergence ---\n")
    conv = stats.get("convergence_check", {})
    print(f"  Converged: {conv.get('converged', False)}")
    print(f"  Diff N=50 to N=100: {conv.get('N_50_to_100_diff', 0.0):.6f}")

    # 2. One-At-A-Time Sensitivity Ranking
    print("\n--- One-At-A-Time (OAT) Sensitivity Ranking ---\n")
    rankings = compute_one_at_a_time_sensitivity(nominal_bts, target_twiss, n_samples=30, seed=args.seed, n_workers=args.workers)
    for rank, (label, val) in enumerate(rankings.items(), start=1):
        print(f"{rank}. {label:35s}: Delta Merit = {val:.6f}")

    summary_data = {
        "timestamp": timestamp,
        "n_samples": n_samples,
        "robustness_statistics": stats,
        "sensitivity_ranking": rankings
    }

    json_path = output_dir / "publication_tolerances_summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    print(f"\nSaved summary JSON: {json_path}")


if __name__ == "__main__":
    main()
