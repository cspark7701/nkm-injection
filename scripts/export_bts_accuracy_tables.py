#!/usr/bin/env python3
"""Export BTS accuracy tables from tracked validation summaries; no tracking run.

Lengths in the input summaries are in m. Clearance errors are displayed in um;
beta peaks and changes remain in m. The output directory must be new.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'docs/paper_bts'
INPUTS = ['generated/transport_validation.json', 'generated/round2_accuracy.json',
          'generated/round2_spatial.json']


def export(output):
    output.mkdir(parents=True, exist_ok=False)
    transport, accuracy, spatial = [json.loads((PAPER / name).read_text()) for name in INPUTS]
    for result, limit in [('nominal_map_difference', 'nominal_map_abs'),
                          ('transverse_symplectic_error', 'symplectic_max_abs')]:
        value = transport[result]
        tolerance = transport['tolerances'][limit]
        if not np.isfinite(value) or not 0 <= value < tolerance:
            raise ValueError('Archived validation result fails its tolerance: ' + result)
    checks = [('Nominal map-entry discrepancy', transport['nominal_map_difference'], None,
               transport['tolerances']['nominal_map_abs']),
              ('Transverse symplectic discrepancy', transport['transverse_symplectic_error'], None,
               transport['tolerances']['symplectic_max_abs']),
              ('Probe-step clearance change', 1e6 * accuracy['max_step_clearance_change_m'], r'\micro\metre', None),
              ('40/80-step clearance change', 1e6 * accuracy['max_40_to_80_clearance_change_m'], r'\micro\metre', None),
              ('Centered-map/nonlinear clearance difference', 1e6 * accuracy['max_quadrature_clearance_error_m'], r'\micro\metre', None),
              ('Order-5/7 quadrature clearance change', 1e6 * accuracy['max_quadrature_5_to_7_bound_m'], r'\micro\metre', None)]
    text = '% Exported by scripts/export_bts_accuracy_tables.py from tracked summaries.\n'
    text += r'\begin{tabular}{@{}p{.45\linewidth}rr@{}}\toprule' + '\n'
    text += r'Check & Discrepancy & Tolerance / scope\\\midrule' + '\n'
    for label, value, unit, tolerance in checks:
        if not np.isfinite(value) or value < 0:
            raise ValueError('Invalid accuracy discrepancy')
        quantity = (r'\num{' if unit is None else r'\SI{') + f'{value:.3g}' + '}'
        if unit is not None:
            quantity += '{' + unit + '}'
        criterion = r'\num{' + f'{tolerance:.3g}' + '}' if tolerance is not None else 'Finite-case diagnostic'
        text += f'{label} & {quantity} & {criterion}' + r'\\' + '\n'
    text += r'\bottomrule\end{tabular}' + '\n'
    (output / 'accuracy_checks.tex').write_text(text)
    profiles = spatial['refined_low_beta']['profiles']
    text = '% Exported by scripts/export_bts_accuracy_tables.py from tracked summaries.\n'
    text += r'\begin{tabular}{rrrr}\toprule' + '\n'
    text += r'Subdivisions & Peak $\beta_x$ [\si{\metre}] & Peak $\beta_y$ [\si{\metre}] & Max. change [\si{\metre}]\\\midrule' + '\n'
    previous = None
    rows = []
    for profile in profiles:
        peaks = np.asarray(profile['peak_beta_m'], dtype=float)
        if peaks.shape != (2,) or not np.isfinite(peaks).all() or np.any(peaks <= 0):
            raise ValueError('Two finite positive beta peaks required')
        change = None if previous is None else float(np.max(np.abs(peaks - previous)))
        display_change = '---' if change is None else r'\num{' + f'{change:.3g}' + '}'
        text += f"{profile['subdivisions']} & {peaks[0]:.6f} & {peaks[1]:.6f} & {display_change}" + r'\\' + '\n'
        rows.append({'subdivisions': profile['subdivisions'], 'peak_beta_m': peaks.tolist(), 'max_change_m': change})
        previous = peaks
    text += r'\bottomrule\end{tabular}' + '\n'
    (output / 'spatial_resolution.tex').write_text(text)
    provenance = {'scope': 'Reformatted archived validation results; no new physics computation.',
                  'input_sha256': {name: hashlib.sha256((PAPER / name).read_bytes()).hexdigest() for name in INPUTS},
                  'exporter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'spatial_rows': rows,
                  'output_sha256': {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                                    for name in ('accuracy_checks.tex', 'spatial_resolution.tex')}}
    (output / 'accuracy_table_provenance.json').write_text(json.dumps(provenance, indent=2, allow_nan=False) + '\n')
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    export(parser.parse_args().output_dir)
