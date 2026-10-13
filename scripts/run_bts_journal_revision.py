#!/usr/bin/env python3
"""Reproduce Reviewer 1 numerical revisions in a new BTS results directory."""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import numpy as np
import scipy
import at
from nkm_injection.bts_journal import *
from nkm_injection.optics import compute_twiss_propagation

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'docs/paper_bts'


def serial(value):
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,np.generic):return value.item()
    raise TypeError(type(value).__name__)


def save(path,data):path.write_text(json.dumps(data,indent=2,default=serial,allow_nan=False)+'\n')


def environment():
    files=['src/nkm_injection/bts_journal.py','scripts/run_bts_journal_revision.py','docs/paper_bts/journal_config.json']
    return {'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in files},
            'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'pyat':at.__version__}


def selected():
    return np.array(json.loads((ROOT/'backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json').read_text())['optimized_strengths_raw'])


def validation(output,config):
    lat=lattice_for(selected(),BTSConfig(**config['bts_config']))
    hard,orbit=independent_maps(lat);tracked,at_orbit=tracked_linear_maps(lat)
    convergence={}
    for steps in [10,20,40,80]:
        trial=lattice_for(selected(),integration_steps=steps);trial_maps,_=tracked_linear_maps(trial)
        convergence[str(steps)]=float(np.max(np.abs(hard-trial_maps)))
    nominal_error=float(np.max(np.abs(hard-tracked)))
    assert nominal_error<2e-6
    j=np.kron(np.eye(2),np.array([[0.,1.],[-1.,0.]]))
    symp=float(np.max(np.abs(hard[-1,:4,:4].T@j@hard[-1,:4,:4]-j)))
    assert symp<1e-10
    coverage=[]
    zero=draw_static(np.random.default_rng(0),lat,0.)
    for kind in ['gradient','offset','roll','dipole']:
        err={k:dict(v) if isinstance(v,dict) else v.copy() for k,v in zero.items()}
        if kind=='dipole':err[kind]['b1']=.0005
        elif kind=='offset':err[kind][0,0]=.0001
        elif kind=='roll':err[kind][0]=.0005
        else:err[kind][0]=.001
        pert=apply_static(lattice_for(selected()),err)
        m,b=independent_maps(pert);a,c=tracked_linear_maps(pert)
        map_error=float(np.max(np.abs(m-a)));orbit_error=float(np.max(np.abs(b-c)))
        assert map_error<1e-3 and orbit_error<2e-6
        coverage.append({'error':kind,'map_max_abs_difference':map_error,'orbit_max_abs_difference_m':orbit_error,'exit_orbit_xy_m':b[-1,[0,2]],'coupling_block_norm':np.linalg.norm(m[-1,:2,2:4]),'change_of_covariance_norm':np.linalg.norm(m[-1]@JournalBeam().covariance()[:5,:5]@m[-1].T-hard[-1]@JournalBeam().covariance()[:5,:5]@hard[-1].T)})
    cov=JournalBeam().covariance();rng=np.random.default_rng(71000)
    particles=rng.multivariate_normal(np.zeros(6),cov,50000).T.copy(order='F')
    track=at.lattice_track(lat,particles,nturns=1,refpts=[len(lat)])[0][:,:,0,0]
    assert np.all(np.isfinite(track))
    predicted=hard[-1]@cov[:5,:5]@hard[-1].T
    rms_ratio=np.std(track[[0,2]],axis=1,ddof=1)/np.sqrt(np.diag(predicted)[[0,2]])
    assert np.all(np.abs(rms_ratio-1)<.02)
    tw=compute_twiss_propagation(lat,DEFAULT_BTS_ENTRANCE_TWISS.to_dict())
    covariance_beta=[]
    for plane in [0,1]:
        i=2*plane;b=DEFAULT_BTS_ENTRANCE_TWISS.to_dict()['beta'][plane];a=DEFAULT_BTS_ENTRANCE_TWISS.to_dict()['alpha'][plane]
        c=np.array([[b,-a],[-a,(1+a*a)/b]])
        m=hard[-1,i:i+2,i:i+2];covariance_beta.append(float((m@c@m.T)[0,0]))
    assert np.max(np.abs(covariance_beta-tw['final_beta']))<1e-5
    initial_d=np.array([.2762,-.0657,0,0,1.]);ind_disp=hard[-1]@initial_d
    assert np.max(np.abs(ind_disp[:4]-tw['final_dispersion']))<2e-6
    energy=[]
    for dp in [-.001,.001]:
        probe=np.zeros((6,1),order='F');probe[:5,0]=initial_d*dp
        end=at.lattice_track(lat,probe,nturns=1,refpts=[len(lat)])[0][:,0,0,0]
        energy.append({'delta':dp,'exit_xy_m':end[[0,2]],'linear_x_m':ind_disp[0]*dp,'linearization_error_x_m':float(end[0]-ind_disp[0]*dp)})
        assert abs(end[0]-ind_disp[0]*dp)<5e-6
    # Deliberate scraping validates actual first loss (aperture index 1).
    probes=np.zeros((6,2),order='F');probes[0,0]=.03
    out=at.lattice_track(lat,probes,nturns=1,refpts=np.arange(len(lat)+1))[0][0,:,:,0]
    assert np.flatnonzero(~np.isfinite(out[0]))[0]==2 and np.isfinite(out[1,-1])
    result={'environment':environment(),'tolerances':{'nominal_map_abs':2e-6,'perturbed_map_abs':1e-3,'orbit_m':2e-6,'symplectic_max_abs':1e-10,'rms_relative':.02,'twiss_beta_m':1e-5,'dispersion_abs':2e-6,'energy_linearization_x_m':5e-6},'integration_step_convergence':convergence,'default_10_step_missed_map_tolerance':convergence['10']>2e-6,'nominal_map_difference':nominal_error,'transverse_symplectic_error':symp,'independent_exit_beta_m':covariance_beta,'independent_exit_dispersion':ind_disp[:4],'error_coverage':coverage,'tracking_seed':71000,'particles':50000,'rms_ratio_tracking_to_linear':rms_ratio,'energy_cases':energy,'first_loss_element_index':1,'invalid_evaluations':0,'all_checks_passed':True}
    save(output/'validation.json',result)
    np.savez_compressed(output/'validation_maps.npz',independent=hard,tracked=tracked,particles_in=particles,particles_out=track)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['validation'],required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=False)
    config=json.loads((PAPER/'journal_config.json').read_text());save(args.output_dir/'config.json',config)
    result=validation(args.output_dir,config)
    print(json.dumps({k:v for k,v in result.items() if k not in ['environment','error_coverage']},default=serial))


if __name__=='__main__':main()
