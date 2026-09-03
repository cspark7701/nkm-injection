"""
NKM Multi-Turn Injection Convergence Study Module

Provides:
- Strongly typed return dataclasses (ConvergenceScanResult, AcceptanceResult, EnsembleStudyResult)
- Separated smoke / pilot / production simulation configurations
- Convergence scanning over particle count, turn count, NKM slice count, and random seed
- Bootstrap confidence interval estimation for capture efficiency
- Stored-beam perturbation quantification (centroid oscillation, emittance growth)
- Loss-map and first-loss-turn distribution reporting
- Injection acceptance and septum clearance metrics
- Tabular pandas DataFrame export support
"""

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Sequence, Union
import json
import numpy as np

from .storage_ring_injection import (
    StorageRingInjectionConfig,
    load_storage_ring_injection_lattice,
    track_multiturn_injection,
    TrackingResult,
)
from .beam import generate_6d_beam
from .kickmap import NKMKickMap2D
from .results_schema import SerializableConfigMixin
from .concurrency import parallel_map, resolve_workers


# ---------------------------------------------------------------------------
# Structured Return Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ConvergenceScanResult(SerializableConfigMixin):
    """
    Structured, strongly typed result of a multi-turn injection convergence scan.
    
    Attributes
    ----------
    scan_parameter : str
        Parameter varied during scan ('particle_count' or 'turn_count').
    scan_values : np.ndarray
        Array of tested scan parameter values (e.g. N_particles or N_turns).
    efficiencies : np.ndarray
        Array of capture efficiencies (survival fractions in [0, 1]).
    survived_counts : np.ndarray
        Array of surviving particle counts.
    cpu_times_s : np.ndarray
        Array of execution times in seconds per scan point.
    final_emittance_x : Optional[np.ndarray] = None
        Horizontal emittance (m*rad or mm*mrad) at scan end.
    final_emittance_y : Optional[np.ndarray] = None
        Vertical emittance (m*rad or mm*mrad) at scan end.
    records : List[Dict[str, Any]] = field(default_factory=list)
        Row dictionaries representing per-point results.
    metadata : Dict[str, Any] = field(default_factory=dict)
        Additional contextual metadata (e.g. kicker_model, turns, particles, seed).
    """
    scan_parameter: str
    scan_values: np.ndarray
    efficiencies: np.ndarray
    survived_counts: np.ndarray
    cpu_times_s: np.ndarray
    final_emittance_x: Optional[np.ndarray] = None
    final_emittance_y: Optional[np.ndarray] = None
    records: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.scan_values, np.ndarray):
            self.scan_values = np.asarray(self.scan_values)
        if not isinstance(self.efficiencies, np.ndarray):
            self.efficiencies = np.asarray(self.efficiencies, dtype=float)
        if not isinstance(self.survived_counts, np.ndarray):
            self.survived_counts = np.asarray(self.survived_counts, dtype=int)
        if not isinstance(self.cpu_times_s, np.ndarray):
            self.cpu_times_s = np.asarray(self.cpu_times_s, dtype=float)
        if self.final_emittance_x is not None and not isinstance(self.final_emittance_x, np.ndarray):
            self.final_emittance_x = np.asarray(self.final_emittance_x, dtype=float)
        if self.final_emittance_y is not None and not isinstance(self.final_emittance_y, np.ndarray):
            self.final_emittance_y = np.asarray(self.final_emittance_y, dtype=float)
        if not self.records:
            param_key = "n_particles" if self.scan_parameter == "particle_count" else "n_turns"
            recs = []
            for i, val in enumerate(self.scan_values):
                rec = {
                    param_key: int(val),
                    "survived": int(self.survived_counts[i]) if i < len(self.survived_counts) else 0,
                    "capture_efficiency": float(self.efficiencies[i]) if i < len(self.efficiencies) else 0.0,
                    "cpu_time_s": float(self.cpu_times_s[i]) if i < len(self.cpu_times_s) else 0.0,
                }
                if self.final_emittance_x is not None and i < len(self.final_emittance_x):
                    rec["emittance_x_mrad"] = float(self.final_emittance_x[i])
                if self.final_emittance_y is not None and i < len(self.final_emittance_y):
                    rec["emittance_y_mrad"] = float(self.final_emittance_y[i])
                recs.append(rec)
            self.records = recs

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, key: Union[int, slice, str]) -> Any:
        if isinstance(key, (int, slice)):
            return self.records[key]
        if isinstance(key, str):
            if key in ("records", "scan_values", "efficiencies", "survived_counts", "cpu_times_s", "final_emittance_x", "final_emittance_y", "metadata", "scan_parameter"):
                return getattr(self, key)
            if key in ("particle_counts", "n_particles") and self.scan_parameter == "particle_count":
                return self.scan_values
            if key in ("turns", "n_turns") and self.scan_parameter == "turn_count":
                return self.scan_values
            if key in ("survivals", "capture_efficiencies"):
                return self.efficiencies
            if key in self.metadata:
                return self.metadata[key]
            raise KeyError(f"Key '{key}' not found in ConvergenceScanResult")
        raise TypeError(f"Invalid index type {type(key)}")

    def mean_efficiency(self) -> float:
        """Return mean capture efficiency across scan points."""
        return float(np.mean(self.efficiencies)) if len(self.efficiencies) > 0 else float("nan")

    def std_efficiency(self) -> float:
        """Return standard deviation of capture efficiency across scan points."""
        return float(np.std(self.efficiencies)) if len(self.efficiencies) > 0 else float("nan")

    def to_dataframe(self):
        """Convert scan results to a pandas DataFrame."""
        import pandas as pd
        param_col = "n_particles" if self.scan_parameter == "particle_count" else "n_turns"
        data = {
            param_col: self.scan_values,
            "survived": self.survived_counts,
            "capture_efficiency": self.efficiencies,
            "cpu_time_s": self.cpu_times_s,
        }
        if self.final_emittance_x is not None:
            data["emittance_x_mrad"] = self.final_emittance_x
        if self.final_emittance_y is not None:
            data["emittance_y_mrad"] = self.final_emittance_y
        return pd.DataFrame(data)


