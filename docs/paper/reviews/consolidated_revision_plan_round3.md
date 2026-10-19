# Consolidated revision plan — round 3 (Reviewers 1 and 2)

**Status updated 2026-10-16:** E1–E11 below were executed in milestones 211–222;
see [the round-3 response](author_response_round3.md). The round-4 assessments of
that revised manuscript identify new work. Their consolidated **F1–F9 follow-up**,
all pending, is in [consolidated_revision_plan_round4.md](consolidated_revision_plan_round4.md).
This does not relabel completed E tasks or imply execution of F tasks.

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

Moved on 2026-10-19 to its own file:
[consolidated_revision_plan_round4.md](consolidated_revision_plan_round4.md) (F1–F9, all pending).
