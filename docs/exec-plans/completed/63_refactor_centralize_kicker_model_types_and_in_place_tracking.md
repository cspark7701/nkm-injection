# Task 63: Refactor — Centralize Kicker Model Types & Optimize Multi-Turn In-Place Tracking

## Summary
- **Refactor Objective (Task 09)**:
  - Centralized the canonical `KickerModelType` and `CANONICAL_KICKER_MODELS` definitions in [`src/nkm/units.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/units.py#L27) along with `validate_kicker_model()`.
  - Enforced kicker model string validation in `get_kicker_evaluator`, `track_multiturn_injection`, and `track_element_resolved_injection` in [`src/nkm/storage_ring_injection.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm/storage_ring_injection.py).
  - Optimized the multi-turn tracking loop in `track_multiturn_injection` by propagating coordinates in-place (`current_beam[:, valid_before] = M66 @ current_beam[:, valid_before]`), eliminating per-turn full-array heap re-allocations.
- **Verification & Regression Testing**:
  - Added [`test_validate_kicker_model`](file:///home/cspark/Work/projects/nkm-injection/tests/test_units.py#L230) in `tests/test_units.py` to verify acceptance of all 4 canonical models and rejection of invalid strings.
  - Ran `pytest tests/test_units.py tests/test_storage_ring_injection.py tests/test_convergence_study.py tests/test_injection.py -v`: 100% passed (37/37 tests).
  - All protected scientific source data files remain clean and untampered.
