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
CAMPAIGN = ROOT / 'results/bts_journal_campaign_r3b_20261015'
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


def render_clearance_profile(data, output):
    """Draw both settings visibly, including their difference [mm] at matched stations."""
    fig, axes = plt.subplots(3, 1, figsize=(7, 6.1), sharex=True,
                             gridspec_kw={'height_ratios': [1, 1, .8]})
    profiles = {}
    styles = {'reference': dict(color='#2166ac', ls='-', marker='o', mfc='#2166ac', ms=3, lw=1.2),
              'low_beta': dict(color='#d66b00', ls='--', marker='s', mfc='none', ms=5, lw=1.3)}
    for name in ('reference', 'low_beta'):
        profiles[name] = {}
        for plane, ax in enumerate(axes[:2]):
            rows = [r for r in data['designs'][name]['profile'] if r['plane'] == plane]
            stations = [(r['index'], r['name'], r['s_m']) for r in rows]
            values = np.array([r['clearance_m'] for r in rows])
            profiles[name][plane] = (stations, values)
            ax.plot([r['s_m'] for r in rows], 1e3 * values, **styles[name],
                    markevery=5, label=LABELS[name])
    for plane, ax in enumerate(axes[:2]):
        ax.set_yscale('log')
        ax.set_yticks([0.5, 1, 2, 5, 10, 20], ['0.5', '1', '2', '5', '10', '20'])
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_ylabel(('Horizontal' if plane == 0 else 'Vertical') + ' clearance [mm]')
        ax.grid(alpha=.3)
        ref_stations, ref_values = profiles['reference'][plane]
        low_stations, low_values = profiles['low_beta'][plane]
        if ref_stations != low_stations:
            raise ValueError('Clearance differences require identical observation stations')
        axes[2].plot([r[2] for r in ref_stations], 1e3 * (low_values - ref_values),
                     color='#2166ac' if plane == 0 else '#d66b00', ls='-' if plane == 0 else '--',
                     label='Horizontal' if plane == 0 else 'Vertical')
    axes[0].annotate('injection-septum blade', xy=(21.0, 0.66), xytext=(13.5, 1.5),
                     arrowprops={'arrowstyle': '->', 'lw': .8}, fontsize=8)
    axes[0].legend(fontsize=8, loc='upper left')
    axes[2].axhline(0, color='0.4', lw=.7)
    axes[2].set_ylabel('Low beta − reference [mm]')
    axes[2].set_xlabel('Path coordinate s [m]')
    axes[2].grid(alpha=.3)
    axes[2].legend(fontsize=8, loc='upper left')
    fig.tight_layout()
    fig.savefig(output / 'round3_clearance_profile.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(output / 'round3_clearance_profile.png', dpi=160)
    plt.close(fig)


def installed_clearance_figure(output):
    """Re-evaluate only deterministic nominal profiles when campaign rows are absent."""
    import hashlib
    import at
    from nkm_injection.bts_journal import JournalBeam
    from nkm_injection.bts_round3 import aperture_lattice, clearance_and_loss, observation_copy

    output.mkdir(parents=True, exist_ok=False)
    source = P / 'generated/round3_apertures.json'
    data = json.loads(source.read_text())
    validation = {'scope': 'Nominal profiles of frozen strengths; no error campaign or optimization rerun.',
                  'pyat_version': at.__version__, 'absolute_tolerance_m': 1e-10, 'designs': {},
                  'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                                    [source, Path(__file__), ROOT / 'src/nkm_injection/bts_round3.py',
                                     ROOT / 'src/nkm_injection/bts_journal.py']}}
    for name in ('reference', 'low_beta'):
        saved = data['designs'][name]
        line = observation_copy(aperture_lattice(saved['strengths_m_minus2'], model=data['model']), data['model'])
        record = clearance_and_loss(line, np.zeros(5), JournalBeam().covariance())
        families = {}
        for row in record['rows']:
            key = row['name'] + ('_x' if row['plane'] == 0 else '_y')
            families[key] = min(families.get(key, np.inf), row['clearance_m'])
        if families.keys() != saved['family_minimum_m'].keys():
            raise ValueError('Re-evaluated aperture families differ from the frozen summary')
        error = max(abs(families[k] - saved['family_minimum_m'][k]) for k in families)
        if error > validation['absolute_tolerance_m']:
            raise ValueError('Nominal clearances differ from the frozen summary')
        saved['profile'] = record['rows']
        validation['designs'][name] = {'max_family_clearance_difference_m': error,
                                       'minimum_clearance_m': record['minimum_m'], 'profile_rows': len(record['rows'])}
    render_clearance_profile(data, output)
    (output / 'clearance_plot_validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    print('Rendered distinguishable nominal clearance profiles and checked all frozen family minima.')


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
        'MinMm': f"{1e3 * ref['minimum_m']:.3f}", 'BladeMm': f"{1e3 * fam['m4_x']:.3f}",
        'SeptInYMm': f"{1e3 * fam['sept_in_y']:.2f}", 'SeptInXMm': f"{1e3 * fam['sept_in_x']:.2f}",
        'InteriorRefMm': f"{1e3 * ref['interior_minimum_m']:.2f}", 'InteriorLowMm': f"{1e3 * low['interior_minimum_m']:.2f}",
        'SagittaBTwoMm': f"{1e3 * a['sagitta_m']['b2']:.1f}", 'SagittaBOneMm': f"{1e3 * a['sagitta_m']['b1']:.1f}",
        'BladeOneMm': f"{1e3 * blade[0.001]:.2f}", 'BladeTwoMm': f"{1e3 * blade[0.002]:.2f}", 'BladeThreeMm': f"{1e3 * blade[0.003]:.2f}"})
    render_clearance_profile(a, P / 'figures')


