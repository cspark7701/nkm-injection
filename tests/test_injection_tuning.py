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
