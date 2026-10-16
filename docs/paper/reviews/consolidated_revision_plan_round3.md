# Consolidated revision plan — round 3 (Reviewers 1 and 2)

**Status updated 2026-10-16:** E1–E11 below were executed in milestones 211–222;
see [the round-3 response](author_response_round3.md). The round-4 assessments of
that revised manuscript identify new work. Their consolidated **F1–F9 follow-up**
is appended below, all pending. This retains the requested round-3 plan as the
entry point; it does not relabel completed E tasks or imply execution of F tasks.

Date: 2026-10-13. Manuscript: `docs/paper/paper.tex` (PRAB REVTeX 4.2) at commit `139c7c7`, as reviewed.

Inputs:
- [Reviewer 1, round 3](reviewer1_round3_20261012_report.md) and its [register](reviewer1_round3_20261012_revision_tasks.md):
  R1C-01 to R1C-08. Recommendation: focused major revision.
- [Reviewer 2, round 3](reviewer2_report_round3.md): R2c-1 to R2c-9. Recommendation: major revision focused on the
  robustness section.

The round-1 and round-2 plans and responses stay unchanged.

## How the two reviews relate

Both reviewers accept the physics core: the finite-length comparison, the independent trajectory check, the
transparency observables and the pulse scope. Neither reopens the round-2 tasks, and both recommend focused major
revision.

They concentrate on different gaps:

- **Reviewer 1** asks for:
  - positioning against Sun et al., PRAB 23, 010702 (2020), which already used segmented finite-field tracking
    (R1C-02);
  - a normalised error result for the sagitta scaling (R1C-03);
  - a physical synthesis of the nominal-to-robust hierarchy (R1C-04);
  - unit and statistical-wording fixes (R1C-05, R1C-06);
  - a streamlined article (R1C-07).

  Reviewer 1 could not find the campaign-03 evidence (R1C-01).
- **Reviewer 2** finds that the low robust capture (14.8 % mean, 1.0 % median) is mostly produced by three modelling
  choices:
  - an operating point never re-selected for the design beam;
  - rings whose orbit correction stops at a 100 µm criterion, without optics correction;
  - an NKM chamber that would enclose its own conductors.

  Reviewer 2 asks for one rerun after fixing these (R2c-1 to R2c-5). Reviewer 2 also verified all 205 round-2
  artifacts and the bundle hash locally, which settles R1C-01 as an access-documentation task.

## Adopted resolution where the reviewers differ

| Topic | Reviewer 1 | Reviewer 2 | Adopted |
| :--- | :--- | :--- | :--- |
| New simulations | No new full campaign or larger seed counts merely for size | One rerun of the robustness study after fixing three identified model defects | One rerun, justified by the defects and not by sample size. The populations are unchanged (10 rings, 150 joint draws, 50 per jitter level), so Reviewer 1's restriction holds. |
| Robustness hierarchy | Explain the current hierarchy from existing data | Explain it on the corrected model; the current one mixes artefacts | Execute R1C-04 on the rerun results (E8). The current numbers are kept in the response as the documented round-2 state, not rewritten. |
| Ring correction | Not raised (a finite declared population is acceptable) | Converge the orbit, add β-beat and coupling correction, or relabel the population | Orbit to convergence and β-beat correction with individual quadrupoles (feasible in the model). Coupling correction only if skew correctors are supplied (B1); otherwise state its absence. Ring 5501 is diagnosed, not dropped. |
| Evidence access | Required before re-review | Verified locally (205/205 hashes, bundle `0e07de5f…`) | Document the access route now (E1). A new round-3 bundle follows the rerun (E11). |
| Article length | Streamline; move derivative tables and secondary cases to a supplement | Adds a chamber justification, a wire Monte Carlo and leakage | Main text keeps the mechanism → accuracy → chamber → robustness → transparency chain. Full derivative tables, the 100 nm diagnostics and the procedures move to a supplement (E10). |
| Wire tolerances | Keep as single-error sensitivities; no compensation demonstration required | Simultaneous-error Monte Carlo recommended (B) | Do the small Monte Carlo (cheap, E9). State the compensation consequence without claiming a compensation design. |

