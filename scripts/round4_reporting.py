"""Campaign-05 (round-4) report macros; all numerical inputs are loaded through the manifest.

Percentages and percentage points are formatted from capture fractions; intervals are the central 95 % realization
bootstrap intervals stored in the artifacts.
"""

CLASS_LABELS = {'bts_magnets': 'BTS magnets', 'beam_shape': 'Beam shape', 'mean_energy': 'Mean energy',
                'nkm_amplitude': 'NKM amplitude/timing', 'nkm_orbit_alignment': 'NKM/orbit alignment',
                'septum': 'Septum', 'longitudinal_timing': 'RF phase/arrival'}
MODELS = (('fieldmap_3d', 'Nkm'), ('dipole', 'Dip'), ('gap', 'Gap'))


def _pts(builder, name, d, fmt='{:+.1f}'):
    """Mean and interval of a capture-fraction bootstrap record, in percentage points."""
    builder.macro(name, 100 * d['mean'], fmt)
    if 'ci95' in d:
        builder.macro(name + 'Lo', 100 * d['ci95'][0], fmt)
        builder.macro(name + 'Hi', 100 * d['ci95'][1], fmt)


def _sci(value):
    """One-significant-figure upper bound in TeX, e.g. $1\\times10^{-7}$."""
    import math
    e = math.floor(math.log10(value))
    m = math.ceil(value / 10 ** e)
    if m == 10:
        m, e = 1, e + 1
    return f"${m}\\times10^{{{e}}}$"


def _interval(d):
    return f"{100 * d['mean']:+.1f} [{100 * d['ci95'][0]:+.1f}, {100 * d['ci95'][1]:+.1f}]"


def ablation(builder):
    d = builder.load('round4_ablation')
    e = d['ensembles']
    for ens, tag in (('all_off', 'AllOff'), ('full', 'Full'), ('alone_bts_magnets', 'BtsAlone'),
                     ('omit_bts_magnets', 'BtsOmit')):
        for model, short in MODELS:
            builder.macro(f'Abl{tag}{short}', 100 * e[ens][model]['mean'], '{:.1f}' if model != 'gap' else '{:+.1f}')
    for kind, tag in (('alone_effect', 'Alone'), ('omitted_effect', 'Omit')):
        for model, short in MODELS:
            _pts(builder, f'AblBts{tag}Eff{short}', d[kind]['bts_magnets'][model])
    others = [c for c in d['classes'] if c != 'bts_magnets']
    builder.macro('AblOtherMax', max(abs(100 * d[k][c][m]['mean']) for k in ('alone_effect', 'omitted_effect')
                                     for c in others for m in ('fieldmap_3d', 'dipole')), '{:.1f}')
    _pts(builder, 'AblNonAddNkm', d['non_additivity']['fieldmap_3d']['difference'])
    _pts(builder, 'AblNonAddDip', d['non_additivity']['dipole']['difference'])
    rows = []
    for c in d['classes']:
        a, o = d['alone_effect'][c], d['omitted_effect'][c]
        rows.append(f"{CLASS_LABELS[c]} & {100 * a['fieldmap_3d']['mean']:+.1f} & {100 * a['dipole']['mean']:+.1f} & "
                    f"{_interval(a['gap'])} & {100 * o['fieldmap_3d']['mean']:+.1f} & {100 * o['dipole']['mean']:+.1f} & "
                    f"{_interval(o['gap'])} \\\\")
    builder.macro('AblationRows', '\n'.join(rows))
    x = d['exit_state_post_hoc']
    name = x['ensemble']
    builder.macro('AblExitYmm', 1e3 * x['mean_std']['centroid_y_m'][name][1], '{:.2f}')
    builder.macro('AblExitYpUrad', 1e6 * x['mean_std']['centroid_yp_rad'][name][1], '{:.0f}')
    builder.macro('AblRhoYNkm', x['spearman_abs_vs_capture']['centroid_y_m']['fieldmap_3d']['rho'], '{:.2f}')
    builder.macro('AblRhoYDip', x['spearman_abs_vs_capture']['centroid_y_m']['dipole']['rho'], '{:.2f}')


