# Task 59: Fix Remote GitHub Actions CI PyAT Element Tracking Energy Bug

## Summary
- **Remote CI Failure Root Cause**:
  - Inspected GitHub Actions workflow run `31778780768` ("CI Workflow").
  - In Python 3.11 on standard `accelerator-toolbox` wheels, element-by-element tracking through multipole elements with radiation pass methods (`StrMPoleSymplectic4RadPass`, e.g. quadrupole `QH1`) requires `energy` to be passed to `_element_pass()`.
  - In [`src/nkm/storage_ring_injection.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py#L500), `track_element_resolved_injection` invoked `elem.track(current_beam)` without specifying the `energy` kwarg, triggering:
    ```
    ValueError: Energy needs to be defined. Check lattice parameters or pass method options.
    ```
    in `tests/test_end_to_end.py::test_end_to_end_pipeline_execution` and `tests/test_moga_pareto.py::test_reevaluate_pareto_finalists`.
- **Fix Implemented**:
  - Updated [`src/nkm/storage_ring_injection.py:L500`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py#L500) to pass `energy=config.energy_eV`:
    ```python
    res_elem = elem.track(current_beam, energy=config.energy_eV)
    ```
- **Verification**:
  - Ran `pytest tests/test_end_to_end.py tests/test_moga_pareto.py tests/test_storage_ring_injection.py -v`: all 11 tests passed.
  - Verified baseline metrics scripts and protected file manifest generators run cleanly without error.
  - Ensured all protected scientific data files remain clean and untampered.