@dataclass
class AcceptanceResult(SerializableConfigMixin):
    """
    Structured, strongly typed result of an injection acceptance scan.
    
    Attributes
    ----------
    x_grid_m : np.ndarray
        Tested horizontal offsets in meters.
    survival_fraction_grid : np.ndarray
        Array of capture efficiencies corresponding to x_grid_m.
    x_offsets_mm : np.ndarray
        Horizontal offsets in millimeters.
    acceptance_area_m_rad : float
        Calculated physical acceptance integral (in mm or m).
    xp_grid_rad : Optional[np.ndarray] = None
        Tested horizontal angles in radians (if 2D acceptance grid), or None.
    records : List[Dict[str, Any]] = field(default_factory=list)
        Row dictionaries representing per-point results.
    metadata : Dict[str, Any] = field(default_factory=dict)
        Additional contextual metadata (e.g. kicker_model, particles, turns, seed).
    """
    x_grid_m: np.ndarray
    survival_fraction_grid: np.ndarray
    x_offsets_mm: np.ndarray
    acceptance_area_m_rad: float = 0.0
    xp_grid_rad: Optional[np.ndarray] = None
    records: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.x_grid_m, np.ndarray):
            self.x_grid_m = np.asarray(self.x_grid_m, dtype=float)
        if not isinstance(self.survival_fraction_grid, np.ndarray):
            self.survival_fraction_grid = np.asarray(self.survival_fraction_grid, dtype=float)
        if not isinstance(self.x_offsets_mm, np.ndarray):
            self.x_offsets_mm = np.asarray(self.x_offsets_mm, dtype=float)
        if self.xp_grid_rad is not None and not isinstance(self.xp_grid_rad, np.ndarray):
            self.xp_grid_rad = np.asarray(self.xp_grid_rad, dtype=float)
        if not self.records:
            recs = []
            for i, x_m in enumerate(self.x_grid_m):
                recs.append({
                    "x_offset_m": float(x_m),
                    "x_offset_mm": float(self.x_offsets_mm[i]) if i < len(self.x_offsets_mm) else float(x_m * 1e3),
                    "capture_efficiency": float(self.survival_fraction_grid[i]) if i < len(self.survival_fraction_grid) else 0.0,
                })
            self.records = recs

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, key: Union[int, slice, str]) -> Any:
        if isinstance(key, (int, slice)):
            return self.records[key]
        if isinstance(key, str):
            if key in ("records", "x_grid_m", "xp_grid_rad", "survival_fraction_grid", "x_offsets_mm", "acceptance_area_m_rad", "metadata"):
                return getattr(self, key)
            if key in ("x_offsets_m", "x_offsets"):
                return self.x_grid_m.tolist()
            if key in ("efficiencies", "capture_efficiencies"):
                return self.survival_fraction_grid.tolist()
            if key in self.metadata:
                return self.metadata[key]
            raise KeyError(f"Key '{key}' not found in AcceptanceResult")
        raise TypeError(f"Invalid index type {type(key)}")

    def acceptance_window_mm(self, threshold: float = 0.9) -> Tuple[float, float]:
        """Return [x_min_mm, x_max_mm] range where capture efficiency >= threshold."""
        mask = self.survival_fraction_grid >= threshold
        if not np.any(mask):
            return float("nan"), float("nan")
        valid_x = self.x_offsets_mm[mask]
        return float(np.min(valid_x)), float(np.max(valid_x))

    def to_dataframe(self):
        """Convert acceptance scan results to a pandas DataFrame."""
        import pandas as pd
        data = {
            "x_offset_m": self.x_grid_m,
            "x_offset_mm": self.x_offsets_mm,
            "capture_efficiency": self.survival_fraction_grid,
        }
        if self.xp_grid_rad is not None:
            data["xp_offset_rad"] = self.xp_grid_rad
        return pd.DataFrame(data)


