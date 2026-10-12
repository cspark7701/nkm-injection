#!/usr/bin/env python3
"""D7 dimensionless sagitta scaling and vector sliced-map comparison; single centroids."""
import argparse
from dataclasses import replace,asdict
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nkm_injection.injection_study import InjectionStudyConfig
from nkm_injection.wire_field import FilamentGeometry,FilamentNKMKicker
from nkm_injection.sliced_vector_map import integrated_filament_kicks,sliced_vector_map


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args();out=a.output_dir
    if out.exists():raise SystemExit('Output must be new')
    out.mkdir(parents=True);rows=[]
    cfg=replace(InjectionStudyConfig(),field_scale=.85)
    for family in (1.,1.25):
        for length in (.2,.35,.525,.75,1.):
            for strength in (.5,1.,1.5):
                g=replace(FilamentGeometry(),x1_m=.0053*family,y1_m=.0053*family,
                          x2_m=.01025*family,y2_m=.01025*family,half_length_m=length/2,
                          current_A=3000*.525/length*family*strength)
                xs=np.linspace(-.02*family,-.002*family,2001)
                k=integrated_filament_kicks(xs,0.,g,scale=cfg.field_scale)[0];j=np.argmin(k)
                peak=float(k[j]);xc=float(xs[j]);above=xs[np.abs(k)>=abs(peak)/2]
                w=float(above.max()-above.min())
                b=np.array([xc,-peak,.001*family,.0002,0.,0.])
                thin=b.copy();kx,ky=integrated_filament_kicks(b[0],b[2],g,scale=cfg.field_scale)
                thin[1]+=float(kx);thin[3]+=float(ky)
                full=b[:,None].copy();span=length/2+.1875
                lost=FilamentNKMKicker(cfg,n_slices=1280,s_span_m=span,geometry=g).apply(full,0.)
                if lost.any():raise RuntimeError('Scaling centroid lost')
                sliced=sliced_vector_map(b,g,scale=cfg.field_scale,slices=1280)
                rows.append({'transverse_family_scale':family,'length_m':length,'strength_scale':strength,
                             'geometry':asdict(g),'peak_kick_rad':peak,'lobe_fwhm_m':w,'eta':abs(peak)*length/(8*w),
                             'initial':b.tolist(),'thin_exit':thin.tolist(),'sliced_exit':sliced.tolist(),
                             'three_d_exit':full[:,0].tolist(),'sliced_minus_3d':(sliced-full[:,0]).tolist(),
                             'thin_minus_3d':(thin-full[:,0]).tolist()})
    fig,axs=plt.subplots(1,2,figsize=(8,3.2),layout='constrained')
    for family,marker in ((1.,'o'),(1.25,'s')):
        selected=[r for r in rows if r['transverse_family_scale']==family]
        for ax,key in zip(axs,('thin_minus_3d','sliced_minus_3d')):
            ax.scatter([r['eta'] for r in selected],[r[key][1]*1e3 for r in selected],marker=marker,label=f'wire scale {family:g}')
            ax.set_xlabel(r'$\eta=|K|L/(8w)$');ax.set_ylabel('horizontal momentum difference [mrad]');ax.axhline(0,color='grey',lw=.5)
    axs[0].set_title('Thin map minus 3-D');axs[1].set_title('Sliced vector map minus 3-D');axs[0].legend()
    fig.savefig(out/'generality_scaling.pdf');plt.close(fig)
    data={'rows':rows,'w_definition':'full width at half maximum of negative horizontal kick lobe',
          'eta_scope':'sagitta divided by lobe width; heuristic expansion parameter, not universal capture criterion',
          'particle_count':1,'distribution':'specified centroids with nonzero y/yprime','energy_spread':0.,
          'initial_twiss':'not applicable','apertures':'1 mm conductor radius; field model domain ±50 mm',
          'loss_definition':'conductor/domain intersection','observation':'NKM centre before and after one passage'}
    (out/'generality_scaling.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
