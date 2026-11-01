# Reviewer 1 — NKM round 5, evidence-checked assessment

Date: 2026-11-01. Target: Physical Review Accelerators and Beams (PRAB).
Manuscript: *Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design lattice*.
Reviewed checkpoint: `ccc5c867bbf7c0b1210fc7104018489dffd04244`.
This is an internal pre-submission referee assessment, not a journal decision.

**Recommendation: minor revision. The scientific content is acceptable within its stated scope after two bounded reporting corrections and final reconciliation. I would recommend acceptance after those changes, without another full scientific review round.**

A [separate round-5 report with its nine-item checklist](review_round_05_reviewer_02_report_and_tasks.md) was written concurrently by another session; it is Reviewer 2's assessment. It is preserved unchanged. This assessment records the fresh evidence checks performed here and its own [three-item checklist](review_round_05_reviewer_01_evidence_tasks.md). The two assessments are distinct; this document neither merges their queues nor claims the separate report has been withdrawn.

## Materials and identity

I read the current 34-page article, 17-page two-column preview and seven-page supplement, the fourth-round requests and protocol, and all four joint author responses:

- [Round 1](review_round_01_author_response_to_reviewers_01_02.md): field/sign correction, mechanism, paired controls and initial conditional tolerances.
- [Round 2](review_round_02_author_response_to_reviewers_01_02.md): design booster beam, chamber, corrected rings, independent integration, inference and evidence access.
- [Round 3](review_round_03_author_response_to_reviewers_01_02.md): literature positioning, normalized diagnostic scaling, corrected optics and operating-point selection. Its booster-angle attribution is superseded by round 4.
- [Round 4](review_round_04_author_response_to_reviewers_01_02.md): paired ablation, two-plane steering sensitivity, point comparisons, loss diagnostics and current-point pulse/transparency recomputation.

The supporting round-4 notes and selected raw records were checked against the claims. The abstract and the two-column page containing Tables VI–VII and Fig. 10 were inspected visually. Older responses describe their own manuscript versions; they are not independent validation of every later interpretation.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `62d03c80d7a404efd64e956c86c54a3ad1b5c606c81707ad797640ea5f96440c` |
| `paper.pdf` | `11786804edf067f3a5e528230b0208c7786ce2682f40a8148c19c78628cb875b` |
| `paper_twocolumn.pdf` | `24ba0a61f99b12ba617b46c95030b936f947c66251d575cbc903530e9ffe3d3c` |
| `supplement.tex` | `35f689b7b4188a746c0ada7de0209e76443c8bfa74af6109df07aa7bb161490c` |
| `supplement.pdf` | `48a9409d4093d8eb33d9bb2ab349c35fe4026d70f1200670eff0859f8e96ceb2` |
| `revision_manifest_round4.json` | `6580a19cc36b89e7fc0738f96c0f461722c204990c54bbbfa6e186ca63521b77` |

## Scientific judgement and disposition of round 4

