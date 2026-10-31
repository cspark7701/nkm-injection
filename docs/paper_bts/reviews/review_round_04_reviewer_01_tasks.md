# Reviewer 1 — BTS round-4 checkbox revision list

Date: 2026-10-31. Basis: [round-4 report](review_round_04_reviewer_01_report.md).
Recommendation: **minor revision; scientifically acceptable in principle after the required corrections**.
All boxes are deliberately unchecked. Writing this review does not execute a revision or establish acceptance.
These `R1D-BTS` IDs are new Reviewer 1 follow-up items, distinct from the executed consolidated `R4-BTS-01–14`.

## Required scientific and documentary corrections

- [ ] **R1D-BTS-01 — Correct the validation/rare-loss comparison (C1).** Distinguish tracked counts, Gaussian
  predictions conditional on the same 600 shots, and nominal-covariance jitter-integrated predictions. Restrict
  the 1% claim to the rows meeting it; disclose the roughly 5% second-test discrepancies and the sparse-count
  uncertainty. For the dispersion-free row, compare one observed loss with 0.2704 expected conditionally, rather
  than treating it as precise validation of the 73.86 integrated expected-count equivalent. Qualify exact averaging
  and any non-Gaussian-tail claim. **Done when:** table/text/evidence use the same conditioning, units and scope;
  no arbitrary increase in particles or shots is required.

- [ ] **R1D-BTS-02 — Qualify transfer equivalence and the cause of paired differences (C2).** Restrict phase-only loss
  statements to the nominal matched Gaussian model. Replace generic optical identity by nominal horizontal
  transfer equivalence; preserve different strengths/interior optics/error responses and design-specific reading
  noise. Shared jitter can amplify a response difference but cannot alone identify its cause. **Done when:**
  the abstract, Table 7 caption and text agree, with exclusive attribution removed unless directly controlled.
  At reduced jitter, retain the measured residual horizontal/vertical centroid contributions rather than describing
  the nominal jitter partition as the entire delivered distribution. A new common-noise or correction run is
  optional if these claims are narrowed.

- [ ] **R1D-BTS-03 — Reconcile conclusions with the new evidence (C3).** Replace the low-beta "unchanged loss"
  statement with the observed small, population-dependent differences and distinguish the role of phase advance
  from vertical peak beta. Distinguish analytic dispersion-free predictions from the new tracked test.
  **Done when:** no conclusion contradicts Table 7, the previous test or the corrected response.

- [ ] **R1D-BTS-04 — Repair provenance, legend and current status documents (C4).** Correct `test_source` to the
  selected `final_test_b/final_test.json` in the exporter and generated record. Change Figure 4's "reachable"
  legend to sampled/found ranges. Identify current 19/nine-page assets and executed work separately from dated
  historical/open-at-review registers. **Done when:** referenced sources exist and match selected hashes; current
  indexes/checklist agree without overwriting earlier reviews or responses. No numerical campaign is needed.

## Required author/submission and final checks

- [ ] **R1D-BTS-05 — Record author choices and provide the required access wording (C5).** Confirm the journal;
  adopt author-approved data-availability wording matching actual access and the chosen journal's requirements;
  obtain final scientific approval before removing approval-pending language. Keep R4-BTS-08's author-dependent
  conditions visibly open until supplied. **Done when:** access and approval are real, with no invented deposit,
  DOI, measured jitter specification or external submission. A sourced jitter input is welcome but not necessary
  to retain the explicit stress-study scope.

- [ ] **R1D-BTS-06 — Reconcile the corrected submission materials (C6).** Write a new response to this assessment,
  run the relevant asset/claim and changed-method checks, rebuild both article and supplement, inspect affected
  pages, and prepare a new verified increment matching the corrected selected evidence. Preserve previous
  attachments, reports and responses. **Done when:** values, conditioning, source pointers and final PDFs agree,
  and numerical execution, author approval and journal delivery are separately recorded. This review does not
  authorize an upload or require a new full campaign.

## Recommended editorial improvement

- [ ] **R1D-BTS-07 — Shorten for the selected journal (C6; editorial recommendation).** Check a manual word count
  against the chosen venue's guidance, remove repeated baseline/history/validation explanations and move detail
  to the existing supplement where useful. Preserve the physical mechanism, error assumptions, paired intervals,
  stress-level qualification and ring-capture limitation. **Done when:** the main argument reads continuously;
  no arbitrary page threshold or deletion of unfavorable results is imposed.

## Order and scope

Address 01–03 from the existing summaries and code definitions, then 04. Item 05 needs author decisions and may
proceed alongside those corrections. Item 06 follows all adopted changes; item 07 can accompany the text pass.
The prior substantive remedies are credited, not reopened. No new global optimization, larger ring/error
population, measured hardware campaign or BTS lattice change is requested. Use new output directories if any
validation is actually rerun. All seven tasks remain pending at the time of this review.
