#!/usr/bin/env python3
"""Reconstruct the round-six BTS reporting checks from frozen simulation outputs.

Losses are fractions unless explicitly labelled percent; D' is dimensionless.
This script performs post-processing only and writes to a new output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / 'results/bts_round5_campaign_20261031'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    sources = {
        'raw_test': CAMPAIGN / 'final_test_b/raw_machines.json',
        'test_summary': CAMPAIGN / 'final_test_b/final_test.json',
        'edge_study': CAMPAIGN / 'edge_study/edge_study.json',
        'protocol': ROOT / 'docs/paper_bts/round5_protocol.json',
        'exported': ROOT / 'docs/paper_bts/generated/round5.json',
    }
    documents = {key: json.loads(path.read_text()) for key, path in sources.items()}
    raw, summary = documents['raw_test'], documents['test_summary']
    protocol = documents['protocol']
    assert len(raw) == protocol['final_test']['machines']
    particles = protocol['final_test']['particles_per_shot']
    counts = {}
    for name in ('reference', 'low_beta', 'edge_best', 'free_best'):
        shots = [shot['results'][name]['full'] for machine in raw for shot in machine['shots']]
        observed = sum(shot['lost'] for shot in shots)
        expected = sum(particles * shot['loss_max'] for shot in shots)
        stored = summary['validation'][name]
        assert observed == stored['observed_count']
        np.testing.assert_allclose(expected, stored['conditional_expected_count'], rtol=1e-13)
        counts[name] = {'observed_count': observed, 'conditional_expected_count': expected}

    edge = counts['edge_best']
    shortfall = 100 * (edge['observed_count'] - edge['conditional_expected_count']) / edge['observed_count']
    exported = documents['exported']['validation_reporting']['edge_prediction_shortfall']
    assert exported['denominator'] == 'observed_count' and exported['unit'] == 'percent'
    np.testing.assert_allclose(shortfall, exported['value'], rtol=1e-13)

    numerator = np.array([m['jitter_integrated_loss']['reference']['full'] for m in raw])
    denominator = np.array([m['jitter_integrated_loss']['edge_best']['full'] for m in raw])
    settings = summary['gain_vs_reference']['edge_best']
    ids = np.random.default_rng(protocol['final_test']['bootstrap_seed']).integers(
        0, len(raw), (settings['resamples'], len(raw)))
    den = denominator[ids].mean(1)
    assert np.all(den > 0)
    ratio = numerator.mean() / denominator.mean()
    interval = np.quantile(numerator[ids].mean(1) / den, [.025, .975])
    np.testing.assert_allclose(ratio, settings['estimate'], rtol=1e-13)
    np.testing.assert_allclose(interval, settings['ci95'], rtol=1e-13)

    starts = [row for row in documents['edge_study']['rows'] if row['D_m'] == .080868 and row['Dp'] == 0]
    matched = [row['start'] for row in starts if row['matched']]
    failed = [row['start'] for row in starts if not row['matched']]
    assert len(matched) == 2 and failed == ['dispersion_free_best']
    assert all(not row['success'] and row['termination'] == 'Iteration limit reached' for row in starts)
    record = {
        'scope': 'Post-processing of stored runs; no tracking or optimization rerun.',
        'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in [*sources.values(), Path(__file__).resolve()]},
        'counts': counts,
        'prediction_shortfall_percent': float(shortfall),
        'discrepancy_denominator': 'observed_count',
        'gain': float(ratio), 'gain_ci95': interval.tolist(),
        'zero_denominator_resamples': int(np.count_nonzero(den == 0)),
        'zero_slope_matched_count': len(matched),
        'zero_slope_matched_starts': matched, 'zero_slope_failed_starts': failed,
        'zero_slope_termination': 'Iteration limit reached for all three starts',
    }
    args.output_dir.mkdir(parents=True, exist_ok=False)
    output = args.output_dir / 'round6_checks.json'
    output.write_text(json.dumps(record, indent=2) + '\n')
    print(output)


if __name__ == '__main__':
    main()
