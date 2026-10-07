"""Tracking must use current lattice physics without shared map state."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Lock

import at
import numpy as np
import pytest

from src.nkm_injection.beam import generate_6d_beam
from src.nkm_injection.storage_ring_injection import (
    StorageRingInjectionConfig, track_multiturn_injection,
)


def make_ring():
    # A small FODO lattice, all in-memory; no scientific source regeneration.
    return at.Lattice([at.Drift('D1', .5), at.Quadrupole('QF', .2, 1.),
                       at.Drift('D2', .5), at.Quadrupole('QD', .2, -1.)], energy=4e9)


@pytest.fixture
def beam():
    return generate_6d_beam(n_particles=8, beta_x=2., alpha_x=0., emit_x=1e-9,
                            beta_y=2., alpha_y=0., emit_y=1e-10, seed=42)


def expected_beam(ring, beam, turns):
    matrix, _ = ring.find_m66(dp=0.0)
    result = beam.copy()
    for _ in range(turns):
        result = matrix @ result
    return result


@pytest.mark.parametrize('change', ['strength', 'length', 'alignment_rotation'])
def test_same_ring_mutations_use_a_fresh_map(beam, change):
    ring = make_ring()
    before = track_multiturn_injection(beam, ring, n_turns=3, kicker_model='off')
    if change == 'strength':
        ring[1].K = 1.5
    elif change == 'length':
        ring[0].Length = .8
    else:
        # Apply a quadrupole roll using the same AT rotation convention as errors.py.
        rotation = np.eye(6)
        c, s = np.cos(.1), np.sin(.1)
        rotation[0, 0] = rotation[1, 1] = rotation[2, 2] = rotation[3, 3] = c
        rotation[0, 2] = rotation[1, 3] = s
        rotation[2, 0] = rotation[3, 1] = -s
        ring[1].R1, ring[1].R2 = rotation, rotation.T
    after = track_multiturn_injection(beam, ring, n_turns=3, kicker_model='off')
    np.testing.assert_allclose(after.particles_6d, expected_beam(ring, beam, 3), rtol=0, atol=1e-14)
    assert np.max(np.abs(before.particles_6d - after.particles_6d)) > 1e-8


def test_map_is_computed_once_per_call_and_energy_change_is_seen(beam, monkeypatch):
    ring = make_ring()
    original = ring.find_m66
    energies = []
    def find(**kwargs):
        energies.append(ring.energy)
        assert kwargs == {'dp': 0.0}
        return original(**kwargs)
    monkeypatch.setattr(ring, 'find_m66', find)
    track_multiturn_injection(beam, ring, n_turns=5, kicker_model='off')
    ring.energy = 5e9
    after = track_multiturn_injection(beam, ring, n_turns=5, kicker_model='off')
    assert energies == [4e9, 5e9]
    matrix, _ = original(dp=0.0)
    np.testing.assert_allclose(after.particles_6d, np.linalg.matrix_power(matrix, 5) @ beam, rtol=0, atol=1e-14)


def test_alternating_rings_match_independent_maps(beam):
    first, second = make_ring(), make_ring()
    second[1].K = .4
    for ring in (first, second, first, second):
        actual = track_multiturn_injection(beam, ring, n_turns=2, kicker_model='off')
        np.testing.assert_allclose(actual.particles_6d, expected_beam(ring, beam, 2), rtol=0, atol=1e-14)


class LinearRing:
    """Controlled map provider for simultaneous Python calls, avoiding pyAT C state."""
    def __init__(self, drift, barrier=None):
        self.matrix = np.eye(6)
        self.matrix[0, 1] = drift
        self.calls = 0
        self.barrier = barrier
        self.lock = Lock()

    def find_m66(self, dp):
        assert dp == 0
        with self.lock:
            self.calls += 1
        if self.barrier is not None:
            self.barrier.wait(timeout=10)
        return self.matrix.copy(), None


@pytest.mark.parametrize('same_ring', [False, True])
def test_concurrent_calls_have_independent_maps(beam, same_ring):
    barrier = Barrier(4)
    rings = ([LinearRing(.2, barrier)] * 4 if same_ring else
             [LinearRing(.2 + index*.1, barrier) for index in range(4)])
    inputs = [beam * (1 + index*.1) for index in range(4)]
    originals = [value.copy() for value in inputs]
    def track(index):
        return track_multiturn_injection(inputs[index], rings[index], n_turns=4, kicker_model='off')
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(track, range(4)))
    for index, result in enumerate(results):
        expected = np.linalg.matrix_power(rings[index].matrix, 4) @ inputs[index]
        np.testing.assert_allclose(result.particles_6d, expected, rtol=0, atol=1e-14)
        np.testing.assert_array_equal(inputs[index], originals[index])
    assert rings[0].calls == (4 if same_ring else 1)
    assert not hasattr(track_multiturn_injection, '_m66_cache')


def test_legacy_cache_attribute_cannot_override_current_map(beam, monkeypatch):
    ring = LinearRing(.3)
    monkeypatch.setattr(track_multiturn_injection, '_m66_cache',
                        {'ring_id': id(ring), 'M66': np.eye(6)*2}, raising=False)
    result = track_multiturn_injection(beam, ring, n_turns=2, kicker_model='off')
    np.testing.assert_allclose(result.particles_6d, np.linalg.matrix_power(ring.matrix, 2) @ beam,
                               rtol=0, atol=1e-14)
    assert ring.calls == 1


def test_zero_turns_do_not_require_map_or_change_beam(beam):
    class NoMapRing:
        def find_m66(self, **kwargs):
            pytest.fail('Zero-turn tracking must not compute a map')
    result = track_multiturn_injection(beam, NoMapRing(), n_turns=0, kicker_model='off')
    np.testing.assert_array_equal(result.particles_6d, beam)
    assert result.survival_history == []


def test_recomputation_preserves_aperture_loss_accounting():
    ring = LinearRing(1.)
    beam = np.zeros((6, 4)); beam[1] = [.01, .01, .02, .02]
    config = StorageRingInjectionConfig(injection_aperture_x_m=.045, aperture_x_m=.025)
    result = track_multiturn_injection(beam, ring, n_turns=3, kicker_model='off', config=config)
    assert ring.calls == 1
    assert result.survival_history == [4, 2, 0]
    assert [(loss['particle_index'], loss['turn']) for loss in result.loss_log] == [(2, 2), (3, 2), (0, 3), (1, 3)]
