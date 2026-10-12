import numpy as np
import pytest
from nkm_injection.pulse_requirements import peak_phase_field_fraction,maximum_peak_phase_duration,thin_shell_diffusion_time


def test_peak_and_finite_support_and_return_bound():
    tau=5.3e-6;assert peak_phase_field_fraction(0.,tau)==1.
    assert peak_phase_field_fraction(2.666e-6,tau)==0.
    maximum=maximum_peak_phase_duration(2.666e-6,.19)
    assert peak_phase_field_fraction(2.666e-6,maximum)==pytest.approx(.19)
    assert peak_phase_field_fraction(2.666e-6,8e-6)==pytest.approx(.5,abs=.001)


def test_timing_small_offset_and_shell_scaling():
    loss=1-peak_phase_field_fraction(2e-9,5.3e-6)
    assert loss==pytest.approx(.5*(np.pi*2e-9/5.3e-6)**2,rel=1e-6)
    assert thin_shell_diffusion_time(1e6,.015,2e-6)==2*thin_shell_diffusion_time(1e6,.015,1e-6)


def test_invalid_pulse_arguments_rejected():
    with pytest.raises(ValueError):peak_phase_field_fraction(0.,0.)
    with pytest.raises(ValueError):maximum_peak_phase_duration(1.,1.)
