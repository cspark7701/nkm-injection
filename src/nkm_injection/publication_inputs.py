"""Read-only publication inputs from explicitly selected simulation run directories.

Positions/beta/dispersion: m; angles: rad; energy: eV; strengths: m^-2;
field: T. Legacy summary keys ending in mm or mrad are converted to SI.
Only documented, consumed metrics are required; unrelated diagnostic fields may
contain undefined values (for example the first-loss turn when no beam is lost).
"""

from dataclasses import dataclass, fields, replace
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple, Optional

import numpy as np

from .bts_lattice import BTSConfig
from .constraints import BTSConstraintConfig
from .objectives import OpticsTargetConfig
from .results_schema import PublicationManifest

MISMATCH_ROUNDOFF_TOLERANCE = 1e-12

QUAD_NAMES = ('q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33')


def _number(value: Any, name: str, minimum: Optional[float] = None,
            maximum: Optional[float] = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name}: expected a numeric value')
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f'{name}: expected a finite value')
    if minimum is not None and result < minimum:
        raise ValueError(f'{name}: must be >= {minimum}')
    if maximum is not None and result > maximum:
        raise ValueError(f'{name}: must be <= {maximum}')
    return result


def _mismatch(value: Any, name: str) -> float:
    """Normalize only nonnegative-metric roundoff within the documented tolerance."""
    return max(0.0, _number(value, name, -MISMATCH_ROUNDOFF_TOLERANCE))


def _count(value: Any, name: str, minimum: int = 1) -> int:
    result = _number(value, name, minimum)
    if result != int(result):
        raise ValueError(f'{name}: expected an integer')
    return int(result)


def _mapping(value: Any, name: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f'{name}: expected an object')
    return value


def _rows(value: Any, name: str) -> list:
    if not isinstance(value, list) or not value:
        raise ValueError(f'{name}: expected a nonempty list')
    return value


def _required(data: Dict[str, Any], key: str) -> Any:
    if key not in data:
        raise ValueError(f'missing required metric/configuration: {key}')
    return data[key]


def _config(cls: Any, data: Any, name: str) -> Any:
    """Require complete saved configurations, rather than filling absent defaults."""
    data = _mapping(data, name)
    missing = {f.name for f in fields(cls)} - data.keys()
    if missing:
        raise ValueError(f'{name}: incomplete saved configuration; missing {sorted(missing)}')
    for key, value in data.items():
        if key != 'quad_bounds':
            _number(value, f'{name}.{key}')
    config = cls.from_dict(data)
    if cls is BTSConstraintConfig:
        for key, bound in _mapping(data['quad_bounds'], f'{name}.quad_bounds').items():
            if key not in QUAD_NAMES:
                raise ValueError(f'{name}: unknown quadrupole {key}')
            for attr in ('k_min', 'k_max'):
                _number(_required(bound, attr), f'{key}.{attr}')
    return config


@dataclass(frozen=True)
class FieldValidationInputs:
    """Field peak/symmetry in T; interpolation error in raw map units (mrad)."""
    peak_by_T: float
    odd_symmetry_residual_T: float
    grid_interpolation_error_mrad: float


@dataclass(frozen=True)
class SliceConvergencePoint:
    """Reference exit angle in rad; survival is a fraction."""
    n_slices: int
    reference_xp_rad: float
    survival_fraction: float


@dataclass(frozen=True)
class SliceConvergenceInputs:
    recommended_slices: int
    points: Tuple[SliceConvergencePoint, ...]


@dataclass(frozen=True)
class OptimizationInputs:
    """Saved lattice, optics targets and hardware/beam configuration in SI units."""
    selected_bts: BTSConfig
    target: OpticsTargetConfig
    constraints: BTSConstraintConfig
    strength_bounds_m_inv2: Tuple[Tuple[float, float], ...]
    mismatch_x: float
    mismatch_y: float

    @property
    def entrance_twiss(self) -> Dict[str, Any]:
        t = self.target
        return {'beta': [t.init_beta_x, t.init_beta_y],
                'alpha': [t.init_alpha_x, t.init_alpha_y],
                'dispersion': [t.init_disp_x, t.init_disp_px, 0.0, 0.0]}


@dataclass(frozen=True)
class InjectionInputs:
    """Capture/CI as fractions; stored centroid oscillation in m."""
    model: str
    n_particles: int
    n_turns: int
    n_seeds: int
    capture: float
    ci_lo: float
    ci_hi: float
    ci_level: float
    stored_oscillation_m: Optional[float]


@dataclass(frozen=True)
class ToleranceInputs:
    """Mismatch and failure probability are dimensionless."""
    n_samples: int
    failure_probability: float
    mismatch_x_median: float
    mismatch_y_median: float


@dataclass(frozen=True)
class MOGASeedInputs:
    """Per-seed feasibility fraction and Pareto count (no hypervolume units assumed)."""
    seed: int
    success: bool
    feasible_fraction: float
    pareto_count: int


