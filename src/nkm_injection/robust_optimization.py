"""
NKM Robust Optimization and Statistical Robustness Evaluation Module

Provides Monte Carlo statistical evaluations (p50, p68, p95, p99 percentiles, failure probability,
bootstrap confidence intervals), one-at-a-time tolerance sensitivity rankings, and robust
design optimization algorithms.
"""

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np
from scipy.optimize import minimize

from .evaluation import (EvaluationOutcome, EvaluationExecutionError,
    EXPECTED_NUMERICAL_ERRORS, exception_context, require_finite, validate_optics_result)
from .fieldmap import OutOfDomainError
from .kickmap import NKMKickMap2D
from .units import validate_kicker_model

from .bts_lattice import BTSConfig, create_bts_lattice
from .optics import compute_twiss_propagation, compute_mismatch_metric, DEFAULT_BTS_ENTRANCE_TWISS
from .errors import ErrorBudgetConfig, sample_error_ensemble, apply_sample_errors
from .concurrency import parallel_map, resolve_workers
from .optimization import BaseOpticsObjective, BTSOptimizationConfig, BTSNormalizedObjectives, BTSHardwareConstraints


class RobustMonteCarloObjective(BaseOpticsObjective):
    """
    Robust Monte Carlo Objective Strategy for Optics Optimization.
    
    Evaluates optics mismatch across an error ensemble sample, returning mean / median
    mismatch residuals for robust optics design.
    """
    def __init__(self,
                 config: Optional[BTSOptimizationConfig] = None,
                 n_samples: int = 20,
                 seed: int = 42,
                 n_workers: Optional[int] = 1,
                 kicker_model: str = "fieldmap",
                 kickmap_path: Optional[Union[str, Path]] = None):
        self.config = config or BTSOptimizationConfig()
        self.objectives = BTSNormalizedObjectives(self.config.target_config)
        self.constraints = BTSHardwareConstraints(self.config.constraint_config)
        self.nominal_strengths = self.objectives.nominal_strengths
        self.quad_names = self.objectives.quad_names
        self.n_samples = n_samples
        self.seed = seed
        self.n_workers = n_workers
        self.kicker_model = validate_kicker_model(kicker_model)
        self.kickmap_path = kickmap_path
        self.samples = sample_error_ensemble(n_samples=n_samples, seed=seed)

    def compute_residual_vector(self, strengths: np.ndarray) -> np.ndarray:
        eval_dict = self.evaluate(strengths)
        return np.array([
            eval_dict["mismatch_x"],
            eval_dict["mismatch_y"],
            eval_dict["disp_x_residual"],
            eval_dict["disp_px_residual"]
        ])

    def evaluate(self, strengths: np.ndarray) -> Dict[str, Any]:
        target_twiss = {
            "beta": [self.config.target_config.target_beta_x, self.config.target_config.target_beta_y],
            "alpha": [self.config.target_config.target_alpha_x, self.config.target_config.target_alpha_y]
        }
        bts_config = BTSConfig(
            k_q11=float(strengths[0]), k_q12=float(strengths[1]), k_q13=float(strengths[2]),
            k_q21=float(strengths[3]), k_q22=float(strengths[4]), k_q23=float(strengths[5]),
            k_q31=float(strengths[6]), k_q32=float(strengths[7]), k_q33=float(strengths[8])
        )
        stats = evaluate_robustness_statistics(bts_config, target_twiss, self.samples, n_workers=self.n_workers,
            kicker_model=self.kicker_model, kickmap_path=self.kickmap_path)
        
        if stats["n_invalid_evaluations"]:
            return {"feasible": False, "violations": ["Invalid Monte Carlo evaluations"],
                    "merit": 1e9, "mismatch_x": 1e4, "mismatch_y": 1e4,
                    "disp_x_residual": 0., "disp_px_residual": 0.,
                    "max_beta_x": 1e6, "max_beta_y": 1e6, "robust_stats": stats,
                    "outcome": EvaluationOutcome("invalid", {"strengths_m_minus2": strengths.tolist()},
                        stats["model_provenance"]).to_dict()}
        mx_p50 = stats["mismatch_x"]["p50"]
        my_p50 = stats["mismatch_y"]["p50"]
        merit = float(mx_p50 + my_p50)
        
        return {
            "feasible": bool(stats["feasible_fraction"] > 0.8),
            "violations": [] if stats["feasible_fraction"] > 0.8 else ["High failure rate in Monte Carlo ensemble"],
            "merit": merit,
            "mismatch_x": mx_p50,
            "mismatch_y": my_p50,
            "disp_x_residual": 0.0,
            "disp_px_residual": 0.0,
            "max_beta_x": stats["max_beta_x_m"]["p50"],
            "max_beta_y": stats["max_beta_y_m"]["p50"],
            "robust_stats": stats,
            "outcome": EvaluationOutcome("valid" if stats["feasible_fraction"] > .8 else "infeasible",
                {"strengths_m_minus2": strengths.tolist()}, stats["model_provenance"],
                [] if stats["feasible_fraction"] > .8 else ["ensemble_failure_rate"]).to_dict()
        }