def points(builder):
    d = builder.load('round4_points_test')
    rows = []
    labels = {'current': 'current', 'earlier': 'earlier', 'extremum': 'extremum-centred'}
    for p, e in d['by_point'].items():
        pt = d['points'][p]
        rows.append(f"{labels[p]} & {1e3 * pt['injection_x_m']:.2f} & {pt['field_scale']:.2f} & {1e3 * pt['centroid_at_nkm_m']:.2f} & "
                    f"{100 * e['zero']['fieldmap_3d']['mean']:.1f} & {100 * e['zero']['dipole']['mean']:.1f} & "
                    f"{100 * e['full']['fieldmap_3d']['mean']:.1f} & {100 * e['full']['dipole']['mean']:.1f} \\\\")
        if p == 'current':
            continue
        tag = 'Earlier' if p == 'earlier' else 'Extremum'
        for b, bt in (('zero', 'Zero'), ('full', 'Full')):
            for model, short in MODELS:
                _pts(builder, f'Pt{tag}{bt}Diff{short}', e[b]['paired_vs_current'][model])
            builder.macro(f'Pt{tag}{bt}Gap', 100 * e[b]['gap']['mean'], '{:+.1f}')
    builder.macro('PointRows', '\n'.join(rows))
    dips = [-100 * d['by_point'][p][b]['paired_vs_current']['dipole']['mean'] for p in ('earlier', 'extremum') for b in ('zero', 'full')]
    builder.macro('PtDipLossMin', min(dips), '{:.0f}')
    builder.macro('PtDipLossMax', max(dips), '{:.0f}')
    builder.macro('PtAdopted', d['decision']['adopted_point'])


def associations(builder):
    d = builder.load('round4_associations')
    z = d['zero_capture']
    for model, short in (('nkm', 'Nkm'), ('dipole', 'Dip')):
        builder.macro(f'ZeroCap{short}', 100 * z[model]['zero_fraction'], '{:.0f}')
        builder.macro(f'CondMean{short}', 100 * z[model]['conditional_mean_nonzero'], '{:.1f}')
    builder.macro('ZeroCapN', str(z['nkm']['n']))
    a = {m: {r['predictor']: r for r in d['associations'][m]} for m in ('nkm', 'dipole', 'difference')}
    for m, short in (('nkm', 'Nkm'), ('dipole', 'Dip')):
        builder.macro(f'AssocAmpOwn{short}', a[m]['amplitude_after_nkm' if m == 'nkm' else 'amplitude_after_dipole']['rho'], '{:.2f}')
    builder.macro('AssocOffsetNkm', a['nkm']['nkm_minus_orbit_m']['rho'], '{:+.2f}')
    builder.macro('AssocOffsetNkmP', a['nkm']['nkm_minus_orbit_m']['p_holm'], '{:.3f}')
    builder.macro('AssocOffsetDip', a['dipole']['nkm_minus_orbit_m']['rho'], '{:+.2f}')
    builder.macro('AssocBoosterXDiff', a['difference']['booster_x_m']['rho'], '{:+.2f}')
    builder.macro('AssocBoosterXDiffP', a['difference']['booster_x_m']['p_holm'], '{:.3f}')
    rows = []
    names = {'0': '0', '0.25': '0.25', '0.5': '0.5', '0.75': '0.75', '1': '1', 'x_only': 'position only', 'xp_only': 'angle only'}
    for level, r in d['jitter_rows'].items():
        cells = []
        for model in ('fieldmap_3d', 'dipole'):
            diff = r[model].get('difference_from_zero')
            cells.append(f"{100 * r[model]['mean']:.1f} & {100 * r[model]['zero_fraction']:.0f} & "
                         + ('---' if diff is None or level == '0' else _interval(diff)))
        rows.append(f"{names[level]} & {cells[0]} & {cells[1]} & {_interval(r['gap'])} \\\\")
    builder.macro('JitterTwoModelRows', '\n'.join(rows))


