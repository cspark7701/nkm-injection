# Milestone 166: Independent Transport and Optics Validation (Task B04)

**Completed:** 2026-10-13  
**Status:** Successfully Executed on branch `bts`.  
**Task Reference:** Task B04 in [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md).

---

## 1. Executive Summary

Milestone 166 completes the independent physical and numerical cross-validation of the transfer matrices, symplecticity conservation, uncoupled Twiss propagation, dispersion vectors, and element-by-element particle tracking engine for the Korea-4GSR BTS transfer line.

Transfer matrix symplecticity errors are verified to be at numerical precision ($2.44 \times 10^{-15}$ for $M_{44}$ and $2.07 \times 10^{-12}$ for $M_{66}$). Tracking simulations with $10,000$ and $100,000$ particles drawn from the design booster beam confirm that tracked beam sizes $\sigma_x, \sigma_y$ agree with linear transfer matrix theory within $< 0.4\%$ statistical precision with $100.0\%$ unperturbed transmission. Divergent particle loss tracking confirmed that physical aperture stations (`ap_rect` at $19.35\text{ mm}$ and `ap_rect2` at $30.00\text{ mm}$) properly intercept halo particles at their exact physical coordinates.

---

## 2. Key Accomplishments & Deliverables

1. **Transport Validation Report (`docs/paper_bts/transport_validation.md`)**:
   - Comprehensive documentation of 4D/6D transfer matrix symplecticity errors.
   - Numerical comparison between analytical covariance propagation ($\Sigma_{\text{out}} = M \Sigma_{\text{in}} M^T$) and element-by-element particle tracking across $10,000$ and $100,000$ particles.
   - Dispersion vector transformation audit and off-momentum tracking verification.
   - Physical aperture loss accounting proving that scraped particles are cleanly halted at the declared stations ($s = 0\text{ m}, 6.833\text{ m}, 11.761\text{ m}, 21.789\text{ m}$).

2. **Automated Regression Test Suite (`tests/test_bts_lattice.py`)**:
   - Implemented [`test_matrix_and_particle_tracking_envelope_consistency`](file:///home/cspark/Work/projects/nkm-injection/tests/test_bts_lattice.py#L128) verifying matrix-tracking covariance agreement within statistical tolerance.
   - Implemented [`test_physical_aperture_station_loss_accounting`](file:///home/cspark/Work/projects/nkm-injection/tests/test_bts_lattice.py#L164) verifying discrete aperture station interception.
   - Verified that all 11 unit and integration tests pass cleanly.

---

## 3. Verification and Standards Compliance

- **Protected Files Integrity:** All protected scientific data files remain untouched.
- **Git Branch:** Executed directly on branch `bts`.
- **Test Suite Status:** `pytest tests/test_bts_lattice.py tests/test_baseline.py -v` passed 16/16 tests.
