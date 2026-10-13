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


def lattice_for(strengths, config=None, integration_steps=40):
    """Build independent lattice with nine K values [m^-2]."""
    if not isinstance(integration_steps,int) or integration_steps<=0:raise ValueError('Positive integration step count required')
    k=np.asarray(strengths,dtype=float)
    if k.shape!=(9,) or not np.all(np.isfinite(k)):
        raise ValueError('Nine finite quadrupole strengths [m^-2] required')
    lat=create_bts_lattice(config or BTSConfig())
    for elem in lat:
        if hasattr(elem,'NumIntSteps'):elem.NumIntSteps=integration_steps
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


def apply_static(lattice, errors):
    """Apply independent fixed gradient, translation, roll and dipole field errors.

    Dipole geometry is fixed; PolynomB[0] represents additional curvature [m^-1].
    Energy jitter enters particle delta, without also rescaling fields/geometry.
    """
    for elem in lattice:
        if elem.FamName in QUADS:
            i=QUADS.index(elem.FamName)
            elem.K*=1+errors['gradient'][i]
            dx,dy=errors['offset'][i]
            elem.T1=np.array([-dx,0,-dy,0,0,0.])
            elem.T2=-elem.T1
            r=np.eye(6);c=np.cos(errors['roll'][i]);s=np.sin(errors['roll'][i])
            for a,b in [(0,2),(1,3)]:r[a,a]=r[b,b]=c;r[a,b]=s;r[b,a]=-s
            elem.R1=r;elem.R2=r.T
        if hasattr(elem,'BendingAngle'):
            elem.PolynomB[0]=elem.BendingAngle/elem.Length*errors['dipole'][elem.FamName]
    return lattice


def draw_static(rng, lattice, amplitude=1.):
    """Independent untruncated normal parametric installation errors."""
    return {'gradient':rng.normal(0,.001*amplitude,9),'offset':rng.normal(0,.0001*amplitude,(9,2)),
            'roll':rng.normal(0,.0005*amplitude,9),'dipole':{e.FamName:float(rng.normal(0,.0005*amplitude)) for e in lattice if hasattr(e,'BendingAngle')}}


def _focusing(k, length):
    if abs(k)<1e-15:return np.array([[1.,length],[0.,1.]])
    w=np.sqrt(abs(k));t=w*length
    c,s=(np.cos(t),np.sin(t)) if k>0 else (np.cosh(t),np.sinh(t))
    return np.array([[c,s/w],[-np.sign(k)*w*s,c]])


def independent_element_map(elem):
    """Independent hard-edge affine 5D map (x,px,y,py,delta).

    Exact thick quadrupoles, sector bends with edge focusing, fixed-field dipole
    errors and AT translations/rotations. Linearization about delta=0;
    excludes second-order chromatic/path-length effects. No AT map calls.
    """
    m=np.eye(5);b=np.zeros(5);length=elem.Length
    if hasattr(elem,'BendingAngle'):
        h=elem.BendingAngle/length
        angle=h*length
        if abs(h)>1e-15:
            m[:2,:2]=_focusing(h*h,length)
            m[0,4]=(1-np.cos(angle))/h;m[1,4]=np.sin(angle)
        else:m[0,1]=length
        m[2,3]=length
        e1=np.eye(5);e2=np.eye(5)
        for e,edge in [(e1,elem.EntranceAngle),(e2,elem.ExitAngle)]:
            e[1,0]=h*np.tan(edge);e[3,2]=-h*np.tan(edge)
        extra=elem.PolynomB[0]
        if abs(h)>1e-15:b[:2]=-extra*np.array([(1-np.cos(angle))/(h*h),np.sin(angle)/h])
        else:b[0]=-extra*length*length/2;b[1]=-extra*length
        m=e2@m@e1;b=e2@b
    elif hasattr(elem,'K'):
        m[:2,:2]=_focusing(elem.K,length);m[2:4,2:4]=_focusing(-elem.K,length)
    else:m[0,1]=m[2,3]=length
    r1=getattr(elem,'R1',np.eye(6))[:5,:5];r2=getattr(elem,'R2',np.eye(6))[:5,:5]
    t1=getattr(elem,'T1',np.zeros(6))[:5];t2=getattr(elem,'T2',np.zeros(6))[:5]
    return r2@m@r1, r2@(m@r1@t1+b)+t2


def independent_maps(lattice):
    """Return cumulative 5D matrices and centroids at all element exits."""
    m=np.eye(5);b=np.zeros(5);maps=[m.copy()];orbits=[b.copy()]
    for elem in lattice:
        e,c=independent_element_map(elem);b=e@b+c;m=e@m;maps.append(m.copy());orbits.append(b.copy())
    return np.array(maps),np.array(orbits)


def tracked_linear_maps(lattice, step=1e-7):
    """AT central-difference 5D map/orbit at every element exit; no linopt calls."""
    probes=np.zeros((6,11),order='F')
    for i in range(5):probes[i,1+2*i]=step;probes[i,2+2*i]=-step
    out=at.lattice_track(lattice,probes,nturns=1,refpts=np.arange(len(lattice)+1))[0][:,:,:,0]
    if not np.all(np.isfinite(out)):raise ValueError('Invalid/lost map probes')
    maps=np.stack([(out[:5,1+2*i,:]-out[:5,2+2*i,:])/(2*step) for i in range(5)],axis=-1).transpose(1,0,2)
    return maps,out[:5,0,:].T


def clearance_profile(lattice, beam, centroid=None, beta_factors=(1.,1.)):
    """Linear coupled five-sigma projected clearance [m] at model apertures.

    Uses independent hard-edge maps; validated separately against AT tracking.
    """
    maps,orbit=independent_maps(lattice);cov=beam.covariance(beta_factors)[:5,:5]
    centroid=np.zeros(5) if centroid is None else np.asarray(centroid)
    if centroid.shape!=(5,) or not np.all(np.isfinite(centroid)):raise ValueError('Finite 5D centroid required')
    means=orbit+np.einsum('nij,j->ni',maps,centroid)
    covs=maps@cov@maps.transpose(0,2,1)
    sigmas=np.sqrt(np.maximum(0,np.diagonal(covs,axis1=1,axis2=2)))
    margins=[]
    for i,elem in enumerate(lattice):
        if hasattr(elem,'Limits'):
            limits=np.array(elem.Limits).reshape(2,2)
            for axis,j in enumerate([0,2]):
                c=min(limits[axis,1]-means[i+1,j],means[i+1,j]-limits[axis,0])-beam.coverage_sigma*sigmas[i+1,j]
                margins.append({'index':i,'name':elem.FamName,'axis':axis,'clearance_m':float(c)})
    return {'minimum_m':min(r['clearance_m'] for r in margins),'stations':margins,'sigma_m':sigmas[:,[0,2]].tolist(),'centroid_m':means[:,[0,2]].tolist()}
