"""
NKM 2D Kick Map Processing and Interpolation Module

Provides read-only ingestion, 2D interpolation, symmetry quantification,
and Lorentz-force kick verification for 2D field/kick maps (e.g. kickmap_file.txt).
"""

from pathlib import Path
from typing import Dict, Tuple, Optional, Any, Union
import numpy as np
from scipy.interpolate import RegularGridInterpolator

from .fieldmap import BaseFieldMap
from ._fieldmap_validation import broadcast_coordinates, validate_axis, validate_values
from .units import (
    KickMapMetadata,
    convert_kick_angle,
    convert_integrated_field,
    integrated_field_to_kick,
    integrated_field_to_transverse_kicks,
    ELECTRON_CHARGE_C
)


def load_2d_kickmap(filepath: Union[str, Path]) -> Tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Parse a 2D kick map text file (e.g. kickmap_file.txt).
    
    Format:
        Length (m)
        Nx, Ny
        START
        x_grid values
        y_coord, row_values... (Section 1: Ky map / vertical field integral By ds)
        START
        x_grid values
        y_coord, row_values... (Section 2: Kx map / horizontal field integral Bx ds)
        
    Returns:
        Tuple of (length_m, x_grid, y_grid, kx_map, ky_map)
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Kick map file not found: {path}")
        
    with open(path, 'r') as f:
        lines = [line.split('#')[0].strip() for line in f if line.split('#')[0].strip()]
        
    tokens = ' '.join(lines).split()
    
    start_indices = [i for i, token in enumerate(tokens) if token == "START"]
    if len(start_indices) != 2 or start_indices[0] != 3:
        raise ValueError("Expected length, Nx, Ny and exactly two START sections")
    length_m = float(tokens[0])
    nx, ny = int(tokens[1]), int(tokens[2])
    if not np.isfinite(length_m) or length_m <= 0:
        raise ValueError("Kick-map length (m) must be finite and positive")
    if nx < 2 or ny < 2:
        raise ValueError("Kick-map dimensions Nx and Ny must each be at least two")
    s1, s2 = start_indices

    def parse_section(section, name):
        expected = nx + ny * (nx + 1)
        if len(section) != expected:
            raise ValueError(f"{name} must contain {expected} values, got {len(section)}")
        values = np.asarray(section, dtype=float)
        x = validate_axis(values[:nx], f"{name} x (m)")
        rows = values[nx:].reshape(ny, nx + 1)
        y = validate_axis(rows[:, 0], f"{name} y (m)")
        return x, y, validate_values(rows[:, 1:], (ny, nx), name)

    x_grid, y_grid, ky_map = parse_section(tokens[s1 + 1:s2], "section 1")
    x_second, y_second, kx_map = parse_section(tokens[s2 + 1:], "section 2")
    if not np.array_equal(x_grid, x_second) or not np.array_equal(y_grid, y_second):
        raise ValueError("Kick-map sections must have identical x and y axes")

    return length_m, x_grid, y_grid, kx_map, ky_map


