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
    'slices_quad': 4, 'slices_bend': 8,
}

# Corrector and monitor layout for trajectory correction (R2B-03), declared.
CORRECTOR_BEFORE = ('q11', 'q21', 'q31', 'sept_ex')
# Amended layout (after the declared one was found not to control the exit angle):
# a corrector before b3 and a monitor at the injection-septum entrance.
AMENDED_CORRECTORS = ('q11', 'q21', 'q31', 'b3', 'sept_ex')
AMENDED_MONITORS = ('sept_ex',)
MONITOR_AFTER = QUADS + ('end',)


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


def elementwise_lattice(strengths, errors=None, model=None, correctors=True, integration_steps=10,
                        corrector_before=None, monitor_before=()):
    """Build the BTS line with an aperture on every element, sliced magnets and correctors.

    Static errors are applied before slicing so AT keeps misalignments on the
    magnet ends. The four legacy aperture markers are removed; an aperture
    element at the end carries the exit-septum limits. Correctors are zero-length
    AT ``Corrector`` elements (KickAngle [rad]) named ``hcv_<family>``; monitors
    are markers ``bpm_<family>`` after each quadrupole and ``bpm_end``.
    """
    model = {**APERTURE_MODEL, **(model or {})}
    corrector_before = CORRECTOR_BEFORE if corrector_before is None else tuple(corrector_before)
    base = lattice_for(np.asarray(strengths, dtype=float))
    if errors is not None:
        apply_static(base, errors)
    elements = []
    for elem in base:
        if isinstance(elem, at.Aperture):
            continue
        if elem.FamName in monitor_before:
            elements.append(at.Marker('bpm_pre_' + elem.FamName))
        if correctors and elem.FamName in corrector_before:
            elements.append(at.Corrector('hcv_' + elem.FamName, 0.0, [0.0, 0.0]))
        if elem.Length > 0 and not isinstance(elem, at.Drift):
            n = model['slices_quad'] if elem.FamName in QUADS else model['slices_bend']
            pieces = elem.divide(np.full(n, 1.0 / n))
        else:
            pieces = [elem]
        for piece in pieces:
            if hasattr(piece, 'NumIntSteps'):
                piece.NumIntSteps = integration_steps
            kind, lim = _limits(elem.FamName, model)
            if elem.Length > 0 or kind == 'rect':
                if kind == 'rect':
                    piece.RApertures = np.array(lim, dtype=float)
                else:
                    piece.EApertures = np.array(lim, dtype=float)
            elements.append(piece)
        if elem.FamName in QUADS:
            elements.append(at.Marker('bpm_' + elem.FamName))
    elements.append(at.Aperture('blade_exit', _limits('blade_exit', model)[1]))
    elements.append(at.Marker('bpm_end'))
    return at.Lattice(elements, energy=base.energy, name='bts_elementwise')


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


def _edges(row, means_i, plane):
    """Lower/upper aperture edge [m] in one plane; ellipses use the other plane's centroid."""
    lim = row['limits_m']
    if row['kind'] == 'rect':
        return (lim[0], lim[1]) if plane == 0 else (lim[2], lim[3])
    a, b = lim
    other = means_i[2] if plane == 0 else means_i[0]
    other_half = b if plane == 0 else a
    scale = np.sqrt(max(0.0, 1.0 - (other / other_half) ** 2))
    half = (a if plane == 0 else b) * scale
    return -half, half