def steering():
    st = load('steering', 'steering.json')
    (P / 'generated/round3_steering.json').write_text(json.dumps(st, indent=2) + '\n')
    names = {'uncorrected': 'none', 'corrected': 'dipole trims'}
    rows = []
    for variant in ('uncorrected', 'corrected'):
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
        for variant, v in (('uncorrected', 'Unc'), ('corrected', 'Cor')):
            e = s[variant][name]
            vals[f'{key}{v}LostPct'] = f"{100 * e['observed_loss_fraction']:.2f}"
            vals[f'{key}{v}PredPct'] = f"{100 * e['predicted_loss_max_mean']:.2f}"
            vals[f'{key}{v}ExitXUm'] = f"{1e6 * e['exit_centroid_rms_m_rad'][0]:.0f}"
            vals[f'{key}{v}ExitXpUrad'] = f"{1e6 * e['exit_centroid_rms_m_rad'][1]:.0f}"
            vals[f'{key}{v}Clear'] = f"{1e3 * e['mean_clearance_m']:.3f}"
            vals[f'{key}{v}Blocks'] = str(e['loss_blocks'])
        for variant, v in (('corrected', 'Cor'),):
            vals[f'{key}{v}KickUrad'] = f"{1e6 * s[variant][name]['kick_rms_rad']:.0f}"
            vals[f'{key}{v}ClearGain'] = f"{1e3 * eff[variant][name]['mean']:+.3f}"
    worst = max(abs(e['observed_loss_fraction'] - e['predicted_loss_max_mean']) / e['predicted_loss_max_mean']
                for v in s.values() for e in v.values())
    vals['PredAgreePct'] = f"{100 * worst:.1f}"
    macros('steering', vals)


