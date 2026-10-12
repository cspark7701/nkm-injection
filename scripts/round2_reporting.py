"""Campaign-03 report panels; all numerical inputs are loaded through the manifest."""
import numpy as np
import matplotlib.pyplot as plt
from nkm_injection.injection_study import wilson_interval


def scientific(value):
    if value==0:return '0'
    exponent=int(np.floor(np.log10(abs(value))))
    return f'{value/10**exponent:.2f}\\times10^{{{exponent}}}'


def parameters(builder):
    if builder.has('round2_lattice_parameters'):
        d=builder.load('round2_lattice_parameters')
        if 'source_elements' in d:builder.macro('FinalSourceElements',d['source_elements'],'{:d}')
        for key,name,scale,fmt in (('rf_frequency_hz','FinalRFfreqMHz',1e-6,'{:.3f}'),
                                   ('rf_voltage_V','FinalRFvoltageMV',1e-6,'{:.2f}'),
                                   ('bunch_length_m','FinalStoredBunchMm',1e3,'{:.2f}')):
            builder.macro(name,d[key]*scale,fmt)
        builder.macro('FinalAlphaC',scientific(d['momentum_compaction']))
        builder.macro('FinalSynchTune',scientific(d['tunes'][2]))
        for value,name in zip(d['damping_times_s'],('X','Y','Z')):builder.macro('FinalDamping'+name+'Ms',value*1e3,'{:.2f}')
        beam=d['study_config']['injected_beam']
        builder.macro('FinalInjectedBunchMm',beam['bunch_length_m']*1e3,'{:.1f}')
        builder.macro('FinalInjectedEmitNm',beam['emit_x_m_rad']*1e9,'{:.2f}')
    if builder.has('round2_trajectory_final'):
        d=builder.load('round2_trajectory_final');rows=[];errors=[]
        labels={'nominal':'nominal','lower_window':'lower angle','upper_window':'upper angle',
                'vertical_position':'vertical position','vertical_angle':'vertical angle','vertical_both':'both vertical',
                'delta_minus':r'$\delta<0$','delta_plus':r'$\delta>0$'}
        for r in d['cases']:
            b=r['initial'];e=np.abs(next(s for s in r['slices'] if s['n_slices']==640)['minus_reference'][:4]);errors.append(e)
            rows.append(f"{labels[r['case']]} & {b[2]*1e3:.1f} & {b[3]/(1+b[4])*1e3:.1f} & {b[4]*1e3:.1f} & "+
                        ' & '.join(f'{v*1e9:.3f}' for v in e)+r' \\')
        builder.macro('ODEValidationRows','\n'.join(rows))
        for value,name in zip(np.max(errors,axis=0),('X','Px','Y','Py')):builder.macro('ODEMax'+name,scientific(value))
        builder.macro('ODEEdgeLoMrad',d['edge_offsets_mrad'][0],'{:.3f}')
        builder.macro('ODEEdgeHiMrad',d['edge_offsets_mrad'][1],'{:.3f}')


def window_points(rows,axis):
    points=[]
    for offset in sorted({r['offset_mm_or_mrad'] for r in rows if r['axis']==axis}):
        selected=[r for r in rows if r['axis']==axis and r['offset_mm_or_mrad']==offset]
        k=sum(r['captured'] for r in selected);n=sum(r['n_particles'] for r in selected)
        points.append({'offset':offset,'capture':k/n,'ci95':wilson_interval(k,n),'captured':k,'n':n})
    return points


def window_bounds(rows,axis,threshold=.8):
    points=window_points(rows,axis);crossings=[]
    if not any(p['offset']==0 and p['capture']>=threshold for p in points):
        raise ValueError(f'{axis} nominal point does not meet the threshold')
    for left,right in zip(points[:-1],points[1:]):
        x0,x1=left['offset'],right['offset'];c0,c1=left['capture'],right['capture']
        if c0==threshold:crossings.append(x0)
        if (c0-threshold)*(c1-threshold)<0:crossings.append(x0+(threshold-c0)*(x1-x0)/(c1-c0))
    if points[-1]['capture']==threshold:crossings.append(points[-1]['offset'])
    negative=[x for x in crossings if x<0];positive=[x for x in crossings if x>0]
    if not negative or not positive:raise ValueError(f'{axis} window is not bracketed')
    return max(negative),min(positive)


