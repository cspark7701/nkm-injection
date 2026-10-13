"""Declared KLS chamber scenarios; half apertures and longitudinal positions in m.

Octagon corners and NKM ceramic chamber are unspecified. Rectangle/ellipse
profiles bracket the given bounding dimensions. Closed-IVU assignments are a
declared selection of ordinary straights, not a surveyed installation map.

``nkm_half_x_m``/``nkm_half_y_m`` apply to the injection straight outside the
magnet. ``nkm_magnet_half_x_m``/``nkm_magnet_half_y_m`` (round 3) define a flat
vacuum chamber inside the magnet, between the conductors; it is checked by the
kicker per slice and must leave ``NKM_CONDUCTOR_ALLOWANCE_M`` (wall plus
conductor radius) below the inner wires. ``None`` keeps the round-2 model.
"""
from dataclasses import dataclass
from typing import Optional

import numpy as np
import at

# Wall thickness plus conductor radius between the chamber aperture and a conductor centre (m). The 1.5 mm value is
# the allowance used for the eight-conductor ALS NLK design (Sun et al., PRAB 23, 010702, 2020).
NKM_CONDUCTOR_ALLOWANCE_M = 1.5e-3
# The two 0.2625 m halves of the magnet in the prepared ring (re-ordered to start at the NKM centre).
NKM_MAGNET_FAMILIES = ('NKM_H1', 'NKM_H2')


@dataclass(frozen=True)
class ChamberProfile:
    arc_half_x_m: float = .012
    arc_half_y_m: float = .009
    centre_bend_half_y_m: float = .00487
    nkm_half_x_m: float = .030
    nkm_half_y_m: float = .015
    ivu_half_y_m: float = .009
    ivu_count: int = 19
    shape: str = 'rectangle'
    nkm_magnet_half_x_m: Optional[float] = None
    nkm_magnet_half_y_m: Optional[float] = None

    def validate(self):
        dims=(self.arc_half_x_m,self.arc_half_y_m,self.centre_bend_half_y_m,
              self.nkm_half_x_m,self.nkm_half_y_m,self.ivu_half_y_m)
        if not np.isfinite(dims).all() or min(dims)<=0 or self.shape not in ('rectangle','ellipse'):
            raise ValueError('Invalid chamber dimensions or shape')
        if type(self.ivu_count) is not int or self.ivu_count<0: raise ValueError('Invalid IVU count')
        if (self.nkm_magnet_half_x_m is None)!=(self.nkm_magnet_half_y_m is None):
            raise ValueError('In-magnet NKM chamber needs both half-apertures')
        if self.nkm_magnet_half_y_m is not None and min(self.nkm_magnet_half_x_m,self.nkm_magnet_half_y_m)<=0:
            raise ValueError('Invalid in-magnet NKM chamber')

    def validate_against_wires(self, geometry, allowance_m=NKM_CONDUCTOR_ALLOWANCE_M):
        """Reject an in-magnet chamber that reaches within ``allowance_m`` of any conductor centre.

        A flat chamber of half-height h passes between the wire rows if every wire satisfies |y_w| >= h + allowance;
        wires beside it (|x_w| > half-width + allowance) are also admissible."""
        if self.nkm_magnet_half_y_m is None: return
        hx,hy=self.nkm_magnet_half_x_m,self.nkm_magnet_half_y_m
        for xw,yw in geometry.wire_positions():
            if abs(yw)<hy+allowance_m and abs(xw)<hx+allowance_m:
                raise ValueError(f'NKM chamber {2e3*hx:.1f} x {2e3*hy:.1f} mm reaches wire at ({1e3*xw:.2f}, {1e3*yw:.2f}) mm')

    def kicker_kwargs(self):
        """Keyword arguments for FilamentNKMKicker's in-magnet chamber."""
        return {'chamber_half_x_m':self.nkm_magnet_half_x_m,'chamber_half_y_m':self.nkm_magnet_half_y_m}