## Author inputs needed

Each input has a default if it is unavailable.

| ID | Input | Needed by | Default if unavailable |
| :--- | :--- | :--- | :--- |
| B1 | Correction hardware of the KLS design beyond the 120 HVC elements: sextupole trim windings (H/V/skew), individual quadrupole supplies | E5 | Orbit: the 120 HVC only. β-beat: individual quadrupoles, stated as an assumption. Coupling: none, stated. |
| B2 | Envisaged NKM vacuum chamber: material, inner height, wall thickness, coating | E4, E9 | Flat ceramic, conductors outside, 1 mm wall, inner half-height = inner-wire y − conductor radius − wall (≈ 3.3 mm); scan 3–4.3 mm |
| B3 | Septum blade for the NKM scheme: 2 mm (current study) or the KLS 1 mm in-vacuum thin septum | E6 | Report both |
| B4 | Accepted septum clearance in σ_x of the design beam | E6 | 3σ, with 5σ as a check |
| B5 | Orbit and β-beat residual targets of the KLS commissioning simulations (Kim et al., IPAC'25) | E5 | Converged SVD residual and β-beat below a declared 2 % rms target; reported as achieved |

## Consolidated tasks in execution order

Each task is archived under the next milestone number (from 211) and committed. New results go to
`results/journal_campaign_04/`, while `journal_campaign_03` stays frozen as the round-2 evidence. Compute estimates
scale from the round-2 logs with 8 workers: one joint-error seed about 10 min, one jitter level about 10 min, tuning
about 25 min, corrected-ring chamber runs about 1.5 h.

| E | Covers | Work | Acceptance | Sim / cost |
| :--- | :--- | :--- | :--- | :--- |
| E1 | R1C-01 | Evidence access: document the location, archive hash, inventory and verification command of the round-2 bundle, and record the local re-verification (205/205, `0e07de5f…`). | Access entry point in `round2_reproduction.md` and the response; verification reproducible by command | No |
| E2 | R1C-02 | Literature and contribution: read Sun et al. (2020) and any directly overlapping NLK modelling work. Compare questions, approximations, geometry and observables. Restate the contribution as a quantified finite-length approximation-error and sensitivity result, not as finite-field tracking itself. | Comparison paragraph; abstract, introduction, discussion and cover letter consistent; no invention claim | No |
| E3 | R1C-03 | Scaling result from existing data: define K, w and the reference path in the main text; normalised error \|Δp_x\|/\|K\| for thin and sliced maps per configuration family; residual spread at comparable η; relate it to a declared angular-response accuracy. | Normalised-error figure or table; claim scoped to the tested families | No (post-processing) |
| E4 | R2c-1; B2 | Feasible NKM chamber: flat, conductors outside, stated wall; half-height scan 3–4.3 mm; normalised aperture against arc and centre bend; replaces the 30 × 15 mm assumption and the 1 mm conductor rule. Eddy and coating estimates of section 8 use this chamber. | Chamber defined and justified; table 1 aperture corrected | Small (config + tests) |
| E5 | R2c-2; B1, B5 | Ring population: rebuild the same ten error seeds (5501–5510) with SVD orbit correction to convergence, β-beat correction with individual quadrupoles (response-matrix fit), tune correction, and coupling correction if B1 allows. Report residuals per seed. Diagnose ring 5501 (DA −7.0/+7.5 mm) with tune, β-beat and resonance checks. | Residual and DA tables per seed; 5501 explained; the population name matches the correction actually applied | Yes, ~2–3 h |
| E6 | R2c-3; B3, B4 | Operating point: re-select with the design beam and an explicit septum clearance rule (2 mm and 1 mm blade). Knobs: x_inj with re-matched x′, and S. Objective: tenth percentile (primary) and mean capture over the E5 population with the E4 chamber. Select with fixed seeds, then validate on fresh particles. Recompute the window on the ideal ring. | New point with selection rule and validation; window regenerated; old point kept as a reference row | Yes, ~3–4 h |
| E7 | R2c-4, R2c-8 | One robustness rerun with E4–E6: joint ensembles (3 seeds × 50, NKM and dipole), jitter scan (0–1, x and x′ only), tuning with matched knobs and a range wide enough that no optimum sits at a boundary (report the boundary fraction). Add a ring-cluster bootstrap and leave-one-ring-out ranges, and the paired NKM − dipole robust difference. | Section 7.2 regenerated; tuning boundary fraction reported; ring-population dependence visible | Yes, ~3 h; overnight queue |
| E8 | R1C-04, R2c-5, R1C-06 | Physical synthesis on the E7 results: the hierarchy table (beam, aperture, ring population, errors, counts, duration per condition); injected amplitude against the per-ring DA margin; NKM against dipole under errors; required DA margin or amplitude for a stated capture target (scan of the DA margin, if cheap). Restate the jitter inference as one-sided noninferiority against the declared −1-point margin. Remove "predeclared" unless it can be dated. | Discussion states the limiting mechanism with data; no causal claim from rank correlations; noninferiority wording consistent in manuscript, notes and response | Small |
| E9 | R1C-05, R2c-6, R2c-7 | Transparency: Δε/ε notation and units for the aligned moments; a simultaneous wire-placement and current-error Monte Carlo at 10, 25 and 50 µm and at 10⁻⁴/10⁻³, giving A_x and A_y distributions and the compensation requirement; septum leakage at the NKM-scheme stored-orbit distance from the published leakage profile, or the required shielding factor. | Units explicit; distribution table or figure; distance-resolved leakage; abstract and conclusion state the compensation consequence | Small |
| E10 | R1C-07, R2c-9 | Presentation: create a supplement (full wire and loop tables, 100 nm sensitivity diagnostics, procedures, repeated bootstrap settings). Fix the minor items: open-IVU half-gap 8 mm from source or justified; population wording in the abstract; comparison table (feasible aperture, robust capture next to nominal); number formatting; "first failed grid point" defined once. | Main text and supplement cross-references resolve; the design-beam and sensitivity cases are unmistakable | No |
| E11 | R1C-08 | Final reconciliation: round-3 manifest for campaign 04 (with campaign-03 artifacts still referenced where used); claim table; cover letter; new frozen bundle with verification; a **new** round-3 author response; full test suite; gated PRAB build (one- and two-column); protected-file check. | Bundle rebuild reproduces the macros; tests pass; earlier responses unchanged | No |

## Order and dependencies

```text
B1–B5 requested from author (defaults allow E4–E6 to proceed)
E1, E2, E3 ─ now, independent (existing data; E2 also informs the E8 framing)
E4 ─┐
E5 ─┴→ E6 → E7 (overnight) → E8        model fixes first, one rerun, then synthesis
E9 ─ in parallel with E5–E7 (cheap; uses the E4 chamber for the eddy/coating estimate)
E10 → E11                              after E8 and E9
```

Rationale:
- **E4 and E5 precede E6.** The operating point must be selected on the chamber and ring population it will be
  evaluated on; otherwise the round-2 mismatch repeats.
- **E7 runs once,** after the three model defects are fixed. This satisfies Reviewer 2's request without Reviewer 1's
  objection to arbitrary enlargement.
- **E8 depends on E7.** The synthesis that Reviewer 1 requests would otherwise explain artefacts that Reviewer 2 has
  identified.
- **E1–E3 and E9 fill the compute wait.**

## Not undertaken

Neither reviewer requires these items for the declared simulation scope:
- hardware measurements;
- a time-dependent pulsed-magnet model;
- a global optimiser;
- additional facilities;
- increased particle or seed counts;
- a compensation-magnet design.

If E7 still yields low robust capture, the paper reports that and its cause; it does not tune the model toward a
target.

Protected inputs remain read-only. Nothing is pushed, submitted or published.


## Round-4 follow-up to the round-3 manuscript

Consolidated 2026-10-16 from [Reviewer 1 round 4](reviewer1_round4_20261016_report.md),
[R1D-01–08](reviewer1_round4_20261016_revision_tasks.md), and
[Reviewer 2 round 4](reviewer2_report_round4.md), R2d-1–7.
This is the current execution queue. **All F tasks are pending; do not execute yet.**
The historical E1–E11 specification above and its response remain the completed round-3 record.
No fifth review round or completed revision response is implied.

### Shared decisions and limits

Both reviewers credit the modelling core and require evidence-based attribution of the NKM–dipole deficit,
a tested operating-point comparison and a current-point pulse calculation. Reviewer 1 additionally requires
clear diagnostic/production-launch scope and physical/numerical loss classification. Correlations do not establish
causation; no arbitrary new ring count, commissioning experiment or universal efficiency target is imposed.
Local access has been checked for all 235 artifact keys; no new access simulation is needed.

| ID | State | Work package and mapped requests | Dependencies | Required output / completion gate |
| :--- | :--- | :--- | :--- | :--- |
| F1 | Pending | Freeze adopted model, point candidates, physical error-class grouping, seeds/particles/ring identities and paired estimands. Supports R1D-01/02/03/05/08 and R2d-1/2/3/4. | Authorization | New protocol/source identity; current point retained until an explicit decision. All-off includes corrected rings and declared nominal model; disabled errors do not alter latent random draws. |
| F2 | Pending | Paired causal ablation at zero booster jitter: all-off, full zero-jitter budget, each class alone, each class omitted. R1D-01; R2d-1. | F1 | Per-model capture, paired NKM-minus-dipole effects and uncertainty; interactions acknowledged, no forced additive decomposition. Same 50 seed-42 draws, particles and rings; no inference from unpaired hierarchy-row subtraction. |
| F3 | Pending | Paired current/earlier/extremum-centred point test at zero/full budget, feasible septum/root checks and recalibrated controls. R1D-02; R2d-2. | F1; F2 informs interpretation | Held-out comparisons and explicit adopted-point decision. If reselecting: declare error-inclusive objective, extend feasible binding bounds, separate training/validation and retain boundary fractions. Honest limited-scope retention is permitted. |
| F4 | Pending | Signed/physical associations for both models and their paired difference; zero-capture/conditional summaries, jitter rows and interval definitions. R1D-05/07; R2d-4/7. | F1; F2/F3 for final narrative | Predictors/signs, multiplicity scope, denominators and bootstrap units recorded. Correlation cannot substitute for F2. A central 95% lower endpoint is labelled conservative if used for a one-sided test. |
| F5 | Pending | Locate losses in selected zero-capture cases/ring 5501, report coupling scope, define numerical-domain/conductor guard and qualify chromaticity inference. R1D-04; R2d-5. | F1; final interpretation after F3 | Plane/location/turn and counts reconcile with existing categories; physical boundary distinguished from numerical rejection. Reuse raw diagnostics; rerun only insufficiently resolved representative cases. Controlled chromaticity check or reduced claim, not mandatory global retuning. |
| F6 | Pending | Septum dispersion and fit/launch scope: D/D', within-bunch/shot angular contributions, empirical eta fit and synthetic-versus-production accuracy wording. R1D-06; R2d-6/7. | F1; adopted-point decision F3 for dependent numbers | Explicit units, assumptions and launch identities. Discuss companion dispersion-free transport as an alternative, without equating it to validated ring capture. Scope wording can avoid an unnecessary new scaling campaign. |
| F7 | Pending | Pulse and transparency consistency at the adopted point/strength; native return positions/kicks, allowance, finite-support timing bounds, correct rescaling laws. R1D-03/07; R2d-3/7. | **F3 point decision**; F6 allowance definition | Current-point source artifacts/macros/manifest checks; common angular allowance; quantities with nonlinear strength dependence re-evaluated appropriately. Historical S=0.85 diagnostics remain labelled. |
| F8 | Pending | Rewrite abstract/synthesis/discussion/conclusions and editorial corrections from F2–F7; restrict novelty, label historical figures, margin-fit degeneracy and dates. R1D-01/06/07; R2d-1/2/5/6/7. | F2–F7 | Every principal claim has the correct paired evidence and point identity. Poor capture may remain; no requirement to improve the result. Tuning gains keep boundary limitation unless resolved. |
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
