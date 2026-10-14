# Milestone 223 — Reviewer 2, round-4 report

Completed: 2026-10-15. Pre-submission review of the round-3 manuscript (commit `4b30e09`), written as Reviewer 2.

**Output.** `docs/paper/reviews/reviewer2_report_round4.md` (new; earlier reports unchanged) and a reviews index entry.

**Recommendation.** Major revision of limited scope; no acceptance in the present form. Acceptance expected after
R2d-1 to R2d-3. All round-3 tasks R2c-1 to R2c-9 are recorded as answered; R2c-3 met as specified but insufficient,
R2c-4's boundary criterion partly unmet (28 % of tuned machines on the outer x_inj bound).

**Findings checked against the campaign-04 artifacts.**
- Paired jitter scan: booster jitter costs NKM −20.6 and dipole −20.3 points; the NKM − dipole gap is −28.4 at zero
  and −28.7 at full jitter. The abstract's "chiefly the booster angle jitter" is not supported.
- The driver analysis enters signed errors as magnitudes (`abs`); exploratory signed check: NKM offset ρ = +0.32
  (NKM) against +0.12 (dipole), magnitude +0.12.
- The selected x_inj is the outermost E6 candidate; tuned machines move outward (32/50) and to lower S (31/50).
- The pulse section uses `round2_pulse` (allowance 0.076 mrad from the old 0.76 mrad window; section 3 uses 0.044).
- 51 % of full-budget realizations capture nothing; > 98 % of NKM losses are dynamical ring losses.
- Injected-beam dispersion at the septum: D = 80.9 mm, D′ = 47.5 mrad, not stated in the paper.

**Tasks.** R2d-1 error-class ablation (A); R2d-2 paired wider-window points (A); R2d-3 pulse at the selected point (A);
R2d-4 signed association analysis (B); R2d-5 loss plane, ring 5501, chromaticity (B); R2d-6 BTS dispersion (B);
R2d-7 editorial (C).

No files other than the report, the index and this record were changed; no simulations were run.