def loss_locations(builder):
    d = builder.load('round4_loss_locations')
    t = d['zero_capture_nkm_totals']
    total = t.get('plane_x', 0) + t.get('plane_y', 0)
    builder.macro('LossCases', str(sum(1 for c in d['cases'] if c['sample_id'] >= 0)))
    builder.macro('LossTotal', f"{total:,}".replace(',', '\\,'))
    builder.macro('LossFirstTurn', f"{t['turns_turn_0']:,}".replace(',', '\\,'))
    builder.macro('LossVertical', str(t.get('plane_y', 0)))
    builder.macro('LossHorizontal', str(t.get('plane_x', 0)))
    ring = next(c for c in d['cases'] if c['sample_id'] < 0)
    builder.macro('RingFiveNkm', 100 * ring['capture']['fieldmap_3d'], '{:.1f}')
    builder.macro('RingFiveDip', 100 * ring['capture']['dipole'], '{:.1f}')
    nkm = next(r for r in ring['ring_losses'] if r['model'] == 'fieldmap_3d')
    builder.macro('RingFiveVertFrac', 100 * nkm['planes'].get('y', 0) / nkm['n_records'], '{:.0f}')
    open_ = builder.load('round4_ring5501_chamber')
    wide = [v for k, v in open_.items() if isinstance(v, dict) and 'capture' in v and k != 'chamber_3p8mm']
    builder.macro('RingFiveOpenNkm', 100 * wide[0]['capture']['fieldmap_3d'], '{:.1f}')
    builder.macro('RingFiveOpenDip', 100 * wide[0]['capture']['dipole'], '{:.1f}')


def dispersion(builder):
    d = builder.load('round4_dispersion_scope')
    b = d['dispersion_budget']
    builder.macro('SeptDispMm', 1e3 * b['D_m'], '{:.1f}')
    builder.macro('SeptDispPrimeMrad', 1e3 * b['Dp'], '{:.1f}')
    builder.macro('SeptBetaDivUrad', 1e6 * b['betatron_divergence_rad'], '{:.0f}')
    builder.macro('SeptDispDivUrad', 1e6 * b['dispersive_divergence_rad'], '{:.0f}')
    builder.macro('SeptShotAngleUrad', 1e6 * b['shot_angle_rad'], '{:.0f}')
    acc = d['production_accuracy']
    builder.macro('ThinProdCurrentUrad', 1e6 * abs(acc['current']['midplane']['thin_minus_3d'][1]), '{:.0f}')
    builder.macro('ThinProdExtremumUrad', 1e6 * abs(acc['extremum']['midplane']['thin_minus_3d'][1]), '{:.0f}')
    builder.macro('SlicedProdMax', _sci(max(abs(v['midplane']['sliced_minus_3d'][1]) for v in acc.values())))
    if 'FinalAngleWidth' in builder.macros:  # window width [mrad] from the final_window step; allowance = width / 10
        builder.macro('ThinProdRatio', 1e6 * abs(acc['current']['midplane']['thin_minus_3d'][1])
                      / (100 * float(builder.macros['FinalAngleWidth'])), '{:.1f}')


def vertical_steering(builder):
    d = builder.load('round4_vertical_steering')['budgets']
    for b, bt in (('zero', 'Zero'), ('full', 'Full')):
        for model, short in MODELS:
            builder.macro(f'Vs{bt}{short}', 100 * d[b]['xy'][model]['mean'], '{:.1f}' if model != 'gap' else '{:+.1f}')
            _pts(builder, f'VsGain{bt}{short}', d[b]['paired_xy_minus_x'][model])
    for key, tag in (('jitter_cost_x_only_steering', 'X'), ('jitter_cost_xy_steering', 'XY')):
        if key in d.get('full', {}):
            for model, short in MODELS:
                _pts(builder, f'VsJit{tag}{short}', d['full'][key][model])
    comp = builder.load('round4_vertical_steering').get('jitter_components')
    if comp:
        for level, lt in (('x_only', 'Pos'), ('xp_only', 'Ang')):
            for model, short in MODELS:
                _pts(builder, f'VsComp{lt}{short}', comp[level]['cost_xy_steering'][model])


def macros(builder):
    for key, fn in (('round4_ablation', ablation), ('round4_points_test', points), ('round4_associations', associations),
                    ('round4_loss_locations', loss_locations), ('round4_dispersion_scope', dispersion),
                    ('round4_vertical_steering', vertical_steering)):
        if builder.has(key):
            fn(builder)
