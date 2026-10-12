"""Ideal static BTS steering; positions m, canonical momenta rad."""
import numpy as np


def subtract_static_horizontal_reference(beam, reference):
    """Subtract only the static reference x and p_x, preserving all other rows.

    ``beam`` is (6,N), including permitted lost columns; ``reference`` is a
    finite (6,1) zero-input particle transported through the perturbed BTS.
    This ideal downstream translation does not undo optics errors or jitter.
    """
    if beam.ndim != 2 or beam.shape[0] != 6 or reference.shape != (6, 1):
        raise ValueError('Expected (6,N) beam and (6,1) reference')
    if not np.isfinite(reference).all():
        raise ValueError('Static reference was lost or is nonfinite')
    beam[0] -= reference[0, 0]
    beam[1] -= reference[1, 0]
    return reference[:2, 0].tolist()
