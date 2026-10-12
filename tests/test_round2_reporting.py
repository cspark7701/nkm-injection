import importlib.util
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location('round2_reporting',Path(__file__).resolve().parents[1]/'scripts/round2_reporting.py')
report=importlib.util.module_from_spec(spec);spec.loader.exec_module(report)


def rows(values):
    return [{'axis':'angle','offset_mm_or_mrad':x,'captured':k,'n_particles':100} for x,k in values]


def test_window_selects_connected_region_containing_fixed_nominal_point():
    # The distant stable island must not enlarge the usable central window.
    data=rows([(-3,90),(-2,70),(-1,70),(0,90),(1,70),(2,90),(3,70)])
    assert report.window_bounds(data,'angle')==pytest.approx((-.5,.5))


def test_unbracketed_or_failed_nominal_window_is_rejected():
    for values in ([(-1,70),(0,90),(1,90)],[(-1,90),(0,70),(1,90)]):
        with pytest.raises(ValueError):report.window_bounds(rows(values),'angle')
