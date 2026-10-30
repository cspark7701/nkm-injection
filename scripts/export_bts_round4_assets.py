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
SHORT = {'reference': 'Matched', 'low_beta': 'Low beta', 'robust': 'Loss-based (R3)', 'scan_best': 'Scan grid best',
         'edge_best': 'Phase edge', 'free_best': 'Disp.-free'}


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


def blade():
    """R4-BTS-02: loss against blade distance at the assumed and a tenfold smaller jitter."""
    data = load('blade_b', 'blade.json')
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    floor = 1e-12
    for scale, ls, marker in ((1.0, '-', 'o'), (0.1, '--', 's')):
        for name in ('reference', 'low_beta', 'robust'):
            rows = sorted((r for r in data['rows'] if r['jitter_scale'] == scale), key=lambda r: r['blade_distance_m'])
            # Points below the axis floor are omitted rather than drawn on it.
            pts = [(1e3 * r['blade_distance_m'], r['designs'][name]['jitter_integrated_loss']) for r in rows
                   if r['designs'][name]['jitter_integrated_loss'] >= floor]
            ax.plot(*zip(*pts), ls=ls, marker=marker, ms=4, mfc='none' if scale < 1 else COLORS[name], color=COLORS[name], lw=1.2,
                    label=f"{SHORT[name]}, jitter ×{scale:g}")
    ax.axhline(data['protocol']['tolerance_loss'], color='0.4', lw=.8, ls=':')
    ax.text(3.0, data['protocol']['tolerance_loss'] * 1.6, '0.1 %', ha='right', va='bottom', fontsize=8, color='0.3')
    ax.axvline(1.478, color='0.6', lw=.8)
    ax.text(1.5, 1e-7, 'model value', rotation=90, va='center', ha='left', fontsize=8, color='0.4')
    ax.set(yscale='log', ylim=(floor, 0.2), xlim=(0.95, 3.05), xlabel='Centroid-to-blade distance $d_b$ [mm]',
           ylabel='Jitter-integrated loss fraction')
    ax.grid(True, which='major', color='0.85', lw=.6)
    ax.legend(fontsize=7, ncol=2, loc='lower right', frameon=True, framealpha=.9, edgecolor='none')
    fig.tight_layout()
    fig.savefig(P / 'figures/round4_blade_distance.pdf', metadata={'CreationDate': None})
    plt.close(fig)
    tol = data['distance_for_tolerance_m']
    get = lambda s, d_b, n: next(r for r in data['rows'] if r['jitter_scale'] == s and abs(r['blade_distance_m'] - d_b) < 1e-9)['designs'][n]['jitter_integrated_loss']
    tenth_one_mm = max(get(0.1, 0.001, n) for n in ('reference', 'low_beta', 'robust'))
    macros('blade', {
        'TolRefMm': f"{1e3 * tol['1.0']['reference']['distance_m']:.2f}",
        'TolLowMm': f"{1e3 * tol['1.0']['low_beta']['distance_m']:.2f}",
        'TolRobustMm': f"{1e3 * tol['1.0']['robust']['distance_m']:.2f}",
        'OneMmFullRefPct': f"{100 * get(1.0, 0.001, 'reference'):.1f}",
        'OneMmFullRobustPct': f"{100 * get(1.0, 0.001, 'robust'):.1f}",
        'OneMmTenthMax': f'{tenth_one_mm:.0e}',
    })
    (P / 'generated/round4_blade.json').write_text(json.dumps({'source': str(CAMPAIGN / 'blade_b/blade.json'),
                                                                'distance_for_tolerance_m': tol, 'rows': data['rows']}, indent=2) + '\n')


