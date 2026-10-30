"""Round-four BTS tests (consolidated R4-BTS tasks). SI units."""
import json
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.bts_journal import LOWER, SCALES, UPPER, draw_static, lattice_for
from nkm_injection import bts_round3 as r3
from nkm_injection import bts_round4 as r4

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = json.loads((ROOT / 'docs/paper_bts/generated/round2_designs.json').read_text())['designs']
REFERENCE = np.array(DESIGNS['baseline']['nominal']['reference']['strengths_m_minus2'])


def _machine(seed=7):
    errors = draw_static(np.random.default_rng(seed), lattice_for(REFERENCE))
    return r3.aperture_lattice(REFERENCE, errors), r3.aperture_lattice(REFERENCE)


def test_full_layout_reproduces_round3_steering():
    """The full layout is the round-3 corrector: same monitors, knobs and steered line."""
    machine, model = _machine()
    bpm = np.random.default_rng(1).normal(0, 5e-5, 11)
    old_line, old_trims = r3.correct_trajectory(machine, r3.response_matrix(model), bpm)
    response = r4.layout_response(model, r4.LAYOUTS['full'])
    assert response[1] == r3.monitor_refpts(model)
    new_line, kicks = r4.correct_with_layout(machine, response, bpm)
    np.testing.assert_allclose(kicks, old_trims, rtol=0, atol=1e-15)
    np.testing.assert_allclose(r3.orbit_at(new_line, [len(new_line)]), r3.orbit_at(old_line, [len(old_line)]), atol=1e-15)


def test_series_bends_share_one_knob_proportional_to_bending_angle():
    _, model = _machine()
    knobs = r4.knob_weights(model, r4.LAYOUTS['series_bends'])
    assert len(knobs) == 4
    series = knobs[2]
    angles = np.array([model[i].BendingAngle for i, _ in series])
    np.testing.assert_allclose([w for _, w in series], angles / np.max(np.abs(angles)), rtol=0, atol=1e-15)
    assert len(r4.layout_monitors(model, r4.LAYOUTS['reduced_monitors'])) == 5


@pytest.mark.parametrize('layout', ['reduced_monitors', 'series_bends', 'reduced_series'])
def test_every_layout_reduces_the_static_exit_offset(layout):
    machine, model = _machine(3)
    line, kicks = r4.correct_with_layout(machine, r4.layout_response(model, r4.LAYOUTS[layout]), np.zeros(11))
    before = abs(r3.orbit_at(machine, [len(machine)])[0, 0])
    after = abs(r3.orbit_at(line, [len(line)])[0, 0])
    assert after < 0.5 * before
    assert np.all(np.abs(kicks) <= 1e-3 + 1e-15)


def test_phase_residual_vanishes_for_a_matched_setting_at_its_own_phase():
    target = np.array([2.336495, 4.256241, -0.016335, 0.017772, 0.080868, 0.047472])
    mu = r3.phase_advance(lattice_for(REFERENCE))[0]
    residual = r4.phase_residual(REFERENCE, target, SCALES, mu)
    assert residual.shape == (7,)
    assert abs(residual[-1]) < 1e-12
    assert np.max(np.abs(residual[:-1])) < 1e-3
    assert r4.active_bounds(np.array(UPPER), LOWER, UPPER) == [(q, 'upper') for q in r4.QUADS]
