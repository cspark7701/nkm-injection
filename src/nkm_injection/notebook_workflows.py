"""Independent notebook studies with explicit configurations, results and outputs.

Interfaces use m, rad, eV, T, T m and geometric emittance m rad. The thick
tracker's legacy energy_GeV argument is converted explicitly from energy_eV.
"""
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Dict, Tuple, Any

import numpy as np
import at

from .configuration import SerializableConfigMixin
from .beam import generate_6d_beam
from .notebook_lattice import NotebookBTSConfig, create_notebook_bts_lattice
from .constraints import BTSConstraintConfig
from .objectives import OpticsTargetConfig
from .optimization import BTSOptimizationConfig, DeterministicObjective, OpticsOptimizer
from .optics import compute_twiss_propagation
from .results_schema import compute_file_hash
from .storage_ring_injection import (StorageRingInjectionConfig, build_storage_ring_nkm_lattice,
    load_storage_ring_injection_lattice, track_multiturn_injection, compute_multiturn_injection_metrics)
from .tracking import TrackingResult, track_nkm_thick_symplectic, track_nkm_thick_rk4
from .tracking_contracts import finite_scalar, positive_count, validate_particle_array
from .fieldmap import load_1d_fieldmap, NKMFieldMap1D, validate_1d_fieldmap
from .kickmap import NKMKickMap2D