def statistics():
    """R4-BTS-06: uncensored mean exit offsets and paired low-beta intervals from the round-3 steering campaign."""
    source = ROOT / 'results/bts_journal_campaign_r3b_20261015/steering/raw_machines.json'
    raw = json.loads(source.read_text())

    def interval(delta, seed=91005, count=10000):
        rng = np.random.default_rng(seed)
        delta = np.asarray(delta, dtype=float)
        means = delta[rng.integers(0, len(delta), (count, len(delta)))].mean(1)
        return {'mean': float(delta.mean()), 'ci95': np.quantile(means, [.025, .975]).tolist()}

    per = lambda n, v, key: np.array([np.mean([s['results'][n][v][key] for s in m['shots']]) for m in raw])
    out = {'source': str(source), 'shots': sum(len(m['shots']) for m in raw), 'variants': {}}
    for v in ('uncorrected', 'corrected'):
        entry = {}
        for n in ('reference', 'low_beta'):
            x = np.array([s['results'][n][v]['exit_centroid'][0] for m in raw for s in m['shots']])
            entry[n] = {'mean_exit_x_m': float(x.mean()), 'exit_x_std_m': float(x.std())}
        entry['low_minus_reference_lost_fraction'] = interval((per('low_beta', v, 'lost') - per('reference', v, 'lost')) / 2000)
        entry['low_minus_reference_clearance_m'] = interval(per('low_beta', v, 'clearance_m') - per('reference', v, 'clearance_m'))
        out['variants'][v] = entry
    (P / 'generated/round4_statistics.json').write_text(json.dumps(out, indent=2) + '\n')


def pct(value):
    """Fraction as a percent string: two decimals, or siunitx scientific notation below 0.01 %."""
    return f'{100 * value:.2f}' if 100 * value >= 0.01 else sci(100 * value)


def _pct_interval(e, key='paired_tracked_vs_reference'):
    i = e[key]
    return f"{100 * i['mean']:+.2f} [{100 * i['ci95'][0]:+.2f}, {100 * i['ci95'][1]:+.2f}]"


def _edge_row(edge):
    """Phase-advance, peak beta, exit jitter and error-free loss of an edge solution (recomputed, analytic)."""
    import sys
    sys.path.insert(0, str(ROOT / 'src'))
    from nkm_injection.bts_journal import independent_maps, lattice_for
    from nkm_injection import bts_round3 as r3
    k = np.array(edge['strengths_m_minus2'])
    m = independent_maps(lattice_for(k))[0][-1]
    jit = m @ r3.entrance_jitter_covariance() @ m.T
    return {'mu_x_deg': edge['mu_x_deg'], 'peak_beta_m': edge['peak_beta_m'], 'strengths_m_minus2': edge['strengths_m_minus2'],
            'exit_jitter_x_m': float(np.sqrt(jit[0, 0])), 'exit_jitter_xp_rad': float(np.sqrt(jit[1, 1])),
            'loss_max': r3.shot_averaged_loss(r3.aperture_lattice(k))['loss_lower']}


