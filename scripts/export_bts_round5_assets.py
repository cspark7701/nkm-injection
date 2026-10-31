#!/usr/bin/env python3
"""Install round-five BTS tables, macros and figures (R5-BTS tasks).

Reads results/bts_round5_campaign_20261031 (shared-reading-noise test and layouts, edge study) and the
round-4 jitter sweep; writes only docs/paper_bts/generated/round5_* and docs/paper_bts/figures/round5_*.
Loss columns are percent unless named as counts; positions in mm and angles in mrad.
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'docs/paper_bts'
CAMPAIGN = ROOT / 'results/bts_round5_campaign_20261031'
R4 = ROOT / 'results/bts_round4_campaign_20261030'
R3 = ROOT / 'results/bts_journal_campaign_r3b_20261015'
plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42, 'pdf.compression': 6})
SHORT = {'reference': 'Matched', 'low_beta': 'Low beta', 'edge_best': 'Loss-based', 'free_best': 'Disp.-free'}
LAYOUT_LABEL = {'full': '11 / 6', 'reduced_monitors': '5 / 6', 'series_bends': '11 / 4', 'reduced_series': '5 / 4',
                'angle_weighted': '11 / 6, ends ×10'}


def rel(path):
    return str(Path(path).relative_to(ROOT))


def load(path):
    return json.loads(Path(path).read_text())


def num(value, digits=2):
    """siunitx number: fixed with ``digits`` decimals, or scientific below 0.01."""
    return f'\\num{{{value:.{digits}f}}}' if abs(value) >= 0.01 or value == 0 else f'\\num{{{value:.1e}}}'


def interval_pp(i):
    """Paired fraction interval as percentage points with proper minus signs."""
    return f"\\num{{{100 * i['mean']:.2f}}} [\\num{{{100 * i['ci95'][0]:.2f}}}, \\num{{{100 * i['ci95'][1]:.2f}}}]"


def macros(values):
    text = '% Exported by scripts/export_bts_round5_assets.py; do not edit.\n'
    text += ''.join('\\newcommand{\\BtsRFive' + k + '}{' + v + '}\n' for k, v in values.items())
    (P / 'generated/round5.tex').write_text(text)


def main():
    test = load(CAMPAIGN / 'final_test_b/final_test.json')
    lay = load(CAMPAIGN / 'layouts_b/layouts.json')
    edge = load(CAMPAIGN / 'edge_study/edge_study.json')
    jit = load(R4 / 'jitter_b/jitter.json')
    scan = load(R4 / 'phase_scan_b/phase_scan.json')
    robust = load(R3 / 'robust/robust.json')['designs']
    s, val, g = test['summary'], test['validation'], test['gain_vs_reference']
    n = test['protocol']['machines'] * test['protocol']['shots_per_machine'] * test['protocol']['particles_per_shot']

    # Settings: phase advance, larger peak beta, exit angle jitter and error-free loss (analytic).
    edge_row = min((e for e in scan['edges'] if e['target'] == 'configured' and e['direction'] == 'min' and e['success'] and e['matched']),
                   key=lambda e: e['mu_x_deg'])
    free = scan['chosen']['free_best']
    info = {k: {'mu': robust[k]['mu_x_deg'], 'peak': max(robust[k]['peak_beta_m']), 'jxp': robust[k]['exit_jitter_xp_rad'],
                'loss': robust[k]['loss_max']} for k in ('reference', 'low_beta')}
    info['edge_best'] = {'mu': edge_row['mu_x_deg'], 'peak': max(edge_row['peak_beta_m']), 'jxp': robust['robust']['exit_jitter_xp_rad'],
                         'loss': robust['robust']['loss_max']}
    info['free_best'] = {'mu': free['mu_x_deg'], 'peak': max(free['peak_beta_m']), 'jxp': free['exit_jitter_xp_rad'], 'loss': free['loss_max']}

    lines = ['\\begin{tabular}{lrrrrrrrl}\\toprule',
             "Setting & $\\mu_x$ & $\\hat\\beta$ & $\\sigma_{x',j}$ & $\\bar P$ & Integr. & \\multicolumn{2}{c}{Lost particles} & "
             "Lost $-$ Matched\\\\",
             " & [deg] & [m] & [mrad] & [\\%] & [\\%] & expected & observed & [pp]\\\\\\midrule"]
    for k in ('reference', 'low_beta', 'edge_best', 'free_best'):
        e, i, v = s[k], info[k], val[k]
        diff = '---' if k == 'reference' else interval_pp(e['paired_tracked_vs_reference'])
        lines.append(f"{SHORT[k]} & {i['mu']:.1f} & {i['peak']:.1f} & {1e3 * i['jxp']:.3f} & {num(100 * i['loss'])} & "
                     f"{num(100 * e['jitter_integrated_loss_mean'])} & {v['conditional_expected_count']:.1f} & {v['observed_count']} & {diff}\\\\")
    lines.append('\\bottomrule\\end{tabular}')
    (P / 'generated/round5_test_rows.tex').write_text('\n'.join(lines) + '\n')

    lines = ['\\begin{tabular}{llrrrrrr}\\toprule',
             "Readings / knobs & Setting & Lost [\\%] & Integr. [\\%] & $x_{\\rm rms}$ [mm] & $x'_{\\rm rms}$ [mrad] & "
             "$y_{\\rm rms}$ [mm] & $y'_{\\rm rms}$ [mrad]\\\\\\midrule"]
    for layout, label in LAYOUT_LABEL.items():
        for k in ('reference', 'edge_best'):
            e = lay['summary'][layout][k]
            r = e['exit_centroid_rms_m_rad']
            lines.append(f"{label if k == 'reference' else ''} & {SHORT[k]} & {100 * e['observed_loss_fraction']:.2f} & "
                         f"{100 * e['jitter_integrated_loss_mean']:.2f} & {1e3 * r[0]:.2f} & {1e3 * r[1]:.2f} & {1e3 * r[2]:.2f} & {1e3 * r[3]:.3f}\\\\")
    lines.append('\\bottomrule\\end{tabular}')
    (P / 'generated/round5_layout_rows.tex').write_text('\n'.join(lines) + '\n')

    # Delivered exit centroid by plane against the nominal jitter alone (matched reference, round-4 jitter sweep).
    lines = ['\\begin{tabular}{rrrrrrr}\\toprule',
             "Jitter & \\multicolumn{4}{c}{Steered realizations (rms)} & \\multicolumn{2}{c}{Nominal jitter only}\\\\",
             "\\cmidrule(lr){2-5}\\cmidrule(lr){6-7}",
             "scale & $x$ [mm] & $x'$ [mrad] & $y$ [mm] & $y'$ [mrad] & $\\sigma_{x,j}$ [mm] & $\\sigma_{x',j}$ [mrad]\\\\\\midrule"]
    rows = {r['scale']: r['designs']['reference'] for r in jit['rows']}
    for scale in (0.0, 0.1, 0.2, 0.5, 1.0):
        e = rows[scale]
        c, j = e['exit_centroid_rms_m_rad'], e['exit_jitter_m_rad']
        lines.append(f"{scale:g} & {1e3 * c[0]:.3f} & {1e3 * c[1]:.3f} & {1e3 * c[2]:.3f} & {1e3 * c[3]:.3f} & "
                     f"{1e3 * j[0]:.3f} & {1e3 * j[1]:.3f}\\\\")
    lines.append('\\bottomrule\\end{tabular}')
    (P / 'generated/round5_residual_rows.tex').write_text('\n'.join(lines) + '\n')

    # Figure 4: jitter transfer only, with the phase-advance ranges found by the constrained searches.
    curve = load(R4 / 'phase_scan_b/phase_scan.json')
    r3curve = load(R3 / 'phase/phase.json')['analytic_curve']
    mu = np.array([c['mu_x_deg'] for c in r3curve])
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.plot(mu, [1e3 * c['exit_jitter_x_m'] for c in r3curve], color='0.2', label='$\\sigma_{x,j}$ [mm]')
    ax.plot(mu, [1e3 * c['exit_jitter_xp_rad'] for c in r3curve], color='0.2', ls='--', label="$\\sigma_{x',j}$ [mrad]")
    found = {}
    for target in ('configured', 'dispersion_free'):
        es = [e for e in curve['edges'] if e['target'] == target and e['matched']]
        found[target] = (min(e['mu_x_deg'] for e in es), max(e['mu_x_deg'] for e in es))
    for target, color, label in (('configured', '#1f5fa8', 'found range, configured exit'),
                                 ('dispersion_free', '#e9a03b', "found range, $D=D'=0$")):
        ax.axvspan(*found[target], color=color, alpha=.25 if target == 'configured' else .18, label=label)
    ax.set(xlim=(150, 260), xlabel='Horizontal phase advance m1$\\to$m4 [deg]', ylabel='Exit jitter (rms)')
    ax.legend(fontsize=6.5, loc='upper left')
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(P / 'figures/round5_jitter_transfer.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)

    lowest = edge['lowest']
    ref0, ref01, ref02 = rows[0.0], rows[0.1], rows[0.2]
    vals = {
        'Gain': f"{g['edge_best']['estimate']:.2f}", 'GainLo': f"{g['edge_best']['ci95'][0]:.2f}", 'GainHi': f"{g['edge_best']['ci95'][1]:.2f}",
        'GainLowBeta': f"{g['low_beta']['estimate']:.3f}", 'GainLowBetaLo': f"{g['low_beta']['ci95'][0]:.3f}",
        'GainLowBetaHi': f"{g['low_beta']['ci95'][1]:.3f}",
        'LayoutGain': f"{lay['gain_vs_reference']['full']['estimate']:.2f}",
        'LayoutGainLo': f"{lay['gain_vs_reference']['full']['ci95'][0]:.2f}", 'LayoutGainHi': f"{lay['gain_vs_reference']['full']['ci95'][1]:.2f}",
        'IntegrRefPct': f"{100 * s['reference']['jitter_integrated_loss_mean']:.2f}",
        'IntegrEdgePct': f"{100 * s['edge_best']['jitter_integrated_loss_mean']:.3f}",
        'LostRef': str(val['reference']['observed_count']), 'ExpRef': f"{val['reference']['conditional_expected_count']:.0f}",
        'LostLow': str(val['low_beta']['observed_count']), 'ExpLow': f"{val['low_beta']['conditional_expected_count']:.0f}",
        'LostEdge': str(val['edge_best']['observed_count']), 'ExpEdge': f"{val['edge_best']['conditional_expected_count']:.0f}",
        # The prediction shortfall is relative to the observed count, as in the archived run.
        'EdgePredictionShortfallPct': f"{100 * (val['edge_best']['observed_count'] - val['edge_best']['conditional_expected_count']) / val['edge_best']['observed_count']:.1f}",
        'EdgeZ': f"{val['edge_best']['poisson_z']:.1f}",
        'LostFree': str(val['free_best']['observed_count']), 'ExpFree': f"{val['free_best']['conditional_expected_count']:.2f}",
        'IntegrCountFree': f"{val['free_best']['integrated_expected_count']:.0f}",
        'LossFracFree': f"{val['free_best']['observed_count'] / n:.1e}".replace('e-0', 'e-'),
        'DiffLow': interval_pp(s['low_beta']['paired_tracked_vs_reference']),
        'DiffEdge': interval_pp(s['edge_best']['paired_tracked_vs_reference']),
        'Particles': f'{n:,}'.replace(',', '\\,'),
        'ResXpZero': f"{1e3 * ref0['exit_centroid_rms_m_rad'][1]:.2f}", 'ResXZero': f"{1e3 * ref0['exit_centroid_rms_m_rad'][0]:.2f}",
        'ResYZero': f"{1e3 * ref0['exit_centroid_rms_m_rad'][2]:.2f}", 'ResYpZero': f"{1e3 * ref0['exit_centroid_rms_m_rad'][3]:.2f}",
        'ResXpTenth': f"{1e3 * ref01['exit_centroid_rms_m_rad'][1]:.2f}", 'JitXpTenth': f"{1e3 * ref01['exit_jitter_m_rad'][1]:.3f}",
        'ResXpFifth': f"{1e3 * ref02['exit_centroid_rms_m_rad'][1]:.2f}", 'JitXpFifth': f"{1e3 * ref02['exit_jitter_m_rad'][1]:.3f}",
        'AngleWeightedXp': f"{1e3 * lay['summary']['angle_weighted']['edge_best']['exit_centroid_rms_m_rad'][1]:.3f}",
        'FullXpEdge': f"{1e3 * lay['summary']['full']['edge_best']['exit_centroid_rms_m_rad'][1]:.3f}",
        'LayoutFullEdgePct': f"{100 * lay['summary']['full']['edge_best']['observed_loss_fraction']:.2f}",
        'EdgeDpConf': f"{lowest['0.080868_0.047472']['mu_x_deg']:.1f}", 'EdgeDpMid': f"{lowest['0.080868_0.032']['mu_x_deg']:.1f}",
        'EdgeDpLow': f"{lowest['0.080868_0.016']['mu_x_deg']:.1f}", 'EdgeDpZero': f"{lowest['0.080868_0.0']['mu_x_deg']:.1f}",
        'EdgeDZeroConf': f"{lowest['0.0_0.047472']['mu_x_deg']:.1f}", 'EdgeFree': f"{lowest['0.0_0.0']['mu_x_deg']:.1f}",
    }
    macros(vals)
    (P / 'generated/round5.json').write_text(json.dumps({
        'sources': {'test': rel(CAMPAIGN / 'final_test_b/final_test.json'), 'layouts': rel(CAMPAIGN / 'layouts_b/layouts.json'),
                    'edge_study': rel(CAMPAIGN / 'edge_study/edge_study.json'), 'jitter': rel(R4 / 'jitter_b/jitter.json'),
                    'scan': rel(R4 / 'phase_scan_b/phase_scan.json')},
        'duplicate_identical': test['duplicate_identical'], 'gain_vs_reference': g, 'layout_gain_vs_reference': lay['gain_vs_reference'],
        'validation': val,
        'validation_reporting': {
            'edge_prediction_shortfall': {
                'formula': '100 * (observed_count - conditional_expected_count) / observed_count',
                'denominator': 'observed_count', 'unit': 'percent',
                'value': 100 * (val['edge_best']['observed_count'] - val['edge_best']['conditional_expected_count']) / val['edge_best']['observed_count'],
            },
            'poisson_z_scope': 'Diagnostic (observed - expected) / sqrt(expected); Poisson approximation without model-systematic uncertainty.',
        },
        'edge_lowest': {k: (None if r is None else {x: r[x] for x in ('mu_x_deg', 'success', 'termination', 'active_bounds',
                                                                                         'peak_beta_active')}) for k, r in lowest.items()},
        'macros': vals}, indent=2) + '\n')
    print(json.dumps({k: vals[k] for k in ('Gain', 'GainLo', 'GainHi', 'LayoutGain', 'EdgePredictionShortfallPct', 'EdgeZ', 'EdgeDpZero', 'ResXpTenth', 'JitXpTenth')}))


if __name__ == '__main__':
    main()
