#!/usr/bin/env python3
"""Install round-three BTS summaries, tables, macros and figures (Reviewer 2 tasks).

Reads stage outputs under the selected campaign and writes only to
docs/paper_bts/generated/round3_* and docs/paper_bts/figures/round3_*.
Macros use mm, mrad and percent as stated in their names.
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
CAMPAIGN = ROOT / 'results/bts_journal_campaign_r3_20261015'
plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42, 'svg.hashsalt': 'bts-r3', 'pdf.compression': 6})
COLORS = {'reference': '#1f5fa8', 'low_beta': '#d1495b', 'robust': '#2a9d55'}
LABELS = {'reference': 'Reference', 'low_beta': 'Refined low beta', 'robust': 'Loss-based'}
SHORT = {'reference': 'Ref.', 'low_beta': 'Low beta', 'robust': 'Loss-based'}


def load(stage, name):
    return json.loads((CAMPAIGN / stage / name).read_text())


def macros(name, values):
    """Write \\BtsR3<key> macros to generated/round3_<name>.tex."""
    text = '% Exported by scripts/export_bts_round3_assets.py; do not edit.\n'
    text += ''.join('\\newcommand{\\BtsR' + 'Three' + k + '}{' + v + '}\n' for k, v in values.items())
    (P / 'generated' / f'round3_{name}.tex').write_text(text)


def strip(data, keys):
    return {k: v for k, v in data.items() if k not in keys}


def apertures():
    a = load('apertures', 'apertures.json')
    summary = {'environment': a['environment'], 'model': a['model'], 'sagitta_m': a['sagitta_m'], 'sweeps': a['sweeps'],
               'designs': {n: strip(d, ['profile', 'apertures']) for n, d in a['designs'].items()}}
    (P / 'generated/round3_apertures.json').write_text(json.dumps(summary, indent=2) + '\n')
    m = a['model']
    rows = [('Drifts', 'round', m['pipe_radius'], m['pipe_radius'], 'assumed, equal to bore'),
            ('Quadrupoles q11--q33', 'round', m['quad_bore_radius'], m['quad_bore_radius'], 'assumed bore'),
            ('Extraction kicker', 'rect.', m['kicker_half'][0], m['kicker_half'][1], 'assumed'),
            ('Extraction septum', 'rect.', m['septum_in_half'][0], m['septum_in_half'][1], 'assumed; swept'),
            ('Bends b1--b3 (curved)', 'rect.', m['dipole_half'][0], m['dipole_half'][1], 'assumed; gap swept'),
            ('Injection septum', 'one-sided', m['septum_ex_blade'], m['septum_ex_half_y'], 'blade from companion')]
    body = '\n'.join(f"{r[0]} & {r[1]} & {1e3 * r[2]:.3f} & {1e3 * r[3]:.2f} & {r[4]} \\\\" for r in rows)
    (P / 'generated/round3_aperture_rows.tex').write_text(
        '\\begin{tabular}{llrrl}\\toprule\nRegion & Shape & $a_x$ [mm] & $a_y$ [mm] & Basis \\\\\\midrule\n' + body +
        '\n\\bottomrule\\end{tabular}\n')
    ref, low = a['designs']['reference'], a['designs']['low_beta']
    fam = ref['family_minimum_m']
    blade = {s['value_m']: s['minimum_m'] for s in a['sweeps'] if s['parameter'] == 'septum_ex_blade_m' and s['design'] == 'reference'}
    macros('apertures', {
        'MinMm': f"{1e3 * ref['minimum_m']:.3f}", 'BladeMm': f"{1e3 * fam['blade_exit_x']:.3f}",
        'SeptInYMm': f"{1e3 * fam['sept_in_y']:.2f}", 'SeptInXMm': f"{1e3 * fam['sept_in_x']:.2f}",
        'InteriorRefMm': f"{1e3 * ref['interior_minimum_m']:.2f}", 'InteriorLowMm': f"{1e3 * low['interior_minimum_m']:.2f}",
        'SagittaBTwoMm': f"{1e3 * a['sagitta_m']['b2']:.1f}", 'SagittaBOneMm': f"{1e3 * a['sagitta_m']['b1']:.1f}",
        'BladeOneMm': f"{1e3 * blade[0.001]:.2f}", 'BladeTwoMm': f"{1e3 * blade[0.002]:.2f}", 'BladeThreeMm': f"{1e3 * blade[0.003]:.2f}"})
    fig, axes = plt.subplots(2, 1, figsize=(7, 4.2), sharex=True)
    for name, d in a['designs'].items():
        for plane, ax in enumerate(axes):
            rows = [r for r in d['profile'] if r['plane'] == plane]
            ax.plot([r['s_m'] for r in rows], [1e3 * r['clearance_m'] for r in rows], '.', ms=3, color=COLORS[name], label=LABELS[name])
    for plane, ax in enumerate(axes):
        ax.set_yscale('log')
        ax.set_yticks([0.5, 1, 2, 5, 10, 20], ['0.5', '1', '2', '5', '10', '20'])
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_ylabel(('Horizontal' if plane == 0 else 'Vertical') + ' clearance [mm]')
        ax.grid(alpha=.3)
    axes[0].annotate('injection-septum blade', xy=(21.0, 0.66), xytext=(13.5, 1.5), arrowprops={'arrowstyle': '->', 'lw': .8}, fontsize=8)
    axes[0].legend(fontsize=7, loc='upper left')
    axes[1].set_xlabel('Path coordinate s [m]')
    fig.tight_layout()
    fig.savefig(P / 'figures/round3_clearance_profile.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def steering():
    st = load('steering', 'steering.json')
    (P / 'generated/round3_steering.json').write_text(json.dumps(st, indent=2) + '\n')
    names = {'uncorrected': 'none', 'corrected': 'declared', 'amended': 'amended'}
    rows = []
    for variant in ('uncorrected', 'corrected', 'amended'):
        for name in ('reference', 'low_beta'):
            e = st['summary'][variant][name]
            rows.append(f"{SHORT[name]} & {names[variant]} & {1e3 * e['mean_clearance_m']:.3f} & {100 * e['observed_loss_fraction']:.2f} & "
                        f"{100 * e['predicted_loss_max_mean']:.2f} & {e['loss_blocks']} & {1e3 * e['exit_centroid_rms_m_rad'][0]:.2f} & "
                        f"{1e3 * e['exit_centroid_rms_m_rad'][1]:.2f} \\\\")
    (P / 'generated/round3_steering_rows.tex').write_text(
        '\\begin{tabular}{llrrrrrr}\\toprule\nSetting & Steering & $\\bar c_{\\min}$ [mm] & Lost [\\%] & Predicted [\\%] & Blocks & '
        '$x_{\\rm rms}$ [mm] & $x'"'"'_{\\rm rms}$ [mrad] \\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')
    s, eff = st['summary'], st['corrected_minus_uncorrected_m']
    vals = {}
    for name, key in (('reference', 'Ref'), ('low_beta', 'Low')):
        for variant, v in (('uncorrected', 'Unc'), ('corrected', 'Cor'), ('amended', 'Amd')):
            e = s[variant][name]
            vals[f'{key}{v}LostPct'] = f"{100 * e['observed_loss_fraction']:.2f}"
            vals[f'{key}{v}PredPct'] = f"{100 * e['predicted_loss_max_mean']:.2f}"
            vals[f'{key}{v}ExitXUm'] = f"{1e6 * e['exit_centroid_rms_m_rad'][0]:.0f}"
            vals[f'{key}{v}ExitXpUrad'] = f"{1e6 * e['exit_centroid_rms_m_rad'][1]:.0f}"
            vals[f'{key}{v}Clear'] = f"{1e3 * e['mean_clearance_m']:.3f}"
            vals[f'{key}{v}Blocks'] = str(e['loss_blocks'])
        for variant, v in (('corrected', 'Cor'), ('amended', 'Amd')):
            vals[f'{key}{v}KickUrad'] = f"{1e6 * s[variant][name]['kick_rms_rad']:.0f}"
            vals[f'{key}{v}ClearGain'] = f"{1e3 * eff[variant][name]['mean']:+.3f}"
    first = json.loads((CAMPAIGN / 'steering_declared_only/steering.json').read_text())['summary']['corrected']['reference']
    vals['FirstRunCorExitXpUrad'] = f"{1e6 * first['exit_centroid_rms_m_rad'][1]:.0f}"
    vals['FirstRunCorLostPct'] = f"{100 * first['observed_loss_fraction']:.2f}"
    worst = max(abs(e['observed_loss_fraction'] - e['predicted_loss_max_mean']) / e['predicted_loss_max_mean']
                for v in s.values() for e in v.values())
    vals['PredAgreePct'] = f"{100 * worst:.1f}"
    macros('steering', vals)


STEPS = {'apertures': apertures, 'steering': steering}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--only', nargs='+', choices=list(STEPS), default=list(STEPS))
    for name in p.parse_args().only:
        STEPS[name]()
        print('Installed', name)


if __name__ == '__main__':
    main()
