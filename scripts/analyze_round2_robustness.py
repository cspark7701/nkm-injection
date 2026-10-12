#!/usr/bin/env python3
"""Final D8 joint-realization statistics, paired jitter and conditional rankings."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from nkm_injection.revision_statistics import capture_by_id,paired_capture_difference,holm_adjust
from run_capture_robustness import cluster_stats
from analyze_capture_robustness import SCALARS,VECTORS,partial_spearman


def analyze(root):
    inputs={}
    def load(folder,name='capture_robustness_raw.json'):
        path=root/folder/name;payload=path.read_bytes();inputs[str(path)]=hashlib.sha256(payload).hexdigest()
        return json.loads(payload)
    combined=[load(f'd8_seed{seed}') for seed in (42,123,777)]
    rows=[r for d in combined for r in d['realizations'] if r['sample_id']>=0]
    pooled={model:cluster_stats([r['models'][model]['capture_fraction'] for r in rows],1729,10000,.8)
            for model in ('fieldmap_3d','dipole')}
    paired=paired_capture_difference({i:r['models']['dipole']['capture_fraction'] for i,r in enumerate(rows)},
                                    {i:r['models']['fieldmap_3d']['capture_fraction'] for i,r in enumerate(rows)})
    baseline=load('d8_jitter_0');reference=capture_by_id(baseline);jitter={}
    indexed={r['sample_id']:r for r in baseline['realizations'] if r['sample_id']>=0}
    for level in ('0','0.25','0.5','0.75','1','x_only','xp_only'):
        raw=combined[0] if level=='1' else load(f'd8_jitter_{level}')
        if raw['cli']['seed']!=42 or raw['cli']['samples']!=50:raise ValueError('Unpaired ensemble settings')
        for r in raw['realizations']:
            if r['sample_id']<0:continue
            old=indexed[r['sample_id']]
            if (old['beam_seed'],old['ring_error_seed'])!=(r['beam_seed'],r['ring_error_seed']):
                raise ValueError('Jitter comparison changes particles or ring draw')
        a=dict(baseline['error_config']);b=dict(raw['error_config'])
        for name in ('booster_x_jitter_std_m','booster_xp_jitter_std_rad'):a.pop(name);b.pop(name)
        if a!=b or baseline['study_config']!=raw['study_config'] or baseline['chamber']!=raw['chamber']:
            raise ValueError('Jitter comparison changes non-jitter inputs')
        jitter[level]=paired_capture_difference(reference,capture_by_id(raw))
        jitter[level]['mean_ci95']=cluster_stats(list(capture_by_id(raw).values()),1729,10000,.8)['mean_ci95_cluster_bootstrap']
        jitter[level]['dipole']=cluster_stats(list(capture_by_id(raw,'dipole').values()),1729,10000,.8)
    feature_rows=[];captures=[];ring_counts={}
    scalar=SCALARS+('septum_strength_rel','rf_phase_rad','arrival_time_s')
    for seed,raw in zip((42,123,777),combined):
        spec=load(f'd8_seed{seed}','checkpoint_inputs.json')
        jobs={j['sample']['sample_id']:j for j in spec['jobs']}
        for r in raw['realizations']:
            if r['sample_id']<0:continue
            job=jobs[r['sample_id']];s=job['sample']
            f={key:abs(s[key]) for key in scalar}
            f.update({f'rms_{key}':float(np.sqrt(np.mean(np.square(s[key])))) for key in VECTORS})
            f.update({key:abs(value) for key,value in job['extra'].items()})
            for ringseed in raw['ring_population'][1:]:f[f'ring_indicator_{ringseed}']=float(r['ring_error_seed']==ringseed)
            feature_rows.append(f);captures.append(r['models']['fieldmap_3d']['capture_fraction'])
            key=str(r['ring_error_seed']);ring_counts[key]=ring_counts.get(key,0)+1
    features={key:np.array([r[key] for r in feature_rows]) for key in feature_rows[0]
              if np.ptp([r[key] for r in feature_rows])>0}
    correlations=[r for r in partial_spearman(features,captures) if not r['variable'].startswith('ring_indicator_')]
    for row,q in zip(correlations,holm_adjust([r['p_value'] for r in correlations])):row['p_holm']=float(q)
    return {'pooled':pooled,'nkm_minus_dipole':paired,'paired_jitter':jitter,'partial_correlations':correlations,
            'ring_draw_counts':ring_counts,'inputs_sha256':inputs,
            'ranking_scope':'partial ranks control other sampled magnitudes and saved ring identity; Holm family is sampled errors',
            'statistical_unit':'joint realization, conditional on the finite population of ten corrected rings',
            'bootstrap':{'seed':1729,'count':10000},'declared_loss_margin':.01,
            'units':'capture fractions; paired differences in capture fraction, not percent'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--campaign',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    a.output.write_text(json.dumps(analyze(a.campaign),indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
