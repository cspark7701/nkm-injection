#!/usr/bin/env python3
"""Native 500-turn aperture-limited horizontal acceptance of the final chamber."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import at
import numpy as np
from nkm_injection.chamber import ChamberProfile,apply_chamber
from nkm_injection.concurrency import parallel_map
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring
from nkm_injection.ring_error_scenario import refresh_prepared_ring


def run(job):
    cfg=InjectionStudyConfig.from_dict(job['config']);base=cached_ring(cfg,Path.cwd(),Path(job['work']))
    native=at.load_mat(job['lattice']) if job['lattice'] else base.ring_c
    chamber,_=apply_chamber(native,ChamberProfile(**job['chamber']),cfg.septum_edge_x_m)
    ring=refresh_prepared_ring(base,chamber);x=np.arange(-.016,.01601,.0005)
    beam=np.repeat(np.asarray(ring.orbit6)[:,None],len(x),axis=1);beam[0]+=x
    _,_,info=ring.ring_c.track(beam,nturns=500,losses=True,in_place=True)
    alive=~np.asarray(info['loss_map']['islost'],bool)
    first=[]
    for sign in (-1,1):
        pairs=sorted([(abs(v),bool(a)) for v,a in zip(x,alive) if v*sign>1e-12])
        first.append(next((sign*v for v,a in pairs if not a),None))
    print(job['label'],first,flush=True)
    return {'ring':job['label'],'da_x_m':x.tolist(),'da_alive':alive.tolist(),
            'first_unstable_negative_positive_m':first,'grid_step_m':.0005,
            'initial_twiss':{'x':ring.twiss_x,'y':ring.twiss_y},'orbit6':np.asarray(ring.orbit6).tolist()}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--study-config',type=Path,required=True)
    p.add_argument('--chamber-config',type=Path,required=True);p.add_argument('--corrected-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--workers',type=int,default=4);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    cfg=InjectionStudyConfig.load(a.study_config);profile=ChamberProfile(**json.loads(a.chamber_config.read_text()))
    source=json.loads((a.corrected_dir/'corrected_ring_summary.json').read_text())
    if not source['passed']:raise SystemExit('Corrected-ring gate failed')
    labels=[('ideal',None)]+[(f'seed{s}',str(a.corrected_dir/f'seed{s}.mat')) for s in source['seeds']]
    jobs=[{'config':cfg.to_dict(),'chamber':asdict(profile),'label':label,'lattice':lattice,
           'work':str(a.output.parent/'_lattice')} for label,lattice in labels]
    rows=parallel_map(run,jobs,n_workers=a.workers,desc='D6 chamber DA')
    data={'rows':rows,'chamber':asdict(profile),'study_config':cfg.to_dict(),'turns':500,'particles_per_ring':65,
          'distribution':'deterministic horizontal grid about each corrected 6-D closed orbit',
          'energy_spread':0.,'launch':'px=py=y=delta=ct offsets zero; x grid in m',
          'observation':'NKM centre','loss_definition':'native AT including final chamber and septum',
          'scope':'aperture-limited horizontal acceptance; not a finite-emittance capture window'}
    a.output.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
