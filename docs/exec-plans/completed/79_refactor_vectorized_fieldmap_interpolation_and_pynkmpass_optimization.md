# Milestone 79 — Task 15: Vectorized 3D Field Map Interpolation and PyNKMPass Optimization

## Executive Summary

Task 15 eliminates per-particle Python loop bottlenecks in `pyNKMPass` (the pure-Python Accelerator Toolbox nonlinear kicker pass method) and provides continuous, vectorized 3D trilinear magnetic field interpolation. By refactoring `pyNKMPass` to iterate over longitudinal slices in the outer loop and computing all $N$ macro-particles simultaneously with vectorized NumPy indexing and linear cell weights, per-turn tracking overhead is drastically reduced. In addition, `NKMFieldMap3D` and `interpolate_3d_field_vectorized` were added to `src/nkm_injection/fieldmap.py`, conforming to `FieldMap3DProtocol`.

---

## Key Achievements

### 1. Vectorized Trilinear 3D Field Interpolation
- **Location**: [`src/nkm_injection/fieldmap.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/fieldmap.py) and [`patches/pyat_extensions/pyat/at/integrators/pyNKMPass.py`](file:///home/cspark/Work/projects/nkm-injection/patches/pyat_extensions/pyat/at/integrators/pyNKMPass.py)
- **Features**:
  - `interpolate_3d_field_vectorized(field_map, x_mm, y_mm, z_mm, ...)`: Vectorized trilinear field interpolation computing normalized grid coordinate fractions and 8-corner linear weights ($c_{000} \dots c_{111}$) simultaneously across arbitrary arrays of particle coordinates without Python loops.
  - `NKMFieldMap3D(BaseFieldMap)`: Object-oriented 3D field map wrapper conforming to `FieldMap3DProtocol`, enabling direct integration into `SymplecticSplitIntegrator` and `LorentzRK4Integrator`.

### 2. Optimized `pyNKMPass` Pass Method
- **Location**: [`patches/pyat_extensions/pyat/at/integrators/pyNKMPass.py`](file:///home/cspark/Work/projects/nkm-injection/patches/pyat_extensions/pyat/at/integrators/pyNKMPass.py) and `/home/cspark/Work/simulation_codes-working/accelerator_toolbox/pyat/at/integrators/pyNKMPass.py`
- **Optimization**:
  - Inverted tracking loop: outer loop iterates over $N_{\text{slices}}$, inner operations compute all particles simultaneously via vectorized NumPy array slicing.
  - Replaced discontinuous step-function indexing (`searchsorted` truncation) with continuous trilinear interpolation.

### 3. Re-generated Unified AT Patch
- **Location**: [`patches/accelerator_toolbox_nkm.patch`](file:///home/cspark/Work/projects/nkm-injection/patches/accelerator_toolbox_nkm.patch)
- **Updates**: Re-generated unified git patch containing the optimized `pyNKMPass.py` implementation.

### 4. Expanded Test Suite
- **Location**: [`tests/test_fieldmap.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_fieldmap.py)
- **Tests Added**:
  - `test_3d_field_vectorized_interpolation_single_vs_batch`: Verified exact numerical match ($< 10^{-14}$) between point-by-point and batch-vectorized evaluations, as well as exact grid node interpolation ($< 10^{-12}$).
  - `test_nkm_fieldmap_3d_class_and_protocol`: Verified `isinstance(fmap3d, FieldMap3DProtocol)` and evaluated slice $(B_y, B_x)$ outputs.
  - `test_py_nkm_pass_vectorized_tracking`: Verified exact numerical agreement ($< 10^{-14}$) between batch-vectorized and sequential particle tracking in `pyNKMPass`.

---

## Verification & Status

- **Unit Test Suite**: 195/195 passing tests (+3 new tests added).
- **Protected Files Integrity**: Unchanged and verified against SHA-256 baseline.
