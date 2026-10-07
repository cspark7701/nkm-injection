"""Explicit evaluation diagnostics; units belong to each model's public interface."""
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
import numpy as np


class NumericalEvaluationError(FloatingPointError):
    """Finite candidate physics could not be evaluated numerically."""


class EvaluationExecutionError(RuntimeError):
    """Unexpected/configuration error with evaluation identity; cause is preserved."""


EXPECTED_NUMERICAL_ERRORS = (FloatingPointError, np.linalg.LinAlgError)


@dataclass
class EvaluationOutcome:
    """JSON-compatible status for a candidate or sample, separate from its metrics.

    status is valid, infeasible (physical thresholds), or invalid (no physics
    result). Identity uses sample IDs or candidate strengths in m^-2.
    """
    status: str
    identity: Dict[str, Any]
    model_provenance: Dict[str, Any]
    physical_failure_reasons: List[str] = field(default_factory=list)
    exception: Optional[Dict[str, str]] = None

    def to_dict(self):
        def json_value(value):
            if isinstance(value, dict):
                return {key: json_value(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [json_value(item) for item in value]
            if isinstance(value, (float, np.floating)):
                return float(value) if np.isfinite(value) else None
            if isinstance(value, np.integer):
                return int(value)
            return value
        return json_value(asdict(self))


def exception_context(error, phase):
    """Preserve exception type, message and evaluation phase in saved diagnostics."""
    return {"type": type(error).__name__, "message": str(error), "phase": phase}


def require_finite(values, name):
    """Classify nonfinite numerical outputs as invalid evaluations."""
    if not np.all(np.isfinite(values)):
        raise NumericalEvaluationError(f"{name} contains NaN/Inf")


def validate_optics_result(prop):
    """Validate numerical optics values: beta/dispersion in m, alpha dimensionless."""
    for key in ("final_beta", "final_alpha", "final_dispersion", "max_beta_x", "max_beta_y"):
        require_finite(prop[key], key)
    if np.any(np.asarray(prop["final_beta"]) <= 0):
        raise NumericalEvaluationError("Propagated beta functions must be positive")