def _eval_single_robustness_sample(args) -> Dict[str, Any]:
    """Pickleable worker: kicks in rad, beta in m; no substitute physics models."""
    nominal_config, sample, target_twiss, capture_efficiency_fn, model, map_path = args
    identity = {"sample_id": sample["sample_id"],
                "nominal_strengths_m_minus2": list(nominal_config.quad_strengths_list)}
    provenance = {"kicker_model": model, "beam_energy_eV": nominal_config.energy_eV,
                  "map_path": str(map_path) if model == "fieldmap" else None}
    phase = "model_setup"
    try:
        from .storage_ring_injection import get_kicker_evaluator, StorageRingInjectionConfig
        kickmap = NKMKickMap2D(map_path) if model == "fieldmap" else None
        if kickmap is not None:
            provenance["map_sha256"] = kickmap.compute_file_hash()
        evaluator, metadata = get_kicker_evaluator(
            model, config=StorageRingInjectionConfig(energy_eV=nominal_config.energy_eV),
            kickmap_obj=kickmap)
        provenance["metadata"] = asdict(metadata)
        phase = "optics"
        lattice, init_twiss = apply_sample_errors(nominal_config, sample)
        prop = compute_twiss_propagation(lattice, init_twiss)
        validate_optics_result(prop)
        beta_end, alpha_end = prop["final_beta"], prop["final_alpha"]
        mx = compute_mismatch_metric(beta_end[0], alpha_end[0], target_twiss["beta"][0], target_twiss["alpha"][0])
        my = compute_mismatch_metric(beta_end[1], alpha_end[1], target_twiss["beta"][1], target_twiss["alpha"][1])
        bx_max, by_max = prop["max_beta_x"], prop["max_beta_y"]
        phase = "stored_beam_kick"
        net_x = float(sample.get("ring_co_x_m", 0.0)) - float(sample.get("nkm_dx_m", 0.0))
        kx, _ = evaluator.evaluate_kicks(np.array([net_x]), np.array([0.0]))
        stored_kick_mrad = abs(float(kx[0]) * (1 + float(sample.get("nkm_scale_err", 0.0)))) * 1e3
        phase = "capture"
        eff = None
        if capture_efficiency_fn is not None:
            eff = float(capture_efficiency_fn(init_twiss.get("nkm_errors", {}), init_twiss.get("ring_errors", {}), init_twiss.get("centroid_offset", [0]*6)))
            require_finite(eff, "Capture efficiency")
            if not 0 <= eff <= 1:
                raise ValueError("Capture callback must return an efficiency between zero and one")
        require_finite([mx, my, bx_max, by_max, stored_kick_mrad], "Robustness metrics")
        reasons = []
        if bx_max > 60 or by_max > 60:
            reasons.append("beta_exceeded")
        if mx > .5 or my > .5:
            reasons.append("mismatch_exceeded")
        if eff is not None and eff < .8:
            reasons.append("capture_failed")
        outcome = EvaluationOutcome("infeasible" if reasons else "valid", identity, provenance, reasons)
        return {"mx": mx, "my": my, "bx_max": bx_max, "by_max": by_max,
                "stored_kick_mrad": stored_kick_mrad, "eff": eff,
                "failed": bool(reasons), "failure_mode": reasons[0] if reasons else None,
                "outcome": outcome.to_dict()}
    except (OutOfDomainError, *EXPECTED_NUMERICAL_ERRORS) as error:
        outcome = EvaluationOutcome("invalid", identity, provenance,
                                    exception=exception_context(error, phase))
        return {"mx": None, "my": None, "bx_max": None, "by_max": None,
                "stored_kick_mrad": None, "eff": None, "failed": False,
                "failure_mode": None, "outcome": outcome.to_dict()}
    except Exception as error:
        raise EvaluationExecutionError(
            f"Sample {identity['sample_id']!r}, model {model!r}, phase {phase}: "
            f"{type(error).__name__}: {error}") from error


