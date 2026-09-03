import numpy as np

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
        Bx, By, Bz = interpolate_field_vectorized(FieldMap, x_mm, y_mm, z_mm)

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


def interpolate_field_vectorized(FieldMap, x, y, z):
    """
    Vectorized trilinear interpolation of 3D magnetic field map (Bx, By, Bz) in Tesla.
    
    Parameters:
        FieldMap: NumPy array of shape (nx, ny, nz, 3).
        x: X coordinates in mm (scalar or 1D array).
        y: Y coordinates in mm (scalar or 1D array).
        z: Z coordinates in mm (scalar or 1D array).
    
    Returns:
        Tuple of (Bx, By, Bz) matching input coordinate shape.
    """
    nx, ny, nz, _ = FieldMap.shape
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    z_arr = np.asarray(z, dtype=float)

    # Grid bounding box in mm
    x_min, x_max = -50.0, 50.0
    y_min, y_max = -50.0, 50.0
    z_min, z_max = -300.0, 300.0

    # Normalized float index coordinates
    ux = np.clip((x_arr - x_min) / (x_max - x_min) * (nx - 1), 0.0, nx - 1.0)
    uy = np.clip((y_arr - y_min) / (y_max - y_min) * (ny - 1), 0.0, ny - 1.0)
    uz = np.clip((z_arr - z_min) / (z_max - z_min) * (nz - 1), 0.0, nz - 1.0)

    # Cell lower corner indices
    i0 = np.floor(ux).astype(int)
    j0 = np.floor(uy).astype(int)
    k0 = np.floor(uz).astype(int)

    # Cell upper corner indices
    i1 = np.minimum(i0 + 1, nx - 1)
    j1 = np.minimum(j0 + 1, ny - 1)
    k1 = np.minimum(k0 + 1, nz - 1)

    # Fractional weights
    wx = ux - i0
    wy = uy - j0
    wz = uz - k0

    if wx.ndim > 0:
        wx = wx[..., np.newaxis]
        wy = wy[..., np.newaxis]
        wz = wz[..., np.newaxis]

    # Trilinear interpolation weights
    c000 = (1.0 - wx) * (1.0 - wy) * (1.0 - wz)
    c100 = wx * (1.0 - wy) * (1.0 - wz)
    c010 = (1.0 - wx) * wy * (1.0 - wz)
    c110 = wx * wy * (1.0 - wz)
    c001 = (1.0 - wx) * (1.0 - wy) * wz
    c101 = wx * (1.0 - wy) * wz
    c011 = (1.0 - wx) * wy * wz
    c111 = wx * wy * wz

    b_interp = (
        c000 * FieldMap[i0, j0, k0]
        + c100 * FieldMap[i1, j0, k0]
        + c010 * FieldMap[i0, j1, k0]
        + c110 * FieldMap[i1, j1, k0]
        + c001 * FieldMap[i0, j0, k1]
        + c101 * FieldMap[i1, j0, k1]
        + c011 * FieldMap[i0, j1, k1]
        + c111 * FieldMap[i1, j1, k1]
    )

    if b_interp.ndim == 1:
        return b_interp[0], b_interp[1], b_interp[2]
    return b_interp[..., 0], b_interp[..., 1], b_interp[..., 2]


def interpolate_field(FieldMap, x, y, z):
    """Legacy wrapper for field interpolation."""
    return interpolate_field_vectorized(FieldMap, x, y, z)
