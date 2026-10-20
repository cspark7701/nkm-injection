"""Ideal static BTS steering; positions m, canonical momenta rad."""
import numpy as np

PLANE_ROWS = {'x': (0, 1), 'xy': (0, 1, 2, 3)}


def subtract_static_reference(beam, reference, planes='x'):
    """Subtract the static reference in the steered planes (``'x'``: x, p_x; ``'xy'``: x, p_x, y, p_y).

    ``beam`` is (6,N), including permitted lost columns; ``reference`` is a finite (6,1) zero-input particle
    transported through the perturbed BTS. The other rows are preserved. This ideal downstream translation does not
    undo optics errors or jitter. Returns the subtracted static coordinates in row order.
    """
    if planes not in PLANE_ROWS:
        raise ValueError(f"planes must be one of {sorted(PLANE_ROWS)}")
    if beam.ndim != 2 or beam.shape[0] != 6 or reference.shape != (6, 1):
        raise ValueError('Expected (6,N) beam and (6,1) reference')
    if not np.isfinite(reference).all():
        raise ValueError('Static reference was lost or is nonfinite')
    rows = PLANE_ROWS[planes]
    for r in rows:
        beam[r] -= reference[r, 0]
    return [float(reference[r, 0]) for r in rows]


def subtract_static_horizontal_reference(beam, reference):
    """Subtract only the static reference x and p_x, preserving all other rows (production steering)."""
    return subtract_static_reference(beam, reference, 'x')
