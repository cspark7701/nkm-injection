# Task: Update Notebook Kernelspec Metadata to pyat-dev

## Summary
- **Kernelspec Alignment**: Updated kernelspec metadata in `metadata.kernelspec` to `pyat-dev` (`name: "pyat-dev"`, `display_name: "pyat-dev"`) across non-protected Jupyter notebooks in the repository.
- **Protected File Preservation**: In accordance with user preference and `AGENTS.md` policy, protected scientific source notebooks (`NKM_radia.ipynb`, `NKM_radia_y=0.ipynb`, `storage_ring.ipynb`) were left unchanged.
- **Modified Tracked Notebooks**:
  - `notebooks/01_bts_main_simulation.ipynb`
  - `notebooks/02_multiturn_injection_validation.ipynb`
  - `notebooks/03_bts_moga_pareto.ipynb`
- **Verification**: Ran `pytest tests/test_paper_regression.py` (8 passed in 2.68s) and verified `git status`.
