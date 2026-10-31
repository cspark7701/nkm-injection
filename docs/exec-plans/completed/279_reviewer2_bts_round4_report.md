# Milestone 279 — Reviewer 2 round-4 report on the BTS manuscript

Completed: 2026-10-31. Pre-submission review of `docs/paper_bts/` at `6a968f8` (19-page article, 9-page supplement),
written as Reviewer 2 after reading all main-branch author responses (Reviewer 1 rounds 1–2, Reviewer 2 round 2 and
the joint round-4 response), the earlier reports and the round-4 stage outputs.

**Output.**
- `docs/paper_bts/reviews/review_round_03_reviewer_02_report.md` (new);
- `docs/paper_bts/reviews/review_round_03_reviewer_02_tasks.md` (new; checkbox task list);
- a reviews index entry.

No earlier review or response was changed.

**Recommendation.** Major revision of limited scope. Not acceptable in present form; acceptance expected after
R2D-01 to R2D-03.

**Finding checked.** From `results/bts_round4_campaign_20261030/jitter_b/jitter.json`, the steered exit centroid of
the matched reference:

| Jitter scale | x [mm] | x′ [mrad] |
| ---: | ---: | ---: |
| 0 | 0.096 | 0.176 |
| 0.1 | 0.113 | 0.179 |
| 0.2 | 0.156 | 0.187 |
| 1 | 0.639 | 0.366 |

The vertical centroid is 1.07 mm / 0.096 mrad at every level. At realistic jitter, the static horizontal angle
residual and the uncorrected vertical offset therefore dominate the jitter, which is 0.06–0.08 mrad in angle. This
contradicts the new abstract's conclusion that the position–angle partition is the design output at realistic jitter.

**Tasks.**

| ID | Priority | Task |
| :--- | :---: | :--- |
| R2D-01 | A | Two-regime conclusion |
| R2D-02 | A | Shared reading errors (rerun) |
| R2D-03 | A | Jitter-integrated headline estimate |
| R2D-04 | B | Physical origin of the lower μ_x edge |
| R2D-05 | B | Consolidation and length |
| R2D-06 | B | Angle-aware steering |
| R2D-07–R2D-12 | C | Editorial, declarations, supplement and response |

No simulations were run and no manuscript or source file was changed.