@dataclass
class EnsembleStudyResult(SerializableConfigMixin):
    """
    Structured, strongly typed result of a multi-seed ensemble injection study.
    
    Attributes
    ----------
    label : str
        Human-readable simulation tier label ('smoke', 'pilot', 'production').
    kicker_model : str
        Kicker model formulation used ('off', 'ideal', 'linear', 'fieldmap').
    tier : Dict[str, Any]
        Tier configuration parameters (n_particles, n_turns, n_slices, seeds).
    capture_efficiency_ci : Dict[str, float]
        Bootstrap confidence interval dict (mean, std, ci_lo, ci_hi).
    per_seed_results : List[Dict[str, Any]]
        List of per-seed metric dictionaries.
    mean_stored_perturbation : Dict[str, float]
        Mean stored-beam perturbation dictionary across all seeds.
    first_loss_distribution : Optional[Dict[str, Any]] = None
        Turn-resolved first loss distribution dictionary from seed 0.
    metadata : Dict[str, Any] = field(default_factory=dict)
        Additional simulation metadata.
    """
    label: str
    kicker_model: str
    tier: Dict[str, Any]
    capture_efficiency_ci: Dict[str, float]
    per_seed_results: List[Dict[str, Any]]
    mean_stored_perturbation: Dict[str, float]
    first_loss_distribution: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        if key in self.metadata:
            return self.metadata[key]
        raise KeyError(f"Key '{key}' not found in EnsembleStudyResult")

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key) or key in self.metadata

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return [
            "label", "kicker_model", "tier", "capture_efficiency_ci",
            "per_seed_results", "mean_stored_perturbation",
            "first_loss_distribution", "metadata"
        ]

    def values(self):
        return [self[k] for k in self.keys()]

    def items(self):
        return [(k, self[k]) for k in self.keys()]

    def to_dataframe(self):
        """Convert per-seed ensemble metrics to a pandas DataFrame."""
        import pandas as pd
        if not self.per_seed_results:
            return pd.DataFrame()
        return pd.DataFrame(self.per_seed_results)


