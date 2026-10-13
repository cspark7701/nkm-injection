import numpy as np
import pytest
from nkm_injection.bts_journal import lattice_for,JournalBeam,clearance_profile
from nkm_injection.bts_lattice import BTSConfig
from nkm_injection.bts_round2 import station_record,centred_maps,set_regime


def test_variance_decomposition_preserves_original_clearance():
    lattice=lattice_for(BTSConfig().quad_strengths_list)
    beam=JournalBeam();centroid=np.array([.0005,.0002,0,0,.001])
    record=station_record(lattice,beam,centroid,(1.05,.95))
    original=clearance_profile(lattice,beam,centroid,(1.05,.95))
    assert record['minimum_m']==pytest.approx(original['minimum_m'],abs=1e-14)
    for row in record['stations']:
        assert row['sigma_m']**2==pytest.approx(row['betatron_variance_m2']+row['dispersive_variance_m2'],abs=1e-20)


def test_centred_map_moment_probes_are_not_censored_by_apertures():
    lattice=lattice_for(BTSConfig().quad_strengths_list)
    centre=np.array([.04,0.,0.,0.,0.])
    maps,means=centred_maps(lattice,centre)
    np.testing.assert_allclose(maps[0],np.eye(5),atol=1e-10)
    np.testing.assert_allclose(means[0],centre)
    assert np.all(np.isfinite(maps)) and lattice[1].Limits[1]<.04
    with pytest.raises(ValueError):centred_maps(lattice,[0,0])


def test_hypothetical_restriction_leaves_original_geometry_unchanged():
    lattice=lattice_for(BTSConfig().quad_strengths_list)
    trial=set_regime(lattice,{'22':[.003,.0015]})
    np.testing.assert_allclose(trial[22].Limits,[-.003,.003,-.0015,.0015])
    np.testing.assert_allclose(lattice[22].Limits,[-.03,.03,-.03,.03])
    assert sum(e.Length for e in trial)==sum(e.Length for e in lattice)


def test_gaussian_quadrature_reproduces_drift_moments():
    import at
    from nkm_injection.bts_round2 import quadrature_moments
    beam=JournalBeam();centre=np.array([.002,.0001,0,0,.001])
    lat=at.Lattice([at.Drift('d',2.)],energy=4e9)
    mean,sigma=quadrature_moments(lat,beam,centre,order=5)
    # Exact drift tracks x -> x + L px/(1+delta) at leading order;
    # entrance moments are exact Gaussian quadrature identities.
    np.testing.assert_allclose(mean[0],centre,atol=1e-16)
    np.testing.assert_allclose(sigma[0],np.sqrt(np.diag(beam.covariance())[:5]),rtol=1e-10)
    assert np.all(np.isfinite(mean)) and np.all(np.isfinite(sigma))
