#!/usr/bin/env python3
"""
Task 07 — Deterministic BTS Quadrupole Optimization Script

Performs physically-constrained 2-stage optimization (Least-Squares + SLSQP)
with feasibility-first candidate selection, multi-start global search using
distinct seeds, Jacobian sensitivity analysis, and saves results under
results/bts_publication_optimization/run_<timestamp>/.

Saved outputs
-------------
- bts_optimization_summary.json   : final selected solution + metadata
- candidate_table.json             : all candidates (feasible and infeasible)
- config.json                      : reproducibility metadata
"""

import sys
import json
import datetime
import hashlib
import subprocess
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.nkm_injection.optimization import (
    BTSOptimizationConfig,
    optimize_bts_quadrupoles,
    compute_sensitivity_matrix,
    round_strengths,
)
from src.nkm_injection.constraints import BTSConstraintConfig


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        ).strip()
    except Exception:
        return "unknown"


def _input_hash(path: Path) -> str:
    """SHA-256 of a source file (first 16 hex chars)."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except Exception:
        return "unknown"


def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = (
        repo_root / "results" / "bts_publication_optimization" / f"run_{timestamp}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== Deterministic BTS Quadrupole Optimization (Task 07) ===")
    print(f"Output directory: {output_dir}")

    config = BTSOptimizationConfig(
        random_seed=42,
        max_iter=20,
        constraint_config=BTSConstraintConfig(),
    )

    # ----------------------------------------------------------------
    # 1. Multi-start optimization  (3 starts: nominal + 2 random)
    # ----------------------------------------------------------------
    print("\nRunning 2-stage optimization (Least-Squares + SLSQP, 3 starts) …")
    res = optimize_bts_quadrupoles(method="least_squares", config=config, n_starts=3)

    print(f"\nOptimization success      : {res.success}")
    print(f"Feasible candidates found : {res.n_feasible_found}/{res.n_total_starts}")
    print(f"Initial Merit J           : {res.initial_merit:.4f}")
    print(f"Final Merit J             : {res.final_merit:.4f}")
    print(f"Final Mismatch X / Y      : {res.final_mismatch_x:.6f} / {res.final_mismatch_y:.6f}")
    print(f"Peak Beta X               : {res.final_max_beta_x:.2f} m")
    print(f"Peak Beta Y               : {res.final_max_beta_y:.2f} m")
    print(f"Constraints satisfied     : {res.constraints_satisfied}")
    if res.violations:
        print("Violations:")
        for v in res.violations:
            print(f"  ✗ {v}")

    rounded_k = round_strengths(res.optimized_strengths, decimals=6)
    print(f"\nOptimized Quad Strengths K [m^-2]:\n{rounded_k}")

    # ----------------------------------------------------------------
    # 2. Jacobian Sensitivity Matrix
    # ----------------------------------------------------------------
    print("\nComputing Jacobian sensitivity matrix …")
    sens = compute_sensitivity_matrix(res.optimized_strengths, config=config)
    print(f"Jacobian Condition Number : {sens['condition_number']:.2f}")
    print(f"Singular Values           : {sens['singular_values']}")

    # ----------------------------------------------------------------
    # 3. Save candidate table (all starts, feasible + infeasible)
    # ----------------------------------------------------------------
    candidate_table_data = [c.as_dict() for c in res.candidate_table]
    candidate_path = output_dir / "candidate_table.json"
    with open(candidate_path, "w") as f:
        json.dump(candidate_table_data, f, indent=2)
    print(f"\nSaved candidate table     : {candidate_path}")

    # ----------------------------------------------------------------
    # 4. Save main summary JSON
    # ----------------------------------------------------------------
    summary_data = {
        "timestamp": timestamp,
        "method": res.method,
        "success": res.success,
        "n_feasible_found": res.n_feasible_found,
        "n_total_starts": res.n_total_starts,
        "initial_merit": res.initial_merit,
        "final_merit": res.final_merit,
        "final_mismatch_x": res.final_mismatch_x,
        "final_mismatch_y": res.final_mismatch_y,
        "final_max_beta_x_m": res.final_max_beta_x,
        "final_max_beta_y_m": res.final_max_beta_y,
        "final_disp_x_residual_m": res.final_disp_x_residual,
        "constraints_satisfied": res.constraints_satisfied,
        "violations": res.violations,
        "optimized_strengths_raw": res.optimized_strengths.tolist(),
        "optimized_strengths_rounded": rounded_k.tolist(),
        "sensitivity": {
            "condition_number": sens["condition_number"],
            "singular_values": sens["singular_values"].tolist(),
            "jacobian_matrix": sens["jacobian_matrix"].tolist(),
        },
    }
    json_path = output_dir / "bts_optimization_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved optimization summary: {json_path}")

    # ----------------------------------------------------------------
    # 5. Save reproducibility config
    # ----------------------------------------------------------------
    config_data = {
        "timestamp": timestamp,
        "git_commit": _git_commit(),
        "random_seed": config.random_seed,
        "max_iter": config.max_iter,
        "n_starts": res.n_total_starts,
        "method": res.method,
        "quad_bounds_global": list(config.quad_bounds),
        "beta_max_limit_m": config.constraint_config.beta_max_limit_m,
        "mismatch_limit": config.constraint_config.mismatch_limit,
        "input_files": {
            "kickmap_file.txt": _input_hash(repo_root / "kickmap_file.txt"),
        },
    }
    cfg_path = output_dir / "config.json"
    with open(cfg_path, "w") as f:
        json.dump(config_data, f, indent=2)
    print(f"Saved reproducibility cfg : {cfg_path}")
    print("\n=== Done ===")


if __name__ == "__main__":
    main()