def _eval_oat_single_category(args: Tuple[BTSConfig, Dict[str, Any], str, str, List[Dict[str, Any]], float]) -> Tuple[str, float]:
    """Top-level pickleable worker function for single OAT error sensitivity evaluation."""
    nominal_config, target_twiss, err_key, label, base_samples, ref_merit = args
    delta_merits = []
    for s in base_samples:
        iso_sample = {
            "sample_id": s["sample_id"],
            "quad_k_err": s["quad_k_err"] if err_key == "quad_k_err" else [0.0]*9,
            "quad_dx_m": s["quad_dx_m"] if err_key == "quad_dx_m" else [0.0]*9,
            "quad_dy_m": [0.0]*9,
            "quad_roll_rad": s["quad_roll_rad"] if err_key == "quad_roll_rad" else [0.0]*9,
            "quad_ds_m": [0.0]*9,
            "booster_x_m": s["booster_x_m"] if err_key == "booster_x_m" else 0.0,
            "booster_xp_rad": s["booster_xp_rad"] if err_key == "booster_xp_rad" else 0.0,
            "energy_dp_p": s["energy_dp_p"] if err_key == "energy_dp_p" else 0.0,
            "beta_mismatch_x": s["beta_mismatch_x"] if err_key == "beta_mismatch" else 0.0,
            "beta_mismatch_y": s["beta_mismatch_y"] if err_key == "beta_mismatch" else 0.0,
            "nkm_scale_err": s["nkm_scale_err"] if err_key == "nkm_scale_err" else 0.0,
            "nkm_dx_m": s["nkm_dx_m"] if err_key == "nkm_dx_m" else 0.0,
            "nkm_timing_mrad": s.get("nkm_timing_mrad", 0.0) if err_key == "nkm_timing_mrad" else 0.0,
            "ring_co_x_m": s["ring_co_x_m"] if err_key == "ring_co_x_m" else 0.0,
            "septum_x_m": s["septum_x_m"] if err_key == "septum_x_m" else 0.0,
        }
        try:
            lattice, init_twiss = apply_sample_errors(nominal_config, iso_sample)
            prop = compute_twiss_propagation(lattice, init_twiss)
            validate_optics_result(prop)
            mx = compute_mismatch_metric(prop["final_beta"][0], prop["final_alpha"][0], target_twiss["beta"][0], target_twiss["alpha"][0])
            my = compute_mismatch_metric(prop["final_beta"][1], prop["final_alpha"][1], target_twiss["beta"][1], target_twiss["alpha"][1])
            delta = abs((mx + my) - ref_merit)
            require_finite(delta, "OAT merit difference")
            delta_merits.append(delta)
        except Exception as error:
            raise EvaluationExecutionError(
                f"OAT sample {s['sample_id']!r}, category {err_key!r}, optics: "
                f"{type(error).__name__}: {error}") from error

    return label, float(np.mean(delta_merits))


