"""Regression contracts for finite grids, closed domains and broadcasting."""
from pathlib import Path
import importlib.util
import shutil
import sys

import numpy as np
import pytest

from nkm_injection.fieldmap import (
    NKMFieldMap1D, NKMFieldMap3D, OutOfDomainError,
    integrate_longitudinal_field, interpolate_3d_field_vectorized,
    load_1d_fieldmap, validate_1d_fieldmap,
)
from nkm_injection.kickmap import NKMKickMap2D, load_2d_kickmap
from patches.pyat_extensions.pyat.at.integrators.pyNKMPass import (
    interpolate_field_vectorized, trackFunction, OutOfDomainError as PyATOutOfDomainError,
)

ROOT = Path(__file__).resolve().parents[1]


def linear_grid():
    """Fields in T affine in x/y/z in mm: trilinear interpolation is exact."""
    x, y, z = np.meshgrid([-50., 0., 50.], [-50., 50.], [-300., 0., 300.], indexing="ij")
    return np.stack((x + 2*y + 3*z, 2*x - y + z, x - z), axis=-1)


def write_kickmap(tmp_path, *, length="0.525", nx="2", ny="2", x1=(-1, 1),
                  x2=(-1, 1), y1=(-2, 2), y2=(-2, 2), values=(1, 3, 5, 7)):
    def section(x, y):
        return ' '.join(map(str, (*x, y[0], *values[:2], y[1], *values[2:])))
    path = tmp_path / 'kick.txt'
    path.write_text(f'{length} {nx} {ny} START {section(x1, y1)} START {section(x2, y2)}\n')
    return path


@pytest.mark.parametrize('axis', range(3))
@pytest.mark.parametrize('side', (0, 1))
def test_every_3d_face_and_immediately_outside(axis, side):
    grid = linear_grid()
    bounds = ((-50., 50.), (-50., 50.), (-300., 300.))
    point = [0., 0., 0.]
    point[axis] = bounds[axis][side]
    for evaluate in (lambda *p: interpolate_3d_field_vectorized(grid, *p),
                     lambda *p: interpolate_field_vectorized(grid, *p)):
        assert np.all(np.isfinite(evaluate(*point)))
        outside = point.copy()
        outside[axis] = np.nextafter(point[axis], -np.inf if side == 0 else np.inf)
        with pytest.raises((OutOfDomainError, PyATOutOfDomainError)):
            evaluate(*outside)
    fmap = NKMFieldMap3D(grid)
    meters = np.array(point) / 1000
    assert np.all(np.isfinite(fmap.evaluate(*meters)))
    meters[axis] = np.nextafter(meters[axis], -np.inf if side == 0 else np.inf)
    with pytest.raises(OutOfDomainError):
        fmap.evaluate(*meters)
    assert fmap.domain_bounds['z'] == (-.3, .3)


@pytest.mark.parametrize('axis', range(2))
@pytest.mark.parametrize('side', (0, 1))
def test_every_2d_face_and_immediately_outside(tmp_path, axis, side):
    fmap = NKMKickMap2D(write_kickmap(tmp_path))
    point = [0., 0.]
    point[axis] = ((-1., 1.), (-2., 2.))[axis][side]
    assert np.all(np.isfinite(fmap.evaluate(*point)))
    point[axis] = np.nextafter(point[axis], -np.inf if side == 0 else np.inf)
    with pytest.raises(OutOfDomainError):
        fmap.evaluate(*point)


@pytest.mark.parametrize('side', (0, 1))
def test_1d_boundaries_and_two_node_linear_map(side):
    fmap = NKMFieldMap1D([-1., 1.], [-2., 2.])
    point = (-1., 1.)[side]
    assert fmap.evaluate(point) == point * 2
    with pytest.raises(OutOfDomainError):
        fmap.evaluate(np.nextafter(point, -np.inf if side == 0 else np.inf))
    with pytest.raises(ValueError, match='four nodes'):
        fmap.evaluate(0, method='cubic')
    with pytest.raises(ValueError, match='method'):
        fmap.evaluate(0, method='unknown')
    assert validate_1d_fieldmap([-1., 1.], [-2., 2.])['valid']


@pytest.mark.parametrize('shape', ((2, 2, 2), (2, 2, 2, 2), (1, 2, 2, 3), (2, 0, 2, 3)))
def test_malformed_3d_shapes(shape):
    for make in (NKMFieldMap3D, lambda grid: interpolate_field_vectorized(grid, 0, 0, 0)):
        with pytest.raises(ValueError, match='shape'):
            make(np.zeros(shape))


