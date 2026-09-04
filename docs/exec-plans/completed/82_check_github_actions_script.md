# Milestone 82 — Task: Create Pre-Push GitHub Actions Validation Script

- **Author**: Chong Shik Park
- **Affiliation**: Department of Accelerator Science and Center for Accelerator Research, Korea University, Sejong, 30019 Republic of Korea
- **Date**: 2026-09-04

---

## Executive Summary

Implemented [`scripts/check_github_actions.sh`](file:///home/cspark/Work/projects/nkm-injection/scripts/check_github_actions.sh) to provide a local pre-push validation utility for all GitHub Actions CI workflows (`ci.yml`, `paper-regression.yml`, `release-zenodo.yml`).

This ensures full adherence to repository safeguards defined in `AGENTS.md` (local-only verification, zero remote API calls, zero pushes) before code is pushed to remote:
1. **Workflow Linting**: Parses and validates YAML schema structure of all `.github/workflows/*.yml` files.
2. **Protected Scientific File Integrity**: Verifies SHA-256 cryptographic hashes for all protected scientific source data files via `scripts/inventory_protected_hashes.py` and `src.nkm_injection.results_schema.compute_input_data_hashes()`.
3. **Baseline Metrics Verification**: Validates regeneration of baseline reference metrics (`scripts/record_baseline_metrics.py`).
4. **Paper Pipeline Reproduction**: Validates end-to-end data-driven paper pipeline reproduction without external dependencies (`scripts/reproduce_paper.py --no-pdf`).
5. **Test Suite Verification**: Supports fast pre-push checks (`-f, --fast` executing `tests/test_paper_regression.py`), targeted single workflow checks (`-w paper`, `-w ci`, `-w release`), and full Pytest execution.
6. **Post-Run Immutability Assertion**: Confirms that protected files remain completely untouched and identical to `results/baseline/protected_files_manifest.json`.

---

## CLI Options & Usage

```bash
./scripts/check_github_actions.sh [OPTIONS]
```

| Flag | Long Option | Description |
| :--- | :--- | :--- |
| `-w` | `--workflow W` | Select workflow to simulate: `all` (default), `ci`, `paper`, or `release`. |
| `-f` | `--fast` | Fast mode: validates YAML, hashes, and runs physics regression tests without the full test suite. |
| `-q` | `--quiet` | Suppress standard output logs for silent CI/pre-commit usage. |
| `-d` | `--dry-run` | Print all validation commands without executing them. |
| `-h` | `--help` | Show command usage and options. |

---

## Verification & Output

- Tested `./scripts/check_github_actions.sh --help` (displayed usage parameters).
- Tested `./scripts/check_github_actions.sh --dry-run` (simulated all checks cleanly).
- Tested `./scripts/check_github_actions.sh --fast` (all steps passed in ~12s).
- Tested `./scripts/check_github_actions.sh -w paper` (all steps and paper regression passed cleanly).
- Verified protected file hashes remained unmodified.
