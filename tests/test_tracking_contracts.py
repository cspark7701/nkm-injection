"""Tracking contracts and limiting cases; SI particles, GeV integrator energy."""
import numpy as np
import pytest
import at

from nkm_injection.tracking_contracts import TrackingParameters, validate_particle_array
from nkm_injection.integrators import SymplecticSplitIntegrator, LorentzRK4Integrator
from nkm_injection.tracking import track_nkm_thin_kick, track_nkm_thick_symplectic, track_nkm_thick_rk4
from nkm_injection.storage_ring_injection import (
    track_multiturn_injection, track_element_resolved_injection, StorageRingInjectionConfig,
)
from nkm_injection.beam import compute_beam_statistics
from nkm_injection.units import ELECTRON_CHARGE_C, compute_rigidity

INTEGRATORS = [SymplecticSplitIntegrator, LorentzRK4Integrator]


def zero_field(x, y, z):
    return np.zeros_like(x), np.zeros_like(y)


def thin(beam, **kwargs):
    return track_nkm_thin_kick(beam, lambda x, y: (0., 0.), **kwargs)


@pytest.mark.parametrize('tracker', [thin, track_nkm_thick_symplectic, track_nkm_thick_rk4])
@pytest.mark.parametrize('shape', [(3, 6), (7, 2), (6,), (6, 2, 1)])
def test_wrong_shapes_rejected(tracker, shape):
    kwargs = {} if tracker is thin else {'field_fn': zero_field}
    with pytest.raises(ValueError, match='shape'):
        tracker(np.zeros(shape), **kwargs)


@pytest.mark.parametrize('tracker', [thin, track_nkm_thick_symplectic, track_nkm_thick_rk4])
def test_integer_input_becomes_independent_float_copy(tracker):
    beam = np.zeros((6, 2), dtype=int); beam[1] = [1, 2]
    original = beam.copy()
    kwargs = {} if tracker is thin else {'field_fn': zero_field}
    result = tracker(beam, length_m=0.5, **kwargs)
    assert result.dtype == np.float64
    np.testing.assert_array_equal(beam, original)
    np.testing.assert_allclose(result[0], [0.5, 1.], atol=1e-14, rtol=0)
    assert not np.shares_memory(beam, result)


@pytest.mark.parametrize('column', [[np.inf, 0, 0, 0, 0, 0], [0, np.nan, 0, 0, 0, 0],
    [np.nan, np.nan, 0, 0, 0, 0], [np.nan, np.inf, 0, 0, 0, 0]])
def test_invalid_coordinates_rejected_at_every_boundary(column):
    beam = np.zeros((6, 3)); beam[:, 1] = column
    for operation in (lambda b: thin(b), lambda b: SymplecticSplitIntegrator(zero_field).track(b),
                      lambda b: LorentzRK4Integrator(zero_field).track(b), compute_beam_statistics,
                      lambda b: track_multiturn_injection(b, [], kicker_model='off'),
                      lambda b: track_element_resolved_injection(b, [], kicker_model='off')):
        with pytest.raises(ValueError, match='indices.*1'):
            operation(beam)


@pytest.mark.parametrize('dtype', [complex, bool, object])
def test_nonnumeric_particle_storage_rejected(dtype):
    with pytest.raises(TypeError, match='real numeric'):
        validate_particle_array(np.zeros((6, 2), dtype=dtype))


@pytest.mark.parametrize('constructor', INTEGRATORS)
@pytest.mark.parametrize('count', [0, -1, 1.5, 2., True, np.bool_(True), np.nan, '2'])
def test_invalid_slice_counts(constructor, count):
    with pytest.raises(ValueError, match='n_slices'):
        constructor(zero_field, n_slices=count)


@pytest.mark.parametrize('constructor', INTEGRATORS)
@pytest.mark.parametrize('kwargs', [
    {'length_m': -1}, {'length_m': np.inf}, {'length_m': np.nan},
    {'scale_factor': -1}, {'scale_factor': np.inf}, {'scale_factor': np.nan},
    {'energy_GeV': 0}, {'energy_GeV': -1}, {'energy_GeV': np.inf}, {'energy_GeV': np.nan},
    {'energy_GeV': True}, {'particle_charge_C': 0}, {'particle_charge_C': np.nan},
    {'particle_charge_C': np.inf}, {'length_m': '1'},
])
def test_invalid_parameters(constructor, kwargs):
    with pytest.raises(ValueError, match=next(iter(kwargs))):
        constructor(zero_field, **kwargs)


@pytest.mark.parametrize('tracker', [track_multiturn_injection, track_element_resolved_injection])
@pytest.mark.parametrize('count', [0, -1, 1.5, 2., True, np.nan])
def test_invalid_turns_precede_lattice_access(tracker, count):
    with pytest.raises(ValueError, match='n_turns'):
        tracker(np.zeros((6, 2)), None, n_turns=count, kicker_model='off')


@pytest.mark.parametrize('tracker', [track_multiturn_injection, track_element_resolved_injection])
@pytest.mark.parametrize('name,value', [('energy_eV', np.nan), ('nkm_length_m', -1),
    ('particle_charge_C', 0), ('aperture_x_m', np.inf)])
def test_ring_parameters_precede_lattice_access(tracker, name, value):
    config = StorageRingInjectionConfig(); setattr(config, name, value)
    with pytest.raises(ValueError):
        tracker(np.zeros((6, 2)), None, config=config, kicker_model='off')