@pytest.mark.parametrize('value', (np.nan, np.inf, -np.inf))
def test_nonfinite_fields_and_queries_always_rejected(tmp_path, value):
    grid = linear_grid()
    grid[0, 0, 0, 0] = value
    with pytest.raises(ValueError, match='finite'):
        NKMFieldMap3D(grid)
    with pytest.raises(ValueError, match='finite'):
        load_2d_kickmap(write_kickmap(tmp_path, values=(value, 3, 5, 7)))
    for allow in (False, True):
        one = NKMFieldMap1D([-1, 1], [-2, 2], allow_extrapolation=allow)
        two = NKMKickMap2D(write_kickmap(tmp_path), allow_extrapolation=allow)
        three = NKMFieldMap3D(linear_grid(), allow_extrapolation=allow)
        with pytest.raises(ValueError, match='finite'):
            one.evaluate(value)
        for axis in range(2):
            point = [0., 0.]; point[axis] = value
            with pytest.raises(ValueError, match='finite'):
                two.evaluate(*point)
        for axis in range(3):
            point = [0., 0., 0.]; point[axis] = value
            with pytest.raises(ValueError, match='finite'):
                three.evaluate(*point)
    for policy in ('raise', 'clip', 'extrapolate'):
        with pytest.raises(ValueError, match='finite'):
            interpolate_field_vectorized(linear_grid(), value, 0, 0, boundary_policy=policy)


@pytest.mark.parametrize('kwargs', [
    {'length':'0'}, {'length':'-1'}, {'length':'nan'}, {'length':'inf'},
    {'nx':'1'}, {'ny':'0'}, {'nx':'2.5'},
    {'x1':(1, -1)}, {'x1':(1, 1)}, {'x1':(0, np.nan)},
    {'y1':(2, -2)}, {'y1':(2, 2)}, {'y1':(0, np.inf)},
    {'x2':(-1, 2)}, {'y2':(-2, 3)},
])
def test_invalid_kickmap_headers_axes_and_section_agreement(tmp_path, kwargs):
    with pytest.raises(ValueError):
        load_2d_kickmap(write_kickmap(tmp_path, **kwargs))


@pytest.mark.parametrize('change', ('empty', 'truncate', 'extra', 'extra_start', 'missing_start'))
def test_malformed_kickmap_token_counts(tmp_path, change):
    path = write_kickmap(tmp_path)
    text = path.read_text()
    if change == 'empty': text = ''
    elif change == 'truncate': text = ' '.join(text.split()[:-1])
    elif change == 'extra': text += ' 9'
    elif change == 'extra_start': text += ' START'
    else: text = text.replace('START', '', 1)
    path.write_text(text)
    with pytest.raises(ValueError):
        load_2d_kickmap(path)


@pytest.mark.parametrize('axis, values', [
    ([], []), ([0], [0]), ([[0, 1]], [[0, 1]]), ([0, 1], [0]),
    ([0, 0], [1, 2]), ([1, 0], [1, 2]), ([0, np.nan], [0, 1]),
    ([0, 1], [0, np.inf]),
])
def test_invalid_1d_maps_and_quadrature(axis, values):
    with pytest.raises(ValueError):
        NKMFieldMap1D(axis, values)
    with pytest.raises(ValueError):
        integrate_longitudinal_field(axis, values)


@pytest.mark.parametrize('bounds', ((0, 0), (1, -1), (0, np.inf), (0, np.nan), (0, 1, 2)))
def test_invalid_3d_ranges(bounds):
    with pytest.raises(ValueError):
        NKMFieldMap3D(linear_grid(), z_range_m=bounds)


def test_broadcast_interpolation_is_exact_for_affine_fields(tmp_path):
    grid = linear_grid()
    x = np.array([[-40.], [20.]])
    y = np.array([-30., 0., 40.])
    z = 100.
    expected = (x + 2*y + 3*z, 2*x - y + z, np.broadcast_to(x-z, (2, 3)))
    evaluators = (lambda: interpolate_3d_field_vectorized(grid, x, y, z),
                  lambda: interpolate_field_vectorized(grid, x, y, z),
                  lambda: NKMFieldMap3D(grid).evaluate(x/1000, y/1000, z/1000))
    for evaluate in evaluators:
        for actual, target in zip(evaluate(), expected):
            np.testing.assert_allclose(actual, target, rtol=0, atol=1e-12)
    # Scalar first coordinate was previously incompatible with array y/z.
    assert interpolate_3d_field_vectorized(grid, 0, y, 0)[0].shape == (3,)
    two = NKMKickMap2D(write_kickmap(tmp_path))
    for actual in two.evaluate(np.array([[-1.], [1.]]), [-2., 0., 2.]):
        np.testing.assert_allclose(actual, [[1, 3, 5], [3, 5, 7]], rtol=0, atol=1e-12)
    assert two.evaluate(0, [-2, 0, 2])[0].shape == (3,)
    assert isinstance(two.evaluate(0, 0)[0], float)
    for evaluate in (lambda: two.evaluate([0, 1], [0, 1, 2]),
                     lambda: interpolate_3d_field_vectorized(grid, [0, 1], [0, 1, 2], 0)):
        with pytest.raises(ValueError, match='broadcast') as error:
            evaluate()
        assert not isinstance(error.value, OutOfDomainError)


