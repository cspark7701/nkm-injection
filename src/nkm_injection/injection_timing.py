"""Separate septum bend, RF phase and arrival time errors in canonical units."""
import numpy as np

C_M_S = 299792458.0


def apply_injection_shot_errors(beam, sample, *, septum_angle_rad=.01, rf_frequency_hz=499593472.8240743,
                                pulse_duration_s=5.3e-6):
    """Mutate (6,N) beam at septum exit; return NKM field-scale multiplier.

    Septum-strength jitter adds canonical p_x = (1+delta)*angle*relative error.
    RF phase gives ct=c*phase/(2*pi*f). The independent arrival time is relative
    to the NKM firing time, not an additional offset from the RF bucket.
    It samples a half-sine NKM pulse at its peak;
    zero is returned outside the finite pulse. Phase is defined in the AT ct sign.
    """
    if beam.ndim != 2 or beam.shape[0] != 6:
        raise ValueError('Expected (6,N) beam')
    vals=[septum_angle_rad, rf_frequency_hz, pulse_duration_s,
          sample.get('septum_strength_rel',0.),sample.get('rf_phase_rad',0.),sample.get('arrival_time_s',0.)]
    if not np.isfinite(vals).all() or rf_frequency_hz <= 0 or pulse_duration_s <= 0:
        raise ValueError('Invalid shot errors or timing parameters')
    dt=sample.get('arrival_time_s',0.)
    beam[1] += (1+beam[4])*septum_angle_rad*sample.get('septum_strength_rel',0.)
    beam[5] += C_M_S*sample.get('rf_phase_rad',0.)/(2*np.pi*rf_frequency_hz)
    return float(np.cos(np.pi*dt/pulse_duration_s)) if abs(dt) <= pulse_duration_s/2 else 0.
