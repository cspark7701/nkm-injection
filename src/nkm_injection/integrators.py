"""
NKM Integrators Module — Symplectic Split and Lorentz RK4 Integrators

Provides centered drift-kick-drift (symplectic split-operator) and 4th-order Runge-Kutta
numerical integrators for tracking relativistic beam distributions through thick magnetic elements.
"""

from typing import Tuple, Callable, Union
import numpy as np

from .units import (
    integrated_field_to_transverse_kicks,
    ELECTRON_CHARGE_C,
    FieldMap3DProtocol
)

from .tracking_contracts import TrackingParameters, validate_particle_array, drift, finite_components, require_finite_active


class _IntegratorSetup:
    """Common parameter setup; integration algorithms remain separate."""
    def __init__(self, field_fn: Union[FieldMap3DProtocol, Callable],
                 length_m: float = 0.525, n_slices: int = 40, energy_GeV: float = 4.0,
                 particle_charge_C: float = ELECTRON_CHARGE_C, scale_factor: float = 1.0):
        if not callable(field_fn):
            raise TypeError('field_fn must be callable and return (By, Bx) in T')
        self.parameters = TrackingParameters(length_m, n_slices, energy_GeV,
                                             particle_charge_C, scale_factor)
        self.field_fn = field_fn
        for name in ('length_m', 'n_slices', 'energy_GeV', 'particle_charge_C', 'scale_factor',
                     'energy_eV', 'brho', 'dz'):
            setattr(self, name, getattr(self.parameters, name))
        self.charge_sign = float(np.sign(self.particle_charge_C))

    def _field(self, x, y, z):
        return finite_components(self.field_fn(x, y, z), x.shape, 'field_fn (By, Bx in T)')


class SymplecticSplitIntegrator(_IntegratorSetup):
    """
    Symplectic Split-Operator Integrator (Drift-Kick-Drift map per slice).
    
    Order: 2nd-order Symplectic (Verlet).
    For each longitudinal slice of thickness dz = L / N_slices:
      1. Half-drift dz / 2
      2. Centered thin kick at slice center z_mid
      3. Half-drift dz / 2
    """
    def track(self, beam: np.ndarray) -> np.ndarray:
        """
        Track 6D particle array of shape (6, n_particles) through N_slices.
        """
        out_beam, valid_mask = validate_particle_array(beam, copy=True)
        if not np.any(valid_mask) or self.length_m == 0 or self.scale_factor == 0:
            drift(out_beam, valid_mask, self.length_m)
            validate_particle_array(out_beam)
            return out_beam

        dz = self.dz
        half_dz = dz * 0.5

        for i in range(self.n_slices):
            z_mid = (i + 0.5) * dz

            # 1. Half drift dz / 2
            drift(out_beam, valid_mask, half_dz)

            # 2. Centered kick at z_mid
            x = out_beam[0, valid_mask]
            y = out_beam[2, valid_mask]

            by_val, bx_val = self._field(x, y, z_mid)
            by_val = by_val * self.scale_factor
            bx_val = bx_val * self.scale_factor

            # Deflection angles in radians via component-aware unified helper
            delta_xp, delta_yp = integrated_field_to_transverse_kicks(
                int_bx_t_m=bx_val * dz,
                int_by_t_m=by_val * dz,
                beam_energy_eV=self.energy_eV,
                particle_charge_C=self.particle_charge_C
            )

            out_beam[1, valid_mask] += delta_xp
            out_beam[3, valid_mask] += delta_yp

            # 3. Half drift dz / 2
            drift(out_beam, valid_mask, half_dz)

        require_finite_active(out_beam, valid_mask)
        return out_beam


class LorentzRK4Integrator(_IntegratorSetup):
    """
    Genuine 4th-Order Runge-Kutta (RK4) Lorentz Force Integrator.
    
    Non-symplectic 4th-order ODE integrator for 6D particle trajectories.
    """
    def _derivatives(self, state: np.ndarray, z: float) -> np.ndarray:
        """
        Compute dx/dz, dx'/dz, dy/dz, dy'/dz for 4D state [x, xp, y, yp].
        """
        x, xp, y, yp = state[0], state[1], state[2], state[3]
        by_val, bx_val = self._field(x, y, z)
        by_val = by_val * self.scale_factor
        bx_val = bx_val * self.scale_factor

        dx_dz = xp
        dy_dz = yp
        dxp_dz, dyp_dz = integrated_field_to_transverse_kicks(
            int_bx_t_m=bx_val,
            int_by_t_m=by_val,
            beam_energy_eV=self.energy_eV,
            particle_charge_C=self.particle_charge_C
        )

        return np.array([dx_dz, dxp_dz, dy_dz, dyp_dz])

    def track(self, beam: np.ndarray) -> np.ndarray:
        """
        Track 6D particle array of shape (6, n_particles) using 4th-order RK4.
        """
        out_beam, valid_mask = validate_particle_array(beam, copy=True)
        if not np.any(valid_mask) or self.length_m == 0 or self.scale_factor == 0:
            drift(out_beam, valid_mask, self.length_m)
            validate_particle_array(out_beam)
            return out_beam

        dz = self.dz

        for i in range(self.n_slices):
            z0 = i * dz
            z_mid = z0 + 0.5 * dz
            z1 = z0 + dz

            state = out_beam[:4, valid_mask]

            k1 = self._derivatives(state, z0)
            k2 = self._derivatives(state + 0.5 * dz * k1, z_mid)
            k3 = self._derivatives(state + 0.5 * dz * k2, z_mid)
            k4 = self._derivatives(state + dz * k3, z1)

            out_beam[:4, valid_mask] += (dz / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        require_finite_active(out_beam, valid_mask)
        return out_beam
