# Reviewer 1 — fourth-round manuscript assessment

Date: 2026-10-16. Target: Physical Review Accelerators and Beams (PRAB).
Manuscript: *Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design lattice*.
Reviewed repository checkpoint: `e2e7ff63019138e4c4db1e7712043248f2cadf3c`.
This is an internal pre-submission referee-style assessment, not a journal decision or an external referee endorsement.

## Recommendation

**Major revision, focused on attribution and internal consistency. I do not recommend acceptance of the present version.**

The finite-length comparison is a credible research contribution when scoped to its tested geometry, launches and
error allowance. The independent trajectory check, explicit chamber, corrected rings, long-turn checks and
manufacturing-error analysis are substantial improvements. Poor robust capture is a publishable negative result;
it is not a reason to demand a better efficiency. The unresolved issue is that the paper's principal engineering
recommendation does not follow from its paired evidence. A consistent pulse calculation and a supported explanation
of the capture deficit are necessary before I would reconsider acceptance. Completing a checklist cannot guarantee
a journal decision.

## Materials and limits of this review

I read the current TeX article and supplement, extracted the 30-page article PDF, inspected the robustness and
normalised-error figures, read the earlier Reviewer 1 reports/round-3 response and Reviewer 2's fourth-round report,
and inspected the selected manifest, installed macros and existing zero/full-jitter raw records. The two-column
preview has 15 pages; the supplement has six. All **235 artifact keys** in the round-3 manifest resolve locally and
match their recorded SHA-256 digests. This is a fresh identity check of those files, not a new archive rebuild or
independent validation of every physical result. I checked sample IDs and beam seeds for the paired jitter rows;
ring IDs also agree. I did not rerun tracking, optimization, uncertainty resampling or the test suite. Scientific
revision tasks below have not been executed.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `9be5b6edd5b4de923eb55f4d376fdc9f534f68c55c80114af18ff6e9bd7bf5f7` |
| `paper.pdf` | `c0887f7f4d8c371e245d1a14dd02821c277a6e91c9708c99b6c9a407b16ac307` |
| `paper.bib` | `b68c8a692ea6715338ed752ab3a66782c6b2e0eebe2ff4f7be24ac292789def2` |
| `paper_twocolumn.pdf` | `2cda75dfd70fb9a2884627c9261344bc89b80ac4207896eb79ed28af86c26b1f` |
| `supplement.tex` | `13a3119f8128f9c2380e4b607bad3b5edf435eb51e89de8c2bc9820302cd4622` |
| `supplement.pdf` | `aa810a3a740db53e0ce8795be3e5807b92fcbc3918d7e61cb4d4b156c0e99673` |
| `revision_manifest_round3.json` | `6c368b7fda7927c0179b8cdd14173c51141fb6891fda65ccce0843f60d7c20fc` |

## Status of my third-round requests

| Previous request | Fourth-round assessment |
| :--- | :--- |
| R1C-01 Evidence access | Closed locally: selected artifacts are accessible; actual referee delivery remains an author action. |
| R1C-02 Literature/contribution | Substantially addressed: segmented tracking is credited to Sun et al.; retain the specific approximation-error contribution rather than an exhaustive novelty claim. |
| R1C-03 Normalised scaling | Addressed for the two tested families; interpretation must retain the launch recipe and distinguish this diagnostic from a matched-production trajectory. |
| R1C-04 Robustness synthesis | Execution completed in E8, but the resulting causal attribution requires correction; see M1. |
| R1C-05 Transparency units | Addressed; a separate selected-strength consistency issue remains in M5. |
| R1C-06 Noninferiority | Declared-margin wording addressed. Specify the interval convention; see M6. |
| R1C-07 Article structure | Addressed by the supplement. Further wholesale restructuring is unnecessary. |
| R1C-08 Reconciliation | Round-3 execution recorded; it did not catch mixed operating-point inputs in the pulse section. A new reconciliation must follow the requested corrections. |

E1–E11 remain completed execution records. A later scientific objection does not mean those tasks were never run.

## Major comments