# ---------------------------------------------------------------------------
# Simulation-Tier Configuration Presets
# ---------------------------------------------------------------------------

@dataclass
class InjectionStudyTierConfig:
    """
    Defines one simulation tier (smoke / pilot / production).

    Fields
    ------
    n_particles : int
        Number of macro-particles per run.
    n_turns : int
        Number of storage-ring turns to track.
    n_slices : int
        NKM thick-kick symplectic slice count.
    seeds : list[int]
        Random seeds used for ensemble bootstrap.
    label : str
        Human-readable label for the tier.
    """
    n_particles: int
    n_turns: int
    n_slices: int
    seeds: List[int]
    label: str


def smoke_config() -> InjectionStudyTierConfig:
    """Smoke-test tier: fast CI validation, not suitable for physics claims."""
    return InjectionStudyTierConfig(
        n_particles=100,
        n_turns=10,
        n_slices=10,
        seeds=[42],
        label="smoke"
    )


def pilot_config() -> InjectionStudyTierConfig:
    """Pilot tier: intermediate study to establish convergence trends."""
    return InjectionStudyTierConfig(
        n_particles=1000,
        n_turns=100,
        n_slices=40,
        seeds=[42, 123, 777],
        label="pilot"
    )


def production_config() -> InjectionStudyTierConfig:
    """
    Production tier: numerically defensible results for publication.

    Particle count and turn count are chosen based on convergence evidence
    from the pilot study. Default values are conservative minima; increase
    if convergence scans show residuals above 0.1 percentage points.
    """
    return InjectionStudyTierConfig(
        n_particles=10000,
        n_turns=1000,
        n_slices=40,
        seeds=[42, 123, 777, 999, 2025],
        label="production"
    )


# ---------------------------------------------------------------------------
# Bootstrap Confidence Interval
# ---------------------------------------------------------------------------

def bootstrap_capture_ci(
    survived_per_seed: List[int],
    n_particles: int,
    n_bootstrap: int = 5000,
    ci_level: float = 0.95,
    rng: Optional[np.random.Generator] = None
) -> Dict[str, float]:
    """
    Estimate a bootstrap confidence interval for mean capture efficiency.

    Parameters
    ----------
    survived_per_seed : list[int]
        Number of surviving particles per seed run.
    n_particles : int
        Total injected particles per run (denominator for efficiency).
    n_bootstrap : int
        Number of bootstrap resamples.
    ci_level : float
        Confidence level (e.g. 0.95 for 95 % CI).
    rng : numpy.random.Generator, optional
        Random number generator for reproducibility.

    Returns
    -------
    dict with keys: mean, std, ci_lo, ci_hi, ci_level, n_seeds, n_bootstrap
    """
    if rng is None:
        rng = np.random.default_rng(0)
    efficiencies = np.asarray(survived_per_seed, dtype=float) / n_particles
    n_seeds = len(efficiencies)
    boot_means = np.array([
        np.mean(rng.choice(efficiencies, size=n_seeds, replace=True))
        for _ in range(n_bootstrap)
    ])
    alpha = (1.0 - ci_level) / 2.0
    ci_lo = float(np.percentile(boot_means, 100 * alpha))
    ci_hi = float(np.percentile(boot_means, 100 * (1 - alpha)))
    return {
        "mean": float(np.mean(efficiencies)),
        "std": float(np.std(efficiencies, ddof=1)) if n_seeds > 1 else 0.0,
        "ci_lo": ci_lo,
        "ci_hi": ci_hi,
        "ci_level": ci_level,
        "n_seeds": n_seeds,
        "n_bootstrap": n_bootstrap
    }


# ---------------------------------------------------------------------------
# Convergence Scanning
# ---------------------------------------------------------------------------

