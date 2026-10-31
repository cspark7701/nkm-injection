# Reviewer 2 round-4 revision tasks — BTS main-branch manuscript

Tasks from the [Reviewer 2 round-4 report](reviewer2_bts_20261031_main_round4_report.md) (2026-10-31) on the
manuscript at `6a968f8`. All tasks are open; tick each box when its completion criterion is met.

- **Priority:** A = required for acceptance, B = strongly recommended, C = editorial.
- **Constraints:** the BTS lattice is not changed. New outputs go in new `results/` directories, and earlier
  reports, responses and campaigns are preserved.

## A — required

- [ ] **R2D-01 — Two-regime conclusion (M1).**
  - [ ] Add the static-residual exit centroid at jitter scale 0, by plane (x, x′, y, y′), next to the jitter-only
        values. Use Table 9 or a short companion table, from `jitter_b` (existing data).
  - [ ] Rewrite the end of the abstract and the corresponding Discussion paragraph:
        - **Stress-level jitter:** the jitter partition and the blade loss matter, and μ_x is the knob.
        - **Realistic jitter:** the blade loss is negligible, and the delivered beam error is set by the steering
          angle residual (about 0.18 mrad) and the uncorrected vertical trajectory (about 1.1 mm).
  - [ ] Qualify the comparison of 0.33–0.39 mrad with the 0.44 mrad NKM acceptance as stress-level only.
  - [ ] State in Section 4.2 that steering reads positions only, so the exit angle is constrained only indirectly.
  - *Completion:* no sentence claims that the position–angle partition is the design output at realistic jitter,
    and the static residuals are reported by plane.
- [ ] **R2D-02 — Shared reading errors (M2).**
  - [ ] Draw reading errors per realization and monitor, shared by all settings. Declare this as a protocol
        amendment before the runs.
  - [ ] Rerun the second fresh test and the steering-layout stage in new directories.
  - [ ] Add a regression test: optically identical settings give identical steered lines and losses.
  - [ ] Update Tables 5 and 7 and the text. Keep the per-setting runs as a recorded sensitivity.
  - *Completion:* the identical-optics pair gives identical results, and the quoted intervals come from the shared-noise
    runs.
- [ ] **R2D-03 — Jitter-integrated headline estimate (M3).**
  - [ ] Report the loss-based gain as the jitter-integrated loss averaged over steered realizations, with a
        realization-cluster interval, for each population where it exists.
  - [ ] Present tracked losses as validation of the per-shot model and an illustration of the tail.
  - [ ] Replace "a factor of 3 to more than 10" in the abstract and Discussion with one estimate and its interval.
  - *Completion:* the abstract, Section 4.3 and the Discussion quote the same estimator and interval.

## B — strongly recommended

- [ ] **R2D-04 — Physical origin of the lower μ_x edge (M4).**
  - [ ] Show whether the edge moves with the D′ (and D) target at m4: an analytic dispersion-closure argument, or a
        short edge search over a few D′ values.
  - [ ] If the inherited exit dispersion sets the edge, state this as a design finding in Sections 4.3–4.4 and the
        Discussion.
  - *Completion:* the edge has a stated physical cause, or the text says explicitly that the cause is not
    identified.
- [ ] **R2D-05 — Consolidation and length (M4).**
  - [ ] Move Table 6 (round-3 test) to the supplement, keeping one test table.
  - [ ] Reduce Fig. 4 to its left panel, and remove "reachable" and "Refined low beta" from its labels.
  - [ ] Replace Table 8 with jitter-integrated values, or merge it into Table 9.
  - [ ] Remove the duplicate wording between Sections 4.2 and 4.3.
  - *Completion:* about 12–14 pages; no superseded table or label remains in the article.
- [ ] **R2D-06 — Angle-aware steering (question 1, optional within B).**
  - [ ] Report the exit-angle residual for a layout that weights the septum-entrance and line-end readings for
        angle, with the lattice unchanged.
  - *Completion:* the angle residual is reported, or the omission is justified.

## C — editorial

- [ ] **R2D-07 — Wording remnants.** Delete or reword "Thus optimization of the baseline BTS line improves nominal
  delivery" (Section 4.1). Use one dispersion-free angle jitter (393 or 394 µrad) consistently (Section 4.4).
- [ ] **R2D-08 — Number formatting.** Use proper minus signs in all intervals, in the text, Table 7 and the macros. Use
  a consistent format per column in Table 9. Write the dispersion-free tracked loss as "1 particle (8 × 10⁻⁷)" or as
  an upper bound.
- [ ] **R2D-09 — Citations.** Cite the booster-stability statement in Section 2.4. Update [13] if a full paper
  exists, and note the availability of [5] to referees.
- [ ] **R2D-10 — Declarations and journal (author decisions).**
  - [ ] Target journal: JKPS or NIM A.
  - [ ] A data-availability statement that matches actual access.
  - [ ] Final approval, with the "pending" wording removed.
- [ ] **R2D-11 — Supplement.** Shorten the four-station accuracy audit in supplement Section 3 to one table and a
  paragraph.
- [ ] **R2D-12 — Response.** Write a point-by-point response to this report, and preserve all earlier reports and
  responses.

## Suggested order

1. **Shared reading errors (R2D-02),** because it changes the numbers.
2. **The estimator and the conclusion (R2D-03, then R2D-01).**
3. **The edge explanation (R2D-04).**
4. **Consolidation (R2D-05).**
5. **R2D-06 to R2D-12.**

## Coordination with the companion NKM manuscript

- **R2D-01:** its vertical exit offset (about 1.1 mm / 0.1 mrad) and horizontal angle residual (about 0.18 mrad) are
  the static injection errors the NKM study needs.
- **Booster jitter:** the level is shared with the NKM study; any change of its source belongs in both papers.
