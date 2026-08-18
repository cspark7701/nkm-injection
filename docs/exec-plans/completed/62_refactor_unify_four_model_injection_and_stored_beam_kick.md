# Task 62: Refactor — Unify 4-Model Injection Tracking & Fix Stored-Beam Closed-Orbit Kick

## Summary
- **Refactor Objective (Task 08)**:
  - Upgraded `simulate_nkm_models` in [`src/nkm/injection.py`](file:///home/cspark/Work/projects/nkm/src/nkm/injection.py#L20) to evaluate all 4 canonical kicker models (`nkm_off`, `nkm_ideal`, `nkm_linear`, `nkm_fieldmap`).
  - Fixed circulating beam tracking under the ideal kicker model to accurately simulate and expose stored-beam dipole perturbation.
  - Fixed closed-orbit stored beam kick calculation in [`src/nkm/robust_optimization.py`](file:///home/cspark/Work/projects/nkm/src/nkm/robust_optimization.py#L112) by evaluating the physical field map deflection $\Delta x'(x_{\text{co}} - \Delta x_{\text{nkm}}) \times (1 + \delta_B)$.
- **Key Code Modifications**:
  - In `src/nkm/injection.py`:
    - Tracked `inj_linear` and `circ_linear` via `get_kicker_evaluator("linear", config=config)`.
    - Applied `kick_ideal` to `circ_ideal` instead of zeroing with `kick_off`.
    - Added `nkm_linear` and `nkm_ideal` (with `nkm_idealized` backward-compatible alias) to output dictionary.
  - In `src/nkm/robust_optimization.py`:
    - Used `nkm_kick_fn` (from fieldmap or analytical model) to compute stored-beam kick across error realizations.
- **Verification & Regression Testing**:
  - Updated [`tests/test_injection.py`](file:///home/cspark/Work/projects/nkm/tests/test_injection.py) to assert stored beam perturbation under ideal dipole ($|\Delta x'_{\text{stored}}| > 0.1\text{ mrad}$) vs. fieldmap transparency ($|\Delta x'_{\text{stored}}| < 0.01\text{ mrad}$).
  - Updated [`tests/test_errors.py`](file:///home/cspark/Work/projects/nkm/tests/test_errors.py) to verify closed-orbit kick scaling and zero kick for on-axis stored beam.
  - Executed full test suite: **175/175 tests passed (100%)**.
  - All protected scientific source data files remain clean and untampered.
