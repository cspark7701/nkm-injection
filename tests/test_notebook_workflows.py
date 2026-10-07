"""Notebook behavior characterization and independent configured study execution."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import at
import numpy as np
import pytest

from nkm_injection.notebook_lattice import NotebookBTSConfig, create_notebook_bts_lattice
from nkm_injection.notebook_workflows import (
    BeamStudyConfig, InjectionStudyConfig, MainNotebookConfig, NotebookMatchingObjective,
    notebook_repository_root, notebook_run_directory, run_injection_notebook_study,
    run_main_notebook_study, run_moga_notebook_study, track_bts_beam,
)
from nkm_injection.storage_ring_injection import track_multiturn_injection

ROOT = Path(__file__).resolve().parents[1]
CHARACTERIZATION = json.loads((Path(__file__).parent / 'fixtures/notebook_bts_characterization.json').read_text())


def test_notebook_lattice_order_matrix_and_tracking_characterization():
    lattice = create_notebook_bts_lattice(NotebookBTSConfig())
    assert [el.FamName for el in lattice] == CHARACTERIZATION['element_names']
    assert sum(el.Length for el in lattice) == pytest.approx(CHARACTERIZATION['length_m'], abs=1e-12)
    np.testing.assert_allclose(at.find_m44(lattice, 0)[0], CHARACTERIZATION['m44'], rtol=1e-10, atol=1e-10)
    beam = np.array(CHARACTERIZATION['beam_in'])
    result = track_bts_beam(lattice, beam)
    expected = np.array(CHARACTERIZATION['beam_out'], dtype=float)
    np.testing.assert_allclose(result.final_beam[:, :3], expected[:, :3], rtol=1e-10, atol=1e-12)
    assert np.isnan(result.final_beam[:, 3]).all()
    np.testing.assert_array_equal(beam, CHARACTERIZATION['beam_in'])
    assert result.survived_particles == 3


@pytest.mark.parametrize('include_dispersion', [False, True])
def test_extracted_raw_matching_and_beta_constraints(include_dispersion):
    config = MainNotebookConfig().matching
    objective = NotebookMatchingObjective(config, create_notebook_bts_lattice(NotebookBTSConfig()), include_dispersion)
    for record in CHARACTERIZATION['records']:
        key = 'merit' if include_dispersion else 'merit_no_disp'
        assert objective.compute_scalar_merit(record['strengths']) == pytest.approx(record[key], rel=1e-10, abs=1e-10)
        assert objective.evaluate(record['strengths'])['merit'] == pytest.approx(record[key], rel=1e-10, abs=1e-10)
        np.testing.assert_allclose(objective.exit_beta_margins(record['strengths']), record['beta_margins_m'], rtol=1e-10, atol=1e-10)


def test_lattices_and_objectives_have_no_shared_mutable_state():
    config = MainNotebookConfig()
    first = create_notebook_bts_lattice(config.bts)
    second = create_notebook_bts_lattice(config.bts)
    objective = NotebookMatchingObjective(config.matching, first)
    objective.compute_scalar_merit(np.ones(9))
    assert next(el.K for el in second if el.FamName == 'q11') == .738
    assert config.bts.strengths_m_minus2[0] == .738
    repeated = [el for el in first if el.FamName == 'btsbm']
    repeated[0].BendingAngle = 0
    assert repeated[1].BendingAngle != 0


@pytest.mark.parametrize('factory', [BeamStudyConfig, NotebookBTSConfig, InjectionStudyConfig, MainNotebookConfig])
def test_complete_configuration_round_trip(factory):
    config = factory()
    assert factory.from_dict(config.to_dict()).to_dict() == config.to_dict()


@pytest.mark.parametrize('field,value', [('n_slices', True), ('gradient_relative_std', float('nan')),
    ('error_seed', -1), ('target_beta_x_scale', 0), ('handoff_x_scale', float('inf'))])
def test_invalid_main_configuration_precedes_output_creation(tmp_path, field, value):
    config = MainNotebookConfig()
    setattr(config, field, value)
    with pytest.raises(ValueError):
        run_main_notebook_study(config, ROOT, tmp_path / 'invalid')
    assert not (tmp_path / 'invalid').exists()


def test_configured_injection_matches_notebook02_shared_tracker(tmp_path):
    config = InjectionStudyConfig(n_turns=2, models=('off', 'ideal', 'linear', 'fieldmap'))
    config.injected.n_particles = config.stored.n_particles = 16
    root_files = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                  for name in (config.source_mat_filename, config.kickmap_filename)}
    study = run_injection_notebook_study(config, ROOT, tmp_path / 'injection')
    generated = study.run_dir / 'storage_ring_lattice_nkm.mat'
    ring = at.load_mat(generated)
    ring = ring.enable_6d(copy=True)
    from nkm_injection.kickmap import NKMKickMap2D
    kickmap = NKMKickMap2D(ROOT / config.kickmap_filename)
    for model in config.models:
        expected = track_multiturn_injection(config.injected.generate(), ring, n_turns=2,
            kicker_model=model, kickmap_obj=kickmap, config=config.ring)
        actual = study.data['injected_results'][model]
        np.testing.assert_allclose(actual.final_beam, expected.final_beam, rtol=1e-12, atol=1e-12, equal_nan=True)
        assert actual.survival_history == expected.survival_history
        assert actual.loss_log == expected.loss_log
    assert json.loads((study.run_dir/'execution.json').read_text())['status'] == 'completed'
    assert json.loads((study.run_dir/'effective_ring_config.json').read_text())['mat_filename'] == str(generated)
    assert root_files == {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in root_files}
    before = {p.name:p.read_bytes() for p in study.run_dir.iterdir() if p.is_file()}
    with pytest.raises(FileExistsError):
        run_injection_notebook_study(config, ROOT, study.run_dir)
    assert before == {p.name:p.read_bytes() for p in study.run_dir.iterdir() if p.is_file()}


def test_main_study_reproducibility_and_saved_metadata(tmp_path):
    config = MainNotebookConfig(n_slices=4, gradient_error_samples=2, optimize=True)
    config.matching.max_iter = 2
    config.beam.n_particles = config.injection.stored.n_particles = 16
    config.injection.n_turns = 2
    before = config.to_dict()
    first = run_main_notebook_study(config, ROOT, tmp_path / 'first')
    second = run_main_notebook_study(config, ROOT, tmp_path / 'second')
    assert config.to_dict() == before
    assert first.summary == second.summary
    for key in ('initial_beam', 'bts_exit', 'injected_beam', 'symplectic_exit', 'rk4_exit'):
        np.testing.assert_allclose(first.data[key], second.data[key], rtol=0, atol=0, equal_nan=True)
    assert len(first.summary['gradient_errors']['samples']) == 2
    assert first.summary['matching']['termination']
    assert len(first.summary['matching']['bounds_m_minus2']) == 9
    assert (first.run_dir/'optimizer_candidates.json').is_file()
    with np.load(first.run_dir/'main_arrays.npz') as arrays:
        assert arrays['initial_beam'].shape == (6, 16)
    effective = json.loads((first.run_dir/'effective_matching_config.json').read_text())
    assert effective['target_config']['target_beta_x'] > 0
    assert 'observation_points' in first.summary['tracking']


def test_moga_is_independent_and_reproducible(tmp_path):
    from nkm_injection.moga import BTSMOGAConfig
    config = BTSMOGAConfig(pop_size=4, n_gen=2, seed=42)
    first = run_moga_notebook_study(config, ROOT, tmp_path/'moga1')
    second = run_moga_notebook_study(config, ROOT, tmp_path/'moga2')
    for key in ('pareto_x', 'pareto_f', 'least_infeasible_x', 'least_infeasible_f'):
        np.testing.assert_allclose(getattr(first.data['result'], key), getattr(second.data['result'], key), rtol=0, atol=0)
    assert first.summary == second.summary
    assert (first.run_dir/'study_config.json').is_file()
    assert (first.run_dir/'moga_summary.json').is_file()


def test_root_and_output_resolution_are_read_only(tmp_path, monkeypatch):
    assert notebook_repository_root(ROOT/'notebooks') == ROOT
    monkeypatch.setenv('NKM_NOTEBOOK_REPO_ROOT', str(ROOT))
    monkeypatch.chdir(tmp_path)
    assert notebook_repository_root() == ROOT
    first = notebook_run_directory(ROOT, 'study')
    second = notebook_run_directory(ROOT, 'study')
    assert first != second
    assert not first.exists() and not second.exists()
    override = tmp_path/'custom'
    monkeypatch.setenv('NKM_NOTEBOOK_RUN_DIR', str(override))
    assert notebook_run_directory(ROOT, 'study') == override
    with pytest.raises(ValueError):
        run_injection_notebook_study(InjectionStudyConfig(), ROOT, ROOT/'notebooks/new_results')
    assert not (ROOT/'notebooks/new_results').exists()


def test_invalid_field_coverage_is_reported_without_extrapolation(tmp_path):
    from nkm_injection.fieldmap import OutOfDomainError
    config = MainNotebookConfig(handoff_x_offset_m=1., gradient_error_samples=1)
    config.beam.n_particles = config.injection.stored.n_particles = 8
    output = tmp_path/'out_of_domain'
    with pytest.raises(OutOfDomainError):
        run_main_notebook_study(config, ROOT, output)
    assert json.loads((output/'execution.json').read_text())['status'] == 'failed'
    assert not (output/'summary.json').exists()


def test_bts_loss_logs_keep_original_identity():
    lattice = create_notebook_bts_lattice(NotebookBTSConfig())
    beam = np.zeros((6, 4))
    beam[:, 0] = np.nan
    beam[0, 3] = 1.
    result = track_bts_beam(lattice, beam)
    assert [entry['particle_index'] for entry in result.loss_log] == [0, 3]
    assert [entry['cause'] for entry in result.loss_log] == ['initial_loss', 'AT_loss']
    assert result.survived_particles == 2


def test_notebooks_only_select_execute_and_plot():
    import ast
    for name in ('01_bts_main_simulation', '02_multiturn_injection_validation', '03_bts_moga_pareto'):
        notebook = json.loads((ROOT/'notebooks'/f'{name}.ipynb').read_text())
        code = '\n'.join(''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type']=='code')
        tree = ast.parse(code)
        assert all(node.name == 'normalize' for node in ast.walk(tree)
                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))  # radar-plot scaling only
        assert 'Path("..")' not in code
        assert 'sys.path' not in code and 'os.chdir' not in code
        assert all(not cell.get('outputs') for cell in notebook['cells'])


def test_optional_acceptance_passes_declared_native_at_settings():
    from nkm_injection.notebook_workflows import compute_notebook_acceptance
    class Ring:
        def get_acceptance(self, **kwargs):
            assert kwargs == {'planes': ['x', 'xp'], 'npoints': (3, 3),
                              'amplitudes': (.01, .001), 'nturns': 1, 'use_mp': False}
            return np.zeros((2, 0)), np.array([[.001], [.0001]]), np.zeros((2, 9))
    result = compute_notebook_acceptance(Ring(), (3, 3), (.01, .001), 1)
    assert result['survived'].shape == (2, 1)
    with pytest.raises(ValueError):
        compute_notebook_acceptance(Ring(), (0, 3), (.01, .001), 1)
