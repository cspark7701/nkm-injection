#!/usr/bin/env python3
"""D11 final-point native/affine backend comparison and conditional long-turn checks."""
import argparse
from dataclasses import asdict,replace
import json
from pathlib import Path
import time
import at
import numpy as np
from nkm_injection.chamber import ChamberProfile,apply_chamber
from nkm_injection.bts_lattice import BTSConfig,create_bts_lattice
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring,booster_beam,track_bts,injected_beam_at_septum,track_injection
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.ring_error_scenario import refresh_prepared_ring
from nkm_injection.linear_ring_reference import linearize_ring
from nkm_injection.wire_field import FilamentNKMKicker


def run_job(job):
    cfg=InjectionStudyConfig.from_dict(job['config']);ring=job['ring']
    beam=track_bts(create_bts_lattice(BTSConfig.from_dict(job['bts'])),
                   booster_beam(job['initial_twiss'],cfg.injected_beam,job['particles'],job['seed']))
    beam=injected_beam_at_septum(cfg,ring,job['seed'],bts_exit_beam=beam)
    lo,hi=job['chunk'];beam=beam[:,lo:hi];start=time.time()
    res=track_injection(cfg,ring,FilamentNKMKicker(cfg,n_slices=640),beam,'element',n_turns=job['turns'])
    res.pop('final_coordinates',None)
    # AT loss turns are zero-based. A loss at index t occurs during turn t+1.
    # The longest run therefore also supplies exact shorter survival counts.
    res['survival_counts']={str(t):res['captured']+sum(v>=t for v in res['first_loss_turn'])
                            for t in (100,500,1000,2000,4000) if t<=job['turns']}
    for record in res['ring_loss_records']:record['particle']+=lo
    return {'case':job['case'],'backend_name':job['backend_name'],'seed':job['seed'],'chunk':[lo,hi],
            'runtime_s':time.time()-start,**res}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-config',type=Path,required=True);p.add_argument('--optimization-summary',type=Path,required=True)
    p.add_argument('--chamber-config',type=Path,required=True);p.add_argument('--degraded-ring',type=Path,required=True)
    p.add_argument('--edge-offsets-mrad',type=float,nargs=2,required=True)
    p.add_argument('--nominal-reference',type=Path,help='D6 summary for exact paired 500-turn consistency')
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--workers',type=int,default=8)
    p.add_argument('--particles',type=int,default=500);p.add_argument('--chunk',type=int,default=100)
    p.add_argument('--resume',action='store_true');a=p.parse_args();out=a.output_dir
    if out.exists() and any(out.iterdir()) and not a.resume:raise SystemExit('Output must be new')
    out.mkdir(parents=True,exist_ok=True);cfg=InjectionStudyConfig.load(a.study_config)
    sel=load_optimization_handoff(a.optimization_summary);profile=ChamberProfile(**json.loads(a.chamber_config.read_text()))
    base=cached_ring(cfg,Path.cwd(),out/'_lattice');ch,_=apply_chamber(base.ring_c,profile,cfg.septum_edge_x_m)
    reference=refresh_prepared_ring(base,ch);linear=linearize_ring(reference)
    perturbation=np.array([1e-8,2e-9,1e-8,2e-9,1e-8,1e-8])[:,None]
    initial=np.asarray(reference.orbit6)[:,None]+perturbation
    native_check=reference.ring_c.track(initial.copy(),nturns=1)[0][:,:,0,0]
    linear_check=linear.ring_c.track(initial.copy(),nturns=1)[0][:,:,0,0]
    errors=np.abs(native_check-linear_check).ravel()
    if not np.isfinite(errors).all() or np.max(errors)>1e-10:raise ValueError('Affine tangent validation failed')
    if abs(linear.ring_c.circumference-reference.ring_c.circumference)>1e-10:raise ValueError('Affine ring length changed')
    (out/'backend_contract.json').write_text(json.dumps({'perturbation':perturbation.ravel().tolist(),
        'absolute_one_turn_difference':errors.tolist(),'tolerance':1e-10,
        'units':'x,y,ct m; px,py rad; delta dimensionless','length_m':reference.ring_c.circumference,
        'apertures':'explicit zero-length checks before and after each affine element'},indent=2)+'\n')
    degraded,_=apply_chamber(at.load_mat(a.degraded_ring),profile,cfg.septum_edge_x_m)
    degraded=refresh_prepared_ring(base,degraded)
    studies=[('nominal_native','native',reference,cfg,4000)]
    studies.append(('nominal_linear','affine_element_map',linear,cfg,500))
    studies.extend((label,'native',reference,replace(cfg,injection_xp_rad=cfg.injection_xp_rad+offset*1e-3),4000)
                   for label,offset in zip(('lower_edge','upper_edge'),a.edge_offsets_mrad))
    studies.append(('degraded_ring','native',degraded,cfg,4000));rows=[]
    for case,backend,ring,config,turns in studies:
        file=out/f'{case}_{turns}.json'
        if file.exists() and a.resume:rows.extend(json.loads(file.read_text()));continue
        jobs=[{'config':config.to_dict(),'ring':ring,'particles':a.particles,'seed':seed,'initial_twiss':sel.initial_twiss,
               'bts':sel.bts.to_dict(),'turns':turns,'case':case,'backend_name':backend,
               'chunk':(lo,min(a.particles,lo+a.chunk))}
              for seed in ((1001,1002) if case.startswith('nominal') else (2001,2002))
              for lo in range(0,a.particles,a.chunk)]
        result=parallel_map(run_job,jobs,n_workers=a.workers,desc=f'D11 {case} {turns}')
        file.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');rows.extend(result)
        print(case,turns,sum(r['captured'] for r in result)/sum(r['n_particles'] for r in result),flush=True)
    consistency=None
    if a.nominal_reference:
        prior=json.loads(a.nominal_reference.read_text())
        expected={(r['seed'],r.get('chunk',[0])[0]+i):bool(alive)
                  for r in prior['rows'] if r['ring']=='ideal' and r['profile']=='reference_open_ellipse'
                  and r['model']=='fieldmap_3d' for i,alive in enumerate(r['alive_mask'])}
        observed={(r['seed'],r['chunk'][0]+i):bool(alive or lost>=500)
                  for r in rows if r['case']=='nominal_native'
                  for i,(alive,lost) in enumerate(zip(r['alive_mask'],r['first_loss_turn']))}
        if expected!=observed:raise ValueError('4000-turn prefix differs from paired D6 500-turn masks')
        consistency={'particles':len(expected),'identical_500_turn_masks':True,'reference':str(a.nominal_reference)}
    data={'rows':rows,'study_config':cfg.to_dict(),'chamber':asdict(profile),'initial_twiss':sel.initial_twiss,
          'prefix_consistency':consistency,
          'edge_offsets_mrad':a.edge_offsets_mrad,'degraded_ring':str(a.degraded_ring),
          'distribution':'Gaussian design-emittance beam transported through selected matched BTS',
          'interval':'particle Wilson intervals; nominal seeds 1001/1002, fresh edge/degraded seeds 2001/2002',
          'observation':'NKM centre',
          'loss_definition':'septum creation, conductor/domain, native AT ring loss',
          'backend_scope':'affine element tangent maps retain identical physical aperture placement; nonlinear dynamics absent'}
    (out/'validation_summary.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
