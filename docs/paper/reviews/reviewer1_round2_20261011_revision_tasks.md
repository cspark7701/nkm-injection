# Reviewer 1 — second-round revision tasks

Date: 2026-10-11  
Basis: [Second-round report](reviewer1_round2_20261011_report.md)  
Recommendation being addressed: focused major revision  
Status: **Proposed; none of these manuscript revisions was executed by this review.**

These tasks supplement the [first-round register](reviewer1_revision_tasks.md). They assess the revised three-dimensional model rather than restarting the old campaign. Preserve all previous reviews and responses. Save any new numerical results in a new results directory and register their provenance; do not overwrite scientific inputs or frozen evidence.

P1 means required to resolve a substantive review concern before submission. P2 means presentation or submission completeness. Numerical thresholds below must be justified against the observable; do not replace validation with an arbitrary particle-count target.

## Ordered register

| Order / ID | Priority | Concern | Work type | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 01 / R1B-01 | P1 | M2: survival duration and estimand | Existing-data analysis and text | None |
| 02 / R1B-02 | P1 | M1: trajectory approximation | Limited independent validation | None |
| 03 / R1B-03 | P1 | M4: correction and sampling | Implementation audit and text | None |
| 04 / R1B-04 | P1 | M3: jitter inference | Existing paired-data analysis | R1B-03 |
| 05 / R1B-05 | P1 | M5: pulse requirements | Analytic check; conditional tracking | R1B-01, R1B-02 |
| 06 / R1B-06 | P1 | M6: contribution and controls | Claim revision; conditional control check | R1B-02 |
| 07 / R1B-07 | P1 | M7: transparency | Existing-data/definition reconciliation | R1B-02 |
| 08 / R1B-08 | P2 | Presentation and uncertainty | Figure, caption and method edits | R1B-01, R1B-04, R1B-07 |
| 09 / R1B-09 | P2 | Referee-accessible evidence | Submission packaging | R1B-01 through R1B-08 |
| 10 / R1B-10 | P1 | Final scientific reconciliation | Build and review gate | All preceding tasks |

## 01 — R1B-01: repair survival reporting and scope the operating window

Replace the turn-count use of `\SurvLong` in `paper.tex` with the dedicated duration macro `\SurvTurns`; retain `\SurvLong` for the percentage. Recompute long-turn uncertainty from saved counts and identify the long-turn ensemble separately from the four-bunch validation ensemble. State that 93.0%, 89.6% and 89.5% are survival at 500, 2000 and 4000 turns in the long-turn study, with a 3.5 percentage-point late loss.

**Acceptance:** source and rebuilt PDF report 4000 turns; the long-turn nominal result includes particle count, seeds and a defined interval. Abstract, window captions, robustness section and conclusion agree that those studies use 500-turn survival. Either restrict the engineering claims to that duration or validate representative longer-turn boundary/degraded cases. Call uncorrected lattice-error/aperture results scenarios rather than bounds unless a bounding argument is supplied. No new long-run ensemble is mandatory if the claims are properly restricted.

## 02 — R1B-02: validate off-midplane transport independently

Compare the finite-slice map against an independent high-accuracy integration of the explicitly stated equations using the same filament field. Include the final nominal point, nonzero vertical position and angle, representative angular-window edges and energy offsets. Check slice count and integration span in both planes. Explain the paraxial momentum/slope convention, sign convention and sequential longitudinal-field update.

**Acceptance:** a concise validation table reports configurations, units, solver tolerances and exit-coordinate discrepancies in x, p_x, y and p_y. The selected numerical tolerance is demonstrably small relative to the reported window and stored-beam response. If discrepancies matter, fix the integrator and regenerate only affected evidence in a fresh directory; otherwise retain the campaign and document the accuracy limit. Do not equate exact field evaluation with exact particle tracking.

## 03 — R1B-03: document the correction and stochastic estimand

Audit the ideal-static-steering implementation and write the applied coordinate transformation. Specify which static reference-centroid components are removed and which optics/magnet/orbit errors remain. Classify static versus shot-dependent variables consistently, including energy and timing. Explain that the present realization distribution mixes machine and shot draws rather than repeatedly sampling shots on fixed machines.

**Acceptance:** replace “only the shot-to-shot errors remain”; table, algorithm and interpretation agree with the implementation. Remove the inference from small Twiss mismatch to negligible capture loss unless supported by a capture-level control. Describe rank correlations as model-conditioned associations. No nested Monte Carlo is required for a clearly stated joint-ensemble claim.

## 04 — R1B-04: quantify the paired jitter difference and soften the tolerance claim

Use the matching sample IDs in the corrected quarter- and zero-jitter files, excluding the negative-ID zero-error reference. Bootstrap the paired capture differences at the realization level with a fixed seed and record method/count. The present review's check gives quarter minus zero = +0.30 percentage points, percentile 95% interval −1.50 to +2.15, with 50 pairs, 10,000 resamples and seed 1729.

