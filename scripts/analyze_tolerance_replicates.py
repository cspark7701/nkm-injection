#!/usr/bin/env python3
"""Task 005 — Post-process saved tolerance ensembles without re-running physics.

Reads ``publication_tolerances_summary.json`` files (per-sample results), and reports for each
run and for the pooled ensemble:

* quantiles p50/p95/p99 of M_x, M_y (dimensionless), beta_max (m) and stored kick (mrad), with
  distribution-free order-statistic confidence intervals (exact binomial, primary);
* percentile-bootstrap intervals of the median M_x for several bootstrap seeds (endpoint stability);
* failure counts with exact Clopper-Pearson and Wilson 95 % intervals and the one-sided 95 %
  zero-failure upper bound 1 - 0.05**(1/N);
* prefix stability of the median M_x (absolute and relative change) and independent-seed spread;
* one-at-a-time ranking agreement across seeds.

Valid and physically infeasible samples enter the statistics; invalid samples are excluded and counted.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import stats

METRICS = {"mismatch_x": "mx", "mismatch_y": "my", "max_beta_x_m": "bx_max", "max_beta_y_m": "by_max",
           "stored_kick_mrad": "stored_kick_mrad"}
QUANTILES = (0.5, 0.95, 0.99)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--summaries", nargs="+", type=Path, required=True)
    p.add_argument("--labels", nargs="+", default=None)
    p.add_argument("--bootstrap-seeds", nargs="+", type=int, default=[1729, 2718, 31415])
    p.add_argument("--bootstrap-count", type=int, default=20000)
    p.add_argument("--ci-level", type=float, default=0.95)
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args(argv)


def order_statistic_ci(sorted_x, q, level):
    """Distribution-free CI for the q-quantile from order statistics (exact binomial)."""
    n = len(sorted_x)
    a = (1 - level) / 2
    lo = int(stats.binom.ppf(a, n, q))
    hi = int(stats.binom.ppf(1 - a, n, q)) + 1
    lo, hi = max(lo, 1), min(hi, n)
    return float(sorted_x[lo - 1]), float(sorted_x[hi - 1])


def bootstrap_median(x, seed, count, level, chunk=250):
    rng = np.random.default_rng(seed)
    n, meds = len(x), []
    for start in range(0, count, chunk):
        m = min(chunk, count - start)
        idx = rng.integers(0, n, size=(m, n))
        meds.append(np.median(x[idx], axis=1))
    meds = np.concatenate(meds)
    a = (1 - level) / 2
    return [float(np.quantile(meds, a)), float(np.quantile(meds, 1 - a))]


def failure_bounds(k, n, level=0.95):
    lo = 0.0 if k == 0 else float(stats.beta.ppf((1 - level) / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(1 - (1 - level) / 2, k + 1, n - k))
    z = stats.norm.ppf(1 - (1 - level) / 2)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return {"k": k, "n": n, "estimate": p, "clopper_pearson": [lo, hi], "wilson": [max(0.0, c - h), min(1.0, c + h)],
            "one_sided_95_upper_zero_failure": (1 - 0.05 ** (1 / n)) if k == 0 else None}


def describe(arrays, level):
    out = {}
    for name, x in arrays.items():
        s = np.sort(x)
        out[name] = {"n": int(len(s)), "mean": float(s.mean())}
        for q in QUANTILES:
            out[name][f"p{int(q * 100)}"] = float(np.quantile(s, q))
            out[name][f"p{int(q * 100)}_ci"] = order_statistic_ci(s, q, level)
    return out


def main(argv=None):
    args = parse_args(argv)
    if args.output.exists():
        raise SystemExit("Output exists; choose a new path")
    labels = args.labels or [p.parent.name for p in args.summaries]
    runs, pooled = {}, {k: [] for k in METRICS}
    for label, path in zip(labels, args.summaries):
        raw = path.read_bytes()
        data = json.loads(raw)
        rs = data["robustness_statistics"]
        samples = [s for s in rs["sample_results"] if s["outcome"]["status"] != "invalid"]
        arrays = {k: np.array([s[v] for s in samples], dtype=float) for k, v in METRICS.items()}
        for k in METRICS:
            pooled[k].append(arrays[k])
        mx = arrays["mismatch_x"]
        conv = rs["convergence_check"]
        est = conv.get("prefix_estimates") or [None, None]
        runs[label] = {
            "path": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
            "mc_seed": data["sampling"]["monte_carlo"]["seed"], "n_requested": data["n_samples"],
            "n_invalid": rs["n_invalid_evaluations"],
            "failures": failure_bounds(rs["n_physical_failures"], rs["n_valid_evaluations"]),
            "failure_modes": rs.get("failure_modes", {}),
            "quantiles": describe(arrays, args.ci_level),
            "median_mx_bootstrap": {str(s): bootstrap_median(mx, s, args.bootstrap_count, args.ci_level)
                                    for s in args.bootstrap_seeds},
            "prefix": {"sizes": conv.get("sample_sizes"), "estimates": est,
                       "absolute_change": conv.get("absolute_difference"),
                       "relative_change": (conv["absolute_difference"] / est[-1]) if est[-1] else None,
                       "target": conv.get("tolerance"), "status": conv.get("status")},
            "oat_ranking": list(data.get("sensitivity_ranking", {}).keys()),
            "oat_values": data.get("sensitivity_ranking", {}),
        }
    pooled = {k: np.concatenate(v) for k, v in pooled.items()}
    medians = [r["quantiles"]["mismatch_x"]["p50"] for r in runs.values()]
    total_fail = sum(r["failures"]["k"] for r in runs.values())
    total_n = sum(r["failures"]["n"] for r in runs.values())
    rankings = [r["oat_ranking"] for r in runs.values()]
    summary = {
        "level": args.ci_level, "bootstrap_count": args.bootstrap_count, "bootstrap_seeds": args.bootstrap_seeds,
        "runs": runs,
        "pooled": {"quantiles": describe(pooled, args.ci_level), "failures": failure_bounds(total_fail, total_n)},
        "seed_comparison": {"median_mx_by_run": medians, "median_mx_range": float(max(medians) - min(medians)),
                            "median_mx_std_across_runs": float(np.std(medians, ddof=1)) if len(medians) > 1 else None,
                            "oat_top3_identical": len({tuple(r[:3]) for r in rankings}) == 1},
        "interpretation": ("Statistics describe the BTS-optics observables of the implemented error model "
                           "(see physics_model.md section 7); injection capture is not part of these ensembles."),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"medians": medians, "range": summary["seed_comparison"]["median_mx_range"],
                      "pooled_p50_ci": summary["pooled"]["quantiles"]["mismatch_x"]["p50_ci"],
                      "pooled_failures": summary["pooled"]["failures"]}, indent=1))


if __name__ == "__main__":
    main()