def _seed(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 0:
        raise ValueError(f'{name} must be a nonnegative integer')


def notebook_repository_root(start=None):
    """Find checkout from cwd/ancestors or an explicit root; never change cwd/sys.path."""
    start = Path(start or os.environ.get('NKM_NOTEBOOK_REPO_ROOT', Path.cwd())).resolve()
    for candidate in (start, *start.parents):
        if (candidate / 'AGENTS.md').is_file() and (candidate / 'pyproject.toml').is_file():
            return candidate
    raise FileNotFoundError('Set NKM_NOTEBOOK_REPO_ROOT to the repository checkout')


def notebook_run_directory(repo_root, study):
    """Select a fresh destination without creating it; env override supports smoke runs."""
    if not study or Path(study).name != study or study in ('.', '..'):
        raise ValueError('study must be a single directory name')
    override = os.environ.get('NKM_NOTEBOOK_RUN_DIR')
    return (Path(override).resolve() if override else Path(repo_root).resolve() / 'results' /
            'notebooks' / study / datetime.now().strftime('run_%Y%m%d_%H%M%S_%f'))


def _json(value):
    # Undefined lost-beam metrics are null; stored particle arrays retain NaN loss markers.
    if isinstance(value, dict):
        return {str(k): _json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list, np.ndarray)):
        return [_json(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, Path):
        return str(value)
    return value


def _write(path, value):
    Path(path).write_text(json.dumps(_json(value), indent=2, allow_nan=False)+'\n', encoding='utf-8')


@contextmanager
def _study_run(config, repo_root, run_dir, input_names):
    config.validate()
    root, output = Path(repo_root).resolve(), Path(run_dir).resolve()
    config.to_dict()  # Reject nonfinite/unsupported configuration values before any writes.
    if output == root or root.is_relative_to(output) or (output.is_relative_to(root) and not output.is_relative_to(root / 'results')):
        raise ValueError('Study outputs must be separate from notebook/source directories')
    hashes = {name: compute_file_hash(root / name) for name in input_names}
    output.mkdir(parents=True, exist_ok=False)
    config.save(output / 'study_config.json')
    _write(output / 'provenance.json', {'input_sha256': hashes, 'repo_root': str(root),
                                      'units': 'm, rad, eV, T, T m, m rad'})
    try:
        yield root, output
        if any(compute_file_hash(root / name) != digest for name, digest in hashes.items()):
            raise RuntimeError('Scientific source bytes changed during study')
        _write(output / 'execution.json', {'status': 'completed'})
    except Exception as error:
        _write(output / 'execution.json', {'status': 'failed', 'exception_type': type(error).__name__,
                                          'error': str(error)})
        raise


@dataclass
class NotebookStudyResult:
    """Returned study data are the sole simulation inputs to notebook plots."""
    run_dir: Path
    summary: Dict[str, Any]
    data: Dict[str, Any]


@dataclass
class BeamStudyConfig(SerializableConfigMixin):
    """Gaussian beam: beta/length/offset m, momenta rad, emittance m rad."""
    n_particles: int = 100
    beta_x: float = 10.
    alpha_x: float = 0.
    emit_x: float = 1e-7
    beta_y: float = 5.
    alpha_y: float = 0.
    emit_y: float = 1e-8
    blength: float = 13.4e-3
    espread: float = 1.1e-3
    x_offset: float = -.016
    xp_offset: float = 0.
    y_offset: float = 0.
    yp_offset: float = 0.
    seed: int = 42

    def validate(self):
        positive_count(self.n_particles, 'n_particles')
        _seed(self.seed, 'seed')
        for name, value in vars(self).items():
            if name not in ('seed', 'n_particles'):
                finite_scalar(value, name)
        for name in ('beta_x', 'beta_y', 'emit_x', 'emit_y', 'blength', 'espread'):
            finite_scalar(getattr(self, name), name, minimum=0, nonzero=True)

    def generate(self):
        """Return seeded canonical (6, N) Gaussian coordinates in m/rad."""
        self.validate()
        return generate_6d_beam(**self.to_dict())


def _stored_beam():
    return BeamStudyConfig(emit_x=1e-8, emit_y=1e-9, x_offset=0.)


@dataclass
class InjectionStudyConfig(SerializableConfigMixin):
    """Notebook 02's original beam/model choices with explicit source lattice."""
    ring: StorageRingInjectionConfig = field(default_factory=StorageRingInjectionConfig)
    injected: BeamStudyConfig = field(default_factory=BeamStudyConfig)
    stored: BeamStudyConfig = field(default_factory=_stored_beam)
    n_turns: int = 10
    models: Tuple[str, ...] = ('off', 'ideal', 'linear', 'fieldmap')
    source_mat_filename: str = 'K4GSR_HBIv4-1.mat'
    kickmap_filename: str = 'kickmap_file.txt'

    def validate(self):
        self.ring.validate(); self.injected.validate(); self.stored.validate()
        positive_count(self.n_turns, 'n_turns')
        if not self.models or len(set(self.models)) != len(self.models) or any(
                model not in ('off', 'ideal', 'linear', 'fieldmap') for model in self.models):
            raise ValueError('Select distinct known kicker models')
        _source_names(self.source_mat_filename, self.kickmap_filename)


def _source_names(*names):
    if any(not name or Path(name).is_absolute() or '..' in Path(name).parts for name in names):
        raise ValueError('Input filenames must be repository-relative without parent traversal')


def _prepare_ring(config, root, output, source_mat_filename):
    # Never depend on a previously generated root lattice or auto-generate into sources.
    ring = build_storage_ring_nkm_lattice(root / source_mat_filename)
    if not np.isclose(ring.energy, config.energy_eV, rtol=1e-12, atol=0):
        raise ValueError('Configured ring energy must match source lattice energy (eV)')
    if not np.isclose(ring[next(i for i, el in enumerate(ring) if el.FamName == 'NKM')].Length, config.nkm_length_m, rtol=0, atol=1e-12):
        raise ValueError('Configured NKM length must match the source-ring insertion geometry (m)')
    path = output / 'storage_ring_lattice_nkm.mat'
    at.save_mat(ring, path)
    effective = replace(config, mat_filename=str(path))
    _write(output / 'effective_ring_config.json', effective.to_dict())
    return load_storage_ring_injection_lattice(effective, mat_path=path, auto_generate=False)[0]


def compare_injection_models(injected, stored, ring, config, kickmap, models, n_turns):
    """Return metrics and raw TrackingResults at the ring entrance each turn.

    Coordinates (6,N) use m/rad. Loss is a pre-existing NaN marker, native-map
    nonfinite result, or configured transverse aperture exceedance. Kicks act
    only on turn 1; this preserves notebook 02's shared tracking behavior.
    """
    metrics, injected_results, stored_results = {}, {}, {}
    for model in models:
        inj = track_multiturn_injection(injected, ring, n_turns=n_turns,
            kicker_model=model, kickmap_obj=kickmap, config=config)
        sto = track_multiturn_injection(stored, ring, n_turns=n_turns,
            kicker_model=model, kickmap_obj=kickmap, config=config)
        metrics[model] = compute_multiturn_injection_metrics(inj, sto, config)
        injected_results[model], stored_results[model] = inj, sto
    return {'metrics': metrics, 'injected_results': injected_results, 'stored_results': stored_results}


def _save_injection(output, data):
    arrays = {}
    for category in ('injected_results', 'stored_results'):
        for model, result in data[category].items():
            for name in ('particles_6d', 'centroid_history', 'emittance_history', 'survival_history'):
                arrays[f'{category}_{model}_{name}'] = getattr(result, name)
    np.savez(output / 'injection_arrays.npz', **arrays)
    _write(output / 'loss_logs.json', {category: {model: result.loss_log for model, result in data[category].items()}
                                     for category in ('injected_results', 'stored_results')})


def run_injection_notebook_study(config: InjectionStudyConfig, repo_root, run_dir):
    """Execute notebook 02 independently; all generated artifacts are run-local."""
    with _study_run(config, repo_root, run_dir, (config.source_mat_filename, config.kickmap_filename)) as (root, output):
        ring = _prepare_ring(config.ring, root, output, config.source_mat_filename)
        kickmap = NKMKickMap2D(root / config.kickmap_filename)
        injected, stored = config.injected.generate(), config.stored.generate()
        comparison = compare_injection_models(injected, stored, ring, config.ring,
                                              kickmap, config.models, config.n_turns)
        summary = {'metrics': comparison['metrics'], 'n_turns': config.n_turns,
                   'observation_point': 'ring entrance after each one-turn map',
                   'distribution': 'seeded Gaussian; complete Twiss/spread in study_config.json',
                   'loss_definition': 'initial NaN, nonfinite map, transverse aperture exceedance'}
        _write(output / 'summary.json', summary)
        _save_injection(output, comparison)
        np.savez(output / 'initial_beams.npz', injected_beam=injected, stored_beam=stored)
        return NotebookStudyResult(output, _json(summary), dict(comparison, injected_beam=injected,
                                    stored_beam=stored, models=config.models))


class NotebookMatchingObjective(DeterministicObjective):
    """Legacy sum of beta/alpha squared errors plus optional horizontal dispersion.

    Target sigmas must be 1 for the original raw objective. Dispersion derivative
    is deliberately omitted, as in notebook 01. The shared evaluator still
    reports physical peak-beta, hardware, envelope and mismatch feasibility.
    """
    def __init__(self, config, lattice, include_dispersion=True):
        super().__init__(config, lattice=lattice)
        self.include_dispersion = include_dispersion

    def compute_residual_vector(self, strengths):
        residuals = super().compute_residual_vector(strengths)
        return residuals[:5 if self.include_dispersion else 4]

    def exit_beta_margins(self, strengths, limit_m=60.):
        """Original endpoint beta constraints (m), distinct from peak-beta feasibility."""
        finite_scalar(limit_m, 'limit_m', minimum=0, nonzero=True)
        self.objectives.set_quads(strengths)
        return limit_m - compute_twiss_propagation(self.objectives.lattice,
                                                  self.objectives.initial_twiss)['final_beta']


def _matching_config():
    target = OpticsTargetConfig(sigma_beta_x=1., sigma_beta_y=1., sigma_alpha_x=1.,
                               sigma_alpha_y=1., sigma_disp_x=1., sigma_disp_px=1.)
    config = BTSOptimizationConfig(target_config=target, quad_bounds=(-5., 5.), max_iter=100)
    # Notebook's nominal q32=4.13 exceeds the production optimizer's default bounds.
    config.constraint_config.quad_bounds = {
        name: replace(bounds, k_min=-5., k_max=5., r_bore_m=.016)
        for name, bounds in config.constraint_config.quad_bounds.items()}
    return config


def _bts_beam():
    return BeamStudyConfig(n_particles=10000, beta_x=7.56, alpha_x=1.5231,
        beta_y=12.269, alpha_y=-1.6547, emit_x=10.89e-9, emit_y=10.89e-9, x_offset=0.)


@dataclass
class MainNotebookConfig(SerializableConfigMixin):
    """Steps 1–5 selections; geometry and all scientific parameters are explicit."""
    bts: NotebookBTSConfig = field(default_factory=NotebookBTSConfig)
    matching: BTSOptimizationConfig = field(default_factory=_matching_config)
    injection: InjectionStudyConfig = field(default_factory=InjectionStudyConfig)
    beam: BeamStudyConfig = field(default_factory=_bts_beam)
    derive_ring_target: bool = True
    target_beta_x_scale: float = .1
    target_alpha_x_scale: float = .1
    include_dispersion: bool = True
    optimize: bool = False
    optimization_method: str = 'Nelder-Mead'
    n_starts: int = 1
    n_slices: int = 40
    by_filename: str = 'By.txt'
    handoff_x_scale: float = .3
    handoff_xp_scale: float = .3
    handoff_x_offset_m: float = -.0057
    handoff_xp_offset_rad: float = .003
    gradient_error_samples: int = 20
    gradient_relative_std: float = .001
    error_seed: int = 42
    compute_acceptance: bool = False
    acceptance_npoints: Tuple[int, int] = (25, 25)
    acceptance_amplitudes: Tuple[float, float] = (.015, .002)  # x [m], xp [rad]
    acceptance_turns: int = 50

    def validate(self):
        self.bts.validate(); self.matching.validate(); self.injection.validate(); self.beam.validate()
        for name in ('n_starts', 'n_slices', 'gradient_error_samples'):
            positive_count(getattr(self, name), name)
        _seed(self.error_seed, 'error_seed')
        _seed(self.matching.random_seed, 'matching.random_seed')
        positive_count(self.matching.max_iter, 'matching.max_iter')
        for name in ('derive_ring_target', 'include_dispersion', 'optimize', 'compute_acceptance'):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f'{name} must be boolean')
        for name in ('target_beta_x_scale', 'target_alpha_x_scale', 'handoff_x_scale',
                     'handoff_xp_scale', 'handoff_x_offset_m', 'handoff_xp_offset_rad', 'gradient_relative_std'):
            finite_scalar(getattr(self, name), name)
        finite_scalar(self.target_beta_x_scale, 'target_beta_x_scale', minimum=0, nonzero=True)
        finite_scalar(self.gradient_relative_std, 'gradient_relative_std', minimum=0)
        energies = (self.bts.energy_eV, self.matching.constraint_config.energy_eV, self.injection.ring.energy_eV)
        if not np.allclose(energies, energies[0], rtol=1e-12, atol=0):
            raise ValueError('BTS, constraints and ring energies must agree')
        target = self.matching.target_config
        entrance = (target.init_beta_x, target.init_alpha_x, target.init_beta_y, target.init_alpha_y)
        if not np.allclose(entrance, (self.beam.beta_x, self.beam.alpha_x, self.beam.beta_y, self.beam.alpha_y), rtol=1e-12, atol=0):
            raise ValueError('BTS beam Twiss must agree with matching entrance optics')
        _source_names(self.by_filename)
        _acceptance_settings(self.acceptance_npoints, self.acceptance_amplitudes, self.acceptance_turns)
        if self.optimization_method not in ('Nelder-Mead', 'Powell', 'SLSQP', 'least_squares'):
            raise ValueError('Unsupported optimization method')


