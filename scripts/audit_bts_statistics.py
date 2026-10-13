#!/usr/bin/env python3
"""Reconstruct the historical BTS optical statistics separately from new transport."""
from __future__ import annotations
import argparse
import gc
import json
from pathlib import Path
import numpy as np
from analyze_tolerance_replicates import describe, failure_bounds
from audit_bts_evidence import sha256

ROOT=Path(__file__).resolve().parents[1]


def reconstruct(output):
    output.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/'docs/paper_bts/evidence_manifest.json').read_text())
    artifacts=[a for a in manifest['artifacts'] if a['path'].endswith('publication_tolerances_summary.json')]
    pooled={name:[] for name in ['mismatch_x','mismatch_y','max_beta_x_m','max_beta_y_m']}
    fields={'mismatch_x':'mx','mismatch_y':'my','max_beta_x_m':'bx_max','max_beta_y_m':'by_max'}
    runs=[];failures=[];baseline=None
    for artifact in artifacts:
        path=ROOT/artifact['path'];assert sha256(path)==artifact['sha256']
        data=json.loads(path.read_text());rs=data['robustness_statistics'];samples=rs['sample_results']
        compatibility={key:data[key] for key in ['nominal_bts_config','nominal_strengths_by_name_m_minus2','target_config','constraint_config','error_config','initial_twiss','target_twiss','units']}
        compatibility['thresholds']=rs['evaluation_thresholds']
        if baseline is None:baseline=compatibility
        assert compatibility==baseline,'Cannot pool incompatible runs'
        assert rs['n_invalid_evaluations']==0
        thresholds=rs['evaluation_thresholds'];assert thresholds=={'mismatch_definition':'sum','beta_tolerance_m':.01,'mismatch_tolerance':.05,'beta_max_limit_m':60.,'mismatch_limit':2.}
        calculated_failures=0
        for i,sample in enumerate(samples):
            assert sample['outcome']['status']!='invalid'
            rule=(sample['bx_max']>60.01 or sample['by_max']>60.01 or sample['mx']+sample['my']>2.05)
            assert bool(sample['failed'])==rule,(artifact['path'],i)
            if rule:
                calculated_failures+=1
                failures.append({'seed':data['seed'],'sample_id':i,'mx':sample['mx'],'my':sample['my'],'bx_max_m':sample['bx_max'],'by_max_m':sample['by_max'],'failure_mode':sample['failure_mode']})
        assert calculated_failures==rs['n_physical_failures']
        arrays={name:np.array([s[key] for s in samples]) for name,key in fields.items()}
        for name,values in arrays.items():pooled[name].append(values)
        sizes=data['statistical_policy']['convergence_sizes'];last=sizes[-1];before=sizes[-2]
        delta=abs(np.median(arrays['mismatch_x'][:last])-np.median(arrays['mismatch_x'][:before]))
        runs.append({'seed':data['seed'],'n':len(samples),'failures':calculated_failures,'sha256':artifact['sha256'],'prefix_sizes':sizes,'prefix_delta_mismatch_x':float(delta),'prefix_status':'met' if delta<1e-5 else 'not met','quantiles':describe(arrays,.95),'oat':data['sensitivity_ranking']})
        del data,rs,samples,arrays;gc.collect()
    arrays={name:np.concatenate(values) for name,values in pooled.items()}
    n=len(arrays['mismatch_x']);k=len(failures)
    assert n==550000 and k==5
    result={'source_identity':'artifact digests checked; artifact-specific generating commits may be unavailable','pool_compatibility':'all frozen BTS, entrance/target, error, constraint and unit fields equal; downstream NKM fields not interpreted as BTS response','n_samples':n,'invalid':0,'rule':'beta_x or beta_y >60.01 m OR Mx+My >2.05','failure_bounds':failure_bounds(k,n),'quantiles':describe(arrays,.95),'runs':runs,'all_failure_records':failures,'distribution':'Independent Gaussian draws in the generating error sampler; entrance beta only, alpha held fixed. No truncation/correlation model established for historical budget.','followup_policy':'The 400k run is a follow-up to the earlier runs; a predeclared adaptive stopping policy is not archived. Intervals are descriptive fixed-N calculations and do not certify optional-stopping coverage.','scope':'Historical optics-only feasibility; no physical loss or certified engineering tolerances. New-model heldout transport remains separate.'}
    expected=json.loads((ROOT/'results/journal_campaign_01/followup_analysis/tolerance_replicates_with_400k.json').read_text())['pooled']
    for name in arrays:
        for key in ['p50','p50_ci','p95','p95_ci','p99','p99_ci']:
            np.testing.assert_allclose(result['quantiles'][name][key],expected['quantiles'][name][key],rtol=1e-12,atol=1e-14)
    np.testing.assert_allclose(result['failure_bounds']['clopper_pearson'],expected['failures']['clopper_pearson'],rtol=1e-12)
    (output/'historical_statistics.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(output/'pooled_optical_samples.npz',**arrays)
    print(f'Reconstructed {n} observations, {k} failures and all quantile intervals.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True)
    reconstruct(parser.parse_args().output_dir)