class NKMKickMap2D(BaseFieldMap):
    """
    2D Interpolator for NKM kick maps with strict bounds checking, explicit metadata, and symmetry analytics.
    """
    def __init__(self, filepath: Union[str, Path],
                 allow_extrapolation: bool = False,
                 metadata: Optional[KickMapMetadata] = None):
        fp = Path(filepath)
        length_m, x_grid, y_grid, kx_map, ky_map = load_2d_kickmap(fp)
        
        meta = metadata or KickMapMetadata(
            coordinate_unit="m",
            value_type="kick_angle",
            value_unit="mrad",
            beam_energy_eV=4.0e9,
            particle_charge_C=ELECTRON_CHARGE_C,
            longitudinal_unit="m",
            sign_convention="AT"
        )

        super().__init__(
            x_min=float(x_grid.min()),
            x_max=float(x_grid.max()),
            y_min=float(y_grid.min()),
            y_max=float(y_grid.max()),
            allow_extrapolation=allow_extrapolation,
            metadata=meta,
            filepath=fp
        )

        self.length_m = length_m
        self.x_grid = x_grid
        self.y_grid = y_grid
        self.kx_map = kx_map
        self.ky_map = ky_map
        self.model_type = "fieldmap"
        self.energy_eV = float(self.metadata.beam_energy_eV) if self.metadata.beam_energy_eV is not None else 4.0e9
        
        fill_val = None if allow_extrapolation else np.nan
        bounds_err = not allow_extrapolation
        
        # RegularGridInterpolator expects points as (y_grid, x_grid) matching matrix shape (ny, nx)
        self._interp_kx = RegularGridInterpolator((self.y_grid, self.x_grid), self.kx_map,
                                                   bounds_error=bounds_err, fill_value=fill_val)
        self._interp_ky = RegularGridInterpolator((self.y_grid, self.x_grid), self.ky_map,
                                                   bounds_error=bounds_err, fill_value=fill_val)

    def __call__(self, x: Union[float, np.ndarray], y: Union[float, np.ndarray]) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
        """Evaluate raw map values (Kx, Ky) at (x, y)."""
        return self.evaluate(x, y)

    def evaluate(self, x: Union[float, np.ndarray], y: Union[float, np.ndarray]) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
        """
        Evaluate raw map values (Kx, Ky) at (x, y) as stored in map file.
        
        Args:
            x: horizontal position in m
            y: vertical position in m
            
        Returns:
            Raw (Kx, Ky) with NumPy broadcast shape, or floats for scalars.
            Nonfinite queries and incompatible shapes raise ValueError; outside
            queries raise OutOfDomainError unless extrapolation is enabled.
        """
        x_arr, y_arr = broadcast_coordinates(("x (m)", x), ("y (m)", y))
        self.check_domain_bounds(x_arr, y_arr)
        pts = np.stack((y_arr, x_arr), axis=-1).reshape(-1, 2)
        kx_eval = self._interp_kx(pts).reshape(x_arr.shape)
        ky_eval = self._interp_ky(pts).reshape(x_arr.shape)
        if x_arr.ndim == 0:
            return float(kx_eval), float(ky_eval)
        return kx_eval, ky_eval

    def evaluate_kick(self, x: Union[float, np.ndarray],
                      y: Union[float, np.ndarray],
                      energy_eV: Optional[float] = None) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
        """
        Evaluate (kick_x, kick_y) kick angles in radians at position (x, y).
        
        Uses self.metadata to perform unit-safe conversion to radians.
        """
        kx_raw, ky_raw = self.evaluate(x, y)
        if self.metadata.value_type == "kick_angle":
            kick_x = convert_kick_angle(kx_raw, self.metadata.value_unit, "rad")
            kick_y = convert_kick_angle(ky_raw, self.metadata.value_unit, "rad")
        elif self.metadata.value_type == "integrated_field":
            int_bx = convert_integrated_field(kx_raw, self.metadata.value_unit, "T_m")
            int_by = convert_integrated_field(ky_raw, self.metadata.value_unit, "T_m")
            energy = energy_eV if energy_eV is not None else self.metadata.beam_energy_eV
            if energy is None:
                raise ValueError("beam_energy_eV must be provided in metadata or as argument")
            kick_x, kick_y = integrated_field_to_transverse_kicks(
                int_bx_t_m=int_bx,
                int_by_t_m=int_by,
                beam_energy_eV=energy,
                particle_charge_C=self.metadata.particle_charge_C,
                coordinate_convention=self.metadata.sign_convention
            )
        else:
            raise ValueError(f"Cannot evaluate kick angle directly from value_type '{self.metadata.value_type}'")
        return kick_x, kick_y

    def evaluate_kicks(self, x: Union[float, np.ndarray],
                       y: Optional[Union[float, np.ndarray]] = None) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
        """
        Evaluate (delta_xp_rad, delta_yp_rad) in radians for transverse coordinates.
        Conforms to KickerEvaluatorProtocol.
        """
        if y is None:
            if isinstance(x, np.ndarray):
                y = np.zeros_like(x)
            else:
                y = 0.0
        return self.evaluate_kick(x, y)

    def verify_grid_interpolation(self) -> float:
        """
        Verify interpolation accuracy at exact grid nodes.
        
        Returns:
            Maximum absolute error between interpolated and original matrix values.
        """
        Y, X = np.meshgrid(self.y_grid, self.x_grid, indexing='ij')
        pts = np.column_stack([Y.ravel(), X.ravel()])
        
        kx_interp = self._interp_kx(pts).reshape(self.kx_map.shape)
        ky_interp = self._interp_ky(pts).reshape(self.ky_map.shape)
        
        err_x = float(np.max(np.abs(kx_interp - self.kx_map)))
        err_y = float(np.max(np.abs(ky_interp - self.ky_map)))
        return max(err_x, err_y)

    def compute_symmetry_residuals(self) -> Dict[str, float]:
        """
        Quantify 2D symmetry and antisymmetry residuals across the x-y grid.
        
        - Kx (Section 1 in kickmap_file) exhibits odd symmetry in x: Kx(-x, y) = -Kx(x, y)
        - Ky (Section 2 in kickmap_file) exhibits odd symmetry in y: Ky(x, -y) = -Ky(x, y)
        """
        kx_flipped_x = np.fliplr(self.kx_map)
        ky_flipped_y = np.flipud(self.ky_map)
        
        odd_sym_kx = float(np.max(np.abs(self.kx_map + kx_flipped_x)))
        odd_sym_ky = float(np.max(np.abs(self.ky_map + ky_flipped_y)))
        
        return {
            "kx_odd_x_symmetry_residual": odd_sym_kx,
            "ky_odd_y_symmetry_residual": odd_sym_ky,
            "kx_peak_value": float(np.max(np.abs(self.kx_map))),
            "ky_peak_value": float(np.max(np.abs(self.ky_map))),
        }

    def verify_lorentz_kick_sign(self, x_offset_m: float = -0.010, energy_GeV: float = 4.0) -> Dict[str, Any]:
        """
        Verify the sign convention of Lorentz-force kick on a relativistic electron beam.
        """
        energy_eV = energy_GeV * 1e9
        kx_rad, ky_rad = self.evaluate_kick(x_offset_m, 0.0, energy_eV=energy_eV)
        kx_raw, ky_raw = self.evaluate(x_offset_m, 0.0)
        
        return {
            "x_offset_mm": x_offset_m * 1e3,
            "kx_value": float(kx_raw),
            "ky_value": float(ky_raw),
            "kx_rad": float(kx_rad),
            "ky_rad": float(ky_rad),
            "kx_mrad": float(kx_rad * 1e3),
            "ky_mrad": float(ky_rad * 1e3),
            "sign_verified": bool(kx_rad < 0 if x_offset_m < 0 else kx_rad > 0),
        }
