"""NumPy-only map contracts, also copied into pyAT by the extension installer.

Axes and bounds use the caller's coordinate units; field values are in T.
This module has no project dependencies so the installed pyAT copy is standalone.
"""
import numpy as np


class OutOfDomainError(ValueError):
    """A finite query lies outside a tabulated map's closed domain."""


def finite_array(values, name):
    """Convert numerical values to float and reject NaN/Inf."""
    array = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def validate_axis(values, name):
    """Require a finite, strictly increasing 1-D axis with at least two nodes."""
    axis = finite_array(values, name)
    if axis.ndim != 1 or axis.size < 2:
        raise ValueError(f"{name} must be a 1-D axis with at least two nodes")
    if not np.all(np.diff(axis) > 0):
        raise ValueError(f"{name} must be strictly increasing without duplicates")
    return axis


def validate_values(values, shape, name):
    """Require finite map values with the exact grid/component shape."""
    array = finite_array(values, name)
    if array.shape != tuple(shape):
        raise ValueError(f"{name} must have shape {tuple(shape)}, got {array.shape}")
    return array


def validate_bounds(bounds, name):
    """Require two finite, increasing limits in the caller's units."""
    array = finite_array(bounds, name)
    if array.shape != (2,) or array[0] >= array[1]:
        raise ValueError(f"{name} must contain two strictly increasing limits")
    return tuple(array)


def broadcast_coordinates(*coordinates):
    """Return finite coordinates with a common NumPy broadcast shape."""
    arrays = [finite_array(value, name) for name, value in coordinates]
    try:
        return np.broadcast_arrays(*arrays)
    except ValueError as error:
        raise ValueError("Coordinate shapes must be broadcast-compatible") from error


def check_bounds(values, bounds, name, allow_extrapolation=False):
    """Reject nonfinite queries even when extrapolation is explicitly allowed."""
    array = finite_array(values, name)
    if not allow_extrapolation and np.any((array < bounds[0]) | (array > bounds[1])):
        raise OutOfDomainError(f"{name} values outside [{bounds[0]}, {bounds[1]}]")


def validate_3d_map(values, ranges):
    """Validate (nx, ny, nz, 3) fields in T on uniform coordinate ranges."""
    array = finite_array(values, "field_map")
    if array.ndim != 4 or array.shape[-1] != 3 or min(array.shape[:3]) < 2:
        raise ValueError("field_map must have shape (nx, ny, nz, 3), each axis >= 2")
    bounds = tuple(validate_bounds(value, name) for name, value in zip(("x", "y", "z"), ranges))
    return array, bounds


def trilinear(field_map, coordinates, ranges, boundary_policy="raise"):
    """Interpolate a validated uniform grid in T; coordinates share grid units.

    Policies: raise (default), extrapolate (linear edge-cell continuation),
    clip (explicit nearest-boundary clamping). Results have broadcast query shape.
    """
    if boundary_policy not in ("raise", "extrapolate", "clip"):
        raise ValueError("boundary_policy must be 'raise', 'extrapolate' or 'clip'")
    arrays = broadcast_coordinates(*zip(("x", "y", "z"), coordinates))
    indices, weights = [], []
    for name, array, bounds, size in zip(("x", "y", "z"), arrays, ranges, field_map.shape[:3]):
        check_bounds(array, bounds, name, boundary_policy != "raise")
        if boundary_policy == "clip":
            array = np.clip(array, *bounds)
        fraction = (array - bounds[0]) / (bounds[1] - bounds[0]) * (size - 1)
        # Choose an edge cell for boundary nodes and explicit extrapolation.
        lower = np.floor(np.clip(fraction, 0, size - 2)).astype(int)
        indices.append(lower)
        weights.append((fraction - lower)[..., None])
    result = np.zeros(arrays[0].shape + (3,))
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                weight = ((weights[0] if i else 1 - weights[0]) *
                          (weights[1] if j else 1 - weights[1]) *
                          (weights[2] if k else 1 - weights[2]))
                result += weight * field_map[indices[0] + i, indices[1] + j, indices[2] + k]
    return tuple(float(result[i]) if result.ndim == 1 else result[..., i] for i in range(3))