def design():
    ph, rb, te = load('phase', 'phase.json'), load('robust', 'robust.json'), load('test', 'test.json')
    pools = ph['pools']
    summary = {'environment': ph['environment'], 'pools': {k: {'starts': v['starts'], 'solutions': v['solutions'],
                                                               'mu_x_range_deg': v['mu_x_range_deg']} for k, v in pools.items()},
               'robust': strip(rb, []), 'test': strip(te, [])}
    (P / 'generated/round3_design.json').write_text(json.dumps(summary, indent=2) + '\n')
    t = te['summary']['corrected']
    d = rb['designs']
    pair = te['paired_loss_fraction_vs_reference']
    rows = []
    for name in ('reference', 'low_beta', 'robust'):
        e = t[name]
        rows.append(f"{SHORT[name]} & {d[name]['mu_x_deg']:.1f} & {max(d[name]['peak_beta_m']):.1f} & {1e3 * d[name]['exit_jitter_x_m']:.3f} & "
                    f"{1e3 * d[name]['exit_jitter_xp_rad']:.3f} & {100 * d[name]['loss_max']:.2f} & {100 * e['observed_loss_fraction']:.2f} & "
                    f"{100 * e['predicted_loss_max_mean']:.2f} & {e['loss_blocks']} \\\\")
    (P / 'generated/round3_design_rows.tex').write_text(
        '\\begin{tabular}{lrrrrrrrr}\\toprule\nSetting & $\\mu_x$ [deg] & $\\hat\\beta$ [m] & $\\sigma_{x,j}$ [mm] & $\\sigma_{x'"'"',j}$ [mrad] & '
        '$\\bar P$ [\\%] & Lost [\\%] & Pred. [\\%] & Blocks \\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')
    cand = {c['start']: c for c in rb['candidates']}
    vals = {'PoolStarts': str(pools['configured']['starts']), 'PoolSolutions': str(pools['configured']['solutions']),
            'MuMin': f"{pools['configured']['mu_x_range_deg'][0]:.1f}", 'MuMax': f"{pools['configured']['mu_x_range_deg'][1]:.1f}",
            'FreeSolutions': str(pools['dispersion_free']['solutions']), 'FreeStarts': str(pools['dispersion_free']['starts']),
            'FreeMuMin': f"{pools['dispersion_free']['mu_x_range_deg'][0]:.1f}", 'FreeMuMax': f"{pools['dispersion_free']['mu_x_range_deg'][1]:.1f}",
            'RobustMu': f"{d['robust']['mu_x_deg']:.1f}", 'RefMu': f"{d['reference']['mu_x_deg']:.1f}", 'LowMu': f"{d['low_beta']['mu_x_deg']:.1f}",
            'RobustShotPct': f"{100 * d['robust']['loss_max']:.2f}", 'RefShotPct': f"{100 * d['reference']['loss_max']:.2f}",
            'LowShotPct': f"{100 * d['low_beta']['loss_max']:.2f}",
            'RobustJxUm': f"{1e6 * d['robust']['exit_jitter_x_m']:.0f}", 'RefJxUm': f"{1e6 * d['reference']['exit_jitter_x_m']:.0f}",
            'RobustJxpUrad': f"{1e6 * d['robust']['exit_jitter_xp_rad']:.0f}", 'RefJxpUrad': f"{1e6 * d['reference']['exit_jitter_xp_rad']:.0f}",
            'TestRefPct': f"{100 * t['reference']['observed_loss_fraction']:.2f}", 'TestLowPct': f"{100 * t['low_beta']['observed_loss_fraction']:.2f}",
            'TestRobustPct': f"{100 * t['robust']['observed_loss_fraction']:.2f}",
            'TestRobustDiff': f"{100 * pair['robust']['mean']:+.2f}", 'TestRobustDiffLo': f"{100 * pair['robust']['ci95'][0]:+.2f}",
            'TestRobustDiffHi': f"{100 * pair['robust']['ci95'][1]:+.2f}",
            'TestLowDiff': f"{100 * pair['low_beta']['mean']:+.2f}", 'TestLowDiffLo': f"{100 * pair['low_beta']['ci95'][0]:+.2f}",
            'TestLowDiffHi': f"{100 * pair['low_beta']['ci95'][1]:+.2f}",
            'TestRobustClear': f"{1e3 * t['robust']['paired_vs_reference_m']['mean']:+.3f}",
            'TestRobustClearLo': f"{1e3 * t['robust']['paired_vs_reference_m']['ci95'][0]:+.3f}",
            'TestRobustClearHi': f"{1e3 * t['robust']['paired_vs_reference_m']['ci95'][1]:+.3f}",
            'TestRobustBlocks': str(t['robust']['loss_blocks']), 'TestRefBlocks': str(t['reference']['loss_blocks']),
            'PoolBestGainPct': f"{100 * (1 - d['robust']['loss_max'] / min(r['loss_max'] for r in pools['configured']['rows'])):.1f}",
            'RobustIter': str(cand['pool_best']['iterations']),
            'AnglePenaltyPct': f"{100 * (d['robust']['exit_jitter_xp_rad'] / d['reference']['exit_jitter_xp_rad'] - 1):.0f}",
            'LossRatio': f"{t['reference']['observed_loss_fraction'] / t['robust']['observed_loss_fraction']:.1f}"}
    macros('design', vals)
    fig, ax = plt.subplots(1, 2, figsize=(7, 2.9))
    curve = ph['analytic_curve']
    mu = np.array([c['mu_x_deg'] for c in curve])
    sx = np.array([1e3 * c['exit_jitter_x_m'] for c in curve])
    sxp = np.array([1e3 * c['exit_jitter_xp_rad'] for c in curve])
    ax[0].plot(mu, sx, color='0.2', label='$\\sigma_{x}$ [mm]')
    ax[0].plot(mu, sxp, color='0.2', ls='--', label="$\\sigma_{x'}$ [mrad]")
    for key, color, label in (('configured', '#1f5fa8', 'reachable, configured exit'), ('dispersion_free', '#e9a03b', 'reachable, $D=D'"'"'=0$')):
        lo, hi = pools[key]['mu_x_range_deg']
        ax[0].axvspan(lo, hi, color=color, alpha=.25 if key == 'configured' else .18, label=label)
    ax[0].set(xlim=(150, 260), xlabel='Horizontal phase advance m1$\\to$m4 [deg]', ylabel='Exit jitter (rms)')
    ax[0].legend(fontsize=6.5, loc='upper left')
    rows = pools['configured']['rows']
    ax[1].semilogy([r['mu_x_deg'] for r in rows], [100 * r['loss_max'] for r in rows], '.', color='0.6', ms=3, label='matched solutions (jitter only)')
    for name in ('reference', 'low_beta', 'robust'):
        ax[1].semilogy(d[name]['mu_x_deg'], 100 * d[name]['loss_max'], 'o', color=COLORS[name], label=LABELS[name])
        ax[1].semilogy(d[name]['mu_x_deg'], 100 * t[name]['observed_loss_fraction'], 'x', color=COLORS[name], ms=7)
    ax[1].plot([], [], 'x', color='0.3', label='tracked, steered test machines')
    ax[1].set(xlabel='Horizontal phase advance m1$\\to$m4 [deg]', ylabel='Blade loss per shot [%]')
    ax[1].set_yticks([0.3, 1, 3], ['0.3', '1', '3'])
    ax[1].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax[1].legend(fontsize=6.5, loc='lower right')
    for a in ax:
        a.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(P / 'figures/round3_jitter_transfer.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def exit_target():
    e = load('exit', 'exit.json')
    summary = strip(e, ['dispersion_free_evaluated'])
    summary['dispersion_free_best'] = e['dispersion_free_best']
    (P / 'generated/round3_exit.json').write_text(json.dumps(summary, indent=2) + '\n')
    b, best = e['budget'], e['dispersion_free_best']
    robust = json.loads((CAMPAIGN / 'robust/robust.json').read_text())['designs']['robust']
    pool = e['dispersion_free_pool']
    macros('exit', {
        'BetDivUrad': f"{1e6 * b['betatron_divergence_rad']:.0f}", 'DispDivUrad': f"{1e6 * b['dispersive_divergence_rad']:.0f}",
        'TotDivUrad': f"{1e6 * b['total_divergence_rad']:.0f}", 'EJitAngUrad': f"{1e6 * b['energy_jitter_angle_rad']:.0f}",
        'EJitPosUm': f"{1e6 * b['energy_jitter_position_m']:.0f}", 'BetSizeUm': f"{1e6 * b['betatron_size_m']:.0f}",
        'DispSizeUm': f"{1e6 * b['dispersive_size_m']:.0f}",
        'FreeWithin': str(pool['within_60m']), 'FreeMinPeak': f"{pool['min_peak_beta_m']:.1f}",
        'FreeBestMu': f"{best['mu_x_deg']:.1f}", 'FreeBestLoss': f"{best['loss_max']:.1e}".replace('e-0', '\\times10^{-') + '}',
        'FreeBestJxUm': f"{1e6 * best['exit_jitter_x_m']:.0f}", 'FreeBestJxpUrad': f"{1e6 * best['exit_jitter_xp_rad']:.0f}",
        'FreeBestPeakX': f"{best['peak_beta_m'][0]:.1f}", 'FreeBestPeakY': f"{best['peak_beta_m'][1]:.1f}",
        'FreeGainFactor': f"{robust['loss_max'] / best['loss_max']:.0f}"})


def sensitivity():
    se = load('sensitivity', 'sensitivity.json')
    (P / 'generated/round3_sensitivity.json').write_text(json.dumps(se, indent=2) + '\n')
    rows = []
    for r in se['rows']:
        d = r['designs']
        rows.append(f"{1e3 * r['roll_rad']:.1f} & {100 * r['energy_jitter']:.2f} & " +
                    ' & '.join(f"{100 * d[n]['predicted_loss_max_mean']:.2f}" for n in ('reference', 'low_beta', 'robust')) + ' & ' +
                    ' & '.join(f"{1e3 * d[n]['mean_clearance_m']:.3f}" for n in ('reference', 'robust')) + ' \\\\')
    (P / 'generated/round3_sensitivity_rows.tex').write_text(
        '\\begin{tabular}{rrrrrrr}\\toprule\nRoll & $\\sigma_{\\delta,j}$ & \\multicolumn{3}{c}{Predicted loss [\\%]} & '
        '\\multicolumn{2}{c}{$\\bar c_{\\min}$ [mm]}\\\\\n{}[mrad] & [\\%] & Ref. & Low beta & Loss-based & Ref. & Loss-based \\\\\\midrule\n'
        + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')
    loss = {(r['roll_rad'], r['energy_jitter']): r['designs'] for r in se['rows']}
    roll_effect = max(abs(loss[(a, e)][n]['predicted_loss_max_mean'] - loss[(b, e)][n]['predicted_loss_max_mean'])
                      for a in se['protocol']['roll_rad'] for b in se['protocol']['roll_rad']
                      for e in se['protocol']['energy_jitter'] for n in ('reference', 'low_beta', 'robust'))
    full, half = loss[(5e-4, 1e-3)], loss[(5e-4, 5e-4)]
    ratios = [full[n]['predicted_loss_max_mean'] / full['robust']['predicted_loss_max_mean'] for n in ('reference',)]
    te = json.loads((CAMPAIGN / 'test/raw_machines.json').read_text())
    per = np.array([np.mean([s['results']['reference']['corrected']['lost'] for s in m['shots']]) for m in te])
    macros('sensitivity', {'RollEffectPct': f"{100 * roll_effect:.3f}",
                           'EnergyRefFull': f"{100 * full['reference']['predicted_loss_max_mean']:.2f}",
                           'EnergyRefHalf': f"{100 * half['reference']['predicted_loss_max_mean']:.2f}",
                           'SensRatio': f"{ratios[0]:.1f}",
                           'TopFiveSharePct': f"{100 * np.sort(per)[-5:].sum() / per.sum():.0f}",
                           'WorstMachinePct': f"{100 * per.max() / 2000:.0f}"})


STEPS = {'apertures': apertures, 'steering': steering, 'design': design, 'exit': exit_target, 'sensitivity': sensitivity}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--only', nargs='+', choices=list(STEPS), default=list(STEPS))
    p.add_argument('--clearance-figure-dir', type=Path, help='New directory for only the frozen nominal clearance figure')
    args = p.parse_args()
    if args.clearance_figure_dir:
        installed_clearance_figure(args.clearance_figure_dir)
        return
    for name in args.only:
        STEPS[name]()
        print('Installed', name)


if __name__ == '__main__':
    main()
