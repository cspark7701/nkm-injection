import numpy as np
import pytest
from nkm_injection.revision_statistics import holm_adjust, paired_capture_difference, capture_by_id


def test_holm_known_family():
    assert np.allclose(holm_adjust([.03, .001, .02, .9]), [.06, .004, .06, .9])


def test_paired_constant_difference_and_alignment():
    r = {9: .4, 1: .2, 3: .8}
    c = {3: .82, 9: .42, 1: .22}
    out = paired_capture_difference(r, c, seed=1729, count=500)
    assert np.allclose(out['ci95'], [.02, .02])
    assert out['n_pairs'] == 3 and out['noninferior_at_declared_margin']
    assert out == paired_capture_difference(r, c, seed=1729, count=500)
    with pytest.raises(ValueError):
        paired_capture_difference(r, {1: .2})


def test_duplicate_realizations_rejected():
    row = {'sample_id': 0, 'models': {'fieldmap_3d': {'capture_fraction': .9}}}
    with pytest.raises(ValueError):
        capture_by_id({'realizations': [row, row]})
