#!/usr/bin/env python3
"""Compare the selected round-3 observables of two campaign directories (R4-BTS-03).

Reports, per stage, the largest absolute change of every selected number between a
reference campaign and a rerun; losses as fractions, clearances in m, phase in deg.
"""
import argparse
import json
from pathlib import Path


def selected(c):
    load = lambda s: json.loads((c / s).read_text())
    out = {}
    for stage in ('steering', 'test'):
        for variant, designs in load(f'{stage}/{stage}.json')['summary'].items():
            for name, e in designs.items():
                key = f'{stage}/{variant}/{name}'
                out[key + '/predicted_loss_max_mean'] = e['predicted_loss_max_mean']
                out[key + '/predicted_loss_union_mean'] = e['predicted_loss_union_mean']
                out[key + '/lost_particles'] = e['lost_particles']
                out[key + '/mean_clearance_m'] = e['mean_clearance_m']
    for name, interval in load('test/test.json')['paired_loss_fraction_vs_reference'].items():
        out[f'test/paired/{name}/mean'] = interval['mean']
    pools = load('phase/phase.json')['pools']
    for label, pool in pools.items():
        out[f'phase/{label}/solutions'] = pool['solutions']
        out[f'phase/{label}/mu_min_deg'], out[f'phase/{label}/mu_max_deg'] = pool['mu_x_range_deg']
    robust = load('robust/robust.json')
    out['robust/selected_start'] = robust['selected_start']
    for name, d in robust['designs'].items():
        out[f'robust/{name}/mu_x_deg'] = d['mu_x_deg']
        out[f'robust/{name}/loss_max'] = d['loss_max']
    best = load('exit/exit.json')['dispersion_free_best']
    out['exit/best_mu_x_deg'], out['exit/best_loss_max'] = best['mu_x_deg'], best['loss_max']
    for i, row in enumerate(load('sensitivity/sensitivity.json')['rows']):
        for name, e in row['designs'].items():
            out[f'sensitivity/{i}/{name}/predicted_loss_max_mean'] = e['predicted_loss_max_mean']
    for name, d in load('apertures/apertures.json')['designs'].items():
        out[f'apertures/{name}/minimum_m'] = d['minimum_m']
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('reference', type=Path)
    p.add_argument('rerun', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    ref, new = selected(a.reference), selected(a.rerun)
    rows = []
    for key in ref:
        r, n = ref[key], new[key]
        change = None if isinstance(r, str) else abs(n - r)
        rel = None if isinstance(r, str) or r == 0 else change / abs(r)
        rows.append({'key': key, 'reference': r, 'rerun': n, 'abs_change': change, 'rel_change': rel,
                     'identical': r == n})
    numeric = [x for x in rows if x['rel_change'] is not None]
    report = {'reference': str(a.reference), 'rerun': str(a.rerun), 'rows': rows,
              'identical': sum(x['identical'] for x in rows), 'total': len(rows),
              'max_rel_change': max(x['rel_change'] for x in numeric),
              'max_rel_key': max(numeric, key=lambda x: x['rel_change'])['key']}
    a.output.write_text(json.dumps(report, indent=2) + '\n')
    print(report['identical'], '/', report['total'], 'identical; max relative change',
          f"{report['max_rel_change']:.3g}", 'at', report['max_rel_key'])


if __name__ == '__main__':
    main()
