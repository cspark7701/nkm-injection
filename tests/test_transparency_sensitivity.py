import numpy as np
import pytest
from nkm_injection.wire_field import FilamentGeometry
from nkm_injection.sliced_vector_map import integrated_filament_kicks


def test_series_current_preserves_axis_cancellation_but_one_loop_does_not():
    g=FilamentGeometry()
    series=integrated_filament_kicks(0.,0.,g,loop_current_relative=np.full(4,.001))
    independent=integrated_filament_kicks(0.,0.,g,loop_current_relative=[.001,0,0,0])
    assert np.max(np.abs(series))<1e-16
    assert np.min(np.abs(independent))>1e-7


def test_wire_displacement_has_linear_dipole_limit():
    g=FilamentGeometry();values=[]
    for amount in (1e-8,2e-8):
        offsets=np.zeros((8,2));offsets[0,0]=amount
        values.append(np.asarray(integrated_filament_kicks(0.,0.,g,wire_offsets_m=offsets)))
    # A horizontal shift of this wire gives a vertical dipole at first order;
    # its horizontal component starts at second order by symmetry.
    assert np.isclose(values[1][1],2*values[0][1],rtol=1e-5)
    assert np.isclose(values[1][0],4*values[0][0],rtol=1e-3,atol=1e-17)
    with pytest.raises(ValueError):integrated_filament_kicks(0.,0.,g,wire_offsets_m=np.zeros((4,2)))
