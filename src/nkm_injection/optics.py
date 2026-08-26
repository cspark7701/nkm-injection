"""
BTS Linear Optics and Mismatch Analysis Module

Provides functions for uncoupled Twiss propagation, phase advances, dispersion,
beam covariance matrix calculations, and plane-by-plane phase-space mismatch metrics.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any, Union, Literal
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import at


@dataclass(frozen=True)
class TwissParameters:
    """Immutable Twiss and dispersion parameters at a specific longitudinal position."""
    beta_x: float
    beta_y: float
    alpha_x: float
    alpha_y: float
    disp_x: float = 0.0
    disp_px: float = 0.0
    disp_y: float = 0.0
    disp_py: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to AT-compatible Twiss dictionary representation."""
        return {
            'beta': [self.beta_x, self.beta_y],
            'alpha': [self.alpha_x, self.alpha_y],
            'dispersion': [self.disp_x, self.disp_px, self.disp_y, self.disp_py]
        }


# Canonical BTS Entrance Optics (extracted beam from Booster)
DEFAULT_BTS_ENTRANCE_TWISS = TwissParameters(
    beta_x=7.560000,
    beta_y=12.269000,
    alpha_x=1.523100,
    alpha_y=-1.654700,
    disp_x=0.276200,
    disp_px=-0.065700,
    disp_y=0.0,
    disp_py=0.0
)

# Canonical BTS Exit Target Optics (matched to Storage Ring Injection Point)
DEFAULT_BTS_TARGET_TWISS = TwissParameters(
    beta_x=2.336495,
    beta_y=4.256241,
    alpha_x=-0.016335,
    alpha_y=0.017772,
    disp_x=0.080868,
    disp_px=0.047472,
    disp_y=0.0,
    disp_py=0.0
)


def beam_sigma_matrix_2d(beta: float, alpha: float, emit: float = 1.0) -> np.ndarray:
    """
    Construct a 2x2 beam covariance matrix Sigma in phase space (u, u').
    
    Sigma = emit * [[beta, -alpha], [-alpha, (1 + alpha^2) / beta]]
    """
    gamma = (1.0 + alpha**2) / beta
    return emit * np.array([
        [beta, -alpha],
        [-alpha, gamma]
    ])


def compute_mismatch_metric(beta_out: float, alpha_out: float,
                            beta_target: float, alpha_target: float) -> float:
    """
    Calculate the plane-by-plane phase space mismatch metric M_u:
    
        M_u = 0.5 * Tr(Sigma_{target}^-1 * Sigma_{out}) - 1
        
    Args:
        beta_out: Output beta function (m)
        alpha_out: Output alpha parameter
        beta_target: Target beta function (m)
        alpha_target: Target alpha parameter
        
    Returns:
        Mismatch value M_u >= 0. Exactly 0 when output matches target.
    """
    sigma_target = beam_sigma_matrix_2d(beta_target, alpha_target, emit=1.0)
    sigma_out = beam_sigma_matrix_2d(beta_out, alpha_out, emit=1.0)
    
    sigma_target_inv = np.linalg.inv(sigma_target)
    tr = np.trace(sigma_target_inv @ sigma_out)
    return float(0.5 * tr - 1.0)