### M1 — Identify the NKM-specific deficit with paired contrasts

The abstract and Sections 7.2, 9 and 10 attribute the distinguishing losses chiefly to booster angle jitter.
Existing **paired seed-42 data**, 50 realizations with 200 particles each, give:

| Quantity [% except differences] | No booster jitter | Full booster jitter | Full minus zero [points] |
| :--- | ---: | ---: | ---: |
| NKM mean | 40.13 | 19.46 | −20.67 |
| Dipole mean | 68.46 | 48.25 | −20.21 |
| NKM minus dipole [points] | −28.33 | −28.79 | −0.46 |

These numbers are arithmetic means recomputed from `e7_jitter_0` and `e7_seed42`, not from the unpaired
150-realization headline. Thus most of the observed model gap already exists at zero booster jitter. The small
change in the gap has no uncertainty analysis here and is not evidence of exact equality or absence of interaction.
A significant association with the NKM's absolute capture does not identify a driver of the *paired model difference*.
Conversely, the roughly four-point difference in the separate corrected-ring-only population cannot be subtracted
from this table as a paired causal effect.

I agree with Reviewer 2's R2d-1 request for paired all-off, each-class-alone and leave-one-class-out comparisons at
zero booster jitter. Keep static errors, particle variates, ring IDs and model calibration paired. Group errors by
physical action, record what each group contains, and include the kicker-to-orbit displacement and field-scale
terms. Analyse the NKM-minus-dipole difference as well as each capture mean. Nonlinear interactions mean alone and
leave-out effects need not add to the total; do not force an additive error budget. The offset-on-a-steep-flank
explanation is plausible, not yet established. Report it only if the evidence supports it. Retain the legitimate
separate conclusion that jitter reduces absolute capture for both models.

### M2 — Test the operating-point recommendation without selection leakage

The point was selected without injection errors. The manuscript then recommends an error-inclusive choice as
though its preference for a wider angular window were demonstrated. It is not. A wider ideal-ring window alone is
not a robust-capture objective. Compare the selected, earlier and an extremum-centred feasible point using the
same zero-jitter and full-budget machines and particles. Recalibrate the uniform control consistently at each
point and report the paired changes and uncertainty. Check the septum-clearance rule and the existence of the
matched root for every candidate.

A targeted comparison and an honest limitation are sufficient; a globally optimal design is not required. If
re-selection is performed, declare the objective/bounds first, extend a binding search edge where physically
feasible, separate selection and held-out validation samples, and propagate the final identity to all dependent
studies. A flat p10 ranking with 100 particles per ring is not evidence of a unique optimum. Keep the 28% tuning
boundary fraction visible until resolved. Avoid a costly full campaign rerun unless the adopted point changes.

### M3 — Reconcile the pulse calculation with the adopted point

This is a directly verifiable consistency defect. The manifest's `round2_pulse` still selects
`results/journal_campaign_03/d12_final_pulse.json`. Installed macros give a residual allowance of **0.076 mrad**,
while the scaling section uses **0.044 mrad**, both described as a tenth of the angular-window width. They concern
different operating points. The return positions/kicks and pulse bounds must be recomputed or explicitly labelled
as a historical example; the present text presents them as current. For the current-point pulse claim, use the
adopted final point, current chamber and native return trajectory, and validate the finite-support half-sine and
arrival-time convention. Add a provenance check that tests operating-point identity, not only byte hashes.
Compute this after any M2 point decision. Spatial single-pass capture is not a time-dependent pulse validation.

### M4 — Explain dynamical losses and distinguish numerical-domain rejection

The zero median and large zero-capture mass deserve an explicit physical diagnostic, not only an ECDF.
`ring_elsewhere` is a bookkeeping category. Inspect plane, element/region and turn for representative zero-capture
realizations and ring 5501, and report their dependence on ring identity and signed kicker offset. Reuse recorded
loss data when sufficient; rerun only the cases requiring finer diagnostics. Distinguish the cause that generated
a trajectory from the boundary at which it is lost. State residual coupling/vertical beam consequences and close
the promise about coupling in Section 5. Ten-ring correlations do not identify a chromaticity mechanism; either
add a controlled check or reduce that inference.