def nkm_chamber_half_height(geometry, allowance_m=NKM_CONDUCTOR_ALLOWANCE_M):
    """Largest flat-chamber half-height (m) that keeps ``allowance_m`` below the lowest wire row."""
    return float(np.min(np.abs(geometry.wire_positions()[:,1])))-allowance_m


def apply_chamber(lattice, profile=ChamberProfile(), septum_edge_x_m=-.016):
    """Copy lattice and apply chamber checks, preserving total length and magnet order.

    Split the two 2.94 m LM11 drifts around each selected straight centre into
    outer 1.44 m and inner 1.5 m pieces. Check the gap at its entrance, centre and
    exit; no magnet is inserted or moved. Arc/magnet limits apply at every element.
    """
    profile.validate();r=lattice.deepcopy();ids=[];assignments=[]
    for i,e in enumerate(r):
        if e.FamName=='SectionStart' and r[(i-2)%len(r)].FamName=='LM11' and r[(i+1)%len(r)].FamName=='LM11':
            ids.append(i)
    if len(ids)<profile.ivu_count: raise ValueError('Too few identified ordinary ID straights')
    selected=ids[:profile.ivu_count]
    expanded=[]
    for i,e in enumerate(r):
        if (i+2)%len(r) in selected and e.FamName=='LM11':
            outer=e.deepcopy();outer.Length=e.Length-1.5
            inner=e.deepcopy();inner.Length=1.5;inner.FamName='LM11_IVU'
            expanded.extend([outer,at.Marker('IVUEntrance'),inner])
        elif (i-1)%len(r) in selected and e.FamName=='LM11':
            inner=e.deepcopy();inner.Length=1.5;inner.FamName='LM11_IVU'
            outer=e.deepcopy();outer.Length=e.Length-1.5
            expanded.extend([inner,at.Marker('IVUExit'),outer])
        elif i in selected or (i+1)%len(r) in selected:
            centre=e.deepcopy();centre.FamName=e.FamName+'_IVUCentre';expanded.append(centre)
        else: expanded.append(e)
    r=at.Lattice(expanded,energy=lattice.energy,periodicity=1,name='declared_KLS_chamber')
    for i,e in enumerate(r):
        wide=e.FamName.startswith(('LH','QH','NKM')) or e.FamName=='BPMHB'
        hx=profile.nkm_half_x_m if wide else profile.arc_half_x_m
        hy=profile.nkm_half_y_m if wide else profile.arc_half_y_m
        region='nkm_straight_assumed' if wide else 'regular_arc'
        if e.FamName=='CENT': hy=profile.centre_bend_half_y_m;region='centre_bend'
        if e.FamName in NKM_MAGNET_FAMILIES and profile.nkm_magnet_half_y_m is not None:
            hx,hy=profile.nkm_magnet_half_x_m,profile.nkm_magnet_half_y_m;region='nkm_magnet_chamber'
        if 'IVU' in e.FamName:
            hy=min(hy,profile.ivu_half_y_m);region='ivu_3m_segment'
        for attr in ('RApertures','EApertures'):
            if hasattr(e,attr): delattr(e,attr)
        if profile.shape=='ellipse' and not wide and region!='ivu_3m_segment': e.EApertures=np.array([hx,hy])
        else: e.RApertures=np.array([-hx,hx,-hy,hy])
        if e.FamName=='NKMUPRING': e.RApertures[0]=septum_edge_x_m
        assignments.append({'index':i,'family':e.FamName,'region':region,'half_x_m':hx,'half_y_m':hy})
    return r,{'assignments':assignments,'ivu_centre_indices':selected,
              'ivu_assignment':'first 19 identified LM11/SectionEnd/SectionStart/LM11 ordinary straights; scenario',
              'ivu_check':'3 m gap with checks at entrance, centre and exit; LM11 drifts split without moving magnets',
              'octagon':'rectangle upper / ellipse inner bound on stated full dimensions; corners unspecified'}
