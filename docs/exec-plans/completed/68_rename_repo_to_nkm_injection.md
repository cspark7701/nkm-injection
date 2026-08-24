# Task 68: Update Repository Name and URLs to `nkm-injection`

## Summary
- **Repository Rename**:
  - Updated all package metadata, URLs, setup scripts, and documentation across the codebase to reflect the repository name **`nkm-injection`** under the **`nkm-injection`** GitHub organization (`https://github.com/nkm-injection/nkm-injection`).
- **Updated Files**:
  - [`pyproject.toml`](file:///home/cspark/Work/projects/nkm/pyproject.toml#L7): `name = "nkm-injection"`
  - [`CITATION.cff`](file:///home/cspark/Work/projects/nkm/CITATION.cff#L6): `title = "NKM-Injection: ..."` and `url = "https://github.com/nkm-injection/nkm-injection"`
  - [`README.md`](file:///home/cspark/Work/projects/nkm/README.md#L1): Updated header title and clone instructions.
  - [`docs/INSTALLATION.md`](file:///home/cspark/Work/projects/nkm/docs/INSTALLATION.md#L21): Updated setup script URL and git clone paths.
  - [`docs/reproducibility.md`](file:///home/cspark/Work/projects/nkm/docs/reproducibility.md#L23): Updated git clone paths.
  - [`scripts/setup_environment.sh`](file:///home/cspark/Work/projects/nkm/scripts/setup_environment.sh#L8): `REPO_URL = "https://github.com/nkm-injection/nkm-injection.git"`, `TARGET_DIR = "nkm-injection"`.
  - [`docs/index.html`](file:///home/cspark/Work/projects/nkm/docs/index.html#L47) & [`docs/site/index.html`](file:///home/cspark/Work/projects/nkm/docs/site/index.html#L47): Updated repository button links to `https://github.com/nkm-injection/nkm-injection`.
  - [`scripts/sync_site.sh`](file:///home/cspark/Work/projects/nkm/scripts/sync_site.sh): Synced updated site bundle to `/home/cspark/Work/simulation_codes-working/nkm-injection.github.io/`.
- **Verification**:
  - Reinstalled package in editable mode (`pip install -e .` -> `nkm-injection==0.2.0`).
  - Ran unit test suite (`pytest tests/test_units.py -v`): 100% passed (12/12 tests).
  - All protected scientific source data files remain clean and untampered.