@pytest.mark.parametrize('constructor', INTEGRATORS)
def test_lost_columns_empty_beams_and_zero_scale(constructor):
    def unexpected(*args):
        pytest.fail('Inactive beam or zero field scale must not evaluate fields')
    beam = np.zeros((6, 4)); beam[:, 1] = np.nan; beam[0, 3] = np.nan
    beam[1, 0] = 0.002
    original = beam.copy()
    result = constructor(unexpected, length_m=0.5, scale_factor=0, n_slices=np.int64(2)).track(beam)
    np.testing.assert_array_equal(result[:, [1, 3]], original[:, [1, 3]])
    np.testing.assert_allclose(result[0, 0], 0.001, atol=1e-14, rtol=0)
    np.testing.assert_array_equal(beam, original)
    assert constructor(unexpected).track(np.empty((6, 0))).shape == (6, 0)
    np.testing.assert_array_equal(constructor(unexpected, length_m=0).track(beam), beam)
    np.testing.assert_array_equal(constructor(unexpected).track(beam[:, [1, 3]]), beam[:, [1, 3]])


@pytest.mark.parametrize('constructor', INTEGRATORS)
def test_uniform_field_sign_strength_and_scalar_broadcast(constructor):
    length = 0.3; by = 0.01
    for charge in (ELECTRON_CHARGE_C, -ELECTRON_CHARGE_C):
        result = constructor(lambda x, y, z: (by, 0.), length_m=length,
                             particle_charge_C=charge).track(np.zeros((6, 2)))
        expected = np.sign(charge) * by * length / compute_rigidity(4e9, charge)
        np.testing.assert_allclose(result[1], expected, atol=1e-14, rtol=0)
        np.testing.assert_allclose(result[0], expected * length / 2, atol=1e-14, rtol=0)


@pytest.mark.parametrize('constructor', INTEGRATORS)
@pytest.mark.parametrize('field', [lambda x, y, z: (np.nan, 0.), lambda x, y, z: (np.inf, 0.),
                                   lambda x, y, z: (np.zeros((2, 2)), 0.)])
def test_invalid_fields_rejected(constructor, field):
    with pytest.raises(ValueError):
        constructor(field).track(np.zeros((6, 2)))


class IdentityRing:
    def find_m66(self, **kwargs):
        return np.eye(6), None


def test_ring_lost_indices_empty_beam_and_at_loss_accounting():
    beam = np.zeros((6, 5)); beam[:, 0] = np.nan; beam[0, 2] = np.nan; beam[0, 3] = .02
    result = track_multiturn_injection(beam, IdentityRing(), n_turns=np.int64(2), kicker_model='off')
    assert result.metadata['initial_lost_indices'] == [0, 2]
    np.testing.assert_array_equal(result.final_beam[:, [0, 2]], beam[:, [0, 2]])
    assert result.n_particles == 5 and result.survived_particles == 3
    ring = at.Lattice([at.Aperture('LIMIT', [-.01, .01, -.01, .01])], energy=4e9)
    result = track_element_resolved_injection(beam, ring, n_turns=2, kicker_model='off')
    assert result.metadata['initial_lost_indices'] == [0, 2]
    assert result.survived_particles == 2
    assert len(result.loss_log) == 1
    assert result.loss_log[0]['particle_index'] == 3
    assert result.loss_log[0]['cause'] == 'at_tracking_loss'
    np.testing.assert_array_equal(result.final_beam[:, [0, 2]], beam[:, [0, 2]])
    for tracker, ring in [(track_multiturn_injection, None), (track_element_resolved_injection, [])]:
        result = tracker(np.empty((6, 0)), ring, n_turns=1, kicker_model='off')
        assert result.n_particles == 0 and result.survival_history == [0]
        assert result.final_beam.shape == (6, 0)


def test_thin_parameters_validated_even_for_empty_beams():
    for kwargs in ({'scale_factor': -1}, {'length_m': np.nan}, {'energy_GeV': 0}):
        with pytest.raises(ValueError):
            thin(np.empty((6, 0)), **kwargs)


@pytest.mark.parametrize('constructor,tolerance', [(SymplecticSplitIntegrator, 1e-9),
                                                   (LorentzRK4Integrator, 1e-14)])
def test_linear_field_matches_analytic_focusing_limit(constructor, tolerance):
    gradient = 1.0  # T/m; electron By=gradient*x gives x''=-k*x
    length = 0.5
    k = gradient / compute_rigidity(4e9)
    beam = np.zeros((6, 2)); beam[0] = [0.001, -0.002]; beam[1] = [0.0002, 0.0003]
    omega = np.sqrt(k)
    phase = omega * length
    expected_x = beam[0] * np.cos(phase) + beam[1] / omega * np.sin(phase)
    expected_xp = -beam[0] * omega * np.sin(phase) + beam[1] * np.cos(phase)
    result = constructor(lambda x, y, z: (gradient*x, np.zeros_like(y)),
                         length_m=length, n_slices=80).track(beam)
    np.testing.assert_allclose(result[0], expected_x, atol=tolerance, rtol=0)
    np.testing.assert_allclose(result[1], expected_xp, atol=tolerance, rtol=0)


def test_zero_length_configuration_roundtrip():
    config = StorageRingInjectionConfig(nkm_length_m=0)
    assert StorageRingInjectionConfig.from_json(config.to_json()) == config


def test_nonfinite_map_outputs_are_errors_not_losses():
    class OverflowRing:
        def find_m66(self, **kwargs):
            return np.eye(6) * 1e308, None
    beam = np.ones((6, 2)) * 10
    with np.errstate(over='ignore', invalid='ignore'):
        with pytest.raises(ValueError, match='nonfinite active'):
            track_multiturn_injection(beam, OverflowRing(), kicker_model='off')
