# Milestone 287 — R5-BTS-04: conclusions, baseline remnant and number formats

Completed: 2026-10-31. Round-5 task R5-BTS-04 (Reviewer 1 R1D-BTS-03; Reviewer 2 R2D-07 and R2D-08).

**Article.**
- **Low beta.**
  - "Leaves the loss unchanged" (Discussion) is replaced by the observed population-dependent differences: −0.21
    and −0.13 percentage points (steering, second test), and unresolved in the first test.
  - These differences are tied to its horizontal phase advance, about 1° smaller, which lowers the error-free loss
    from 1.28 % to 1.16 %. In the nominal model the vertical peak beta does not enter the horizontal blade loss.
  - Section 4.2 is reworded the same way.
- **Dispersion-free result.** "The dispersion-free results are analytic" became "the scan and its loss predictions
  are analytic, and its tracked test records a single lost particle".
- **Baseline remnant (Section 4.1).** "Thus optimization of the baseline BTS line improves nominal delivery" became
  "Matching is required for nominal delivery".
- **Dispersion-free angle jitter.** One source is used throughout: the scan setting's 393 µrad
  (`\BtsRFourFreeBestJxpUrad`) replaces the round-3 point's 394 µrad in Section 4.4.
- **Minus signs.** The round-3 interval macros in the first-test paragraph are wrapped in `\num`, so they print as
  mathematical minus signs. The round-5 tables already use `\num`.
- **Units.** The dispersion-free count is reported as a count, plus a fraction of 8.3 × 10⁻⁷ (R5-BTS-02); the percent
  mislabel is gone.
- **Table 9.** Every loss column now uses scientific notation, including the zero exponents
  (`export_bts_round4_assets.py`, `sci_all`).

The prose follows the humanizer rules. The isolated build is clean. Protected files are unchanged.
