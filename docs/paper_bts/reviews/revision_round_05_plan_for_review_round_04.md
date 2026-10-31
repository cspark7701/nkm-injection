# Consolidated tasks from the round-4 reviews — BTS round-5 revision

Prepared: 2026-10-31. Applies to the round-4 manuscript at `6a968f8`:
*Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*.

This is the single execution register for the next revision. It consolidates:

- [Reviewer 1 round-4 report](review_round_04_reviewer_01_report.md) and
  [seven tasks](review_round_04_reviewer_01_tasks.md), R1D-BTS-01–07:
  minor revision, scientifically acceptable in principle after corrections.
- [Reviewer 2 round-4 report](review_round_04_reviewer_02_report.md) and
  [twelve tasks](review_round_04_reviewer_02_tasks.md), R2D-01–12:
  major revision of limited scope, no acceptance in present form.

Both reports and source registers remain unchanged. Their different recommendations are not averaged into an
acceptance decision. The previously executed [round-4 consolidated plan](revision_round_04_plan_for_review_round_03.md)
answered the round-3 reviews; it is preserved. Hence this follow-up uses **round 5** and new **R5-BTS** IDs.

**All tasks below are pending.** Consolidation does not execute revisions, authorize simulation runs, constitute
author approval, or authorize journal submission, external uploads or a git push.

Priority A means required by at least one reviewer, including submission gates. B means recommended or conditional.
A completed task needs recorded evidence for its applicable source requirements; author-dependent conditions must
not be marked complete merely because numerical work passes.

## Decisions where the reviews differ

| Topic | Consolidated decision |
| :--- | :--- |
| Shared reading noise | Retain Reviewer 2's required protocol amendment and targeted reruns, although Reviewer 1 would accept narrower wording without them. Use a regression test for genuinely identical complete configurations. Equal nominal horizontal transfer alone does not imply equal perturbed lattices, and must not be made to do so. |
| Primary loss estimate | Use the jitter-integrated population-mean comparison requested by Reviewer 2, while retaining Reviewer 1's distinctions between the nominal objective, integrated surrogate, conditional shot prediction and observed counts. |
| Physical cause of the phase edge | Retain the recommended analysis, with Reviewer 2's explicit alternative of admitting that the cause remains unidentified. A global proof is not required. |
| Article length | Aim for the suggested 12–14-page range if practical, while treating it as an editorial target, not a scientific acceptance threshold. Check the selected journal's actual guidance; do not remove unfavorable results or necessary assumptions to meet a page count. |
| Author decisions | Journal, access wording and approval remain open until provided. A measured jitter specification is welcome; it is not to be invented and is not required to retain a clearly labelled stress study. |

## Consolidated checkbox register

- [x] **R5-BTS-01 — Share reading errors and rerun the targeted comparisons. Priority A.**
  **Sources:** R2D-02; R1D-BTS-02 (pairing and attribution).
  - Declare a protocol amendment before running anything: reading errors are keyed by realization and physical
    monitor location, shared across all settings. Preserve the same error at a shared monitor across layouts;
    avoid design-order-dependent seeds. Keep magnet errors, jitter and particle variates paired as before.
  - Rerun the second fresh test and steering-layout stage in new directories, using the declared seeds. Retain
    the old per-setting-noise runs as a labelled sensitivity, not overwritten evidence.
  - Add a regression check that two copies of the **same full configuration**, with identical errors/readings,
    give identical steered lines and losses. Different strength vectors with the same nominal horizontal
    end-to-end matrix can have different error/steering responses; diagnose such differences rather than forcing
    their losses to agree. If a stronger equivalence claim is kept, demonstrate its premises first.
  - Update the corresponding steering-layout/test tables, paired intervals and attribution text.
  **Completion:** shared-noise protocol and generating identity recorded; duplicate-configuration regression
  passes; the revised comparisons use the new paired runs and preserve the original ones.
  **Done (milestone 283, `af08ff1`):** shared reading errors declared in `round5_protocol.json`; the duplicate configuration and the round-3/edge settings lose identical particles (942); Tables 5 and 7 use the reruns; per-setting runs kept as a sensitivity.

