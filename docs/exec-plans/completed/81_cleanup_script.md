# Milestone 81 — Task: Create cleanup.sh Script to Clean Output Folders

- **Author**: Chong Shik Park
- **Affiliation**: Department of Accelerator Science and Center for Accelerator Research, Korea University, Sejong, 30019 Republic of Korea
- **Date**: 2026-09-04

---

## Executive Summary

Created [`scripts/cleanup.sh`](file:///home/cspark/Work/projects/nkm-injection/scripts/cleanup.sh) in `scripts/` to provide a safe, convenient, and deterministic cleanup utility for generated simulation outputs, caches, and temporary build artifacts across the repository.

The script strictly enforces repository safeguards specified in `AGENTS.md`:
1. **Never deletes immutable protected scientific source data files** (`By.txt`, `kickmap_file.txt`, `K4GSR_HBIv4-1.mat`, `nkm_field.xlsx`, `nkm_field_expanded.xlsx`, `nlk.py`, `NKM_radia.ipynb`, `NKM_radia_y=0.ipynb`, `storage_ring.ipynb`).
2. **Never deletes baseline validation references** (`results/baseline/`).
3. Includes an automated integrity guard asserting that no protected file or baseline path can ever be staged for deletion.
4. Supports preview mode via `-d` / `--dry-run`, non-interactive execution via `-y` / `--yes`, and granular scopes (`--results`, `--cache`, `--all`).

---

## CLI Options & Usage

```bash
./scripts/cleanup.sh [OPTIONS]
```

| Flag | Long Option | Description |
| :--- | :--- | :--- |
| `-r` | `--results` | Clean simulation run outputs under `results/` (preserving `results/baseline/`) and untracked root simulation outputs. |
| `-c` | `--cache` | Clean Python bytecode caches (`__pycache__`, `*.pyc`), `.pytest_cache/`, and `.ipynb_checkpoints/`. |
| `-a` | `--all` | Clean all simulation runs, root temporary files, caches, and LaTeX build artifacts (`docs/jinst-paper/*.aux, *.log, *.bbl, ...`). |
| `-d` | `--dry-run` | Display files and folders identified for removal without performing deletions. |
| `-y` | `--yes` | Skip the interactive confirmation prompt (`[y/N]`). |
| `-h` | `--help` | Show command usage and documentation. |

---

## Verification & Safeguards

- Verified `./scripts/cleanup.sh --help` displays usage instructions.
- Verified `./scripts/cleanup.sh --dry-run` correctly identifies simulation output directories under `results/` and generated root files (`storage_ring_lattice_nkm.mat`), while strictly excluding `results/baseline/`.
- Verified `./scripts/cleanup.sh --cache --dry-run` targets `__pycache__` and `.pytest_cache/`.
- Verified `./scripts/cleanup.sh --all --dry-run` combines simulation outputs, caches, and LaTeX auxiliary files.
- Verified cryptographic integrity of all protected scientific data files via `scripts/inventory_protected_hashes.py` (`Verification SUCCESS: All protected file hashes match!`).
