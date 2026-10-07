#!/usr/bin/env python3
"""
Task 06 — Publication Error Model & Tolerance Budget Simulation Script

Runs Monte Carlo ensemble simulations across 5 physical error categories,
evaluates percentiles (p50, p68, p95, p99), computes bootstrap confidence intervals,
ranks dominant error contributors via OAT sensitivity scans, and outputs JSON metrics under
results/publication_tolerances/run_<timestamp>/.
"""

import argparse
import json
import datetime
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

from nkm_injection.optimization_handoff import (
    HANDOFF_UNITS, QUAD_NAMES, load_optimization_handoff, reference_handoff, load_error_budget,
)
from nkm_injection.statistics import StatisticalPolicy, InvalidStatisticalSamplesError
from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble
from nkm_injection.robust_optimization import (
    evaluate_robustness_statistics,
    compute_one_at_a_time_sensitivity
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Publication Error Model & Tolerance Budget Simulation")
    parser.add_argument("-w", "--workers", type=int, default=None,
                        help="Number of parallel CPU worker cores.")
    parser.add_argument("--samples", type=int, default=100,
                        help="Number of Monte Carlo error samples.")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility.")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Override output directory path.")
    parser.add_argument("--kicker-model", choices=("fieldmap", "linear", "ideal", "off"),
                        default="fieldmap", help="Explicit kicker model; never a fallback")
    parser.add_argument("--kickmap-path", type=Path, default=None,
                        help="Selected field map; defaults to the protected repository map")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--optimization-summary", type=Path,
                           help="Selected feasible summary with adjacent complete config.json")
    selection.add_argument("--reference", action="store_true",
                           help="Explicitly use canonical reference optics instead of an optimization")
    parser.add_argument("--error-config", type=Path, default=None,
                        help="Complete ErrorBudgetConfig JSON; default budget is saved explicitly")
    parser.add_argument("--oat-samples", type=int, default=30,
                        help="Number of one-at-a-time samples per category")
    parser.add_argument("--oat-seed", type=int, default=None,
                        help="OAT seed; defaults to the Monte Carlo seed")
    parser.add_argument('--bootstrap-count', type=int, default=1000)
    parser.add_argument('--bootstrap-seed', type=int, default=42)
    parser.add_argument('--ci-level', type=float, default=.95)
    parser.add_argument('--convergence-sizes', type=int, nargs=2, default=(50, 100), metavar=('SMALL', 'LARGE'))
    parser.add_argument('--convergence-tolerance', type=float, default=.05)
    parser.add_argument('--invalid-sample-policy', choices=('exclude', 'raise'), default='exclude')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.samples <= 0 or args.oat_samples <= 0 or args.seed < 0 or (args.oat_seed is not None and args.oat_seed < 0):
        raise ValueError("Sample counts must be positive and seeds non-negative")
    policy = StatisticalPolicy(bootstrap_count=args.bootstrap_count, bootstrap_seed=args.bootstrap_seed,
                               ci_level=args.ci_level, convergence_sizes=tuple(args.convergence_sizes),
                               convergence_tolerance=args.convergence_tolerance,
                               invalid_sample_policy=args.invalid_sample_policy)
    policy.validate()
    selected = reference_handoff() if args.reference else load_optimization_handoff(args.optimization_summary)
    config, error_source = load_error_budget(args.error_config)
    nominal_bts, target_twiss = selected.bts, selected.target_twiss
    optimization_source = selected.source
    oat_seed = args.seed if args.oat_seed is None else args.oat_seed
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_dir = args.output_dir or (repo_root / "results" / "publication_tolerances" / f"run_{timestamp}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Tolerance output directory must be new or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    print("=== NKM Publication Error Model & Tolerance Budget ===")
    print(f"Input mode: {selected.source['mode']}")
    print(f"Output directory: {output_dir}")
    reproducibility = {
        "tolerance_input_schema_version": 1,
        "optimization_source": optimization_source,
        "error_config_source": error_source,
        "nominal_bts_config": nominal_bts.to_dict(),
        "nominal_strengths_by_name_m_minus2": dict(zip(QUAD_NAMES, nominal_bts.quad_strengths_list)),
        "target_config": selected.target.to_dict(),
        "constraint_config": selected.constraints.to_dict(),
        "error_config": config.to_dict(),
        "initial_twiss": selected.initial_twiss,
        "target_twiss": target_twiss,
        "units": dict(HANDOFF_UNITS),
        "statistical_policy": policy.to_dict(),
        "sampling": {"monte_carlo": {"n_samples": args.samples, "seed": args.seed},
                     "oat": {"n_samples_per_category": args.oat_samples, "seed": oat_seed},
                     "bootstrap": {"seed": policy.bootstrap_seed, "replicates": policy.bootstrap_count,
                                   "ci_level": policy.ci_level, "estimator": "median_mismatch_x"}},
    }

    # 1. Fast Monte Carlo Ensemble
    n_samples = args.samples
    print(f"\nSampling Monte Carlo ensemble (N={n_samples}, workers={args.workers})...\n")
    samples = sample_error_ensemble(config, n_samples=n_samples, seed=args.seed)

    evaluation_kwargs = {"statistical_policy": policy, "n_workers": args.workers, "initial_twiss": selected.initial_twiss,
                         "beta_max_limit_m": selected.constraints.beta_max_limit_m,
                         "mismatch_limit": selected.constraints.mismatch_limit,
                         "mismatch_definition": "sum", "beta_tolerance_m": .01, "mismatch_tolerance": .05}
    if args.kicker_model != "fieldmap" or args.kickmap_path is not None:
        evaluation_kwargs.update(kicker_model=args.kicker_model, kickmap_path=args.kickmap_path)
    try:
        stats = evaluate_robustness_statistics(nominal_bts, target_twiss, samples, **evaluation_kwargs)
    except InvalidStatisticalSamplesError as error:
        # Archive the rejected ensemble without rerunning any physics evaluations.
        stats = error.summary
    print(f"Invalid evaluations: {stats.get('n_invalid_evaluations', 0)}")
    if stats.get("n_invalid_evaluations", 0):
        diagnostic_path = output_dir / "publication_tolerances_summary.json"
        diagnostic_path.write_text(json.dumps({**reproducibility, "timestamp": timestamp, "seed": args.seed,
            "workers": args.workers, "optimization_source": optimization_source,
            "n_samples": n_samples, "robustness_statistics": stats,
            "sensitivity_ranking": {}}, indent=2, allow_nan=False) + "\n")
        failed_ids = [r["outcome"]["identity"]["sample_id"] for r in stats["sample_results"]
                      if r["outcome"]["status"] == "invalid"]
        raise RuntimeError(f"Invalid evaluations for samples {failed_ids}; diagnostics: {diagnostic_path}")

    print("\n--- Monte Carlo Robustness Percentiles ---\n")
    print(f"Failure Probability: {stats['failure_probability']*100:.1f}%")
    print(f"Horizontal Mismatch Mx: p50={stats['mismatch_x']['p50_median']:.4f}, p68={stats['mismatch_x']['p68']:.4f}, p95={stats['mismatch_x']['p95']:.4f}, p99={stats['mismatch_x']['p99']:.4f}")
    print(f"Vertical Mismatch My:   p50={stats['mismatch_y']['p50_median']:.4f}, p68={stats['mismatch_y']['p68']:.4f}, p95={stats['mismatch_y']['p95']:.4f}, p99={stats['mismatch_y']['p99']:.4f}")
    interval = stats['mismatch_x'].get('bootstrap_ci_median', stats['mismatch_x'].get('bootstrap_95ci_median'))
    print(f"Bootstrap {policy.ci_level:.0%} CI for Median Mx: [{interval[0]:.4f}, {interval[1]:.4f}]")
    print(f"\n--- Failure Modes ---\n")
    for fm, count in stats.get("failure_modes", {}).items():
        print(f"  {fm}: {count}")
    print(f"\n--- MC Convergence ---\n")
    conv = stats.get("convergence_check", {})
    print(f"  Prefix stability status: {conv.get('status', 'unavailable')}")
    print(f"  Within configured tolerance: {conv.get('converged')}")
    print(f"  Compared sample sizes: {conv.get('sample_sizes', list(policy.convergence_sizes))}")
    print(f"  Absolute difference: {conv.get('absolute_difference')}")

    # 2. One-At-A-Time Sensitivity Ranking
    print("\n--- One-At-A-Time (OAT) Sensitivity Ranking ---\n")
    rankings = compute_one_at_a_time_sensitivity(nominal_bts, target_twiss, n_samples=args.oat_samples, seed=oat_seed, n_workers=args.workers,
        error_config=config, initial_twiss=selected.initial_twiss)
    for rank, (label, val) in enumerate(rankings.items(), start=1):
        print(f"{rank}. {label:35s}: Delta Merit = {val:.6f}")

    summary_data = {
        **reproducibility,
        "timestamp": timestamp,
        "seed": args.seed,
        "workers": args.workers,
        "optimization_source": optimization_source,
        "n_samples": n_samples,
        "robustness_statistics": stats,
        "sensitivity_ranking": rankings
    }

    json_path = output_dir / "publication_tolerances_summary.json"
    with open(json_path, 'w') as f:
        json.dump(summary_data, f, indent=2, allow_nan=False)
    print(f"\nSaved summary JSON: {json_path}")


if __name__ == "__main__":
    main()
