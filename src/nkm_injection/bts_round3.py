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


# ---------------------------------------------------------------------------
# R2B-01: element-wise aperture model
# ---------------------------------------------------------------------------
from copy import deepcopy  # noqa: E402

import at  # noqa: E402
from scipy.stats import norm  # noqa: E402

from .bts_journal import QUADS, apply_static, lattice_for  # noqa: E402

BENDS = ('kext', 'sept_in', 'b1', 'b2', 'b3', 'sept_ex')

# Declared parametric aperture model [m]. Only the exit-septum blade position is
# derived from a source (the companion NKM geometry: stored-beam edge -16 mm,
# 2 mm blade, injected beam at -19.478 mm, i.e. 1.478 mm from the blade's outer
# face, blade on the +x side of the injected beam). Everything else is an
# assumption to be swept, not a hardware specification.
APERTURE_MODEL = {
    'pipe_radius': 0.01935,          # drifts: round pipe equal to the assumed bore
    'quad_bore_radius': 0.01935,     # quadrupoles: round bore (assumed, as for B_pole)
    'kicker_half': (0.015, 0.010),   # extraction kicker: rectangular x, y
    'dipole_half': (0.030, 0.010),   # b1-b3: curved chamber, x halfwidth, y half-gap
    'septum_in_half': (0.0075, 0.005),   # extraction septum channel: x, y
    'septum_ex_blade': 0.001478,     # exit septum: blade (+x side) distance from the beam axis
    'septum_ex_outer': 0.0085,       # exit septum: outer channel wall (-x side)
    'septum_ex_half_y': 0.005,       # exit septum: vertical half-gap
    'observe_quad': 4, 'observe_bend': 8,   # observation-only subdivisions for interior envelopes
}

# Steering uses only existing magnets: horizontal field trims of the six dipoles
# (PolynomB[0], fixed geometry, as for dipole field errors). Readings are taken
# at existing element boundaries: each quadrupole exit, the injection-septum
# entrance and the line end. No element is added; there is no vertical knob.
TRIM_DIPOLES = BENDS
MONITOR_AFTER = QUADS


def bend_sagitta(lattice):
    """Sagitta [m] of each bend's reference arc relative to its chord: L theta / 8 (small angle)."""
    return {e.FamName: abs(e.BendingAngle) * e.Length / 8 for e in lattice if e.FamName in BENDS}


def _limits(name, model):
    """Return ('rect', [xmin, xmax, ymin, ymax]) or ('ellipse', [ax, ay]) for an element family."""
    if name in QUADS:
        return 'ellipse', [model['quad_bore_radius']] * 2
    if name == 'kext':
        x, y = model['kicker_half']
        return 'rect', [-x, x, -y, y]
    if name in ('b1', 'b2', 'b3'):
        x, y = model['dipole_half']
        return 'rect', [-x, x, -y, y]
    if name == 'sept_in':
        x, y = model['septum_in_half']
        return 'rect', [-x, x, -y, y]
    if name in ('sept_ex', 'blade_exit'):
        y = model['septum_ex_half_y']
        return 'rect', [-model['septum_ex_outer'], model['septum_ex_blade'], -y, y]
    r = model['pipe_radius']
    return 'ellipse', [r, r]


def aperture_lattice(strengths, errors=None, model=None):
    """The unchanged 36-element BTS line with an aperture attribute on every element.

    No element is added, removed or sliced. Static errors are applied as in
    ``apply_static``. Drifts and quadrupoles get round apertures, the kicker,
    septa and bends rectangular ones, and the end marker m4 carries the
    injection-septum limits so that the blade is also checked at the line end.
    The four legacy aperture elements are kept with their original limits.
    AT checks these apertures at each element entrance.
    """
    model = {**APERTURE_MODEL, **(model or {})}
    lat = lattice_for(np.asarray(strengths, dtype=float))
    if errors is not None:
        apply_static(lat, errors)
    for elem in lat:
        if isinstance(elem, at.Aperture):
            continue
        if elem.FamName == 'm4':
            elem.RApertures = np.array(_limits('sept_ex', model)[1], dtype=float)
            continue
        if elem.Length == 0:
            continue
        kind, lim = _limits(elem.FamName, model)
        setattr(elem, 'RApertures' if kind == 'rect' else 'EApertures', np.array(lim, dtype=float))
    return lat


