"""Keep the original BTS reference distinct from the matched campaign baseline."""
import json
from pathlib import Path

import numpy as np

from nkm_injection.bts_lattice import BTSConfig
from scripts.export_bts_round3_assets import nominal_original_comparison

ROOT = Path(__file__).resolve().parents[1]


def test_original_figure_reference_is_not_the_matched_campaign_baseline():
    source = ROOT / 'docs/paper_bts/generated/round3_apertures.json'
    saved = json.loads(source.read_text())
    before = json.dumps(saved, sort_keys=True)
    comparison, diagnostics = nominal_original_comparison(saved)
    original = BTSConfig().quad_strengths_list
    np.testing.assert_array_equal(comparison['designs']['reference']['strengths_m_minus2'], original)
    assert not np.allclose(original, saved['designs']['reference']['strengths_m_minus2'])
    assert json.dumps(saved, sort_keys=True) == before
    # Original matching fails and the five-sigma envelope overlaps the blade;
    # the optimized setting meets the same target and restores nominal clearance.
    assert not diagnostics['reference']['satisfies_exit_match']
    assert diagnostics['reference']['minimum_clearance_m'] < 0
    assert diagnostics['low_beta']['satisfies_exit_match']
    assert diagnostics['low_beta']['minimum_clearance_m'] > 0
    assert diagnostics['low_beta']['max_family_clearance_difference_m'] < 1e-10
