#!/usr/bin/env python3
"""Reconstruct BTS station diagnostics in a new directory (SI units)."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import numpy as np
import scipy
import at
from nkm_injection.bts_journal import JournalBeam,lattice_for,apply_static,TARGET,SCALES,LOWER,UPPER
from nkm_injection.bts_round2 import station_record,quadrature_moments,spatial_profile,nominal_observables

ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT/'docs/paper_bts'


def serial(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)


def save(path,data):path.write_text(json.dumps(data,indent=2,default=serial,allow_nan=False)+'\n')


def environment():
    return {'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'pyat':at.__version__,
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['src/nkm_injection/bts_round2.py','src/nkm_injection/bts_journal.py','scripts/run_bts_round2.py','docs/paper_bts/round2_protocol.json']}}


def original():
    old=ROOT/'results/bts_journal_campaign_r1_20261013/comparison'
    result=json.loads((old/'heldout.json').read_text());raw=json.loads((old/'raw_realizations.json').read_text())
    return [np.array(result[d]['strengths_m_minus2']) for d in ['nominal','alternative']],raw


def errors_from(row):
    errors=row['static_errors'].copy()
    for key in ['gradient','offset','roll']:errors[key]=np.asarray(errors[key])
    return errors


def stations(output):
    strengths,raw=original();records=[];counts=[Counter(),Counter()];differences=[];downstream=[]
    nominal=[station_record(lattice_for(k)) for k in strengths]
    for row in raw:
        pair=[]
        for d,k in enumerate(strengths):
            record=station_record(apply_static(lattice_for(k),errors_from(row)),centroid=row['centroid'],beta_factors=row['beta_factors'])
            assert abs(record['minimum_m']-row['design_results'][d]['clearance_m'])<1e-12
            counts[d][str(record['active'])]+=1;pair.append(record)
        records.append({'machine':row['machine'],'shot':row['shot'],'designs':pair})
        differences.append(pair[1]['minimum_m']-pair[0]['minimum_m'])
        downstream.append(pair[1]['downstream_minimum_m']-pair[0]['downstream_minimum_m'])
    delta=np.array(differences);machine=delta.reshape(200,3).mean(1)
    equal=delta==0
    result={'environment':environment(),'units':'m and m^2','nominal':nominal,'active_frequencies':list(map(dict,counts)),
            'equal_shots':int(sum(equal)),'equal_machines':int(sum(machine==0)),
            'equal_shots_both_entrance':int(sum(same and all(d['active'][0]==1 for d in r['designs']) for same,r in zip(equal,records))),
            'paired_machine_mean_m':float(machine.mean()),'paired_machine_sd_m':float(machine.std(ddof=1)),
            'paired_machine_quantiles_m':np.quantile(machine,[0,.05,.5,.95,1]),
            'machine_gain_loss_tie_counts':[int(sum(machine>0)),int(sum(machine<0)),int(sum(machine==0))],
            'downstream_diagnostic_paired_mean_m':float(np.mean(downstream)),
            'scope':'Retrospective original-test audit, not a new holdout. Downstream-only results are secondary diagnostics.'}
    save(output/'station_realizations.json',records);save(output/'stations.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['environment','nominal']},default=serial))


def interval(delta,seed=82005):
    rng=np.random.default_rng(seed);delta=np.asarray(delta)
    means=delta[rng.integers(0,len(delta),(10000,len(delta)))].mean(1)
    return {'mean_m':float(delta.mean()),'ci95_m':np.quantile(means,[.025,.975]).tolist()}


def accuracy(output):
    strengths,raw=original();records=[];deltas=[];old=[];changed=[0,0]
    max_step=0.;max_integration=0.;cases=[]
    # Representative actual shots: extreme momentum, extreme x, and first case.
    selected=sorted(set([0,int(np.argmax([r['centroid'][4] for r in raw])),int(np.argmin([r['centroid'][4] for r in raw])),int(np.argmax([abs(r['centroid'][0]) for r in raw]))]))
    for n,row in enumerate(raw):
        pair=[];oldpair=[]
        for d,k in enumerate(strengths):
            lat=apply_static(lattice_for(k),errors_from(row))
            affine=station_record(lat,centroid=row['centroid'],beta_factors=row['beta_factors'])
            centred=station_record(lat,centroid=row['centroid'],beta_factors=row['beta_factors'],method='centred')
            changed[d]+=centred['active']!=affine['active'];pair.append(centred['minimum_m']);oldpair.append(affine['minimum_m'])
            records.append({'shot_index':n,'design':d,'affine':affine,'centred':centred})
            if n in selected:
                step_records=[station_record(lat,centroid=row['centroid'],beta_factors=row['beta_factors'],method='centred',step=s) for s in [1e-6,1e-7,1e-8]]
                max_step=max(max_step,max(abs(a['clearance_m']-b['clearance_m']) for rec in step_records for a,b in zip(rec['stations'],centred['stations'])))
                fine=station_record(apply_static(lattice_for(k,integration_steps=80),errors_from(row)),centroid=row['centroid'],beta_factors=row['beta_factors'],method='centred')
                max_integration=max(max_integration,max(abs(a['clearance_m']-b['clearance_m']) for a,b in zip(fine['stations'],centred['stations'])))
                moments=[quadrature_moments(lat,JournalBeam(),row['centroid'],row['beta_factors'],order=o) for o in [3,5,7]]
                mean,sigma=moments[-1];quadrature=[];conv=0.;bias=0.
                for station in centred['stations']:
                    i=station['index']+1;j=0 if station['axis']==0 else 2
                    clear=station['aperture_halfwidth_m']-abs(mean[i,j])-5*sigma[i,j]
                    conv=max(conv,abs(moments[-2][0][i,j]-mean[i,j])+5*abs(moments[-2][1][i,j]-sigma[i,j]))
                    bias=max(bias,abs(clear-station['clearance_m']))
                    quadrature.append({'index':i-1,'axis':station['axis'],'mean_m':mean[i,j],'sigma_m':sigma[i,j],'clearance_m':clear,'centred_error_m':station['clearance_m']-clear})
                cases.append({'shot_index':n,'design':d,'moment_order':7,'quadrature_5_to_7_clearance_bound_m':conv,'max_centred_vs_quadrature_clearance_error_m':bias,'quadrature_stations':quadrature})
        deltas.append(pair[1]-pair[0]);old.append(oldpair[1]-oldpair[0])
    old=np.array(old).reshape(200,3).mean(1);new=np.array(deltas).reshape(200,3).mean(1)
    max_model=max(abs(a['clearance_m']-b['clearance_m']) for r in records for a,b in zip(r['affine']['stations'],r['centred']['stations']))
    result={'environment':environment(),'scope':'Retrospective original ensemble; centred AT Jacobian about actual shot centroid. Quadrature checks unrestricted Gaussian moments, not loss tails.',
            'original_affine_interval':interval(old,71004),'centred_interval':interval(new,71004),'paired_mean_model_shift_m':float(np.mean(new-old)),
            'active_changed_shots':changed,'max_station_affine_vs_centred_error_m':max_model,'max_step_clearance_change_m':max_step,'max_40_to_80_clearance_change_m':max_integration,
            'quadrature_cases':cases,'max_quadrature_clearance_error_m':max(c['max_centred_vs_quadrature_clearance_error_m'] for c in cases),
            'max_quadrature_5_to_7_bound_m':max(c['quadrature_5_to_7_clearance_bound_m'] for c in cases)}
    save(output/'accuracy_realizations.json',records);save(output/'accuracy.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['environment','quadrature_cases']},default=serial))


def spatial(output):
    from scipy.optimize import minimize
    strengths,_=original();profiles=[]
    for k in strengths:
        profiles.append([spatial_profile(lattice_for(k),n) for n in [1,8,16,32,64]])
    def residual(k):return (nominal_observables(lattice_for(k))-TARGET)/SCALES
    cache={}
    def peaks(k):
        key=tuple(k)
        if key not in cache:cache[key]=spatial_profile(lattice_for(k),16)['peak_beta_m']
        return np.array(cache[key])
    res=minimize(lambda k:peaks(k)[1],strengths[1],method='SLSQP',bounds=list(zip(LOWER,UPPER)),constraints=[{'type':'eq','fun':residual},{'type':'ineq','fun':lambda k:60-peaks(k)[0]}],options={'maxiter':200,'ftol':1e-8})
    final=[spatial_profile(lattice_for(res.x),n) for n in [8,16,32,64]]
    assert res.success and max(abs(residual(res.x)))<1e-3
    assert max(abs(np.array(final[-1]['peak_beta_m'])-final[-2]['peak_beta_m']))<.02
    result={'environment':environment(),'original_profiles':[{str(p['subdivisions']):{k:v for k,v in p.items() if k not in ['rows','exit_map']} for p in ps} for ps in profiles],
            'refined_low_beta':{'strengths_m_minus2':res.x,'success':bool(res.success),'iterations':res.nit,'termination':str(res.message),'normalized_residual':residual(res.x),'bounds':list(zip(LOWER,UPPER)),'active_bounds':[int(i) for i in np.flatnonzero(np.minimum(res.x-LOWER,UPPER-res.x)<1e-6)],'profiles':[{k:v for k,v in p.items() if k not in ['rows','exit_map']} for p in final]},
            'objective':'vertical peak beta on 16 subdivisions per finite element; verified at 32/64','limits':'finite sampled maxima, not analytic global optimization','peak_convergence_tolerance_m':.02}
    save(output/'spatial_profiles.json',{'original':profiles,'refined':final});save(output/'spatial.json',result)
    print(json.dumps(result,default=serial))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage',choices=['stations','accuracy','spatial'],required=True);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=False)
    save(args.output_dir/'configuration.json',{'stage':args.stage,'protocol':json.loads((PAPER/'round2_protocol.json').read_text()),'environment':environment()})
    globals()[args.stage](args.output_dir)


if __name__=='__main__':main()
