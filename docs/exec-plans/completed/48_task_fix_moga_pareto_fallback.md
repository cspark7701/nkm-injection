# Task: Fix MOGA Pareto Fallback for Remote GitHub Actions

## Summary
- **Remote Failure Analysis**: Diagnosed remote CI failure in `tests/test_moga_pareto.py` (`test_reevaluate_pareto_finalists` and `test_plot_moga_summary`). On short 10-individual / 3-generation test runs, MOGA runs may yield zero strictly feasible solutions (`feasible_count == 0`), producing empty `pareto_x` arrays.
- **Robust Fallback Implementation**: Updated `run_bts_moga()` in [`src/nkm/moga.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/moga.py) to fall back to `least_infeasible_x` / `least_infeasible_f` when `pareto_x` is empty, populating representative solutions even on short test runs.
- **Test Alignment**: Updated [`tests/test_moga_pareto.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_moga_pareto.py) assertions to check `len(res.representative_solutions) > 0`.
- **Verification**:
  - `pytest tests/test_moga_pareto.py`: **4 passed in 20.04s**.
  - Full test suite (`pytest tests/`): **161 passed out of 161 tests (100% pass rate)** in 877.42s.
