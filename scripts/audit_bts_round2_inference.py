#!/usr/bin/env python3
"""Reconstruct round-two machine inference; clearance m, transmission fraction."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta

ROOT=Path(__file__).resolve().parents[1]


def reconstruct(campaign):
    summary=json.loads((campaign/'comparison/comparison.json').read_text())
    blocks=json.loads((campaign/'comparison/machine_results.json').read_text())
    raw=json.loads((campaign/'comparison/raw_realizations.json').read_text())
    protocol=summary['protocol'];n=protocol['machines'];shots=protocol['shots_per_machine'];particles=protocol['particles_per_shot']
    rng=np.random.default_rng(protocol['bootstrap_seed']);indices=rng.integers(0,n,(protocol['bootstrap_count'],n))
    results={}
    for regime,designs in summary['results'].items():
        base=np.array([r['results'][regime]['reference']['mean_clearance_m'] for r in blocks])
        reference_loss=np.array([r['results'][regime]['reference']['lost'] for r in raw]).reshape(n,shots).sum(1)/(shots*particles)
        for name,value in designs.items():
            values=np.array([r['results'][regime][name]['mean_clearance_m'] for r in blocks]);delta=values-base
            ci=np.quantile(delta[indices].mean(1),[.025,.975])
            np.testing.assert_allclose(ci,value['paired_difference']['ci95_m'],atol=1e-14,rtol=0)
            np.testing.assert_allclose(delta.mean(),value['paired_difference']['mean_m'],atol=1e-14,rtol=0)
            loss=np.array([r['results'][regime][name]['lost'] for r in raw]).reshape(n,shots).sum(1)/(shots*particles)
            transmission_delta=reference_loss-loss
            k=value['loss_blocks'];exact=[0 if k==0 else beta.ppf(.025,k,n-k+1),1 if k==n else beta.ppf(.975,k+1,n-k)]
            np.testing.assert_allclose(exact,value['loss_block_ci95'],atol=1e-14,rtol=0)
            results.setdefault(regime,{})[name]={'paired_transmission_change_fraction':float(transmission_delta.mean()),'paired_transmission_ci95':np.quantile(transmission_delta[indices].mean(1),[.025,.975]).tolist(),'paired_clearance_change_m':float(delta.mean()),'paired_clearance_ci95_m':ci.tolist(),'loss_block_fraction':k/n,'loss_block_ci95':exact,'gain_over_declared_scale':bool(ci[0]>protocol['relevant_clearance_change_m'])}
    return {'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [campaign/'comparison/comparison.json',campaign/'comparison/machine_results.json',campaign/'comparison/raw_realizations.json',Path(__file__).resolve()]},'results':results,'machine_event':f'Any observed particle loss in a randomly generated block of {shots} shots, each with {particles} untruncated Gaussian particles. Not indefinitely operated machine loss.','zero_loss_block_one_sided_upper95':1-.05**(1/n),'inference':'Pointwise descriptive intervals; no simultaneous or rare-tail-convergence claim. Illustrative useful scale 0.1 mm, not a hardware specification.','all_checks_passed':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--campaign-dir',type=Path,default=ROOT/'results/bts_journal_campaign_r2_20261013');parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=False)
    result=reconstruct(args.campaign_dir.resolve());(args.output_dir/'inference.json').write_text(json.dumps(result,indent=2)+'\n');print('Verified all nine clearance intervals and exact block-loss intervals.')


if __name__=='__main__':main()
