# Reviewer 1 — ordered BTS main-branch round-2 revision tasks

Based on the [second main-branch report](reviewer1_bts_20261013_main_round2_report.md), 2026-10-13. **All tasks are open at review.** Prefix `R2-BTS` distinguishes this register from the recovered historical branch rounds and the executed `R1-BTS` main-branch tasks. This request creates the review and tasks; it does not execute manuscript revisions.

Do not overwrite previous reports, responses, source inputs or frozen campaign results. New numerical outputs must use new `results/` directories with configuration, units, seeds, budgets, environment, failures and validation tolerances. Archive executed tasks in the established completion sequence. Task completion alone does not imply journal acceptance.

## R2-BTS-01 — Freeze the reviewed version and reconcile contribution statements

Priority: major. Dependencies: none. Addresses M2 and presentation comment 3.

- Record the reviewed manuscript hashes and preserve the current campaign and 200-machine test results as historical evidence.
- Correct `literature_comparison.md`: the current alternative minimizes vertical peak beta, not clearance. Audit abstract, scope, evidence ledger and supporting notes for the same distinction.
- State the new research contribution and identify what will remain a parametric assumption. Separate original confirmatory results from post-review exploratory analyses.

Acceptance evidence: a versioned identity/claim update with no unsupported clearance-optimization or hardware claims; original assets retained and new work separately identified.

## R2-BTS-02 — Resolve the limiting-station mechanism

Priority: major. Dependencies: 01. Addresses M1 and M5.

- Export all four station/plane clearances and their decomposition into aperture, centroid, betatron/coupled size and dispersion contributions for both settings.
- Derive the fixed-entrance upper bound on minimum clearance. Reconstruct active station/plane frequencies for the original 600 paired shots.
- Explain 406 exactly equal shot minima and 93 equal machine averages; report paired quantiles, standard deviation and gain/loss frequencies, including the approximately -0.923 to +1.401 mm machine-average range.
- Present downstream-only clearance as a clearly labelled diagnostic alongside the full metric, without replacing the original estimand retrospectively.

Acceptance evidence: an auditable station-resolved table/figure and records that explain the aggregate near-zero mean, rather than inferring the active restriction from tied values alone.

## R2-BTS-03 — Bound transport approximation error in clearance units

Priority: major. Dependencies: 01–02. Addresses M3.

- Compare both independent affine and AT local maps at actual shot centroids under simultaneous gradient, offset, roll, dipole and momentum errors, at every aperture.
- Check finite-difference step and 40/80-step integration convergence. Explain the larger isolated offset/dipole derivative discrepancies and use observables with explicit units instead of a mixed-entry map norm alone.
- Validate propagated centroid and projected RMS against particle tracking with finite-sample uncertainty; test covariance effects from off-momentum/chromatic transport.
- Quantify paired-clearance bias, active-limit changes and sensitivity of the reported effect/interval. Correct approximation terms or qualify the result if accuracy is insufficient.

Acceptance evidence: errors in micrometres and a justified error budget relative to the tens-of-micrometres inference scale. A passing nominal map or generic 2% RMS check alone is insufficient.

## R2-BTS-04 — Check interior extrema and refine the beta objective

Priority: major. Dependencies: 01; finish before 05. Addresses M4.

- Evaluate beta/envelope inside thick quadrupoles, bends and drifts with analytic extrema or converged spatial subdivision.
- Compare refined maxima with the published boundary samples for both settings; verify matching and feasibility.
- If materially changed, rerun the alternative with the refined objective, retaining the original setting/results. Report actual bounds and optimizer termination, including q32's active lower bound.

Acceptance evidence: spatial convergence and the distinction between optimized sampled maxima and refined maxima. No changes to protected scientific inputs.

## R2-BTS-05 — Test a clearance-based design and a non-entrance-limited regime

Priority: major. Dependencies: 02–04. Addresses M1–M2.

- Compare reference, low-beta and clearance-based settings with identical exit constraints and actuator bounds, using a declared finite optimization budget and recording all outcomes.
- Treat entrance-ceiling degeneracy explicitly. Use a modest, predeclared parametric sweep of aperture restrictions or beam/target assumptions to expose at least one non-entrance-limited regime. Source-confirmed chamber geometry is preferable if available; do not label hypothetical restrictions as hardware.
- Define training/selection rules and physically meaningful effects before new evaluation. Freeze settings and use independent new machine/shot seeds for validation after the exploratory analyses; do not silently reuse the inspected test as a fresh holdout.
- Report conditional regimes where beta reduction helps, is immaterial or is counteracted by dispersion/orbit, without asserting global optimality. If no transferable mechanism emerges, explicitly reconsider the Research Article scope.

Acceptance evidence: a fair, reproducible strategy comparison and regime diagram/table explaining the physical mechanism. No compulsory large rare-tail campaign or experimental commissioning is imposed.

## R2-BTS-06 — Clarify precision and zero-loss event definitions

Priority: major clarification. Dependencies: 02, 03, 05. Addresses M5.

- Specify the primary effect, relevant effect scale and machine-level inferential target. Preserve the original interval and avoid converting failure to resolve a benefit into equivalence.
- Report heterogeneity and tail diagnostics supported by the independent-machine sample; label exploratory comparisons appropriately.
- Define the 1.4867% bound as a probability for a sampled three-shot block with 2,000 particles per shot, not an indefinitely operated machine.
- Retain explicit assumptions if reporting the descriptive particle-binomial bound, preferably in supplementary material. Add the exact-binomial reference. Increase independent machines only if justified by the scientific precision target.

Acceptance evidence: clear estimand/event statements, reproducible cluster uncertainty and limitations that remain attached to numerical claims.

## R2-BTS-07 — Recast the article around physical results and reconcile evidence

Priority: required editorial/scientific integration. Dependencies: 02–06.

- Give the limiting-station mechanism and validated design comparison the main Results/Discussion space. Move detailed historical pooling, prefix and legacy OAT reconstruction to supplementary material while preserving its provenance.
- Update figures with station/plane clearance information and paired uncertainty; give justified significant digits and standalone captions.
- Reconcile every changed claim with source artifacts, JSON pointers and the new campaign identity. Reverify beam-source numbers and missing bibliography metadata against primary publications.
- Produce a point-by-point response to this report, marking unresolved findings honestly. Build a new source/PDF package and check citations, local links and rendered layouts.

Acceptance evidence: an internally consistent article/supplement, complete claim-to-evidence mapping and clean build; no earlier reviews overwritten.

## R2-BTS-08 — Complete author declarations and referee access

Priority: submission blocker. Dependencies: 07; author input required.

- Obtain the deferred funding statement/grants, competing interests, acknowledgments, contributions and final scientific approval. Do not infer absent declarations as “none.”
- Preserve an accurate generative-assistance disclosure and author responsibility. Recheck the [official JKPS guidance](https://link.springer.com/journal/40042/submission-guidelines) at submission.
- Provide a stable reviewer-accessible evidence attachment or repository and match the availability statement to actual access. Keep historical records distinguishable from current conclusions.
- Record what is complete and what is still author-dependent. Public deposit or actual journal submission requires explicit authorization; preparing and validating an attachment does not.

Acceptance evidence: author-confirmed declarations, final approved manuscript and tested evidence access. This register does not authorize a journal submission or remote push.
