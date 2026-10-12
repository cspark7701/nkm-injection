"""Independent adaptive reference for the stated paraxial equations (m, rad, T, eV).

This validates numerical integration of the model, not its approximation to the
full Lorentz equations. No finite-slice tracker routines are used by the ODE.
"""
import numpy as np
from scipy.integrate import solve_ivp
from .wire_field import FilamentNKMField, brho_T_m


def integrate_reference(config, coordinate, *, span_m=.45, rtol=2e-11, atol=2e-13, field=None):
    """Return six AT coordinates referred to s=0 after a pass over ±span_m.

    Input/output: x,y,ct in m; normalized momenta rad; delta dimensionless.
    Tolerances apply componentwise to those canonical units. delta is constant.
    """
    b = np.asarray(coordinate, dtype=float).copy()
    if b.shape != (6,) or not np.isfinite(b).all() or b[4] <= -1:
        raise ValueError('Expected finite (6,) coordinates with delta > -1')
    if not np.isfinite(span_m) or span_m <= 0 or not 0 < rtol < 1 or not 0 < atol < 1:
        raise ValueError('Invalid integration span or solver tolerances')
    field = FilamentNKMField() if field is None else field
    gain = config.kicker_polarity * config.field_scale / brho_T_m(config.energy_eV)
    offset = config.nkm_dx_m - config.closed_orbit_x_m

    def drift(u, length):
        xp, yp = u[1] / (1 + u[4]), u[3] / (1 + u[4])
        u[0] += length * xp; u[2] += length * yp
        u[5] += length * .5 * (xp*xp + yp*yp)

    drift(b, -span_m)

    def rhs(s, u):
        xp, yp = u[1] / (1 + u[4]), u[3] / (1 + u[4])
        bx, by, bs = (float(v[0]) for v in field(u[0] - offset, u[2], s))
        return [xp, gain * (by - yp*bs), yp, gain * (-bx + xp*bs), 0, .5*(xp*xp + yp*yp)]

    solution = solve_ivp(rhs, (-span_m, span_m), b, method='DOP853', rtol=rtol, atol=atol,
                         max_step=.01)
    if not solution.success or not np.isfinite(solution.y[:, -1]).all():
        raise RuntimeError('Adaptive reference integration failed')
    b = solution.y[:, -1].copy()
    drift(b, -span_m)
    b[1] += config.kick_offset_rad
    return b
