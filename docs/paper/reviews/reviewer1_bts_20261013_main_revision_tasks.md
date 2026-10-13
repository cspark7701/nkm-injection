# Reviewer 1 — BTS revision register (main-branch manuscript)

Date: 2026-10-13. Applies to the eight-page BTS draft on `main`, reviewed at `bee78914caa16945ef63dba8bf5205c434d0415c`. See the [report and manuscript hashes](reviewer1_bts_20261013_main_report.md). This register does not assess or supersede the later `bts` manuscript's reviews.

All tasks below are **open**. Their B-task mappings refer to the existing [BTS preparation plan](../../paper_bts/002_manuscript_tasks.md); mapping is not proof of completion. New analysis must be evaluated in the actual revision selected for review. Do not overwrite earlier review reports or regenerate protected scientific inputs. Save new runs separately and archive each executed revision under its next unique milestone number.

## Ordered overview

| Task | Priority | Report | Existing plan | Required outcome |
| :--- | :--- | :--- | :--- | :--- |
| R1-BTS-01 | Essential | §1, M4/M8 | B01/B11/B12 | Freeze the reviewed/revised branch and artifact identity |
| R1-BTS-02 | Essential | M4/M7 | Reopen B01 audit | Correct and verify the claim ledger and provenance |
| R1-BTS-03 | Essential | M1/M5 | B01 | Establish a supported novelty/closest-literature comparison |
| R1-BTS-04 | Essential | M2 | B02/B03 | Source the boundary, lattice, beam and constraints |
| R1-BTS-05 | Essential | M3 | B04/B07 | Validate transport and active-error coverage |
| R1-BTS-06 | Major | M1/M4 | B05 | Reproduce matching and assess all search outcomes fairly |
| R1-BTS-07 | Major | M6 | B06 | Validate normalized correction knobs or withdraw their claims |
| R1-BTS-08 | Essential | M1/M6 | B08/B10 | Complete a physical margin/correction comparison |
| R1-BTS-09 | Major | M7 | B09/B10 | Qualify statistical and error-budget conclusions |
| R1-BTS-10 | Essential | M8/§4 | B11/B12 | Deliver a complete article, evidence attachment and response |

## R1-BTS-01 — Fix manuscript and evidence version identity

**Dependencies:** none.

Choose the exact branch/commit and PDF for the next review. If using the later BTS article, preserve this report as a review of the early main draft rather than blindly applying already-resolved early-draft tasks. Record source, PDF and installed-asset hashes; state what changed between versions. Reconcile B01's completed status with stale manuscript/README statements that all B tasks are pending.

**Deliverables:** version record and claim/evidence selection linked from the revised manuscript.

**Acceptance:** every response and scientific result points to one identified manuscript version. The revision is not described as accepted merely because a different version has an internal acceptance report.

## R1-BTS-02 — Correct the evidence ledger and inventory

**Dependencies:** R1-BTS-01.

Audit every BC claim against exact files, JSON paths, code definitions and manuscript locations. Correct the nominal-plus-two-random start design; distinguish the successful infeasible candidate from the budget-limited failed candidate. Remove the inference of 33% feasible search-space volume. Correct the raw/normalized Jacobian distinction, OAT order and values, beta-only entrance perturbation, three main bends, the order-statistic CI path and actual failure thresholds. Replace erroneous byte sizes and global generating-commit claims with artifact-specific records.

Use asymmetric failure intervals and the actual Wilson values when cited. Explain rather than hide discrepancies between the inventory, scope, survey and TeX.

**Deliverables:** regenerated claim ledger, metadata inventory and discrepancy-resolution table.

**Acceptance:** all claimed verification labels are backed by the selected evidence; unresolved target/hardware provenance remains labelled unresolved. Earlier reports remain unchanged. A checker or explicit audit detects absent JSON keys and mismatched file digests.

## R1-BTS-03 — Establish the article's physical contribution and literature

**Dependencies:** R1-BTS-02.

Verify the closest BTS design, correction and tolerance studies against primary records and the actual passages supporting comparisons. Correct the MAX IV title mismatch; resolve the unverified PLS-II, RAON, Sirius and ESRF entries. Remove unsupported claims about universal sample budgets, target provenance and full six-dimensional mismatch. Cite the closest studies in the manuscript, not only in planning notes.

State one physical question answered by the final completed analysis: a reachable correction range, a margin benefit or a well-interpreted limitation. Disclose shared data/code/design with the NKM work.

**Deliverables:** verified comparison table, revised introduction and bounded contribution statement.

**Acceptance:** the contribution is distinct and justified without algorithm novelty or sample count being the sole basis. Quantitative literature comparisons carry primary-source support; unresolved references are omitted or qualified.

## R1-BTS-04 — Establish physical boundary and specifications

**Dependencies:** R1-BTS-03.

Identify entrance and exit locations, frames, target sources and intervening transport. Reconcile the AT/MAD-X element-order difference before comparing codes. Confirm or label the family limits, bores, apertures and 60 m ceiling as assumptions. Distinguish the historical 100/10 nm rad beam from the 7.67 nm rad horizontal design input. Specify the complete beam distribution, vertical/coupled covariance and energy spread for any transport result.

Convert K to gradient/pole field and convert beta/dispersion/orbit to physical beam clearance at declared aperture stations. A beta reduction must not be expressed as an equal physical stay-clear increase.

**Deliverables:** source-labelled configuration, boundary/geometry figure, magnet/beam/constraint table.

**Acceptance:** the reported target is derived at the stated BTS boundary or explicitly remains a parametric target. No assumed hardware setting is presented as measured. Equivalent-code studies use equivalent lattices.

## R1-BTS-05 — Validate transport and error coverage

