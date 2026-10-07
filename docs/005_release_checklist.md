# NKM Reproducible Publication Release Checklist

## Pre-Release Verification

- [x] **Clean Checkout Test**: Verified repository clones cleanly and installs dependencies.
- [x] **Test Suite**: Run `pytest -v` (all **161 tests** passing 100%).
- [x] **Input Hashes**: Verified SHA-256 hashes of protected scientific input files (`By.txt`, `kickmap_file.txt`, `K4GSR_HBIv4-1.mat`, `nkm_field.xlsx`, `nkm_field_expanded.xlsx`).
- [x] **Single-Command Pipeline**: Run `python3 scripts/reproduce_paper.py [--manifest <path>] [-w N]` to confirm figure/table generation.
- [x] **Protected Files Integrity**: Verified all protected files (`NKM_radia.ipynb`, `nlk.py`, `storage_ring.ipynb`, etc.) are 100% clean and unmodified via `git status` and `git diff`.
- [x] **Metadata Alignment**: `LICENSE` (MIT), `CITATION.cff`, `README.md`, and `pyproject.toml` aligned.
- [x] **CI Workflows**: GitHub Actions workflows `.github/workflows/ci.yml`, `.github/workflows/paper-regression.yml`, and `.github/workflows/release-zenodo.yml` created and passing.
- [x] **Notebook Kernelspec**: All notebooks (`notebooks/01_*` through `notebooks/04_*`) configured with `pyat-dev` kernelspec.
- [x] **Notebook Visualizations**: Notebooks 01–03 include rich inline visualization cells (field maps, phase-space portraits, Pareto scatter matrices, BTS optics functions, dynamic aperture footprint, radar charts, hypervolume convergence).
- [x] **CLI Standardization**: All scripts use `-w, --workers W` (Number of parallel CPU worker cores) — replaces old `-p, --parallel N`.
- [x] **Baseline Manifest**: `results/baseline/protected_files_manifest.json` auto-generated on clean CI checkout by `validate_publication_manifest()`.
- [x] **MOGA Fallback**: `run_bts_moga()` and `plot_moga_summary()` correctly fall back to `least_infeasible_x/f` when no feasible Pareto solutions exist.
- [x] **Test Consolidation**: `tests/test_task08_error_model.py` consolidated into `tests/test_errors.py`.

## Tagging & Zenodo Release

1. Tag release candidate:
   ```bash
   git tag -a v0.1.0-rc1 -m "Release Candidate 1 for Journal Manuscript Submission"
   ```
2. Export source archive:
   ```bash
   git archive --format=zip --output=nkm-v0.1.0-rc1.zip v0.1.0-rc1
   ```
3. Zenodo Archival: Link GitHub repository to Zenodo for automatic DOI generation upon final tag push.
