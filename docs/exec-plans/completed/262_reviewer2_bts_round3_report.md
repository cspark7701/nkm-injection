# Milestone 262 — Reviewer 2 round-3 report on the BTS manuscript

Completed: 2026-10-30. Pre-submission review of `docs/paper_bts/` at `603c3ab` (15-page article), written as
Reviewer 2 after reading the three main-branch author responses (Reviewer 1 rounds 1–2 and Reviewer 2), the
round-2 Reviewer 2 report and the generated tables.

**Output.**
- `docs/paper_bts/reviews/reviewer2_bts_20261030_main_round3_report.md` (new);
- `docs/paper_bts/reviews/reviewer2_bts_20261030_main_round3_revision_tasks.md` (new);
- a reviews index entry.

No earlier review or response was changed.

**Recommendation.** Major revision; not acceptable in present form, with a short route to acceptance.

**Findings checked.**
- **Booster jitter at m1:** 0.5 mm / 0.2 mrad against a beam of 0.379 mm / 91 µrad, i.e. 1.3σ / 2.2σ. Its mean
  centroid action is about 54 times the emittance.
- **Exit jitter:** 0.643 / 0.506 mm, i.e. 4.0σ / 3.2σ of σ_x = 0.159 mm. The blade distance of 1.478 mm is 2.3 /
  2.9 jitter standard deviations.
- **Baseline exit:** β_x / β_y = 45.0 / 242.6 m against a target of 2.34 / 4.26 m (residual 4.8 × 10³). The blade
  distance is defined as 3σ_x + 1 mm of the matched beam.
- **Static residual:** it roughly doubles the loss (error-free 1.28 % / 0.27 % against tracked 2.30 % / 0.69 %).
- **Text slips:**
  - the corrected angle spread does not fall (364 to 367 µrad);
  - "indistinguishable" is used for 1.68 % against 1.47 % with no interval.

**Tasks.**

| ID | Priority | Task |
| :--- | :---: | :--- |
| R2C-01 | A | Jitter level and sweep |
| R2C-02 | A | Baseline framing and abstract |
| R2C-03 | A | Constrained μ_x scan |
| R2C-04 | A | Blade-distance sweep |
| R2C-05 | B | Steering assumptions and vertical exit centroid |
| R2C-06 | B | Dispersion-free tracking |
| R2C-07 | C | Length and structure |
| R2C-08 | C | Title and wording |
| R2C-09 | C | Supplement and declarations |
| R2C-10 | C | Response update |

No simulations were run and no manuscript or source file was changed.