def window(builder):
    if not builder.has('round2_window'):return
    data=builder.load('round2_window');fig,axes=plt.subplots(1,2,figsize=(7.4,3.0),layout='constrained')
    for axis,ax,label,prefix in zip(('angle','position'),axes,('angle offset [mrad]','position offset [mm]'),('FinalAngle','FinalPosition')):
        points=window_points(data['rows'],axis);x=[p['offset'] for p in points]
        ax.plot(x,[p['capture']*100 for p in points],'o-',color='#1765a6')
        ax.fill_between(x,[p['ci95'][0]*100 for p in points],[p['ci95'][1]*100 for p in points],color='#1765a6',alpha=.15)
        ax.axhline(80,color='.4',ls='--');ax.axvline(0,color='.5',ls=':',lw=.7)
        ax.set_xlabel(label);ax.set_ylabel('500-turn capture [%]');ax.set_ylim(-2,102)
        lo,hi=window_bounds(data['rows'],axis)
        for value,name in ((lo,'Lo'),(hi,'Hi'),(hi-lo,'Width')):builder.macro(prefix+name,value,'{:.2f}')
    builder.save(fig,'fig5_operating_window',['round2_window'],
                 'design-emittance beam and reference chamber; 2 x 500 particles, 500 native turns; 95% particle Wilson intervals; crossing cells refined to 0.1 mm/mrad')


def validation(builder):
    if not builder.has('round2_validation'):return
    data=builder.load('round2_validation');rows=data['rows']
    if builder.has('round2_backend_contract'):
        contract=builder.load('round2_backend_contract')
        builder.macro('FinalBackendTangentMax',scientific(max(contract['absolute_one_turn_difference'])))
    def selected(case):return [r for r in rows if r['case']==case]
    def aggregate(case,turns):
        rs=selected(case);n=sum(r['n_particles'] for r in rs)
        k=sum(r['survival_counts'][str(turns)] for r in rs)
        return k/n,wilson_interval(k,n),k,n
    fig,axes=plt.subplots(1,3,figsize=(7.4,3.0),layout='constrained')
    for i,case in enumerate(('nominal_native','nominal_linear')):
        cap,ci,_,_=aggregate(case,500)
        axes[0].bar(i,cap*100,color=('#1765a6','#dc7b23')[i])
        axes[0].errorbar(i,cap*100,yerr=[[(cap-ci[0])*100],[(ci[1]-cap)*100]],fmt='none',ecolor='.2',capsize=4)
        builder.macro('FinalBackend'+('Native' if i==0 else 'Linear'),cap*100,'{:.1f}')
    axes[0].set_xticks([0,1],['native','affine']);axes[0].set_ylabel('500-turn capture [%]')
    turns=(100,500,1000,2000,4000);values=[aggregate('nominal_native',t) for t in turns]
    axes[1].plot(turns,[v[0]*100 for v in values],'o-',color='#1765a6')
    axes[1].fill_between(turns,[v[1][0]*100 for v in values],[v[1][1]*100 for v in values],color='#1765a6',alpha=.15)
    axes[1].set_xlabel('turns');axes[1].set_ylabel('nominal survival [%]')
    for i,(case,label) in enumerate((('lower_edge','lower edge'),('upper_edge','upper edge'),('degraded_ring','ring 5501'))):
        a=aggregate(case,500);b=aggregate(case,4000)
        axes[2].plot([i-.12,i+.12],[a[0]*100,b[0]*100],'-',color='#1765a6',lw=.8)
        for x,value,marker,face,label in ((i-.12,a,'o','#1765a6','500 turns'),
                                          (i+.12,b,'s','white','4000 turns')):
            cap,ci,_,_=value
            axes[2].errorbar(x,cap*100,yerr=[[(cap-ci[0])*100],[(ci[1]-cap)*100]],
                            fmt=marker,color='#1765a6',markerfacecolor=face,capsize=2,
                            label=label if i==0 else '_nolegend_')
        for value,name in ((a[0],'Short'),(b[0],'Long'),(b[1][0],'LongLo'),(b[1][1],'LongHi')):
            builder.macro('Final'+{'lower_edge':'Lower','upper_edge':'Upper','degraded_ring':'Degraded'}[case]+name,value*100,'{:.1f}')
    axes[2].set_xticks(range(3),['lower','upper','degraded']);axes[2].set_ylabel('500 to 4000 turns [%]')
    axes[2].legend(loc='center left',fontsize=7)
    long=aggregate('nominal_native',4000);short=aggregate('nominal_native',500)
    for value,name in ((long[0],'FinalLong'),(long[1][0],'FinalLongLo'),(long[1][1],'FinalLongHi'),
                       (short[0]-long[0],'FinalLateLoss')):builder.macro(name,value*100,'{:.1f}')
    builder.save(fig,'fig3_model_validation',['round2_validation'],
                 '3-D NKM at final point and chamber; nominal 2 x 500 particles; fresh seeds 2001/2002 at edges and degraded ring; Wilson intervals conditional on model')