**Dependencies:** R1-BTS-04.

Check independent transfer matrices, Twiss/dispersion propagation and symmetry/symplecticity under appropriate assumptions. Use zero-field/zero-error and physically isolated perturbations. Show which sampled errors alter orbit, covariance, coupling, envelope and transmission. Check rigidity/bending treatment, quadrupole translations and rolls. Supply coupled checks where uncoupled Twiss is insufficient. Exclude inactive downstream NKM diagnostics from BTS claims.

**Deliverables:** error coverage table, independent validation report and meaningful numerical checks with predeclared tolerances.

**Acceptance:** claimed active responses are verified; numerical near-zero responses are distinguished from absent effects and physical insensitivity. The historical offset/roll responses do not certify alignment/coupling tolerances. Invalid evaluations remain separately counted.

## R1-BTS-06 — Reproduce matching and compare search outcomes

**Dependencies:** R1-BTS-05.

Recompute baseline and selected optics using the frozen configuration. Preserve all starts, termination messages, objective values and independent feasibility records. Distinguish box-constrained search with post-selection from explicitly nonlinear-constrained optimization. Increase restart or iteration budgets only if a conclusion about search reliability needs them; three historical starts alone are descriptive evidence.

Report raw optical residuals and an engineering-relevant precision rather than emphasizing floating-point zeros. Revalidate rounded strengths if providing them as actionable settings.

**Deliverables:** candidate comparison table, validated settings, optics/dispersion/envelope profiles and termination records.

**Acceptance:** at least one design is independently feasible at the declared tolerances. Successful convergence, low residual and physical feasibility are not conflated. Any optimizer comparison uses equal physical conditions and accounts for invalid/failed starts.

## R1-BTS-07 — Demonstrate normalized correction knobs

**Dependencies:** R1-BTS-06.

Scale response rows by optical tolerances and columns by allowed/meaningful strength changes. Check finite-difference step convergence and rank, report singular values and null-space conventions, and validate finite corrections and actuator saturation. If measurements are assumed for correction, specify what is observable and how it would be estimated.

Do not reuse the archived mixed-unit condition number 1421.636 as proof of a dimensionless knob analysis. If knobs are outside the final scope, remove their achieved-performance claims and provide another completed physical contribution in R1-BTS-08.

**Deliverables:** normalized response definition/matrix, correction vectors and finite-step checks or an explicit claim withdrawal.

**Acceptance:** every retained correction claim is supported by finite reevaluation within strength and envelope limits. Local SVD orthogonality is not claimed to guarantee practical optical decoupling.

## R1-BTS-08 — Complete a meaningful design/correction comparison

**Dependencies:** R1-BTS-06, and R1-BTS-07 for correction claims.

Compare nominal matching with at least one justified margin or correction strategy under the same target, beam, apertures and error assumptions. Freeze training/tuning and evaluate on held-out static realizations with independent shot jitter. Show usable clearance, optical-error range or transmission, as appropriate to the contribution, and uncertainty on paired differences. Report a negative result if warranted.

For transmission claims, record particle count, distribution/truncation, seeds, energy spread, Twiss/covariance, loss criterion, aperture locations and first losses. Zero observed losses require a nonzero uncertainty/upper loss bound; they do not establish exactly zero physical failure probability.

**Deliverables:** validated design/strategy comparison and physical interpretation.

**Acceptance:** a completed result answers the contribution identified in R1-BTS-03. Claimed benefits are distinguishable from uncertainty and are not merely beta changes relabelled as clearance. Ring capture and MOGA are not compulsory. If MOGA is retained, normalize dispersion objectives and use the same physical validation as deterministic designs.

## R1-BTS-09 — Qualify precision and tolerance conclusions

**Dependencies:** R1-BTS-05/R1-BTS-08.

Keep historical and new-model datasets separate. Audit pooling compatibility, failure definitions, all failure records, interval methods and prefix outcomes. Specify Gaussian/truncated or other distributions, independence/correlations, static versus shot errors and any adaptive follow-up decision. Interpret OAT as mean absolute change of Mx+My under the selected amplitudes, distinct from the least-squares objective J.

Scan error amplitudes if claiming tolerance specifications, and justify physical/numerical acceptance thresholds. Size additional ensembles according to the required interval precision; do not automatically demand a larger campaign. Assess median, tail and rare-failure uncertainty separately.

**Deliverables:** statistical summary, active-error tolerance curves where claimed, and clearly limited engineering conclusions.

**Acceptance:** beta >60.01 m or Mx+My >2.05 is the identified historical rule. Exact rare-event intervals remain asymmetric; missed prefix targets remain reported. Sampling precision is not equated with accuracy of hardware or error-budget assumptions.

## R1-BTS-10 — Finish the manuscript and referee evidence package

**Dependencies:** R1-BTS-01–09.

Replace prospective analyses with completed results, then remove draft notes. Include the figures needed to understand the geometry, optics/margins and physical comparison. Reconcile abstract, tables, bibliography, ledger, discussion and conclusions. Verify current JKPS guidance and supply author-confirmed declarations.

Provide a separately accessible selected-output attachment with raw data, complete configurations, artifact-specific source/environment identity, hashes and numerical reproduction instructions. Confirm a fresh isolated PDF build and visual layout checks. Write a point-by-point response to this exact review, giving evidence links and claim withdrawals where relevant.

**Deliverables:** frozen article, response, claim ledger, source/evidence package and submission checklist.

**Acceptance:** no unresolved references/citations, unreported layout failures, contradictory claimed completion status or unsupported scientific claims. A referee can inspect/reproduce selected outputs without relying on personal absolute paths. All relevant numerical checks pass; template compilation alone is not a publication recommendation. No external submission or push is authorized by this task list.