def clearance_and_loss(lattice, centroid, covariance, coverage=5.0, table=None):
    """Five-sigma clearance [m] and Gaussian loss probability at every aperture.

    For each aperture and plane, with projected centroid mu and rms sigma,
    clearance = min(a+ - mu, mu - a-) - n sigma and the projected loss
    probability is Phi((a- - mu)/sigma) + Phi((mu - a+)/sigma). The line loss
    is bracketed by the largest single-aperture probability (lower bound) and
    the union bound (sum, upper bound). Returns a dict with per-aperture rows,
    the minimum clearance, its location and both loss bounds.
    """
    table = table or aperture_table(lattice)
    means, covs = moments(lattice, centroid, covariance)
    rows = []
    for row in table:
        i = row['index']
        for plane, j in ((0, 0), (1, 2)):
            lo, hi = _edges(row, means[i], plane)
            mu, sigma = means[i, j], float(np.sqrt(max(covs[i, j, j], 0.0)))
            p = float(norm.cdf((lo - mu) / sigma) + norm.sf((hi - mu) / sigma)) if sigma > 0 else 0.0
            rows.append({'index': i, 'name': row['name'], 's_m': row['s_m'], 'plane': plane, 'centroid_m': float(mu),
                         'sigma_m': sigma, 'clearance_m': float(min(hi - mu, mu - lo) - coverage * sigma),
                         'loss_probability': p})
    active = min(rows, key=lambda r: r['clearance_m'])
    probs = np.array([r['loss_probability'] for r in rows])
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


def _indices(lattice, prefix):
    return [i for i, e in enumerate(lattice) if e.FamName.startswith(prefix)]


def orbit_at(lattice, refpts, centroid=None):
    """Single-particle trajectory (x, y) [m] at ``refpts`` for a given entrance centroid (default zero)."""
    p = np.zeros((6, 1), order='F')
    if centroid is not None:
        p[:5, 0] = centroid
    out = at.lattice_track(_unrestricted(lattice), p, nturns=1, refpts=refpts)[0][:, 0, :, 0]
    return out[[0, 2]].T


def response_matrix(lattice, step=1e-5):
    """BPM (x, y) response [m/rad] to each corrector's (h, v) kick, from the model line."""
    bpms, cors = _indices(lattice, 'bpm_'), _indices(lattice, 'hcv_')
    base = orbit_at(lattice, bpms).ravel()
    columns = []
    for plane in (0, 1):
        for c in cors:
            trial = deepcopy(lattice)
            kick = np.zeros(2)
            kick[plane] = step
            trial[c].KickAngle = kick
            columns.append((orbit_at(trial, bpms).ravel() - base) / step)
    return np.array(columns).T, bpms, cors


def line_names(lattice):
    return [e.FamName for e in lattice]


def correct_trajectory(lattice, model_response, bpm_errors, settings=None):
    """Steer a static machine with its correctors; returns the corrected line and the kicks [rad].

    Readings are the zero-input trajectory at the BPMs plus static BPM errors
    (offset and calibration residual). Weighted, Tikhonov-regularised least
    squares with the model response, ``iterations`` passes, kicks clipped to
    the declared limit. Shot jitter is not corrected.
    """
    settings = {**STEERING, **(settings or {})}
    matrix, bpms, cors = model_response
    weights = np.ones((len(bpms), 2))
    weights[-1] = settings['end_weight']
    for n, i in enumerate(bpms):
        if line_names(lattice)[i].startswith('bpm_pre_'):
            weights[n] = settings['end_weight']
    w = weights.ravel()
    line = deepcopy(lattice)
    kicks = np.zeros(2 * len(cors))
    for _ in range(settings['iterations']):
        reading = orbit_at(line, bpms).ravel() + np.asarray(bpm_errors).ravel()
        a = matrix * w[:, None]
        reg = settings['tikhonov'] * np.linalg.norm(a, 2)
        delta = np.linalg.lstsq(np.vstack([a, reg * np.eye(a.shape[1])]),
                                np.concatenate([-w * reading, np.zeros(a.shape[1])]), rcond=None)[0]
        kicks = np.clip(kicks + delta, -settings['kick_limit_rad'], settings['kick_limit_rad'])
        for n, c in enumerate(cors):
            line[c].KickAngle = np.array([kicks[n], kicks[len(cors) + n]])
    return line, kicks