def evaluate_robustness_statistics(nominal_config: BTSConfig,
                                   target_twiss: Dict[str, Any],
                                   samples: List[Dict[str, Any]],
                                   capture_efficiency_fn: Optional[Any] = None,
                                   n_workers: Optional[int] = 1,
                                   kicker_model: str = "fieldmap",
                                   kickmap_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Evaluate Monte Carlo statistics (p50, p68, p95, p99, failure probability, bootstrap CI)
    across a set of error realization samples using sequential or parallel execution.

    Kicks are reported in mrad and beta in m. The default explicitly loads the
    repository field map; alternate kicker_model values require selection.
    Invalid evaluations have null metrics and are excluded from percentiles.
    failure_probability is physical failures / valid evaluations (None if none);
    feasible_fraction is physically feasible / all requested evaluations.
    """
    n_samples = len(samples)
    if n_samples == 0:
        return {}

    model = validate_kicker_model(kicker_model)
    map_path = Path(kickmap_path or Path(__file__).resolve().parents[2] / "kickmap_file.txt").resolve()
    for key in ("beta", "alpha"):
        values = np.asarray(target_twiss[key], dtype=float)
        if values.shape != (2,) or not np.all(np.isfinite(values)):
            raise ValueError(f"Target {key} must contain two finite values")
    if np.any(np.asarray(target_twiss["beta"]) <= 0):
        raise ValueError("Target beta functions must be positive (m)")
    task_args = [(nominal_config, s, target_twiss, capture_efficiency_fn, model, map_path) for s in samples]
    results = parallel_map(_eval_single_robustness_sample, task_args, n_workers=n_workers, desc="evaluate_robustness_statistics")

    mx_list = []
    my_list = []
    bx_max_list = []
    by_max_list = []
    failures = 0
    failure_modes = {"beta_exceeded": 0, "mismatch_exceeded": 0, "capture_failed": 0}
    stored_kick_list = []
    eff_list = []

    valid_results = [res for res in results if res["outcome"]["status"] != "invalid"]
    n_valid = len(valid_results)
    for res in valid_results:
        mx_list.append(res["mx"])
        my_list.append(res["my"])
        bx_max_list.append(res["bx_max"])
        by_max_list.append(res["by_max"])
        stored_kick_list.append(res["stored_kick_mrad"])
        eff_list.append(res["eff"])
        if res["failed"]:
            failures += 1
            for reason in res["outcome"]["physical_failure_reasons"]:
                failure_modes[reason] += 1

    mx_arr = np.array(mx_list)
    my_arr = np.array(my_list)
    bx_arr = np.array(bx_max_list)
    by_arr = np.array(by_max_list)

    # Bootstrap 95% confidence interval for median mismatch Mx
    rng = np.random.default_rng(42)
    boot_medians = []
    for _ in range(1000 if n_valid else 0):
        boot_sample = rng.choice(mx_arr, size=n_valid, replace=True)
        boot_medians.append(np.median(boot_sample))
    ci_lower = float(np.percentile(boot_medians, 2.5)) if n_valid else None
    ci_upper = float(np.percentile(boot_medians, 97.5)) if n_valid else None

    # Convergence check
    convergence_check = {}
    if n_valid == n_samples and n_samples >= 10:
        mx_50_val = np.median(mx_arr[:min(50, n_samples)])
        mx_100_val = np.median(mx_arr[:min(100, n_samples)])
        diff = abs(mx_100_val - mx_50_val)
        convergence_check = {
            "converged": bool(diff < 0.05),
            "N_50_to_100_diff": float(diff)
        }

    return {
        "n_samples": n_samples,
        "evaluation_schema_version": 1,
        "n_valid_evaluations": n_valid,
        "n_invalid_evaluations": n_samples - n_valid,
        "invalid_evaluation_fraction": (n_samples - n_valid) / n_samples,
        "sample_results": results,
        "model_provenance": {"kicker_model": model, "map_path": str(map_path) if model == "fieldmap" else None},
        "feasible_fraction": (n_valid - failures) / n_samples,
        "failure_probability": failures / n_valid if n_valid else None,
        "failure_modes": failure_modes,
        "convergence_check": convergence_check,
        "mismatch_x": {
            "p50": (float(np.median(mx_arr)) if n_valid else None),
            "p50_median": (float(np.median(mx_arr)) if n_valid else None),
            "p68": (float(np.percentile(mx_arr, 68)) if n_valid else None),
            "p95": (float(np.percentile(mx_arr, 95)) if n_valid else None),
            "p99": (float(np.percentile(mx_arr, 99)) if n_valid else None),
            "mean": (float(np.mean(mx_arr)) if n_valid else None),
            "std": (float(np.std(mx_arr)) if n_valid else None),
            "bootstrap_95ci_median": [ci_lower, ci_upper]
        },
        "mismatch_y": {
            "p50": (float(np.median(my_arr)) if n_valid else None),
            "p50_median": (float(np.median(my_arr)) if n_valid else None),
            "p68": (float(np.percentile(my_arr, 68)) if n_valid else None),
            "p95": (float(np.percentile(my_arr, 95)) if n_valid else None),
            "p99": (float(np.percentile(my_arr, 99)) if n_valid else None),
            "mean": (float(np.mean(my_arr)) if n_valid else None),
            "std": (float(np.std(my_arr)) if n_valid else None),
        },
        "max_beta_x_m": {
            "p50": (float(np.median(bx_arr)) if n_valid else None),
            "p50_median": (float(np.median(bx_arr)) if n_valid else None),
            "p95": (float(np.percentile(bx_arr, 95)) if n_valid else None),
            "p99": (float(np.percentile(bx_arr, 99)) if n_valid else None),
        },
        "max_beta_y_m": {
            "p50": (float(np.median(by_arr)) if n_valid else None),
            "p50_median": (float(np.median(by_arr)) if n_valid else None),
            "p95": (float(np.percentile(by_arr, 95)) if n_valid else None),
            "p99": (float(np.percentile(by_arr, 99)) if n_valid else None),
        },
        "stored_beam_kick_mrad": {
            "p50": (float(np.median(stored_kick_list)) if n_valid else None),
            "p95": (float(np.percentile(stored_kick_list, 95)) if n_valid else None),
            "p99": (float(np.percentile(stored_kick_list, 99)) if n_valid else None),
            "max": (float(np.max(stored_kick_list)) if n_valid else None)
        },
        "capture_efficiency": {
            "p50": (float(np.median(eff_list)) if n_valid else None),
            "mean": (float(np.mean(eff_list)) if n_valid else None)
        } if capture_efficiency_fn is not None else {}
    }


def compute_one_at_a_time_sensitivity(nominal_config: BTSConfig,
                                       target_twiss: Dict[str, Any],
                                       n_samples: int = 50,
                                       seed: int = 42,
                                       n_workers: Optional[int] = 1) -> Dict[str, float]:
    """
    Perform One-At-A-Time (OAT) sensitivity scans across individual error categories
    to rank dominant error contributors using sequential or parallel execution.
    """
    base_samples = sample_error_ensemble(n_samples=n_samples, seed=seed)

    ref_lattice = create_bts_lattice(nominal_config)
    ref_twiss = DEFAULT_BTS_ENTRANCE_TWISS.to_dict()
    ref_prop = compute_twiss_propagation(ref_lattice, ref_twiss)
    ref_mx = compute_mismatch_metric(ref_prop["final_beta"][0], ref_prop["final_alpha"][0], target_twiss["beta"][0], target_twiss["alpha"][0])
    ref_my = compute_mismatch_metric(ref_prop["final_beta"][1], ref_prop["final_alpha"][1], target_twiss["beta"][1], target_twiss["alpha"][1])
    ref_merit = ref_mx + ref_my

    error_types = [
        ("quad_k_err", "Quad Gradient Error (0.1%)"),
        ("quad_dx_m", "Quad Alignment Offset (100 um)"),
        ("quad_roll_rad", "Quad Roll Error (0.5 mrad)"),
        ("booster_x_m", "Booster Centroid Jitter X (0.5 mm)"),
        ("booster_xp_rad", "Booster Centroid Jitter Xp (0.2 mrad)"),
        ("energy_dp_p", "Energy Error (0.1%)"),
        ("beta_mismatch", "Twiss Beta Mismatch (5%)"),
        ("nkm_scale_err", "NKM Field Scale Jitter (0.5%)"),
        ("nkm_dx_m", "NKM Horizontal Alignment (200 um)"),
        ("ring_co_x_m", "Ring Closed-Orbit Error (200 um)"),
        ("septum_x_m", "Septum Position Error (100 um)"),
    ]

    task_args = [
        (nominal_config, target_twiss, err_key, label, base_samples, ref_merit)
        for err_key, label in error_types
    ]
    results = parallel_map(_eval_oat_single_category, task_args, n_workers=n_workers, desc="compute_one_at_a_time_sensitivity")
    rankings = dict(results)

    return dict(sorted(rankings.items(), key=lambda item: item[1], reverse=True))

def nominal_vs_robust_comparison(nominal_config: BTSConfig,
                                 robust_config: BTSConfig,
                                 target_twiss: Dict[str, Any],
                                 samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    nom_stats = evaluate_robustness_statistics(nominal_config, target_twiss, samples)
    rob_stats = evaluate_robustness_statistics(robust_config, target_twiss, samples)
    
    return {
        "nominal_stats": nom_stats,
        "robust_stats": rob_stats,
        "improvement_mismatch_x_p95": float(nom_stats["mismatch_x"]["p95"] - rob_stats["mismatch_x"]["p95"]),
        "improvement_mismatch_y_p95": float(nom_stats["mismatch_y"]["p95"] - rob_stats["mismatch_y"]["p95"])
    }
