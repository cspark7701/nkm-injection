"""Element-resolved affine one-turn reference about the 6-D closed orbit (m, rad)."""
import at
import numpy as np


def linearize_ring(prepared):
    """Return a PreparedRing with affine linear elements and the same aperture checks.

    Each map is the local tangent of the native lattice at its closed orbit.
    Physical elements are replaced by M66 maps; physical lengths and relative
    family order are retained. Zero-length drifts enforce entrance/exit apertures
    because AT's M66Pass ignores aperture attributes. Nonlinear acceptance
    is deliberately absent. This is a comparison backend, not capture evidence.
    """
    r=prepared.ring_c;refs=np.arange(len(r)+1,dtype=np.uint32)
    _,orbit=r.find_orbit6(refpts=refs)
    _,prefix=r.find_m66(refpts=refs,orbit=prepared.orbit6)
    elements=[];septum_index=None
    for i,e in enumerate(r):
        matrix=np.linalg.solve(prefix[i].T,prefix[i+1].T).T
        item=at.M66(e.FamName,matrix)
        item.Length=e.Length;item.T1=-np.asarray(orbit[i],float);item.T2=np.asarray(orbit[i+1],float)
        aperture=at.Drift(e.FamName+'_AP',0.)
        for attr in ('RApertures','EApertures'):
            if hasattr(e,attr):setattr(aperture,attr,np.array(getattr(e,attr),copy=True))
        has_aperture=any(hasattr(aperture,attr) for attr in ('RApertures','EApertures'))
        if i==prepared.septum_index:septum_index=len(elements)
        if has_aperture:elements.append(aperture)
        elements.append(item)
        if has_aperture:elements.append(aperture.deepcopy())
    linear=at.Lattice(elements,energy=r.energy,periodicity=1,name='affine_linear_ring_reference')
    from dataclasses import replace
    return replace(prepared,ring_c=linear,septum_index=septum_index)
