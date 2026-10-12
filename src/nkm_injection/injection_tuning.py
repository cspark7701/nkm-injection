"""Reduced bounded injection-knob search (x in m, angle rad, field scale dimensionless)."""
import numpy as np


def coordinate_sweep(evaluate, nominal, bounds, steps, *, seed=42):
    """One deterministic bounded sweep; evaluate the centre and ±step for each knob.

    Fixed simulation/measurement seeds belong to the caller. Strict improvement
    avoids choosing a larger change on a noisy tie. This is a reduced study, not
    a global optimizer or proof of an operational tuning procedure.
    """
    x=np.asarray(nominal,float).copy();bounds=np.asarray(bounds,float);steps=np.asarray(steps,float)
    if x.shape!=(3,) or bounds.shape!=(3,2) or steps.shape!=(3,) or not np.isfinite([*x,*bounds.ravel(),*steps]).all():
        raise ValueError('Expected three finite knobs, bounds and steps')
    if np.any(bounds[:,0]>=bounds[:,1]) or np.any(steps<=0) or np.any((x<bounds[:,0])|(x>bounds[:,1])):
        raise ValueError('Invalid bounds, steps or initial feasibility')
    evaluations=[]
    def score(knobs):
        value=float(evaluate(knobs))
        if not np.isfinite(value) or not 0<=value<=1:raise ValueError('Capture objective outside [0,1]')
        evaluations.append({'knobs':knobs.tolist(),'capture':value});return value
    best=score(x)
    for j in range(3):
        centre=x.copy();chosen=x.copy();local=best
        for direction in (-1,1):
            trial=centre.copy();trial[j]=np.clip(centre[j]+direction*steps[j],*bounds[j])
            value=score(trial)
            if value>local:chosen=trial;local=value
        x,best=chosen,local
    return {'knobs':x.tolist(),'training_capture':best,'bounds':bounds.tolist(),'steps':steps.tolist(),
            'seed':seed,'termination':'one declared coordinate sweep','evaluations':evaluations,
            'feasible':bool(np.all((x>=bounds[:,0])&(x<=bounds[:,1])))}