- [x] **R5-BTS-02 — Use a defined headline estimator and repair the rare-loss validation. Priority A.**
  **Sources:** R2D-03; R1D-BTS-01; R2D-08 (sparse-loss reporting).
  - Before interpreting the new test, identify the primary evaluation population. For each available population,
    report jitter-integrated losses averaged over steered realizations and their paired realization-bootstrap
    uncertainty. Define the gain as a ratio of the population means (or another explicitly justified estimand),
    not an unlabelled mean of per-realization ratios. Apply the same resampled realization IDs to both settings.
    State how zero/small denominators are handled. Do not select the largest gain after seeing the populations.
  - Replace the abstract's variable factor-of-3-to-over-10 headline by the chosen estimator and its interval;
    retain other populations as labelled sensitivity/validation rows. Match the abstract, results and conclusions.
  - Distinguish the nominal error-free objective; the nominal-covariance jitter-integrated surrogate; predictions
    conditional on the actual sampled shots/beta factors; and observed particle counts. Do not subtract or compare
    differently conditioned quantities as though they were the same estimator.
  - Restrict the 1% agreement claim to rows that meet it. The old second-test loss-based/edge rows have about
    5% relative conditional prediction/count differences, which need sampling qualification rather than a universal
    tolerance claim. New shared-noise rows must be assessed on their own data.
  - For the existing dispersion-free case, retain the distinction between one observed loss, about 0.2704
    conditionally expected particles and the 73.86 integrated expected-count equivalent. Report the revised run's
    values after R5-BTS-01. One rare event does not validate an unconditional tail at fixed relative precision.
    Prefer the count and its denominator to an unsupported machine-reliability bound.
  - Qualify exact averaging as a result within the stated Gaussian/linearized-transport, nominal-covariance model
    and event surrogate. Non-Gaussian tails could matter if present; their dominance is not established here.
  **Completion:** estimator, population, units and conditioning agree across tables/text/evidence; uncertainty is
  attached to the claimed gain, and finite-shot validation is not misrepresented as tail certification.
  **Done (milestone 285, `3157639`):** ratio of mean jitter-integrated losses with a paired bootstrap, 4.48 [4.33, 4.63] (layouts 4.59); four loss quantities separated; 1 % claim restricted; 6.5 % loss-based excess and the dispersion-free count (1 against 0.51 expected) stated.

- [x] **R5-BTS-03 — State both jitter regimes and the residual delivery errors. Priority A.**
  **Sources:** R2D-01; R1D-BTS-02 (nominal scope and low-jitter residuals).
  - Add the scale-zero exit centroid RMS by plane (x, x′, y, y′), next to nominal jitter-only values, from the existing
    jitter sweep; distinguish any retained momentum jitter from a pure static-error calculation. Label scale-zero
    betatron jitter accurately because momentum jitter is not switched off by that scale.
  - At stress-level betatron jitter, discuss blade loss and its phase-dependent position–angle partition.
    At the lower tested jitter levels, discuss negligible blade loss **and** the remaining horizontal angle and
    vertical centroid errors; the nominal partition is not the whole delivered distribution.
  - State that steering fits position readings, so exit angle is controlled indirectly. Qualify the comparison
    of 0.33–0.39 mrad with the companion's conditional 0.44 mrad window as stress-level and nominal-jitter context.
  - Restrict phase-only loss statements to the nominal matched Gaussian model. Replace generic optical identity
    by nominal horizontal transfer equivalence where that is all that is established. Do not attribute paired
    differences solely to a jitter draw shared by the settings; use the controlled R5-BTS-01 evidence or qualify it.
  **Completion:** abstract, methods, test caption and discussion describe the same two regimes, include the
  residual delivered-beam limitations, and avoid an unsupported exclusive causal claim.
  **Done (milestone 286, `a896d60`):** Table 10 (exit centroid against nominal jitter by scale); abstract and Discussion state both regimes and the 0.18 mrad / about 1 mm residuals; phase-only statements restricted to the nominal model.

- [x] **R5-BTS-04 — Reconcile conclusions, baseline framing and sparse-count wording. Priority A.**
  **Sources:** R1D-BTS-03; R2D-07; R2D-08.
  - Replace “unchanged loss” for low beta by the observed small, population-dependent paired results. Distinguish
    vertical peak-beta reduction from its accompanying horizontal phase change; neither claim equivalence nor
    require a positive effect in every test.
  - Distinguish analytic dispersion-free scans/integrated predictions from its tracked test. Preserve the sparse
    count caveat. Remove the outdated statement that all dispersion-free results are analytic.
  - Reword the remaining statement promoting matching of the unmatched baseline as a design result. Keep it as a
    documented starting-point comparison, not a competing design or the headline result.
  - Use one source and rounding convention for the dispersion-free angle jitter. Use proper mathematical minus
    signs in intervals, consistent numeric formats per column, and explicit fraction-versus-percent units. For
    example, one loss out of 1.2 million is 8.33e-7 as a fraction, not as a percentage.
  **Completion:** conclusions and generated macros/tables agree with the updated comparisons and their scope.
  **Done (milestone 287, `72bff40`):** low-beta, dispersion-free and baseline sentences corrected; one angle-jitter value; minus signs; uniform Table 9 format.

