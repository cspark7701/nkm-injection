from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path('docs/paper_bts');R=Path('results/bts_journal_campaign_r2_20261013')
c=json.loads((P/'generated/round2_comparison.json').read_text());d=json.loads((P/'generated/round2_designs.json').read_text());s=json.loads((P/'generated/round2_spatial.json').read_text());old=json.loads((P/'generated/round2_stations.json').read_text())
plt.rcParams.update({'font.size':9,'pdf.fonttype':42})
from export_bts_at_figures import export_figures
export_figures(P/'figures')
fig,ax=plt.subplots(1,2,figsize=(7,2.9))
for label,rec in zip(['Reference','Old low beta'],old['nominal']):
 for axis,style in [(0,'-o'),(1,'--s')]:
  rows=[r for r in rec['stations'] if r['axis']==axis];ax[0].plot([r['s_m'] for r in rows],[r['clearance_m']*1000 for r in rows],style,label=label+' '+('x' if axis==0 else 'y'))
ax[0].set(xlabel='Station s [m]',ylabel='Nominal clearance [mm]');ax[0].legend(fontsize=7)
for i,label in enumerate(['Reference','Old low beta']):
 vals=[old['active_frequencies'][i].get(k,0) for k in ['[1, 0]','[34, 0]','[34, 1]']];ax[1].bar(np.arange(3)+(i-.5)*.32,vals,width=.32,label=label)
ax[1].set_xticks(range(3),['Entrance x','Exit x','Exit y']);ax[1].set_ylabel('Limiting shots / 600');ax[1].legend(fontsize=7);fig.tight_layout();fig.savefig(P/'figures/round2_stations.pdf');plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(7,2.9),sharey=True)
labels={'baseline':'Baseline','horizontal_restriction':'Hypothetical x restriction','vertical_restriction':'Hypothetical y restriction'}
for ax,(regime,results) in zip(axes,c['results'].items()):
 for i,name in enumerate(['low_beta','clearance']):
  v=results[name]['paired_difference'];lo,hi=np.array(v['ci95_m'])*1000;m=v['mean_m']*1000
  ax.errorbar(m,i,xerr=[[m-lo],[hi-m]],fmt='o',capsize=3)
 ax.axvline(0,color='grey',lw=1);ax.axvline(.1,color='grey',ls=':',lw=1);ax.axvline(-.1,color='grey',ls=':',lw=1);ax.set_title(labels[regime],fontsize=8);ax.set_xlabel('Paired change [mm]');ax.set_yticks([0,1],['Low beta','Clearance']);ax.invert_yaxis()
fig.tight_layout();fig.savefig(P/'figures/round2_strategies.pdf');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(6.5,2.9))
for ax,regime in zip(axes,['horizontal_restriction','vertical_restriction']):
 for name in ['reference','low_beta','clearance']:
  vals=[r for r in d['nominal_sweep'] if r['regime']==regime and r['design']==name];reference={r['halfwidth_m']:r['minimum_m'] for r in d['nominal_sweep'] if r['regime']==regime and r['design']=='reference'};ax.plot([r['halfwidth_m']*1000 for r in vals],[(r['minimum_m']-reference[r['halfwidth_m']])*1000 for r in vals],'-o',label=name.replace('_',' '))
 ax.set_xscale('log');ax.set_xticks([1.5,3,5,30],['1.5','3','5','30']);ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter());ax.set_xlabel('Hypothetical halfwidth [mm]');ax.set_title('Horizontal m2' if regime.startswith('horizontal') else 'Vertical m3');ax.legend(fontsize=7)
