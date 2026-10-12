from dataclasses import replace
import numpy as np
import pytest
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.trajectory_reference import integrate_reference
from nkm_injection.wire_field import FilamentNKMKicker


def test_zero_field_referred_to_centre_is_identity():
    cfg=replace(InjectionStudyConfig(), field_scale=0.)
    b=np.array([-.008,.005,.001,.0002,.002,.003])
    assert np.allclose(integrate_reference(cfg,b),b,rtol=0,atol=1e-14)


def test_off_midplane_map_converges_to_independent_reference():
    cfg=replace(InjectionStudyConfig(),field_scale=.85)
    b=np.array([-.0085,.00485,.001,.0002,.002,0.])
    ref=integrate_reference(cfg,b)
    errors=[]
    for n in (320,1280):
        beam=b[:,None].copy(); FilamentNKMKicker(cfg,n_slices=n).apply(beam,0.)
        errors.append(np.linalg.norm(beam[:4,0]-ref[:4]))
    assert errors[1] < errors[0] and errors[1] < 1e-8


def test_reference_rejects_invalid_coordinates():
    with pytest.raises(ValueError): integrate_reference(InjectionStudyConfig(),np.zeros((6,1)))
    with pytest.raises(ValueError): integrate_reference(InjectionStudyConfig(),[0,0,0,0,-1,0])
