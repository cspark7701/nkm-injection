"""Tolerance studies use only explicit, validated inputs with reconstructible seeds."""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pytest

from scripts import run_publication_tolerances as cli
from nkm_injection.bts_lattice import BTSConfig, create_bts_lattice
from nkm_injection.constraints import BTSConstraintConfig
from nkm_injection.errors import ErrorBudgetConfig, sample_error_ensemble, apply_sample_errors
from nkm_injection.objectives import OpticsTargetConfig
from nkm_injection.optimization_handoff import (
    QUAD_NAMES, HANDOFF_UNITS, load_optimization_handoff,
)
from nkm_injection.robust_optimization import evaluate_robustness_statistics, compute_one_at_a_time_sensitivity


@pytest.fixture
def optimization_runs(tmp_path):
    def build(name, offset=0.):
        folder = tmp_path/'results/bts_publication_optimization'/name
        folder.mkdir(parents=True)
        bts = BTSConfig(energy_eV=5e9, l_dr1=2.1+offset, ap1_limit=.023)
        target = OpticsTargetConfig(init_beta_x=8.2+offset, init_alpha_y=-1.3,
                                   init_disp_x=.2, target_beta_x=2.5+offset)
        constraints = BTSConstraintConfig(energy_eV=5e9, beta_max_limit_m=70., mismatch_limit=1.1)
        strengths = bts.quad_strengths_list; strengths[0] += offset
        config = {'publication_input_schema_version':1, 'units':HANDOFF_UNITS,
                  'quadrupole_names':list(QUAD_NAMES), 'quad_bounds_global':[-3.,3.],
                  'bts_config':bts.to_dict(), 'target_config':target.to_dict(),
                  'constraint_config':constraints.to_dict()}
        summary = {'success':True, 'constraints_satisfied':True, 'violations':[],
                   'optimized_strengths_raw':strengths,
                   'optimized_strengths_by_name_m_minus2':dict(zip(QUAD_NAMES,strengths))}
        path = folder/'bts_optimization_summary.json'
        path.write_text(json.dumps(summary))
        (folder/'config.json').write_text(json.dumps(config))
        return path
    return build


def fake_statistics():
    metric = {'p50_median':.01, 'p68':.02, 'p95':.03, 'p99':.04,
              'bootstrap_95ci_median':[.005,.015]}
    return {'failure_probability':0., 'mismatch_x':metric, 'mismatch_y':metric}


def test_only_supplied_run_is_used_and_metadata_reconstructs_inputs(optimization_runs, tmp_path, monkeypatch):
    first = optimization_runs('run_aaa', .1)
    second = optimization_runs('run_zzz', .2)
    os.utime(first, (999999999,999999999))
    os.utime(second, (1999999999,1999999999))
    snapshots = {p:p.read_bytes() for p in first.parent.parent.rglob('*.json')}
    budget = ErrorBudgetConfig(quad_k_rel_std=.003)
    error_path = tmp_path/'budget.json'; error_path.write_text(budget.to_json())
    monkeypatch.setattr(cli, 'repo_root', tmp_path)
    observed = []
    def evaluate(bts, target, samples, **kwargs):
        observed.append((bts,target,samples,kwargs))
        return fake_statistics()
    oat = []
    monkeypatch.setattr(cli,'evaluate_robustness_statistics',evaluate)
    monkeypatch.setattr(cli,'compute_one_at_a_time_sensitivity',lambda *args, **kwargs: oat.append((args,kwargs)) or {})
    output = tmp_path/'new tolerance'
    cli.main(['--optimization-summary',str(first), '--error-config',str(error_path),
              '--samples','3','--seed','123','--oat-samples','4','--oat-seed','99',
              '--workers','2','--output-dir',str(output)])
    saved = json.loads((output/'publication_tolerances_summary.json').read_text())
    nominal = BTSConfig.from_dict(saved['nominal_bts_config'])
    restored_budget = ErrorBudgetConfig.from_dict(saved['error_config'])
    assert nominal.k_q11 == pytest.approx(.548572,abs=1e-12)
    assert nominal.energy_eV == 5e9 and nominal.l_dr1 == 2.2 and nominal.ap1_limit == .023
    assert observed[0][0].to_dict() == nominal.to_dict()
    assert observed[0][1]['beta'][0] == 2.6
    assert observed[0][3]['initial_twiss']['beta'][0] == pytest.approx(8.3,abs=1e-12)
    assert observed[0][3]['beta_max_limit_m'] == 70
    assert observed[0][3]['mismatch_limit'] == 1.1
    assert observed[0][2] == sample_error_ensemble(restored_budget,n_samples=3,seed=123)
    assert oat[0][1]['seed'] == 99 and oat[0][1]['n_samples'] == 4
    assert oat[0][1]['error_config'].to_dict() == budget.to_dict()
    assert oat[0][1]['initial_twiss'] == saved['initial_twiss']
    assert saved['sampling']['bootstrap']['seed'] == 42
    for artifact in (saved['optimization_source'], saved['optimization_source']['config'], saved['error_config_source']):
        assert hashlib.sha256(Path(artifact['path']).read_bytes()).hexdigest() == artifact['sha256']
    assert saved['nominal_strengths_by_name_m_minus2'] == dict(zip(QUAD_NAMES,nominal.quad_strengths_list))
    assert all(p.read_bytes() == data for p,data in snapshots.items())