axes[0].set_ylabel('Nominal change vs reference [mm]');fig.tight_layout();fig.savefig(P/'figures/round2_sweep.pdf');plt.close(fig)
macros={'NewBaselineMean':c['results']['baseline']['low_beta']['paired_difference']['mean_m']*1000,'NewBaselineLo':c['results']['baseline']['low_beta']['paired_difference']['ci95_m'][0]*1000,'NewBaselineHi':c['results']['baseline']['low_beta']['paired_difference']['ci95_m'][1]*1000,'NewMomentError':c['max_centred_moment_error_m']*1e6}
(P/'generated/round2_results.tex').write_text('% Exported from round2 selected numerical summaries.\n'+''.join('\\newcommand{\\Bts'+k+'}{'+f'{v:.4f}'+'}\n' for k,v in macros.items()))
rows=[]
for regime,results in c['results'].items():
 for name in ['low_beta','clearance']:
  v=results[name];ci=v['paired_difference'];lo,hi=np.array(ci['ci95_m'])*1000
  effect='--' if regime=='baseline' and name=='clearance' else f"{ci['mean_m']*1000:+.3f}"
  limits='degenerate' if regime=='baseline' and name=='clearance' else f'[{lo:+.3f}, {hi:+.3f}]'
  rows.append(labels[regime].replace('Hypothetical ','')+' & '+name.replace('_',' ')+' & '+f"{d['designs'][regime]['nominal'][name]['clearance']['minimum_m']*1000:.3f}"+' & '+effect+' & '+limits+r' \\')
(P/'generated/round2_strategy_rows.tex').write_text('\n'.join(rows)+'\n')
rows=[]
for regime,results in c['results'].items():
 for name,v in results.items():rows.append(labels[regime].replace('Hypothetical ','')+' & '+name.replace('_',' ')+' & '+str(v['lost_particles'])+' & '+str(v['loss_blocks'])+r' \\')
(P/'generated/round2_loss_rows.tex').write_text('\n'.join(rows)+'\n')
rows=[]
for i in range(0,8,2):
 r=old['nominal'][0]['stations'][i];a=old['nominal'][1]['stations'][i:i+2];b=old['nominal'][0]['stations'][i:i+2]
 rows.append(f"{r['s_m']:.3f} & {b[0]['clearance_m']*1000:.3f} & {a[0]['clearance_m']*1000:.3f} & {b[1]['clearance_m']*1000:.3f} & {a[1]['clearance_m']*1000:.3f}"+r' \\')
(P/'generated/round2_station_rows.tex').write_text('\n'.join(rows)+'\n')
print('Exported four figures, tables and numerical macros.')

# Complete tabular environments keep booktabs rules in the same TeX input.
headers={
 'round2_station_rows.tex':('rrrrr',r'$s$ [m] & $c_{x,R}$ & $c_{x,L}$ & $c_{y,R}$ & $c_{y,L}$'),
 'round2_strategy_rows.tex':('llrrl',r'Regime & Strategy & Nominal & Mean change & 95\% interval'),
 'round2_loss_rows.tex':('llrr',r'Regime & Strategy & Lost particles & Affected blocks')}
for filename,(columns,header) in headers.items():
 path=P/'generated'/filename
 path.write_text('\\begin{tabular}{'+columns+'}\\toprule\n'+header+' '+chr(92)*2+'\\midrule\n'+path.read_text()+'\\bottomrule\\end{tabular}\n')

raw=json.loads((R/'comparison/raw_realizations.json').read_text());components={}
for regime,index,axis in [('horizontal_restriction',12,0),('vertical_restriction',22,1)]:
 components[regime]={}
 for name,record in d['designs'][regime]['nominal'].items():
  station=next(r for r in record['clearance']['stations'] if (r['index'],r['axis'])==(index,axis))
  samples=[next(r for r in row['results'][regime][name]['stations'] if (r['index'],r['axis'])==(index,axis)) for row in raw]
  components[regime][name]={'nominal_betatron_rms_m':np.sqrt(station['betatron_variance_m2']),'nominal_dispersive_rms_m':np.sqrt(station['dispersive_variance_m2']),'mean_absolute_centroid_m':np.mean([abs(r['centroid_m']) for r in samples]),'mean_five_sigma_size_m':np.mean([5*r['sigma_m'] for r in samples])}
(P/'generated/round2_components.json').write_text(json.dumps(components,indent=2)+'\n')
