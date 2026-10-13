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


def optics_record(strengths, steps=40):
    lat=lattice_for(strengths,integration_steps=steps)
    prop=compute_twiss_propagation(lat,DEFAULT_BTS_ENTRANCE_TWISS.to_dict())
    observables=np.r_[prop['final_beta'],prop['final_alpha'],prop['final_dispersion'][:2]]
    residual=observables-TARGET
    independent,_=independent_maps(lat)
    initial=DEFAULT_BTS_ENTRANCE_TWISS.to_dict();betas=[]
    for plane in [0,1]:
        i=2*plane;b=initial['beta'][plane];a=initial['alpha'][plane]
        cov=np.array([[b,-a],[-a,(1+a*a)/b]])
        block=independent[:,i:i+2,i:i+2]
        betas.append((block@cov@block.transpose(0,2,1))[:,0,0])
    peak=np.max(betas,axis=1)
    margin=clearance_profile(lat,JournalBeam())
    feasible=bool(np.all(np.array(strengths)>=LOWER) and np.all(np.array(strengths)<=UPPER) and np.all(peak<=60.) and np.max(np.abs(residual/SCALES))<1. and margin['minimum_m']>0.)
    return {'strengths_m_minus2':strengths,'raw_residuals_beta_alpha_dispersion':residual,'max_abs_normalized_residual':np.max(np.abs(residual/SCALES)),'peak_beta_m':peak,'independently_feasible':feasible,'minimum_five_sigma_clearance_m':margin['minimum_m'],'s_m':prop['s_pos'],'beta_m':prop['beta'],'dispersion_m':prop['dispersion'],'sigma_m':margin['sigma_m'],'clearance_stations':margin['stations']}


def matching(output,config):
    from nkm_injection.optimization import BTSOptimizationConfig, DeterministicObjective, OpticsOptimizer
    optconfig=BTSOptimizationConfig(random_seed=42,max_iter=100)
    objective=DeterministicObjective(optconfig,lattice=create_bts_lattice(BTSConfig(**config['bts_config'])))
    historical_replay=OpticsOptimizer(config=optconfig,objective=objective).optimize(method='least_squares',n_starts=3)
    candidates=[c.as_dict() for c in historical_replay.candidate_table]
    for c in candidates:c['independent_40_step_reevaluation']=optics_record(np.array(c['strengths']))
    save(output/'candidate_table.json',candidates)
    result={'environment':environment(),'seed':42,'n_starts':3,'start_design':'nominal plus two random uniform box starts','budget':100,'method':'box-constrained least_squares then conditional box-constrained SLSQP; physical post-selection, no nonlinear constraints in historical search','bounds_m_minus2':list(zip(LOWER,UPPER)),'archived_reference':optics_record(selected()),'rounded_six_decimals':optics_record(np.round(selected(),6)),'initial_baseline':optics_record(np.array(BTSConfig(**config['bts_config']).quad_strengths_list)),'replay_selected':optics_record(historical_replay.optimized_strengths),'replay_candidates':[{'start_idx':c['start_idx'],'optimizer_success':c['optimizer_success'],'physically_feasible':c['physically_feasible'],'merit':c['merit'],'termination':c['optimizer_message'],'max_beta_x_m':c['max_beta_x_m'],'max_beta_y_m':c['max_beta_y_m']} for c in candidates]}
    assert result['archived_reference']['independently_feasible']
    assert result['rounded_six_decimals']['independently_feasible']
    assert result['replay_selected']['independently_feasible']
    save(output/'matching.json',result)
    return result


