#!/usr/bin/env python3
"""Select round-5 paired jitter evidence without changing prior manifests."""
import argparse
import hashlib
import json
from pathlib import Path
from make_round4_manifest import point_identity

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = json.loads((ROOT/'docs/paper/revision_manifest_round4.json').read_text())
    artifacts = dict(base['artifacts'])
    for key, rel in artifacts.items():
        if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() != base['sha256'][key]:
            raise ValueError('Historical evidence changed: '+key)
    additions = {'round5_protocol':'docs/paper/round5_protocol.json',
                 'round5_companion_audit':'docs/paper/round5_companion_audit_final.json',
                 'round5_companion_audit_declared':'docs/paper/round5_companion_audit.json',
                 'round5_jitter':'results/journal_campaign_06/g2_jitter_analysis.json',
                 'round5_preparation':'results/journal_campaign_06/preparation.json',
                 'round5_bts_jitter_reference':'results/bts_round4_campaign_20261030/jitter_b/jitter.json',
                 'round5_bts_article':'docs/paper_bts/paper.pdf',
                 'round5_bts_design_reference':'docs/paper_bts/generated/round2_designs.json',
                 'round5_bts_summary':'docs/paper_bts/generated/round5.json',
                 'round5_implementation':'results/journal_campaign_06/implementation_identity.json',
                 'round5_field_sheet':'nkm_field.xlsx',
                 'round5_expanded_field_sheet':'nkm_field_expanded.xlsx'}
    protocol = json.loads((ROOT/'docs/paper/round5_protocol.json').read_text())
    prep = json.loads((ROOT/protocol['campaign']/'preparation.json').read_text())
    folders = dict(protocol['endpoints'])
    folders.update({s:r['output'] for s,r in prep['variants'].items()})
    for scale, folder in folders.items():
        label = scale.replace('.', 'p')
        additions['round5_raw_'+label] = folder+'/capture_robustness_raw.json'
        additions['round5_jobs_'+label] = folder+'/checkpoint_inputs.json'
    artifacts.update(additions)
    point_identity(artifacts)
    selected = json.loads((ROOT/artifacts['round3_operating_point']).read_text())
    for key, rel in additions.items():
        if not key.startswith('round5_raw_'):
            continue
        cfg = json.loads((ROOT/rel).read_text())['study_config']
        if any(abs(cfg[k]-selected[k]) > 1e-12 for k in ('field_scale','injection_x_m','injection_xp_rad')):
            raise ValueError('New scan point differs from adopted point')
    record = {'description':'Round-5 NKM evidence: unchanged round-4 selection plus the paired two-plane jitter scan.',
              'artifacts':artifacts,
              'sha256':{k:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for k,rel in artifacts.items()}}
    with args.output.open('x') as stream:
        json.dump(record, stream, indent=2);stream.write('\n')
    print('Selected',len(artifacts),'artifact keys')


if __name__ == '__main__':
    main()
