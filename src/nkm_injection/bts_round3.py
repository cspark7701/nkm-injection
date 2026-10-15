"""Round-three BTS physics (Reviewer 2): boundary-fixed clearances, element-wise
apertures, trajectory correction, jitter transfer and analytic loss tails.

Units: positions, apertures and clearances in m; angles and canonical momenta
in rad; K in m^-2; phase advances in rad. AT coordinates (x, px, y, py, delta, ct).
"""
from __future__ import annotations

import numpy as np

from .bts_journal import JournalBeam
from .optics import DEFAULT_BTS_ENTRANCE_TWISS

# Exit target (m4) of the configured line; identical to the injected beam of the
# companion NKM study (study configuration ``injected_beam``).
EXIT_TWISS = {'beta_x': 2.336495, 'alpha_x': -0.016335, 'beta_y': 4.256241,
              'alpha_y': 0.017772, 'disp_x': 0.080868, 'disp_px': 0.047472}


def boundary_sigma(beta, emittance, dispersion=0.0, sigma_delta=0.0):
    """Projected rms size [m] from Twiss beta [m], emittance [m rad] and dispersion [m]."""
    if beta <= 0 or emittance <= 0 or sigma_delta < 0:
        raise ValueError('Positive beta and emittance, non-negative spread required')
    return float(np.sqrt(emittance * beta + (dispersion * sigma_delta) ** 2))


def boundary_clearances(halfwidth=0.01935, beam=None):
    """Nominal five-sigma clearances [m] at the entrance and exit stations.

    Both stations sit where the optics are fixed by boundary data: the entrance
    Twiss/dispersion are inputs and the exit is matched to its target. A centred
    nominal beam therefore has clearance ``halfwidth - n sigma`` there for every
    quadrupole setting that satisfies the exit match. Returns
    ``{'entrance': (cx, cy), 'exit': (cx, cy)}``.
    """
    beam = beam or JournalBeam()
    tw = DEFAULT_BTS_ENTRANCE_TWISS
    n = beam.coverage_sigma
    entrance = (halfwidth - n * boundary_sigma(tw.beta_x, beam.emit_x_m_rad, tw.disp_x, beam.sigma_delta),
                halfwidth - n * boundary_sigma(tw.beta_y, beam.emit_y_m_rad, tw.disp_y, beam.sigma_delta))
    ex = EXIT_TWISS
    exit_ = (halfwidth - n * boundary_sigma(ex['beta_x'], beam.emit_x_m_rad, ex['disp_x'], beam.sigma_delta),
             halfwidth - n * boundary_sigma(ex['beta_y'], beam.emit_y_m_rad, 0.0, beam.sigma_delta))
    return {'entrance': entrance, 'exit': exit_}