def track_bts_beam(lattice, beam):
    """Preserve AT single-pass transport at BTS exit; coordinates (6,N) in m/rad."""
    particles, valid = validate_particle_array(beam)
    result = particles.copy(order='F')
    if np.any(valid):
        result[:, valid] = at.lattice_track(lattice, particles[:, valid].copy(order='F'), 1)[1]['rout']
    result[:, ~np.isfinite(result).all(axis=0)] = np.nan
    lost = np.flatnonzero(~np.isfinite(result).all(axis=0))
    losses = [{'particle_index': int(index), 'cause': 'AT_loss' if valid[index] else 'initial_loss',
               'observation_point': 'BTS exit', 'element_index': None, 'element_name': None}
              for index in lost]
    return TrackingResult.from_beam(result, loss_log=losses, metadata={'observation_point': 'BTS exit',
        'loss_definition': 'initial NaN or AT nonfinite/aperture loss'})


def _acceptance_settings(npoints, amplitudes, n_turns):
    if len(npoints) != 2 or len(amplitudes) != 2:
        raise ValueError('Acceptance requires horizontal (x, xp) grid settings')
    for count in npoints:
        positive_count(count, 'acceptance grid count')
    for value in amplitudes:
        finite_scalar(value, 'acceptance amplitude (m, rad)', minimum=0, nonzero=True)
    positive_count(n_turns, 'acceptance_turns')


