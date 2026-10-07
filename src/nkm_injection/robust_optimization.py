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
from .statistics import StatisticalPolicy, summarize_robustness_results
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
    nominal_config, sample, target_twiss, capture_efficiency_fn, model, map_path, *extra = args
    options = extra[0] if extra else {}
    entrance = options.get("initial_twiss")
    beta_limit = options.get("beta_max_limit_m", 60.)
    mismatch_limit = options.get("mismatch_limit", .5)
    beta_tolerance = options.get("beta_tolerance_m", 0.)
    mismatch_tolerance = options.get("mismatch_tolerance", 0.)
    mismatch_definition = options.get("mismatch_definition", "per_plane")
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
        lattice, init_twiss = apply_sample_errors(nominal_config, sample,
            **({"initial_twiss": entrance} if entrance is not None else {}))
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
        if bx_max > beta_limit + beta_tolerance or by_max > beta_limit + beta_tolerance:
            reasons.append("beta_exceeded")
        mismatch_value = mx + my if mismatch_definition == "sum" else max(mx, my)
        if mismatch_value > mismatch_limit + mismatch_tolerance:
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
    nominal_config, target_twiss, err_key, label, base_samples, ref_merit, initial_twiss = args
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
            lattice, init_twiss = apply_sample_errors(nominal_config, iso_sample, initial_twiss=initial_twiss)
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
                                   kickmap_path: Optional[Union[str, Path]] = None,
                                   initial_twiss: Optional[Dict[str, Any]] = None,
                                   beta_max_limit_m: float = 60.,
                                   mismatch_limit: float = .5,
                                   mismatch_definition: str = "per_plane",
                                   beta_tolerance_m: float = 0.,
                                   mismatch_tolerance: float = 0.,
                                   statistical_policy: Optional[StatisticalPolicy] = None) -> Dict[str, Any]:
    """
    Evaluate Monte Carlo statistics (p50, p68, p95, p99, failure probability, bootstrap CI)
    across a set of error realization samples using sequential or parallel execution.

    Kicks are reported in mrad and beta in m. The default explicitly loads the
    repository field map; alternate kicker_model values require selection.
    Invalid evaluations have null metrics and are excluded from percentiles.
    failure_probability is physical failures / valid evaluations (None if none);
    feasible_fraction is physically feasible / all requested evaluations.
    Optional entrance optics use m and dimensionless Twiss values. Thresholds
    default to per-plane mismatch with zero tolerance; explicit sum mode and
    beta/mismatch tolerances support saved optimizer feasibility conventions.
    StatisticalPolicy saves bootstrap and ordered-prefix stability settings;
    insufficient or invalid data cannot establish stability. Empty ensembles
    return explicit null summaries and insufficient-evidence diagnostics.
    """
    policy = statistical_policy or StatisticalPolicy()
    policy.validate()

    model = validate_kicker_model(kicker_model)
    map_path = Path(kickmap_path or Path(__file__).resolve().parents[2] / "kickmap_file.txt").resolve()
    for key in ("beta", "alpha"):
        values = np.asarray(target_twiss[key], dtype=float)
        if values.shape != (2,) or not np.all(np.isfinite(values)):
            raise ValueError(f"Target {key} must contain two finite values")
    if np.any(np.asarray(target_twiss["beta"]) <= 0):
        raise ValueError("Target beta functions must be positive (m)")
    for label, limit in (("beta_max_limit_m", beta_max_limit_m), ("mismatch_limit", mismatch_limit)):
        if not np.isfinite(limit) or limit <= 0:
            raise ValueError(f"{label} must be finite and positive")
    if mismatch_definition not in ("per_plane", "sum"):
        raise ValueError("mismatch_definition must be 'per_plane' or 'sum'")
    for label, tolerance in (("beta_tolerance_m", beta_tolerance_m), ("mismatch_tolerance", mismatch_tolerance)):
        if not np.isfinite(tolerance) or tolerance < 0:
            raise ValueError(f"{label} must be finite and non-negative")
    options = {"mismatch_definition": mismatch_definition, "beta_tolerance_m": beta_tolerance_m,
               "mismatch_tolerance": mismatch_tolerance, "initial_twiss": initial_twiss, "beta_max_limit_m": beta_max_limit_m,
               "mismatch_limit": mismatch_limit}
    task_args = [(nominal_config, s, target_twiss, capture_efficiency_fn, model, map_path, options) for s in samples]
    results = parallel_map(_eval_single_robustness_sample, task_args, n_workers=n_workers, desc="evaluate_robustness_statistics")

    statistics = summarize_robustness_results(results, policy, capture_enabled=capture_efficiency_fn is not None)
    return {**statistics, "evaluation_schema_version": 1,
            "evaluation_thresholds": {key: value for key, value in options.items() if key != "initial_twiss"},
            "model_provenance": {"kicker_model": model, "map_path": str(map_path) if model == "fieldmap" else None}}