def observation_copy(lattice, model=None):
    """Observation-only copy with magnets subdivided, to sample interior envelopes.

    Used solely to evaluate clearances inside magnets; tracking and losses use
    the unchanged line. Pieces inherit the element's aperture attributes.
    """
    model = {**APERTURE_MODEL, **(model or {})}
    pieces = []
    for elem in lattice:
        if elem.Length > 0 and not isinstance(elem, at.Drift):
            n = model['observe_quad'] if elem.FamName in QUADS else model['observe_bend']
            pieces.extend(elem.divide(np.full(n, 1.0 / n)))
        else:
            pieces.append(elem.deepcopy())
    return at.Lattice(pieces, energy=lattice.energy, name='bts_observation')


def aperture_table(lattice):
    """Every aperture in the line: index, family, s at entrance [m], kind and limits [m]."""
    rows, s = [], 0.0
    for i, e in enumerate(lattice):
        for kind, attr in (('rect', 'RApertures'), ('ellipse', 'EApertures')):
            if hasattr(e, attr):
                rows.append({'index': i, 'name': e.FamName, 's_m': s, 'kind': kind,
                             'limits_m': np.asarray(getattr(e, attr)).tolist()})
        if isinstance(e, at.Aperture):
            rows.append({'index': i, 'name': e.FamName, 's_m': s, 'kind': 'rect', 'limits_m': np.asarray(e.Limits).tolist()})
        s += e.Length
    return rows


def _unrestricted(lattice):
    result = deepcopy(lattice)
    for e in result:
        for attr in ('RApertures', 'EApertures'):
            if hasattr(e, attr):
                delattr(e, attr)
        if isinstance(e, at.Aperture):
            e.Limits = np.array([-np.inf, np.inf, -np.inf, np.inf])
    return result


def moments(lattice, centroid, covariance, step=1e-7):
    """Centroids [m, rad] and 5x5 covariances at every element entrance (and line end).

    Central-difference AT Jacobians about the actual centroid, uncensored by
    apertures; returns ``(means (n+1, 5), covs (n+1, 5, 5))``.
    """
    centroid = np.asarray(centroid, dtype=float)
    probes = np.zeros((6, 11), order='F')
    probes[:5] = centroid[:, None]
    for j in range(5):
        probes[j, 1 + 2 * j] += step
        probes[j, 2 + 2 * j] -= step
    out = at.lattice_track(_unrestricted(lattice), probes, nturns=1,
                           refpts=np.arange(len(lattice) + 1))[0][:, :, :, 0]
    if not np.all(np.isfinite(out)):
        raise ValueError('Invalid moment probes')
    maps = np.stack([(out[:5, 1 + 2 * j] - out[:5, 2 + 2 * j]) / (2 * step) for j in range(5)], axis=-1)
    maps = maps.transpose(1, 0, 2)
    cov = np.asarray(covariance)[:5, :5]
    return out[:5, 0].T, maps @ cov @ maps.transpose(0, 2, 1)