def compute_notebook_acceptance(ring, npoints=(25, 25), amplitudes=(.015, .002), n_turns=50):
    """Native AT horizontal acceptance at ring entrance; x m, xp rad, no extra kick.

    Matches the original optional AT API/grid selection, with explicit parameters.
    Results are returned directly; missing cached acceptance is never invented.
    """
    _acceptance_settings(npoints, amplitudes, n_turns)
    boundary, survived, tracked = ring.get_acceptance(planes=['x', 'xp'],
        npoints=npoints, amplitudes=amplitudes, nturns=n_turns, use_mp=False)
    return {'boundary': np.asarray(boundary), 'survived': np.asarray(survived),
            'tracked': np.asarray(tracked)}


def run_main_notebook_study(config: MainNotebookConfig, repo_root, run_dir):
    """Run field validation, thick tracking, injection, BTS matching and gradient errors.

    Thick tracking is a separate field-model comparison, not an extra pre-kick
    for multi-turn injection. The transfer beam uses the declared artificial
    scaled/offset handoff. Gradient errors cover quadrupole strength only.
    """
    inputs = (config.by_filename, config.injection.kickmap_filename, config.injection.source_mat_filename)
    with _study_run(config, repo_root, run_dir, inputs) as (root, output):
        ring = _prepare_ring(config.injection.ring, root, output, config.injection.source_mat_filename)
        lattice = create_notebook_bts_lattice(config.bts)
        matching = BTSOptimizationConfig.from_dict(config.matching.to_dict())
        if config.derive_ring_target:
            entrance = ring.get_optics()[0]
            matching.target_config = replace(matching.target_config,
                target_beta_x=float(entrance['beta'][0])*config.target_beta_x_scale,
                target_beta_y=float(entrance['beta'][1]),
                target_alpha_x=float(entrance['alpha'][0])*config.target_alpha_x_scale,
                target_alpha_y=float(entrance['alpha'][1]),
                target_disp_x=float(entrance['dispersion'][0]), target_disp_px=float(entrance['dispersion'][1]))
        matching.save(output / 'effective_matching_config.json')
        objective = NotebookMatchingObjective(matching, lattice, config.include_dispersion)
        optimizer = OpticsOptimizer(objective, matching)
        optimized = optimizer.optimize(config.optimization_method, config.n_starts) if config.optimize else None
        strengths = optimized.optimized_strengths if optimized else np.array(config.bts.strengths_m_minus2)
        evaluation = objective.evaluate(strengths)
        if evaluation['outcome']['status'] == 'invalid':
            raise ValueError(f'Invalid selected optics: {evaluation["exception"]}')
        optics = compute_twiss_propagation(lattice, objective.objectives.initial_twiss)
        initial = config.beam.generate()
        transported = track_bts_beam(lattice, initial)
        injected = transported.final_beam.copy()
        injected[0] = injected[0]*config.handoff_x_scale + config.handoff_x_offset_m
        injected[1] = injected[1]*config.handoff_xp_scale + config.handoff_xp_offset_rad
        stored = config.injection.stored.generate()
        x, by = load_1d_fieldmap(root / config.by_filename)
        fieldmap = NKMFieldMap1D(x, by)
        kickmap = NKMKickMap2D(root / config.injection.kickmap_filename)
        def field_fn(x, y, z):
            return fieldmap.evaluate(x), np.zeros_like(x)
        thick_options = dict(length_m=config.injection.ring.nkm_length_m, n_slices=config.n_slices,
            energy_GeV=config.bts.energy_eV*1e-9, particle_charge_C=config.injection.ring.particle_charge_C)
        symplectic = track_nkm_thick_symplectic(injected, field_fn, **thick_options)
        rk4 = track_nkm_thick_rk4(injected, field_fn, **thick_options)
        comparison = compare_injection_models(injected, stored, ring, config.injection.ring,
                                               kickmap, config.injection.models, config.injection.n_turns)
        acceptance = compute_notebook_acceptance(ring, config.acceptance_npoints,
            config.acceptance_amplitudes, config.acceptance_turns) if config.compute_acceptance else None
        if acceptance is not None:
            np.savez(output / 'acceptance.npz', **acceptance)
        errors = []
        for index, error in enumerate(np.random.default_rng(config.error_seed).normal(
                0., config.gradient_relative_std, size=(config.gradient_error_samples, 9))):
            candidate = strengths*(1.+error)
            # Every realization reconstructs geometry: no optimizer/global cross-cell state.
            sample_objective = NotebookMatchingObjective(matching, create_notebook_bts_lattice(config.bts), config.include_dispersion)
            metrics = sample_objective.evaluate(candidate)
            errors.append({'sample_id': index, 'strengths_m_minus2': candidate,
                'merit': metrics['merit'] if metrics['outcome']['status'] != 'invalid' else None,
                'outcome': metrics['outcome'], 'feasible': metrics['feasible']})
        finite = np.isfinite(symplectic) & np.isfinite(rk4)
        summary = {'field_validation': validate_1d_fieldmap(x, by),
            'kickmap_symmetry': kickmap.compute_symmetry_residuals(),
            'tracking': {'n_particles': config.beam.n_particles, 'seed': config.beam.seed,
                'distribution': 'Gaussian; full Twiss, energy spread and length in study_config.json',
                'bts_survival_fraction': transported.survival_fraction,
                'n_slices': config.n_slices, 'symplectic_rk4_max_abs_difference_by_coordinate':
                    [float(np.max(np.abs(symplectic[row, finite[row]]-rk4[row, finite[row]])))
                     if finite[row].any() else None for row in range(6)],
                'comparison_coordinate_units': ['m', 'rad', 'm', 'rad', 'fraction', 'm'],
                'observation_points': ['BTS exit', 'NKM exit', 'ring entrance after each turn'],
                'loss_definition': 'initial NaN, AT nonfinite/aperture loss, configured ring aperture'},
            'matching': {'optimizer_requested': config.optimize, 'method': config.optimization_method,
                'bounds_m_minus2': optimizer._build_bounds_list(), 'seed': matching.random_seed,
                'termination': optimized.message if optimized else 'optimization not requested',
                'optimizer_success': optimized.success if optimized else None,
                'final_feasible': evaluation['feasible'], 'violations': evaluation['violations'],
                'strengths_m_minus2': strengths, 'merit': evaluation['merit'],
                'mismatch_x': evaluation['mismatch_x'], 'mismatch_y': evaluation['mismatch_y'],
                'exit_beta_margins_m': objective.exit_beta_margins(strengths)},
            'injection': comparison['metrics'],
            'injection_tracking': {'n_injected_particles': injected.shape[1],
                'n_stored_particles': stored.shape[1], 'n_turns': config.injection.n_turns,
                'injected_distribution': 'BTS exit with explicitly configured scale/offset handoff',
                'stored_distribution': config.injection.stored.to_dict(),
                'first_turn_kick_only': True},
            'acceptance': {'requested': config.compute_acceptance,
                'observation_point': 'configured NKM ring entrance', 'model': 'native AT, no extra kick',
                'n_turns': config.acceptance_turns, 'npoints': config.acceptance_npoints,
                'amplitudes_m_rad': config.acceptance_amplitudes},
            'gradient_errors': {'scope': 'independent relative errors of nine matching quadrupoles only',
                'seed': config.error_seed, 'n_samples': config.gradient_error_samples, 'samples': errors}}
        _write(output / 'summary.json', summary)
        if optimized:
            _write(output / 'optimizer_candidates.json', [c.as_dict() for c in optimized.candidate_table])
        _save_injection(output, comparison)
        _write(output / 'bts_loss_log.json', transported.loss_log)
        np.savez(output / 'main_arrays.npz', initial_beam=initial, bts_exit=transported.final_beam,
            injected_beam=injected, stored_beam=stored, symplectic_exit=symplectic, rk4_exit=rk4,
            s_m=optics['s_pos'], beta_m=optics['beta'], x_field_m=x, by_T=by)
        return NotebookStudyResult(output, _json(summary), dict(comparison, optics=optics,
            initial_beam=initial, injected_beam=injected, stored_beam=stored,
            bts_exit=transported.final_beam, symplectic_exit=symplectic, rk4_exit=rk4,
            x_field_m=x, by_T=by, lattice=lattice, acceptance=acceptance))


