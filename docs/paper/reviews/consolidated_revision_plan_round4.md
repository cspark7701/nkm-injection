# Consolidated revision plan — round 4 (Reviewers 1 and 2)

Split on 2026-10-19 from the [round-3 plan](consolidated_revision_plan_round3.md), where this section was appended on
2026-10-16; its content is unchanged apart from cross-references. The round-3 plan (E1–E11, executed in milestones
211–222) and its [response](author_response_round3.md) remain the completed round-3 record.

Manuscript: `docs/paper/paper.tex` (PRAB REVTeX 4.2) as revised in round 3 (E1–E11).

Inputs:
- [Reviewer 1, round 4](reviewer1_round4_20261016_report.md) and its [register](reviewer1_round4_20261016_revision_tasks.md):
  R1D-01 to R1D-08. Recommendation: major revision focused on attribution and internal consistency.
- [Reviewer 2, round 4](reviewer2_report_round4.md): R2d-1 to R2d-7. Recommendation: major revision of limited scope.

## Status


Consolidated 2026-10-16 from [Reviewer 1 round 4](reviewer1_round4_20261016_report.md),
[R1D-01–08](reviewer1_round4_20261016_revision_tasks.md), and
[Reviewer 2 round 4](reviewer2_report_round4.md), R2d-1–7.
This is the current execution queue. **Execution authorised 2026-10-19; the State column records progress.**
The historical E1–E11 specification in the [round-3 plan](consolidated_revision_plan_round3.md) and its response remain the completed round-3 record.
No fifth review round or completed revision response is implied.

### Shared decisions and limits

Both reviewers credit the modelling core and require evidence-based attribution of the NKM–dipole deficit,
a tested operating-point comparison and a current-point pulse calculation. Reviewer 1 additionally requires
clear diagnostic/production-launch scope and physical/numerical loss classification. Correlations do not establish
causation; no arbitrary new ring count, commissioning experiment or universal efficiency target is imposed.
Local access has been checked for all 235 artifact keys; no new access simulation is needed.

| ID | State | Work package and mapped requests | Dependencies | Required output / completion gate |
| :--- | :--- | :--- | :--- | :--- |
| F1 | Done (milestone 236) | Freeze adopted model, point candidates, physical error-class grouping, seeds/particles/ring identities and paired estimands. Supports R1D-01/02/03/05/08 and R2d-1/2/3/4. | Authorization | New protocol/source identity; current point retained until an explicit decision. All-off includes corrected rings and declared nominal model; disabled errors do not alter latent random draws. |
| F2 | Done (milestone 241) | Paired causal ablation at zero booster jitter: all-off, full zero-jitter budget, each class alone, each class omitted. R1D-01; R2d-1. | F1 | Per-model capture, paired NKM-minus-dipole effects and uncertainty; interactions acknowledged, no forced additive decomposition. Same 50 seed-42 draws, particles and rings; no inference from unpaired hierarchy-row subtraction. |
| F2v | Done (milestone 243) | Declared post hoc sensitivity: ideal static steering in both planes at the current point, zero-jitter and full budgets (author-approved 2026-10-20). | F2, F3 | Paired with E7 references; sensitivity only, production x-only steering stays headline; no BTS lattice change. |
| F3 | Done (milestone 242; current point retained) | Paired current/earlier/extremum-centred point test at zero/full budget, feasible septum/root checks and recalibrated controls. R1D-02; R2d-2. | F1; F2 informs interpretation | Held-out comparisons and explicit adopted-point decision. If reselecting: declare error-inclusive objective, extend feasible binding bounds, separate training/validation and retain boundary fractions. Honest limited-scope retention is permitted. |
| F4 | Done (milestone 237) | Signed/physical associations for both models and their paired difference; zero-capture/conditional summaries, jitter rows and interval definitions. R1D-05/07; R2d-4/7. | F1; F2/F3 for final narrative | Predictors/signs, multiplicity scope, denominators and bootstrap units recorded. Correlation cannot substitute for F2. A central 95% lower endpoint is labelled conservative if used for a one-sided test. |
| F5 | Done (milestone 239) | Locate losses in selected zero-capture cases/ring 5501, report coupling scope, define numerical-domain/conductor guard and qualify chromaticity inference. R1D-04; R2d-5. | F1; final interpretation after F3 | Plane/location/turn and counts reconcile with existing categories; physical boundary distinguished from numerical rejection. Reuse raw diagnostics; rerun only insufficiently resolved representative cases. Controlled chromaticity check or reduced claim, not mandatory global retuning. |
| F6 | Done (milestones 238, 244) | Septum dispersion and fit/launch scope: D/D', within-bunch/shot angular contributions, empirical eta fit and synthetic-versus-production accuracy wording. R1D-06; R2d-6/7. | F1; adopted-point decision F3 for dependent numbers | Explicit units, assumptions and launch identities. Discuss companion dispersion-free transport as an alternative, without equating it to validated ring capture. Scope wording can avoid an unnecessary new scaling campaign. |
| F7 | Done (milestone 244) | Pulse and transparency consistency at the adopted point/strength; native return positions/kicks, allowance, finite-support timing bounds, correct rescaling laws. R1D-03/07; R2d-3/7. | **F3 point decision**; F6 allowance definition | Current-point source artifacts/macros/manifest checks; common angular allowance; quantities with nonlinear strength dependence re-evaluated appropriately. Historical S=0.85 diagnostics remain labelled. |
| F8 | Done (milestone 245) | Rewrite abstract/synthesis/discussion/conclusions and editorial corrections from F2–F7; restrict novelty, label historical figures, margin-fit degeneracy and dates. R1D-01/06/07; R2d-1/2/5/6/7. | F2–F7 | Every principal claim has the correct paired evidence and point identity. Poor capture may remain; no requirement to improve the result. Tuning gains keep boundary limitation unless resolved. |
| F9 | Pending | Final response to both round-4 reports, ledger/manifest/provenance, frozen evidence rebuild, both PRAB layouts and supplement, relevant/full checks as justified and author/access gates. R1D-08; final reconciliation of R2d-1–7. | F8 | New response preserves previous reviews/responses; point-aware checks and accessible selected evidence. Local checks distinct from external submission and acceptance. |

