"""Vector straight-line filament kick map and finite-length slicing (m, rad)."""
import numpy as np
from .wire_field import brho_T_m


def integrated_filament_kicks(x, y, geometry, energy_eV=4e9, scale=1., polarity=1,
                             wire_offsets_m=None, loop_current_relative=None):
    """Infinite-span integral of closed-filament field; both kick components in rad.

    Integrating each longitudinal segment and both end connectors over s gives
    the straight-wire transverse kernel times the longitudinal wire length.
    The vertical component carries the physical minus sign. No iron or chamber.
    """
    x,y=np.broadcast_arrays(np.asarray(x,float),np.asarray(y,float))
    if not np.isfinite(x).all() or not np.isfinite(y).all() or energy_eV<=0:
        raise ValueError('Finite positions and positive energy required')
    kx=np.zeros_like(x);ky=np.zeros_like(y)
    gain=2e-7*geometry.current_A*2*geometry.half_length_m*scale*polarity/brho_T_m(energy_eV)
    offsets=np.zeros((8,2)) if wire_offsets_m is None else np.asarray(wire_offsets_m,float)
    currents=np.zeros(4) if loop_current_relative is None else np.asarray(loop_current_relative,float)
    if offsets.shape!=(8,2) or currents.shape!=(4,) or not np.isfinite(offsets).all() or not np.isfinite(currents).all():
        raise ValueError('Expected finite (8,2) wire offsets in m and (4,) relative loop currents')
    for j,(sx,sy) in enumerate(((1,1),(-1,1),(-1,-1),(1,-1))):
        for inner,(wx,wy,direction) in enumerate(((sx*geometry.x1_m,sy*geometry.y1_m,1),
                                                 (sx*geometry.x2_m,sy*geometry.y2_m,-1))):
            wx+=offsets[2*j+inner,0];wy+=offsets[2*j+inner,1]
            dx,dy=x-wx,y-wy;r2=dx*dx+dy*dy
            if np.any(r2==0): raise ValueError('Coordinate on filament')
            kx+=direction*gain*(1+currents[j])*dx/r2;ky+=direction*gain*(1+currents[j])*dy/r2
    return kx,ky


def sliced_vector_map(coordinate, geometry, *, energy_eV=4e9, scale=1., polarity=1, slices=640):
    """Distribute a vector map uniformly over the wire length; return (6,) at centre.

    This retains self-deflection and physical vertical kick while approximating
    the longitudinal field density. It is a comparison model, not an exact field.
    """
    b=np.asarray(coordinate,float).copy()
    if b.shape!=(6,) or not np.isfinite(b).all() or b[4]<=-1 or type(slices) is not int or slices<1:
        raise ValueError('Invalid coordinate or slice count')
    length=2*geometry.half_length_m;ds=length/slices
    def drift(distance):
        xp,yp=b[1]/(1+b[4]),b[3]/(1+b[4]);b[0]+=distance*xp;b[2]+=distance*yp
        b[5]+=distance*.5*(xp*xp+yp*yp)
    drift(-length/2)
    for _ in range(slices):
        drift(ds/2)
        kx,ky=integrated_filament_kicks(b[0],b[2],geometry,energy_eV,scale,polarity)
        b[1]+=float(kx)/slices;b[3]+=float(ky)/slices;drift(ds/2)
    drift(-length/2)
    return b
