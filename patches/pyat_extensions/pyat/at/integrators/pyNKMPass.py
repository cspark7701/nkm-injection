import numpy as np

try:
    from ._nkm_fieldmap import OutOfDomainError, validate_3d_map, trilinear
except ModuleNotFoundError as error:
    if error.name != __package__ + "._nkm_fieldmap":
        raise
    # Repository use before installation; installer supplies the standalone copy.
    try:
        from nkm_injection._fieldmap_validation import OutOfDomainError, validate_3d_map, trilinear
    except ModuleNotFoundError as error:
        if error.name != "nkm_injection":
            raise
        from src.nkm_injection._fieldmap_validation import OutOfDomainError, validate_3d_map, trilinear


try:
    from ..constants import clight
except (ImportError, ValueError):
    try:
        from at.constants import clight
    except (ImportError, ValueError):
        clight = 299792458.0

#*********************************Pass Method for Nonlinear Kicker Magnet
def trackFunction(r_in, elem=None):
    """
    Pure Python vectorized tracking function for the nonlinear kicker magnet.
    
    Parameters:
        r_in: (6, num_particles) NumPy array containing 6D phase space coordinates.
        elem: NonlinearKicker element with field map.
    
    Returns:
        Updated 6D phase space coordinates.
    """
    # Extract properties
    Length = elem.Length
    Nslice = elem.Nslice
    Energy = elem.Energy
    FieldMap = elem.FieldMap
    
    if FieldMap is None:
        raise ValueError("FieldMap is required for nkmpassmethod.")

    FieldMap, ranges = validate_3d_map(
        FieldMap, ((-50.0, 50.0), (-50.0, 50.0), (-300.0, 300.0)))
    # AT marks lost particles with NaN in x; do not query their coordinates.
    live = ~np.isnan(r_in[0])
    if not np.all(live):
        if np.any(live):
            r_in[:, live] = trackFunction(r_in[:, live].copy(), elem)
        return r_in

    Brho = - 1e9 * Energy / clight    # Brho in T*m (negative for electrons in AT)

    num_particles = r_in.shape[1]
    if num_particles == 0:
        return r_in

    dz = Length / Nslice  # Slice thickness

    # Vectorized tracking loop over longitudinal slices
    for j in range(Nslice):
        x_mm = r_in[0, :] * 1e3
        y_mm = r_in[2, :] * 1e3
        z_mm = r_in[5, :] * 1e3 - Length * 1e3 * 0.5
        
        # Vectorized trilinear field interpolation
        Bx, By, Bz = trilinear(FieldMap, (x_mm, y_mm, z_mm), ranges)

        # Compute kicks (AT conventions: Delta px = - By * dz / Brho)
        delta_p_x = - By * dz / Brho
        delta_p_y = 0.0

        # Update transverse momenta
        r_in[1, :] += delta_p_x
        r_in[3, :] += delta_p_y

        # Drift motion update (x, y) due to slice thickness
        r_in[0, :] += r_in[1, :] * dz
        r_in[2, :] += r_in[3, :] * dz

        # Longitudinal motion update
        delta_E = (r_in[1, :] * By) * dz / Brho
        r_in[4, :] += delta_E
        r_in[5, :] += dz * (1.0 + r_in[4, :]) / np.sqrt(1.0 + 2.0 * r_in[4, :])

    r_in[5, :] -= Length
   
    return r_in


def interpolate_field_vectorized(FieldMap, x, y, z, boundary_policy="raise"):
    """Return (Bx, By, Bz) in T for broadcast coordinates in mm.

    Fixed uniform bounds are x/y=[-50,50], z=[-300,300] mm.
    Outside queries raise by default. Explicit policies 'extrapolate' and 'clip'
    permit edge-cell continuation and nearest-boundary clamping respectively.
    """
    values, ranges = validate_3d_map(
        FieldMap, ((-50.0, 50.0), (-50.0, 50.0), (-300.0, 300.0)))
    return trilinear(values, (x, y, z), ranges, boundary_policy)


def interpolate_field(FieldMap, x, y, z):
    """Legacy wrapper for field interpolation."""
    return interpolate_field_vectorized(FieldMap, x, y, z)
