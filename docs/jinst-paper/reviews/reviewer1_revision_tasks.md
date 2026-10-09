# Reviewer 1 — Revision task register

Date: 2026-10-10. All tasks are **open/planned**, not executed by the review.
Decision: major revision; acceptance is not recommended for the reviewed version.
Read [the report](reviewer1_report.md) for evidence and scope.

This register supplements the [original journal tasks](../tasks/README.md), whose
completion records do not automatically close these new referee concerns. Review
comments refer to the current manuscript, not the older technical-framework draft.

Priority A means an acceptance blocker must be resolved by new evidence, a
quantitative bound, or an explicit change of claim/scope. Priority B means a
necessary reporting or submission correction. Suggested numerical budgets below
are starting points, not guaranteed convergence criteria. Do not launch expensive
Cartesian scans before deciding the physical model and precision targets.

## Ordered tasks

| ID | Priority | Work and deliverable | Dependencies | Acceptance test |
| :--- | :---: | :--- | :--- | :--- |
| R1-01 | A | Write a concise novelty/scope statement and comparison with the closest NLK/MIK studies; identify the lattice/version and distinguish design assumptions from machine specifications. | None | One demonstrated contribution beyond existing near-extremum injection ideas; no unsupported general or operational claim. |
| R1-02 | A | Audit finite-length transport, AT momentum/slope conventions, dimensionality, field normalization, polarity, interpolation and longitudinal coordinates; create `kicker_model_validation.md`. | R1-01 | Same-model comparisons converge at the operating point; omitted field/fringe/vertical and coordinate effects have quantitative bounds or claims are narrowed. Adding slices alone is insufficient. |
| R1-03 | A | Establish the signed-angle mechanism with centroid trajectories and accumulated kicks; select the principal model and rerun only affected controls/nominal/error studies. | R1-02 | The thin/finite-length reversal is explained with controlled comparisons; headline numbers and figures use the selected model or present an explicit model-uncertainty result. |
| R1-04 | A | Define a useful capture threshold, refine the angle/offset/scale window and validate selected points on fresh bunches; test angle cancellation against capture optimization. | R1-03 | Both threshold crossings and uncertainty are resolved; asymmetric width is stated; selected-point uncertainty is distinguished from pointwise grid intervals. |
| R1-05 | A | Source or parameterize the beam/error inputs; produce a full applied-budget table and jitter/alignment/beam-size tolerance curves; explain ideal static correction. | R1-01, R1-03 | A required stability range follows from a declared performance threshold; conditional driver ranking and static/shot-to-shot assumptions are explicit. |
| R1-06 | A | Validate final-point particle precision, long-turn survival, realistic or bounded aperture/ring-error sensitivity, and complete loss accounting; add geometry/phase-space diagrams. | R1-03, R1-04 | Numerical changes are below declared tolerances or conclusions are restricted; survival duration and DA scope are justified; original particle denominator reconciles with all loss categories. |
| R1-07 | A | Validate near-axis horizontal/vertical response using symmetry/multipole analysis or deterministic integration and sample/interpolation checks; distinguish one-pass estimates from multi-turn tracking. | R1-02 | Uncertainty floor on the aligned centroid is reported; emittance and differential kick are separate; large hypothetical control kicks are not presented as surviving operational oscillations. |
| R1-08 | A | Document pulse and timing assumptions, revolution period, residual-field and train effects; validate the timing surrogate or limit claims to ideal single-pass spatial-field transparency. | R1-01, R1-07 | Practical claims have supported temporal estimates; otherwise abstract/conclusions clearly exclude practical pulse transparency. |
| R1-09 | A | Complete or explicitly restrict paired controls; quantify nominal differences, finite-particle effects and tail-fraction precision; qualify correlations and interventions. | R1-03, R1-05 | Every comparison has matched IDs, sample size and paired uncertainty; no unmatched pooled subtraction or unqualified causal ranking. |
| R1-10 | B | Freeze accessible raw evidence, configuration, input hashes, software/generator versions and rebuild instructions; complete figure dependencies and current claim matrix. | R1-03–R1-09 for retained claims | A clean reviewer environment can inspect selected observations and rebuild assets without private/ignored backup paths; no invented public release/DOI. |
| R1-11 | B | Apply signed-kick/DA-extent/distance/notation corrections, parameter tables, geometry, abstract reduction, figure readability and JINST formatting. | R1-01; finalize after R1-10 | Text, captions, macros, bibliography and final PDF agree; figures readable in print; current official author instructions checked. |
| R1-12 | A | Prepare a point-by-point author response and final scientific acceptance checklist for a second review. | R1-01–R1-11 | Each major comment is closed by evidence or accepted claim restriction; no task is closed only because scripts/tests/PDF generation succeeded. |

