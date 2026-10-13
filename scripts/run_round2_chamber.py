#!/usr/bin/env python3
"""D6: declared aperture profile, ideal/corrected rings, paired capture and loss maps."""
import argparse
from dataclasses import asdict,replace
import json
from pathlib import Path
import time
import at
from nkm_injection.bts_lattice import create_bts_lattice
from nkm_injection.chamber import ChamberProfile,apply_chamber
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring,booster_beam,track_bts,injected_beam_at_septum,track_injection,wilson_interval
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.ring_error_scenario import refresh_prepared_ring
from nkm_injection.wire_field import FilamentNKMKicker,CalibratedControl,calibrate_controls
from nkm_injection.concurrency import parallel_map


def run_capture_case(job):
    cfg=InjectionStudyConfig.from_dict(job['config']);ring=job['ring'];seed=job['seed']
    from nkm_injection.bts_lattice import BTSConfig
    bts=create_bts_lattice(BTSConfig.from_dict(job['bts']))
    beam=track_bts(bts,booster_beam(job['initial_twiss'],cfg.injected_beam,job['particles'],seed))
    beam=injected_beam_at_septum(cfg,ring,seed,bts_exit_beam=beam)
    lo,hi=job.get('chunk',(0,job['particles']))
    beam=beam[:,lo:hi]
    t=time.time();model=job['model']
    chamber=job.get('kicker_chamber') or {}
    kicker=FilamentNKMKicker(cfg,n_slices=640,**chamber) if model=='fieldmap_3d' else CalibratedControl(model,*job['calibration'],**chamber)
    result=track_injection(cfg,ring,kicker,beam,'element',n_turns=job['turns'])
    result.pop('final_coordinates',None)
    row={'ring':job['ring_label'],'profile':job['profile_label'],'chamber':job['chamber'],'seed':seed,
         'model':model,'chunk':[lo,hi],'runtime_s':time.time()-t,**result}
    for record in row['ring_loss_records']:record['particle']+=lo
    print(job['ring_label'],job['profile_label'],seed,model,result['capture_fraction'],flush=True)
    return row


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-config',type=Path,required=True)
    p.add_argument('--optimization-summary',type=Path,required=True)
    p.add_argument('--corrected-dir',type=Path)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--particles',type=int,default=500)
    p.add_argument('--turns',type=int,default=500)
    p.add_argument('--resume',action='store_true')
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--ring-scope',choices=('ideal','corrected','all'),default='all')
    p.add_argument('--chunk',type=int,default=100)
    p.add_argument('--nkm-magnet-half-mm',type=float,nargs=2,default=None,
                   help='round 3: flat in-magnet NKM chamber half-width and half-height (mm), applied to every profile')
    a=p.parse_args();out=a.output_dir
    if out.exists() and any(out.iterdir()) and not a.resume: raise SystemExit('Output must be new')
    out.mkdir(parents=True,exist_ok=True)
    cfg=InjectionStudyConfig.load(a.study_config);sel=load_optimization_handoff(a.optimization_summary)
    base=cached_ring(cfg,Path.cwd(),out/'_lattice');calibration=calibrate_controls(cfg)
    profiles={'reference_open_rectangle':ChamberProfile(),
              'reference_open_ellipse':ChamberProfile(shape='ellipse'),
              'closed_rectangle':ChamberProfile(ivu_half_y_m=.0025),
              'closed_ellipse':ChamberProfile(ivu_half_y_m=.0025,shape='ellipse')}
    for hx in (.010,.012,.015):
        for hy in (.00487,.0075,.009):
            profiles[f'scan_x{hx*1e3:g}_y{hy*1e3:g}']=ChamberProfile(arc_half_x_m=hx,arc_half_y_m=hy,
                centre_bend_half_y_m=min(.00487,hy),ivu_half_y_m=hy)
    if a.nkm_magnet_half_mm:
        profiles={k:replace(v,nkm_magnet_half_x_m=a.nkm_magnet_half_mm[0]*1e-3,nkm_magnet_half_y_m=a.nkm_magnet_half_mm[1]*1e-3)
                  for k,v in profiles.items()}
    lattice_files={'ideal':None}
    if a.corrected_dir:
        d=json.loads((a.corrected_dir/'corrected_ring_summary.json').read_text())
        if not d['passed']: raise SystemExit('D5 gate has not passed')
        lattice_files.update({f'seed{s}':a.corrected_dir/f'seed{s}.mat' for s in d['seeds']})
    if a.ring_scope=='corrected':lattice_files.pop('ideal')
    elif a.ring_scope=='ideal':lattice_files={'ideal':None}
    rows=[]
    for label,source in lattice_files.items():
        for name,profile in profiles.items():
            if label!='ideal' and name.startswith('scan_'):continue
            filename=out/f'{label}_{name}.json'
            if filename.exists() and a.resume:rows.extend(json.loads(filename.read_text())['rows']);continue
            lattice=base.ring_c if source is None else at.load_mat(source)
            chamber,assignment=apply_chamber(lattice,profile,cfg.septum_edge_x_m)
            ring=refresh_prepared_ring(base,chamber)
            jobs=[{'config':cfg.to_dict(),'ring':ring,'seed':seed,'bts':sel.bts.to_dict(),
                   'initial_twiss':sel.initial_twiss,'particles':a.particles,'turns':a.turns,
                   'model':model,'calibration':calibration,'ring_label':label,'profile_label':name,
                   'chamber':asdict(profile),'kicker_chamber':profile.kicker_kwargs(),'chunk':(lo,min(a.particles,lo+a.chunk))}
                  for seed in (1001,1002) for model in ('fieldmap_3d','dipole') for lo in range(0,a.particles,a.chunk)]
            case=parallel_map(run_capture_case,jobs,n_workers=a.workers,desc=f'D6 {label} {name}')
            filename.write_text(json.dumps({'rows':case,'assignment':assignment},indent=2,allow_nan=False)+'\n');rows.extend(case)
    summary={'rows':rows,'study_config':cfg.to_dict(),'optimization_source':sel.source,
             'statistical_unit':'particle for nominal Wilson intervals, ring seed for scenario distribution',
             'initial_twiss':sel.initial_twiss,'distribution':'Gaussian design-emittance bunch transported through matched BTS',
             'loss_definition':'native AT loss before final turn, septum or conductor/domain loss',
             'observation':'NKM centre','scope':'declared chamber bracket and 19 ordinary-straight IVU assignments, not surveyed KLS geometry'}
    (out/'chamber_summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
