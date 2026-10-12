"""Selected corrected-ring scenario. Lengths m, angles rad, multipoles AT units."""
from dataclasses import dataclass
import numpy as np
import at
from scipy.linalg import svd


@dataclass(frozen=True)
class RingErrorScenario:
    girder_offset_std_m: float = 30e-6
    magnet_offset_std_m: float = 30e-6
    roll_std_rad: float = 100e-6
    gradient_rel_std: float = 5e-4
    sextupole_rel_std: float = 1e-3
    skew_quad_relative_std: float = 1e-4
    max_corrector_rad: float = .001
    svd_relative_cutoff: float = .001
    orbit_tolerance_m: float = 20e-6
    tune_tolerance: float = 1e-5


def apply_errors(ring, seed, config=RingErrorScenario()):
    """Copy lattice; add correlated girder and independent magnet shifts/roll/multipoles."""
    r=ring.deepcopy()
    rng=np.random.default_rng([int(seed),5505])
    girder=np.zeros(2);record=[];ng=0
    for i,e in enumerate(r):
        if e.FamName=='GirderStart': girder=rng.normal(0,config.girder_offset_std_m,2);ng+=1
        if not isinstance(e,(at.Quadrupole,at.Sextupole,at.Dipole)): continue
        offset=girder+rng.normal(0,config.magnet_offset_std_m,2)
        roll=float(rng.normal(0,config.roll_std_rad))
        at.set_shift([e],*offset);at.set_tilt([e],roll)
        pb=np.array(e.PolynomB,float);pa=np.array(e.PolynomA,float)
        dk=float(rng.normal(0,config.gradient_rel_std));ds=float(rng.normal(0,config.sextupole_rel_std))
        if len(pb)>1 and pb[1]!=0:
            pa[1]+=pb[1]*rng.normal(0,config.skew_quad_relative_std);pb[1]*=1+dk
        if len(pb)>2 and pb[2]!=0: pb[2]*=1+ds
        e.PolynomB=pb;e.PolynomA=pa
        record.append({'index':i,'family':e.FamName,'dx_m':float(offset[0]),'dy_m':float(offset[1]),
                       'roll_rad':roll,'gradient_rel':dk,'sextupole_rel':ds})
    return r,{'seed':seed,'girder_count':ng,'magnets':record}


def bpm_orbit(ring, bpms):
    """(2*nBPM,) x then y closed-orbit positions (m)."""
    _, orbit=ring.find_orbit4(refpts=bpms)
    values=np.concatenate([orbit[:,0],orbit[:,2]])
    if not np.isfinite(values).all(): raise RuntimeError('Nonfinite ring orbit')
    return values


def response_matrix(ring, bpms, correctors, step_rad=1e-6):
    """Central-difference coupled orbit response (m/rad), x then y correctors."""
    matrix=np.empty((2*len(bpms),2*len(correctors)))
    for axis in (0,1):
        for j,index in enumerate(correctors):
            e=ring[index];saved=e.KickAngle.copy()
            try:
                e.KickAngle=saved.copy();e.KickAngle[axis]+=step_rad;plus=bpm_orbit(ring,bpms)
                e.KickAngle=saved.copy();e.KickAngle[axis]-=step_rad;minus=bpm_orbit(ring,bpms)
                matrix[:,axis*len(correctors)+j]=(plus-minus)/(2*step_rad)
            finally: e.KickAngle=saved
    return matrix


