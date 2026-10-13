#!/usr/bin/env python3
"""Track nominal BTS distributions and plot positions [mm] versus slopes [mrad]."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import shutil

import at
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from nkm_injection.bts_journal import JournalBeam, independent_maps, lattice_for
from nkm_injection.optics import DEFAULT_BTS_ENTRANCE_TWISS

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / 'docs/paper_bts/generated/round2_designs.json'


def slopes(coordinates):
    """Convert AT normalized canonical momenta to geometric slopes [rad]."""
    out = coordinates.copy()
    pz2 = (1 + out[4])**2 - out[1]**2 - out[3]**2
    if not np.all(np.isfinite(out)) or np.any(pz2 <= 0):
        raise ValueError('Invalid particle coordinates or longitudinal momentum')
    out[[1, 3]] /= np.sqrt(pz2)
    return out


def run(output, particles=20000, seed=83001):
    if particles < 1000 or seed < 0:
        raise ValueError('At least 1000 particles and a nonnegative seed required')
    output.mkdir(parents=True, exist_ok=False)
    beam = JournalBeam()
    initial = np.asfortranarray(np.random.default_rng(seed).multivariate_normal(
        np.zeros(6), beam.covariance(), size=particles).T)
    designs = json.loads(DESIGNS.read_text())['designs']['baseline']['nominal']
    arrays = {'initial_at': initial, 'initial_slopes': slopes(initial)}
    summary = {'particles': particles, 'seed': seed, 'beam': asdict(beam),
               'entrance_twiss': asdict(DEFAULT_BTS_ENTRANCE_TWISS),
               'energy_eV': 4e9, 'distribution': 'untruncated centred Gaussian with dispersion',
               'errors': 'nominal; no machine errors or shot jitter', 'integration_steps': 40,
               'observation_points': 'm1 entrance before first element; m4 after final element',
               'loss_definition': 'nonfinite tracked coordinate at exit after all configured apertures',
               'aperture_halfwidths_m': {'0.0': .01935, '6.833': .03, '11.761': .03, '21.789': .01935},
               'slope_definition': "x'=px/sqrt((1+delta)^2-px^2-py^2); similarly y'",
               'rms_relative_validation_tolerance': .02, 'designs': {}}
    for name in ['reference', 'low_beta']:
        lattice = lattice_for(designs[name]['strengths_m_minus2'])
        tracked = at.lattice_track(lattice, initial.copy(order='F'), nturns=1,
                                   refpts=[len(lattice)])[0][:, :, 0, 0]
        surviving = np.all(np.isfinite(tracked), axis=0)
        lost = int(particles - surviving.sum())
        if lost:
            raise ValueError('Nominal diagnostic unexpectedly lost particles; inspect before plotting')
        linear = independent_maps(lattice)[0][-1] @ initial[:5]
        rms = tracked[:4].std(axis=1, ddof=1)
        relative_error = np.abs(rms / linear[:4].std(axis=1, ddof=1) - 1)
        if np.max(relative_error) > .02:
            raise ValueError('Tracked RMS differs from independent-map prediction by over 2%')
        arrays[name+'_final_at'] = tracked
        arrays[name+'_final_slopes'] = slopes(tracked)
        summary['designs'][name] = {'strengths_m_minus2': designs[name]['strengths_m_minus2'],
                                   'surviving_particles': int(surviving.sum()), 'lost_particles': lost,
                                   'max_rms_relative_error': float(relative_error.max()),
                                   'final_rms_position_m': rms[[0, 2]].tolist(),
                                   'final_slope_covariance': np.cov(slopes(tracked)).tolist()}
    plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 3, figsize=(7, 4.6), sharex='row', sharey='row')
    views = [('initial_slopes', 'Entrance (shared)'),
             ('reference_final_slopes', 'Exit: reference'),
             ('low_beta_final_slopes', 'Exit: refined low beta')]
    for col, (key, title) in enumerate(views):
        values = arrays[key] * 1000
        for row, (position, angle, plane) in enumerate([(0, 1, 'x'), (2, 3, 'y')]):
            ax = axes[row, col]
            ax.scatter(values[position], values[angle], s=1, alpha=.15, rasterized=True,
                       color='C0', edgecolors='none')
            ellipses = at.plot.plot_sigma(np.cov(values), axis=(plane, plane+'p'), scale=2,
                                         ax=ax, color='black', linewidth=1, label='2 RMS ellipse')
            for line in ellipses:
                line.set_xdata(line.get_xdata() + values[position].mean())
                line.set_ydata(line.get_ydata() + values[angle].mean())
            ax.set_title(title if row == 0 else '')
            ax.set_xlabel(f'{plane} [mm]')
            ax.set_ylabel(f"{plane}' [mrad]" if col == 0 else '')
            ax.grid(alpha=.2)
    axes[0, 0].legend(fontsize=7, loc='upper right')
    fig.tight_layout()
    fig.savefig(output/'phase_space.pdf', metadata={'CreationDate': None})
    plt.close(fig)
    np.savez_compressed(output/'particles.npz', **arrays)
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    sources = [DESIGNS, Path(__file__).resolve(), ROOT/'src/nkm_injection/bts_journal.py',
               ROOT/'src/nkm_injection/bts_lattice.py', ROOT/'src/nkm_injection/optics.py']
    configuration = {'pyat_version': at.__version__, 'numpy_version': np.__version__,
                     'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in sources}, 'seed': seed, 'particles': particles}
    (output/'configuration.json').write_text(json.dumps(configuration, indent=2)+'\n')
    shutil.copy2(__file__, output/'generating_script.py')
    print(json.dumps({k: {'lost': v['lost_particles'], 'rms_error': v['max_rms_relative_error']}
                      for k, v in summary['designs'].items()}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--particles', type=int, default=20000)
    parser.add_argument('--seed', type=int, default=83001)
    args = parser.parse_args()
    run(args.output_dir, args.particles, args.seed)
