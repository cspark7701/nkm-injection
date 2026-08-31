# Task 71: Create `accelerator-toolbox` Patch and Automated Installer

## Summary
- **Patch & Extension Isolation**:
  - Extracted and structured the custom Accelerator Toolbox (`pyAT`) extensions (`pyNKMPass` and `NonlinearKicker`) from `/home/cspark/Work/simulation_codes-working/accelerator_toolbox`.
  - Created [`patches/accelerator_toolbox_nkm.patch`](file:///home/cspark/Work/projects/nkm-injection/patches/accelerator_toolbox_nkm.patch) containing unified git diff for `pyat/at/integrators/__init__.py`, `pyat/at/integrators/pyNKMPass.py`, `pyat/at/lattice/elements/__init__.py`, and `pyat/at/lattice/elements/nonlinear_kicker.py`.
  - Stored standalone source files in [`patches/pyat_extensions/`](file:///home/cspark/Work/projects/nkm-injection/patches/pyat_extensions/).
  - Provided comprehensive documentation in [`patches/README.md`](file:///home/cspark/Work/projects/nkm-injection/patches/README.md).
- **Automated Installer Script**:
  - Created [`scripts/install_accelerator_toolbox.sh`](file:///home/cspark/Work/projects/nkm-injection/scripts/install_accelerator_toolbox.sh) to automatically apply the patch, register element/passmethod imports, and build `accelerator-toolbox` in editable mode with OpenMP multiprocessing enabled.
- **Verification**:
  - Successfully executed `./scripts/install_accelerator_toolbox.sh`.
  - Verified `import at; at.NonlinearKicker; from at.integrators import pyNKMPass` with `at.__version__ == 0.7.2.dev26+g4701d48c.d20260831`.
  - Updated [`docs/INSTALLATION.md`](file:///home/cspark/Work/projects/nkm-injection/docs/INSTALLATION.md#L68-L80) with pyAT setup instructions.
  - All protected scientific source data files remain clean and untampered.
