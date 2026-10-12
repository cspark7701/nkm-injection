from dataclasses import dataclass
import at
import numpy as np
import pytest
from nkm_injection.linear_ring_reference import linearize_ring


@dataclass
class Prepared:
    ring_c: object
    orbit6: np.ndarray
    septum_index: int


class TangentSource(list):
    energy=4e9
    def find_orbit6(self,refpts):return np.zeros(6),np.zeros((len(self)+1,6))
    def find_m66(self,refpts,orbit):
        prefix=[np.eye(6)]
        for e in self:prefix.append(e.M66@prefix[-1])
        return prefix[-1],np.array(prefix)


@pytest.mark.parametrize('elliptical',[False,True])
def test_affine_reference_enforces_apertures_and_preserves_tangent(elliptical):
    matrix=np.eye(6);matrix[0,1]=.3;matrix[2,3]=.3
    element=at.M66('NativeTangent',matrix);element.Length=.3
    if elliptical:element.EApertures=np.array([.01,.005])
    else:element.RApertures=np.array([-.01,.01,-.005,.005])
    source=TangentSource([element]);linear=linearize_ring(Prepared(source,np.zeros(6),0))
    beam=np.zeros((6,2));beam[0]=[.001,.02];beam[1,0]=.0001
    tracked,_,info=linear.ring_c.track(beam,nturns=1,losses=True)
    assert info['loss_map']['islost'].tolist()==[False,True]
    assert np.allclose(tracked[:,0,0,0],matrix@beam[:,0])
    assert sum(e.Length for e in linear.ring_c)==pytest.approx(.3)
