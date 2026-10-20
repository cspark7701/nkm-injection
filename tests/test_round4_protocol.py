"""Round-4 protocol (F1): error-class ablation keeps every other draw identical. Units as in ErrorBudgetConfig."""
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble

ROOT = Path(__file__).resolve().parents[1]
from scripts import run_round4_campaign as r4

SAMPLE_KEYS = {  # sampled field -> configuration standard deviation
    'quad_k_err': 'quad_k_rel_std', 'dipole_b_err': 'dipole_b_rel_std', 'quad_dx_m': 'quad_dx_std_m',
    'quad_dy_m': 'quad_dy_std_m', 'quad_roll_rad': 'quad_roll_std_rad', 'energy_dp_p': 'energy_dp_p_std',
    'beta_mismatch_x': 'beta_mismatch_rel_std', 'beta_mismatch_y': 'beta_mismatch_rel_std',
    'nkm_scale_err': 'nkm_scale_std', 'nkm_dx_m': 'nkm_dx_std_m', 'nkm_timing_mrad': 'nkm_timing_std_mrad',
    'ring_co_x_m': 'ring_co_x_std_m', 'septum_x_m': 'septum_x_std_m', 'septum_strength_rel': 'septum_strength_rel_std',
    'rf_phase_rad': 'rf_phase_std_rad', 'arrival_time_s': 'arrival_time_std_s'}


@pytest.fixture
def round4_case(tmp_path, monkeypatch):
    """Synthetic inputs for the real campaign/manifest readers, independent of ignored results."""
    from nkm_injection.injection_study import InjectedBeamConfig, InjectionStudyConfig
    from scripts import make_round4_manifest as m4

    def write(relative, value):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return path

    # Representative current-point geometry [m, rad]; beam units follow InjectionStudyConfig.
    current = InjectionStudyConfig(
        field_scale=.95, injection_x_m=-.0194781, injection_xp_rad=.0053194320337647,
        injected_beam=InjectedBeamConfig(emit_x_m_rad=7.67e-9, emit_y_m_rad=.767e-9,
                                       energy_spread=.00106))
    write(r4.PROTOCOL['adopted_model']['study_config_current'], current.to_dict())
    historical = replace(current, field_scale=.85, injection_x_m=-.0195)
    write('results/journal_campaign_04/e6_operating_point/operating_point_round2.json', historical.to_dict())
    # Exercise every class, including timing/septum terms that default to zero.
    full = ErrorBudgetConfig(septum_strength_rel_std=.001, rf_phase_std_rad=.001,
                             arrival_time_std_s=2e-9).to_dict()
    zero = {**full, 'booster_x_jitter_std_m': 0., 'booster_xp_jitter_std_rad': 0.}
    write(r4.PROTOCOL['budgets']['zero_jitter'], zero)
    write('results/journal_campaign_03/error_budget.json', full)
    artifacts = {'round3_operating_point': r4.PROTOCOL['adopted_model']['study_config_current']}
    for key in m4.OVERRIDES:
        relative = f'results/historical/{key}.json'
        write(relative, {'study_config': historical.to_dict()})
        artifacts[key] = relative
    artifacts['round2_pulse'] = 'results/journal_campaign_03/d12_final_pulse.json'
    write(artifacts['round2_pulse'], {'study_config': historical.to_dict()})
    for key, relative in m4.ROUND4.items():
        write(relative, r4.PROTOCOL if key == 'round4_protocol' else {})
    for key, relative in m4.OVERRIDES.items():
        value = {'study_config': current.to_dict()}
        if key == 'round2_pulse':
            width = .44342419894787183e-3  # rad; synthetic pulse metadata
            value.update(window_width_rad=width, residual_kick_allowance_rad=.1*width)
        write(relative, value)
    base = write('docs/paper/revision_manifest_round3.json', {
        'artifacts': artifacts, 'sha256': {k: m4.sha256(tmp_path/v) for k, v in artifacts.items()}})
    monkeypatch.setattr(r4, 'ROOT', tmp_path)
    monkeypatch.setattr(r4, 'CAMPAIGN', tmp_path/r4.PROTOCOL['campaign'])
    monkeypatch.setattr(m4, 'REPO', tmp_path)
    monkeypatch.setattr(m4, 'ROUND3', base)
    return tmp_path, current


