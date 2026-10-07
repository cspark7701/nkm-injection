"""Read-only optimization inputs for tolerance studies; no run discovery.

Schema 1 uses m, rad, eV and m^-2, with strengths ordered q11..q33.
"""
from dataclasses import dataclass, fields, replace
import hashlib
import json
from pathlib import Path
import numpy as np

from .bts_lattice import BTSConfig
from .constraints import BTSConstraintConfig, QuadrupoleHardwareBounds
from .objectives import OpticsTargetConfig
from .errors import ErrorBudgetConfig

QUAD_NAMES = ('q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33')
HANDOFF_UNITS = {'energy': 'eV', 'position': 'm', 'angle': 'rad',
                 'quadrupole_strength': 'm^-2', 'beta': 'm', 'alpha': '1',
                 'dispersion': 'm', 'dispersion_prime': '1'}


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value):
        raise ValueError(f'{label} must be a finite number')
    return float(value)


def complete_config(cls, data):
    """Validate a complete saved config without supplying missing defaults."""
    names = {field.name for field in fields(cls)}
    if not isinstance(data, dict) or set(data) != names:
        raise ValueError(f'{cls.__name__} requires exactly its complete saved fields')
    for key, value in data.items():
        if key == 'quad_bounds':
            if not isinstance(value, dict) or any(name not in QUAD_NAMES for name in value):
                raise ValueError('Invalid quadrupole bounds names')
            for name, bound in value.items():
                expected = {f.name for f in fields(QuadrupoleHardwareBounds)}
                if not isinstance(bound, dict) or set(bound) != expected or bound['name'] != name:
                    raise ValueError(f'Invalid saved bounds for {name}')
                for attr, val in bound.items():
                    if attr != 'name':
                        number(val, f'{name}.{attr}')
        else:
            number(value, f'{cls.__name__}.{key}')
    result = cls.from_dict(data)
    result.validate()
    return result


def read_json_artifact(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError(f'{path}: expected a JSON object')
    return data, {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()}


@dataclass(frozen=True)
class OptimizationHandoff:
    """Selected nominal lattice, entrance/target optics and feasibility settings."""
    bts: BTSConfig
    target: OpticsTargetConfig
    constraints: BTSConstraintConfig
    source: dict

    @property
    def initial_twiss(self):
        return {'beta': [self.target.init_beta_x, self.target.init_beta_y],
                'alpha': [self.target.init_alpha_x, self.target.init_alpha_y],
                'dispersion': [self.target.init_disp_x, self.target.init_disp_px, 0., 0.]}

    @property
    def target_twiss(self):
        return {'beta': [self.target.target_beta_x, self.target.target_beta_y],
                'alpha': [self.target.target_alpha_x, self.target.target_alpha_y],
                'dispersion': [self.target.target_disp_x, self.target.target_disp_px, 0., 0.]}


def reference_handoff():
    """Explicit reference mode in canonical units; never an optimization fallback."""
    return OptimizationHandoff(BTSConfig(), OpticsTargetConfig(), BTSConstraintConfig(),
                               {'mode': 'reference'})


def load_optimization_handoff(summary_path):
    """Read a successful feasible summary and adjacent config.json, hashing both.

    Complete schema-1 configurations without explicit units/names retain their
    documented canonical units/order; contradictory declarations are rejected.
    """
    path = Path(summary_path).resolve()
    summary, summary_artifact = read_json_artifact(path)
    saved, config_artifact = read_json_artifact(path.with_name('config.json'))
    if type(saved.get('publication_input_schema_version')) is not int or saved['publication_input_schema_version'] != 1:
        raise ValueError('Expected publication_input_schema_version=1')
    if summary.get('success') is not True or summary.get('constraints_satisfied') is not True or summary.get('violations'):
        raise ValueError('Selected optimization must be successful and finally feasible')
    if saved.get('units', HANDOFF_UNITS) != HANDOFF_UNITS:
        raise ValueError('Optimization units must match the canonical schema-1 units')
    names = saved.get('quadrupole_names', QUAD_NAMES)
    if not isinstance(names, (list, tuple)) or tuple(names) != QUAD_NAMES:
        raise ValueError('Expected nine named strengths in q11..q33 order')
    raw = summary.get('optimized_strengths_raw')
    if not isinstance(raw, list) or len(raw) != 9:
        raise ValueError('Expected exactly nine optimized strengths')
    strengths = [number(value, name) for name, value in zip(QUAD_NAMES, raw)]
    named = summary.get('optimized_strengths_by_name_m_minus2')
    if named is not None:
        if not isinstance(named, dict) or set(named) != set(QUAD_NAMES):
            raise ValueError('Expected exactly nine quadrupole names')
        if [number(named[name], name) for name in QUAD_NAMES] != strengths:
            raise ValueError('Named and ordered optimized strengths disagree')
    bts = complete_config(BTSConfig, saved.get('bts_config'))
    target = complete_config(OpticsTargetConfig, saved.get('target_config'))
    constraints = complete_config(BTSConstraintConfig, saved.get('constraint_config'))
    if bts.energy_eV != constraints.energy_eV:
        raise ValueError('Lattice and constraint beam energies differ (eV)')
    for key, limit in (("final_max_beta_x_m", constraints.beta_max_limit_m + .01),
                       ("final_max_beta_y_m", constraints.beta_max_limit_m + .01),
                       ("final_mismatch_x", constraints.mismatch_limit),
                       ("final_mismatch_y", constraints.mismatch_limit + .05)):
        if key in summary:
            value = number(summary[key], key)
            if value < -1e-12 or value > limit:
                raise ValueError(f'{key} contradicts final feasibility')
    if all(key in summary for key in ("final_mismatch_x", "final_mismatch_y")):
        if summary["final_mismatch_x"] + summary["final_mismatch_y"] > constraints.mismatch_limit + .05:
            raise ValueError('Total mismatch contradicts final feasibility')
    global_bounds = saved.get('quad_bounds_global')
    if not isinstance(global_bounds, list) or len(global_bounds) != 2:
        raise ValueError('Missing two global quadrupole bounds (m^-2)')
    lo, hi = [number(value, 'quad_bounds_global') for value in global_bounds]
    if lo >= hi:
        raise ValueError('Quadrupole bounds must be increasing')
    for name, strength in zip(QUAD_NAMES, strengths):
        bound = constraints.quad_bounds.get(name)
        lower, upper = (bound.k_min, bound.k_max) if bound is not None else (lo, hi)
        if not lower <= strength <= upper:
            raise ValueError(f'{name} violates saved strength bounds')
    nominal = replace(bts, **dict(zip(('k_' + name for name in QUAD_NAMES), strengths)))
    return OptimizationHandoff(nominal, target, constraints,
        {**summary_artifact, 'mode': 'optimization', 'config': config_artifact,
         'schema_version': 1, 'units': dict(HANDOFF_UNITS)})


def load_error_budget(path=None):
    """Return complete error configuration and optional selected-file provenance."""
    if path is None:
        return ErrorBudgetConfig(), None
    data, artifact = read_json_artifact(path)
    return complete_config(ErrorBudgetConfig, data), artifact
