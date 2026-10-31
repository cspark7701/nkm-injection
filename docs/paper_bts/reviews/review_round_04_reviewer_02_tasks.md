# Reviewer 2 — BTS review round 5: revision checklist

Prepared: 2026-10-31. Reviewed baseline: `50d46991ca91290a500c7c3b50ca85f297dec6c7`.

Source: [round-5 report](review_round_04_reviewer_02_report.md). Recommendation: **minor revision; scientifically acceptable in principle after the bounded corrections below**. These are new **R2E-BTS** task IDs, distinct from the completed R5-BTS revision cycle. All checkboxes are open at review; no task is executed here.

This checklist covers scientific reporting and review reconciliation only. It requires no new broad simulation campaign, hardware modification or global-optimum proof.

- [ ] **R2E-BTS-01 — Correct and define the count-discrepancy percentage. Required; report C1.**
  - Choose a named denominator for the edge-row discrepancy. With 942 observed and 880.453324 expected, the prediction is 6.5% below observation, or observation is 7.0% above prediction.
  - Make the generating calculation/label, macros, article Results and Discussion agree. Preserve the count records and the headline integrated gain.
  - Identify the reported 2.1 standard deviations as a Poisson approximation used diagnostically. Retain the unresolved-discrepancy and sparse-tail limitations; do not restore a universal 1% accuracy claim.
  - **Completion evidence:** reconstruct the chosen percentage from unrounded source counts and show consistent rendered text. No new tracked particles are required.

- [ ] **R2E-BTS-02 — Qualify phase-edge, steering and residual claims. Required; report C2.**
  - Correct the D′ = 0 start accounting: the `dispersion_free_best` start fails the declared match test; only two starts yield matched candidates there. Retain iteration-limit flags at the changed D′ targets.
  - In Results and Discussion, describe the observed D′ dependence as evidence within local searches. Do not turn it into an exclusive binding-cause or globally certified edge claim.
  - Restrict the endpoint-weighting conclusion to the tested 3-to-10 weighting and the assumed readings. Do not infer that position readings in general cannot improve angle or that a direct angle measurement is necessary.
  - Scope the opening jitter-dominance claim to stress-level jitter; scope static-residual invariance to the tested settings and steering model. Preserve the useful two-regime conclusion.
  - **Completion evidence:** each statement maps to its stored test/termination record, with the same qualification in the abstract, Results and Discussion where applicable. Wording corrections suffice; no new optimization is mandatory.

- [ ] **R2E-BTS-03 — Reconcile test populations and cross-references. Required; report C3.**
  - Replace Section 4.2's stale unresolved-low-beta reference to Section 4.3 by an explicit reference to the earlier test in supplement Section 5.
  - Retain the primary-test low-beta difference, −0.13 [−0.24, −0.04] percentage points, and the population-dependent interpretation.
  - Identify retained earlier jitter/blade sensitivities by their setting and reading-noise convention so they cannot be mistaken for the new shared-reading primary test.
  - Use current compiled labels in new response/status descriptions: primary comparison Table 6; residuals Table 8. Preserve earlier dated review records as history.
  - **Completion evidence:** article, supplement, captions and new response distinguish earlier/primary populations and all new cross-references resolve.

- [ ] **R2E-BTS-04 — Record the response and verify the bounded revision. Required; review closure.**
  - Create a new `review_round_05_author_response_to_reviewer_02.md`, answering C1–C3 and these task IDs. Preserve all earlier reports, tasks and responses.
  - Rebuild article and supplement in a new results directory. Refresh only the current affected generated assets, claim/provenance entries and selected hashes; retain the reviewed snapshot and earlier evidence identities.
  - Run the evidence audit, selected-asset verification and relevant existing tests for changed code. Check changed PDF passages and links; record actual results and numerical limitations.
  - Update the review index/current status and archive execution milestones. Do not describe a pre-submission recommendation as a journal acceptance.
  - **Completion evidence:** point-by-point response, consistent PDFs/evidence and checks recorded against the new revision. This task does not authorize external delivery or submission.

Optional editorial shortening is described in the report; it is not an acceptance-blocking task.
