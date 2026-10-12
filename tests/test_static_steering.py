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
