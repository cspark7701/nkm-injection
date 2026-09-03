"""
Unit and Integration Tests for Milestone 3 NKM Field Map Ingestion & Validation
"""

import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.nkm_injection.fieldmap import (
    load_1d_fieldmap,
    validate_1d_fieldmap,
    BaseFieldMap,
    NKMFieldMap1D,
    integrate_longitudinal_field,
    OutOfDomainError
)
from src.nkm_injection.kickmap import (
    load_2d_kickmap,
    NKMKickMap2D
)


@pytest.fixture
def by_txt_path():
    p = REPO_ROOT / "By.txt"
    assert p.is_file(), f"By.txt missing at {p}"
    return p


@pytest.fixture
def excel_path():
    p = REPO_ROOT / "nkm_field.xlsx"
    assert p.is_file(), f"nkm_field.xlsx missing at {p}"
    return p


@pytest.fixture
def kickmap_path():
    p = REPO_ROOT / "kickmap_file.txt"
    assert p.is_file(), f"kickmap_file.txt missing at {p}"
    return p


def test_1d_fieldmap_loading_and_validation(by_txt_path, excel_path):
    """Test loading and validating 1D field maps."""
    x_by, by_vals = load_1d_fieldmap(by_txt_path)
    assert len(x_by) == 201
    val_by = validate_1d_fieldmap(x_by, by_vals)
    assert val_by["valid"] is True
    assert pytest.approx(val_by["peak_by_T"], abs=1e-3) == 0.146

    x_ex, by_ex = load_1d_fieldmap(excel_path)
    assert len(x_ex) == 51
    val_ex = validate_1d_fieldmap(x_ex, by_ex)
    assert val_ex["valid"] is True


def test_1d_interpolation_accuracy(by_txt_path):
    """Verify 1D interpolation reproduces tabulated source data points."""
    x_by, by_vals = load_1d_fieldmap(by_txt_path)
    fmap = NKMFieldMap1D(x_by, by_vals)
    
    by_interp = fmap.evaluate(x_by, method='linear')
    max_err = float(np.max(np.abs(by_interp - by_vals)))
    assert max_err < 1e-12


def test_1d_out_of_domain_protection(by_txt_path):
    """Verify that silent extrapolation is disabled by default."""
    x_by, by_vals = load_1d_fieldmap(by_txt_path)
    fmap = NKMFieldMap1D(x_by, by_vals, allow_extrapolation=False)
    
    with pytest.raises(OutOfDomainError):
        fmap.evaluate(0.10)  # x=100mm is outside [-50mm, 50mm]


def test_1d_symmetry_residuals(by_txt_path):
    """Verify odd symmetry residual for By.txt."""
    x_by, by_vals = load_1d_fieldmap(by_txt_path)
    val = validate_1d_fieldmap(x_by, by_vals)
    assert val["odd_symmetry_residual_T"] is not None
    assert val["odd_symmetry_residual_T"] < 1e-6


def test_2d_kickmap_loading_and_properties(kickmap_path):
    """Test 2D kick map parsing and dimension verification."""
    length_m, x_grid, y_grid, kx_map, ky_map = load_2d_kickmap(kickmap_path)
    assert length_m == 0.525
    assert len(x_grid) == 201
    assert len(y_grid) == 201
    assert kx_map.shape == (201, 201)
    assert ky_map.shape == (201, 201)


def test_2d_grid_interpolation_accuracy(kickmap_path):
    """Verify 2D interpolation error at grid nodes is zero."""
    kmap = NKMKickMap2D(kickmap_path)
    max_err = kmap.verify_grid_interpolation()
    assert max_err < 1e-12


def test_2d_out_of_domain_protection(kickmap_path):
    """Verify that silent extrapolation is disabled by default."""
    kmap = NKMKickMap2D(kickmap_path, allow_extrapolation=False)
    with pytest.raises(OutOfDomainError):
        kmap.evaluate(0.10, 0.0)  # 100 mm is outside [-50mm, 50mm]


