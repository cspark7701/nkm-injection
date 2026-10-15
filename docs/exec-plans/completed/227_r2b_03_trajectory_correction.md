# Milestone 227 — R2B-03: Trajectory correction of the BTS line

Completed: 2026-10-15. Reviewer 2 BTS task R2B-03 (M3).

**Model** (`bts_round3.response_matrix`, `correct_trajectory`):
- Thin H/V correctors; monitors with a static 50 µm rms reading error.
- Weighted least squares with the error-free model response, Tikhonov-regularised, kicks ±1 mrad, two passes.
- Shot jitter is not corrected.

**Declared layout and its amendment.**
- The declared layout (correctors before q11, q21, q31, sept_ex; monitors after each quadrupole and at the end)
  corrected the exit position but raised the exit-angle spread from 0.36 to 0.54 mrad. The last corrector, 1 m
  upstream of the exit, buys position with angle.
- After this first run (kept in `steering_declared_only/`), the protocol was amended, and the amendment recorded,
  before any later campaign: a corrector before b3 and a monitor at the septum entrance.
- Both layouts are reported on identical machines.

**Result** (stage `steering`, 200 machines × 3 shots × 2 000 particles, seeds 91001–91004):

| Steering | Lost (reference) | Exit x rms | Exit x′ rms |
| :--- | ---: | ---: | ---: |
| None | 10.08 % | 1.20 mm | 0.36 mrad |
| Declared | 2.39 % | 0.69 mm | 0.54 mrad |
| Amended | 1.60 % | 0.68 mm | 0.34 mrad |

- After amended correction, the exit spread equals the booster-jitter transfer.
- Low beta is indistinguishable from the reference (amended 1.56 %).
- The Gaussian loss prediction agrees with tracking within 0.6 % (relative) in every row.
- Mean minimum clearance mis-ranks the variants: uncorrected has the highest mean (0.584 mm) and six times the loss.

**Manuscript.** New Section 2.4 (errors, jitter, correction) and Results 4.2 with Table 3.

**Tests** (9 pass): amended steering reduces the exit offset to < 25 % with exit angle < 0.2 mrad and kicks within
limits; zero-kick correctors leave the line unchanged.
