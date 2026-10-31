# Consolidated BTS revision register — round-5 work and round-6 follow-up

Prepared: 2026-10-31. This is the current execution register for the BTS manuscript,
*Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*.

It consolidates these two source lists without replacing their historical records:

- [Round-5 plan answering both round-4 reviews](revision_round_05_plan_for_review_round_04.md): R5-BTS-01–10, with nine completed items and one deferred author-decision item.
- [Reviewer 2 round-5 revision checklist](review_round_05_reviewer_02_tasks.md): R2E-BTS-01–04, all pending at review, following the [round-5 report](review_round_05_reviewer_02_report.md) on manuscript `50d46991ca91290a500c7c3b50ca85f297dec6c7`.

**Current state: nine completed source tasks, one completed and three pending follow-up tasks, one deferred source item.**
The active queue below uses **R6-BTS-01–04** to distinguish this revision cycle from the completed round-5 implementation. Each item retains its original reviewer ID. Review round 5 and revision round 6 are different identifiers.

Reviewer 2 recommends minor revision and scientific acceptance in principle after bounded corrections. Reviewer 1's latest assessment remains round 4. Consolidation does not execute a revision, imply author approval or constitute journal acceptance. Both source lists, their completion evidence, all previous reports and author responses remain unchanged. The old plan's opening “all tasks pending” sentence describes its initial preparation; its checked entries and final completion summary record the later execution state.

## Completed work retained from round 5

The original task definitions and full completion records remain authoritative for what was done. These completed entries record historical execution; they do not claim that the new reporting corrections are already complete.

| Status | Source task | Completed work and recorded evidence | Remaining follow-up |
| :--- | :--- | :--- | :--- |
| Completed | R5-BTS-01 | Shared monitor errors; targeted final-test/layout reruns; duplicate-configuration check. Milestone [283](../../exec-plans/completed/283_r5_bts_01_shared_reading_errors.md). | Preserve runs and pairing; distinguish older populations under R6-BTS-03. No automatic rerun. |
| Completed | R5-BTS-02 | Defined integrated-loss headline and paired bootstrap; separated four loss quantities and sparse-count limits. Milestone [285](../../exec-plans/completed/285_r5_bts_02_headline_estimator.md). | Correct discrepancy wording under R6-BTS-01; retain the supported headline. |
| Completed | R5-BTS-03 | Two jitter regimes and low-jitter exit residuals. Milestone [286](../../exec-plans/completed/286_r5_bts_03_two_regimes.md). | Qualify dominance and residual claims under R6-BTS-02. |
| Completed | R5-BTS-04 | Baseline framing, population-dependent low-beta conclusion and sparse-count/formatting corrections. Milestone [287](../../exec-plans/completed/287_r5_bts_04_conclusions_formatting.md). | Repair the remaining population reference under R6-BTS-03. |
| Completed | R5-BTS-05 | Declared local dispersion/phase-edge study. Milestone [288](../../exec-plans/completed/288_r5_bts_05_phase_edge.md). | Correct match accounting and qualify causal scope under R6-BTS-02. |
| Completed | R5-BTS-06 | Endpoint-weight sensitivity with unchanged lattice. Milestone [289](../../exec-plans/completed/289_r5_bts_06_angle_weighted_steering.md). | Limit the conclusion to the tested weighting under R6-BTS-02. |
| Completed | R5-BTS-07 | Earlier tables moved to the supplement; jitter figure simplified; repeated historical material compressed. Milestone [290](../../exec-plans/completed/290_r5_bts_07_consolidation.md). | Further shortening remains optional, not an acceptance condition. |
| Completed | R5-BTS-08 | Provenance/citation repairs and current-status updates. Milestones [284](../../exec-plans/completed/284_r5_bts_08_provenance_citations.md) and [292](../../exec-plans/completed/292_r5_bts_10_reconciliation.md). | Refresh only affected current pointers/labels under R6-BTS-03/04. |
| Completed | R5-BTS-10 | Joint response, evidence reconciliation, installed PDFs and verified referee increment. Milestone [292](../../exec-plans/completed/292_r5_bts_10_reconciliation.md). | A new response and verification are needed for this follow-up under R6-BTS-04. |

Completion evidence includes the [joint response to round-4 reviews](review_round_04_author_response_to_reviewers_01_02.md), [round-5 protocol](../round5_protocol.json) and [round-5 reproduction guide](../round5_reproduction.md). Historical table numbers and percentages in those dated records are not silently rewritten by this consolidation.

## Active revision checklist

All four items are required by the new reviewer checklist; completion is recorded below. Items 01–03 can be prepared independently; complete them before final reconciliation in 04. Reuse existing evidence wherever it supports a wording or reference correction. No broad simulation campaign, hardware change, global search or measured-jitter requirement is introduced.

- [x] **R6-BTS-01 — Define and correct the count-discrepancy percentage.**
  **Source:** R2E-BTS-01, report C1; follows completed R5-BTS-02.
  - Choose a named denominator. For 942 observed losses against 880.453324 expected, the prediction is 6.5% below observation, or observation is 7.0% above prediction. The phrase “6.5% more” does not describe the latter convention.
  - Make the generating calculation or label, macros, Results and Discussion agree. Preserve the recorded counts and integrated headline gain of 4.48 [4.33, 4.63].
  - Identify the reported 2.1 standard deviations as a diagnostic Poisson approximation. Retain the unresolved-discrepancy and sparse-tail limitations; do not restore a universal 1% accuracy claim.
  **Completion:** the chosen percentage reconstructs from unrounded counts and matches the rendered text. No new tracked particles are required for this correction.
  **Done:** milestone [295](../../exec-plans/completed/295_r6_bts_01_validation_percentage.md); exporter names the observed-count denominator, the shortfall reconstructs as 6.533617385%, and the isolated article build passes without warnings. Counts and headline gain are unchanged.

