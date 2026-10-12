#!/usr/bin/env python3
"""Record manuscript RF/radiation parameters from the source lattice (SI units)."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import at
from nkm_injection.injection_study import InjectionStudyConfig,cached_ring


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-config',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    cfg=InjectionStudyConfig.load(a.study_config)
    source=at.load_mat(cfg.ring_source)
    ring=cached_ring(cfg,Path.cwd(),a.output.parent/'_lattice');rad=ring.ring_c.radiation_parameters()
    data={'study_config':cfg.to_dict(),'source_sha256':hashlib.sha256(Path(cfg.ring_source).read_bytes()).hexdigest(),
          'source_elements':len(source),'source_circumference_m':float(source.circumference),
          'prepared_elements':len(ring.ring_c),
          'rf_frequency_hz':float(ring.ring_c.get_rf_frequency()),'rf_voltage_V':float(rad.voltage),
          'momentum_compaction':float(rad.alphac),'damping_times_s':np.asarray(rad.Tau).tolist(),
          'bunch_length_m':float(rad.sigma_l),'energy_spread':float(rad.sigma_e),
          'energy_loss_per_turn_eV':float(rad.U0),'tunes':np.asarray(rad.fulltunes).tolist(),
          'chromaticities':np.asarray(rad.chromaticities).tolist(),
          'scope':'ideal supplied design lattice; linear radiation equilibrium, assumed vertical coupling separate'}
    a.output.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
