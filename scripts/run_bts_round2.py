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
from nkm_injection.bts_journal import JournalBeam,lattice_for,apply_static
from nkm_injection.bts_round2 import station_record

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


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage',choices=['stations'],required=True);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=False)
    save(args.output_dir/'configuration.json',{'stage':args.stage,'protocol':json.loads((PAPER/'round2_protocol.json').read_text()),'environment':environment()})
    globals()[args.stage](args.output_dir)


if __name__=='__main__':main()