### Execution order and minimum additional computation

F1 precedes any study. F2 and F3 share latent draws and can be prepared together; F4–F6 can reuse current data while
that work runs. **F7 follows the F3 decision**, because a point change invalidates pulse/strength-specific results.
This refines Reviewer 2's suggested early pulse calculation to avoid immediately repeating it. Then F8 and F9.
No automatic full-campaign rerun: recompute only results dependent on an adopted-point/model change. If a new point
is adopted, audit the chamber, window, long-turn checks, controls, corrected-ring validation, robust ensembles,
tuning, pulse and transparency for dependencies; regenerate affected headline evidence before final packaging.
Retain old campaigns and use new output directories. Never overwrite protected scientific source inputs.

### Author decisions and unresolved inputs

- Retain the current point as a no-injection-error selection or authorize error-inclusive re-selection after F3.
- Confirm final scientific wording, title/authorship/declarations and actual attachment access/delivery before submission.
- Do not invent chamber materials, corrected-ring capabilities, funding, a compensation design or a DOI.
- Preserve the original BTS lattice. The companion's existing-dipole steering and dispersion-free alternative are
  separate studies; importing either into NKM capture requires explicit configuration identity and validation.

The present authorization covers review, planning and status-document maintenance only. No F task is started or
closed by the review's read-only artifact checks.

### Complete request crosswalk

| Review request | Consolidated packages (all pending) |
| :--- | :--- |
| R1D-01 | F1, F2, F8 |
| R1D-02 | F1, F3 |
| R1D-03 | F1, F7 |
| R1D-04 | F5 |
| R1D-05 | F1, F4 |
| R1D-06 | F6, F8 |
| R1D-07 | F4, F7, F8 |
| R1D-08 | F9 |
| R2d-1 | F1, F2, F8 |
| R2d-2 | F1, F3, F8 |
| R2d-3 | F1, F7 |
| R2d-4 | F4 |
| R2d-5 | F5, F8 |
| R2d-6 | F6, F8 |
| R2d-7 | F4, F6, F7, F8 |
