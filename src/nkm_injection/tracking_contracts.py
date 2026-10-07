"""Shared tracking boundaries: positions/ct in m, momenta in rad, delta unitless."""
from dataclasses import dataclass
from numbers import Real

import numpy as np

from .units import ELECTRON_CHARGE_C, compute_rigidity


def positive_count(value, name):
    """Require an actual positive Python/NumPy integer, excluding booleans."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value <= 0:
        raise ValueError(f'{name} must be a positive integer')
    return int(value)


def finite_scalar(value, name, *, minimum=None, nonzero=False):
    """Validate a real finite scalar in the units identified by its name."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real) or not np.isfinite(value):
        raise ValueError(f'{name} must be a finite real scalar')
    value = float(value)
    if not np.isfinite(value):
        raise ValueError(f'{name} must be finite in float64')
    if minimum is not None and value < minimum:
        raise ValueError(f'{name} must be >= {minimum}')
    if nonzero and value == 0:
        raise ValueError(f'{name} must be nonzero')
    return value


@dataclass(frozen=True)
class TrackingParameters:
    """Validated thick tracking settings; energy in GeV, charge in C, length in m.

    Energy must be finite and positive. Either charge sign is supported; charge
    must be finite/nonzero. Length and dimensionless field scale may be zero.
    """
    length_m: float = 0.525
    n_slices: int = 40
    energy_GeV: float = 4.0
    particle_charge_C: float = ELECTRON_CHARGE_C
    scale_factor: float = 1.0

    def __post_init__(self):
        object.__setattr__(self, 'n_slices', positive_count(self.n_slices, 'n_slices'))
        for name in ('length_m', 'scale_factor'):
            object.__setattr__(self, name, finite_scalar(getattr(self, name), name, minimum=0))
        object.__setattr__(self, 'energy_GeV', finite_scalar(self.energy_GeV, 'energy_GeV', minimum=0, nonzero=True))
        object.__setattr__(self, 'particle_charge_C', finite_scalar(self.particle_charge_C, 'particle_charge_C', nonzero=True))
        if not np.isfinite(self.energy_eV) or not np.isfinite(self.brho) or self.brho <= 0:
            raise ValueError('energy/charge must produce finite positive rigidity in T m')

    @property
    def energy_eV(self):
        return self.energy_GeV * 1e9

    @property
    def brho(self):
        return compute_rigidity(self.energy_eV, self.particle_charge_C)

    @property
    def dz(self):
        return self.length_m / self.n_slices


def validate_particle_array(beam, *, copy=False):
    """Return float64 (6,N) coordinates and an active-column mask.

    Empty beams are supported. Lost columns are all-NaN or AT's NaN-x marker
    with five finite remaining coordinates. Other partial NaNs and any Inf are
    invalid. Lost coordinates and original column order are preserved. Integer
    inputs are converted; complex, boolean, object and nonnumeric arrays fail.
    ``copy=True`` returns independent, writable Fortran-order storage.
    """
    array = np.asarray(beam)
    if array.ndim != 2 or array.shape[0] != 6:
        raise ValueError(f'beam must have shape (6, N), got {array.shape}')
    if array.dtype.kind not in 'fiu':
        raise TypeError('beam coordinates must be real numeric values')
    array = np.array(array, dtype=np.float64, order='F', copy=True) if copy else np.asarray(array, dtype=np.float64)
    nan = np.isnan(array)
    lost = nan.all(axis=0) | (nan[0] & np.isfinite(array[1:]).all(axis=0))
    active = np.isfinite(array).all(axis=0)
    invalid = ~(active | lost)
    if invalid.any():
        raise ValueError(f'beam has Inf or invalid partial NaN columns at indices {np.flatnonzero(invalid).tolist()}')
    return array, active


def require_finite_active(beam, active):
    """Reject numerical corruption of active coordinates, rather than recording loss."""
    if not np.isfinite(beam[:, active]).all():
        raise ValueError('tracking generated nonfinite active coordinates')


def drift(beam, active, length_m):
    """Advance transverse coordinates in place by a drift length in m."""
    beam[0, active] += beam[1, active] * length_m
    beam[2, active] += beam[3, active] * length_m
    require_finite_active(beam, active)


def finite_components(values, shape, name):
    """Broadcast two finite real field/kick components to active particle shape."""
    if not isinstance(values, (tuple, list)) or len(values) != 2:
        raise ValueError(f'{name} must return two components')
    result = []
    for value in values:
        array = np.asarray(value)
        if array.dtype.kind not in 'fiu':
            raise TypeError(f'{name} components must be real numeric values')
        try:
            array = np.broadcast_to(np.asarray(array, dtype=float), shape)
        except ValueError as exc:
            raise ValueError(f'{name} components must broadcast to {shape}') from exc
        if not np.isfinite(array).all():
            raise ValueError(f'{name} components must be finite')
        result.append(array)
    return tuple(result)
