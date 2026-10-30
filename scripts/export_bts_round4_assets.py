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


PARTS = {'jitter': jitter, 'blade': blade, 'statistics': statistics}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--part', choices=sorted(PARTS) + ['all'], default='all')
    a = p.parse_args()
    for name, fn in PARTS.items():
        if a.part in (name, 'all'):
            fn()


if __name__ == '__main__':
    main()