def ellipse_loss_probability(mean, covariance, halfwidths, angles=256):
    """Exact probability [1] that a 2-D Gaussian (x, y) lies outside the ellipse x^2/a^2 + y^2/b^2 <= 1.

    ``mean`` [m] and ``covariance`` [m^2] are the transverse (x, y) centroid and
    covariance, ``halfwidths`` = (a, b) [m]. In scaled coordinates the ellipse
    is the unit circle; along each polar direction the radial integral from 1
    to infinity has a closed form, and the periodic angular integral converges
    spectrally with the trapezoidal rule. Unlike 1 - P(inside), the result keeps
    full relative accuracy in the far tail. Example: a centred isotropic beam
    with rms sigma at a circle of radius 5 sigma gives exp(-12.5).
    """
    a, b = halfwidths
    scale = np.diag([1.0 / a, 1.0 / b])
    m = scale @ np.asarray(mean, dtype=float)
    c = scale @ np.asarray(covariance, dtype=float) @ scale
    if np.linalg.det(c) <= 0:
        raise ValueError('Positive-definite (x, y) covariance required')
    inv = np.linalg.inv(c)
    theta = np.linspace(0.0, 2 * np.pi, angles, endpoint=False)
    e = np.stack([np.cos(theta), np.sin(theta)])
    big_a = np.einsum('in,ij,jn->n', e, inv, e)
    big_b = e.T @ inv @ m
    r0, s = big_b / big_a, 1.0 / np.sqrt(big_a)
    # Exponent of the density at the radial maximum r0, relative to the centre value.
    offset = 0.5 * (m @ inv @ m - big_b ** 2 / big_a)
    radial = (s ** 2 * np.exp(-0.5 * ((1 - r0) / s) ** 2 - offset)
              + r0 * s * np.sqrt(2 * np.pi) * np.exp(-offset) * norm.sf((1 - r0) / s))
    value = radial.mean() / np.sqrt(np.linalg.det(c))
    return float(min(1.0, max(0.0, value)))


def _edges(row, means_i, plane):
    """Lower/upper aperture edge [m] in one plane; ellipses use the other plane's centroid.

    For a round or elliptical aperture this chord is a geometric construction
    used for the five-sigma clearance only; its loss probability is evaluated
    exactly in two dimensions by ``ellipse_loss_probability``.
    """
    lim = row['limits_m']
    if row['kind'] == 'rect':
        return (lim[0], lim[1]) if plane == 0 else (lim[2], lim[3])
    a, b = lim
    other = means_i[2] if plane == 0 else means_i[0]
    other_half = b if plane == 0 else a
    scale = np.sqrt(max(0.0, 1.0 - (other / other_half) ** 2))
    half = (a if plane == 0 else b) * scale
    return -half, half


def clearance_and_loss(lattice, centroid, covariance, coverage=5.0, table=None, round_aperture='exact'):
    """Five-sigma clearance [m] and Gaussian loss probability at every aperture.

    For each aperture and plane, with projected centroid mu and rms sigma,
    clearance = min(a+ - mu, mu - a-) - n sigma. Loss events are exact for a
    Gaussian beam: a rectangular or one-sided aperture contributes one
    interval event per plane, Phi((a- - mu)/sigma) + Phi((mu - a+)/sigma), and a
    round or elliptical aperture one two-dimensional event
    (``ellipse_loss_probability``). The line loss is then bracketed by the
    largest event probability (lower bound) and their sum (union upper bound).
    ``round_aperture='chord'`` reproduces the round-3 projected-chord
    probabilities, which are an approximation and give no valid bracket for
    round apertures. Returns a dict with per-aperture rows, the minimum
    clearance, its location and both loss bounds.
    """
    if round_aperture not in ('exact', 'chord'):
        raise ValueError("round_aperture must be 'exact' or 'chord'")
    table = table or aperture_table(lattice)
    means, covs = moments(lattice, centroid, covariance)
    rows, events = [], []
    for row in table:
        i = row['index']
        exact_round = row['kind'] == 'ellipse' and round_aperture == 'exact'
        if exact_round:
            event = ellipse_loss_probability(means[i, [0, 2]], covs[i][np.ix_([0, 2], [0, 2])], row['limits_m'])
            events.append(event)
        for plane, j in ((0, 0), (1, 2)):
            lo, hi = _edges(row, means[i], plane)
            mu, sigma = means[i, j], float(np.sqrt(max(covs[i, j, j], 0.0)))
            p = float(norm.cdf((lo - mu) / sigma) + norm.sf((hi - mu) / sigma)) if sigma > 0 else 0.0
            if not exact_round:
                events.append(p)
            rows.append({'index': i, 'name': row['name'], 's_m': row['s_m'], 'plane': plane, 'centroid_m': float(mu),
                         'sigma_m': sigma, 'clearance_m': float(min(hi - mu, mu - lo) - coverage * sigma),
                         'loss_probability': event if exact_round else p, 'projected_probability': p,
                         'event': 'ellipse' if exact_round else 'interval'})
    active = min(rows, key=lambda r: r['clearance_m'])
    probs = np.array(events)
    return {'rows': rows, 'minimum_m': active['clearance_m'], 'active': [active['name'], active['plane'], active['s_m']],
            'loss_lower': float(probs.max()), 'loss_union': float(min(1.0, probs.sum())),
            'exit_centroid': means[-1].tolist(), 'exit_covariance': covs[-1].tolist()}


