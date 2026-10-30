# Milestone 265 — R4-BTS-03: exact round-aperture loss and valid bounds

Completed: 2026-10-30. Round-4 task R4-BTS-03 (Reviewer 1 R3-BTS-02; Reviewer 2 R2C-08, in part).

**Change.**
- **`bts_round3.ellipse_loss_probability`** gives the exact probability that a 2-D Gaussian (x, y) lies outside an
  ellipse. It uses a closed-form radial integral and the periodic trapezoidal rule in angle, and keeps full relative
  accuracy in the far tail.
- **`clearance_and_loss`** now treats round and elliptical apertures as one exact 2-D event. Rectangular and
  one-sided apertures remain one exact interval event per plane.
  - `loss_lower` is the largest event and `loss_union` the sum, a valid bracket for every aperture shape.
  - The chord at the other plane's centroid is kept only for the geometric five-sigma clearance.
  - `round_aperture='chord'` reproduces the round-3 projected probabilities.
- **Tests.** Three new tests:
  - a centred isotropic beam at a 5σ circle gives exp(−12.5) = 3.73 × 10⁻⁶, not 4Φ(−5) = 1.15 × 10⁻⁶;
  - an offset, correlated beam at an ellipse agrees with 2 × 10⁶ samples;
  - for a beam scraping a reduced round pipe, the tracked loss lies inside the bracket; chord mode is checked too.
- **Article.**
  - Section 3.3 states the exact treatment, the counterexample and the bracket.
  - "Within 1 %" now reads as relative agreement of the mean prediction per tracked row (Sections 4.2–4.4 and the
    Discussion).
  - A Gaussian-consistency caveat is added: it does not test non-Gaussian booster tails.

**Effect on the results.** All round-3 stages were rerun with the exact treatment in
`results/bts_round4_r403_exact_20261030`. `scripts/compare_bts_round3_campaigns.py` finds all 66 selected
observables bitwise identical to `results/bts_journal_campaign_r3b_20261015`, including the frozen loss-based
setting, the tracked losses and the union means. The round apertures (19.35 mm) contribute nothing at these beam
sizes. The correction is therefore methodological, and no installed number changes.

**Checks.** 16 round-3 tests pass; the full-suite result is recorded in R4-BTS-09. The PDF is rebuilt in R4-BTS-09.
Protected files are unchanged.
