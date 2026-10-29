# Milestone 260 — Rewrite setup.sh as a sourced environment loader

Completed: 2026-10-29 at the author's request to model `setup.sh` on `mobo-linac/setup.sh`.

## Change

The one-line `conda activate pyat-dev` script is replaced by a loader that:
- refuses direct execution and must be sourced;
- exports `PROJECT_ROOT`;
- enables `conda activate` when needed and activates `pyat-dev` (override with `NKM_INJECTION_ENV`), warning
  with the create/install commands if the environment or conda is missing;
- reports the active Python and checks that `nkm_injection` is imported from this checkout's `src/` (editable
  install), warning otherwise or when `PYTHONPATH` still contains `src`;
- does not modify the Python module search path and unsets its helper variables.

The ASTRA tool paths and `install.sh` of the template have no counterpart here and are omitted. The default
environment remains `pyat-dev`; `environment.yml` names `nkm-env`.

## Validation

- `bash -n setup.sh` passes; direct execution exits 1 with the sourcing message.
- Sourcing in a fresh interactive shell activates `pyat-dev` and reports the package at `src/nkm_injection`.
- Protected files unchanged.