def normalized_response(output,config):
    strengths=selected();jacobians=[]
    for step in [1e-4,1e-5,1e-6]:
        jac=np.column_stack([(np.array(optics_record(strengths+np.eye(9)[j]*step)['raw_residuals_beta_alpha_dispersion'])-np.array(optics_record(strengths-np.eye(9)[j]*step)['raw_residuals_beta_alpha_dispersion']))/(2*step) for j in range(9)])
        jacobians.append(jac)
    strength_scales=np.full(9,.01)
    response=jacobians[-1]/SCALES[:,None]*strength_scales[None,:]
    u,s,vt=np.linalg.svd(response,full_matrices=True)
    convergence=[np.linalg.norm(j-jacobians[-1])/np.linalg.norm(jacobians[-1]) for j in jacobians]
    assert convergence[0]<1e-4 and convergence[1]<1e-5
    checks=[]
    for mode in range(6):
        # Local finite perturbation only; no claimed operational correction.
        dk=strength_scales*vt[mode]*.01
        measured=(np.array(optics_record(strengths+dk)['raw_residuals_beta_alpha_dispersion'])-np.array(optics_record(strengths)['raw_residuals_beta_alpha_dispersion']))/SCALES
        prediction=response@(dk/strength_scales)
        checks.append({'mode':mode,'delta_k_m_minus2':dk,'actual_normalized_change':measured,'linear_prediction':prediction,'relative_error':np.linalg.norm(measured-prediction)/np.linalg.norm(prediction),'within_bounds':bool(np.all(strengths+dk>=LOWER)&np.all(strengths+dk<=UPPER))})
    assert all(c['relative_error']<.01 and c['within_bounds'] for c in checks)
    result={'environment':environment(),'row_order':['beta_x_m','beta_y_m','alpha_x','alpha_y','Dx_m','Dpx'],'row_scales':SCALES,'column_scales_m_minus2':strength_scales,'finite_difference_steps_m_minus2':[1e-4,1e-5,1e-6],'relative_jacobian_convergence':convergence,'response_matrix':response,'singular_values':s,'condition_number':s[0]/s[-1],'rank':int(np.sum(s>s[0]*1e-10)),'rank_relative_threshold':1e-10,'right_vectors':vt,'null_space_dimension':3,'null_vector_sign_convention':'SVD signs arbitrary; rows 6:9 of full Vt span the local null space','finite_local_checks':checks,'claim_withdrawal':'No achieved commissioning correction, practical decoupling, measured observability or static/shot retuning benefit is claimed. SVD is a local model diagnostic only.'}
    save(output/'normalized_response.json',result);return result


def paired_interval(values, seed, count=10000):
    """Percentile bootstrap of paired machine means, not independent particles."""
    values=np.asarray(values);rng=np.random.default_rng(seed)
    estimates=np.mean(values[rng.integers(0,len(values),(count,len(values)))],axis=1)
    return {'mean':float(np.mean(values)),'ci95':np.quantile(estimates,[.025,.975]).tolist(),'n_machines':len(values),'method':'paired machine-cluster percentile bootstrap','bootstrap_count':count,'seed':seed}


