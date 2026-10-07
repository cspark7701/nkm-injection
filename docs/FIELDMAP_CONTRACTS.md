# Field-map validation and interpolation contracts

All loaders read scientific inputs without modifying them. Parsing and grid validation finish before interpolators are constructed. Generated validation metrics and plots belong in a fresh results directory.

## Units and grid layout

| Interface | Coordinates | Values | Required grid |
| --- | --- | --- | --- |
| `load_1d_fieldmap`, `NKMFieldMap1D` | x in m | By in T | Matching 1-D arrays, at least two nodes |
| `integrate_longitudinal_field` | z in m | By in T, integral in T m | Matching 1-D arrays, at least two nodes |
| `load_2d_kickmap`, `NKMKickMap2D` | x/y and length in m | Raw file values; `evaluate_kick` converts to rad using metadata | Each component `(ny, nx)`, at least two nodes per axis |
| `NKMFieldMap3D` | x/y/z and range limits in m | `(Bx, By, Bz)` in T | Uniform grid `(nx, ny, nz, 3)`, at least two nodes per axis |
| `interpolate_3d_field_vectorized`, pyAT `interpolate_field_vectorized` | x/y/z and range limits in mm | `(Bx, By, Bz)` in T | Same 3-D layout |

Axes and values must be finite. Tabulated axes must be strictly increasing without duplicates. Uniform-grid bounds must have two finite, strictly increasing limits. The 1-D file loader retains its historical sorting of input rows; direct constructors and quadrature require increasing axes. Text/CSV 1-D files contain exactly two columns. Linear interpolation accepts two nodes; cubic interpolation requires four and raises a descriptive error when requested on a smaller grid.

The 2-D format requires a finite positive length, integer Nx/Ny, exactly two START sections and the exact number of grid values in each section. Both sections must carry identical x and y axes (exact numerical equality, without a tolerance). Existing section-to-component assignments and kick sign conventions are preserved. Default kick metadata remains mrad; raw evaluation performs no field-integral reinterpretation.

The 3-D class call interface still returns `(By, Bx)` for the tracking protocol; `evaluate` returns `(Bx, By, Bz)`.

## Query behavior and migration

Domains include both endpoints. A finite coordinate outside any face raises `OutOfDomainError`, a `ValueError` subclass, by default. This includes longitudinal z in 3-D. No boundary tolerance admits immediately outside values. NaN/Inf queries and incompatible coordinate shapes raise `ValueError`, even with extrapolation enabled.

Coordinate inputs follow NumPy broadcasting. Scalars mix with arrays, and `(n, 1)` and `(m,)` coordinates produce `(n, m)` output arrays. Scalar queries return scalar components. Shape errors are distinguished from domain errors.

`allow_extrapolation=True` explicitly enables extrapolation in all map classes. The 3-D implementation continues the edge cell linearly. Low-level 3-D helpers accept `boundary_policy="raise"` (default), `"extrapolate"` or `"clip"`. The clip policy explicitly requests the former nearest-boundary behavior. Production callers should normally retain the default and ensure tracked coordinates lie within map coverage.

Previously, the 3-D helper and pyAT extension silently clamped outside coordinates, including when the class had `allow_extrapolation=False`. Callers relying on that behavior must explicitly select `boundary_policy="clip"` at the low-level helper, or correct their coverage. The class's existing extrapolation flag now selects actual extrapolation. There are no saved-result schema changes.

## Shared pyAT implementation

`src/nkm_injection/_fieldmap_validation.py` contains the NumPy-only grid checks and trilinear interpolation. The installer copies it to pyAT as `at/integrators/_nkm_fieldmap.py`; the patch artifact contains the same source. The installed extension has no runtime dependency on the NKM package. Repository imports use the project's helper until installed. Reinstall the extensions to update an existing external pyAT checkout; Task 03 does not modify that checkout.

The pass validates its map once before slicing. AT particles already marked lost by NaN in x remain unchanged and are excluded from field queries. Finite live coordinates outside coverage raise. Tracking equations, field component order, rigidity signs and GeV/mm conversions remain unchanged.

## Verification

Run `pytest -q tests/test_fieldmap.py tests/test_fieldmap_contracts.py` and the full suite in the configured pyat-dev environment. Regressions cover every closed domain face and its immediately outside floating-point neighbor, malformed dimensions, finite values, duplicate/reversed axes, section agreement, broadcasting, explicit policies and the standalone extension copy.

Source-grid interpolation tolerances remain absolute error below `1e-12`; synthetic affine-field checks use `1e-12` with zero relative tolerance. Existing batch-versus-scalar interpolation and tracking checks retain `1e-14`. Source-map SHA-256 assertions remain unchanged.

A small clean-process check, separate from full production simulation, is:

```bash
MPLBACKEND=Agg python scripts/validate_nkm_fieldmap.py --output-dir results/task03_field_validation_new
```