@pytest.fixture
def round4_manifest(round4_case):
    from scripts import make_round4_manifest as m4
    root, _ = round4_case
    path = root/'docs/paper/revision_manifest_round4.json'
    m4.main(['--require-all', '--output', str(path)])
    return json.loads(path.read_text())


def _draws(cfg):
    return sample_error_ensemble(ErrorBudgetConfig.from_dict(cfg), 5, 42)


def test_classes_cover_every_applied_error_term(round4_case):
    zero, _ = r4.budgets()
    classes = r4.PROTOCOL['error_classes']
    grouped = {k for c, keys in classes.items() if c not in ('not_applied', 'disabling_rule') for k in keys}
    applied = {k for k, v in zero.items() if v and k not in classes['not_applied']}
    assert applied <= grouped
    assert not set(classes['not_applied']) & grouped


def test_disabling_a_class_leaves_other_draws_unchanged(round4_case):
    zero, _ = r4.budgets()
    full = _draws(zero)
    configs, classes = r4.ablation_configs()
    for c in classes:
        disabled = set(r4.PROTOCOL['error_classes'][c])
        omitted = _draws(configs[f'omit_{c}'])
        for a, b in zip(full, omitted):
            for key, std in SAMPLE_KEYS.items():
                if std in disabled:
                    assert np.all(np.asarray(b[key]) == 0.0), (c, key)
                else:
                    assert np.array_equal(np.asarray(a[key]), np.asarray(b[key])), (c, key)


def test_all_off_and_alone_configurations(round4_case):
    configs, classes = r4.ablation_configs()
    zero, _ = r4.budgets()
    assert len(configs) == 1 + 2 * len(classes) == 15
    applied = [k for c in classes for k in r4.PROTOCOL['error_classes'][c]]
    assert all(configs['all_off'][k] == 0.0 for k in applied)
    for c in classes:
        on = set(r4.PROTOCOL['error_classes'][c])
        assert all(configs[f'alone_{c}'][k] == (zero[k] if k in on else 0.0) for k in applied)
    assert zero['booster_x_jitter_std_m'] == zero['booster_xp_jitter_std_rad'] == 0.0


def test_point_candidates_recorded():
    """Optional integration check of the archived F1 candidates; unit tests use temporary inputs."""
    path = ROOT / r4.PROTOCOL['campaign'] / 'points/points.json'
    if not path.exists():
        pytest.skip('Archived F1 point candidates are not part of a clean checkout')
    pts = json.loads(path.read_text())['points']
    assert pts['extremum']['centroid_at_nkm_m'] == pytest_approx(-0.0085, 1e-6)
    assert all(p['septum_clearance_ok'] and p['root_reproduced'] for p in pts.values())


def pytest_approx(value, tol):
    import pytest
    return pytest.approx(value, abs=tol)


def test_post_kick_amplitude_is_matched_for_an_error_free_shot(round4_case):
    """F4 predictor: with every error zero, the NKM centroid leaves the magnet with zero angle (matched root)."""
    from scripts import analyze_round4_associations as f4
    from nkm_injection.wire_field import calibrate_controls
    _, cfg = round4_case
    job = {'config': cfg.to_dict(), 'sample': {key: 0. for key in SAMPLE_KEYS},
           'calibration_3d': calibrate_controls(cfg), 'rf_frequency_hz': 500e6,
           'pulse_duration_us': 5.3}
    realization = {'bts_exit': {'centroid_x_m': 0.0, 'centroid_xp_rad': 0.0, 'delta_mean': 0.0}, 'ring_error_seed': 5501}
    out = f4.post_kick_amplitudes(job, realization, {5501: (16.27, -0.145)})
    assert abs(out['fieldmap_3d']['xp_rad']) < 1e-9
    assert abs(out['dipole']['xp_rad']) < 1e-6


