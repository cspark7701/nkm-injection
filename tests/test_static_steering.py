import numpy as np
import pytest
from nkm_injection.steering import subtract_static_horizontal_reference


def test_static_translation_preserves_jitter_spread_and_other_coordinates():
    rng=np.random.default_rng(42)
    shot=rng.normal(size=(6,20))*.001
    static=np.array([.002,.0004,.0001,.0002,0.,0.])[:,None]
    beam=shot+static
    covariance=np.cov(beam[:2])
    other=beam[2:].copy()
    assert subtract_static_horizontal_reference(beam,static)==[.002,.0004]
    assert np.allclose(beam[:2],shot[:2])
    assert np.allclose(np.cov(beam[:2]),covariance)
    assert np.array_equal(beam[2:],other)


def test_lost_reference_is_an_explicit_error():
    with pytest.raises(ValueError):
        subtract_static_horizontal_reference(np.zeros((6,2)),np.full((6,1),np.nan))


def test_two_plane_steering_removes_vertical_static_only():
    from nkm_injection.steering import subtract_static_reference
    rng=np.random.default_rng(7)
    shot=rng.normal(size=(6,20))*.001
    static=np.array([.002,.0004,.0009,.00008,.0003,0.])[:,None]
    beam=shot+static
    assert subtract_static_reference(beam,static,'xy')==[.002,.0004,.0009,.00008]
    assert np.allclose(beam[:4],shot[:4])
    assert np.array_equal(beam[4:],(shot+static)[4:])
    with pytest.raises(ValueError):
        subtract_static_reference(beam,static,'y')
