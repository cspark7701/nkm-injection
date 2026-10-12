#!/usr/bin/env python3
"""Design-beam centroid window with a fixed chamber; x in m and angle in rad."""
import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path
import numpy as np
from nkm_injection.chamber import ChamberProfile, apply_chamber
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig, cached_ring
from nkm_injection.optimization_handoff import load_optimization_handoff
from nkm_injection.ring_error_scenario import refresh_prepared_ring
from nkm_injection.wire_field import calibrate_controls
from run_round2_chamber import run_capture_case


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-config',type=Path,required=True)
    p.add_argument('--optimization-summary',type=Path,required=True)
    p.add_argument('--chamber-config',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--particles',type=int,default=500)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--resume',action='store_true')
    a=p.parse_args();out=a.output_dir
    if out.exists() and any(out.iterdir()) and not a.resume:raise SystemExit('Output must be new')
    out.mkdir(parents=True,exist_ok=True)
    cfg=InjectionStudyConfig.load(a.study_config);sel=load_optimization_handoff(a.optimization_summary)
    profile=ChamberProfile(**json.loads(a.chamber_config.read_text()))
    base=cached_ring(cfg,Path.cwd(),out/'_lattice')
    lattice,_=apply_chamber(base.ring_c,profile,cfg.septum_edge_x_m)
    ring=refresh_prepared_ring(base,lattice);calibration=calibrate_controls(cfg);rows=[]
    def point(axis,offset):
        offset=float(round(offset,8));label=f'{axis}_{offset:+.2f}'
        path=out/f'{label}.json'
        if path.exists() and a.resume:
            case=json.loads(path.read_text());rows.extend(case)
            return sum(r['captured'] for r in case)/sum(r['n_particles'] for r in case)
        config=replace(cfg,**({'injection_xp_rad':cfg.injection_xp_rad+offset*1e-3} if axis=='angle'
                              else {'injection_x_m':cfg.injection_x_m+offset*1e-3}))
        jobs=[{'config':config.to_dict(),'ring':ring,'seed':seed,'bts':sel.bts.to_dict(),
               'initial_twiss':sel.initial_twiss,'particles':a.particles,'turns':500,
               'model':'fieldmap_3d','calibration':calibration,'ring_label':'ideal','profile_label':label,
               'chamber':asdict(profile),'chunk':(lo,min(a.particles,lo+100))}
              for seed in (1001,1002) for lo in range(0,a.particles,100)]
        case=parallel_map(run_capture_case,jobs,n_workers=a.workers,desc=f'D6 window {label}')
        for r in case:r.update(axis=axis,offset_mm_or_mrad=offset)
        path.write_text(json.dumps(case,indent=2,allow_nan=False)+'\n');rows.extend(case)
        return sum(r['captured'] for r in case)/sum(r['n_particles'] for r in case)
    # Fixed coarse grid plus a predeclared one-step refinement of every 80%
    # crossing to 0.1 mm/mrad spacing. The operating point is never reselected.
    for axis in ('angle','position'):
        offsets=list(np.linspace(-1.2,1.2,13))
        captures=[point(axis,value) for value in offsets]
        # Extend a boundary that is still above threshold; never change the
        # selected operating point. The fixed 0.2 step and 3.0 limit make the
        # extension deterministic and prevent an unbracketed reported width.
        while captures[0]>=.8 and offsets[0]>-3.+1e-8:
            offsets.insert(0,round(offsets[0]-.2,8))
            captures.insert(0,point(axis,offsets[0]))
        while captures[-1]>=.8 and offsets[-1]<3.-1e-8:
            offsets.append(round(offsets[-1]+.2,8))
            captures.append(point(axis,offsets[-1]))
        if captures[0]>=.8 or captures[-1]>=.8:
            raise ValueError(f'{axis} window not bracketed within the declared extension limit')
        for x0,x1,c0,c1 in zip(offsets[:-1],offsets[1:],captures[:-1],captures[1:]):
            if (c0-.8)*(c1-.8)<0:point(axis,(x0+x1)/2)
    result={'rows':rows,'threshold':.8,'study_config':cfg.to_dict(),'chamber':asdict(profile),
            'selection':'fixed selected centroid; initial +/-1.2 grid extended in 0.2 mm/mrad steps if unbracketed, maximum +/-3; 80% crossing cells refined once to 0.1 spacing; no knob reselection',
            'initial_twiss':sel.initial_twiss,'optimization_source':sel.source,
            'distribution':f'Gaussian design beam, 2 seeds x {a.particles} particles per grid point',
            'observation':'NKM centre after 500 native turns; same loss definition as chamber study'}
    (out/'window_summary.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
