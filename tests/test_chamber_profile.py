import at
import numpy as np
import pytest
from nkm_injection.chamber import ChamberProfile,apply_chamber


def test_ivu_segments_preserve_length_and_magnet_order():
    r=at.Lattice([at.Drift('LM11',2.94),at.Marker('SectionEnd'),at.Marker('SectionStart'),
                  at.Drift('LM11',2.94),at.Quadrupole('Q',.2,1.2),at.Dipole('CENT',.2,.01)],energy=4e9)
    ch,meta=apply_chamber(r,ChamberProfile(ivu_count=1,ivu_half_y_m=.0025))
    assert ch.circumference==pytest.approx(r.circumference)
    assert [e.FamName for e in ch if isinstance(e,at.Quadrupole)]==['Q']
    assert sum(e.Length for e in ch if e.FamName=='LM11_IVU')==3.
    assert all(e.RApertures[3]==.0025 for e in ch if 'IVU' in e.FamName)
    assert not hasattr(r[-1],'RApertures')
    assert ch[-1].RApertures[3]==.00487


def test_invalid_shapes_and_straight_assignments_fail():
    r=at.Lattice([at.Drift('D',1.)],energy=4e9)
    with pytest.raises(ValueError):apply_chamber(r,ChamberProfile())
    with pytest.raises(ValueError):apply_chamber(r,ChamberProfile(ivu_count=0,shape='octagon'))


def test_rectangular_and_elliptic_bounds_differ_at_corner():
    r=at.Lattice([at.Drift('D',1.)],energy=4e9)
    b=np.zeros((6,1));b[0]=.011;b[2]=.008
    rect,_=apply_chamber(r,ChamberProfile(ivu_count=0));ell,_=apply_chamber(r,ChamberProfile(ivu_count=0,shape='ellipse'))
    _,_,rloss=rect.track(b.copy(),nturns=1,losses=True)
    _,_,eloss=ell.track(b.copy(),nturns=1,losses=True)
    assert not rloss['loss_map']['islost'][0] and eloss['loss_map']['islost'][0]
