# Milestone 286 — R5-BTS-03: two jitter regimes and residual delivery errors

Completed: 2026-10-31. Round-5 task R5-BTS-03 (Reviewer 2 R2D-01; Reviewer 1 R1D-BTS-02, nominal scope and
low-jitter residuals).

**Evidence.** These are existing data (`results/bts_round4_campaign_20261030/jitter_b`), installed as
`generated/round5_residual_rows.tex` (new Table 10). The scale applies to the betatron jitter, and the 0.1 %
momentum jitter is retained at every scale, as the caption states. Matched reference:

| Scale | Steered x | Steered x′ | Steered y | Steered y′ | Nominal σ_x′,j |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.096 mm | 0.176 mrad | 1.073 mm | 0.096 mrad | 0.047 mrad |
| 0.1 | — | 0.179 mrad | — | — | 0.057 mrad |
| 0.2 | — | 0.187 mrad | — | — | 0.080 mrad |

At scale 0 the vertical centroid is 1.07 / 0.92 / 0.78 mm for the matched reference, low beta and loss-based
settings.

**Article.**
- **Abstract.** The phase-only statements are now "in the nominal matched model". The closing sentences give the
  two regimes. At stress-level jitter the reported gain applies. At 0.1–0.2 of it the blade loss is negligible,
  and the exit centroid is set by the steering residual (0.18 mrad) and the uncorrected vertical plane (1.07 mm).
  "The design output … is the partition" is removed.
- **Section 4.2.** Steering fits position readings only, so the exit angle is constrained only indirectly.
- **Section 4.5.** New regime paragraph and Table 10. The vertical centroid is stated as setting-dependent but
  uncorrected in every setting, which corrects a draft sentence that called it setting-independent.
- **Discussion.**
  - The 0.33–0.39 mrad against 0.44 mrad comparison is qualified as stress-level, and the 0.44 mrad is attributed to
    the companion study.
  - The low-jitter paragraph now says that correction and instrumentation, especially vertical, matter more than
    the choice among matched optics.
- **Attribution.** The controlled shared-noise evidence of R5-BTS-01 replaces the exclusive attribution of
  paired differences.

The prose follows the humanizer rules. The isolated build is clean. Protected files are unchanged.
