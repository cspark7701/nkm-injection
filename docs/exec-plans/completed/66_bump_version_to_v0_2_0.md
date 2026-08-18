# Task 66: Bump Version to v0.2.0

## Summary
- **Version Bump**:
  - Incremented repository version from `0.1.0` to **`0.2.0`** across all metadata and configuration files to reflect the major pre-1.0 feature expansions and physics refactorings (Milestones 01–65).
- **Synchronized Files**:
  - [`pyproject.toml`](file:///home/cspark/Work/projects/nkm/pyproject.toml#L7): `version = "0.2.0"`
  - [`src/nkm/__init__.py`](file:///home/cspark/Work/projects/nkm/src/nkm/__init__.py#L3): `__version__ = "0.2.0"`
  - [`CITATION.cff`](file:///home/cspark/Work/projects/nkm/CITATION.cff#L7): `version: 0.2.0`, `date-released: 2026-08-18`
  - [`docs/index.html`](file:///home/cspark/Work/projects/nkm/docs/index.html#L42): `Version: v0.2.0 (latest)`
- **Verification**:
  - Reinstalled package in editable mode (`pip install -e .`) confirming `nkm==0.2.0`.
  - Ran unit tests: **100% passed**.
  - All protected scientific source data files remain clean and untampered.