def particle_count_convergence_scan(
    n_particle_values: List[int],
    n_turns: int,
    ring,
    kicker_model: str,
    kickmap_obj: Optional[NKMKickMap2D],
    config: StorageRingInjectionConfig,
    seed: int = 42,
) -> ConvergenceScanResult:
    """
    Run injection tracking across a series of particle counts; return strongly typed ConvergenceScanResult.

    Returns
    -------
    ConvergenceScanResult
        Structured scan result with scan_values, efficiencies, survived_counts, cpu_times_s, records, and to_dataframe().
    """
    results = []
    effs = []
    survived_list = []
    times = []
    emit_x_list = []
    emit_y_list = []

    for np_val in n_particle_values:
        t0 = time.perf_counter()
        beam = generate_6d_beam(
            n_particles=np_val,
            beta_x=config.inj_beta_x_m, alpha_x=config.inj_alpha_x, emit_x=config.inj_emit_x_m,
            beta_y=config.inj_beta_y_m, alpha_y=config.inj_alpha_y, emit_y=config.inj_emit_y_m,
            espread=config.inj_espread, blength=config.inj_blength_m,
            x_offset=config.septum_x_offset_m,
            seed=seed
        )
        res = track_multiturn_injection(
            beam, ring, n_turns=n_turns,
            kicker_model=kicker_model,
            kickmap_obj=kickmap_obj,
            config=config
        )
        dt = time.perf_counter() - t0
        effs.append(res.survival_fraction)
        survived_list.append(res.survived_particles)
        times.append(dt)
        emit_x_list.append(res.emittance_x_mrad)
        emit_y_list.append(res.emittance_y_mrad)
        results.append({
            "n_particles": np_val,
            "survived": res.survived_particles,
            "capture_efficiency": res.survival_fraction,
            "cpu_time_s": dt,
            "emittance_x_mrad": res.emittance_x_mrad,
            "emittance_y_mrad": res.emittance_y_mrad
        })

    return ConvergenceScanResult(
        scan_parameter="particle_count",
        scan_values=np.array(n_particle_values, dtype=int),
        efficiencies=np.array(effs, dtype=float),
        survived_counts=np.array(survived_list, dtype=int),
        cpu_times_s=np.array(times, dtype=float),
        final_emittance_x=np.array(emit_x_list, dtype=float),
        final_emittance_y=np.array(emit_y_list, dtype=float),
        records=results,
        metadata={"n_turns": n_turns, "kicker_model": kicker_model, "seed": seed}
    )


def turn_count_convergence_scan(
    n_turn_values: List[int],
    n_particles: int,
    ring,
    kicker_model: str,
    kickmap_obj: Optional[NKMKickMap2D],
    config: StorageRingInjectionConfig,
    seed: int = 42,
) -> ConvergenceScanResult:
    """
    Run injection tracking across a series of turn counts; return strongly typed ConvergenceScanResult.
    """
    results = []
    effs = []
    survived_list = []
    times = []
    emit_x_list = []
    emit_y_list = []

    beam_base = generate_6d_beam(
        n_particles=n_particles,
        beta_x=config.inj_beta_x_m, alpha_x=config.inj_alpha_x, emit_x=config.inj_emit_x_m,
        beta_y=config.inj_beta_y_m, alpha_y=config.inj_alpha_y, emit_y=config.inj_emit_y_m,
        espread=config.inj_espread, blength=config.inj_blength_m,
        x_offset=config.septum_x_offset_m,
        seed=seed
    )
    for n_turn_val in n_turn_values:
        t0 = time.perf_counter()
        res = track_multiturn_injection(
            beam_base.copy(), ring, n_turns=n_turn_val,
            kicker_model=kicker_model,
            kickmap_obj=kickmap_obj,
            config=config
        )
        dt = time.perf_counter() - t0
        effs.append(res.survival_fraction)
        survived_list.append(res.survived_particles)
        times.append(dt)
        emit_x_list.append(res.emittance_x_mrad)
        emit_y_list.append(res.emittance_y_mrad)
        results.append({
            "n_turns": n_turn_val,
            "survived": res.survived_particles,
            "capture_efficiency": res.survival_fraction,
            "cpu_time_s": dt,
            "emittance_x_mrad": res.emittance_x_mrad,
            "emittance_y_mrad": res.emittance_y_mrad
        })

    return ConvergenceScanResult(
        scan_parameter="turn_count",
        scan_values=np.array(n_turn_values, dtype=int),
        efficiencies=np.array(effs, dtype=float),
        survived_counts=np.array(survived_list, dtype=int),
        cpu_times_s=np.array(times, dtype=float),
        final_emittance_x=np.array(emit_x_list, dtype=float),
        final_emittance_y=np.array(emit_y_list, dtype=float),
        records=results,
        metadata={"n_particles": n_particles, "kicker_model": kicker_model, "seed": seed}
    )


