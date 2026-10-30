# Milestone 266 — R4-BTS-04: scope of the boundary theorems

Completed: 2026-10-30. Round-4 task R4-BTS-04 (Reviewer 1 R3-BTS-01; Reviewer 2 R2C-05, "small residual").

**Article changes.**
- **Section 3.1.** The K-independence of the end-station clearance is restricted to the nominal, error-free,
  exactly matched line.
  - Under errors, Σ_out = M(K,e) Σ_in(e) M(K,e)ᵀ depends on K through gradient errors, rolls, chromatic transport
    and the entrance beta factors.
  - Restrictions upstream of q11 stay K-independent even with errors; downstream ones only nominally.
  - All error-study results transport the full perturbed covariance and centroid.
- **Section 3.2.** Eq. (6) is stated for the error-free, uncoupled, exactly matched line.
  - J is defined as the covariance of the non-dispersive part of the shot centroid; the momentum jitter is added
    through the dispersion.
  - "Steered static errors add a small residual" is replaced by the recorded effect: the static contributions raise
    the error-free loss by a factor of 1.8–2.6 (Table 7: 1.28 → 2.30 %, 1.16 → 2.27 %, 0.27 → 0.69 %).
- **Section 4.2.** The corrected spread of 0.68 mm / 0.37 mrad is compared with the error-free jitter of
  0.64 mm / 0.33 mrad. The static residual adds about 0.2 mm in quadrature, yet nearly doubles the loss.
- **Discussion.**
  - "Nominal beam size".
  - Static trajectory errors are "reduced", not removed; the horizontal residual, the optics errors and the
    uncorrected vertical trajectory remain.
  - The phase-only statement is limited to the nominal matched line.

**Computation.** None. The code already transported the perturbed covariance; only the interpretation changes.
The PDF is rebuilt in R4-BTS-09. Protected files are unchanged.
