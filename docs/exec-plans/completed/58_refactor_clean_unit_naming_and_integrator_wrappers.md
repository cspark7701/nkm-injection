# Task 58: Clean Unit Naming, Legacy Integrator Wrappers, and Thread Safety (Task 06)

## Summary
- **Canonical SI Emittance Naming**:
  - Added canonical SI geometric emittance keys `emittance_x_m_rad` and `emittance_y_m_rad` ($\text{m}\cdot\text{rad}$) to [`compute_beam_statistics`](file:///home/cspark/Work/projects/nkm/src/nkm/beam.py#L87) in `src/nkm/beam.py` and [`TrackingResult`](file:///home/cspark/Work/projects/nkm/src/nkm/tracking.py#L23) in `src/nkm/tracking.py`, preserving `emittance_x_mrad` as a backward-compatible alias.
  - Updated [`BoosterExtractionConfig`](file:///home/cspark/Work/projects/nkm/src/nkm/end_to_end.py#L30) in `src/nkm/end_to_end.py` and [`BTSMOGAConfig`](file:///home/cspark/Work/projects/nkm/src/nkm/moga.py#L35) in `src/nkm/moga.py` to use `emit_x_m_rad` / `emittance_x_m_rad`.
- **Clarified Tracking Integrator Wrapper APIs**:
  - Added [`track_nkm_symplectic`](file:///home/cspark/Work/projects/nkm/src/nkm/tracking.py#L268) in `src/nkm/tracking.py` as an explicit alias for `track_nkm_thick_symplectic`.
  - Clarified documentation for legacy [`track_nkm_rk4`](file:///home/cspark/Work/projects/nkm/src/nkm/tracking.py#L290), noting delegation to 2nd-order symplectic integration for 1D profiles and directing users needing true 4th-order ODE integration to `track_nkm_thick_rk4`.
- **Thread-Safe Lattice Handling in Objectives**:
  - Extended [`BTSNormalizedObjectives`](file:///home/cspark/Work/projects/nkm/src/nkm/objectives.py#L50) `__init__` with `lattice` and `copy_lattice=True` parameters, enabling thread-safe evaluations without shared mutable state across workers.
- **Verification & Testing**:
  - Added unit tests [`test_canonical_emittance_naming_and_compatibility`](file:///home/cspark/Work/projects/nkm/tests/test_units.py#L190) and [`test_tracking_result_si_emittance`](file:///home/cspark/Work/projects/nkm/tests/test_units.py#L209) in `tests/test_units.py`.
  - Added [`test_track_nkm_symplectic_alias_and_legacy_rk4`](file:///home/cspark/Work/projects/nkm/tests/test_nkm_integrators.py#L126) in `tests/test_nkm_integrators.py`.
  - Verified all 21 tests in `tests/test_units.py`, `tests/test_nkm_integrators.py`, `tests/test_end_to_end.py`, and `tests/test_moga.py` pass.
  - Verified protected scientific source data files remain clean and untampered.