def test_holm_adjustment_is_monotone_and_bounded():
    from scripts import analyze_round4_associations as f4
    adj = f4.holm([0.01, 0.04, 0.03, 0.5])
    assert np.allclose(adj, [0.04, 0.09, 0.09, 0.5])


def test_dispersion_budget_and_production_accuracy(round4_case):
    """F6: septum dispersion terms and sliced-map accuracy on the production trajectory (current point)."""
    from scripts import analyze_round4_dispersion_scope as f6
    from nkm_injection.injection_study import InjectionStudyConfig
    root, _ = round4_case
    cfg = InjectionStudyConfig.load(root / r4.PROTOCOL['adopted_model']['study_config_current'])
    b = f6.dispersion_budget(cfg)
    assert abs(b['dispersive_divergence_rad'] - 0.047472 * 0.00106) < 1e-12
    assert abs(b['shot_angle_rad'] - 4.7472e-5) < 1e-12
    acc = f6.accuracy(cfg)
    assert abs(acc['sliced_minus_3d'][1]) < 1e-6 < abs(acc['thin_minus_3d'][1])


def test_classifying_kicker_matches_production_kicker(round4_case):
    """F5: the loss-classifying copy of FilamentNKMKicker.apply is physically identical to the production one."""
    from scripts import run_round4_loss_locations as f5
    from nkm_injection.injection_study import InjectionStudyConfig
    from nkm_injection.wire_field import FilamentNKMKicker
    root, _ = round4_case
    cfg = InjectionStudyConfig.load(root / r4.PROTOCOL['adopted_model']['study_config_current'])
    rng = np.random.default_rng(3)
    beam = np.zeros((6, 64))
    beam[0] = cfg.injection_x_m + 2.2625 * cfg.injection_xp_rad + rng.normal(0, 3e-3, 64)
    beam[1] = cfg.injection_xp_rad + rng.normal(0, 3e-4, 64)
    beam[2] = rng.normal(0, 2.5e-3, 64)
    kw = {'chamber_half_x_m': 0.016, 'chamber_half_y_m': 0.0038}
    a, b = beam.copy(), beam.copy()
    lost_a = FilamentNKMKicker(cfg, n_slices=160, **kw).apply(a, 0.0)
    f5.RECORDS.clear()
    lost_b = f5.ClassifyingKicker(cfg, n_slices=160, **kw).apply(b, 0.0)
    assert np.array_equal(lost_a, lost_b) and lost_a.any()
    np.testing.assert_array_equal(np.nan_to_num(a, nan=9.0), np.nan_to_num(b, nan=9.0))
    assert sum(f5.RECORDS[-1]['magnet_reasons'].values()) == int(lost_a.sum())


def test_ablation_estimands_and_pairing_guard():
    """F2: alone/omitted effects and non-additivity on synthetic paired ensembles; unpaired ensembles are rejected."""
    import pytest
    from scripts import analyze_round4_ablation as f2

    def ens(nkm, dip, seeds=(1, 2, 3)):
        return {i: {'beam_seed': s, 'ring_error_seed': 5501, 'models': {'fieldmap_3d': {'capture_fraction': nkm},
                                                                         'dipole': {'capture_fraction': dip}}}
                for i, s in enumerate(seeds)}
    cls = f2.classes()
    ensembles = {'all_off': ens(.8, .85), 'full': ens(.4, .7)}
    for c in cls:
        ensembles[f'alone_{c}'] = ens(.4 if c == 'bts_magnets' else .8, .7 if c == 'bts_magnets' else .85)
        ensembles[f'omit_{c}'] = ens(.8 if c == 'bts_magnets' else .4, .85 if c == 'bts_magnets' else .7)
    out = f2.analyse(ensembles)
    assert out['alone_effect']['bts_magnets']['fieldmap_3d']['mean'] == pytest.approx(-.4)
    assert out['omitted_effect']['bts_magnets']['gap']['mean'] == pytest.approx(-.25)
    assert out['omitted_effect']['septum']['dipole']['mean'] == pytest.approx(0.0)
    assert out['non_additivity']['fieldmap_3d']['difference']['mean'] == pytest.approx(0.0)
    ensembles['omit_septum'] = ens(.4, .7, seeds=(1, 2, 4))
    with pytest.raises(ValueError):
        f2.analyse(ensembles)


