import numpy as np
from ..constants import clight

#*********************************Pass Method for Nonlinear Kicker Magnet
def trackFunction(r_in, elem=None):
    """
    Pure Python tracking function for the nonlinear kicker magnet.
    
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

    Brho = - 1e9 * Energy / clight    # Brho

    num_particles = r_in.shape[1]  # Number of particles
    dz = Length / Nslice  # Slice thickness

    for i in range(num_particles):
        for j in range(Nslice):
            x_mm = r_in[0, i] * 1e3              # convert to mm
            y_mm = r_in[2, i] * 1e3              # convert to mm
            z_mm = r_in[5, i] * 1e3 - Length * 1e3 / 2 # convert relative z to mm and shift to -l/2
            
            # Interpolate B field in Tesla at (x, y, z)
            Bx, By, Bz = interpolate_field(FieldMap, x_mm, y_mm, z_mm)

            # Compute kicks (AT conventions)
            delta_p_x = - By * dz / Brho
            delta_p_y = 0.0
            #delta_p_y =   Bx * dz / Brho
            #delta_delta = 0  # No energy gain from purely magnetic kicker

            # Update momenta and energy deviation
            r_in[1, i] += delta_p_x
            r_in[3, i] += delta_p_y
            #r_in[5, i] += delta_delta  # no energy change for magnetic fields

            # Drift motion update (x, y) due to finite element length
            r_in[0, i] += r_in[1, i] * dz  # x += px * dz
            r_in[2, i] += r_in[3, i] * dz  # y += py * dz
            #r_in[4, i] += dz               # Step along the relative z-axis

            # Longitudinal motion update
            tau = r_in[4, i]
            delta = r_in[5, i]

            delta_E = (r_in[1, i] * By - r_in[3, i] * Bx) * dz / Brho 
            delta_E = (r_in[1, i] * By) * dz / Brho
            r_in[4, i] += delta_E

            r_in[5, i] += dz * (1 + r_in[4, i]) / np.sqrt(1 + 2 * r_in[4, i])

    r_in[5,:] -= Length
   
    return r_in

def interpolate_field(FieldMap, x, y, z):
    """
    Interpolates the 3D field map at a given (x, y, z).
    
    Parameters:
        FieldMap: Precomputed field map stored in NumPy format.
        x: X position of the particle.
        y: Y position of the particle.
        z: Z position of the particle.
    
    Returns:
        Interpolated (Bx, By, Bz) field values at (x, y, z).
    """
    nx, ny, nz, _ = FieldMap.shape
    x_range = np.linspace(-50, 50, nx)
    y_range = np.linspace(-50, 50, ny)
    z_range = np.linspace(-300, 300, nz)
    
    x_idx = np.searchsorted(x_range, x) - 1
    y_idx = np.searchsorted(y_range, y) - 1
    z_idx = np.searchsorted(z_range, z) - 1
    
    return FieldMap[x_idx, y_idx, z_idx, 0], FieldMap[x_idx, y_idx, z_idx, 1], FieldMap[x_idx, y_idx, z_idx, 2]
