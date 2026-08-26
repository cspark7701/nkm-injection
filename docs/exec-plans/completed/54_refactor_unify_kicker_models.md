# Task 54: Unify Analytical Kicker Models Across Tracking Modes (Task 02)

## Summary
- **Centralized Kicker Evaluator Factory**:
  - Created [`get_kicker_evaluator`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py#L174) in `src/nkm/storage_ring_injection.py` as the single source of truth for all 4 canonical kicker models:
    - **`off`**: Zero transverse kick ($\Delta x' = 0$, $\Delta y' = 0$).
    - **`ideal`**: Courant–Snyder optimal angle minimizing betatron invariant at nominal injection:
      $$\Delta x'_{\text{ideal}} = -\frac{\alpha_{x,\text{NKM}}}{\beta_{x,\text{NKM}}} \cdot x_{\text{inj}} \approx -0.1269\text{ mrad}$$
    - **`linear`**: Taylor expansion around RADIA field value at nominal injection position ($x_{\text{inj}} = -16.0\text{ mm}$):
      $$\Delta x'(x) = K_0 + K_1 \cdot (x_{\text{mm}} - X_{\text{ref,mm}}) = -2.1046 - 0.45043 \cdot (x_{\text{mm}} + 16.0)\text{ mrad}$$
    - **`fieldmap`**: Evaluated directly via `kickmap_obj.evaluate` with validated metadata.
- **Refactored Tracking Engines**:
  - Refactored [`track_multiturn_injection`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py#L249) to instantiate its kicker evaluator via `get_kicker_evaluator`.
  - Refactored [`track_element_resolved_injection`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py#L425) to instantiate its kicker evaluator via `get_kicker_evaluator`, eliminating legacy unphysical `-5.7491 mrad` hardcodings.
  - Refactored [`simulate_nkm_models`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/injection.py#L20) in `src/nkm/injection.py` to use `get_kicker_evaluator`.
- **Loss Accounting Vectorization**:
  - Vectorized aperture loss checking in `track_multiturn_injection` (`src/nkm/storage_ring_injection.py`), removing per-particle Python iterations when no losses occur.
- **Verification & Testing**:
  - Added unit tests [`test_get_kicker_evaluator_unification`](file:///home/cspark/Work/projects/nkm-injection/tests/test_storage_ring_injection.py#L114) and [`test_kicker_model_consistency_across_tracking_modes`](file:///home/cspark/Work/projects/nkm-injection/tests/test_storage_ring_injection.py#L144) to verify identical kick angles across tracking modes.
  - Ran full test suite: **163 passed out of 163 tests (100% pass rate)**.
  - Verified protected source data files remain clean and untampered.