# ---------------------------------------------------------------------------
# First-Loss Turn Distribution
# ---------------------------------------------------------------------------

def compute_first_loss_turn_distribution(tracking_result: TrackingResult, n_turns: int) -> Dict[str, Any]:
    """
    From loss_log, compute distribution of first loss turns.

    Returns
    -------
    dict with keys:
        first_loss_turns : list[int], turn of first loss for each lost particle
        turn_histogram : dict[int, int], number of first losses per turn
        mean_first_loss_turn : float
        fraction_lost_on_turn_1 : float
    """
    particle_first_loss: Dict[int, int] = {}
    for entry in tracking_result.loss_log:
        pidx = entry.get("particle_index", entry.get("particle_idx", -1))
        turn = entry.get("turn", 0)
        if pidx not in particle_first_loss:
            particle_first_loss[pidx] = turn

    first_loss_turns = list(particle_first_loss.values())
    histogram: Dict[int, int] = {}
    for t in range(1, n_turns + 1):
        histogram[t] = sum(1 for v in first_loss_turns if v == t)

    n_lost = len(first_loss_turns)
    mean_first = float(np.mean(first_loss_turns)) if n_lost > 0 else float("nan")
    frac_turn1 = float(histogram.get(1, 0) / n_lost) if n_lost > 0 else float("nan")

    return {
        "first_loss_turns": first_loss_turns,
        "turn_histogram": histogram,
        "mean_first_loss_turn": mean_first,
        "fraction_lost_on_turn_1": frac_turn1,
        "n_lost_particles": n_lost
    }


# ---------------------------------------------------------------------------
# Stored-Beam Perturbation
# ---------------------------------------------------------------------------

def compute_stored_beam_perturbation(stored_result: TrackingResult) -> Dict[str, float]:
    """
    Quantify stored-beam perturbation from NKM fringe fields.

    Metrics
    -------
    centroid_oscillation_x_mm : max |<x>| over turns
    centroid_oscillation_y_mm : max |<y>| (if available)
    emittance_growth_x_percent : relative emittance growth
    emittance_growth_y_percent : relative emittance growth vertical
    """
    cent_hist = stored_result.centroid_history  # shape (n_turns, 2): [x_mm, xp_mrad]
    emit_hist = stored_result.emittance_history   # shape (n_turns, 2): [emit_x, emit_y]

    valid_cx = cent_hist[:, 0][~np.isnan(cent_hist[:, 0])]
    centroid_osc_x = float(np.max(np.abs(valid_cx))) if len(valid_cx) > 0 else float("nan")

    emit_x = emit_hist[:, 0][~np.isnan(emit_hist[:, 0])]
    emit_y = emit_hist[:, 1][~np.isnan(emit_hist[:, 1])]
    emittance_growth_x = float(((emit_x[-1] - emit_x[0]) / emit_x[0]) * 100.0) if len(emit_x) > 1 and emit_x[0] > 0 else 0.0
    emittance_growth_y = float(((emit_y[-1] - emit_y[0]) / emit_y[0]) * 100.0) if len(emit_y) > 1 and emit_y[0] > 0 else 0.0

    return {
        "centroid_oscillation_x_mm": centroid_osc_x,
        "emittance_growth_x_percent": emittance_growth_x,
        "emittance_growth_y_percent": emittance_growth_y
    }