- [x] **R5-BTS-05 — Explain, or explicitly leave open, the lower phase edge. Priority B.**
  **Sources:** R2D-04.
  - Examine dispersion closure analytically, or make a small declared edge study varying D′ and, if informative,
    D at m4. Keep the bounds, beta constraints and local-search termination records explicit.
  - If the evidence identifies a cause, state it with its range of validity. Otherwise state that the physical
    origin is not identified; convergence at an edge is not a global causal explanation.
  **Completion:** a supported explanation or an explicit limitation appears in results and discussion. No new
  global optimizer or large campaign is required.
  **Done (milestone 288, `53e54cf`):** declared edge study; the lower edge falls from 200.2° to 184.1° as D′ goes from 47.5 to 0 mrad with no bound active, so the inherited D′ sets it within local searches.

- [x] **R5-BTS-06 — Assess angle-aware steering, or justify its omission. Priority B, conditional.**
  **Sources:** R2D-06.
  - Using the unchanged lattice, examine a position-reading layout/weighting that better constrains the exit angle
    through the septum-entrance and line-end readings. If run, declare the objective and report the position,
    angle and loss trade together, preserving the existing knob limits and pairing.
  - Alternatively explain why this additional steering design is outside the present scope, using the residuals
    already reported in R5-BTS-03. Do not invent an angle monitor or a hardware capability.
  **Completion:** a documented sensitivity or a justified omission; no automatic requirement to improve capture.
  **Done (milestone 289, `c1da6d7`):** angle-weighted layout (end weight 10) leaves the exit-angle residual at 0.41 mrad and the losses unchanged; stated without an angle monitor.

- [ ] **R5-BTS-07 — Consolidate the article and supplement. Priority B, editorial.**
  **Sources:** R2D-05, R2D-11; R1D-BTS-07.
  - Move the older tracked-test table to the supplement if the revised shared-noise table carries the main argument;
    keep the earlier population/results accessible and clearly labelled rather than silently deleting them.
  - Consider keeping only Figure 4's jitter-transfer panel if Figure 5 supersedes its other panel. Remove old
    “reachable”/“Refined low beta” labels and keep consistent setting names after any figure renumbering.
  - Replace or merge the older sampled roll/energy table with integrated results where appropriate, without mixing
    estimator definitions or claiming uncomputed sensitivity. Remove repeated text across Sections 4.2–4.3.
  - Reduce the supplement's four-station accuracy audit to a concise table/paragraph where feasible, retaining its
    historical model, provenance and numerical limitations.
  - Check a manual word count and the selected journal's guidance. Aim for the suggested 12–14 pages if practical;
    preserve assumptions, stress-level qualification, intervals and negative results. The page target is advisory.
  **Completion:** one clear main comparison, traceable historical material, and consistent figure/table references;
  no acceptance decision is inferred from page count.

- [ ] **R5-BTS-08 — Repair provenance, citations and current status records. Priority A for provenance; editorial for formatting.**
  **Sources:** R1D-BTS-04; R2D-09; labels/formatting from R2D-05 and R2D-08.
  - Correct the exporter and generated `test_source` pointer to the selected actual test file. Initially this is
    `final_test_b/final_test.json`; after R5-BTS-01 it must identify the newly selected shared-noise output. Refresh
    affected digests without relabelling old runs as new ones.
  - Cite an authoritative source for the general booster-stability statement, or narrow/remove the unsupported
    generalization. Keep the KLS stress level distinct from a measured specification.
  - Check whether the TPS abstract now has a full paper; update only verified bibliographic details. Provide
    referees with access to the companion NKM manuscript in preparation without asserting publication.
  - Update current checklists/indexes and layout counts after the final build; distinguish prepared versus
    author-approved gates. Preserve dated reviews, source registers and responses verbatim.
  **Completion:** selected paths exist and are hash-consistent, source claims are verified or qualified, and
  current status documents describe the actual revision rather than earlier page counts or an old execution queue.
  **In progress (milestone 284, `90ca9b8`):** `test_source` pointer fixed and provenance paths made relative; uncited stability statement removed; TPS reference checked against JaCoW (unpublished, TUP2685). Status documents and layout counts follow the final build in R5-BTS-10.