def compute_one_at_a_time_sensitivity(nominal_config: BTSConfig,
                                       target_twiss: Dict[str, Any],
                                       n_samples: int = 50,
                                       seed: int = 42,
                                       n_workers: Optional[int] = 1,
                                       error_config: Optional[ErrorBudgetConfig] = None,
                                       initial_twiss: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """
    Perform One-At-A-Time (OAT) sensitivity scans across individual error categories
    to rank dominant error contributors using sequential or parallel execution.
    Optional error_config sets the sampled budget; entrance beta/dispersion use
    m and alpha/dispersion derivatives are dimensionless. Reference and sampled
    optics share the same supplied entrance configuration.
    """
    error_config = error_config or ErrorBudgetConfig()
    base_samples = sample_error_ensemble(error_config, n_samples=n_samples, seed=seed)

    ref_lattice = create_bts_lattice(nominal_config)
    ref_twiss = initial_twiss if initial_twiss is not None else DEFAULT_BTS_ENTRANCE_TWISS.to_dict()
    ref_prop = compute_twiss_propagation(ref_lattice, ref_twiss)
    ref_mx = compute_mismatch_metric(ref_prop["final_beta"][0], ref_prop["final_alpha"][0], target_twiss["beta"][0], target_twiss["alpha"][0])
    ref_my = compute_mismatch_metric(ref_prop["final_beta"][1], ref_prop["final_alpha"][1], target_twiss["beta"][1], target_twiss["alpha"][1])
    ref_merit = ref_mx + ref_my

    error_types = [
        ("quad_k_err", f"Quad Gradient Error ({error_config.quad_k_rel_std*100:g}%)"),
        ("quad_dx_m", f"Quad Alignment Offset ({error_config.quad_dx_std_m*1e6:g} um)"),
        ("quad_roll_rad", f"Quad Roll Error ({error_config.quad_roll_std_rad*1e3:g} mrad)"),
        ("booster_x_m", f"Booster Centroid Jitter X ({error_config.booster_x_jitter_std_m*1e3:g} mm)"),
        ("booster_xp_rad", f"Booster Centroid Jitter Xp ({error_config.booster_xp_jitter_std_rad*1e3:g} mrad)"),
        ("energy_dp_p", f"Energy Error ({error_config.energy_dp_p_std*100:g}%)"),
        ("beta_mismatch", f"Twiss Beta Mismatch ({error_config.beta_mismatch_rel_std*100:g}%)"),
        ("nkm_scale_err", f"NKM Field Scale Jitter ({error_config.nkm_scale_std*100:g}%)"),
        ("nkm_dx_m", f"NKM Horizontal Alignment ({error_config.nkm_dx_std_m*1e6:g} um)"),
        ("ring_co_x_m", f"Ring Closed-Orbit Error ({error_config.ring_co_x_std_m*1e6:g} um)"),
        ("septum_x_m", f"Septum Position Error ({error_config.septum_x_std_m*1e6:g} um)"),
    ]

    task_args = [
        (nominal_config, target_twiss, err_key, label, base_samples, ref_merit, initial_twiss)
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
