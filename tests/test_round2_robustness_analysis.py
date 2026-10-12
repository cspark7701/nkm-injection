"""Pairing must preserve actual machine/shot draws, not merely their seed labels."""
import copy
import importlib
from pathlib import Path

import pytest


@pytest.fixture
def analysis(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    return importlib.import_module('analyze_round2_robustness')


def jobs():
    return {'jobs': [{'work_dir': '/first', 'particles': 200, 'beam_seed': 4,
                      'ring_error_seed': 5501, 'extra': {'emit_rel': .1},
                      'sample': {'sample_id': 0, 'booster_x_m': 0.,
                                 'booster_xp_rad': 0., 'quad_k_err': [.01, .02]}}]}


def test_jitter_and_output_directory_can_change(analysis):
    before=jobs();after=copy.deepcopy(before)
    after['jobs'][0]['work_dir']='/second'
    after['jobs'][0]['sample']['booster_x_m']=.0005
    after['jobs'][0]['sample']['booster_xp_rad']=.0002
    analysis.verify_paired_jobs(before,after)


@pytest.mark.parametrize('change',['static_error','extra_shot','ring','particles'])
def test_actual_pairing_rejects_non_jitter_changes(analysis,change):
    before=jobs();after=copy.deepcopy(before);job=after['jobs'][0]
    if change=='static_error':job['sample']['quad_k_err'][0]+=.001
    elif change=='extra_shot':job['extra']['emit_rel']+=.01
    elif change=='ring':job['ring_error_seed']=5502
    else:job['particles']=100
    with pytest.raises(ValueError,match='actual non-jitter'):
        analysis.verify_paired_jobs(before,after)
