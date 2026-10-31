# Response to Reviewers 1 and 2 — BTS round-4 reviews (round-5 revision)

This joint response addresses:
- the [Reviewer 1 round-4 report](review_round_04_reviewer_01_report.md) (minor revision) and its tasks R1D-BTS-01
  to 07;
- the [Reviewer 2 round-4 report](review_round_04_reviewer_02_report.md) (major revision of limited scope) and its
  tasks R2D-01 to 12.

Both were executed through the [round-5 plan](revision_round_05_plan_for_review_round_04.md), R5-BTS-01 to 10,
milestones 283–292. The reports, task registers and all earlier responses are unchanged. This is a pre-submission
revision record. It is not a journal decision and not author approval.

**Evidence.**
- **Protocol:** [round-5 protocol](../round5_protocol.json), declared before the runs.
- **Reproduction:** [round-5 reproduction guide](../round5_reproduction.md).
- **Claims:** BR5-01 to BR5-10 in the [claim ledger](../claim_evidence.csv). All 73 claims verify.
- **Lattice:** the BTS lattice is not changed.

## What changed in the conclusions

1. **Reading errors are shared.** They are now drawn per realization and monitor and shared by all settings. With
   shared readings, the round-3 loss-based setting, the converged edge setting and a duplicate configuration lose
   the same 942 particles. Their different round-4 counts (1 022 and 1 564) therefore came from separate reading
   errors.
2. **One headline gain.** The gain is the ratio of mean jitter-integrated losses on the primary population: 4.48,
   with a 95 % interval of 4.33–4.63. The layout population gives 4.59. The earlier tracked gains of 3.3 to 11 are
   attributed to sampling of the jitter tail.
3. **Two regimes.** At the stress-level jitter, the phase advance is the knob for blade loss. At 0.1–0.2 of it, the
   blade loss is negligible, and the delivered beam is dominated by the 0.18 mrad horizontal angle left by steering
   and the uncorrected vertical centroid (about 1 mm).
4. **The edge has a cause.** The lower μ_x edge falls from 200.2° to 184.1° as the exit D′ goes from 47.5 to 0 mrad.
   Within local searches, the inherited D′ sets it.

## Reviewer 1 (R1D-BTS)

| Task | Response | Milestones |
| :--- | :--- | :--- |
| R1D-BTS-01 validation and rare loss | Section 3.3 now separates four loss quantities: the error-free objective, the jitter-integrated loss (linearized, nominal covariance, max-event), the shot-conditional prediction and the observed count. The 1 % claim is restricted to the steering and first-test rows. In the second test, the matched reference and low beta agree within half a Poisson standard deviation, and the loss-based count exceeds its prediction by 6.5 % (z = 2.1); the cause is stated as unresolved. Dispersion-free: 1 observed particle against 0.51 expected conditionally and 76 integrated, without a claim to test the tail. "Exactly averaged" and "would dominate" are qualified. | 285, 287 |
| R1D-BTS-02 transfer equivalence and attribution | Phase-only statements are restricted to the nominal matched model, including in the abstract. "Optically identical" became "the same nominal horizontal transfer". The attribution now rests on the controlled shared-reading rerun. Low-jitter residuals are reported (Table 8). | 283, 286 |
| R1D-BTS-03 conclusions | The low-beta change is population-dependent: −0.21 and −0.13 percentage points, and unresolved in the first test. It goes with a 1° smaller μ_x. The dispersion-free results are no longer called analytic only. | 287 |
| R1D-BTS-04 provenance, legend, status | `test_source` points to `final_test_b`, with repository-relative paths. Figure 4 uses "found range". Current status documents name the 19-page article and the 10-page supplement. | 284, 290, 292 |
| R1D-BTS-05 author choices | Recorded as open in the submission checklist: journal, data availability, companion access, jitter source and approval. Nothing is invented. | 291 |
| R1D-BTS-06 reconciliation | 10 new claims; the audit and `--verify` pass; full tests pass; clean builds; a new verified referee increment. | 292 |
| R1D-BTS-07 shortening | Superseded tables are moved to the supplement and Figure 4 has one panel. The article is 19 pages (about 9,900 tokens including captions); see R2D-05. | 290 |

## Reviewer 2 (R2D)

| Task | Response | Milestones |
| :--- | :--- | :--- |
| R2D-01 two regimes | Table 8 (exit centroid against nominal jitter by scale). The abstract and Discussion state the stress-level and low-jitter regimes and the 0.18 mrad / about 1 mm residuals. Steering reads positions only. The 0.44 mrad comparison is qualified as stress-level. | 286 |
| R2D-02 shared reading errors | Protocol amendment; the second test and the layouts are rerun with shared readings. The duplicate-configuration check passes. | 283 |
| R2D-03 headline estimate | 4.48 [4.33, 4.63], a ratio of means with a paired bootstrap, declared before the run. | 285 |
| R2D-04 lower edge | The D′ edge study (above). | 288 |
| R2D-05 consolidation | One main test table and a one-panel Figure 4. The first test and the sampled roll table moved to supplement Section 5. The 12–14-page target was not reached; further cuts would remove author-requested material (baseline figures, literature review) and are left to the author. | 290 |
| R2D-06 angle-aware steering | Weighting the exit readings 10 instead of 3 leaves the angle residual at 0.41 mrad. Position readings alone cannot reduce it. | 289 |
| R2D-07 wording remnants | The baseline sentence was reworded, and one dispersion-free angle value (393 µrad) is used. | 287 |
| R2D-08 formatting | Proper minus signs, a uniform Table 7 format, and counts and fractions for the dispersion-free row. | 285, 287 |
| R2D-09 citations | The uncited stability statement is removed. TPS [13] is cited as JaCoW records it (presented, unpublished, TUP2685). [5] stays in preparation. | 284 |
| R2D-10 declarations and journal | Open author decisions, recorded. | 291 |
| R2D-11 supplement | The four-station audit paragraph is halved. | 290 |
| R2D-12 response | This document. | 292 |

## Answers to Reviewer 2's questions

1. **Angle residual with angle-aware weighting:** 0.411 mrad, against 0.413 mrad for the loss-based setting.
   Reweighting does not help.
2. **Does the edge move with D′, and is D′ binding?** Yes; see the edge study. No strength bound and no peak limit
   are active at those edges.
3. **Vertical trims of existing elements:** none exists in the studied model. The article states the uncorrected
   vertical centroid as a limitation of this line, and its correction is left to a future study.

## Open items (author decisions)

- **Target journal:** JKPS or NIM A.
- **Data availability:** wording that matches actual access.
- **Companion manuscript:** how referees get access to it.
- **Booster jitter:** a source for the jitter level, which should then change in both papers.
- **Final approval:** final scientific approval of the revised text.
