"""Round-three BTS physics tests (Reviewer 2 tasks R2B-01 to R2B-06). SI units."""
import json
from pathlib import Path

import at
import numpy as np
import pytest

from nkm_injection.bts_journal import JournalBeam, QUADS, lattice_for
from nkm_injection.bts_round2 import station_record
from nkm_injection.bts_round3 import (APERTURE_MODEL, aperture_table, boundary_clearances, clearance_and_loss,
                                      elementwise_lattice)

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = json.loads((ROOT / 'docs/paper_bts/generated/round2_designs.json').read_text())['designs']


@pytest.mark.parametrize('name', ['reference', 'low_beta'])
def test_end_station_clearances_are_fixed_by_boundary_optics(name):
    """Every matched setting has the analytic entrance and exit clearances (R2B-02)."""
    k = np.array(DESIGNS['baseline']['nominal'][name]['strengths_m_minus2'])
    record = station_record(lattice_for(k))
    analytic = boundary_clearances()
    by_station = {(r['s_m'] > 1.0, r['axis']): r['clearance_m'] for r in record['stations']
                  if r['s_m'] in (0.0,) or abs(r['s_m'] - 21.789) < 1e-3}
    for axis in (0, 1):
        assert by_station[(False, axis)] == pytest.approx(analytic['entrance'][axis], abs=1e-9)
        assert by_station[(True, axis)] == pytest.approx(analytic['exit'][axis], abs=2e-7)
    assert record['minimum_m'] == pytest.approx(analytic['entrance'][0], abs=1e-9)


def test_boundary_clearance_values_match_table_2():
    analytic = boundary_clearances()
    assert np.round(np.array(analytic['entrance']) * 1e3, 3).tolist() == [17.455, 18.865]
    assert np.round(np.array(analytic['exit']) * 1e3, 3).tolist() == [18.555, 19.064]

REFERENCE = np.array(DESIGNS['baseline']['nominal']['reference']['strengths_m_minus2'])


def _track_end(line, particle):
    p = np.zeros((6, 1), order='F')
    p[:, 0] = particle
    return at.lattice_track(line, p, nturns=1)[0][:, 0, 0, 0]


def test_elementwise_line_preserves_transport():
    """Slicing, correctors at zero and markers leave the single-pass map unchanged (R2B-01)."""
    particle = np.array([2e-4, 1e-5, -1e-4, 2e-5, 1e-3, 0.0])
    original = lattice_for(REFERENCE)
    sliced = elementwise_lattice(REFERENCE)
    np.testing.assert_allclose(_track_end(sliced, particle), _track_end(original, particle), atol=1e-10)


def test_every_magnet_slice_has_an_aperture():
    line = elementwise_lattice(REFERENCE)
    for e in line:
        if e.FamName in QUADS + ('b1', 'b2', 'b3', 'sept_in', 'sept_ex', 'kext'):
            assert hasattr(e, 'RApertures') or hasattr(e, 'EApertures'), e.FamName
    names = {r['name'] for r in aperture_table(line)}
    assert {'q11', 'b2', 'sept_ex', 'blade_exit'} <= names


def test_blade_is_active_and_independent_of_quadrupoles():
    beam = JournalBeam()
    low = np.array(json.loads((ROOT / 'docs/paper_bts/generated/round2_spatial.json').read_text())
                   ['refined_low_beta']['strengths_m_minus2'])
    results = [clearance_and_loss(elementwise_lattice(k), np.zeros(5), beam.covariance()) for k in (REFERENCE, low)]
    for r in results:
        assert r['active'][0] == 'sept_ex' and r['active'][1] == 0
    assert results[0]['minimum_m'] == pytest.approx(results[1]['minimum_m'], abs=1e-9)
    blade = next(x for x in results[0]['rows'] if x['name'] == 'blade_exit' and x['plane'] == 0)
    assert blade['clearance_m'] == pytest.approx(APERTURE_MODEL['septum_ex_blade'] - 5 * blade['sigma_m'], abs=1e-9)


def test_gaussian_loss_probability_and_particle_loss_agree():
    """A beam pushed onto the blade loses the analytic Gaussian tail fraction in tracking."""
    from scipy.stats import norm
    beam = JournalBeam()
    line = elementwise_lattice(REFERENCE)
    record = clearance_and_loss(line, np.zeros(5), beam.covariance())
    blade = next(x for x in record['rows'] if x['name'] == 'blade_exit' and x['plane'] == 0)
    assert blade['loss_probability'] == pytest.approx(norm.sf(APERTURE_MODEL['septum_ex_blade'] / blade['sigma_m'])
                                                      + norm.cdf(-0.0085 / blade['sigma_m']), rel=1e-9)
    rng = np.random.default_rng(5)
    shifted = np.array([-1e-3, -1.5e-4, 0, 0, 0])  # entrance offset that moves the exit beam towards the blade
    pred = clearance_and_loss(line, shifted, beam.covariance())
    assert pred['loss_lower'] > 0.01
    sample = rng.multivariate_normal(np.zeros(6), beam.covariance(), 20000).T
    sample[:5] += shifted[:, None]
    out = at.lattice_track(line, np.array(sample, order='F'), nturns=1)[0][:, :, 0, 0]
    observed = np.mean(~np.isfinite(out[0]))
    assert pred['loss_lower'] <= observed + 4 * np.sqrt(pred['loss_union'] / 20000) + 1e-4
    assert observed <= pred['loss_union'] + 4 * np.sqrt(pred['loss_union'] / 20000) + 1e-4


