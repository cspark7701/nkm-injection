"""Declared KLS chamber scenarios; half apertures and longitudinal positions in m.

Octagon corners and NKM ceramic chamber are unspecified. Rectangle/ellipse
profiles bracket the given bounding dimensions. Closed-IVU assignments are a
declared selection of ordinary straights, not a surveyed installation map.
"""
from dataclasses import dataclass
import numpy as np
import at


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

    def validate(self):
        dims=(self.arc_half_x_m,self.arc_half_y_m,self.centre_bend_half_y_m,
              self.nkm_half_x_m,self.nkm_half_y_m,self.ivu_half_y_m)
        if not np.isfinite(dims).all() or min(dims)<=0 or self.shape not in ('rectangle','ellipse'):
            raise ValueError('Invalid chamber dimensions or shape')
        if type(self.ivu_count) is not int or self.ivu_count<0: raise ValueError('Invalid IVU count')


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
