#!/usr/bin/env python3
"""Render selected BTS optics with pyAT; coordinates and beta are in metres."""
import argparse
import hashlib
import json
import warnings
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import at

from nkm_injection.bts_journal import lattice_for, TARGET, SCALES
from nkm_injection.bts_lattice import BTSConfig
from nkm_injection.bts_round2 import spatial_profile, nominal_observables
from nkm_injection.optics import DEFAULT_BTS_ENTRANCE_TWISS

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'docs/paper_bts'


def transfer_line_call(function, *args, **kwargs):
    # pyAT also evaluates periodic stability/chromaticity for plot_linear.
    # This open line has explicit entrance optics, not a periodic solution.
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='Unstable ring', category=at.AtWarning)
        warnings.filterwarnings('ignore', message='FigureCanvasAgg is non-interactive.*',
                                category=UserWarning)
        return function(*args, **kwargs)


def export_figures(output):
    """Validate and draw the original and optimized settings on the same observation mesh."""
    designs = json.loads((PAPER / 'generated/round2_designs.json').read_text())
    original = np.asarray(BTSConfig().quad_strengths_list)
    initial_record = json.loads((PAPER / 'generated/matching.json').read_text())['initial_baseline']
    np.testing.assert_array_equal(original, initial_record['strengths_m_minus2'])
    settings = {'reference': original,
                'low_beta': np.array(designs['designs']['baseline']['nominal']['low_beta']['strengths_m_minus2'])}
    profiles = {name: spatial_profile(lattice_for(k), 64) for name, k in settings.items()}
    saved = json.loads((PAPER / 'generated/round2_spatial.json').read_text())
    np.testing.assert_allclose(profiles['low_beta']['peak_beta_m'],
                               saved['refined_low_beta']['profiles'][-1]['peak_beta_m'], rtol=0, atol=1e-8)
    np.testing.assert_allclose(spatial_profile(lattice_for(original), 1)['peak_beta_m'],
                               initial_record['peak_beta_m'], rtol=0, atol=1e-5)
    profile_sources = [PAPER / 'generated/matching.json', PAPER / 'generated/round2_spatial.json',
                       ROOT / 'src/nkm_injection/bts_lattice.py', ROOT / 'src/nkm_injection/bts_round2.py',
                       ROOT / 'src/nkm_injection/bts_journal.py']
    profile_origin = 'Baseline BTSConfig settings versus the frozen optimized low-beta settings; exact-map profiles'
    tw = DEFAULT_BTS_ENTRANCE_TWISS
    twiss = dict(beta=[tw.beta_x, tw.beta_y], alpha=[tw.alpha_x, tw.alpha_y],
                 dispersion=[tw.disp_x, tw.disp_px, tw.disp_y, tw.disp_py])
    plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 1, figsize=(6.3, 4.2), sharex=True)
    report = {'pyat_version': at.__version__, 'subdivisions': 64,
              'beta_absolute_tolerance_m': 1e-4, 'designs': {}, 'profile_origin': profile_origin,
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in profile_sources + [PAPER / 'generated/round2_designs.json', Path(__file__) ]}}
    for name, label in [('reference', 'Baseline setting (reference)'), ('low_beta', 'Optimized low beta')]:
        profile = profiles[name]
        lattice = lattice_for(settings[name])
        dense = lattice.slice_elements([i for i, e in enumerate(lattice) if e.Length], slices=64)
        _, _, optics = transfer_line_call(at.get_optics, dense, refpts=range(1, len(dense)+1),
                                    twiss_in=twiss, method=at.linopt2)
        expected = np.array([[r['s_m'], *r['beta_m']] for r in profile['rows']])
        np.testing.assert_allclose(optics.s_pos, expected[:, 0], rtol=0, atol=1e-10)
        np.testing.assert_allclose(optics.beta, expected[:, 1:], rtol=0, atol=1e-4)
        report['designs'][name] = {'max_beta_difference_m': float(np.max(abs(optics.beta-expected[:, 1:]))),
                                  'peak_beta_m': optics.beta.max(axis=0).tolist(),
                                  'strengths_m_minus2': settings[name].tolist(), 'label': label,
                                  'exit_lattice_functions': nominal_observables(lattice).tolist(),
                                  'max_normalized_exit_residual': float(np.max(np.abs((nominal_observables(lattice) - TARGET) / SCALES)))}
        for plane, ax in enumerate(axes):
            transfer_line_call(at.plot.plot_linear, dense, ('beta', plane), axes=(ax, None),
                                slices=1, twiss_in=twiss, method=at.linopt2, legend=False)
            line = ax.lines[-1]
            # baseplot omits coincident zero-length end markers from i_range.
            plotted_s = line.get_xdata()
            if plotted_s[0] != 0 or not np.isclose(plotted_s[-1], expected[-1, 0]):
                raise ValueError('Native plot must cover the complete transfer line')
            np.testing.assert_allclose(line.get_ydata(),
                                       np.interp(plotted_s, expected[:, 0], expected[:, plane+1]),
                                       rtol=0, atol=1e-4)
            line.set_label(label)
            line.set_color('C0' if name == 'reference' else 'C1')
            line.set_linestyle('-' if name == 'reference' else '--')
    axes[0].set_ylabel('Horizontal beta [m]')
    axes[1].set_ylabel('Vertical beta [m]')
    axes[1].set_xlabel('Path coordinate [m]')
    for ax in axes:
        ax.set_axisbelow(True)
        ax.grid(True, which='major', color='0.8', linewidth=0.6, alpha=0.8)
    axes[0].legend()
    fig.tight_layout()
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / 'round2_optics.pdf', metadata={'CreationDate': None})
    plt.close(fig)

    reference = lattice_for(original)
    fig, ax = plt.subplots(figsize=(7, 2.6))
    syn = at.plot.plot_synopt(reference, axes=ax)
    if isinstance(syn, tuple):  # pyAT 0.8 returns (synoptic_axes, parent_axes).
        syn = syn[0]
    syn.set_ylim(0, 4.0)
    ax.set_facecolor('none')
    ax.set(xlim=(-0.3, reference.get_s_pos(len(reference))[0] + 0.3), ylim=(0, 1),
           xlabel='Path coordinate [m]', yticks=[])
    ax.spines[['left', 'right', 'top']].set_visible(False)
    s_pos = reference.get_s_pos(range(len(reference) + 1))
    for i, e in enumerate(reference):
        if hasattr(e, 'Limits'):
            ax.axvline(s_pos[i], color='0.4', linestyle=':', linewidth=1)
        centre = s_pos[i] + e.Length / 2
        if isinstance(e, at.Quadrupole):
            ax.text(centre, .43, e.FamName, rotation=90, ha='center', va='bottom', fontsize=7)
        elif e.FamName in ('b1', 'b2', 'b3'):
            ax.text(centre, .30, e.FamName, ha='center', va='bottom', fontsize=7)
        elif isinstance(e, at.Marker):
            last = s_pos[i] >= s_pos[-1] - 1e-9
            ax.text(s_pos[i] + (-.15 if last else .15), .97, e.FamName, ha='right' if last else 'left',
                    va='top', fontsize=7, color='0.3')
    # Injection-system dipole elements, named in the same order as the beam.
    names = {'kext': ('extraction kicker (kext)', .80, 0.4), 'sept_in': ('extraction septum (sept_in)', .62, 2.0),
             'sept_ex': ('injection septum (sept_ex)', .62, 17.0)}
    for i, e in enumerate(reference):
        if e.FamName in names:
            label, y, x_text = names[e.FamName]
            ax.annotate(label, xy=(s_pos[i] + e.Length / 2, .30), xytext=(x_text, y), fontsize=7,
                        ha='left', va='center', arrowprops={'arrowstyle': '->', 'lw': .7, 'color': '0.3'})
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=(1, .5, .5), label='Quadrupoles q11–q33'),
                       Patch(facecolor=(.5, .5, 1), label='Dipole elements (bends b1–b3, kicker, septa)')],
              loc='upper center', bbox_to_anchor=(.5, 1.12), ncol=2, frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(output / 'layout.pdf', metadata={'CreationDate': None})
    plt.close(fig)
    (output / 'at_plot_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print('Exported original/optimized native pyAT optics; validated against exact maps.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    export_figures(args.output_dir)
