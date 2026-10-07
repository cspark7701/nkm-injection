"""
NKM 1D Field Map Ingestion and Validation Module

Provides read-only loading, validation, interpolation, and symmetry analysis
for 1D magnetic field maps (e.g. nkm_field.xlsx, nkm_field_expanded.xlsx, By.txt).
"""

from pathlib import Path
from typing import Dict, Tuple, Optional, Any, Union
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from .units import KickMapMetadata, compute_rigidity, convert_coordinate, convert_kick_angle


import hashlib


from ._fieldmap_validation import (
    OutOfDomainError, broadcast_coordinates, check_bounds, validate_axis,
    validate_bounds, validate_values, validate_3d_map, trilinear,
)


class BaseFieldMap:
    """
    Abstract Base Class for 1D and 2D Magnetic Field & Kick Map Evaluators.
    
    Provides common domain bounds checking, file integrity verification (SHA-256),
    metadata handling, and symmetry evaluation interfaces.
    """
    def __init__(self,
                 x_min: float,
                 x_max: float,
                 y_min: Optional[float] = None,
                 y_max: Optional[float] = None,
                 allow_extrapolation: bool = False,
                 metadata: Optional[KickMapMetadata] = None,
                 filepath: Optional[Union[str, Path]] = None):
        validate_bounds((x_min, x_max), "x")
        if y_min is not None or y_max is not None:
            validate_bounds((y_min, y_max), "y")
        self.x_min = float(x_min)
        self.x_max = float(x_max)
        self.y_min = float(y_min) if y_min is not None else None
        self.y_max = float(y_max) if y_max is not None else None
        self.allow_extrapolation = allow_extrapolation
        self.metadata = metadata
        self.filepath = Path(filepath) if filepath else None

    def check_domain_bounds(self,
                            x: Union[float, np.ndarray],
                            y: Optional[Union[float, np.ndarray]] = None) -> None:
        """
        Validate whether (x, y) coordinates fall within tabulated map domain bounds.
        
        Raises OutOfDomainError if points fall outside domain bounds and allow_extrapolation is False.
        """
        check_bounds(x, (self.x_min, self.x_max), "x", self.allow_extrapolation)
        if y is not None and self.y_min is not None:
            check_bounds(y, (self.y_min, self.y_max), "y", self.allow_extrapolation)

    def compute_file_hash(self, filepath: Optional[Union[str, Path]] = None, algorithm: str = "sha256") -> str:
        """
        Compute cryptographic hash (default SHA-256) of the map file.
        """
        target_path = Path(filepath) if filepath else self.filepath
        if not target_path or not target_path.is_file():
            raise FileNotFoundError(f"Map file path not found: {target_path}")

        hasher = hashlib.new(algorithm)
        with open(target_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def verify_file_hash(self, expected_hash: str, algorithm: str = "sha256") -> bool:
        """
        Verify that map file hash matches an expected hash checksum string.
        """
        computed = self.compute_file_hash(algorithm=algorithm)
        return computed.lower() == expected_hash.lower()

    @property
    def domain_bounds(self) -> Dict[str, Tuple[float, float]]:
        """Return dict of domain bounds for x (and y if applicable)."""
        bounds = {"x": (self.x_min, self.x_max)}
        if self.y_min is not None and self.y_max is not None:
            bounds["y"] = (self.y_min, self.y_max)
        return bounds


def integrate_longitudinal_field(z: np.ndarray,
                                 by: np.ndarray,
                                 method: str = "simpson") -> float:
    """
    Perform direct 1D numerical quadrature along longitudinal axis z (in meters)
    to calculate integrated magnetic field I_y = integral B_y(z) dz in T*m.
    
    Args:
        z: Longitudinal position array in meters (must be sorted).
        by: Magnetic field component array B_y(z) in Tesla.
        method: Numerical integration method ('simpson' or 'trapezoid').
        
    Returns:
        Integrated field I_y in T*m.
    """
    z_arr = validate_axis(z, "z (m)")
    by_arr = validate_values(by, z_arr.shape, "By (T)")

    if method == "simpson":
        try:
            from scipy.integrate import simpson
            int_val = float(simpson(y=by_arr, x=z_arr))
        except ImportError:
            from scipy.integrate import simps
            int_val = float(simps(y=by_arr, x=z_arr))
    elif method == "trapezoid":
        try:
            from scipy.integrate import trapezoid
            int_val = float(trapezoid(y=by_arr, x=z_arr))
        except ImportError:
            int_val = float(np.trapz(y=by_arr, x=z_arr))
    else:
        raise ValueError(f"Unsupported numerical integration method: '{method}'")

    return int_val


def load_1d_fieldmap(filepath: Union[str, Path],
                    x_col: str = "x",
                    by_col: str = "By") -> Tuple[np.ndarray, np.ndarray]:
    """
    Load a 1D field map from an Excel or text file in read-only mode.
    
    Args:
        filepath: Path to spreadsheet (.xlsx) or CSV/text (.txt) file.
        x_col: Name or index of horizontal position column (m).
        by_col: Name or index of vertical magnetic field column (T).
        
    Returns:
        Tuple of (x_array, by_array) in meters and Tesla.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Field map file not found: {path}")
        
    ext = path.suffix.lower()
    if ext in ('.xlsx', '.xls'):
        df = pd.read_excel(path)
        if x_col in df.columns and by_col in df.columns:
            x = df[x_col].values.astype(float)
            by = df[by_col].values.astype(float)
        else:
            x = df.iloc[:, 0].values.astype(float)
            by = df.iloc[:, 1].values.astype(float)
    elif ext in ('.txt', '.csv'):
        df = pd.read_csv(path, sep=r"[,\s]+", header=None, engine="python")
        if df.shape[1] != 2:
            raise ValueError("Text field map must contain exactly two columns: x (m), By (T)")
        x = df.iloc[:, 0].values.astype(float)
        by = df.iloc[:, 1].values.astype(float)
    else:
        raise ValueError(f"Unsupported field map extension: {ext}")
        
    # Sort by x coordinate
    sort_idx = np.argsort(x)
    x = validate_axis(x[sort_idx], "x (m)")
    return x, validate_values(by[sort_idx], x.shape, "By (T)")


def validate_1d_fieldmap(x: np.ndarray, by: np.ndarray) -> Dict[str, Any]:
    """
    Perform rigorous numerical and symmetry checks on a 1D field map.
    
    Returns:
        Dictionary of validation metrics.
    """
    x = np.asarray(x, dtype=float)
    by = np.asarray(by, dtype=float)
    if x.ndim != 1 or x.size < 2 or by.shape != x.shape:
        raise ValueError("x and By must be equal-length 1-D arrays with at least two nodes")
    is_finite_x = bool(np.all(np.isfinite(x)))
    is_finite_by = bool(np.all(np.isfinite(by)))
    
    # Check duplicates
    has_duplicates = bool(len(x) != len(np.unique(x)))
    
    # Check monotonicity
    dx = np.diff(x)
    is_strictly_monotonic = bool(np.all(dx > 0))
    
    # Range
    x_min, x_max = float(np.min(x)), float(np.max(x))
    by_min, by_max = float(np.min(by)), float(np.max(by))
    peak_by = float(np.max(np.abs(by)))
    
    # Symmetry metric (odd or even symmetry check around x=0)
    if is_finite_x and is_finite_by and is_strictly_monotonic and x_min < 0 and x_max > 0:
        pos_mask = (x > 0) & (x <= min(abs(x_min), abs(x_max)))
        x_pos = x[pos_mask]
        by_pos = by[pos_mask]
        
        if x_pos.size == 0:
            x_pos = np.array([min(abs(x_min), abs(x_max))])
            by_pos = np.interp(x_pos, x, by)
        by_neg_interp = np.interp(-x_pos, x, by)
        odd_sym_residual = float(np.max(np.abs(by_pos + by_neg_interp)))
        even_sym_residual = float(np.max(np.abs(by_pos - by_neg_interp)))
    else:
        odd_sym_residual = None
        even_sym_residual = None
        
    all_passed = is_finite_x and is_finite_by and is_strictly_monotonic and not has_duplicates
    
    return {
        "valid": all_passed,
        "n_samples": len(x),
        "x_range_m": [x_min, x_max],
        "by_range_T": [by_min, by_max],
        "peak_by_T": peak_by,
        "is_strictly_monotonic": is_strictly_monotonic,
        "has_duplicates": has_duplicates,
        "odd_symmetry_residual_T": odd_sym_residual,
        "even_symmetry_residual_T": even_sym_residual,
    }


class NKMFieldMap1D(BaseFieldMap):
    """
    1D NKM Field Map Interpolator with strict domain checking, explicit metadata, and integrated kick utilities.
    """
    def __init__(self, x: np.ndarray, by: np.ndarray,
                 allow_extrapolation: bool = False,
                 metadata: Optional[KickMapMetadata] = None,
                 filepath: Optional[Union[str, Path]] = None):
        x = validate_axis(x, "x (m)")
        by = validate_values(by, x.shape, "By (T)")
        val = validate_1d_fieldmap(x, by)
        if not val["valid"]:
            raise ValueError(f"Invalid 1D field map data: {val}")
            
        meta = metadata or KickMapMetadata(
            coordinate_unit="m",
            value_type="field",
            value_unit="T",
            beam_energy_eV=4.0e9
        )

        super().__init__(
            x_min=float(x.min()),
            x_max=float(x.max()),
            allow_extrapolation=allow_extrapolation,
            metadata=meta,
            filepath=filepath
        )
        
        self.x = x
        self.by = by
        
        fill_val = "extrapolate" if allow_extrapolation else np.nan
        self._interp_linear = interp1d(x, by, kind='linear', bounds_error=False, fill_value=fill_val)
        self._interp_cubic = (interp1d(x, by, kind='cubic', bounds_error=False, fill_value=fill_val)
                              if x.size >= 4 else None)

    def evaluate(self, x_eval: Union[float, np.ndarray], method: str = 'linear') -> Union[float, np.ndarray]:
        """
        Evaluate interpolated field B_y at x_eval.
        
        Raises OutOfDomainError if points are outside bounds and allow_extrapolation is False.
        """
        self.check_domain_bounds(x_eval)
            
        if method not in ("linear", "cubic"):
            raise ValueError("Interpolation method must be 'linear' or 'cubic'")
        if method == "cubic" and self._interp_cubic is None:
            raise ValueError("Cubic interpolation requires at least four nodes")
        interp_fn = self._interp_cubic if method == 'cubic' else self._interp_linear
        res = interp_fn(x_eval)
        
        if np.ndim(x_eval) == 0:
            return float(res)
        return res

    def compute_integrated_kick(self, x_pos: float, length_m: float = 0.525, energy_GeV: float = 4.0) -> float:
        """
        Calculate horizontal kick angle Delta x' in mrad for a particle at position x_pos.
        
        Delta x' = (q / p0) * B_y(x) * L
        """
        by_val = self.evaluate(x_pos)
        energy_eV = energy_GeV * 1e9
        charge_C = self.metadata.particle_charge_C if self.metadata else -1.602176634e-19
        brho = compute_rigidity(energy_eV, charge_C)
        charge_sign = float(np.sign(charge_C))
        kick_rad = charge_sign * (by_val * length_m) / brho
        return float(kick_rad * 1e3)  # mrad

    def fit_polynomial(self, degree: int = 5) -> Tuple[np.ndarray, float]:
        """
        Fit a polynomial of given degree to B_y(x) and return coefficients and max residual.
        """
        coeffs = np.polyfit(self.x, self.by, degree)
        fit_vals = np.polyval(coeffs, self.x)
        max_residual = float(np.max(np.abs(self.by - fit_vals)))
        return coeffs, max_residual


# ---------------------------------------------------------------------------
# 3D Vectorized Field Map Interpolation
# ---------------------------------------------------------------------------

def interpolate_3d_field_vectorized(
    field_map: np.ndarray,
    x_mm: Union[float, np.ndarray],
    y_mm: Union[float, np.ndarray],
    z_mm: Union[float, np.ndarray],
    x_range_mm: Tuple[float, float] = (-50.0, 50.0),
    y_range_mm: Tuple[float, float] = (-50.0, 50.0),
    z_range_mm: Tuple[float, float] = (-300.0, 300.0),
    boundary_policy: str = "raise",
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Vectorized trilinear interpolation of 3D magnetic field map (Bx, By, Bz) in Tesla.

    Parameters
    ----------
    field_map : np.ndarray
        Array of shape (nx, ny, nz, 3) containing [Bx, By, Bz] in Tesla.
    x_mm, y_mm, z_mm : float or np.ndarray
        Coordinates in millimeters.
    x_range_mm, y_range_mm, z_range_mm : tuple of float
        Bounding box of grid in mm (default [-50, 50], [-50, 50], [-300, 300]).

    Returns
    -------
    Bx, By, Bz : float or np.ndarray
        Interpolated fields in T with NumPy broadcast coordinate shape.
        Outside queries raise by default; boundary_policy explicitly permits
        linear extrapolation or clipping. NaN/Inf always raise ValueError.
    """
    values, ranges = validate_3d_map(field_map, (x_range_mm, y_range_mm, z_range_mm))
    return trilinear(values, (x_mm, y_mm, z_mm), ranges, boundary_policy)


class NKMFieldMap3D(BaseFieldMap):
    """
    3D Field Map evaluator with vectorized trilinear interpolation conforming to FieldMap3DProtocol.
    """
    def __init__(self,
                 field_map: np.ndarray,
                 x_range_m: Tuple[float, float] = (-0.050, 0.050),
                 y_range_m: Tuple[float, float] = (-0.050, 0.050),
                 z_range_m: Tuple[float, float] = (-0.300, 0.300),
                 allow_extrapolation: bool = False,
                 metadata: Optional[KickMapMetadata] = None,
                 filepath: Optional[Union[str, Path]] = None):
        field_map, ranges = validate_3d_map(field_map, (x_range_m, y_range_m, z_range_m))
        x_range_m, y_range_m, z_range_m = ranges
        super().__init__(
            x_min=x_range_m[0],
            x_max=x_range_m[1],
            y_min=y_range_m[0],
            y_max=y_range_m[1],
            allow_extrapolation=allow_extrapolation,
            metadata=metadata,
            filepath=filepath
        )
        self.field_map = field_map
        self.x_range_m = x_range_m
        self.y_range_m = y_range_m
        self.z_range_m = z_range_m
        self.z_min = z_range_m[0]
        self.z_max = z_range_m[1]

    def evaluate(self, x_m: Union[float, np.ndarray],
                 y_m: Union[float, np.ndarray],
                 z_m: Union[float, np.ndarray]) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray], Union[float, np.ndarray]]:
        """
        Evaluate (Bx, By, Bz) in Tesla at (x_m, y_m, z_m) in meters.
        """
        return trilinear(
            self.field_map, (x_m, y_m, z_m),
            (self.x_range_m, self.y_range_m, self.z_range_m),
            "extrapolate" if self.allow_extrapolation else "raise",
        )

    @property
    def domain_bounds(self):
        """Closed x, y and z domain bounds in meters."""
        return {**super().domain_bounds, "z": (self.z_min, self.z_max)}

    def __call__(self, x: np.ndarray, y: np.ndarray, z: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """Conforms to FieldMap3DProtocol returning (By, Bx) in Tesla for transverse coords (x, y) at slice z."""
        bx, by, _ = self.evaluate(x, y, z)
        return by, bx