- [ ] **R5-BTS-09 — Record the author-dependent submission choices. Priority A, author input.**
  **Sources:** R1D-BTS-05; R2D-10.
  - Confirm the target journal (JKPS or NIM A), then check its applicable submission requirements.
  - Supply author-approved availability wording consistent with actual access and the chosen journal; no invented
    public deposit, DOI or delivery claim. Preserve supplied funding and competing-interest information.
  - Obtain final scientific approval before removing approval-pending text. Record the remaining conditions of
    the earlier R4-BTS-08 separately from completed numerical work.
  - If an actual KLS jitter source is supplied, coordinate the shared assumption with the NKM paper. Otherwise keep
    the specified stress-study scope; do not fabricate a source or require measured stability to retain that scope.
  **Completion:** decisions and access are real and recorded. No external submission is authorized by this plan.

- [ ] **R5-BTS-10 — Final reconciliation and one response to both reviews. Priority A.**
  **Sources:** R1D-BTS-06; R2D-12; final reconciliation of all source requests.
  - Write one new response mapping every original reviewer item through the crosswalk below to the actual change
    or justified limitation. Preserve all earlier reports, task registers, responses and attachments.
  - Update claim pointers, selected artifact/source identities, protocol amendments and final assets. Run tests
    appropriate to changed methods, including the shared-noise identity checks; build and visually inspect article
    and supplement. Broaden testing when the changes or failures justify it, not by rerunning every old campaign.
  - Prepare a fresh verified referee increment matching the selected evidence and corrected PDFs. Record numerical
    checks, author approval and actual journal delivery separately.
  **Completion:** sources, estimands, values, units, figures, response and evidence agree; all author-dependent
  conditions are either fulfilled or still visibly open. Completion is a basis for reassessment, not acceptance.

## Complete source-request crosswalk

| Original request | Consolidated task(s) |
| :--- | :--- |
| R1D-BTS-01 | R5-BTS-02 |
| R1D-BTS-02 | R5-BTS-01, R5-BTS-03 |
| R1D-BTS-03 | R5-BTS-04 |
| R1D-BTS-04 | R5-BTS-07, R5-BTS-08 |
| R1D-BTS-05 | R5-BTS-09 |
| R1D-BTS-06 | R5-BTS-10 |
| R1D-BTS-07 | R5-BTS-07 |
| R2D-01 | R5-BTS-03 |
| R2D-02 | R5-BTS-01 |
| R2D-03 | R5-BTS-02 |
| R2D-04 | R5-BTS-05 |
| R2D-05 | R5-BTS-07, R5-BTS-08 |
| R2D-06 | R5-BTS-06 |
| R2D-07 | R5-BTS-04 |
| R2D-08 | R5-BTS-02, R5-BTS-04, R5-BTS-08 |
| R2D-09 | R5-BTS-08 |
| R2D-10 | R5-BTS-09 |
| R2D-11 | R5-BTS-07 |
| R2D-12 | R5-BTS-10 |

## Order, scope and coordination

1. Freeze the new shared-noise protocol and primary estimator/population definitions (R5-BTS-01/02) **before** the
   targeted runs. Start author decisions (09) independently.
2. Complete the targeted test/layout reruns (01); process the headline and conditional validation (02).
3. Update the two-regime message and consistent conclusions (03/04). Edge and angle-aware studies (05/06) can
   proceed alongside, or be closed through their explicit limitation/omission alternatives.
4. Consolidate presentation and provenance/citations (07/08), then author gates (09) and final reconciliation (10).

Keep the 36-element BTS source lattice, protected inputs and old campaigns unchanged. Use new results directories.
The mandatory additional tracking is the focused shared-reading-noise second test and steering-layout reruns;
other numerical work is post-processing or explicitly conditional. Do not silently replace the NKM paper's shared
beam, jitter or correction assumptions; document any proposed change and its validation separately.

**Current completion state (updated 2026-10-31): 6 of 10 consolidated tasks done (01–06); 08 in progress; 07 in progress; 09 awaits author decisions; 10 pending.** All 19 original top-level requests are mapped.
