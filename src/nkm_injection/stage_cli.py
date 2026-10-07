"""Shared stage CLI paths: read-only inputs and new/empty run-local outputs."""
from datetime import datetime
from pathlib import Path
from .results_schema import compute_file_hash


def add_source_argument(parser):
    parser.add_argument('--repo-root', type=Path, default=None,
                        help='Scientific source checkout; defaults to this script checkout')


def source_root(args, default):
    root = Path(args.repo_root or default).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f'Source root missing: {root}')
    return root


def stage_output(args, root, category, *, default=None):
    """Select an exact destination without writing; refuse occupied/source paths."""
    output = Path(args.output_dir or default or
        root / 'results' / category / f'run_{datetime.now():%Y%m%d_%H%M%S_%f}').resolve()
    if output == root or root.is_relative_to(output) or (
            output.is_relative_to(root) and not output.is_relative_to(root / 'results')):
        raise ValueError('Stage output must be separate from sources and under results/ inside the checkout')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Stage output directory must be new or empty')
    return output


def input_hashes(root, names):
    """Require every selected source and return complete SHA-256 digests."""
    return {name: compute_file_hash(root / name) for name in names}


def check_seed(seed):
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError('seed must be a nonnegative integer')


def nullable_result_metrics(value):
    """Serialize result metrics with undefined NaN observations represented by null.

    Infinity remains an error. This adapter is for computed result metrics only;
    configuration and input validation must continue rejecting nonfinite values.
    """
    import dataclasses
    import math
    import numpy as np
    from .configuration import _to_serializable
    if dataclasses.is_dataclass(value):
        value = dataclasses.asdict(value)
    if isinstance(value, dict):
        return {key: nullable_result_metrics(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [nullable_result_metrics(item) for item in value]
    if isinstance(value, (float, np.floating)) and math.isnan(value):
        return None
    return _to_serializable(value)
