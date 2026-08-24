# NKM Reproducibility & Publication Release Guide

## 1. Overview

This repository contains the complete simulation, optics matching, thick-element tracking, error robustness analysis, and MOGA optimization pipeline for the Nonlinear Kicker Magnet (NKM) and BTS transfer line.

For the single-file comprehensive end-to-end simulation procedure and publication workflow specification, see:
[docs/SIMULATION_PROCEDURE_AND_PUBLICATION_WORKFLOW.md](file:///home/cspark/Work/projects/nkm/docs/SIMULATION_PROCEDURE_AND_PUBLICATION_WORKFLOW.md)

Every manuscript figure, table, and reported metric can be dynamically reproduced from a clean checkout using fixed random seeds and cryptographic input file verification.

---

## 2. Environment Setup & Dependency Locking

### Python Version
- Supported Python Version: **Python 3.10** or **Python 3.11**

### Installation
Clone the repository and install locked dependencies:

```bash
git clone https://github.com/nkm-injection/nkm-injection.git
cd nkm-injection
pip install -r requirements-lock.txt
pip install -e .[dev,moga]
```

---

## 3. Single-Command Publication Reproduction

To execute the data-driven paper pipeline and regenerate all figures, tables, and metrics:

```bash
python3 scripts/reproduce_paper.py
```

Outputs are saved under `results/paper/paper_run_<timestamp>/`.

---

## 4. Test Suite Execution

Run all 177 unit, integration, and paper regression tests:

```bash
pytest -v
```

---

## 5. Scientific Input Data Cryptographic Hashes

Authoritative input data files are protected against silent corruption:

- `By.txt`: SHA-256 verified at execution
- `kickmap_file.txt`: SHA-256 verified at execution
- `K4GSR_HBIv4-1.mat`: SHA-256 verified at execution
- `storage_ring_lattice_nkm.mat`: SHA-256 verified at execution
- `nkm_field.xlsx`: SHA-256 verified at execution
- `nkm_field_expanded.xlsx`: SHA-256 verified at execution

---

## 6. Notebook Visualization

Notebooks 01-03 include inline publication-quality visualization cells.