# ---------------------------------------------------------------------------
# Injection Acceptance (sweep over x-offset)
# ---------------------------------------------------------------------------

def compute_injection_acceptance(
    x_offsets_m: Union[Sequence[float], np.ndarray],
    n_particles: int,
    n_turns: int,
    ring,
    kicker_model: str,
    kickmap_obj: Optional[NKMKickMap2D],
    config: StorageRingInjectionConfig,
    seed: int = 42,
) -> AcceptanceResult:
    """
    Sweep injection x-offset to map the injection acceptance window; return strongly typed AcceptanceResult.

    Returns
    -------
    AcceptanceResult
        Structured acceptance result with x_grid_m, survival_fraction_grid, x_offsets_mm, acceptance_area_m_rad, and to_dataframe().
    """
    results = []
    x_arr = np.asarray(x_offsets_m, dtype=float)
    effs = []

    for x_off in x_arr:
        beam = generate_6d_beam(
            n_particles=n_particles,
            beta_x=config.inj_beta_x_m, alpha_x=config.inj_alpha_x, emit_x=config.inj_emit_x_m,
            beta_y=config.inj_beta_y_m, alpha_y=config.inj_alpha_y, emit_y=config.inj_emit_y_m,
            espread=config.inj_espread, blength=config.inj_blength_m,
            x_offset=float(x_off),
            seed=seed
        )
        res = track_multiturn_injection(
            beam, ring, n_turns=n_turns,
            kicker_model=kicker_model,
            kickmap_obj=kickmap_obj,
            config=config
        )
        effs.append(res.survival_fraction)
        results.append({
            "x_offset_m": float(x_off),
            "x_offset_mm": float(x_off * 1e3),
            "capture_efficiency": res.survival_fraction
        })

    effs_arr = np.array(effs, dtype=float)
    if len(x_arr) > 1:
        trapz_fn = getattr(np, "trapezoid", getattr(np, "trapz", None))
        area = float(abs(trapz_fn(effs_arr, x_arr))) if trapz_fn else float(np.sum(effs_arr) * abs(x_arr[1] - x_arr[0]))
    else:
        area = 0.0

    return AcceptanceResult(
        x_grid_m=x_arr,
        survival_fraction_grid=effs_arr,
        x_offsets_mm=x_arr * 1e3,
        acceptance_area_m_rad=area,
        records=results,
        metadata={"n_particles": n_particles, "n_turns": n_turns, "kicker_model": kicker_model, "seed": seed}
    )


# ---------------------------------------------------------------------------
# Full Multi-Seed Ensemble Runner
# ---------------------------------------------------------------------------