@pytest.mark.parametrize('field,value', [
    ('optimized_strengths_raw',None), ('optimized_strengths_raw',[1.]*8),
    ('optimized_strengths_raw',[np.nan]*9), ('optimized_strengths_raw',[np.inf]*9),
    ('optimized_strengths_raw',[True]*9), ('optimized_strengths_raw',['1']*9),
    ('success',False), ('constraints_satisfied',False), ('violations',['bad beta']),
    ('final_max_beta_x_m',np.inf), ('final_mismatch_x',2.),
])
def test_invalid_optimization_summary_is_rejected(optimization_runs, field, value):
    path=optimization_runs('run_bad')
    data=json.loads(path.read_text()); data[field]=value; path.write_text(json.dumps(data))
    with pytest.raises(ValueError): load_optimization_handoff(path)


@pytest.mark.parametrize('mutation', ['energy','nonfinite_energy','missing_geometry','missing_target',
    'bad_target','wrong_units','wrong_names','bad_bounds','named_disagreement','missing_config','unknown_schema'])
def test_incomplete_or_contradictory_saved_configuration_is_rejected(optimization_runs,mutation):
    path=optimization_runs('run_bad')
    config_path=path.with_name('config.json'); config=json.loads(config_path.read_text())
    if mutation=='energy': config['bts_config']['energy_eV']=4e9
    elif mutation=='nonfinite_energy': config['bts_config']['energy_eV']=np.nan
    elif mutation=='missing_geometry': config['bts_config'].pop('l_dr1')
    elif mutation=='missing_target': config['target_config'].pop('init_disp_x')
    elif mutation=='bad_target': config['target_config']['target_beta_x']=-1
    elif mutation=='wrong_units': config['units']['energy']='GeV'
    elif mutation=='wrong_names': config['quadrupole_names'][0]='q12'
    elif mutation=='bad_bounds': config['constraint_config']['quad_bounds']['q11']['k_max']=.1
    elif mutation=='named_disagreement':
        data=json.loads(path.read_text()); data['optimized_strengths_by_name_m_minus2']['q11']=.9; path.write_text(json.dumps(data))
    elif mutation=='unknown_schema': config['publication_input_schema_version']=2
    else: config_path.unlink()
    if mutation!='missing_config': config_path.write_text(json.dumps(config))
    with pytest.raises((ValueError,FileNotFoundError)): load_optimization_handoff(path)


def test_missing_input_never_creates_an_output(tmp_path):
    output=tmp_path/'out'
    with pytest.raises(SystemExit): cli.main(['--output-dir',str(output)])
    assert not output.exists()
    with pytest.raises(FileNotFoundError):
        cli.main(['--optimization-summary',str(tmp_path/'missing.json'),'--output-dir',str(output)])
    assert not output.exists()