def test_amended_steering_controls_exit_position_and_angle():
    """Correction with the model response removes most of the static exit offset and angle (R2B-03)."""
    from nkm_injection.bts_journal import draw_static
    from nkm_injection.bts_round3 import (AMENDED_CORRECTORS, AMENDED_MONITORS, correct_trajectory, orbit_at,
                                          response_matrix)
    kwargs = {'corrector_before': AMENDED_CORRECTORS, 'monitor_before': AMENDED_MONITORS}
    response = response_matrix(elementwise_lattice(REFERENCE, **kwargs))
    before, after = [], []
    for m in range(6):
        errors = draw_static(np.random.default_rng([7, m]), lattice_for(REFERENCE))
        machine = elementwise_lattice(REFERENCE, errors, **kwargs)
        bpm = np.random.default_rng([8, m]).normal(0, 5e-5, (len(response[1]), 2))
        line, kicks = correct_trajectory(machine, response, bpm)
        assert np.all(np.abs(kicks) <= 1e-3 + 1e-15)
        for target, lat in ((before, machine), (after, line)):
            p = np.zeros((6, 1), order='F')
            target.append(at.lattice_track(lat, p, nturns=1, refpts=[len(lat)])[0][:2, 0, 0, 0])
    before, after = np.array(before), np.array(after)
    assert np.sqrt(np.mean(after[:, 0] ** 2)) < 0.25 * np.sqrt(np.mean(before[:, 0] ** 2))
    assert np.sqrt(np.mean(after[:, 1] ** 2)) < 2e-4


def test_zero_kick_correctors_do_not_change_the_line():
    from nkm_injection.bts_round3 import AMENDED_CORRECTORS, AMENDED_MONITORS
    particle = np.array([3e-4, -2e-5, 1e-4, 1e-5, -1e-3, 0.0])
    plain = elementwise_lattice(REFERENCE, correctors=False)
    amended = elementwise_lattice(REFERENCE, corrector_before=AMENDED_CORRECTORS, monitor_before=AMENDED_MONITORS)
    np.testing.assert_allclose(_track_end(amended, particle), _track_end(plain, particle), atol=1e-12)


def test_jitter_transfer_depends_only_on_phase_advance():
    """For matched settings the exit jitter from maps equals the rotation formula of Eq. (transfer) (R2B-04)."""
    from nkm_injection.bts_journal import independent_maps
    from nkm_injection.bts_round3 import entrance_jitter_covariance, jitter_transfer, phase_advance
    low = np.array(json.loads((ROOT / 'docs/paper_bts/generated/round2_spatial.json').read_text())
                   ['refined_low_beta']['strengths_m_minus2'])
    robust = np.array(json.loads((ROOT / 'docs/paper_bts/generated/round3_design.json').read_text())
                      ['robust']['designs']['robust']['strengths_m_minus2'])
    for k in (REFERENCE, low, robust):
        lat = lattice_for(k)
        m = independent_maps(lat)[0][-1]
        maps = (m @ entrance_jitter_covariance() @ m.T)[:2, :2]
        np.testing.assert_allclose(jitter_transfer(phase_advance(lat)[0]), maps, rtol=2e-4, atol=1e-14)


def test_shot_averaged_loss_equals_average_over_shots():
    """Gaussian beam with a Gaussian centroid: summed-covariance tail equals the mean per-shot tail."""
    from nkm_injection.bts_round3 import entrance_jitter_covariance, shot_averaged_loss
    beam = JournalBeam()
    line = elementwise_lattice(REFERENCE, correctors=False)
    table = aperture_table(line)
    averaged = shot_averaged_loss(line)
    blade = lambda r: next(x for x in r['rows'] if x['name'] == 'blade_exit' and x['plane'] == 0)['loss_probability']
    rng = np.random.default_rng(11)
    shots = rng.multivariate_normal(np.zeros(5), entrance_jitter_covariance(), 400)
    mean = np.mean([blade(clearance_and_loss(line, c, beam.covariance(), table=table)) for c in shots])
    assert mean == pytest.approx(blade(averaged), rel=0.15)


def test_dispersion_free_exit_setting_is_matched_and_reduces_blade_loss():
    """The selected dispersion-free solution matches D = D' = 0 with the same Twiss and lowers the blade loss (R2B-05)."""
    from nkm_injection.bts_journal import TARGET
    from nkm_injection.bts_round2 import nominal_observables
    from nkm_injection.bts_round3 import EXIT_TWISS, phase_advance, shot_averaged_loss
    exit_data = json.loads((ROOT / 'docs/paper_bts/generated/round3_exit.json').read_text())
    k = np.array(exit_data['dispersion_free_best']['strengths_m_minus2'])
    observed = nominal_observables(lattice_for(k))
    np.testing.assert_allclose(observed[:4], TARGET[:4], atol=5e-5)
    np.testing.assert_allclose(observed[4:], 0.0, atol=2e-6)
    assert EXIT_TWISS['disp_x'] == TARGET[4] and EXIT_TWISS['disp_px'] == TARGET[5]
    assert np.degrees(phase_advance(lattice_for(k))[0]) < 190
    free = shot_averaged_loss(elementwise_lattice(k, correctors=False))['loss_lower']
    configured = shot_averaged_loss(elementwise_lattice(REFERENCE, correctors=False))['loss_lower']
    assert free < 0.01 * configured