def correct_orbit(ring, bpms, correctors, response, config=RingErrorScenario(), iterations=6):
    """Apply truncated-SVD correction with explicit bounds and residual diagnostics."""
    u,s,vh=svd(response,full_matrices=False)
    keep=s>config.svd_relative_cutoff*s[0]
    inverse=(vh[keep].T/s[keep])@u[:,keep].T
    history=[]
    for iteration in range(iterations+1):
        orbit=bpm_orbit(ring,bpms)
        history.append({'iteration':iteration,'rms_x_m':float(np.sqrt(np.mean(orbit[:len(bpms)]**2))),
                        'rms_y_m':float(np.sqrt(np.mean(orbit[len(bpms):]**2))),
                        'max_abs_m':float(np.max(np.abs(orbit)))})
        if max(history[-1]['rms_x_m'],history[-1]['rms_y_m'])<=config.orbit_tolerance_m or iteration==iterations: break
        delta=-inverse@orbit
        for j,index in enumerate(correctors):
            e=ring[index]
            e.KickAngle=np.clip(e.KickAngle+np.array([delta[j],delta[len(correctors)+j]]),
                                -config.max_corrector_rad,config.max_corrector_rad)
    kicks=np.array([ring[i].KickAngle for i in correctors])
    return {'history':history,'singular_values':s.tolist(),'retained':int(keep.sum()),
            'max_abs_corrector_rad':float(np.max(np.abs(kicks))),
            'bound_rad':config.max_corrector_rad,'termination':'residual tolerance' if
            max(history[-1]['rms_x_m'],history[-1]['rms_y_m'])<=config.orbit_tolerance_m else 'iteration limit',
            'feasible':bool(max(history[-1]['rms_x_m'],history[-1]['rms_y_m'])<=config.orbit_tolerance_m)}


def refresh_prepared_ring(base, lattice):
    """Recompute orbit, maps and optics after lattice correction; keep injection geometry."""
    from dataclasses import replace
    orbit,_=lattice.find_orbit6();m66,_=lattice.find_m66(orbit=orbit)
    _,_,opt=at.get_optics(lattice,refpts=[0]);params=lattice.radiation_parameters()
    return replace(base,ring_c=lattice,orbit6=np.asarray(orbit),m66=np.asarray(m66),
                   septum_index=next(i for i,e in enumerate(lattice) if e.FamName=='NKMUPRING'),
                   twiss_x=(float(opt.beta[0,0]),float(opt.alpha[0,0])),
                   twiss_y=(float(opt.beta[0,1]),float(opt.alpha[0,1])),
                   disp_x=(float(opt.dispersion[0,0]),float(opt.dispersion[0,1])),
                   emit_x_m_rad=float(params.emittances[0]),energy_spread=float(params.sigma_e),
                   bunch_length_m=float(params.sigma_l))


def correct_tunes(ring, families, target, tolerance=1e-5, max_iterations=30, max_shift_m2=.002):
    """Bounded, damped Newton tune fit; reject unstable trials and report termination.

    Family shifts are additive quadrupole gradients in m^-2. Each accepted step
    must reduce the maximum fractional-tune residual; no unstable trial persists.
    """
    history=[];total=np.zeros(2)
    for iteration in range(max_iterations+1):
        values=np.asarray(ring.get_tune())[:2];residual=values-target
        history.append({'iteration':iteration,'tunes':values.tolist(),'max_residual':float(np.max(np.abs(residual)))})
        if history[-1]['max_residual']<tolerance: break
        if iteration==max_iterations: break
        saved=[[ring[i].PolynomB[1] for i in ids] for ids in families]
        def set_shift(delta):
            for j,ids in enumerate(families):
                for i,k in zip(ids,saved[j]): ring[i].PolynomB[1]=k+delta[j]
        jac=np.zeros((2,2))
        for j in range(2):
            step=np.zeros(2);step[j]=1e-5
            set_shift(step);plus=np.asarray(ring.get_tune())[:2]
            set_shift(-step);minus=np.asarray(ring.get_tune())[:2]
            jac[:,j]=(plus-minus)/(2e-5)
        set_shift(np.zeros(2))
        delta=np.linalg.lstsq(jac,-residual,rcond=None)[0]
        delta*=min(1.,max_shift_m2/max(np.max(np.abs(delta)),1e-20))
        accepted=False
        for factor in (1.,.5,.25,.125,.0625,.03125):
            set_shift(delta*factor)
            try:
                trial=np.asarray(ring.get_tune())[:2]
                accepted=np.isfinite(trial).all() and np.max(np.abs(trial-target))<history[-1]['max_residual']
            except (ValueError,RuntimeError,np.linalg.LinAlgError): accepted=False
            if accepted: total+=delta*factor;break
        if not accepted: set_shift(np.zeros(2));break
    return {'history':history,'family_total_shifts_m_minus2':total.tolist(),
            'step_bound_m_minus2':max_shift_m2,'tolerance':tolerance,
            'termination':'tolerance' if history[-1]['max_residual']<tolerance else 'iteration or line-search limit',
            'feasible':bool(history[-1]['max_residual']<tolerance)}
