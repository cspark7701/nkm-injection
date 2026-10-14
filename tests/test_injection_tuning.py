import pytest
import numpy as np
from nkm_injection.injection_tuning import coordinate_sweep


def test_sweep_improves_with_bounds_and_reports_termination():
    objective=lambda x:1.-float(np.sum((x-np.array([.5,-.5,.5]))**2)/4.)
    out=coordinate_sweep(objective,[0,0,0],[[-1,1]]*3,[.5]*3)
    assert out['knobs']==[.5,-.5,.5] and out['training_capture']==1.
    assert out['feasible'] and len(out['evaluations'])==7
    assert out==coordinate_sweep(objective,[0,0,0],[[-1,1]]*3,[.5]*3)


def test_ties_preserve_nominal_knobs():
    out=coordinate_sweep(lambda x:.9,[0,0,1],[[-1,1],[-1,1],[.5,1.5]],[.5,.5,.1])
    assert out['knobs']==[0,0,1]


def test_iterated_search_climbs_to_interior_optimum_and_flags_bounds():
    from nkm_injection.injection_tuning import iterated_coordinate_search
    f = lambda k: max(0.0, 1.0 - (k[0] - 0.3) ** 2 - (k[1] + 0.2) ** 2)
    r = iterated_coordinate_search(f, [0.0, 0.0], [[-1, 1], [-1, 1]], [0.1, 0.1], max_sweeps=10)
    assert r['knobs'] == pytest.approx([0.3, -0.2]) and r['termination'] == 'no improvement in a full sweep'
    assert r['at_bound'] == [False, False]
    g = lambda k: min(1.0, 0.5 + 0.1 * k[0])
    r = iterated_coordinate_search(g, [0.0], [[-1, 1]], [0.5], max_sweeps=10)
    assert r['knobs'] == pytest.approx([1.0]) and r['at_bound'] == [True]
