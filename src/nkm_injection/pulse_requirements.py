"""Half-sine peak-phase pulse estimates; time in s, field fractions dimensionless."""
import numpy as np


def peak_phase_field_fraction(delay_s, duration_s):
    """Half-sine field at delay from peak, zero outside its finite support."""
    if not np.isfinite(duration_s) or duration_s<=0:
        raise ValueError('Pulse duration must be finite and positive')
    dt=np.asarray(delay_s,float)
    if not np.isfinite(dt).all():raise ValueError('Nonfinite time delay')
    return np.where(np.abs(dt)<=duration_s/2,np.cos(np.pi*dt/duration_s),0.)


def maximum_peak_phase_duration(return_time_s, allowed_fraction):
    """Longest half-sine satisfying a fractional field limit on a return pass."""
    if not np.isfinite([return_time_s,allowed_fraction]).all() or return_time_s<=0 or not 0<=allowed_fraction<1:
        raise ValueError('Invalid return time or fractional allowance')
    return float(np.pi*return_time_s/np.arccos(allowed_fraction))


def thin_shell_diffusion_time(conductivity_s_per_m, radius_m, thickness_m):
    """Order-of-magnitude transverse-field time for a thin cylindrical shell.

    tau≈mu0*sigma*a*t/2. This is a hypothetical thin-shell estimate; it does not
    solve field diffusion in the unspecified NKM chamber or predict its leakage.
    """
    values=[conductivity_s_per_m,radius_m,thickness_m]
    if not np.isfinite(values).all() or min(values)<=0:raise ValueError('Positive finite shell parameters required')
    return float(4*np.pi*1e-7*conductivity_s_per_m*radius_m*thickness_m/2)
