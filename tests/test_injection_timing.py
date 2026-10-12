import numpy as np
import pytest
from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble
from nkm_injection.injection_timing import apply_injection_shot_errors, C_M_S


def test_separate_shot_terms_have_expected_units_and_momentum_scaling():
    beam=np.zeros((6,2));beam[4]=[0.,.002]
    sample={'septum_strength_rel':.001,'rf_phase_rad':.01,'arrival_time_s':2e-9}
    scale=apply_injection_shot_errors(beam,sample,rf_frequency_hz=5e8,pulse_duration_s=5.3e-6)
    assert np.allclose(beam[1],[1e-5,1.002e-5])
    assert np.allclose(beam[5],C_M_S*.01/(2*np.pi*5e8))
    assert scale==pytest.approx(np.cos(np.pi*2e-9/5.3e-6))


def test_zero_and_outside_pulse_limits():
    beam=np.zeros((6,1));assert apply_injection_shot_errors(beam,{})==1.
    assert np.array_equal(beam,np.zeros((6,1)))
    assert apply_injection_shot_errors(beam,{'arrival_time_s':3e-6})==0.
    assert np.array_equal(beam,np.zeros((6,1)))  # pulser-relative timing does not move the RF phase


def test_new_stream_does_not_change_existing_samples():
    a=sample_error_ensemble(ErrorBudgetConfig(),3,42)
    b=sample_error_ensemble(ErrorBudgetConfig(septum_strength_rel_std=.001,rf_phase_std_rad=.01,
                                          arrival_time_std_s=2e-9),3,42)
    new={'septum_strength_rel','rf_phase_rad','arrival_time_s'}
    assert [{k:v for k,v in row.items() if k not in new} for row in a]==[{k:v for k,v in row.items() if k not in new} for row in b]
    assert b==sample_error_ensemble(ErrorBudgetConfig(septum_strength_rel_std=.001,rf_phase_std_rad=.01,
                                                    arrival_time_std_s=2e-9),3,42)


def test_nonfinite_budget_rejected():
    with pytest.raises(ValueError):ErrorBudgetConfig(arrival_time_std_s=np.nan).validate()
