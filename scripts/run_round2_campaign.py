#!/usr/bin/env python3
"""Run the gated final D8 ensembles, jitter curve and reduced tuning in sequence."""
import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys
from nkm_injection.chamber import ChamberProfile


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign',type=Path,required=True)
    p.add_argument('--optimization-summary',type=Path,required=True)
    p.add_argument('--chamber-config',type=Path,required=True)
    p.add_argument('--workers',type=int,default=12)
    a=p.parse_args();root=a.campaign
    correction=json.loads((root/'d5_selected_scenario/corrected_ring_summary.json').read_text())
    ideal=json.loads((root/'d6_chamber_full/chamber_summary.json').read_text())
    corrected=json.loads((root/'d6_corrected_chamber/chamber_summary.json').read_text())
    if not correction['passed'] or len(correction['seeds'])!=10:raise SystemExit('D5 gate incomplete')
    required={(f'seed{s}',profile) for s in correction['seeds'] for profile in
              ('reference_open_rectangle','reference_open_ellipse','closed_rectangle','closed_ellipse')}
    observed={(r['ring'],r['profile']) for r in corrected['rows']}
    if not required<=observed:raise SystemExit('D6 corrected-ring chamber gate incomplete')
    profile=asdict(ChamberProfile(**json.loads(a.chamber_config.read_text())))
    if not any(r['chamber']==profile for r in ideal['rows']):raise SystemExit('Final reference chamber was not validated')
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MPLBACKEND='Agg')
    def run(script,args,log):
        command=[sys.executable,'scripts/'+script,*map(str,args)]
        print('Running',script,log,flush=True)
        with (root/log).open('a') as handle:
            subprocess.run(command,env=env,stdout=handle,stderr=subprocess.STDOUT,check=True)
    budget=root/'error_budget.json';variants=root/'input_variants';variants.mkdir(exist_ok=True)
    common=['--study-config',root/'operating_point_design_beam.json','--optimization-summary',a.optimization_summary,
            '--chamber-config',a.chamber_config,'--corrected-ring-dir',root/'d5_selected_scenario',
            '--kicker-models','fieldmap_3d','dipole','--control-reference','3d','--timing-model','scale',
            '--correct-static-orbit','--samples','50','--particles','200','--turns','500',
            '--workers',a.workers,'--capture-threshold','.8','--resume']
    for seed in (42,123,777):
        run('run_capture_robustness.py',common+['--seed',seed,'--error-config',budget,'--output-dir',root/f'd8_seed{seed}'],
            f'd8_seed{seed}.log')
    original=json.loads(budget.read_text())
    for label,sx,sxp in (('0',0,0),('0.25',.25,.25),('0.5',.5,.5),('0.75',.75,.75),('x_only',1,0),('xp_only',0,1)):
        values=dict(original);values['booster_x_jitter_std_m']*=sx;values['booster_xp_jitter_std_rad']*=sxp
        path=variants/f'jitter_{label}.json'
        if path.exists() and json.loads(path.read_text())!=values:raise SystemExit('Existing jitter budget changed')
        path.write_text(json.dumps(values,indent=2)+'\n')
        run('run_capture_robustness.py',common+['--seed','42','--error-config',path,'--output-dir',root/f'd8_jitter_{label}'],
            f'd8_jitter_{label}.log')
    if not (root/'d8_final_statistics.json').exists():
        run('analyze_round2_robustness.py',['--campaign',root,'--output',root/'d8_final_statistics.json'],'d8_analysis.log')
    run('run_round2_tuning.py',['--full-ensemble',root/'d8_seed42','--zero-ensemble',root/'d8_jitter_0',
        '--quarter-ensemble',root/'d8_jitter_0.25','--output-dir',root/'d8_tuning','--workers',a.workers,'--resume'],'d8_tuning.log')
    print('D8 numerical campaign complete',flush=True)


if __name__=='__main__':main()