Define `outside_field_map` and the 1 mm conductor guard relative to the declared chamber. A numerical-domain
rejection must be reported separately from a demonstrated material aperture loss. No arbitrary increase in the
number of rings is required, provided conclusions remain conditional on the supplied ten scenarios.

### M5 — Use signed predictors and consistent displacement/strength conventions

The magnitude-only rank analysis can conceal one-sided sensitivity on the asymmetric operating window. Report
signed predictors or a physically defined predicted centroid kick, including the appropriate relative
kicker-to-orbit displacement sign. Show both models and the paired difference; control ring identity, disclose the
exploratory/multiple-testing scope, and avoid causal claims from correlations. Confirm that the control and NKM
share the intended amplitude-error convention and are calibrated under the same nominal rule. These are
controlled model comparisons, not proof that either complete injection scheme is optimal.

Transparency tables/near-axis coefficients still use the earlier S=0.85 while the selected point uses S=0.95.
State the reference strength beside every quoted quantity, or regenerate/rescale with the proper dependence:
centroid kicks/linear coefficients scale with field, while emittance/moment changes need their own formula or
re-evaluation. Do not apply one linear factor to every observable. Keep simultaneous construction errors distinct
from the single-wire limits and from the placement/common-amplitude joint capture study.

## Other revisions and scope

### M6 — Quantitative interpretation and presentation

- The eta^1.46 fit is an empirical descriptor of the stated range and launch family, not a universal asymptotic law.
  The synthetic off-midplane comparison at the kick extremum is not identical to the matched injected-centroid
  trajectory. Restrict the abstract's selected-point accuracy wording accordingly, or supply that direct comparison.
  The opening claim that thin-map accuracy "has not been quantified" is broader than the literature audit proves.
  A specific statement about this geometry and operating regime is sufficient. Sun et al.'s earlier optimization
  paper is verified at its [official APS record](https://journals.aps.org/prab/abstract/10.1103/PhysRevAccelBeams.23.010702);
  that record is not an exhaustive novelty search.
- State the septum D=0.080868 m and D'=0.047472 and their contribution to angular spread/jitter. The dispersion-free
  BTS result in the companion is an alternative transport study, not evidence of ring capture. Importing it would
  require a consistent beam/configuration and new ring validation; discussion alone is adequate here.
- A central 95% interval's lower endpoint is a conservative 97.5% one-sided bound, not a nominal 95% one-sided
  bound. Specify whether the acceptable-loss test intentionally uses that convention or a fifth percentile.
  This is a definition/wording issue, not a demand to convert a failed test into a passed one.
- Report zero-capture fraction and capture conditional on nonzero survival for both models, alongside the
  unconditional means. Preserve denominators and distinguish particles, joint draws and ring scenarios.
- Label historical sensitivity figures with their actual point; keep plane/model-specific jitter rows, the
  degenerate margin fit, dates and captions consistent. Retain the separate supplement and PRAB layouts.

### M7 — Evidence and submission

Local evidence access is now demonstrated; requiring a DOI would add no scientific validity. Prepare a new frozen
attachment only after scientific corrections, and verify its archived-source rebuild and operating-point consistency.
The current submission checklist and review index still contain obsolete pending round-3 statements and old page
counts/results. Correct current status documents without rewriting dated reviewer reports or historical responses.
Final author approval and actual evidence delivery remain separate from software execution. Do not claim journal
acceptance or delivery based on local file existence.

## Requested disposition

Complete [R1D-01–08](reviewer1_round4_20261016_revision_tasks.md) together with Reviewer 2's R2d-1–7 through the
[round-3 consolidated follow-up plan](consolidated_revision_plan_round3.md#round-4-follow-up-to-the-round-3-manuscript).
I would reconsider the paper after the paired attribution and operating-point evidence, consistent point-dependent
quantities and reconciled claims are available. Neither hardware commissioning, a new global optimizer nor a new
large ring ensemble is a prerequisite for a carefully scoped simulation article.
