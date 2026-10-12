#!/usr/bin/env python3
"""D9: wire/loop dipole and quadrupole sensitivity, tolerances and finite-beam moments."""
import argparse
import json
from pathlib import Path
import numpy as np
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring
from nkm_injection.wire_field import FilamentGeometry
from nkm_injection.sliced_vector_map import integrated_filament_kicks


def derivative_observables(kick):
    h=1e-6
    dipole=np.array([float(k) for k in kick(0.,0.)])
    jac=np.column_stack([(np.array(kick(h,0.))-np.array(kick(-h,0.)))/(2*h),
                         (np.array(kick(0.,h))-np.array(kick(0.,-h)))/(2*h)])
    return np.concatenate([dipole,jac.ravel()])


def projected_emit(q,p):
    q=q-q.mean();p=p-p.mean()
    return float(np.sqrt(max(0.,np.mean(q*q)*np.mean(p*p)-np.mean(q*p)**2)))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--study-config',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    cfg=InjectionStudyConfig.load(a.study_config);ring=cached_ring(cfg,Path.cwd(),a.output.parent/'_lattice')
    g=FilamentGeometry();betas=np.array([ring.twiss_x[0],ring.twiss_y[0]])
    emits=np.array([ring.emit_x_m_rad,ring.emit_x_m_rad*cfg.stored_vertical_emittance_ratio])
    sigmas=np.sqrt(betas*emits);kick_limits=.1*sigmas/betas
    rows=[]
    for wire in range(8):
        for axis in range(2):
            h=1e-7;values=[]
            for sign in (-1,1):
                offsets=np.zeros((8,2));offsets[wire,axis]=sign*h
                values.append(derivative_observables(lambda x,y:integrated_filament_kicks(x,y,g,
                    cfg.energy_eV,cfg.field_scale,cfg.kicker_polarity,wire_offsets_m=offsets)))
            sensitivity=(values[1]-values[0])/(2*h)
            dip=sensitivity[:2]
            # Symmetry-forbidden first derivatives are unresolved at finite-
            # difference precision; do not turn roundoff into kilometre tolerances.
            resolved=np.abs(dip)>1e-8*np.max(np.abs(dip))
            tolerances=np.divide(kick_limits,np.abs(dip),out=np.full(2,np.inf),where=resolved)
            finite=[float(v) if np.isfinite(v) else None for v in tolerances]
            rows.append({'wire':wire,'axis':'xy'[axis],'position_m':g.wire_positions()[wire].tolist(),
                         'dipole_derivative_rad_per_m':dip.tolist(),'quadrupole_derivative_rad_per_m2':sensitivity[2:].reshape(2,2).tolist(),
                         'tolerance_x_y_m':finite,'joint_single_error_tolerance_m':float(np.min(tolerances)),
                         'derivative_step_m':h})
    current=[]
    for loop in range(4):
        h=1e-5;values=[]
        for sign in (-1,1):
            error=np.zeros(4);error[loop]=h*sign
            values.append(derivative_observables(lambda x,y:integrated_filament_kicks(x,y,g,cfg.energy_eV,
                cfg.field_scale,cfg.kicker_polarity,loop_current_relative=error)))
        sensitivity=(values[1]-values[0])/(2*h);dip=sensitivity[:2]
        current.append({'loop':loop,'dipole_derivative_rad_per_relative_current':dip.tolist(),
                        'quadrupole_derivative_rad_per_m_per_relative_current':sensitivity[2:].reshape(2,2).tolist(),
                        'single_loop_tolerance_relative':float(np.min(kick_limits/np.abs(dip)))})
    # Deterministic Gauss-Hermite full-beam covariance, not just a symmetry-axis centroid.
    moment=[]
    for order in (20,40,60):
        nodes,weights=np.polynomial.hermite.hermgauss(order);nodes*=np.sqrt(2);weights/=np.sqrt(np.pi)
        x,y=np.meshgrid(nodes*sigmas[0],nodes*sigmas[1],indexing='ij');w=np.outer(weights,weights)
        kx,ky=integrated_filament_kicks(x,y,g,cfg.energy_eV,cfg.field_scale,cfg.kicker_polarity)
        covariance=[]
        for q,k,em,beta in ((x,kx,emits[0],betas[0]),(y,ky,emits[1],betas[1])):
            mean=float(np.sum(w*k));spread=float(np.sum(w*(k-mean)**2));qk=float(np.sum(w*q*(k-mean)))
            # Exact one-pass determinant after adding k(q): em^2 + em*beta*Var(k)-Cov(q,k)^2.
            ratio=np.sqrt(max(0.,em*em+em*beta*spread-qk*qk))/em
            covariance.append({'mean_kick_rad':mean,'rms_kick_rad':np.sqrt(spread),'emittance_ratio_after_single_pass':float(ratio),
                               'filamented_emittance_growth':float(beta*spread/(2*em))})
        moment.append({'gh_order_per_axis':order,'planes':covariance})
    out={'wire_sensitivity':rows,'independent_loop_current_sensitivity':current,
         'series_case':'common current scales all loops; dipole remains zero by symmetry, provided loop currents are equal',
         'beam_moments':moment,'beta_x_y_m':betas.tolist(),'sigma_x_y_m':sigmas.tolist(),
         'kick_limits_x_y_rad':kick_limits.tolist(),'emittance_ratio_assumption':cfg.stored_vertical_emittance_ratio,
         'scaling':'vertical amplitude/sigma proportional to epsilon_y^(-1/2)',
         'criterion':'one error at a time: <=0.1 sigma_x and <=0.1 sigma_y centroid response; not a simultaneous allocation',
         'unresolved_derivative':'null tolerance means no resolved first-order dipole response (relative derivative floor 1e-8); higher orders remain',
         'units':'positions m, angles rad, currents relative, gradients rad/m',
         'study_config':cfg.to_dict()}
    a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('wire tolerance range [um]',min(r['joint_single_error_tolerance_m'] for r in rows)*1e6,
          max(r['joint_single_error_tolerance_m'] for r in rows)*1e6)
    print('loop relative tolerances',[r['single_loop_tolerance_relative'] for r in current])


if __name__=='__main__':main()