def phase():
    """R4-BTS-05/12: constrained phase-advance scan, edges, trade curve and the fresh tracked test."""
    scan = load('phase_scan_b', 'phase_scan.json')
    test = load('final_test_b', 'final_test.json')
    frozen = json.loads((ROOT / 'results/bts_journal_campaign_r3b_20261015/robust/robust.json').read_text())['designs']
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.0))
    styles = {'configured': ('#1f5fa8', 'Configured exit'), 'dispersion_free': ('#e08214', 'Dispersion-free exit')}
    for target, (color, label) in styles.items():
        rows = [r for r in scan['rows'] if r['target'] == target and r['matched']]
        for feasible in (True, False):
            sel = [r for r in rows if r['feasible'] == feasible]
            if not sel:
                continue
            kw = dict(color=color, ms=4, ls='none', marker='o', mfc=color if feasible else 'none',
                      label=label if feasible else f'{label}, peak beta > 60 m')
            axes[0].plot([r['mu_x_deg'] for r in sel], [max(r['loss_max'], 1e-12) for r in sel], **kw)
            axes[1].plot([1e3 * r['exit_jitter_xp_rad'] for r in sel], [max(r['loss_max'], 1e-12) for r in sel], **kw)
        for e in scan['edges']:
            if e['target'] == target and e['matched']:
                axes[0].axvline(e['mu_x_deg'], color=color, lw=.6, ls=':')
    for name, marker in (('reference', 's'), ('low_beta', '^'), ('robust', 'D')):
        d = frozen[name]
        axes[0].plot(d['mu_x_deg'], d['loss_max'], marker=marker, color='k', mfc='none', ms=6, ls='none', label=SHORT[name])
        axes[1].plot(1e3 * d['exit_jitter_xp_rad'], d['loss_max'], marker=marker, color='k', mfc='none', ms=6, ls='none')
    for ax in axes:
        ax.set_yscale('log')
        ax.grid(True, color='0.88', lw=.6)
    axes[0].set(xlabel='Horizontal phase advance $\\mu_x$ [deg]', ylabel='Predicted blade loss (error-free)')
    axes[1].set(xlabel="Exit angle jitter $\\sigma_{x',j}$ [mrad]")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=7, ncol=3, loc='upper center', frameon=False)
    fig.tight_layout(rect=(0, 0, 1, .84))
    fig.savefig(P / 'figures/round4_phase_scan.pdf', metadata={'CreationDate': None})
    plt.close(fig)
    # Edges: smallest and largest matched mu found by the edge search, with active constraints.
    edges = {}
    for target in styles:
        for direction in ('min', 'max'):
            found = [e for e in scan['edges'] if e['target'] == target and e['direction'] == direction and e['matched']]
            if found:
                best = (min if direction == 'min' else max)(found, key=lambda e: e['mu_x_deg'])
                edges[f'{target}_{direction}'] = {k: best[k] for k in ('mu_x_deg', 'active_bounds', 'peak_beta_m', 'peak_beta_active',
                                                                        'iterations', 'termination', 'success')}
    summary = test['summary']
    names = ('reference', 'low_beta', 'robust', 'scan_best', 'edge_best', 'free_best')
    chosen = dict(scan['chosen'])
    edge = min((e for e in scan['edges'] if e['target'] == 'configured' and e['direction'] == 'min' and e['success'] and e['matched']),
               key=lambda e: e['mu_x_deg'])
    chosen['edge_best'] = _edge_row(edge)
    info = {n: {'mu_x_deg': frozen[n]['mu_x_deg'], 'peak': max(frozen[n]['peak_beta_m']), 'jx': frozen[n]['exit_jitter_x_m'],
                'jxp': frozen[n]['exit_jitter_xp_rad'], 'loss': frozen[n]['loss_max']} for n in names[:3]}
    for n in names[3:]:
        c = chosen[n]  # scan rows and the recomputed edge row share these keys
        info[n] = {'mu_x_deg': c['mu_x_deg'], 'peak': max(c['peak_beta_m']), 'jx': c['exit_jitter_x_m'],
                   'jxp': c['exit_jitter_xp_rad'], 'loss': c['loss_max']}
    lines = ['\\begin{tabular}{lrrrrrrl}\\toprule',
             "Setting & $\\mu_x$ [deg] & $\\hat\\beta$ [m] & $\\sigma_{x',j}$ [mrad] & $\\bar P$ [\\%] & Integr.\\ [\\%] & Lost [\\%] & "
             "Lost $-$ Matched [pp]\\\\\\midrule"]
    for n in names:
        e, i = summary[n], info[n]
        diff = '---' if n == 'reference' else _pct_interval(e)
        lines.append(f"{SHORT[n]} & {i['mu_x_deg']:.1f} & {i['peak']:.1f} & {1e3 * i['jxp']:.3f} & {pct(i['loss'])} & "
                     f"{pct(e['jitter_integrated_loss_mean'])} & {pct(e['observed_loss_fraction'])} & {diff}\\\\")
    lines.append('\\bottomrule\\end{tabular}')
    (P / 'generated/round4_test_rows.tex').write_text('\n'.join(lines) + '\n')
    conf = [r['mu_x_deg'] for r in scan['rows'] if r['target'] == 'configured' and r['matched']]
    free = [r['mu_x_deg'] for r in scan['rows'] if r['target'] == 'dispersion_free' and r['matched']]
    first = {n: summary[n]['first_loss_families'] for n in names}
    ratio = summary['reference']['observed_loss_fraction'] / summary['scan_best']['observed_loss_fraction']
    values = {
        'ScanConfMin': f'{min(conf):.0f}', 'ScanConfMax': f'{max(conf):.0f}', 'ScanFreeMin': f'{min(free):.0f}', 'ScanFreeMax': f'{max(free):.0f}',
        'ScanBestMu': f"{info['scan_best']['mu_x_deg']:.0f}", 'ScanBestPeak': f"{info['scan_best']['peak']:.1f}",
        'ScanBestLossPct': f"{100 * info['scan_best']['loss']:.2f}", 'ScanBestJxpUrad': f"{1e6 * info['scan_best']['jxp']:.0f}",
        'FreeBestMu': f"{info['free_best']['mu_x_deg']:.0f}", 'FreeBestPeak': f"{info['free_best']['peak']:.1f}",
        'FreeBestJxpUrad': f"{1e6 * info['free_best']['jxp']:.0f}",
        'TestRefPct': f"{100 * summary['reference']['observed_loss_fraction']:.2f}",
        'TestScanPct': f"{100 * summary['scan_best']['observed_loss_fraction']:.2f}",
        'TestRobustPct': f"{100 * summary['robust']['observed_loss_fraction']:.2f}",
        'TestFreeLost': str(summary['free_best']['lost_particles']),
        'TestFreeIntegratedPct': pct(summary['free_best']['jitter_integrated_loss_mean']),
        'TestRobustIntegratedPct': pct(summary['robust']['jitter_integrated_loss_mean']),
        'TestEdgeIntegratedPct': pct(summary['edge_best']['jitter_integrated_loss_mean']),
        'TestEdgePct': f"{100 * summary['edge_best']['observed_loss_fraction']:.2f}",
        'TestEdgeDiff': _pct_interval(summary['edge_best']),
        'TestLowPct': f"{100 * summary['low_beta']['observed_loss_fraction']:.2f}",
        'TestEdgeRatio': f"{summary['reference']['observed_loss_fraction'] / summary['edge_best']['observed_loss_fraction']:.1f}",
        'EdgeRobustMuDiffDeg': f"{abs(info['edge_best']['mu_x_deg'] - info['robust']['mu_x_deg']):.0e}",
        'FreeBestLossPct': pct(info['free_best']['loss']),
        'TestScanRatio': f'{ratio:.1f}',
        'TestScanDiff': _pct_interval(summary['scan_best']), 'TestFreeDiff': _pct_interval(summary['free_best']),
        'TestRobustDiff': _pct_interval(summary['robust']), 'TestLowDiff': _pct_interval(summary['low_beta']),
    }
    for key, e in edges.items():
        tag = ''.join(w.capitalize() for w in key.split('_'))
        values[f'Edge{tag}'] = f"{e['mu_x_deg']:.1f}"
    macros('phase', values)
    (P / 'generated/round4_phase.json').write_text(json.dumps({'scan_source': str(CAMPAIGN / 'phase_scan_b/phase_scan.json'),
                                                                'test_source': str(CAMPAIGN / 'final_test/final_test.json'),
                                                                'edges': edges, 'settings': info, 'first_losses': first,
                                                                'chosen_strengths_m_minus2': {n: chosen[n]['strengths_m_minus2'] for n in names[3:]},
                                                                'test': {n: {k: summary[n][k] for k in ('observed_loss_fraction', 'predicted_loss_max_mean',
                                                                                                        'jitter_integrated_loss_mean', 'paired_tracked_vs_reference',
                                                                                                        'exit_centroid_rms_m_rad', 'loss_blocks')}
                                                                         for n in names}}, indent=2) + '\n')