def test_point_decision_rule():
    """F3: a candidate replaces the current point only with a significant full-budget NKM gain and no zero-jitter loss
    beyond the declared 1-point margin."""
    from scripts import analyze_round4_points as f3
    ci = lambda lo, hi: {'ci95': [lo, hi]}
    assert f3.meets_rule(ci(0.01, 0.1), ci(-0.005, 0.02))
    assert not f3.meets_rule(ci(-0.01, 0.1), ci(0.0, 0.02))
    assert not f3.meets_rule(ci(0.01, 0.1), ci(-0.02, 0.02))


def test_round4_manifest_points_pulse_and_transparency_at_current_point(round4_case, round4_manifest):
    """F7: the pulse and transparency keys resolve to S = 0.95 current-point artifacts; S = 0.85 kept as history."""
    root, _ = round4_case
    from scripts import make_round4_manifest as m4
    art = round4_manifest['artifacts']
    installed = json.loads((ROOT/'docs/paper/revision_manifest_round4.json').read_text())['artifacts']
    for key in m4.OVERRIDES:
        assert installed[key] == art[key] == m4.OVERRIDES[key]
        data = json.loads((root / art[key]).read_text())
        assert data['study_config']['field_scale'] == 0.95, key
    pulse = json.loads((root / art['round2_pulse']).read_text())
    assert abs(pulse['window_width_rad'] - 0.44342419894787183e-3) < 1e-15
    assert abs(pulse['residual_kick_allowance_rad'] - 0.1 * pulse['window_width_rad']) < 1e-15
    assert art['historical_round2_pulse'] == 'results/journal_campaign_03/d12_final_pulse.json'


def test_round4_reporting_formats():
    """F8: TeX upper-bound formatting and interval strings of the round-4 report macros."""
    from scripts import round4_reporting as r4r
    assert r4r._sci(8.3e-8) == '$9\\times10^{-8}$'
    assert r4r._sci(9.6e-8) == '$1\\times10^{-7}$'
    assert r4r._interval({'mean': -0.172, 'ci95': [-0.254, -0.092]}) == '-17.2 [-25.4, -9.2]'


@pytest.mark.parametrize('mismatch', ['field_scale', 'injection_x_m'])
def test_round4_manifest_point_identity_check(round4_case, round4_manifest, mismatch):
    """F9: the point-identity check accepts the selected point and rejects a historical (S = 0.85) artifact."""
    import pytest
    from scripts import make_round4_manifest as m4
    root, _ = round4_case
    art = round4_manifest['artifacts']
    assert set(m4.point_identity(art)) == set(m4.OVERRIDES)
    with pytest.raises(SystemExit, match='point identity: round2_pulse'):
        m4.point_identity({**art, 'round2_pulse': art['historical_round2_pulse']})
    pulse_path = root / art['round2_pulse']
    pulse = json.loads(pulse_path.read_text())
    pulse['study_config'][mismatch] += .01
    pulse_path.write_text(json.dumps(pulse))
    with pytest.raises(SystemExit, match=mismatch):
        m4.point_identity(art)