def _run_single_seed_ensemble(args: Tuple[int, int, InjectionStudyTierConfig, str, Any, Optional[NKMKickMap2D], StorageRingInjectionConfig, int]) -> Dict[str, Any]:
    """Top-level pickleable worker function for single-seed ensemble tracking."""
    i, seed, tier, kicker_model, ring, kickmap_obj, config, stored_beam_n_particles = args
    beam = generate_6d_beam(
        n_particles=tier.n_particles,
        beta_x=config.inj_beta_x_m, alpha_x=config.inj_alpha_x, emit_x=config.inj_emit_x_m,
        beta_y=config.inj_beta_y_m, alpha_y=config.inj_alpha_y, emit_y=config.inj_emit_y_m,
        espread=config.inj_espread, blength=config.inj_blength_m,
        x_offset=config.septum_x_offset_m,
        seed=seed
    )
    stored_beam = generate_6d_beam(
        n_particles=stored_beam_n_particles,
        beta_x=config.stored_beta_x_m, alpha_x=config.stored_alpha_x, emit_x=config.stored_emit_x_m,
        beta_y=config.stored_beta_y_m, alpha_y=config.stored_alpha_y, emit_y=config.stored_emit_y_m,
        espread=config.stored_espread, blength=config.stored_blength_m,
        x_offset=0.0,
        seed=seed
    )

    inj_res = track_multiturn_injection(
        beam, ring, n_turns=tier.n_turns,
        kicker_model=kicker_model,
        kickmap_obj=kickmap_obj,
        config=config
    )
    stored_res = track_multiturn_injection(
        stored_beam, ring, n_turns=tier.n_turns,
        kicker_model=kicker_model,
        kickmap_obj=kickmap_obj,
        config=config
    )

    perturbation = compute_stored_beam_perturbation(stored_res)
    fld = compute_first_loss_turn_distribution(inj_res, tier.n_turns)

    final_centroid = inj_res.centroid
    if final_centroid is not None:
        sep_clearance_mm = abs(final_centroid["x_mm"] - config.septum_x_offset_m * 1e3)
    else:
        sep_clearance_mm = float("nan")

    per_seed_item = {
        "seed": seed,
        "n_particles": tier.n_particles,
        "n_turns": tier.n_turns,
        "survived": inj_res.survived_particles,
        "capture_efficiency": inj_res.survival_fraction,
        "centroid_x_mm": final_centroid["x_mm"] if final_centroid else float("nan"),
        "emittance_x_mrad": inj_res.emittance_x_mrad,
        "emittance_y_mrad": inj_res.emittance_y_mrad,
        "septum_clearance_mm": sep_clearance_mm,
        "n_losses": len(inj_res.loss_log),
        "stored_perturbation": perturbation
    }

    return {
        "index": i,
        "survived": inj_res.survived_particles,
        "perturbation": perturbation,
        "fld": fld,
        "per_seed_item": per_seed_item
    }


def run_ensemble_study(
    tier: InjectionStudyTierConfig,
    ring,
    kicker_model: str,
    kickmap_obj: Optional[NKMKickMap2D],
    config: Optional[StorageRingInjectionConfig] = None,
    stored_beam_n_particles: int = 1000,
    n_workers: Optional[int] = 1,
) -> EnsembleStudyResult:
    """
    Run multi-seed ensemble injection study for one (kicker_model, tier) combination using sequential or parallel execution.

    Returns
    -------
    EnsembleStudyResult
        Structured ensemble study result with bootstrap confidence intervals, per-seed results, stored beam perturbations, and to_dataframe().
    """
    if config is None:
        config = StorageRingInjectionConfig()

    task_args = [
        (i, seed, tier, kicker_model, ring, kickmap_obj, config, stored_beam_n_particles)
        for i, seed in enumerate(tier.seeds)
    ]
    results = parallel_map(_run_single_seed_ensemble, task_args, n_workers=n_workers, desc="run_ensemble_study")

    survived_counts: List[int] = []
    per_seed: List[Dict[str, Any]] = []
    all_stored_perturbations: List[Dict[str, float]] = []
    first_loss_dist: Optional[Dict[str, Any]] = None

    for res in results:
        survived_counts.append(res["survived"])
        all_stored_perturbations.append(res["perturbation"])
        per_seed.append(res["per_seed_item"])
        if res["index"] == 0:
            first_loss_dist = res["fld"]

    ci = bootstrap_capture_ci(survived_counts, tier.n_particles)

    # Mean stored perturbation across seeds
    mean_perturbation: Dict[str, float] = {}
    if all_stored_perturbations:
        for k in all_stored_perturbations[0]:
            vals = [p[k] for p in all_stored_perturbations if not np.isnan(p[k])]
            mean_perturbation[k] = float(np.mean(vals)) if vals else float("nan")

    return EnsembleStudyResult(
        label=tier.label,
        kicker_model=kicker_model,
        tier={
            "n_particles": tier.n_particles,
            "n_turns": tier.n_turns,
            "n_slices": tier.n_slices,
            "seeds": tier.seeds
        },
        capture_efficiency_ci=ci,
        per_seed_results=per_seed,
        mean_stored_perturbation=mean_perturbation,
        first_loss_distribution=first_loss_dist,
    )
