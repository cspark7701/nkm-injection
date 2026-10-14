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


def iterated_coordinate_search(evaluate, nominal, bounds, steps, *, max_sweeps=4, seed=42):
    """Repeated strict-improvement coordinate sweeps (round 3, E7).

    Each sweep evaluates +/- one step per knob from the current best and moves on strict improvement; sweeps repeat
    until a full sweep brings no improvement or ``max_sweeps`` is reached (declared evaluation budget). The result
    records which knobs end on a bound, so an optimum truncated by the search range is visible."""
    x=np.asarray(nominal,float).copy();bounds=np.asarray(bounds,float);steps=np.asarray(steps,float)
    n=len(x)
    if bounds.shape!=(n,2) or steps.shape!=(n,) or not np.isfinite([*x,*bounds.ravel(),*steps]).all():
        raise ValueError('Expected finite knobs, bounds and steps of matching length')
    if np.any(bounds[:,0]>=bounds[:,1]) or np.any(steps<=0) or np.any((x<bounds[:,0])|(x>bounds[:,1])):
        raise ValueError('Invalid bounds, steps or initial feasibility')
    evaluations=[]
    def score(knobs):
        value=float(evaluate(knobs))
        if not np.isfinite(value) or not 0<=value<=1:raise ValueError('Capture objective outside [0,1]')
        evaluations.append({'knobs':knobs.tolist(),'capture':value});return value
    best=score(x);sweeps=0
    for sweeps in range(1,max_sweeps+1):
        improved=False
        for j in range(n):
            for direction in (-1,1):
                trial=x.copy();trial[j]=np.clip(x[j]+direction*steps[j],*bounds[j])
                if trial[j]==x[j]:continue
                value=score(trial)
                if value>best:x,best,improved=trial,value,True
        if not improved:break
    at_bound=[bool(np.isclose(x[j],bounds[j,0]) or np.isclose(x[j],bounds[j,1])) for j in range(n)]
    return {'knobs':x.tolist(),'training_capture':best,'bounds':bounds.tolist(),'steps':steps.tolist(),'seed':seed,
            'sweeps':sweeps,'termination':'no improvement in a full sweep' if not improved else 'sweep budget reached',
            'evaluations':evaluations,'at_bound':at_bound,'feasible':bool(np.all((x>=bounds[:,0])&(x<=bounds[:,1])))}