The paper now distinguishes established tools from its contribution. Segmented field tracking and finite-conductor modeling are credited to earlier work, including [Sun et al., PRAB 23, 010702 (2020)](https://journals.aps.org/prab/abstract/10.1103/PhysRevAccelBeams.23.010702). I checked that official record, without conducting a new exhaustive literature audit. The contribution is a quantified single-thin-map error in this angle-cancelling geometry, and a paired investigation of vertical injection errors and point-dependent capture.

The production-trajectory error is 161 microradians, about 3.7 times the declared 0.044 mrad allowance. A sliced vector map agrees with the filament reference below 1e-7 rad on the tested production trajectories. The empirical eta exponent is restricted to the diagnostic recipe and two related wire families. Independent integration validates the stated paraxial equations rather than proving the model exact for a real magnet. This is a credible specialist contribution within [PRAB's accelerator-science scope and significance criteria](https://journals.aps.org/prab/about).

| Previous request | Assessment |
| :--- | :--- |
| R1D-01: paired attribution | Substantively resolved by alone/omitted error-class interventions and the vertical steering sensitivity. |
| R1D-02: operating point | Resolved within the agreed scope: paired alternatives, recalibrated controls, declared retention rule and no robust-optimum claim. |
| R1D-03: pulse | Resolved: adopted point, S = 0.95, consistent tenth-window allowance and explicit analytic/time-dependent distinction. |
| R1D-04: loss/domain diagnostics | Substantively resolved; one chamber-location statement remains incorrect, as detailed below. |
| R1D-05: signed predictors | Resolved: exploratory signed associations are separated from intervention-based attribution. |
| R1D-06: scope/inference | Resolved: production versus diagnostic launches, dispersion and the interval convention are explicit. |
| R1D-07: quantities/presentation | Substantively resolved: recomputed transparency, historical labels and conditional capture summaries. The recovery budget still needs a local qualifier. |
| R1D-08: reconciliation | Numerical reconciliation is demonstrated. Current status documents lagged behind completed F work; final reporting edits still need their own rebuild and identities. |

F1–F9 are completed execution records. Low robustness is a supported negative result, not a reason to demand better efficiency or to repeat the resolved major work.

## What the paired evidence establishes

The central steering comparison uses the same 50 seed-42 realizations, 200 particles per realization and corrected-ring identities:

| Budget and steering | NKM [%] | Dipole [%] | NKM minus dipole [points] |
| :--- | ---: | ---: | ---: |
| Zero booster jitter, horizontal-only | 40.13 | 68.46 | −28.33 |
| Zero booster jitter, ideal two-plane | 76.57 | 82.64 | −6.07 |
| Full booster jitter, horizontal-only | 19.46 | 48.25 | −28.79 |
| Full booster jitter, ideal two-plane | 33.91 | 57.22 | −23.31 |

The ablation identifies the BTS magnet group, and removing its static vertical centroid restores most of that group's capture loss. The full-minus-zero jitter effect on the gap after two-plane correction is −17.2 [−25.4, −9.2] points; position-only and angle-only sensitivities both produce an NKM-specific cost. This supports an interacting mechanism conditional on the steering model, replacing the old universal booster-angle attribution.

The alternative-point NKM gains, +2.9 [−4.7, +10.4] and +2.1 [−5.7, +9.7] points, do not resolve an improvement. The uniform control loses roughly 17–23 points there. The gap is therefore point-dependent; the intervals do not establish equivalence or a unique optimum. Retaining the adopted point is defensible under the stated rule. The disclosed 28% tuning-bound fraction remains a limitation.

A two-plane reduced-jitter scan could inform a future design study. I do not require it to accept the present conditional mechanism article: the production steering and its limitations are explicit, zero/full and component interventions already support the attribution, and the paper does not claim a deployable correction system. Likewise, numerical agreement between different BTS ensembles need not be forced if their settings or populations differ. Any practical stabilization specification would require further evidence; the present sensitivity should not be promoted to such a specification.

## Required reporting corrections

### R1E-01: qualify the recovery by error budget

The abstract's “raises the NKM to 76.6%” follows the 16.1% joint-error headline without explicitly repeating that 76.6% excludes booster jitter. State the budget beside that number and check abbreviated conclusion wording. The paired recovery is 40.13 → 76.57% without booster jitter; with full jitter it is 19.46 → 33.91%. The headline 16.1% is a separate 150-draw mean. No sentence should suggest recovery from 16.1 to 76.6% under an unchanged full budget. This needs a qualifier, not necessarily four extra abstract numbers. Retain the ideal-sensitivity qualification.

### R1E-02: correct the physical interception statement

Section V, `paper.tex` line 225, says corrected-ring losses occur “but not at this chamber.” The F5 ring-5501 record contradicts this: NKM losses at `NKM_H1/H2` total 100 + 33 = 133; the dipole has 107 + 47 = 154. These are later physical ring-aperture interceptions, distinct from numerical `outside_field_map` rejection during the injection pass.

Opening the chamber to an infeasible 15 mm half-height gives only 29.8 → 33.2% NKM and 33.2 → 37.6% dipole capture. That supports the narrower conclusion that widening alone does not remove the slow-loss limitation, not a claim of no chamber interception. Distinguish interception location from the dynamics that created the motion. Restrict no-in-magnet-loss observations to their actual ideal-ring or selected zero-capture NKM cases. Existing records suffice.

### R1E-03: reconcile the corrected presentation

Use the Humanizer skill for manuscript prose edits. Rebuild both PRAB layouts and the supplement, update current source/PDF identities and affected claim locations, and write a short response. Preserve old reports, responses and frozen packages. Final submission sources must identify the final wording; the round-4 raw-evidence attachment can remain a labeled scientific snapshot with an explicit relationship to the final manuscript. No new scientific campaign or public deposit is required solely for these corrections.

## Fresh verification and limits

- All **250 artifact keys** in the round-4 manifest resolve and match their SHA-256 values. Keys may share files; this is not 250 independent experiments.
- Fresh saved-output analyses reproduce the selected ablation, two-plane steering and point-comparison JSON records exactly. Sample IDs, beam seeds and ring identities match across the 50-draw comparisons.
- A full figure/macro rebuild reproduces the installed macro file byte for byte. New checks are in `results/nkm_reviewer1_round5_20261101/`; no outputs were installed into the manuscript.
- The frozen archive digest is `dbe3a7a82f138c9709a14950ca45cdd678033a71de03e55b1ca3dde02c9dab67`; all **258 inventory entries** verify by reading the archived members. Its archived code was not executed here.
- Installed sources and PDF text match the recorded October-31 humanized builds. Their records include template notices and underfull boxes; they are not described here as entirely warning-free.
- **26 tests pass** across `test_round4_protocol.py`, `test_submission_package.py` and `test_journal_figures.py`, including draw-invariance and point-aware manifest checks.

No new tracking, optimization, TeX compilation, full-suite rerun or exhaustive literature audit was performed. These checks establish evidence consistency, not realism of assumed machine inputs.

## Decision

I would recommend acceptance after the three bounded items in the companion evidence checklist. No new ring population, global optimization, commissioning experiment or higher capture target is required by this assessment. Final author approval, declarations, access and actual journal delivery remain separate. This review executes no manuscript revisions and does not supersede the separate concurrent assessment by silently replacing it.
