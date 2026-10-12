#!/usr/bin/env python3
"""D8 reduced static-machine tuning with held-out, shot-perturbed validation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_tuning import coordinate_sweep
from run_capture_robustness import run_realization, cluster_stats

SHOT_KEYS=('booster_x_m','booster_xp_rad','energy_dp_p','nkm_scale_err',
           'nkm_timing_mrad','septum_strength_rel','rf_phase_rad','arrival_time_s')


def tune_machine(task):
    source=task['source'];identifier=source['sample']['sample_id'];base=copy.deepcopy(source)
    base.pop('checkpoint',None);base['models']=['fieldmap_3d'];base['particles']=100
    base['beam_seed']=source['beam_seed']+100000000
    base['extra']={'emit_rel':0.,'espread_abs':0.}
    for key in SHOT_KEYS:base['sample'][key]=0.
    names=('injection_x_m','injection_xp_rad','field_scale')
    nominal=[base['config'][name] for name in names]
    def evaluate(knobs):
        job=copy.deepcopy(base)
        job['config'].update(dict(zip(names,knobs)))
        return run_realization(job)['models']['fieldmap_3d']['capture_fraction']
    search=coordinate_sweep(evaluate,nominal,[[-.022,-.0182],[.0035,.0065],[.7,1.2]],
                            [.0005,.0003,.05],seed=base['beam_seed'])
    heldout=[]
    for scale in (0.,.25):
        job=copy.deepcopy(source);job.pop('checkpoint',None);job['models']=['fieldmap_3d']
        job['sample']['booster_x_m']*=scale;job['sample']['booster_xp_rad']*=scale
        job['config'].update(dict(zip(names,search['knobs'])))
        result=run_realization(job)
        original=task['untuned'][str(scale)]
        assert original['beam_seed']==result['beam_seed']
        assert original['ring_error_seed']==result['ring_error_seed']
        heldout.append({'jitter_scale':scale,'untuned':original,'tuned':result})
    row={'sample_id':identifier,'training':search,'heldout':heldout}
    path=Path(task['checkpoint']);temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(row,indent=2,allow_nan=False)+'\n');temporary.replace(path)
    print('tuned realization',identifier,'training capture',search['training_capture'],flush=True)
    return row


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--full-ensemble',type=Path,required=True)
    p.add_argument('--zero-ensemble',type=Path,required=True)
    p.add_argument('--quarter-ensemble',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--workers',type=int,default=8);p.add_argument('--resume',action='store_true')
    a=p.parse_args();out=a.output_dir
    if out.exists() and any(out.iterdir()) and not a.resume:raise SystemExit('Output must be new')
    out.mkdir(parents=True,exist_ok=True)
    spec=json.loads((a.full_ensemble/'checkpoint_inputs.json').read_text())
    jobs=[j for j in spec['jobs'] if j['sample']['sample_id']>=0]
    if len(jobs)!=50:raise ValueError('D8 tuning requires 50 machines')
    references={str(scale):{r['sample_id']:r for r in json.loads((path/'capture_robustness_raw.json').read_text())['realizations']}
                for scale,path in ((0.,a.zero_ensemble),(.25,a.quarter_ensemble))}
    # Changing a source realization or the search implementation invalidates resume.
    signature={'source':spec,'references':references,
               'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'search_sha256':hashlib.sha256(Path('src/nkm_injection/injection_tuning.py').read_bytes()).hexdigest()}
    signature=json.loads(json.dumps(signature));signature_path=out/'tuning_inputs.json'
    if signature_path.exists() and json.loads(signature_path.read_text())!=signature:raise SystemExit('Tuning inputs changed')
    signature_path.write_text(json.dumps(signature,indent=2)+'\n')
    rows=[];tasks=[]
    for job in jobs:
        identifier=job['sample']['sample_id'];path=out/f'tuning_{identifier}.json'
        if a.resume and path.exists():rows.append(json.loads(path.read_text()));continue
        tasks.append({'source':job,'untuned':{scale:ref[identifier] for scale,ref in references.items()},'checkpoint':str(path)})
    rows+=parallel_map(tune_machine,tasks,n_workers=a.workers,desc='D8 reduced tuning')
    rows.sort(key=lambda r:r['sample_id']);statistics={}
    for scale in (0.,.25):
        pairs=[next(h for h in r['heldout'] if h['jitter_scale']==scale) for r in rows]
        before=np.array([h['untuned']['models']['fieldmap_3d']['capture_fraction'] for h in pairs])
        after=np.array([h['tuned']['models']['fieldmap_3d']['capture_fraction'] for h in pairs]);diff=after-before
        rng=np.random.default_rng(1729);boot=diff[rng.integers(0,len(diff),(10000,len(diff)))].mean(axis=1)
        statistics[str(scale)]={'untuned':cluster_stats(before,1729,10000,.8),'tuned':cluster_stats(after,1729,10000,.8),
                                'paired_gain':float(diff.mean()),'gain_ci95':np.quantile(boot,[.025,.975]).tolist()}
    result={'rows':rows,'statistics':statistics,'training_particles':100,'heldout_particles':jobs[0]['particles'],
            'training_scope':'static-machine errors only; independent training particles; all shot errors zero',
            'validation_scope':'same held-out particles and joint error draws as zero/quarter-jitter ensembles',
            'optimizer':'one bounded coordinate sweep, seven evaluations, fixed seed per machine',
            'bootstrap':{'unit':'joint realization','seed':1729,'count':10000},
            'units':'x m, canonical angle rad, field scale dimensionless'}
    (out/'tuning_summary.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