def test_explicit_boundary_policies(tmp_path):
    grid = linear_grid()
    assert interpolate_3d_field_vectorized(grid, 60, 0, 0, boundary_policy='clip') == (50, 100, 50)
    np.testing.assert_allclose(interpolate_3d_field_vectorized(grid, 60, 0, 0, boundary_policy='extrapolate'), (60, 120, 60), rtol=0, atol=1e-12)
    np.testing.assert_allclose(NKMFieldMap3D(grid, allow_extrapolation=True).evaluate(.06, 0, 0), (60, 120, 60), atol=1e-12)
    with pytest.raises(ValueError, match='boundary_policy'):
        interpolate_3d_field_vectorized(grid, 0, 0, 0, boundary_policy='unknown')
    assert NKMFieldMap1D([-1, 1], [-2, 2], allow_extrapolation=True).evaluate(2) == 4
    assert NKMKickMap2D(write_kickmap(tmp_path), allow_extrapolation=True).evaluate(2, 0) == (6., 6.)


def test_text_loader_preserves_sorting_and_supports_csv(tmp_path):
    path = tmp_path / 'field.csv'
    path.write_text('1,2\n-1,-2\n')
    x, by = load_1d_fieldmap(path)
    np.testing.assert_array_equal(x, [-1, 1])
    np.testing.assert_array_equal(by, [-2, 2])
    for content in ('0 1\n0 2\n', '0 1\n1 nan\n', '0\n1\n', '0 1 2\n1 2 3\n'):
        path.write_text(content)
        with pytest.raises(ValueError):
            load_1d_fieldmap(path)


def test_standalone_pyat_copy_and_patch_match_shared_source(tmp_path):
    # Exercise the installed relative import without importing the NKM package.
    package = tmp_path / 'standalone_integrators'
    package.mkdir()
    (package / '__init__.py').write_text('')
    for source, target in ((ROOT/'src/nkm_injection/_fieldmap_validation.py', '_nkm_fieldmap.py'),
                           (ROOT/'patches/pyat_extensions/pyat/at/integrators/pyNKMPass.py', 'pyNKMPass.py')):
        shutil.copyfile(source, package / target)
        patch = (ROOT/'patches/accelerator_toolbox_nkm.patch').read_text()
        section = patch.split(f'+++ b/pyat/at/integrators/{target}\n', 1)[1].split('diff --git', 1)[0]
        reconstructed = '\n'.join(line[1:] for line in section.splitlines() if line.startswith('+')) + '\n'
        assert reconstructed == source.read_text()
    spec = importlib.util.spec_from_file_location('standalone_integrators', package/'__init__.py', submodule_search_locations=[str(package)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        from standalone_integrators.pyNKMPass import interpolate_field_vectorized as standalone
        np.testing.assert_allclose(standalone(linear_grid(), 10, 20, 30), (140, 30, -20), atol=1e-12)
        with pytest.raises(ValueError, match='outside'):
            standalone(linear_grid(), 0, 0, 301)
    finally:
        for name in list(sys.modules):
            if name.startswith('standalone_integrators'):
                del sys.modules[name]


def test_pyat_preserves_lost_particles_and_rejects_live_outside():
    from types import SimpleNamespace
    elem = SimpleNamespace(Length=.525, Nslice=10, Energy=4., FieldMap=np.zeros((2, 2, 2, 3)))
    particles = np.zeros((6, 2))
    particles[0, 1] = np.nan
    original_lost = particles[:, 1].copy()
    result = trackFunction(particles, elem)
    np.testing.assert_allclose(result[:, 0], 0, atol=1e-14)
    np.testing.assert_array_equal(result[:, 1], original_lost)
    particles[0, 0] = .051
    with pytest.raises(PyATOutOfDomainError):
        trackFunction(particles, elem)