def test_2d_symmetry_residuals(kickmap_path):
    """Verify 2D Kx and Ky odd symmetry residuals across x-y domain."""
    kmap = NKMKickMap2D(kickmap_path)
    sym = kmap.compute_symmetry_residuals()
    assert sym["kx_odd_x_symmetry_residual"] < 1e-6
    assert sym["ky_odd_y_symmetry_residual"] < 1e-6


def test_lorentz_kick_sign(kickmap_path):
    """Verify sign of Lorentz force kick at off-axis position."""
    kmap = NKMKickMap2D(kickmap_path)
    lorentz = kmap.verify_lorentz_kick_sign(x_offset_m=-0.010)
    assert lorentz["sign_verified"] is True
    assert lorentz["kx_value"] < 0.0  # negative kick for x < 0 in injection region


def test_base_fieldmap_inheritance_and_hashing(by_txt_path, kickmap_path):
    """Verify BaseFieldMap inheritance, domain bounds property, and file hash verification."""
    x_by, by_vals = load_1d_fieldmap(by_txt_path)
    fmap = NKMFieldMap1D(x_by, by_vals, filepath=by_txt_path)
    kmap = NKMKickMap2D(kickmap_path)

    assert isinstance(fmap, BaseFieldMap)
    assert isinstance(kmap, BaseFieldMap)

    assert "x" in fmap.domain_bounds
    assert "x" in kmap.domain_bounds and "y" in kmap.domain_bounds

    # Check SHA-256 hash verification
    expected_by_hash = "fa7be11ac01ab09826c997a7855050aa533c9ad5a2478684463dd9afaabcc305"
    assert fmap.verify_file_hash(expected_by_hash) is True

    expected_kick_hash = "5c1a3f1437cec79917515eb13443fc176550b9040553811b644db02412c2e42b"
    assert kmap.verify_file_hash(expected_kick_hash) is True


def test_integrate_longitudinal_field():
    """Test direct 1D longitudinal numerical quadrature along z."""
    z = np.linspace(-0.2625, 0.2625, 201)
    # Gaussian field profile By(z) = B0 * exp(-(z/w)^2)
    B0 = 0.146
    w = 0.10
    by = B0 * np.exp(-((z / w) ** 2))

    int_simpson = integrate_longitudinal_field(z, by, method="simpson")
    int_trapz = integrate_longitudinal_field(z, by, method="trapezoid")

    # Analytical integral B0 * sqrt(pi) * w * erf(0.2625 / 0.10) ~ 0.146 * 0.177245 * 0.99977 ~ 0.02587 T*m
    expected_int = float(B0 * np.sqrt(np.pi) * w * scipy_erf(0.2625 / w))
    assert pytest.approx(int_simpson, rel=1e-4) == expected_int
    assert pytest.approx(int_trapz, rel=1e-4) == expected_int


def scipy_erf(x):
    from scipy.special import erf
    return erf(x)


# ---------------------------------------------------------------------------
# Task 15 — 3D Field Map Vectorized Interpolation and pyNKMPass Tests
# ---------------------------------------------------------------------------

from src.nkm_injection.fieldmap import interpolate_3d_field_vectorized, NKMFieldMap3D
from src.nkm_injection.units import FieldMap3DProtocol
from patches.pyat_extensions.pyat.at.integrators.pyNKMPass import (
    trackFunction as pyNKMPass_track,
    interpolate_field_vectorized as pyNKMPass_interp
)


