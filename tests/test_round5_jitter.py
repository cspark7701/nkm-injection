"""Round-5 scan: preserve non-jitter draws and distinguish the two paired estimands."""
from copy import deepcopy
import numpy as np
import pytest
from scripts.analyze_round5_jitter import validate_jobs, summarize


def job():
    scientific = ('config bts_config initial_twiss target_twiss models backend thick_slices particles turns '
                  'correct_static_orbit slices_3d timing_model calibration_3d septum_angle_mrad rf_frequency_hz '
                  'pulse_duration_us chamber static_steering_planes extra beam_seed ring_error_seed corrected_ring_path').split()
    out = {k: None for k in scientific}
    out.update(sample={'sample_id': 0, 'booster_x_m': .0004, 'booster_xp_rad': -.0001,
                       'quad_dx_m': [.0001] * 9}, beam_seed=42, ring_error_seed=5501)
    return out


def test_scan_accepts_only_scaled_jitter_and_preserved_pairing():
    ref = job(); scaled = deepcopy(ref)
    for k in ('booster_x_m', 'booster_xp_rad'):
        scaled['sample'][k] *= .25
    assert validate_jobs([ref], [scaled], .25) == [0]
    for k in ('beam_seed', 'ring_error_seed', 'static_steering_planes', 'config'):
        altered = deepcopy(scaled); altered[k] = 'changed'
        with pytest.raises(ValueError, match='Changed paired'):
            validate_jobs([ref], [altered], .25)
    altered = deepcopy(scaled); altered['sample']['quad_dx_m'][0] += 1e-6
    with pytest.raises(ValueError, match='Non-jitter'):
        validate_jobs([ref], [altered], .25)
    with pytest.raises(ValueError, match='Unpaired'):
        validate_jobs([ref], [scaled, scaled], .25)


def test_noninferiority_is_jitter_cost_not_model_gap():
    zero = {'fieldmap_3d': np.array([.70, .80, .75]), 'dipole': np.array([.85, .95, .90])}
    small = {m: v - .002 for m, v in zero.items()}
    result = summarize(small, zero)
    assert result['nkm_noninferior_to_zero_jitter']
    assert result['gap']['mean'] == pytest.approx(-.15)
    assert result['gap_change']['mean'] == pytest.approx(0)
    large = {m: v - .02 for m, v in zero.items()}
    assert not summarize(large, zero)['nkm_noninferior_to_zero_jitter']


def test_reporting_keeps_jitter_cost_separate_from_gap(tmp_path):
    from scripts import round5_reporting
    zero = {'fieldmap_3d': np.array([.70, .80, .75]), 'dipole': np.array([.85, .95, .90])}
    reduced = {m: v - .002 for m, v in zero.items()}
    class Builder:
        out = tmp_path
        values = {}
        def has(self, key):return key == 'round5_jitter'
        def load(self, key):return {'rows':[{'scale':0., **summarize(zero,zero)},
                                           {'scale':.25, **summarize(reduced,zero)}],
                                   'largest_passing_nonzero_tested_scale':.25}
        def macro(self, name, value, fmt=None):self.values[name] = fmt.format(value) if fmt else value
        def save(self, fig, name, keys, caption):
            import matplotlib.pyplot as plt
            self.provenance_keys = keys
            fig.savefig(self.out/('figures/'+name+'.pdf'));plt.close(fig)
    (tmp_path/'figures').mkdir()
    b=Builder();round5_reporting.macros(b)
    assert b.provenance_keys == ['round5_jitter']
    assert b.values['RFiveQuarterGap'] == '-15.0'
    assert b.values['RFiveQuarterCost'] == '-0.2'
    assert 'pass' in b.values['RFiveJitterRows']
    assert b.values['RFivePassingScale'] == '0.25'
    assert (tmp_path/'figures/fig12_two_plane_jitter.pdf').stat().st_size > 1000


def test_exact_loss_margin_is_not_mistaken_for_noninferiority():
    # 30 to 28 survivors out of 200 is exactly the one-point loss boundary.
    baseline = {'fieldmap_3d':np.full(3,30/200), 'dipole':np.full(3,60/200)}
    boundary = {'fieldmap_3d':np.full(3,28/200), 'dipole':np.full(3,58/200)}
    assert not summarize(boundary, baseline)['nkm_noninferior_to_zero_jitter']