- [ ] **R6-BTS-02 — Qualify phase-edge, steering and residual claims.**
  **Source:** R2E-BTS-02, report C2; follows completed R5-BTS-03/05/06.
  - Correct D′ = 0 start accounting: `dispersion_free_best` fails the declared matching test, while two starts yield matched candidates. Retain iteration-limit flags for the changed-D′ searches.
  - Describe the phase shift with D′ as evidence within the local searches. Do not infer an exclusive binding cause or a globally certified edge. Carry that qualification through Results and Discussion.
  - Limit the endpoint-weighting conclusion to the tested change from 3 to 10 and the assumed readings/error model. Do not infer that position readings generally cannot improve angle or that a direct angle measurement is necessary.
  - Scope the opening jitter-dominance statement to the assumed stress-level jitter. Scope statements about static-residual invariance to the tested settings and correction scheme; preserve the supported two-regime conclusion.
  **Completion:** claims in the abstract, Results and Discussion agree with the stored match/termination and steering records. Wording corrections suffice; no new optimization is mandatory.

- [ ] **R6-BTS-03 — Reconcile test populations, sensitivity labels and cross-references.**
  **Source:** R2E-BTS-03, report C3; follows completed R5-BTS-01/04/07/08.
  - Replace Section 4.2's stale unresolved-low-beta reference to Section 4.3 with an explicit reference to the earlier test in supplement Section 5.
  - Retain the current primary-test decrease of −0.13 [−0.24, −0.04] percentage points and the population-dependent interpretation.
  - Identify earlier retained jitter/blade sensitivities by setting and reading-noise convention. Keep them distinct from the new shared-reading primary comparison; do not relabel old runs or require reruns merely to preserve labelled sensitivity evidence.
  - Use the actual compiled labels in new response/status descriptions: the reviewed primary comparison is Table 6 and residuals are Table 8. Recheck labels after rebuilding; preserve earlier dated records.
  **Completion:** article, supplement, captions and new response distinguish earlier and primary populations, with valid cross-references.

- [ ] **R6-BTS-04 — Respond to the review and verify the bounded revision.**
  **Source:** R2E-BTS-04; follows completed R5-BTS-08/10 and depends on R6-BTS-01–03.
  - Create a new `review_round_05_author_response_to_reviewer_02.md`, answering C1–C3 and all four R2E-BTS items through the crosswalk below. Preserve every earlier report, task list and response.
  - Rebuild the article and supplement in a new results directory. Refresh only affected current generated assets, claim/provenance entries and selected hashes; retain the reviewed snapshot and earlier identities.
  - Run the evidence audit, selected-asset verification and relevant existing tests for changed code. Inspect changed PDF passages and links, and record actual results and numerical limitations. Do not claim a production rerun or broader test coverage unless performed.
  - Update current status/review indexes, this register's execution evidence and the completed-milestone archive. Keep the historical round-5 response and attachment identifiable.
  **Completion:** the new response, PDFs, source evidence, units, values and checks agree. Scientific reassessment remains distinct from a journal decision. No external delivery or submission is authorized by this task.

## Complete source-task crosswalk

Every top-level task from both input lists is accounted for. Completed tasks are carried as history, not reopened wholesale; the new corrections are explicit follow-ups.

| Source item | Consolidated disposition |
| :--- | :--- |
| R5-BTS-01 | Completed ledger; preserve pairing/population context in R6-BTS-03. |
| R5-BTS-02 | Completed ledger; follow-up R6-BTS-01. |
| R5-BTS-03 | Completed ledger; follow-up R6-BTS-02. |
| R5-BTS-04 | Completed ledger; follow-up R6-BTS-03. |
| R5-BTS-05 | Completed ledger; follow-up R6-BTS-02. |
| R5-BTS-06 | Completed ledger; follow-up R6-BTS-02. |
| R5-BTS-07 | Completed ledger; optional shortening only; labels checked in R6-BTS-03. |
| R5-BTS-08 | Completed ledger; current labels/pointers reconciled in R6-BTS-03/04. |
| R5-BTS-09 | Deferred to submission readiness; outside the active checklist. |
| R5-BTS-10 | Completed ledger; a separate follow-up response/verification in R6-BTS-04. |
| R2E-BTS-01 | R6-BTS-01. |
| R2E-BTS-02 | R6-BTS-02. |
| R2E-BTS-03 | R6-BTS-03. |
| R2E-BTS-04 | R6-BTS-04. |

## Deferred submission-stage decisions

**R5-BTS-09 remains deferred, outside the active checklist.** Journal choice, availability wording, companion-manuscript access, any supplied jitter source and final author approval remain in the [submission checklist](../submission_checklist.md) and source plan. Funding and competing-interest statements are preserved. Deferral is neither completion nor a reason to add these decisions back to the present scientific revision queue. No approval, public deposit or journal delivery is inferred.

## Execution boundaries

Preserve the 36-element BTS source lattice, protected scientific inputs, earlier campaigns and NKM manuscript. Any later numerical work must use a new results directory and record assumptions, units, seeds and validation. Do not silently change assumptions shared with the NKM paper. Optional article shortening must preserve unfavorable results and necessary qualifications.

This document consolidates requirements only. **Active tasks completed: 1 of 4.** Consolidation itself executed no revisions.