def robustness(builder):
    if not builder.has('round2_robustness') or not builder.has('round2_tuning'):return
    data=builder.load('round2_robustness');tuning=builder.load('round2_tuning')
    raw=[builder.load(f'round2_errors_{seed}') for seed in (42,123,777)]
    fig,axes=plt.subplots(1,3,figsize=(7.4,3.1),layout='constrained')
    colors={'fieldmap_3d':'#1765a6','dipole':'#dc7b23'}
    for model,label in (('fieldmap_3d','3-D NKM'),('dipole','dipole')):
        caps=sorted(r['models'][model]['capture_fraction']*100 for d in raw for r in d['realizations'] if r['sample_id']>=0)
        axes[0].step(caps,np.arange(1,len(caps)+1)/len(caps),where='post',color=colors[model],label=label)
    axes[0].set_xlabel('500-turn capture [%]');axes[0].set_ylabel('fraction of joint realizations');axes[0].legend()
    jitter=data['paired_jitter'];levels=('0','0.25','0.5','0.75','1');x=np.array(list(map(float,levels)))
    axes[1].plot(x,[100*jitter[q]['mean'] for q in levels],'o-',color=colors['fieldmap_3d'],label='NKM mean')
    axes[1].fill_between(x,[100*jitter[q]['mean_ci95'][0] for q in levels],
                         [100*jitter[q]['mean_ci95'][1] for q in levels],color=colors['fieldmap_3d'],alpha=.15)
    axes[1].plot(x,[100*jitter[q]['p10'] for q in levels],'s--',color=colors['fieldmap_3d'],label='NKM p10')
    axes[1].plot(x,[100*jitter[q]['dipole']['mean_capture'] for q in levels],'o-',color=colors['dipole'],label='dipole mean')
    axes[1].set_xlabel('booster jitter / reference');axes[1].set_ylabel('capture [%]');axes[1].legend(fontsize=7)
    for i,level in enumerate(('0.0','0.25')):
        result=tuning['statistics'][level];gain=result['paired_gain']*100;ci=np.array(result['gain_ci95'])*100
        axes[2].errorbar(i,gain,yerr=[[gain-ci[0]],[ci[1]-gain]],fmt='o',color=colors['fieldmap_3d'],capsize=4)
    axes[2].axhline(0,color='.5',lw=.7);axes[2].set_xticks([0,1],['zero jitter','quarter jitter'])
    axes[2].set_ylabel('tuned minus untuned [points]')
    for model,prefix in (('fieldmap_3d','FinalNkm'),('dipole','FinalDip')):
        stats=data['pooled'][model]
        for key,name in (('mean_capture','Mean'),('median_capture','Median'),('p10_capture','Pten'),
                         ('fraction_realizations_above_threshold','AboveEighty')):
            builder.macro(prefix+name,stats[key]*100,'{:.1f}')
        for value,name in zip(stats['mean_ci95_cluster_bootstrap'],('Lo','Hi')):builder.macro(prefix+name,value*100,'{:.1f}')
    pair=data['nkm_minus_dipole']
    for value,name in zip([pair['mean_difference'],*pair['ci95']],('Diff','DiffLo','DiffHi')):
        builder.macro('FinalControl'+name,value*100,'{:+.1f}')
    for level,name in (('0','Zero'),('0.25','Quarter'),('0.5','Half'),('1','Full'),('x_only','Xonly'),('xp_only','Xponly')):
        stats=jitter[level]
        for key,quantity in (('mean','Mean'),('median','Median'),('p10','Pten'),('fraction_ge_80pct','AboveEighty')):
            builder.macro('FinalJitter'+name+quantity,stats[key]*100,'{:.1f}')
        for value,quantity in zip([stats['mean_difference'],*stats['ci95']],('Diff','DiffLo','DiffHi')):
            builder.macro('FinalJitter'+name+quantity,value*100,'{:+.1f}')
    for level,name in (('0.0','Zero'),('0.25','Quarter')):
        result=tuning['statistics'][level]
        for value,quantity in zip([result['paired_gain'],*result['gain_ci95']],('Gain','GainLo','GainHi')):
            builder.macro('FinalTune'+name+quantity,value*100,'{:+.1f}')
        for key,quantity in (('mean_capture','Mean'),('median_capture','Median'),('p10_capture','Pten'),
                             ('fraction_realizations_above_threshold','AboveEighty')):
            builder.macro('FinalTune'+name+quantity,result['tuned'][key]*100,'{:.1f}')
    rows=[]
    for level in ('0','0.25','0.5','0.75','1','x_only','xp_only'):
        r=jitter[level];label=level.replace('_',r'\_')
        rows.append(f"{label} & {r['mean']*100:.1f} & {r['median']*100:.1f} & {r['p10']*100:.1f} & "
                    f"{r['fraction_ge_80pct']*100:.0f} & {r['mean_difference']*100:+.1f} & "
                    f"[{r['ci95'][0]*100:+.1f}, {r['ci95'][1]*100:+.1f}] \\\\")
    builder.macro('FinalJitterRows','\n'.join(rows))
    rows=[]
    for r in data['partial_correlations']:
        label=r['variable'].replace('_',r'\_')
        rows.append(f"{label} & {r['partial_spearman_rho']:+.2f} & {r['p_value']:.3g} & {r['p_holm']:.3g} \\\\")
    builder.macro('FinalRankRows','\n'.join(rows))
    names={'booster_x_m':'booster position', 'booster_xp_rad':'booster angle',
           'energy_dp_p':'mean energy', 'beta_mismatch_x':'horizontal beta mismatch',
           'beta_mismatch_y':'vertical beta mismatch', 'nkm_scale_err':'common NKM amplitude',
           'nkm_dx_m':'NKM displacement', 'ring_co_x_m':'residual orbit',
           'septum_x_m':'septum displacement', 'dipole_b_err':'BTS dipole field',
           'septum_strength_rel':'septum strength', 'rf_phase_rad':'RF phase',
           'arrival_time_s':'pulse-relative timing', 'emit_rel':'emittance variation',
           'espread_abs':'energy-spread variation', 'rms_quad_k_err':'quadrupole strength rms',
           'rms_quad_dx_m':'quadrupole horizontal-offset rms',
           'rms_quad_dy_m':'quadrupole vertical-offset rms', 'rms_quad_roll_rad':'quadrupole roll rms'}
    significant=sorted((r for r in data['partial_correlations'] if r['p_holm']<.05),key=lambda r:r['p_holm'])
    if significant:
        terms=[f"{names.get(r['variable'],r['variable'].replace('_',' '))} "
               f"($\\rho={r['partial_spearman_rho']:+.2f}$, $p_\\mathrm{{Holm}}={scientific(r['p_holm'])}$)"
               for r in significant[:5]]
        summary='The smallest Holm-adjusted probabilities below 0.05 correspond to '+ '; '.join(terms)+'.'
    else:
        summary='No sampled-error magnitude passes the Holm-adjusted 0.05 threshold.'
    builder.macro('FinalRankSummary',summary)
    builder.save(fig,'fig8_robustness',['round2_robustness','round2_tuning']+[f'round2_errors_{s}' for s in (42,123,777)],
                 '150 joint draws conditional on ten corrected rings; paired jitter has 50 draws; tuning gains use held-out particles and 95% realization bootstrap')
