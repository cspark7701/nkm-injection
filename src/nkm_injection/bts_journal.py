"""Explicit BTS journal study: SI units and parametric machine assumptions.

Coordinates are AT (x, px, y, py, delta, ct): m, rad, m, rad, 1, m.
No ring boundary derivation or measured chamber/hardware specification is implied.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np
import at
from .bts_lattice import BTSConfig, create_bts_lattice
from .optics import DEFAULT_BTS_ENTRANCE_TWISS, DEFAULT_BTS_TARGET_TWISS

QUADS = ('q11','q12','q13','q21','q22','q23','q31','q32','q33')
TARGET = np.array([2.336495,4.256241,-0.016335,0.017772,0.080868,0.047472])
SCALES = np.array([.05,.05,.01,.01,.002,.001])
LOWER = np.array([-2.5,-3,-3,-3,-3,-3,-3,-3,-2.5])
UPPER = -LOWER

@dataclass(frozen=True)
class JournalBeam:
    """Untruncated Gaussian betatron beam plus independent momentum spread."""
    emit_x_m_rad: float = 7.67e-9
    emit_y_m_rad: float = .767e-9
    sigma_delta: float = .00106
    coverage_sigma: float = 5.0

    def validate(self):
        if not all(np.isfinite(v) and v > 0 for v in asdict(self).values()):
            raise ValueError('Beam emittances, spread and coverage must be finite and positive')

    def covariance(self, beta_factors=(1.0,1.0)):
        """Return full 6x6 covariance; no initial coupling, ct fixed to zero."""
        self.validate()
        factors=np.asarray(beta_factors,dtype=float)
        if factors.shape!=(2,) or np.any(factors<=0) or not np.all(np.isfinite(factors)):
            raise ValueError('Two positive finite entrance beta factors required')
        tw=DEFAULT_BTS_ENTRANCE_TWISS
        cov=np.zeros((6,6))
        for i,b,a,e,f in [(0,tw.beta_x,tw.alpha_x,self.emit_x_m_rad,factors[0]),(2,tw.beta_y,tw.alpha_y,self.emit_y_m_rad,factors[1])]:
            b*=f;cov[i:i+2,i:i+2]=e*np.array([[b,-a],[-a,(1+a*a)/b]])
        dispersion=np.array([tw.disp_x,tw.disp_px,tw.disp_y,tw.disp_py,1.,0.])
        return cov+self.sigma_delta**2*np.outer(dispersion,dispersion)


def lattice_for(strengths, config=None):
    """Build independent lattice with nine K values [m^-2]."""
    k=np.asarray(strengths,dtype=float)
    if k.shape!=(9,) or not np.all(np.isfinite(k)):
        raise ValueError('Nine finite quadrupole strengths [m^-2] required')
    lat=create_bts_lattice(config or BTSConfig())
    for elem in lat:
        if elem.FamName in QUADS: elem.K=float(k[QUADS.index(elem.FamName)])
    return lat


def geometry(lattice):
    """Record actual element entrance/exit positions and aperture limits [m]."""
    s=0.; rows=[]
    for index,elem in enumerate(lattice):
        row={'index':index,'name':elem.FamName,'s_in_m':s,'s_out_m':s+elem.Length,'length_m':elem.Length,'pass_method':elem.PassMethod}
        if hasattr(elem,'Limits'):row['limits_m']=np.asarray(elem.Limits).tolist()
        if hasattr(elem,'BendingAngle'):row['bend_rad']=elem.BendingAngle
        rows.append(row);s+=elem.Length
    return rows
