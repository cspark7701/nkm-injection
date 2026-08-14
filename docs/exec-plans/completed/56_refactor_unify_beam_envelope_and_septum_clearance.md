# Task 56: Unify Beam Envelope & Septum Clearance Calculations (Task 04)

## Summary
- **Unified Beam Envelope Calculation**:
  - Implemented [`compute_beam_envelope`](file:///home/cspark/Work/projects/nkm/src/nkm/optics.py#L166) in `src/nkm/optics.py` supporting both statistical RMS quadrature and conservative linear arithmetic methods:
    - **`rms_quadrature`**:
      $$\sigma_x(s) = \sqrt{\epsilon_x \beta_x(s) + \left(D_x(s) \sigma_\delta\right)^2}, \quad E_x(s) = n_\sigma \cdot \sigma_x(s)$$
    - **`conservative_linear`**:
      $$E_x(s) = n_\sigma \sqrt{\epsilon_x \beta_x(s)} + |D_x(s)| \sigma_\delta$$
- **Standardized Call Sites**:
  - Refactored [`compute_rms_envelope`](file:///home/cspark/Work/projects/nkm/src/nkm/results_schema.py#L203) in `src/nkm/results_schema.py` to delegate directly to `compute_beam_envelope(..., method="rms_quadrature")`.
  - Refactored [`check_aperture_margin`](file:///home/cspark/Work/projects/nkm/src/nkm/constraints.py#L320) in `src/nkm/constraints.py` to use `compute_beam_envelope(..., method="conservative_linear")`.
  - Refactored [`compute_true_aperture_margin`](file:///home/cspark/Work/projects/nkm/src/nkm/moga.py#L128) and [`reevaluate_pareto_finalists`](file:///home/cspark/Work/projects/nkm/src/nkm/moga.py#L139) in `src/nkm/moga.py` to use `compute_beam_envelope`.
- **Local Septum Optics Evaluation**:
  - Fixed [`check_septum_clearance`](file:///home/cspark/Work/projects/nkm/src/nkm/constraints.py#L477) in `src/nkm/constraints.py` to evaluate the beam envelope using local Twiss functions at the injection septum location (`sept_ex` near $s \ge 16.0\text{ m}$) instead of global peak beta across the entire transfer line.
- **Verification & Testing**:
  - Added [`TestUnifiedBeamEnvelopeAndSeptumClearance`](file:///home/cspark/Work/projects/nkm/tests/test_constrained_optimization.py#L518) in `tests/test_constrained_optimization.py`.
  - Verified 51 passed tests across `test_constrained_optimization.py`, `test_moga_pareto.py`, and `test_manifest_paper_pipeline.py`.
  - Verified protected source data files remain clean and untampered.