## Study design details

### R1-02/R1-03: resolve the model before increasing ensemble sizes

Reuse `src/nkm_injection/injection_study.py`, `scripts/run_thick_nkm_check.py` and
`scripts/run_capture_robustness.py` where appropriate; extend them only with the
units/configurations needed for the accepted model. Start with centroid and
limiting-case tests, then paired bunches at the selected and nearby points.
Compare refinements such as 80/160/320 slices on the *same* field approximation;
these do not replace field-fidelity checks. Test zero field, uniform field,
midplane/nonzero-y and small nonzero-delta cases. Derive slope/canonical-momentum
relations before modifying chromatic scaling. Set an observable discrepancy
budget (capture and stored response), not only a reference-particle angle budget.

Do not execute a protected RADIA notebook to obtain more fields under this review
request. Any necessary new field calculation is separate simulation work with
explicit authorization and new outputs; protected notebooks/data remain unchanged.

### R1-04/R1-06: characterize the final operating point

Use a coarse grid for discovery and an adaptive grid near threshold crossings;
0.1 mrad or finer is a reasonable initial angular refinement. Report the actual
precision achieved. Check independent particle samples and selected nested budgets
(e.g. 500, 2000, 10000), balancing cost against the target confidence width.
500/2000/4000-turn comparisons are a useful starting sequence, but extend if
late losses remain significant. Apply to the final principal model, nominal point,
window edges and representative error realizations rather than every grid cell.

If actual chamber/ring error specifications cannot be obtained, use a clearly
hypothetical sensitivity envelope and bound the practical interpretation. No
universal requirement for ten ring seeds or a particular DA percentage reduction
is assumed. Ring and beam/error realizations are different sampling levels.

### R1-05/R1-09: convert an assumed budget into a design statement

Keep paired initial particles and latent error draws across changed jitter scales,
controls and interventions. Include zero, nominal and neighboring jitter values,
refining near an agreed performance threshold. Independently vary position and
angle jitter, document their covariance, and trace the BTS transport of both.
Resolve required jitter/alignment with confidence intervals and a low-capture
quantile, not just a mean at one assumed amplitude. If reporting a fraction of
realizations exceeding a threshold, show an interval and finite-particle sensitivity.

Do not demand more 550,000-sample optics ensembles by default: first show their
physical relevance to the capture question. Resampling saved observations can
answer statistical questions without rerunning particle physics.

### R1-07/R1-08: bound ideal transparency honestly

Use the exact symmetry as an analytical check, not a finite-sample mean as proof
of a sub-nanometre physical motion. Estimate the cubic coefficient and interpolation
residual in the beam-occupied region; include y and both kick components. Report
centroid mean/uncertainty, kick variance and emittance change separately. Test a
representative offset and realistic pulse residual if those effects are claimed.
A pulse field-scale change and an additive constant kick are different error models.

### R1-10/R1-11/R1-12: submission closure

Provide an evidence bundle accessible during review, preferably immutable and with
a persistent identifier when available. Keep generated outputs separate from
protected sources. Check every includegraphics/input dependency, actual figure
hash and macro against the selected final model. Update superseded claim rows,
submission checklist, cover letter and data availability statement after scientific
closure. Use JINST's current official style; verify metadata, funding and the
accuracy of the AI-assistance disclosure with the author.

The response file should contain, for each R1 ID: original concern, action or scope
restriction, revised section/figure, evidence/configuration path, numerical result
with uncertainty/tolerance, and remaining limitation. Archive each task's actual
execution under the next numerical milestone in `docs/exec-plans/completed/`.
This register does not authorize journal submission, remote publication or changes
to protected scientific inputs.