def compute_twiss_propagation(lattice: at.Lattice, initial_twiss: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propagate linear optics through the lattice given initial Twiss parameters.
    
    Args:
        lattice: at.Lattice instance
        initial_twiss: dict with keys 'beta', 'alpha', 'dispersion'
        
    Returns:
        Dictionary containing arrays of s_pos, beta, alpha, dispersion, mu, and final Twiss values.
    """
    linopt0, latopt, linopt = at.linopt6(lattice, refpts=range(len(lattice) + 1), twiss_in=initial_twiss)
    
    s_pos = np.array([elem['s_pos'] for elem in linopt])
    beta_all = np.array([elem['beta'] for elem in linopt])
    alpha_all = np.array([elem['alpha'] for elem in linopt])
    disp_all = np.array([elem['dispersion'] for elem in linopt])
    mu_all = np.array(linopt['mu']) if 'mu' in linopt.dtype.names else np.zeros_like(beta_all)

    return {
        "s_pos": s_pos,
        "beta": beta_all,
        "alpha": alpha_all,
        "dispersion": disp_all,
        "mu": mu_all,
        "final_beta": beta_all[-1],
        "final_alpha": alpha_all[-1],
        "final_dispersion": disp_all[-1],
        "max_beta_x": float(np.max(beta_all[:, 0])),
        "max_beta_y": float(np.max(beta_all[:, 1])),
        "max_dispersion_x": float(np.max(disp_all[:, 0])),
    }


def compute_bts_optics_metrics(lattice: at.Lattice,
                               initial_twiss: Dict[str, Any],
                               target_twiss: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute optics propagation and evaluate mismatch metrics relative to target parameters.
    """
    prop = compute_twiss_propagation(lattice, initial_twiss)
    
    beta_end = prop["final_beta"]
    alpha_end = prop["final_alpha"]
    disp_end = prop["final_dispersion"]
    
    target_beta = target_twiss["beta"]
    target_alpha = target_twiss["alpha"]
    target_disp = target_twiss["dispersion"]
    
    mismatch_x = compute_mismatch_metric(beta_end[0], alpha_end[0], target_beta[0], target_alpha[0])
    mismatch_y = compute_mismatch_metric(beta_end[1], alpha_end[1], target_beta[1], target_alpha[1])
    
    disp_residual_x = float(disp_end[0] - target_disp[0])
    disp_px_residual_x = float(disp_end[1] - target_disp[1])
    
    return {
        "propagation": prop,
        "mismatch_x": mismatch_x,
        "mismatch_y": mismatch_y,
        "dispersion_x_residual_m": disp_residual_x,
        "dispersion_px_residual": disp_px_residual_x,
        "final_beta_x": float(beta_end[0]),
        "final_beta_y": float(beta_end[1]),
        "target_beta_x": float(target_beta[0]),
        "target_beta_y": float(target_beta[1]),
    }


def plot_bts_optics(lattice: at.Lattice,
                    initial_twiss: Dict[str, Any],
                    output_path: Optional[Path] = None) -> plt.Figure:
    """
    Generate publication-quality plots of BTS beta functions, dispersion, and phase advances.
    """
    prop = compute_twiss_propagation(lattice, initial_twiss)
    s = prop["s_pos"]
    beta_x, beta_y = prop["beta"][:, 0], prop["beta"][:, 1]
    dx = prop["dispersion"][:, 0]
    mu_x, mu_y = prop["mu"][:, 0], prop["mu"][:, 1]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    # 1. Beta functions
    ax1.plot(s, beta_x, 'b-', label=r'$\beta_x$ (m)')
    ax1.plot(s, beta_y, 'r--', label=r'$\beta_y$ (m)')
    ax1.set_ylabel(r'$\beta$ [m]')
    ax1.set_title('BTS Optical Functions')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # 2. Dispersion
    ax2.plot(s, dx, 'g-', label=r'$D_x$ (m)')
    ax2.set_ylabel(r'$D_x$ [m]')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')
    
    # 3. Phase advance
    ax3.plot(s, mu_x, 'b-', label=r'$\mu_x$ (rad)')
    ax3.plot(s, mu_y, 'r--', label=r'$\mu_y$ (rad)')
    ax3.set_xlabel('s [m]')
    ax3.set_ylabel(r'$\mu$ [rad]')
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.legend(loc='upper right')
    
    plt.tight_layout()
    
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        
    return fig


def compute_beam_envelope(
    beta: Union[float, np.ndarray],
    dispersion: Union[float, np.ndarray] = 0.0,
    emittance_m_rad: float = 1.0e-7,
    energy_spread: float = 1.1e-3,
    n_sigma: float = 3.0,
    method: Literal["rms_quadrature", "conservative_linear"] = "rms_quadrature"
) -> Union[float, np.ndarray]:
    """
    Compute transverse beam envelope in meters.

    Parameters
    ----------
    beta : float or np.ndarray
        Betatron function [m].
    dispersion : float or np.ndarray, optional
        Dispersion function [m] (default: 0.0).
    emittance_m_rad : float, optional
        Beam emittance [m*rad] (default: 1.0e-7).
    energy_spread : float, optional
        Fractional energy spread sigma_delta (default: 1.1e-3).
    n_sigma : float, optional
        Envelope scale factor (default: 3.0).
    method : {"rms_quadrature", "conservative_linear"}, optional
        - 'rms_quadrature': n_sigma * sqrt(emittance * beta + (dispersion * energy_spread)**2)
        - 'conservative_linear': n_sigma * sqrt(emittance * beta) + abs(dispersion * energy_spread)

    Returns
    -------
    envelope : float or np.ndarray
        Transverse beam half-envelope [m].
    """
    beta_arr = np.asarray(beta)
    disp_arr = np.asarray(dispersion)

    if method == "rms_quadrature":
        sigma = np.sqrt(np.maximum(emittance_m_rad * beta_arr, 0.0) + (disp_arr * energy_spread)**2)
        envelope = n_sigma * sigma
    elif method == "conservative_linear":
        sigma_bet = np.sqrt(np.maximum(emittance_m_rad * beta_arr, 0.0))
        envelope = n_sigma * sigma_bet + np.abs(disp_arr * energy_spread)
    else:
        raise ValueError(f"Unknown envelope method '{method}'. Choose 'rms_quadrature' or 'conservative_linear'.")

    if np.ndim(beta) == 0 and np.ndim(dispersion) == 0:
        return float(envelope.item())
    return envelope

