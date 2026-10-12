#!/usr/bin/env python3
"""D10 native later-turn centroid positions and consistent conditional pulse estimates."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import numpy as np
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring,_apply_kick
from nkm_injection.wire_field import FilamentNKMKicker,FilamentGeometry
from nkm_injection.sliced_vector_map import integrated_filament_kicks
from nkm_injection.pulse_requirements import peak_phase_field_fraction,maximum_peak_phase_duration,thin_shell_diffusion_time
from nkm_injection.chamber import ChamberProfile,apply_chamber
from nkm_injection.ring_error_scenario import refresh_prepared_ring


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--study-config',type=Path,required=True)
    p.add_argument('--window-width-mrad',type=float,default=.74);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--chamber-config',type=Path)
    a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    cfg=InjectionStudyConfig.load(a.study_config);ring=cached_ring(cfg,Path.cwd(),a.output.parent/'_lattice')
    profile=json.loads(a.chamber_config.read_text()) if a.chamber_config else None
    if profile:
        chamber,_=apply_chamber(ring.ring_c,ChamberProfile(**profile),cfg.septum_edge_x_m)
        ring=refresh_prepared_ring(ring,chamber)
    b=np.asarray(ring.orbit6)[:,None].copy();b[0]+=cfg.injection_x_m;b[1]+=cfg.injection_xp_rad
    b=ring.inj_segment.track(b,nturns=1)[0][:,:,0,0]
    _apply_kick(b,FilamentNKMKicker(cfg,n_slices=640),cfg.closed_orbit_x_m)
    tracked,_,loss=ring.ring_c.track(b,nturns=3,refpts=[len(ring.ring_c)],losses=True)
    if loss['loss_map']['islost'].any():raise SystemExit('Native centroid lost before later-pass pulse estimate')
    coords=np.asarray(tracked)[:,0,0,:]
    revolution=ring.circumference_m/299792458.;allow=a.window_width_mrad*1e-3*.1
    turns=[];g=FilamentGeometry()
    for j in range(3):
        full_kick=float(integrated_filament_kicks(coords[0,j],coords[2,j],g,cfg.energy_eV,cfg.field_scale,cfg.kicker_polarity)[0])
        maximum=min(.999999,allow/abs(full_kick)) if full_kick else .999999
        turns.append({'turn':j+1,'coordinate':coords[:,j].tolist(),'straight_line_full_kick_rad':full_kick,
                      'allowed_fraction':maximum,'maximum_peak_phase_duration_s':maximum_peak_phase_duration((j+1)*revolution,maximum)})
    duration=5.3e-6
    timing=[{'duration_s':tau,'deterministic_offset_s':dt,'relative_loss':float(1-peak_phase_field_fraction(dt,tau))}
            for tau in (5e-6,5.3e-6,8e-6) for dt in (1e-9,2e-9,5e-9)]
    train=[{'train_duration_s':t,'peak_at_first_bunch_field_loss_at_last':float(1-peak_phase_field_fraction(t,duration))}
           for t in (100e-9,200e-9,500e-9)]
    shells=[{'conductivity_S_per_m':sigma,'radius_m':.015,'thickness_m':thick,
             'diffusion_time_s':thin_shell_diffusion_time(sigma,.015,thick)} for sigma,thick in ((1e6,1e-6),(5e7,1e-3))]
    out={'study_config':cfg.to_dict(),'native_turns':turns,'revolution_period_s':revolution,
         'window_width_rad':a.window_width_mrad*1e-3,'residual_kick_allowance_rad':allow,
         'allowance_status':'assumed one tenth of conditional 500-turn angular window',
         'peak_phase_maximum_duration_s':min(r['maximum_peak_phase_duration_s'] for r in turns),
         'no_return_field_maximum_duration_s':2*revolution,'compatible_example_duration_s':duration,
         'example_timing_margin_s':revolution-duration/2,
         'example_return_field_fractions':[float(peak_phase_field_fraction(i*revolution,duration)) for i in (1,2,3)],
         'eight_us_first_return_fraction':float(peak_phase_field_fraction(revolution,8e-6)),
         'timing':timing,'train':train,'eddy_shell_scenarios':shells,
         'timing_definition':'listed offsets are deterministic; rms=2 ns is a Gaussian draw in D4, not a hard bound',
         'scope':'native centroid observations plus analytic requirements; no time-dependent capture or measured chamber prediction',
         'particle_count':1,'distribution':'nominal centroid','energy_spread':0.,'initial_twiss':'not applicable',
         'apertures':profile or 'study septum only','loss_definition':'native AT loss','observation':'end of turns 1,2,3 at NKM centre'}
    a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps({k:out[k] for k in
        ('peak_phase_maximum_duration_s','no_return_field_maximum_duration_s','example_return_field_fractions','eight_us_first_return_fraction')},indent=2))


if __name__=='__main__':main()