def test_3d_field_vectorized_interpolation_single_vs_batch():
    """Verify single-particle vs batch-vectorized 3D field interpolation precision (< 1e-12)."""
    nx, ny, nz = 11, 11, 21
    x_grid = np.linspace(-50, 50, nx)
    y_grid = np.linspace(-50, 50, ny)
    z_grid = np.linspace(-300, 300, nz)

    # Create synthetic 3D field: Bx = y, By = B0 * exp(-x^2), Bz = z/1000
    X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid, indexing='ij')
    field_map = np.zeros((nx, ny, nz, 3))
    field_map[..., 0] = Y * 1e-3
    field_map[..., 1] = 0.146 * np.exp(-((X / 15.0) ** 2))
    field_map[..., 2] = Z * 1e-4

    # 1. Exact node interpolation test
    bx_node, by_node, bz_node = interpolate_3d_field_vectorized(
        field_map, x_grid[5], y_grid[5], z_grid[10]
    )
    assert pytest.approx(bx_node, abs=1e-12) == field_map[5, 5, 10, 0]
    assert pytest.approx(by_node, abs=1e-12) == field_map[5, 5, 10, 1]
    assert pytest.approx(bz_node, abs=1e-12) == field_map[5, 5, 10, 2]

    # 2. Batch vs single-point comparison
    rng = np.random.default_rng(42)
    test_x = rng.uniform(-40, 40, size=50)
    test_y = rng.uniform(-40, 40, size=50)
    test_z = rng.uniform(-250, 250, size=50)

    # Batch evaluation
    bx_batch, by_batch, bz_batch = interpolate_3d_field_vectorized(
        field_map, test_x, test_y, test_z
    )

    # Point-by-point evaluation
    bx_single = np.zeros(50)
    by_single = np.zeros(50)
    bz_single = np.zeros(50)
    for i in range(50):
        bx_single[i], by_single[i], bz_single[i] = interpolate_3d_field_vectorized(
            field_map, test_x[i], test_y[i], test_z[i]
        )

    np.testing.assert_allclose(bx_batch, bx_single, atol=1e-14)
    np.testing.assert_allclose(by_batch, by_single, atol=1e-14)
    np.testing.assert_allclose(bz_batch, bz_single, atol=1e-14)


def test_nkm_fieldmap_3d_class_and_protocol():
    """Verify NKMFieldMap3D conforms to FieldMap3DProtocol."""
    nx, ny, nz = 11, 11, 21
    field_map = np.zeros((nx, ny, nz, 3))
    field_map[..., 1] = 0.146  # Uniform By = 0.146 T

    fmap3d = NKMFieldMap3D(field_map)
    assert isinstance(fmap3d, FieldMap3DProtocol)

    x = np.array([-0.010, 0.0, 0.010])
    y = np.array([0.0, 0.005, -0.005])
    by, bx = fmap3d(x, y, z=0.0)

    np.testing.assert_allclose(by, 0.146)
    np.testing.assert_allclose(bx, 0.0)


def test_py_nkm_pass_vectorized_tracking():
    """Verify pyNKMPass vectorized tracking gives identical results to single-particle tracking."""
    class DummyElem:
        Length = 0.525
        Nslice = 10
        Energy = 4.0
        FieldMap = np.zeros((11, 11, 21, 3))

    elem = DummyElem()
    elem.FieldMap[..., 1] = 0.146  # Uniform By = 0.146 T

    rng = np.random.default_rng(42)
    n_part = 20
    r_batch = np.zeros((6, n_part))
    r_batch[0, :] = rng.uniform(-0.020, 0.020, n_part)
    r_batch[1, :] = rng.uniform(-1e-3, 1e-3, n_part)
    r_batch[2, :] = rng.uniform(-0.010, 0.010, n_part)
    r_batch[3, :] = rng.uniform(-1e-3, 1e-3, n_part)

    # 1. Batch vectorized tracking
    r_out_batch = pyNKMPass_track(r_batch.copy(), elem)

    # 2. Individual particle tracking
    r_out_single = np.zeros_like(r_batch)
    for i in range(n_part):
        single_p = r_batch[:, i:i+1].copy()
        r_out_single[:, i:i+1] = pyNKMPass_track(single_p, elem)

    np.testing.assert_allclose(r_out_batch, r_out_single, atol=1e-14)



