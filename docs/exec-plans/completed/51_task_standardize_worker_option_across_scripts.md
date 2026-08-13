# Task: Standardize Worker Option to `-w, --workers W` Across All Scripts

## Summary
- **CLI Option Standardization**: Replaced `-p, --parallel N` in [`scripts/run_full_production_simulation.sh`](file:///home/cspark/Work/projects/nkm/scripts/run_full_production_simulation.sh) with `-w, --workers W Number of parallel CPU worker cores`.
- **Python CLI Extensions**: Added `-w, --workers W` (`Number of parallel CPU worker cores`) to the `argparse` parsers of all executable python scripts:
  - [`scripts/reproduce_paper.py`](file:///home/cspark/Work/projects/nkm/scripts/reproduce_paper.py)
  - [`scripts/run_bts_moga.py`](file:///home/cspark/Work/projects/nkm/scripts/run_bts_moga.py)
  - [`scripts/run_multiturn_injection.py`](file:///home/cspark/Work/projects/nkm/scripts/run_multiturn_injection.py)
- **Verification**: Executed `--help` on all updated scripts and verified help menu formatting. All 8 paper regression tests passed cleanly.
- **Protected Files**: Verified via `git status` that all protected scientific data files remain untouched.