**Acceptance:** manuscript gives the paired result or a justified alternative and replaces “costs nothing” with a precision-limited statement. If claiming equivalence, declare an engineering loss margin and show the appropriate interval supports it. Present 0.125 mm / 0.05 mrad as a conditional candidate target unless a successful joint allocation supports a stronger requirement. Mean, median, lower quantile and fraction above 80% are not interchanged. Existing evidence can satisfy this task without new simulations.

## 05 — R1B-05: reconcile pulse phase, jitter and repeat-pass limits

Label the linear-rotation coordinates used by `pulse_macros` as illustrative, or replace them with selected-point native tracking. Identify the arbitrary one-tenth-window allowance as a design assumption. Define half-sine duration and injection phase and check both timing sensitivity and residual field at subsequent passages. At peak phase, `1 − cos(pi dt/tau)` spans approximately 7.7e−8 to 4.9e−6 over the stated ranges; an 8 microsecond pulse retains about 0.50 at the first return.

**Acceptance:** section 8, supporting note and generated numbers use consistent definitions and distinguish estimates from tracked observations. Give a compatible illustrative pulse/phase or explicitly leave feasibility outside scope. If claiming actual pulsed capture, validate it with time-dependent repeat-pass tracking. Retaining the ideal single-pass scope does not require a full hardware/pulse simulation.

## 06 — R1B-06: tighten mechanism, novelty and control interpretation

Separate longitudinal thin-map limitations from the corrected vertical-sign error. A vector map can represent the vertical kick. Explain the focusing/defocusing sign on the tested flank rather than asserting defocusing for every nonzero gradient. Restrict numerical tolerance statements to the selected KLS model and budget. Document which nominal quantities the thin controls match and which finite-length transport correlations they do not.

**Acceptance:** abstract, introduction contribution paragraph, discussion and conclusion make the same specific physical claim. Capture differences are called paired model comparisons unless a matched finite-length control isolates a pure nonlinearity effect. The vertical-aperture mechanism is presented as an interpretation unless a ring diagnostic demonstrates it. No new magnet design or global optimization is required.

## 07 — R1B-07: distinguish centroid symmetry from full beam transparency

Reconcile deterministic quadrature observables with the stored-beam tracking definitions. The tracked centroid amplitude uses the first 50 turns; the final emittance ratio uses turn 1000. State two seeds and 300 particles per tracked bunch. Describe the cubic term as leading order. If claiming the aligned beam is completely undisturbed, show the relevant moment change; otherwise restrict the statement to exact centroid cancellation under symmetry.

**Acceptance:** Figure 7 caption and plotted curves distinguish kick-spread centered emittance from total filamented growth and tracked final emittance. The abstract and conclusion use the same observable and scope. The 0.2 mm result is an assumed-model response scale, not an unconditional hardware specification. Use saved aligned/offset data where adequate.

## 08 — R1B-08: improve statistical and figure reporting

Identify the interval method and sampling unit for every headline result and caption. Qualify the selection-noise statement as independent validation of a selected grid point. Improve visibility of the nominal paired-control gap, for example with an inset, while keeping the kicker-off reference. Make lattice version, distributions, apertures, vertical emittance ratio and observation points easy to locate.

**Acceptance:** readers can distinguish particle uncertainty, between-realization uncertainty and model/systematic limitations. Captions accurately describe generated curves and samples. A rendered PDF inspection finds no misleading units, illegible legends or conflicting turn labels.

## 09 — R1B-09: prepare a usable evidence package for referees

Refresh the claim-to-evidence table after the substantive revisions and create a new frozen bundle only if evidence changes. Supply code revision, source-input hashes, configurations, seeds, environment and regeneration instructions. Check access through the intended submission attachment or archive; do not merely promise access later.

**Acceptance:** the selected bundle verifies against its manifest and can regenerate the revised numerical tables/macros. Clearly distinguish legacy optics evidence from the revised three-dimensional capture studies. Document access in the data/code availability statement. Preserve old bundles and do not invent a DOI or claim publication before it exists.

## 10 — R1B-10: build and write a new round-two response

After revisions, rebuild the article from selected evidence, inspect the PDF and reconcile abstract/conclusion numbers and claim scope. Run relevant numerical tests only for implementation changes; perform the publication consistency checks for document/evidence changes. Create a new dated round-two author response linking each R1B task and new evidence.

**Acceptance:** the PDF includes the corrected duration, conditional survival/window definitions, precise transparency observable and defensible jitter/pulse statements. All task outcomes cite actual evidence or explain a deliberately narrowed claim. Old reviews and `author_response.md` remain unchanged. Protected scientific inputs are unchanged, results are separate from sources, and git status plus the task archive record the completed work. Completion supports a new review; it does not predetermine journal acceptance.

## Work not required merely to close this review

Measured prototype data, an arbitrarily larger Monte Carlo campaign, a full corrected as-built ring, a new global optimizer and a comprehensive time-dependent pulsed-magnet model are not blanket requirements. They become necessary only if the manuscript expands its claims to measured hardware performance, operational reliability, or validated pulsed capture. The present tasks allow a defensible, explicitly conditional physics article.