@dataclass(frozen=True)
class PublicationInputs:
    """Validated inputs plus exact upstream paths and SHA-256 artifact hashes."""
    field: FieldValidationInputs
    convergence: SliceConvergenceInputs
    optimization: OptimizationInputs
    injection: Tuple[InjectionInputs, ...]
    tolerance: ToleranceInputs
    moga: Tuple[MOGASeedInputs, ...]
    artifacts: Dict[str, Dict[str, str]]

    def provenance(self) -> Dict[str, Any]:
        return {'schema_version': 1, 'artifacts': self.artifacts,
                'units': {'position': 'm', 'angle': 'rad', 'energy': 'eV',
                          'field': 'T', 'quadrupole_strength': 'm^-2',
                          'emittance': 'm rad', 'capture': 'fraction'},
                'validation_tolerances': {'mismatch_roundoff': MISMATCH_ROUNDOFF_TOLERANCE},
                'optics_source': 'recomputed from selected strengths and saved entrance Twiss'}


def load_publication_inputs(manifest: PublicationManifest, repo_root: Path) -> PublicationInputs:
    """Load exact named artifacts; never search for a latest run or substitute defaults.

    Missing/malformed consumed metrics raise ValueError with the artifact path.
    Missing files raise FileNotFoundError. Reading never changes upstream files.
    """
    root = Path(repo_root).resolve()
    artifacts = {}

    def read(stage: str, filename: str) -> Any:
        path = (root / getattr(manifest, stage) / filename).resolve()
        raw = path.read_bytes()
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError(f'{path}: invalid JSON') from exc
        artifacts[stage + '/' + filename] = {
            'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()}
        return data

    def parse(stage: str, filename: str, parser: Any) -> Any:
        data = read(stage, filename)
        try:
            return parser(data)
        except (ValueError, TypeError, KeyError) as exc:
            raise ValueError(f'{artifacts[stage + "/" + filename]["path"]}: {exc}') from exc

    def field_parser(raw):
        raw = _mapping(raw, 'field validation')
        one = _mapping(_required(raw, '1d_fieldmap_validation'), '1d_fieldmap_validation')
        two = _mapping(_required(raw, '2d_kickmap_validation'), '2d_kickmap_validation')
        if _required(one, 'valid') is not True:
            raise ValueError('1-D field validation did not pass')
        if _required(_mapping(_required(two, 'lorentz_kick_test'), 'lorentz_kick_test'), 'sign_verified') is not True:
            raise ValueError('Lorentz kick sign validation did not pass')
        return FieldValidationInputs(
            _number(_required(one, 'peak_by_T'), 'peak_by_T', 0),
            _number(_required(one, 'odd_symmetry_residual_T'), 'odd_symmetry_residual_T', 0),
            _number(_required(two, 'grid_interpolation_max_err'), 'grid_interpolation_max_err', 0))

    def convergence_parser(raw):
        raw = _mapping(raw, 'tracking convergence')
        points = []
        for row in _rows(_required(raw, 'results'), 'results'):
            row = _mapping(row, 'convergence row')
            points.append(SliceConvergencePoint(
                _count(_required(row, 'n_slices'), 'n_slices'),
                _number(_required(row, 'ref_xp_exit_mrad'), 'ref_xp_exit_mrad') * 1e-3,
                _number(_required(row, 'inj_survival_fraction'), 'inj_survival_fraction', 0, 1)))
        counts = [p.n_slices for p in points]
        if any(b <= a for a, b in zip(counts, counts[1:])):
            raise ValueError('slice counts must be strictly increasing and unique')
        return SliceConvergenceInputs(_count(_required(raw, 'recommended_production_slices'),
                                             'recommended_production_slices'), tuple(points))

    field = parse('field_validation_run', 'fieldmap_validation_metrics.json', field_parser)
    convergence = parse('tracking_convergence_run', 'tracking_convergence_summary.json', convergence_parser)
    def configuration_parser(raw):
        config = _mapping(raw, 'optimization config')
        if _required(config, 'publication_input_schema_version') != 1:
            raise ValueError('unsupported publication_input_schema_version (expected 1)')
        bts = _config(BTSConfig, _required(config, 'bts_config'), 'bts_config')
        target = _config(OpticsTargetConfig, _required(config, 'target_config'), 'target_config')
        constraints = _config(BTSConstraintConfig, _required(config, 'constraint_config'), 'constraint_config')
        if bts.energy_eV != constraints.energy_eV:
            raise ValueError('lattice and constraint beam energies differ')
        global_bounds = _required(config, 'quad_bounds_global')
        if not isinstance(global_bounds, list) or len(global_bounds) != 2:
            raise ValueError('quad_bounds_global must contain two values')
        lo, hi = [_number(k, 'quad_bounds_global') for k in global_bounds]
        if lo >= hi:
            raise ValueError('quad_bounds_global must be ordered')
        bounds = tuple((constraints.quad_bounds[q].k_min, constraints.quad_bounds[q].k_max)
                       if q in constraints.quad_bounds else (lo, hi) for q in QUAD_NAMES)
        return bts, target, constraints, bounds

    bts, target, constraints, bounds = parse('bts_optimization_run', 'config.json', configuration_parser)

    def optimization_parser(raw):
        raw = _mapping(raw, 'optimization summary')
        if _required(raw, 'success') is not True or _required(raw, 'constraints_satisfied') is not True:
            raise ValueError('selected optimization must be successful and feasible')
        strengths = _rows(_required(raw, 'optimized_strengths_raw'), 'optimized_strengths_raw')
        if len(strengths) != len(QUAD_NAMES):
            raise ValueError('expected nine quadrupole strengths in q11..q33 order')
        strengths = [_number(k, 'optimized_strengths_raw') for k in strengths]
        if any(not lower <= k <= upper for k, (lower, upper) in zip(strengths, bounds)):
            raise ValueError('optimized strengths violate saved hardware bounds')
        selected = replace(bts, **dict(zip(('k_' + q for q in QUAD_NAMES), strengths)))
        return OptimizationInputs(selected, target, constraints, bounds,
                                  _mismatch(_required(raw, 'final_mismatch_x'), 'final_mismatch_x'),
                                  _mismatch(_required(raw, 'final_mismatch_y'), 'final_mismatch_y'))

    optimization = parse('bts_optimization_run', 'bts_optimization_summary.json', optimization_parser)

    def injection_parser(raw):
        rows = []
        for row in _rows(raw, 'injection summary'):
            row = _mapping(row, 'injection row')
            model = _required(row, 'kicker_model')
            if model not in ('off', 'ideal', 'linear', 'fieldmap') or model in [r.model for r in rows]:
                raise ValueError('unknown or duplicate kicker model')
            capture = _number(_required(row, 'capture_mean'), 'capture_mean', 0, 1)
            lo = _number(_required(row, 'capture_ci_lo'), 'capture_ci_lo', 0, 1)
            hi = _number(_required(row, 'capture_ci_hi'), 'capture_ci_hi', 0, 1)
            if not lo <= capture <= hi:
                raise ValueError('capture mean must lie inside the confidence interval')
            stored = _required(row, 'stored_centroid_osc_mm')
            # Explicit null means the stored-beam metric is unavailable, independently of
            # injected capture. Legacy zero-capture NaN remains compatible; never use zero.
            if stored is None or capture == 0 and isinstance(stored, float) and np.isnan(stored):
                stored_m = None
            else:
                stored_m = _number(stored, 'stored_centroid_osc_mm', 0) * 1e-3
            rows.append(InjectionInputs(model,
                _count(_required(row, 'n_particles'), 'n_particles'),
                _count(_required(row, 'n_turns'), 'n_turns'),
                _count(_required(row, 'n_seeds'), 'n_seeds'), capture, lo, hi,
                _number(_required(row, 'capture_ci_level'), 'capture_ci_level', 0, 1), stored_m))
            if not 0 < rows[-1].ci_level < 1:
                raise ValueError('capture_ci_level must lie strictly between zero and one')
        return tuple(rows)

    injection = parse('injection_run', 'injection_metrics_summary.json', injection_parser)

    def tolerance_parser(raw):
        raw = _mapping(raw, 'tolerance summary')
        stats = _mapping(_required(raw, 'robustness_statistics'), 'robustness_statistics')
        if stats.get('n_invalid_evaluations', 0) != 0:
            raise ValueError('Tolerance publication requires zero invalid evaluations')
        count = _count(_required(raw, 'n_samples'), 'n_samples')
        if count != _count(_required(stats, 'n_samples'), 'robustness_statistics.n_samples'):
            raise ValueError('tolerance sample counts differ')
        return ToleranceInputs(count,
            _number(_required(stats, 'failure_probability'), 'failure_probability', 0, 1),
            _mismatch(_required(_mapping(_required(stats, 'mismatch_x'), 'mismatch_x'), 'p50_median'), 'mismatch_x.p50_median'),
            _mismatch(_required(_mapping(_required(stats, 'mismatch_y'), 'mismatch_y'), 'p50_median'), 'mismatch_y.p50_median'))

    tolerance = parse('tolerance_run', 'publication_tolerances_summary.json', tolerance_parser)

    def moga_parser(raw):
        raw = _mapping(raw, 'MOGA summary')
        seeds = [_count(s, 'seed', 0) for s in _rows(_required(raw, 'seeds'), 'seeds')]
        if len(set(seeds)) != len(seeds):
            raise ValueError('duplicate MOGA seeds')
        metrics = _mapping(_required(raw, 'seed_metrics'), 'seed_metrics')
        rows = []
        for seed in seeds:
            row = _mapping(_required(metrics, f'seed_{seed}'), f'seed_{seed}')
            success = _required(row, 'success')
            if not isinstance(success, bool):
                raise ValueError('MOGA success must be boolean')
            rows.append(MOGASeedInputs(seed, success,
                _number(_required(row, 'feasible_fraction'), 'feasible_fraction', 0, 1),
                _count(_required(row, 'pareto_count'), 'pareto_count', 0)))
        return tuple(rows)

    moga = parse('moga_run', 'multi_seed_moga_summary.json', moga_parser)
    return PublicationInputs(field, convergence, optimization, injection, tolerance, moga, artifacts)