# ---------------------------------------------------------------------------
# Jitter transfer between matched ends (R2B-04/R2B-05)
# ---------------------------------------------------------------------------
# Booster shot jitter at the entrance m1 (the convention of both manuscripts):
# position 0.5 mm, angle 0.2 mrad, centroid momentum 0.1 % rms, independent.
JITTER = {'x_m': 5e-4, 'xp_rad': 2e-4, 'delta': 1e-3}


def entrance_jitter_covariance(jitter=None, twiss=None):
    """5x5 covariance [m, rad, 1] of the shot centroid at m1, momentum jitter carried by dispersion."""
    jitter = {**JITTER, **(jitter or {})}
    tw = twiss or DEFAULT_BTS_ENTRANCE_TWISS
    t = np.zeros((5, 3))
    t[0, 0] = t[1, 1] = t[4, 2] = 1.0
    t[0, 2], t[1, 2] = tw.disp_x, tw.disp_px
    return t @ np.diag([jitter['x_m'] ** 2, jitter['xp_rad'] ** 2, jitter['delta'] ** 2]) @ t.T


def phase_advance(lattice):
    """Unwrapped horizontal and vertical betatron phase advance [rad] from m1 to the line end."""
    from .bts_journal import independent_maps
    tw = DEFAULT_BTS_ENTRANCE_TWISS
    maps = independent_maps(lattice)[0]
    result = []
    for i, b0, a0 in ((0, tw.beta_x, tw.alpha_x), (2, tw.beta_y, tw.alpha_y)):
        result.append(float(np.unwrap([np.arctan2(m[i, i + 1], b0 * m[i, i] - a0 * m[i, i + 1]) for m in maps])[-1]))
    return tuple(result)


def jitter_transfer(mu_x, jitter=None):
    """Exit (x, x') centroid covariance [m^2, m rad, rad^2] for matched ends and phase advance mu_x [rad].

    With both ends matched, M = B_exit R(mu) B_entrance^-1 in each plane, so the
    betatron part of the exit jitter depends on the optics only through mu_x;
    the momentum part is D_exit delta and D'_exit delta for every matched setting.
    """
    jitter = {**JITTER, **(jitter or {})}
    tw, ex = DEFAULT_BTS_ENTRANCE_TWISS, EXIT_TWISS
    b0, a0, be, ae = tw.beta_x, tw.alpha_x, ex['beta_x'], ex['alpha_x']
    inv0 = np.array([[1 / np.sqrt(b0), 0.0], [a0 / np.sqrt(b0), np.sqrt(b0)]])
    be_mat = np.array([[np.sqrt(be), 0.0], [-ae / np.sqrt(be), 1 / np.sqrt(be)]])
    rot = np.array([[np.cos(mu_x), np.sin(mu_x)], [-np.sin(mu_x), np.cos(mu_x)]])
    m = be_mat @ rot @ inv0
    betatron = m @ np.diag([jitter['x_m'] ** 2, jitter['xp_rad'] ** 2]) @ m.T
    d = np.array([ex['disp_x'], ex['disp_px']])
    return betatron + jitter['delta'] ** 2 * np.outer(d, d)


