# Task: Fix plot_moga_summary Fallback for Empty Pareto Fronts

## Summary
- **Remote Log Failure Analysis**: Inspected GitHub Actions log for run `31664410778` (job `94335796874`). `test_plot_moga_summary` in `tests/test_moga_pareto.py` failed because `plot_moga_summary()` exited early (`if not result.success or len(result.pareto_f) == 0: return`) when `pareto_f` was empty on small test runs, causing no figure to be saved to `tmp_path`.
- **Fix Applied**: Updated `plot_moga_summary()` in [`src/nkm/moga.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/moga.py) to fall back to `least_infeasible_f` when `pareto_f` is empty.
- **Verification**:
  - `pytest tests/test_moga_pareto.py`: **4 passed in 9.95s**.
  - `pytest tests/`: **161 passed out of 161 tests (100% pass rate)** in 868.72s.
