# Task 70: Rename `src/nkm` to `src/nkm_injection`

## Summary
- **Python Source Package Rename**:
  - Renamed the source package directory from `src/nkm` to `src/nkm_injection` adhering to Python naming standards (valid module identifier).
  - Updated all Python import statements across:
    - 21 test files in `tests/` (`from nkm_injection...` / `import nkm_injection...`)
    - 18 script files in `scripts/`
    - CI workflows (`.github/workflows/release-zenodo.yml`)
    - Simulation notebooks in `notebooks/` (skipping protected reference files)
  - Reinstalled the package in editable mode via `pip install -e .` (`nkm-injection==0.2.0`).
- **Verification**:
  - Executed full test suite: **177/177 passed (100%)**.
  - All protected scientific source data files remain clean and untampered.
