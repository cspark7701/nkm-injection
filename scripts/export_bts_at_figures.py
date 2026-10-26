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

from nkm_injection.bts_journal import lattice_for
from nkm_injection.bts_round2 import spatial_profile
from nkm_injection.optics import DEFAULT_BTS_ENTRANCE_TWISS

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'docs/paper_bts'
PROFILE = ROOT / 'results/bts_journal_campaign_r2_20261013/spatial/spatial_profiles.json'


def transfer_line_call(function, *args, **kwargs):
    # pyAT also evaluates periodic stability/chromaticity for plot_linear.
    # This open line has explicit entrance optics, not a periodic solution.
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='Unstable ring', category=at.AtWarning)
        warnings.filterwarnings('ignore', message='FigureCanvasAgg is non-interactive.*',
                                category=UserWarning)
        return function(*args, **kwargs)


def export_figures(output):
    """Validate and draw the frozen designs on their 64-subdivision mesh."""
    designs = json.loads((PAPER / 'generated/round2_designs.json').read_text())
    if PROFILE.is_file():
        profiles = json.loads(PROFILE.read_text())
        profile_sources = [PROFILE]
        profile_origin = 'Archived full independent-map profiles'
    else:
        # Frozen strengths and peak summaries are tracked; regenerate only the
        # deterministic observation profiles when ignored campaign rows are absent.
        summary = PAPER / 'generated/round2_spatial.json'
        saved = json.loads(summary.read_text())
        profiles = {'original': [], 'refined': []}
        for name in ('reference', 'low_beta'):
            k = designs['designs']['baseline']['nominal'][name]['strengths_m_minus2']
            profile = spatial_profile(lattice_for(k), 64)
            expected = (saved['original_profiles'][0]['64'] if name == 'reference'
                        else saved['refined_low_beta']['profiles'][-1])
            np.testing.assert_allclose(profile['peak_beta_m'], expected['peak_beta_m'], rtol=0, atol=1e-8)
            if name == 'reference':
                profiles['original'].append([profile])
            else:
                profiles['refined'].append(profile)
        profile_sources = [summary, ROOT / 'src/nkm_injection/bts_round2.py',
                           ROOT / 'src/nkm_injection/bts_journal.py']
        profile_origin = 'Re-evaluated exact maps of frozen strengths; peaks checked against tracked summaries'
    tw = DEFAULT_BTS_ENTRANCE_TWISS
    twiss = dict(beta=[tw.beta_x, tw.beta_y], alpha=[tw.alpha_x, tw.alpha_y],
                 dispersion=[tw.disp_x, tw.disp_px, tw.disp_y, tw.disp_py])
    plt.rcParams.update({'font.size': 9, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 1, figsize=(6.3, 4.2), sharex=True)
    report = {'pyat_version': at.__version__, 'subdivisions': 64,
              'beta_absolute_tolerance_m': 1e-4, 'designs': {}, 'profile_origin': profile_origin,
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in profile_sources + [PAPER / 'generated/round2_designs.json', Path(__file__) ]}}
    for name, label, profile in [('reference', 'Reference', profiles['original'][0][-1]),
                                  ('low_beta', 'Refined low beta', profiles['refined'][-1])]:
        lattice = lattice_for(designs['designs']['baseline']['nominal'][name]['strengths_m_minus2'])
        dense = lattice.slice_elements([i for i, e in enumerate(lattice) if e.Length], slices=64)
        _, _, optics = transfer_line_call(at.get_optics, dense, refpts=range(1, len(dense)+1),
                                    twiss_in=twiss, method=at.linopt2)
        expected = np.array([[r['s_m'], *r['beta_m']] for r in profile['rows']])
        np.testing.assert_allclose(optics.s_pos, expected[:, 0], rtol=0, atol=1e-10)
        np.testing.assert_allclose(optics.beta, expected[:, 1:], rtol=0, atol=1e-4)
        report['designs'][name] = {'max_beta_difference_m': float(np.max(abs(optics.beta-expected[:, 1:]))),
                                  'peak_beta_m': optics.beta.max(axis=0).tolist()}
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

    reference = lattice_for(designs['designs']['baseline']['nominal']['reference']['strengths_m_minus2'])
    fig, ax = plt.subplots(figsize=(7, 1.9))
    syn = at.plot.plot_synopt(reference, axes=ax)
    if isinstance(syn, tuple):  # pyAT 0.8 returns (synoptic_axes, parent_axes).
        syn = syn[0]
    syn.set_ylim(0, 2.5)
    ax.set_facecolor('none')
    ax.set(xlim=(0, reference.get_s_pos(len(reference))[0]), ylim=(0, 1),
           xlabel='Path coordinate [m]', yticks=[])
    ax.spines[['left', 'right', 'top']].set_visible(False)
    for i, e in enumerate(reference):
        if hasattr(e, 'Limits'):
            ax.axvline(reference.get_s_pos(i)[0], color='0.4', linestyle=':', linewidth=1)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=(1, .5, .5), label='Quadrupoles'),
                       Patch(facecolor=(.5, .5, 1), label='Dipoles')],
              loc='upper center', ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(output / 'layout.pdf', metadata={'CreationDate': None})
    plt.close(fig)
    (output / 'at_plot_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print('Exported native pyAT optics and synoptic; validated against frozen exact-map profiles.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    export_figures(args.output_dir)
