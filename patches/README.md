# Accelerator Toolbox (`accelerator-toolbox` / `pyAT`) Custom Patches

This directory contains the custom extensions and patch for the **Accelerator Toolbox (`accelerator-toolbox` / `pyAT`)** to enable native 3D/2D field map tracking for the Nonlinear Kicker Magnet (`pyNKMPass` and `NonlinearKicker` element class).

---

## Patch Files

| File / Directory | Description |
| :--- | :--- |
| [`accelerator_toolbox_nkm.patch`](accelerator_toolbox_nkm.patch) | Unified Git patch file for `accelerator-toolbox` repository. |
| [`pyat_extensions/`](pyat_extensions/) | Standalone source files for `pyNKMPass.py` and `nonlinear_kicker.py`. |

---

## Included Extensions

1. **`pyNKMPass` Integration**:
   - Location in pyAT: `pyat/at/integrators/pyNKMPass.py`
   - Pure Python pass method supporting slice-by-slice 3D field map interpolation ($B_x, B_y, B_z$) and coordinate updates using AT coordinate conventions.
   - Automatically exported in `pyat/at/integrators/__init__.py`.

2. **`NonlinearKicker` Element**:
   - Location in pyAT: `pyat/at/lattice/elements/nonlinear_kicker.py`
   - Subclasses `at.Element` with default `PassMethod = 'pyNKMPass'`, supporting properties `Length`, `Energy`, `Nslice`, `Filename_in`, and `FieldMap`.
   - Exported in `pyat/at/lattice/elements/__init__.py`.

---

## How to Install `accelerator-toolbox` with the Patch

### Option A: Using the Automated Helper Script *(Recommended)*
```bash
# From the nkm-injection repository root:
./scripts/install_accelerator_toolbox.sh /path/to/accelerator_toolbox
```
If `/path/to/accelerator_toolbox` already exists locally (e.g. `/home/cspark/Work/simulation_codes-working/accelerator_toolbox`), the script will apply the patch and build `pyat` in editable mode with OpenMP optimization enabled.

### Option B: Manual Application
```bash
# 1. Navigate to your accelerator_toolbox repository
cd /path/to/accelerator_toolbox

# 2. Apply the patch
git apply /path/to/nkm-injection/patches/accelerator_toolbox_nkm.patch

# 3. Install pyat in editable mode with OpenMP
pip install --config-settings openmp=1 --config-settings omp_particle_threshold=4 -e ./pyat
```