def layouts():
    """R4-BTS-10: steering with reduced monitors and series-powered bends, with the vertical exit centroid."""
    data = load('layouts_b', 'layouts.json')
    labels = {'full': '11 / 6', 'reduced_monitors': '5 / 6', 'series_bends': '11 / 4', 'reduced_series': '5 / 4'}
    lines = ['\\begin{tabular}{llrrrrrr}\\toprule',
             "Readings / knobs & Setting & Lost [\\%] & Pred. [\\%] & $x_{\\rm rms}$ [mm] & $x'_{\\rm rms}$ [mrad] & $y_{\\rm rms}$ [mm] & "
             "$y'_{\\rm rms}$ [mrad]\\\\\\midrule"]
    for layout, label in labels.items():
        for n in ('reference', 'robust'):
            e = data['summary'][layout][n]
            r = e['exit_centroid_rms_m_rad']
            lines.append(f"{label if n == 'reference' else ''} & {SHORT[n]} & {100 * e['observed_loss_fraction']:.2f} & "
                         f"{100 * e['predicted_loss_max_mean']:.2f} & {1e3 * r[0]:.2f} & {1e3 * r[1]:.2f} & {1e3 * r[2]:.3f} & {1e3 * r[3]:.3f}\\\\")
    lines.append('\\bottomrule\\end{tabular}')
    (P / 'generated/round4_layout_rows.tex').write_text('\n'.join(lines) + '\n')
    s = data['summary']
    vy = s['full']['reference']['exit_centroid_rms_m_rad']
    macros('layouts', {
        'LayoutFullRefPct': f"{100 * s['full']['reference']['observed_loss_fraction']:.2f}",
        'LayoutReducedRefPct': f"{100 * s['reduced_monitors']['reference']['observed_loss_fraction']:.2f}",
        'LayoutSeriesRefPct': f"{100 * s['series_bends']['reference']['observed_loss_fraction']:.2f}",
        'LayoutBothRefPct': f"{100 * s['reduced_series']['reference']['observed_loss_fraction']:.2f}",
        'LayoutBothRobustPct': f"{100 * s['reduced_series']['robust']['observed_loss_fraction']:.2f}",
        'LayoutFullRobustPct': f"{100 * s['full']['robust']['observed_loss_fraction']:.2f}",
        'VertExitYUm': f'{1e6 * vy[2]:.0f}', 'VertExitYpUrad': f'{1e6 * vy[3]:.0f}',
        'ReproLost': str(data['reproduction_check']['full_lost_particles']),
        'ReproLostRThree': str(data['reproduction_check']['round3_lost_particles']),
    })
    (P / 'generated/round4_layouts.json').write_text(json.dumps({'source': str(CAMPAIGN / 'layouts_b/layouts.json'),
                                                                  'reproduction_check': data['reproduction_check'],
                                                                  'summary': {l: {n: {k: e[k] for k in ('observed_loss_fraction', 'predicted_loss_max_mean',
                                                                                                         'exit_centroid_rms_m_rad', 'mean_exit_centroid_m_rad',
                                                                                                         'kick_rms_rad', 'paired_tracked_vs_reference', 'loss_blocks')}
                                                                                  for n, e in d.items()} for l, d in s.items()}}, indent=2) + '\n')


PARTS = {'jitter': jitter, 'blade': blade, 'statistics': statistics, 'phase': phase, 'layouts': layouts}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--part', choices=sorted(PARTS) + ['all'], default='all')
    a = p.parse_args()
    for name, fn in PARTS.items():
        if a.part in (name, 'all'):
            fn()


if __name__ == '__main__':
    main()
