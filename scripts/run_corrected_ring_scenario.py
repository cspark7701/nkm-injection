#!/usr/bin/env python3
"""D5: 10 seeded corrected ring-error scenarios, orbit/tune residuals and native DA."""
import argparse
from dataclasses import asdict,replace
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import at
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring
from nkm_injection.ring_error_scenario import (RingErrorScenario,apply_errors,bpm_orbit,response_matrix,correct_orbit,correct_tunes)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-config',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--seeds',nargs='+',type=int,default=list(range(5501,5511)))
    p.add_argument('--turns',type=int,default=500)
    p.add_argument('--resume',action='store_true')
    p.add_argument('--orbit-tolerance-um',type=float,default=100.,
                   help='Declared scenario RMS acceptance, distinct from an as-built orbit specification')
    a=p.parse_args();out=a.output_dir
    if out.exists() and any(out.iterdir()) and not a.resume: raise SystemExit('Output must be new')
    out.mkdir(parents=True,exist_ok=True)
    base=cached_ring(InjectionStudyConfig.load(a.study_config),Path.cwd(),out/'_lattice')
    ideal=base.ring_c.disable_6d(copy=True)
    bpms=np.array([i for i,e in enumerate(ideal) if 'BPM' in e.FamName])
    correctors=np.array([i for i,e in enumerate(ideal) if isinstance(e,at.Corrector)])
    if len(correctors)!=120 or len(bpms)==0: raise RuntimeError('Expected 120 HVC correctors and BPM markers')
    target_tunes=np.asarray(ideal.get_tune())[:2]
    response_path=out/'response.npy'
    if response_path.exists() and a.resume: response=np.load(response_path)
    else:
        print('Building coupled numerical orbit response',flush=True)
        response=response_matrix(ideal,bpms,correctors);np.save(response_path,response)
    cfg=replace(RingErrorScenario(),orbit_tolerance_m=a.orbit_tolerance_um*1e-6);rows=[]
    for seed in a.seeds:
        file=out/f'seed{seed}.json'
        if file.exists() and a.resume: rows.append(json.loads(file.read_text()));continue
        start=time.time();print('Correcting seed',seed,flush=True)
        commissioning=[];previous=np.zeros((len(correctors),2))
        for fraction in np.linspace(.1,1.,10):
            stage_cfg=replace(cfg,**{key:getattr(cfg,key)*fraction for key in
                ('girder_offset_std_m','magnet_offset_std_m','roll_std_rad','gradient_rel_std',
                 'sextupole_rel_std','skew_quad_relative_std')})
            lattice,errors=apply_errors(base.ring_c,seed,stage_cfg);lin=lattice.disable_6d(copy=True)
            for j,index in enumerate(correctors): lin[index].KickAngle=previous[j].copy()
            step=correct_orbit(lin,bpms,correctors,response,cfg)
            commissioning.append({'error_fraction':float(fraction),'correction':step})
            previous=np.array([lin[index].KickAngle for index in correctors])
        initial_tunes=np.asarray(lin.get_tune())[:2]
        correction=commissioning[-1]['correction']
        qf=lin.get_uint32_index('Q11');qd=lin.get_uint32_index('Q12')
        tune_correction=correct_tunes(lin,[qf,qd],target_tunes,tolerance=cfg.tune_tolerance)
        final_tunes=np.asarray(lin.get_tune())[:2]
        correction_after_tune=correct_orbit(lin,bpms,correctors,response,cfg)
        for dst,src in zip(lattice,lin):
            if hasattr(src,'KickAngle'): dst.KickAngle=src.KickAngle.copy()
            if hasattr(src,'PolynomB'): dst.PolynomB=src.PolynomB.copy()
        orbit,_=lattice.find_orbit6()
        xs=np.arange(-16.,16.01,.5)*1e-3
        b=np.zeros((6,len(xs)));b[0]=xs;b+=orbit[:,None]
        _,_,loss=lattice.track(b,nturns=a.turns,losses=True,in_place=True)
        alive=~np.asarray(loss['loss_map']['islost'],bool)
        neg=xs[(xs<0)&alive];pos=xs[(xs>0)&alive]
        feasibility=correction_after_tune['feasible'] and np.max(np.abs(final_tunes-target_tunes))<=cfg.tune_tolerance
        row={'seed':seed,'scenario':asdict(cfg),'errors':errors,'initial_tunes':initial_tunes.tolist(),
             'target_tunes':target_tunes.tolist(),'final_tunes':final_tunes.tolist(),
             'commissioning':commissioning,'initial_tune_definition':'full errors after staged orbit correction, before tune correction',
             'tune_residual':(final_tunes-target_tunes).tolist(),'correction':correction,'tune_correction':tune_correction,
             'correction_after_tune':correction_after_tune,'feasible':bool(feasibility),
             'da_x_m':xs.tolist(),'da_alive':alive.tolist(),'da_negative_extent_m':float(neg.min()) if len(neg) else None,
             'da_positive_extent_m':float(pos.max()) if len(pos) else None,
             'turns':a.turns,'particle_count':len(xs),'distribution':'single-particle horizontal line, 0.5 mm grid',
             'energy_spread':0.,'initial_twiss':'not applicable to single-particle DA',
             'apertures':'septum only; D6 adds chamber','loss_definition':'native AT loss before final turn',
             'observation':'NKM centre','runtime_s':time.time()-start}
        at.save_mat(lattice,out/f'seed{seed}.mat')
        file.write_text(json.dumps(row,indent=2,allow_nan=False)+'\n');rows.append(row)
        print(seed,'feasible',feasibility,'DA',row['da_negative_extent_m'],row['da_positive_extent_m'],flush=True)
    summary={'rows':rows,'seeds':a.seeds,'source_sha256':hashlib.sha256(Path('K4GSR_HBIv4-1.mat').read_bytes()).hexdigest(),
             'bpm_count':len(bpms),'corrector_count':len(correctors),'passed':all(r['feasible'] for r in rows),
             'scope':'selected error/correction scenario; not as-built KLS prediction'}
    (out/'corrected_ring_summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    if not summary['passed']: raise SystemExit('Correction residual gate failed')


if __name__=='__main__':main()
