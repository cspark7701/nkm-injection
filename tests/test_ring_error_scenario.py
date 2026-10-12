from dataclasses import replace
import at
import numpy as np
from nkm_injection.ring_error_scenario import RingErrorScenario,apply_errors,correct_orbit


def small_lattice():
    return at.Lattice([at.Marker('GirderStart'),at.Quadrupole('Q',.2,1.2),
                       at.Sextupole('S',.1,2.),at.Marker('GirderEnd')],energy=4e9)


def test_seeded_errors_are_repeatable_and_do_not_mutate_source():
    r=small_lattice();a,ra=apply_errors(r,42);b,rb=apply_errors(r,42)
    assert ra==rb and ra['girder_count']==1
    assert np.array_equal(a[1].PolynomB,b[1].PolynomB)
    assert not np.array_equal(a[1].PolynomB,r[1].PolynomB)
    assert not hasattr(r[1],'T1')


def test_error_ramp_preserves_the_realization():
    c=RingErrorScenario();r=small_lattice()
    full,rec=apply_errors(r,42,c)
    half,half_rec=apply_errors(r,42,replace(c,girder_offset_std_m=c.girder_offset_std_m/2,
                                         magnet_offset_std_m=c.magnet_offset_std_m/2))
    assert np.allclose(half[1].T1,full[1].T1/2)
    assert half_rec['magnets'][0]['dx_m']==rec['magnets'][0]['dx_m']/2


def test_svd_correction_bounds_and_residual_gate(monkeypatch):
    from nkm_injection import ring_error_scenario as mod
    r=at.Lattice([at.Corrector('HVCOR',0.,[0.,0.])],energy=4e9)
    monkeypatch.setattr(mod,'bpm_orbit',lambda ring,bpms:np.array([.003,.002])+ring[0].KickAngle)
    out=correct_orbit(r,[0],[0],np.eye(2),iterations=2)
    assert not out['feasible'] and out['termination']=='iteration limit'
    assert np.all(np.abs(r[0].KickAngle)<=.001)