def run_moga_notebook_study(config, repo_root, run_dir):
    """Execute optional notebook 03 independently and archive NSGA-II settings/results."""
    from .moga import run_bts_moga, save_moga_results_json
    positive_count(config.pop_size, 'pop_size')
    positive_count(config.n_gen, 'n_gen')
    positive_count(config.eval_n_mc_seeds, 'eval_n_mc_seeds')
    _seed(config.seed, 'seed')
    with _study_run(config, repo_root, run_dir, ()) as (_, output):
        result = run_bts_moga(config)
        save_moga_results_json(result, output)
        summary = {'seed': config.seed, 'termination': f'n_gen={config.n_gen}',
            'bounds_m_minus2': config.quad_bounds, 'constraints': {
                'beta_max_limit_m': config.beta_max_limit,
                'active_hardware': BTSConstraintConfig().to_dict(),
                'evaluator_diagnostics': config.bts_opt_config.constraint_config.to_dict(),
                'feasibility_tolerance': 1e-5},
            'final_feasible': result.success, 'feasible_fraction': result.feasible_fraction,
            'min_violation': result.min_violation, 'n_evaluations': result.n_evals}
        _write(output / 'summary.json', summary)
        np.savez(output / 'moga_arrays.npz', pareto_x=result.pareto_x, pareto_f=result.pareto_f,
                 least_infeasible_x=result.least_infeasible_x, least_infeasible_f=result.least_infeasible_f)
        return NotebookStudyResult(output, summary, {'result': result})
