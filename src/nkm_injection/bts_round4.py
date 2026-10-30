"""Round-four BTS physics (consolidated R4-BTS tasks): steering layouts and
constrained phase-advance matching.

Units: positions in m; angles, kicks and canonical momenta in rad; K in m^-2;
phase advances in rad. AT coordinates (x, px, y, py, delta, ct). The BTS line
itself is never changed: layouts only choose which existing element boundaries
are read and which existing dipoles are trimmed.
"""
from __future__ import annotations

from copy import deepcopy

import numpy as np

from .bts_journal import QUADS, lattice_for
from .bts_round2 import nominal_observables
from . import bts_round3 as r3

# Steering layouts. ``monitors_after``: families whose exit boundary is read
# (in addition to the injection-septum entrance and the line end, weighted).
# ``knobs``: each knob is a group of existing dipoles trimmed together; within a
# group the kick of each magnet is proportional to its design bending angle, as
# for magnets powered in series.
LAYOUTS = {
    'full': {'monitors_after': list(QUADS), 'knobs': [['kext'], ['sept_in'], ['b1'], ['b2'], ['b3'], ['sept_ex']]},
    'reduced_monitors': {'monitors_after': ['q13', 'q23', 'q33'],
                         'knobs': [['kext'], ['sept_in'], ['b1'], ['b2'], ['b3'], ['sept_ex']]},
    'series_bends': {'monitors_after': list(QUADS), 'knobs': [['kext'], ['sept_in'], ['b1', 'b2', 'b3'], ['sept_ex']]},
    'reduced_series': {'monitors_after': ['q13', 'q23', 'q33'],
                       'knobs': [['kext'], ['sept_in'], ['b1', 'b2', 'b3'], ['sept_ex']]},
}


def layout_monitors(lattice, layout):
    """Monitor reference points: exits of the listed families, septum entrance, line end (last two weighted)."""
    names = [e.FamName for e in lattice]
    points = [i + 1 for i, n in enumerate(names) if n in layout['monitors_after']]
    return points + [names.index('sept_ex'), len(lattice)]


def knob_weights(lattice, layout):
    """Per knob, a list of (element index, kick per unit knob [1]); series groups scale with bending angle."""
    knobs = []
    for group in layout['knobs']:
        members = [(i, e) for i, e in enumerate(lattice) if e.FamName in group]
        if len(members) != len(group):
            raise ValueError(f'Knob group {group} not found once each in the line')
        ref = max(abs(e.BendingAngle) for _, e in members)
        knobs.append([(i, (e.BendingAngle / ref) if len(members) > 1 else 1.0) for i, e in members])
    return knobs


def apply_knobs(lattice, knobs, values):
    """Copy of ``lattice`` with horizontal dipole field trims; ``values`` [rad] are knob kicks."""
    line = deepcopy(lattice)
    for knob, value in zip(knobs, values):
        for i, w in knob:
            line[i].PolynomB = np.array(line[i].PolynomB, dtype=float)
            line[i].PolynomB[0] = line[i].PolynomB[0] - w * value / line[i].Length
    return line


def layout_response(lattice, layout, step=1e-5):
    """Horizontal monitor response [m/rad] to each knob of an error-free model line."""
    monitors, knobs = layout_monitors(lattice, layout), knob_weights(lattice, layout)
    base = r3.orbit_at(lattice, monitors)[:, 0]
    columns = []
    for k in range(len(knobs)):
        values = np.zeros(len(knobs))
        values[k] = step
        columns.append((r3.orbit_at(apply_knobs(lattice, knobs, values), monitors)[:, 0] - base) / step)
    return np.array(columns).T, monitors, knobs


def correct_with_layout(lattice, response, bpm_errors, settings=None):
    """Steer a static machine with a layout; same algorithm and settings as ``bts_round3.correct_trajectory``.

    Returns the steered line and the kick of every trimmed magnet [rad].
    """
    settings = {**r3.STEERING, **(settings or {})}
    matrix, monitors, knobs = response
    w = np.ones(len(monitors))
    w[-2:] = settings['end_weight']
    values = np.zeros(len(knobs))
    line = lattice
    for _ in range(settings['iterations']):
        reading = r3.orbit_at(line, monitors)[:, 0] + np.asarray(bpm_errors)[:len(monitors)]
        a = matrix * w[:, None]
        reg = settings['tikhonov'] * np.linalg.norm(a, 2)
        delta = np.linalg.lstsq(np.vstack([a, reg * np.eye(len(knobs))]),
                                np.concatenate([-w * reading, np.zeros(len(knobs))]), rcond=None)[0]
        values = np.clip(values + delta, -settings['kick_limit_rad'], settings['kick_limit_rad'])
        line = apply_knobs(lattice, knobs, values)
    kicks = np.array([w_ * v for knob, v in zip(knobs, values) for _, w_ in knob])
    return line, kicks


# ---------------------------------------------------------------------------
# Constrained phase-advance matching (R4-BTS-05)
# ---------------------------------------------------------------------------
def phase_residual(k, target, scales, mu_x):
    """Scaled exit residuals [1] plus the horizontal phase-advance residual [rad / 0.01 rad]."""
    lat = lattice_for(np.asarray(k, dtype=float))
    return np.append((nominal_observables(lat) - target) / scales, (r3.phase_advance(lat)[0] - mu_x) / 0.01)


def active_bounds(k, lower, upper, tol=1e-6):
    """Quadrupole families at a strength bound: list of (family, 'lower'|'upper')."""
    out = []
    for name, value, lo, hi in zip(QUADS, k, lower, upper):
        if value - lo < tol:
            out.append((name, 'lower'))
        elif hi - value < tol:
            out.append((name, 'upper'))
    return out
