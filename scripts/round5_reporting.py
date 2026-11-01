"""Round-5 paired jitter reporting from hash-verified manifest artifacts."""
import numpy as np
import matplotlib.pyplot as plt


def pp(d):
    return f"{100*d['mean']:+.1f} [{100*d['ci95'][0]:+.1f}, {100*d['ci95'][1]:+.1f}]"


def macros(builder):
    if not builder.has('round5_jitter'):
        return
    data = builder.load('round5_jitter')
    if builder.has('round5_companion_audit'):
        audit = builder.load('round5_companion_audit')
        builder.macro('RFiveJitterXBeamUnits', audit['jitter_in_nominal_rms_sizes'][0], '{:.1f}')
        builder.macro('RFiveJitterXpBeamUnits', audit['jitter_in_nominal_rms_sizes'][1], '{:.1f}')
    if builder.has('round5_bts_jitter_reference'):
        companion = builder.load('round5_bts_jitter_reference')
        ref = next(row['designs']['reference'] for row in companion['rows'] if row['scale'] == 0)
        builder.macro('RFiveBtsYmm', 1000*ref['exit_centroid_rms_m_rad'][2], '{:.2f}')
        builder.macro('RFiveBtsYpMrad', 1000*ref['exit_centroid_rms_m_rad'][3], '{:.3f}')
    rows = data['rows']
    main, supplemental = [], []
    for row in rows:
        scale = row['scale']
        nkm, dip = row['fieldmap_3d'], row['dipole']
        result = 'reference' if scale == 0 else ('pass' if row['nkm_noninferior_to_zero_jitter'] else 'fail')
        main.append(f"{scale:g} & {100*nkm['mean']:.1f} & {100*dip['mean']:.1f} & "
                    f"{pp(nkm['jitter_cost'])} & {pp(row['gap'])} & {result} \\\\")
        supplemental.append(f"{scale:g} & {100*nkm['zero_fraction']:.0f} & {100*dip['zero_fraction']:.0f} & "
                            f"{pp(dip['jitter_cost'])} & {pp(row['gap_change'])} \\\\")
        if scale in (.1, .25):
            label = 'Tenth' if scale == .1 else 'Quarter'
            for suffix, record in [('Gap', row['gap']), ('Cost', nkm['jitter_cost'])]:
                builder.macro('RFive'+label+suffix, 100*record['mean'], '{:+.1f}')
                builder.macro('RFive'+label+suffix+'Lo', 100*record['ci95'][0], '{:+.1f}')
                builder.macro('RFive'+label+suffix+'Hi', 100*record['ci95'][1], '{:+.1f}')
    builder.macro('RFiveJitterRows', '\n'.join(main))
    builder.macro('RFiveJitterSupplementRows', '\n'.join(supplemental))
    passing = data['largest_passing_nonzero_tested_scale']
    builder.macro('RFivePassingScale', 'none' if passing is None else f'{passing:g}')
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
    x = np.array([row['scale'] for row in rows])
    for name, label, color in [('fieldmap_3d', 'NKM', '#1f5fa8'), ('dipole', 'Uniform kick', '#e87819')]:
        y = 100*np.array([row[name]['mean'] for row in rows])
        ci = 100*np.array([row[name]['ci95'] for row in rows])
        axes[0].plot(x, y, 'o-', label=label, color=color)
        axes[0].fill_between(x, ci[:,0], ci[:,1], color=color, alpha=.15)
    gap = 100*np.array([row['gap']['mean'] for row in rows])
    ci = 100*np.array([row['gap']['ci95'] for row in rows])
    axes[1].errorbar(x, gap, yerr=np.vstack([gap-ci[:,0], ci[:,1]-gap]), fmt='o-', color='#1f5fa8', capsize=3)
    axes[1].axhline(0, color='.5', ls=':', lw=.8)
    axes[0].set_ylabel('Mean capture [%]')
    axes[1].set_ylabel('NKM minus uniform kick [points]')
    axes[0].legend(fontsize=7)
    for ax in axes:
        ax.set_xlabel('Booster jitter / assumed stress level')
        ax.grid(alpha=.25)
    fig.tight_layout()
    builder.save(fig, 'fig12_two_plane_jitter', ['round5_jitter'],
                 '50 paired realizations, two-plane ideal steering; pointwise 95% realization intervals; sampled scales joined as guides.')
