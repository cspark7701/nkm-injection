# Reviewer 2 — BTS review round 6: revision checklist

Tasks from the [round-6 report](review_round_05_reviewer_02_report.md) (2026-10-31) on the revision-round-6
manuscript at `79dce19`. Recommendation: **minor revision; acceptable after these corrections, without another
review round.** These are new R2F-BTS task IDs. All boxes are open at review; no task is executed here.

Not included: the R5-BTS-09 submission decisions, which stay deferred to the submission-ready stage.

Constraints: the BTS lattice is not changed. Any rerun uses a new `results/` directory, and earlier reports,
responses and campaigns are preserved.

## Required

- [ ] **R2F-BTS-01 — Base the low-beta effect on controlled evidence (M1).**
  - [ ] Choose one:
    - add low beta to the shared-reading layout stage on the Table 4 realizations, declared before the run, and quote
      its paired difference; or
    - label the Table 4 value (−0.21 percentage points) as confounded by per-setting reading errors.
  - [ ] Make Section 4.2 and the Discussion cite only the controlled result, the primary-test −0.13 [−0.24, −0.04],
        and any new shared-reading value, as evidence of the low-beta effect.
  - *Completion:* no low-beta statement relies on a per-setting-reading population without saying so.
- [ ] **R2F-BTS-02 — Qualify the per-shot bracket and localize the loss-based excess (M2).**
  - [ ] Qualify the Section 3.3 bracket sentence as holding within the linearized Gaussian model.
  - [ ] From the saved per-shot output, state in Section 4.3 that the 942-particle count comes from 20 shots and
        that one near-blade shot (454 lost against 410.9 expected) carries most of the excess.
  - [ ] Recommended: compare that shot's linear-moment prediction with a nonlinear moment calculation and report
        the outcome. If it is not done, keep the excess explicitly unresolved.
  - *Completion:* the text no longer states an unconditional bracket that the tracked count violates, and the
    excess is localized.
- [ ] **R2F-BTS-03 — Say what the headline interval covers (M3).**
  - [ ] In the abstract or Section 4.3, state that 4.48 (4.33–4.63) is a prediction of the linearized Gaussian model
        at the assumed jitter, and that the interval reflects only the sampling of error realizations.
  - *Completion:* no reader can take the interval as a measured-transmission uncertainty.

## Editorial

- [ ] **R2F-BTS-04 — Wording and labels.**
  - [ ] Attribute the uncorrected vertical residual to the absence of a vertical corrector in the modelled line, in
        the abstract and the Discussion (minor 1).
  - [ ] Remove the dangling "therefore" in Section 4.5 (minor 2).
  - [ ] Write "different tracked losses" in Section 3.2 (minor 3).
  - [ ] Use one setting name in the Figure 5 and 6 legends, with "Loss-based" for the equivalent round-3 and edge
        settings, and regenerate those figures (minor 4).
- [ ] **R2F-BTS-05 — Optional shortening (minor 5, advisory).**
  - [ ] Consider moving Table 4 to the supplement once R2F-BTS-01 is settled.
- [ ] **R2F-BTS-06 — Reconciliation and response.**
  - [ ] Update any affected claims and generated assets, and refresh the selected hashes.
  - [ ] Rebuild and visually check the article and supplement, and run the tests that the changes call for.
  - [ ] Write a short response to this report, preserving all earlier reports, tasks and responses.
  - *Completion:* PDFs, evidence and response agree; this register is updated with ticked boxes.

## Order

R2F-BTS-01 and R2F-BTS-02 first, because they may need a short computation. R2F-BTS-03 and R2F-BTS-04 next, then
R2F-BTS-06.
