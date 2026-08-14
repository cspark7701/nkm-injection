"""
NKM End-to-End Injection Simulation & Performance Evaluation Module

Compares NKM injection dynamics across three models:
1. NKM Off (zero field)
2. Idealized Linear Kicker
3. Validated RADIA Field-Map NKM

Computes injected beam separation, stored beam perturbation, transmission, and phase-space metrics.
"""

from typing import Dict, Tuple, Optional, Any, Callable, Union
import numpy as np

from .beam import compute_beam_statistics, compute_beam_centroid, compute_projected_emittance
from .tracking import track_nkm_thin_kick
from .units import KickMapMetadata


def simulate_nkm_models(injected_beam: np.ndarray,
                         circulating_beam: np.ndarray,
                         kickmap_obj: Any,
                         length_m: float = 0.525,
                         energy_GeV: float = 4.0,
                         scale_factor: float = 1.0,
                         config: Optional[Any] = None) -> Dict[str, Any]:
    """
    Simulate injection tracking for both injected and circulating beams across three models:
    - Model 1: NKM Off
    - Model 2: Idealized Kicker
    - Model 3: Realistic RADIA 2D Kick Map
    
    Returns:
        Dictionary containing tracking outputs and comparison metrics.
    """
    from .storage_ring_injection import get_kicker_evaluator, StorageRingInjectionConfig

    if config is None:
        config = StorageRingInjectionConfig(
            energy_eV=energy_GeV * 1e9,
            nkm_length_m=length_m
        )

    # 1. Model 1: NKM Off
    kick_off, meta_off = get_kicker_evaluator("off", config=config)
    inj_off = track_nkm_thin_kick(injected_beam, kick_off, scale_factor=0.0, length_m=length_m, energy_GeV=energy_GeV, metadata=meta_off)
    circ_off = track_nkm_thin_kick(circulating_beam, kick_off, scale_factor=0.0, length_m=length_m, energy_GeV=energy_GeV, metadata=meta_off)
    
    # 2. Model 2: Idealized Kicker
    kick_ideal, meta_ideal = get_kicker_evaluator("ideal", config=config)
    inj_ideal = track_nkm_thin_kick(injected_beam, kick_ideal, scale_factor=scale_factor, length_m=length_m, energy_GeV=energy_GeV, metadata=meta_ideal)
    circ_ideal = track_nkm_thin_kick(circulating_beam, kick_off, scale_factor=0.0, length_m=length_m, energy_GeV=energy_GeV, metadata=meta_off)
    
    # 3. Model 3: Realistic 2D Kick Map
    kick_map_fn, meta_map = get_kicker_evaluator("fieldmap", config=config, kickmap_obj=kickmap_obj)
    inj_fieldmap = track_nkm_thin_kick(injected_beam, kick_map_fn, scale_factor=scale_factor, length_m=length_m, energy_GeV=energy_GeV, metadata=meta_map)
    circ_fieldmap = track_nkm_thin_kick(circulating_beam, kick_map_fn, scale_factor=scale_factor, length_m=length_m, energy_GeV=energy_GeV, metadata=meta_map)
    
    # Compute centroids
    c_inj_in = compute_beam_centroid(injected_beam)
    c_circ_in = compute_beam_centroid(circulating_beam)
    
    c_inj_fieldmap = compute_beam_centroid(inj_fieldmap)
    c_circ_fieldmap = compute_beam_centroid(circ_fieldmap)
    
    # Separation distance at NKM exit (in mm)
    separation_mm = float(abs(c_inj_fieldmap[0] - c_circ_fieldmap[0]) * 1e3)
    
    # Stored beam perturbation at NKM exit (in mrad)
    circ_kick_mrad = float((c_circ_fieldmap[1] - c_circ_in[1]) * 1e3)
    
    # Injected beam kick angle (in mrad)
    inj_kick_mrad = float((c_inj_fieldmap[1] - c_inj_in[1]) * 1e3)
    
    return {
        "models": {
            "nkm_off": {
                "injected_stats": compute_beam_statistics(inj_off),
                "circulating_stats": compute_beam_statistics(circ_off),
            },
            "nkm_idealized": {
                "injected_stats": compute_beam_statistics(inj_ideal),
                "circulating_stats": compute_beam_statistics(circ_ideal),
            },
            "nkm_fieldmap": {
                "injected_stats": compute_beam_statistics(inj_fieldmap),
                "circulating_stats": compute_beam_statistics(circ_fieldmap),
            }
        },
        "performance_metrics": {
            "injected_kick_mrad": inj_kick_mrad,
            "stored_beam_kick_mrad": circ_kick_mrad,
            "beam_separation_mm": separation_mm,
            "injected_survival_fraction": compute_beam_statistics(inj_fieldmap)["survival_fraction"],
            "circulating_survival_fraction": compute_beam_statistics(circ_fieldmap)["survival_fraction"],
        },
        "beams": {
            "inj_fieldmap": inj_fieldmap,
            "circ_fieldmap": circ_fieldmap,
        }
    }
