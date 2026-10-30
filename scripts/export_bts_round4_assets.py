#!/usr/bin/env python3
"""Install round-four BTS summaries, tables, macros and figures (consolidated R4-BTS tasks).

Reads stage outputs under the round-4 campaign and writes only to
docs/paper_bts/generated/round4_* and docs/paper_bts/figures/round4_*.
Macros use mm, mrad, urad and percent as stated in their names.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'docs/paper_bts'
CAMPAIGN = ROOT / 'results/bts_round4_campaign_20261030'
plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42, 'pdf.compression': 6})
COLORS = {'reference': '#1f5fa8', 'low_beta': '#d1495b', 'robust': '#2a9d55', 'scan_best': '#7b3294', 'free_best': '#e08214'}
SHORT = {'reference': 'Matched', 'low_beta': 'Low beta', 'robust': 'Loss-based', 'scan_best': 'Scan best',
         'free_best': 'Disp.-free'}


def load(stage, name):
    return json.loads((CAMPAIGN / stage / name).read_text())


def macros(name, values):
    """Write \\BtsRFour<key> macros to generated/round4_<name>.tex."""
    text = '% Exported by scripts/export_bts_round4_assets.py; do not edit.\n'
    text += ''.join('\\newcommand{\\BtsRFour' + k + '}{' + v + '}\n' for k, v in values.items())
    (P / 'generated' / f'round4_{name}.tex').write_text(text)


def sci(value, digits=2):
    """Percent value as siunitx \\num with ``digits`` significant figures."""
    return '\\num{' + f'{value:.{digits - 1}e}' + '}'


def jitter():
    """R4-BTS-01: jitter in beam-size units and the jitter-level sweep table."""
    data = load('jitter_b', 'jitter.json')
    u = data['beam_units']
    rows = data['rows']
    full = next(r for r in rows if r['scale'] == 1.0)
    x_ratio, xp_ratio = full['jitter']['x_m'] / u['m1_beam_size_m'], full['jitter']['xp_rad'] / u['m1_beam_divergence_rad']
    exit_ref = full['designs']['reference']['exit_jitter_m_rad'][0] / u['m4_beam_size_m']
    exit_rob = full['designs']['robust']['exit_jitter_m_rad'][0] / u['m4_beam_size_m']
    lines = ['\\begin{tabular}{rrrrrrr}\\toprule',
             'Jitter & \\multicolumn{2}{c}{At m1 [beam sizes]} & \\multicolumn{4}{c}{Jitter-integrated loss, steered [\\%]}\\\\',
             '\\cmidrule(lr){2-3}\\cmidrule(lr){4-7}',
             'scale & position & angle & Matched & Low beta & Loss-based & Error-free matched\\\\\\midrule']
    for r in rows:
        d = r['designs']
        lines.append(f"{r['scale']:g} & {r['jitter']['x_m'] / u['m1_beam_size_m']:.2f} & {r['jitter']['xp_rad'] / u['m1_beam_divergence_rad']:.2f} & "
                     + ' & '.join(sci(100 * d[n]['jitter_integrated_loss_mean']) for n in ('reference', 'low_beta', 'robust'))
                     + f" & {sci(100 * d['reference']['error_free_loss'])}\\\\")
    lines.append('\\bottomrule\\end{tabular}')
    (P / 'generated/round4_jitter_rows.tex').write_text('\n'.join(lines) + '\n')
    get = lambda s, n, k='jitter_integrated_loss_mean': next(r for r in rows if r['scale'] == s)['designs'][n][k]
    realistic = max(get(s, n) for s in (0.1, 0.2) for n in ('reference', 'low_beta', 'robust'))
    macros('jitter', {
        'JitPosSigma': f'{x_ratio:.1f}', 'JitAngSigma': f'{xp_ratio:.1f}',
        'JitActionRatio': f"{u['centroid_action_over_emittance']:.0f}",
        'ExitJitSigmaRef': f'{exit_ref:.1f}', 'ExitJitSigmaRobust': f'{exit_rob:.1f}',
        'BeamSizeMOneMm': f"{u['m1_beam_size_m'] * 1e3:.3f}", 'BeamDivMOneUrad': f"{u['m1_beam_divergence_rad'] * 1e6:.0f}",
        'RealisticMaxLoss': sci(realistic, 1).replace('\\num{', '').replace('}', ''),
        'FullRefPct': f"{100 * get(1.0, 'reference'):.2f}", 'FullRobustPct': f"{100 * get(1.0, 'robust'):.2f}",
        'FullRefFreePct': f"{100 * get(1.0, 'reference', 'error_free_loss'):.2f}",
        'FullRobustFreePct': f"{100 * get(1.0, 'robust', 'error_free_loss'):.2f}",
        'StaticRefPct': f"{100 * (get(1.0, 'reference') / get(1.0, 'reference', 'error_free_loss') - 1):.0f}",
        'StaticRobustPct': f"{100 * (get(1.0, 'robust') / get(1.0, 'robust', 'error_free_loss') - 1):.0f}",
        'GainFull': f"{get(1.0, 'reference') / get(1.0, 'robust'):.1f}",
        'GainHalf': f"{get(0.5, 'reference') / get(0.5, 'robust'):.0f}",
        'SampledRefPct': f"{100 * get(1.0, 'reference', 'predicted_loss_max_mean'):.2f}",
    })
    (P / 'generated/round4_jitter.json').write_text(json.dumps({'source': str(CAMPAIGN / 'jitter_b/jitter.json'), 'beam_units': u,
                                                                  'rows': [{'scale': r['scale'], **{n: {k: e[k] for k in ('jitter_integrated_loss_mean', 'predicted_loss_max_mean', 'error_free_loss', 'exit_jitter_m_rad')}
                                                                                                     for n, e in r['designs'].items()}} for r in rows]}, indent=2) + '\n')


PARTS = {'jitter': jitter}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--part', choices=sorted(PARTS) + ['all'], default='all')
    a = p.parse_args()
    for name, fn in PARTS.items():
        if a.part in (name, 'all'):
            fn()


if __name__ == '__main__':
    main()