def test_explicit_reference_mode_ignores_other_runs(optimization_runs,tmp_path,monkeypatch):
    optimization_runs('run_zzz',.2)
    monkeypatch.setattr(cli,'repo_root',tmp_path)
    monkeypatch.setattr(cli,'evaluate_robustness_statistics',lambda *a,**k: fake_statistics())
    monkeypatch.setattr(cli,'compute_one_at_a_time_sensitivity',lambda *a,**k: {})
    output=tmp_path/'reference'
    cli.main(['--reference','--output-dir',str(output),'--seed','5','--oat-samples','2'])
    saved=json.loads((output/'publication_tolerances_summary.json').read_text())
    assert saved['optimization_source']=={'mode':'reference'}
    assert saved['nominal_bts_config']==BTSConfig().to_dict()
    assert saved['sampling']['oat']['seed']==5
    with pytest.raises(ValueError,match='new or empty'):
        cli.main(['--reference','--output-dir',str(output)])


def test_schema_one_declares_canonical_units_when_explicit_annotations_are_absent(optimization_runs):
    path=optimization_runs('run_legacy_schema1')
    data=json.loads(path.with_name('config.json').read_text()); data.pop('units'); data.pop('quadrupole_names')
    path.with_name('config.json').write_text(json.dumps(data))
    assert load_optimization_handoff(path).source['units']==HANDOFF_UNITS


def test_error_application_preserves_geometry_energy_and_custom_entrance():
    nominal=BTSConfig(energy_eV=5e9,l_dr1=2.4,ap1_limit=.024)
    zero=sample_error_ensemble(ErrorBudgetConfig(**{key:0. for key in ErrorBudgetConfig().to_dict()}),n_samples=1)[0]
    entrance={'beta':[8.,13.],'alpha':[1.,-1.],'dispersion':[.2,.03,.04,.05]}
    lattice,twiss=apply_sample_errors(nominal,zero,initial_twiss=entrance)
    reference=create_bts_lattice(nominal)
    assert lattice.energy==5e9
    assert [element.Length for element in lattice]==[element.Length for element in reference]
    for key in entrance: assert twiss[key]==entrance[key]
    zero['energy_dp_p']=.01
    lattice,_=apply_sample_errors(nominal,zero,initial_twiss=entrance)
    assert lattice.energy==5e9*1.01
    assert lattice[0].Length==reference[0].Length


@pytest.mark.parametrize('workers',[1,2])
def test_saved_entrance_and_thresholds_reach_real_workers(workers):
    config=BTSConfig()
    budget=ErrorBudgetConfig(**{key:0. for key in ErrorBudgetConfig().to_dict()})
    samples=sample_error_ensemble(budget,n_samples=2,seed=9)
    entrance={'beta':[8.,13.],'alpha':[1.,-1.],'dispersion':[.2,.03,0.,0.]}
    target={'beta':[2.5,4.2],'alpha':[0.,0.]}
    stats=evaluate_robustness_statistics(config,target,samples,n_workers=workers,
        kicker_model='off',initial_twiss=entrance,beta_max_limit_m=1e6,mismatch_limit=1e6)
    from nkm_injection.optics import compute_twiss_propagation,compute_mismatch_metric
    lattice,twiss=apply_sample_errors(config,samples[0],initial_twiss=entrance)
    prop=compute_twiss_propagation(lattice,twiss)
    expected=compute_mismatch_metric(prop['final_beta'][0],prop['final_alpha'][0],2.5,0.)
    assert stats['mismatch_x']['p50']==pytest.approx(expected,abs=1e-12)
    assert stats['feasible_fraction']==1.
    ranking=compute_one_at_a_time_sensitivity(config,target,n_samples=2,seed=9,
        n_workers=workers,error_config=budget,initial_twiss=entrance)
    assert all(value==pytest.approx(0.,abs=1e-12) for value in ranking.values())
    assert any('Quad Gradient Error (0%)'==label for label in ranking)


def test_feasibility_validation_uses_saved_total_mismatch_and_optimizer_tolerances(optimization_runs):
    path=optimization_runs('run_thresholds')
    data=json.loads(path.read_text())
    data.update(final_mismatch_x=.6,final_mismatch_y=.6)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError,match='Total mismatch'): load_optimization_handoff(path)
    data.update(final_mismatch_x=.55,final_mismatch_y=.59,final_max_beta_x_m=70.005)
    path.write_text(json.dumps(data))
    assert load_optimization_handoff(path).constraints.mismatch_limit==1.1
