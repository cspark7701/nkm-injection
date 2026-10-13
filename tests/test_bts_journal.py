import numpy as np
import pytest
import at
from nkm_injection.bts_journal import (JournalBeam,lattice_for,independent_maps,tracked_linear_maps,apply_static,draw_static,clearance_profile,QUADS)
from nkm_injection.bts_lattice import BTSConfig


def test_independent_bend_dispersion_and_edge_maps():
    lat=lattice_for(BTSConfig().quad_strengths_list)
    analytic,_=independent_maps(lat);tracked,_=tracked_linear_maps(lat)
    np.testing.assert_allclose(analytic,tracked,rtol=2e-5,atol=2e-6)


def test_translations_drive_orbit_and_rolls_drive_coupling():
    lat=lattice_for(BTSConfig().quad_strengths_list)
    errors=draw_static(np.random.default_rng(17),lat)
    lat=apply_static(lat,errors)
    maps,orbit=independent_maps(lat);amaps,aorbit=tracked_linear_maps(lat)
    np.testing.assert_allclose(maps,amaps,rtol=3e-3,atol=1e-3)
    np.testing.assert_allclose(orbit,aorbit,rtol=5e-3,atol=2e-6)
    assert abs(orbit[-1,0])+abs(orbit[-1,2])>1e-6
    assert np.linalg.norm(maps[-1,:2,2:4])>1e-5


def test_zero_fields_are_drift_and_covariance_has_dispersion():
    lat=lattice_for(np.zeros(9))
    for elem in lat:
        if hasattr(elem,'BendingAngle'):elem.BendingAngle=elem.EntranceAngle=elem.ExitAngle=0.
    maps,_=independent_maps(lat)
    assert maps[-1,0,1]==pytest.approx(21.789)
    assert maps[-1,2,3]==pytest.approx(21.789)
    cov=JournalBeam().covariance();assert cov[0,4]>0
    assert np.linalg.eigvalsh(cov).min()>-1e-18
    with pytest.raises(ValueError):JournalBeam().covariance((-1,1))


def test_loss_location_at_entrance_and_transmission_shape():
    lat=lattice_for(BTSConfig().quad_strengths_list)
    particles=np.zeros((6,2),order='F');particles[0,0]=.03
    out=at.lattice_track(lat,particles,nturns=1,refpts=np.arange(len(lat)+1))[0]
    assert out.shape==(6,2,len(lat)+1,1)
    lost=np.flatnonzero(~np.isfinite(out[0,0,:,0]))
    assert lost[0]==2
    assert np.isfinite(out[0,1,-1,0])
    assert clearance_profile(lat,JournalBeam())['minimum_m']>0