def comparison(output,config):
    from scipy.optimize import minimize
    from scipy.stats import beta as beta_dist
    original=selected()
    def residual(k):return np.array(optics_record(k)['raw_residuals_beta_alpha_dispersion'])/SCALES
    def score(k):return optics_record(k)['peak_beta_m'][1]
    res=minimize(score,original,method='SLSQP',bounds=list(zip(LOWER,UPPER)),constraints=[{'type':'eq','fun':residual},{'type':'ineq','fun':lambda k:60.-optics_record(k)['peak_beta_m'][0]}],options={'maxiter':200,'ftol':1e-8})
    alternative=optics_record(res.x)
    assert res.success and alternative['independently_feasible']
    save(output/'margin_optimizer.json',{'environment':environment(),'objective':'minimize vertical peak beta sampled at element boundaries','nonlinear_constraints':'six exact optical residual equalities and beta_x <=60 m','bounds':list(zip(LOWER,UPPER)),'start':original,'termination':str(res.message),'success':bool(res.success),'iterations':res.nit,'alternative':alternative,'reference':optics_record(original)})
    beam=JournalBeam(**config['beam']);nominal=lattice_for(original)
    # Training/audit set is separate from the test and does not select/tune on it.
    train_rng=np.random.default_rng(config['training_seed']);training=[]
    for machine in range(60):
        errors=draw_static(train_rng,nominal);values=[]
        for k in [original,res.x]:values.append(clearance_profile(apply_static(lattice_for(k),errors),beam)['minimum_m'])
        training.append(values)
    save(output/'training.json',{'seed':config['training_seed'],'n_machines':60,'clearance_pairs_m':training,'policy':'Design optimized on nominal physics only; separate training audit frozen before test. No correction or per-shot retuning.'})
    test_rng=np.random.default_rng(config['heldout_seed']);particle_rng=np.random.default_rng(config['particle_seed'])
    machine_rows=[];first_losses=[{},{}];particle_lost=[0,0];particle_total=0;raw=[]
    for machine in range(config['heldout_machines']):
        errors=draw_static(test_rng,nominal)
        lattices=[apply_static(lattice_for(k),errors) for k in [original,res.x]]
        shots=[]
        for shot in range(config['shots_per_machine']):
            factors=1+test_rng.normal(0,.05,2)
            dx,px,dp=test_rng.normal(0,[.0005,.0002,.001])
            centroid=np.array([dx+.2762*dp,px-.0657*dp,0.,0.,dp])
            cov=beam.covariance(factors)
            particles=particle_rng.multivariate_normal(np.zeros(6),cov,config['particles_per_shot']).T
            particles[:5]+=centroid[:,None]
            values=[]
            for design,lat in enumerate(lattices):
                margin=clearance_profile(lat,beam,centroid,factors)
                track=at.lattice_track(lat,np.array(particles,order='F'),nturns=1,refpts=np.arange(len(lat)+1))[0][:,:,:,0]
                finite=np.isfinite(track[0]);lost=~finite[:,-1];nlost=int(lost.sum());particle_lost[design]+=nlost
                for particle in np.flatnonzero(lost):
                    first=int(np.flatnonzero(~finite[particle])[0])-1
                    name=f'{first}:{lat[first].FamName}'
                    first_losses[design][name]=first_losses[design].get(name,0)+1
                survivors=track[:4,~lost,-1]
                if not np.all(np.isfinite(survivors)):raise ValueError('Invalid surviving particle coordinates')
                values.append({'clearance_m':margin['minimum_m'],'lost':nlost,'transmission':1-nlost/config['particles_per_shot'],'exit_centroid_xy_m':np.mean(survivors[[0,2]],axis=1).tolist(),'exit_rms_xy_m':np.std(survivors[[0,2]],axis=1,ddof=1).tolist()})
            particle_total+=config['particles_per_shot'];shots.append(values)
            raw.append({'machine':machine,'shot':shot,'beta_factors':factors,'centroid':centroid,'static_errors':errors,'design_results':values})
        machine_rows.append({'machine':machine,'mean_clearance_m':[np.mean([s[d]['clearance_m'] for s in shots]) for d in [0,1]],'mean_transmission':[np.mean([s[d]['transmission'] for s in shots]) for d in [0,1]],'shots':shots})
    paired=np.array([m['mean_clearance_m'] for m in machine_rows]);trans=np.array([m['mean_transmission'] for m in machine_rows])
    ci=paired_interval(paired[:,1]-paired[:,0],config['bootstrap_seed'],config['bootstrap_count'])
    loss_bound=[]
    for k in particle_lost:
        low=0. if k==0 else float(beta_dist.ppf(.025,k,particle_total-k+1));hi=1. if k==particle_total else float(beta_dist.ppf(.975,k+1,particle_total-k))
        loss_bound.append({'lost':k,'total':particle_total,'conditional_particle_binomial_ci95':[low,hi],'interpretation':'Conditional descriptive interval; shared machine/shot effects prevent interpreting all particles as iid machine reliability.'})
    result={'environment':environment(),'nominal':optics_record(original),'alternative':alternative,'optimizer_success':bool(res.success),'optimizer_termination':str(res.message),'training_seed':config['training_seed'],'heldout_seed':config['heldout_seed'],'particle_seed':config['particle_seed'],'design_frozen_before_heldout':True,'machines':config['heldout_machines'],'shots_per_machine':config['shots_per_machine'],'particles_per_shot':config['particles_per_shot'],'paired_clearance_difference_m':ci,'paired_transmission_difference':paired_interval(trans[:,1]-trans[:,0],config['bootstrap_seed']+1,config['bootstrap_count']),'mean_clearance_m':np.mean(paired,axis=0),'clearance_machine_quantiles_m':np.quantile(paired,[.05,.5,.95],axis=0),'loss_counts':loss_bound,'first_loss_counts':first_losses,'zero_loss_shot_upper95':float(1-.05**(1/config['heldout_machines'])),'zero_loss_shot_upper_note':'Only applicable when all independent machine blocks have no losses; one-sided bound for a block with any loss, not per-particle hardware reliability.','invalid_evaluations':0,'claim_scope':'No correction, continuous-chamber certification or storage-ring capture; frozen margin versus nominal under parametric station apertures.'}
    save(output/'heldout.json',result);save(output/'raw_realizations.json',raw);save(output/'machine_results.json',machine_rows)
    print('Comparison paired clearance [m]',ci)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['validation','matching','response','comparison'],required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=False)
    config=json.loads((PAPER/'journal_config.json').read_text());save(args.output_dir/'config.json',config)
    result={'validation':validation,'matching':matching,'response':normalized_response,'comparison':comparison}[args.stage](args.output_dir,config)
    print(json.dumps({k:v for k,v in result.items() if k not in ['environment','error_coverage']},default=serial))


if __name__=='__main__':main()
