# Task: Fix GitHub Actions Release Workflow File-Hash Verification Step

## Summary
- **Root Cause Identified**: `.github/workflows/release-zenodo.yml` contained an invalid inline Python snippet that instantiated `PaperResultSchema()` without required arguments (`run_id` and `base_dir`) and called an un-implemented method `schema.compute_input_hashes()`.
- **Fix Applied**: Refactored step "Verify Protected Input File Hashes" in `.github/workflows/release-zenodo.yml` to import `compute_input_data_hashes` directly from `src.nkm.results_schema` and evaluate with `Path('.')`.
- **Local Verification**: Executed all CI workflow commands locally (`python3 scripts/record_baseline_metrics.py`, `python3 scripts/inventory_protected_hashes.py`, `python3 scripts/reproduce_paper.py`, and `pytest tests/test_paper_regression.py`). All 8 paper regression tests passed in 96.19s, and input hashes matched expected values.
- **Protected Files**: Verified via `git status` that all protected files remain unchanged.

## Checklist
- [x] Identify root cause of workflow failure in `.github/workflows/release-zenodo.yml`.
- [x] Update Python snippet to use correct `compute_input_data_hashes(Path('.'))` interface.
- [x] Run local verification of CI workflow steps.
- [x] Ensure protected scientific files are untouched.
