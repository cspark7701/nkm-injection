"""
NKM Concurrency and Parallel Worker Dispatch Utility Module

Provides standardized multi-process dispatch (`parallel_map`), CPU core resolution (`resolve_workers`),
deterministic worker seed generation (`generate_worker_seeds`), and robust sequential fallbacks.
"""

from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os
import sys
from typing import Callable, Sequence, List, TypeVar, Optional, Any, Tuple
import numpy as np

T = TypeVar("T")
R = TypeVar("R")


def get_mp_context():
    """Return forkserver or spawn multiprocessing context to ensure OpenMP/C safety."""
    for method in ["forkserver", "spawn"]:
        try:
            return multiprocessing.get_context(method)
        except ValueError:
            continue
    return multiprocessing.get_context()


def resolve_workers(workers: Optional[int] = None) -> int:
    """
    Resolve requested worker count to a valid positive integer.
    
    If workers is None or <= 0:
        Returns max(1, (os.cpu_count() or 1) - 1).
    Otherwise returns int(workers).
    """
    if workers is None or workers <= 0:
        cpu_count = os.cpu_count() or 1
        return max(1, cpu_count - 1 if cpu_count > 1 else 1)
    return int(workers)


def generate_worker_seeds(base_seed: int, n_items: int) -> List[int]:
    """
    Generate n_items deterministic, distinct random seeds for parallel workers.
    
    Prevents RNG seed collisions across spawned child processes.
    """
    return [int(base_seed + i * 10007) for i in range(n_items)]


def _sample_square(x: int) -> int:
    """Module-level test helper for multiprocessing test dispatch."""
    return x * x


def _failing_worker(x: int) -> int:
    """Module-level test helper that raises ValueError for negative inputs."""
    if x < 0:
        raise ValueError("Negative number error")
    return x * 2


def parallel_map(
    func: Callable[[T], R],
    items: Sequence[T],
    n_workers: Optional[int] = 1,
    chunksize: int = 1,
    desc: Optional[str] = None
) -> List[R]:
    """
    Execute func over items in parallel using a ProcessPoolExecutor, preserving input order.
    
    Parameters
    ----------
    func : Callable[[T], R]
        Top-level pickleable function to apply to each item.
    items : Sequence[T]
        Sequence of input items.
    n_workers : int, optional
        Number of worker processes. If <= 1 or len(items) <= 1, executes
        synchronously in the main process (sequential fallback).
    chunksize : int, optional
        Chunk size passed to executor.map. Defaults to 1.
    desc : str, optional
        Optional description string for logging context.
        
    Returns
    -------
    List[R]
        Ordered list of results matching the input items sequence.
        
    Raises
    ------
    RuntimeError
        If any worker process raises an exception, wraps the original exception
        with item and worker context.
    """
    items_list = list(items)
    n_items = len(items_list)
    if n_items == 0:
        return []

    workers = 1 if n_workers is None else int(n_workers)

    # Sequential execution fallback
    if workers <= 1 or n_items <= 1:
        results = []
        for idx, item in enumerate(items_list):
            try:
                results.append(func(item))
            except Exception as exc:
                msg = f"Sequential execution failed on item {idx}/{n_items}"
                if desc:
                    msg += f" ({desc})"
                msg += f": {exc}"
                raise RuntimeError(msg) from exc
        return results

    # Multi-process parallel execution
    actual_workers = min(workers, n_items)
    ctx = get_mp_context()
    try:
        with ProcessPoolExecutor(max_workers=actual_workers, mp_context=ctx) as executor:
            # executor.map preserves input sequence order
            results = list(executor.map(func, items_list, chunksize=max(1, chunksize)))
        return results
    except Exception as exc:
        msg = f"Parallel execution with {actual_workers} workers failed"
        if desc:
            msg += f" ({desc})"
        msg += f": {exc}"
        raise RuntimeError(msg) from exc
