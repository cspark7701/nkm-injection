"""
NKM BTS Normalized Objectives and Merit Function Module

Defines target optics observables, physical normalization scales, and normalized
residual calculations for least-squares and constrained optimization.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np

from .bts_lattice import BTSConfig, create_bts_lattice
from .optics import (
    compute_twiss_propagation,
    compute_mismatch_metric,
    DEFAULT_BTS_ENTRANCE_TWISS,
    DEFAULT_BTS_TARGET_TWISS
)


@dataclass
class OpticsTargetConfig:
    """Target optics parameters and physical normalization tolerances at BTS exit."""
    # Target Twiss values at BTS exit
    target_beta_x: float = DEFAULT_BTS_TARGET_TWISS.beta_x
    target_beta_y: float = DEFAULT_BTS_TARGET_TWISS.beta_y
    target_alpha_x: float = DEFAULT_BTS_TARGET_TWISS.alpha_x
    target_alpha_y: float = DEFAULT_BTS_TARGET_TWISS.alpha_y
    target_disp_x: float = DEFAULT_BTS_TARGET_TWISS.disp_x
    target_disp_px: float = DEFAULT_BTS_TARGET_TWISS.disp_px

    # Physical normalization scales (sigma_i tolerances)
    sigma_beta_x: float = 0.05
    sigma_beta_y: float = 0.05
    sigma_alpha_x: float = 0.01
    sigma_alpha_y: float = 0.01
    sigma_disp_x: float = 0.002
    sigma_disp_px: float = 0.001

    # Initial Twiss values at BTS entrance
    init_beta_x: float = DEFAULT_BTS_ENTRANCE_TWISS.beta_x
    init_beta_y: float = DEFAULT_BTS_ENTRANCE_TWISS.beta_y
    init_alpha_x: float = DEFAULT_BTS_ENTRANCE_TWISS.alpha_x
    init_alpha_y: float = DEFAULT_BTS_ENTRANCE_TWISS.alpha_y
    init_disp_x: float = DEFAULT_BTS_ENTRANCE_TWISS.disp_x
    init_disp_px: float = DEFAULT_BTS_ENTRANCE_TWISS.disp_px



class BTSNormalizedObjectives:
    """
    Computes normalized objective residuals r_i = (O_i - O_i,target) / sigma_i
    and sum of squared residuals J = sum(r_i^2).
    """
    def __init__(self, config: Optional[OpticsTargetConfig] = None,
                 lattice: Optional[Any] = None,
                 copy_lattice: bool = False):
        self.config = config or OpticsTargetConfig()

        self.initial_twiss = {
            'beta': [self.config.init_beta_x, self.config.init_beta_y],
            'alpha': [self.config.init_alpha_x, self.config.init_alpha_y],
            'dispersion': [self.config.init_disp_x, self.config.init_disp_px, 0.0, 0.0]
        }

        self.nominal_bts_config = BTSConfig()
        self.nominal_strengths = np.array(self.nominal_bts_config.quad_strengths_list)
        if lattice is not None:
            self.lattice = lattice.copy() if copy_lattice else lattice
        else:
            self.lattice = create_bts_lattice(self.nominal_bts_config)
            if copy_lattice:
                self.lattice = self.lattice.copy()

        self.quad_names = ['q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33']
        self._quad_elems = [elem for elem in self.lattice if elem.FamName in self.quad_names]

    def set_quads(self, strengths: np.ndarray) -> None:
        """Update quadrupole strengths K in the lattice in-place."""
        k_map = dict(zip(self.quad_names, strengths))
        for elem in self._quad_elems:
            elem.K = k_map[elem.FamName]

    def compute_residual_vector(self, strengths: np.ndarray) -> np.ndarray:
        """
        Compute normalized residual vector [r_bx, r_by, r_ax, r_ay, r_dx, r_dpx].
        
        r_i = (O_i - O_i,target) / sigma_i
        """
        self.set_quads(strengths)
        try:
            prop = compute_twiss_propagation(self.lattice, self.initial_twiss)
            beta_end = prop["final_beta"]
            alpha_end = prop["final_alpha"]
            disp_end = prop["final_dispersion"]

            r_bx = (beta_end[0] - self.config.target_beta_x) / self.config.sigma_beta_x
            r_by = (beta_end[1] - self.config.target_beta_y) / self.config.sigma_beta_y
            r_ax = (alpha_end[0] - self.config.target_alpha_x) / self.config.sigma_alpha_x
            r_ay = (alpha_end[1] - self.config.target_alpha_y) / self.config.sigma_alpha_y
            r_dx = (disp_end[0] - self.config.target_disp_x) / self.config.sigma_disp_x
            r_dpx = (disp_end[1] - self.config.target_disp_px) / self.config.sigma_disp_px

            return np.array([r_bx, r_by, r_ax, r_ay, r_dx, r_dpx])
        except Exception:
            return np.full(6, 1e4)

    def compute_scalar_merit(self, strengths: np.ndarray) -> float:
        """
        Compute sum of squared normalized residuals J = sum(r_i^2).
        """
        r_vec = self.compute_residual_vector(strengths)
        return float(np.sum(r_vec**2))