def shot_averaged_loss(lattice, beam=None, jitter=None, coverage=5.0):
    """Shot-averaged Gaussian loss probability at every aperture of an error-free line.

    A Gaussian beam whose centroid is itself Gaussian (linear transport of the
    entrance jitter) has, in projection, a Gaussian distribution with the summed
    covariance, so the expected lost fraction per aperture is a Gaussian tail
    of beam plus jitter. Returns the ``clearance_and_loss`` dict for that
    combined covariance (clearances there use the combined size).
    """
    beam = beam or JournalBeam()
    total = beam.covariance()[:5, :5] + entrance_jitter_covariance(jitter)
    return clearance_and_loss(lattice, np.zeros(5), total, coverage)


# ---------------------------------------------------------------------------
# Trajectory correction (R2B-03)
# ---------------------------------------------------------------------------
STEERING = {'bpm_error_m': 5e-5, 'end_weight': 3.0, 'kick_limit_rad': 1e-3, 'tikhonov': 1e-3, 'iterations': 2}


def monitor_refpts(lattice):
    """Existing element boundaries used as horizontal monitors: quadrupole exits,
    injection-septum entrance and line end (weighted ends last two)."""
    names = [e.FamName for e in lattice]
    points = [i + 1 for i, n in enumerate(names) if n in MONITOR_AFTER]
    return points + [names.index('sept_ex'), len(lattice)]


def trim_indices(lattice):
    return [i for i, e in enumerate(lattice) if e.FamName in TRIM_DIPOLES]


def apply_trims(lattice, trims):
    """Copy of ``lattice`` with horizontal dipole field trims; ``trims`` [rad] are the added kicks."""
    line = deepcopy(lattice)
    for i, t in zip(trim_indices(line), trims):
        line[i].PolynomB = np.array(line[i].PolynomB, dtype=float)
        line[i].PolynomB[0] = line[i].PolynomB[0] - t / line[i].Length
    return line


def orbit_at(lattice, refpts, centroid=None):
    """Single-particle trajectory (x, y) [m] at ``refpts`` for a given entrance centroid (default zero)."""
    p = np.zeros((6, 1), order='F')
    if centroid is not None:
        p[:5, 0] = centroid
    out = at.lattice_track(_unrestricted(lattice), p, nturns=1, refpts=refpts)[0][:, 0, :, 0]
    return out[[0, 2]].T


def response_matrix(lattice, step=1e-5):
    """Horizontal monitor response [m/rad] to each dipole trim, from the error-free model line."""
    monitors, n = monitor_refpts(lattice), len(trim_indices(lattice))
    base = orbit_at(lattice, monitors)[:, 0]
    columns = []
    for k in range(n):
        trims = np.zeros(n)
        trims[k] = step
        columns.append((orbit_at(apply_trims(lattice, trims), monitors)[:, 0] - base) / step)
    return np.array(columns).T, monitors, n


def correct_trajectory(lattice, model_response, bpm_errors, settings=None):
    """Steer a static machine horizontally with dipole field trims; returns the steered line and trims [rad].

    Readings are the zero-input horizontal trajectory at the monitor points plus
    static reading errors. Weighted (septum entrance and end ``end_weight``),
    Tikhonov-regularised least squares with the model response, ``iterations``
    passes, trims clipped to the declared limit. Shot jitter and the vertical
    plane are not corrected.
    """
    settings = {**STEERING, **(settings or {})}
    matrix, monitors, n = model_response
    w = np.ones(len(monitors))
    w[-2:] = settings['end_weight']
    trims = np.zeros(n)
    line = lattice
    for _ in range(settings['iterations']):
        reading = orbit_at(line, monitors)[:, 0] + np.asarray(bpm_errors)[:len(monitors)]
        a = matrix * w[:, None]
        reg = settings['tikhonov'] * np.linalg.norm(a, 2)
        delta = np.linalg.lstsq(np.vstack([a, reg * np.eye(n)]), np.concatenate([-w * reading, np.zeros(n)]), rcond=None)[0]
        trims = np.clip(trims + delta, -settings['kick_limit_rad'], settings['kick_limit_rad'])
        line = apply_trims(lattice, trims)
    return line, trims
