# Consolidated NKM revision plan — round 5

Consolidated: 2026-11-01. Target: Physical Review Accelerators and Beams (PRAB).

This is the single execution register answering both fifth-round assessments:

- Reviewer 1: [report](review_round_05_reviewer_01_evidence_report.md) and [three-item checklist](review_round_05_reviewer_01_evidence_tasks.md), R1E-01–03.
- Reviewer 2: [report and nine-item checklist](review_round_05_reviewer_02_report_and_tasks.md), R2e-1–9, including its minor comments and three questions.

Both recommend minor revision. Their original reports/checklists remain unchanged and retain their review-time wording. This register merges overlapping work and states the adopted treatment where they differ. D, E and F work remains completed history; no old scientific task is reopened.

**Status: planning only. All G tasks are pending.** The request to consolidate does not execute manuscript edits or authorize starting the proposed simulations. Final approval and journal submission remain separate author actions. Completing the register does not guarantee acceptance.

## Consolidation decisions

1. **Include the targeted scan.** Reviewer 1 considers the present evidence sufficient without a new scan; Reviewer 2 requires one. Adopt Reviewer 2's paired two-plane scan so the revision can answer both assessments. Do not add a new ring population, global search or hardware correction design.
2. **Preserve Reviewer 1's corrections.** Explicitly qualify the zero-jitter recovery and correct the chamber-interception claim. The second issue is absent from Reviewer 2's list and must not be lost in consolidation.
3. **Keep estimands and populations separate.** The 150-draw horizontal-only headline and the 50-draw steering sensitivity cannot be subtracted as a paired recovery. The declared one-point noninferiority test concerns loss from adding jitter to the same NKM/steering model, not automatically noninferiority of NKM to dipole capture. Report the model gap separately.
4. **Verify companion identity before interpreting discrepancies.** Do not presume that 0.90 versus 1.07 mm is purely sampling until strengths, observation point, error definitions and statistic agree. Document genuine differences rather than modifying either lattice to force agreement.
5. **Qualify ideal-correction language.** Describe the two-plane translation as an optimistic ideal static-removal benchmark. It is not a proved global upper bound on capture: the study does not establish that all possible correction/optimization procedures must capture less. Do not infer a numerical hardware performance penalty from the companion's horizontal residual alone.
6. **Use Humanizer for manuscript prose.** Preserve supported physical claims, population labels, uncertainty, numerical values, citations and notation. This consolidation does not edit manuscript prose.

## Ordered checkbox register

### G1 — Freeze the paired comparison and reconcile the shared BTS model

Maps to R2e-2 (regime), R2e-3, questions 2–3; supports R1E-01 and R2e-1.

- [ ] Record the current manuscript/configuration identity, adopted point, beam distribution, chamber, tracking settings, corrected-ring files, source versions and existing zero/full two-plane artifacts in a **new round-5 protocol** before any new run. Preserve the round-4 protocol.
- [ ] Compare actual NKM/BTS quadrupole strengths, optics/dispersion, coordinate and observation conventions, vertical correction assumptions, and error-draw definitions. Identify whether the companion setting is identical or differs; do not assume equality from the shared line name.
- [ ] Identify the populations/statistics behind NKM's 0.90 mm / 77 microradian vertical centroid (50 seed-42 realizations) and the companion's approximately 1.07 mm / 0.096 mrad (200 realizations). Verify rms versus standard-deviation definitions and avoid claiming a sampling-only explanation without support.
- [ ] Express 0.5 mm / 0.2 mrad booster jitter in the appropriate extraction beam-size units, including the declared dispersion and energy spread. Verify the companion's approximate 1.3 / 2.2 ratios before quoting them; retain the stress/sensitivity label unless an actual specification is supplied.
- [ ] Record whether vertical correction hardware is known to be planned. If no author input establishes it, state that it is unspecified; the sensitivity remains ideal. No hardware answer is required to run the declared sensitivity.
- [ ] Freeze the G2 estimands, seed/sample pairing, resampling and reporting rules below.

Completion: a reproducible protocol and a concise companion-comparison record distinguish shared settings, differences and unknowns. No protected input or lattice is modified.

### G2 — Run the targeted two-plane jitter scan

Maps to R2e-2 and question 1. Depends on G1. Required by the consolidated plan to address Reviewer 2; not a new requirement attributed to Reviewer 1.

- [ ] Evaluate booster position/angle jitter scaled together at **0, 0.1, 0.25, 0.5 and 1**, using the same 50 seed-42 realizations, 200 Gaussian particles per realization, 500 native turns and corrected-ring identities as the existing two-plane sensitivity. Keep all other machine/shot draws fixed, both kicker calibrations consistent, and the adopted point unchanged.
- [ ] Include both the NKM and dipole. Reuse existing zero/full endpoints only after verifying complete source/configuration and pairing identities; generate missing scales in new result directories. Extend the existing driver only as needed; do not present an unimplemented command as available.
- [ ] Verify sample IDs, particle seeds, ring identities and unchanged latent errors across scales. Report configuration, particle distribution, energy spread, Twiss/dispersion, apertures, loss definition, observation points and counting denominators.
- [ ] Report each model's mean, zero-capture fraction and paired NKM-minus-dipole gap, with pointwise paired realization-bootstrap 95% intervals (10,000 resamples, seed 1729, consistent with the existing analysis).
- [ ] For the declared one-point acceptable-loss test, compute **NKM(scale) minus NKM(zero)** under two-plane steering on the same realizations. Passing means that the lower endpoint of the central 95% interval exceeds −1 percentage point; retain its conservative 97.5% one-sided interpretation. Report dipole jitter costs and the paired change of the model gap separately.
- [ ] Do not relabel that test as NKM-versus-dipole noninferiority. Any additional formal model-to-model noninferiority test would need its own explicit estimand and justified margin declared before analysis; it is not required by this consolidated plan.
- [ ] State the outcome at each sampled scale, including no demonstrated nonzero passing scale if applicable. A passing zero-jitter reference is not evidence of a usable nonzero tolerance. Describe a largest passing **tested** scale, not a continuous threshold or hardware specification; disclose pointwise intervals and avoid an unsupported monotonicity claim.

Completion: selected raw records, pairing checks and an analysis table/figure answer the quarter-jitter gap question and quantify the assumed stabilization regime. Unfavorable outcomes are valid; no improved capture is required. An optional 0.2 scale may be declared before running if needed to compare directly with the companion's low-jitter discussion.

### G3 — Reframe the headline and shorten the abstract

Maps to R1E-01, R2e-1 and R2e-4. Depends on G1–G2.

- [ ] Name the horizontal-only production steering and the absent vertical correction beside the joint-error headline. Present the full-budget ideal two-plane result as a sensitivity, with its population stated.
- [ ] Keep the population identities visible: pooled horizontal-only NKM/dipole 16.1/44.1% uses 150 draws; the paired 50-draw full-budget comparison is 19.46/48.25% horizontal-only versus 33.91/57.22% two-plane. Do not calculate a paired gain from 16.1 to 33.9%.
- [ ] Qualify any 76.6% recovery value locally as **without booster jitter**: its paired baseline is 40.13%, not the 16.1% pooled headline. The same distinction must hold in the conclusions.
- [ ] Integrate G2's actual results into the stabilization discussion and retain the stress-level, ideal-steering and conditional-lattice qualifications. Do not equate the companion's low blade loss with ring capture.
- [ ] Replace the awkward “3.7 times a tenth” phrasing with the explicit allowance: 161 microradians, 3.7 times 0.044 mrad, where the allowance is one tenth of the approximately 0.44 mrad window.
- [ ] Aim for an abstract of about 250 words as an editorial target, retaining necessary budget/uncertainty qualifications and moving secondary detail to the Introduction. Do not describe that target as a newly verified hard journal limit.

Completion: abstract and conclusions distinguish production, ideal sensitivity, zero/full jitter and sample populations without implying commissioned performance.

### G4 — Correct physical chamber-interception wording

Maps to R1E-02. Uses existing F5 evidence; may proceed independently of G2 after G1 identifies the unchanged model.

- [ ] Correct Section V's statement that corrected-ring vertical losses do not occur at the NKM chamber.
- [ ] Distinguish later physical ring-aperture interception at `NKM_H1/H2`, numerical injection-pass domain/conductor rejection, and the dynamics that generated the large amplitude.
- [ ] Retain the ring-5501 evidence: 133 NKM and 154 dipole interceptions at the two magnet halves; opening the half-height to an infeasible 15 mm gives 29.8 → 33.2% NKM and 33.2 → 37.6% dipole capture. Widening alone does not remove the slow-loss limitation, although interceptions occur there.
- [ ] Restrict “no loss inside the magnet” to the actual ideal-ring or selected zero-capture NKM cases supporting it.

Completion: text agrees with existing F5 records. No additional tracking, aperture redesign or compensation simulation is required for this correction.

### G5 — Reconcile selected-point labels, recovery conditions and metadata

Maps to R2e-5 and R2e-6; supports R1E-03. Can proceed alongside G2; finalize with G3.

- [ ] In Tables I–II, supply the selected S = 0.95 peak kick from the adopted model or explicitly distinguish historical S = 0.85 quantities from selected-point quantities. Do not mix their disturbance and kick values without labels.
- [ ] Update the manuscript/supplement date consistently with the completed revision, preserving dates in historical reports and responses.
- [ ] Qualify two-plane steering as ideal static centroid removal, not a fitted system with BPM/actuator errors. Address Reviewer 2's optimistic-bound concern using the precise scope above; do not claim an unproved universal capture upper bound or guaranteed reduction from any particular residual.
- [ ] Attach “horizontal-only steering and without booster jitter” to the approximately +11.9-point tuning gain. Preserve the 28% outer-bound fraction, existing author decision not to widen the search, and held-out/ideal-observable limitations.

Completion: every shortened recovery/strength statement retains its point, budget, steering and observable definition.

### G6 — Reconcile evidence, rebuild and respond to both reviewers

Maps to R1E-03, R2e-7 and R2e-8. Depends on G1–G5.

- [ ] Add the new scan/configuration and analysis records to an appropriate new current manifest, preserving older selections and point-aware checks. Update generated macros, figures, claim locations and provenance only where affected.
- [ ] Rebuild the one-column PRAB article, shared-source two-column version and supplement. Check log failures, citations, references, layout and the changed pages; refresh current source/PDF identities and page counts.
- [ ] Run meaningful pairing, error-draw invariance, inference and manifest tests for the new scan/analysis, plus the relevant packaging/figure checks. Broaden testing if changes or failures justify it; no simulation rerun merely to regenerate prose.
- [ ] Prepare a joint point-by-point response using the source reviewer IDs and the crosswalk below, including all three Reviewer 2 questions. Explain adopted qualifications rather than silently rewriting the reviewer requests.
- [ ] Update current indexes, submission checklist and reproduction commands to the completed G status. Archive each executed revision/milestone sequentially and use the established formatted Git commit messages.
- [ ] Prepare source/evidence packaging that contains the new scan and final wording; verify the selected identities and required isolated rebuild steps. An increment over an identified existing attachment is acceptable. Do not represent the old round-4 archive as containing new results.

Completion: final text, macros, figures, manifests, packaging, response and status records agree. Earlier reviews/responses remain unchanged; execution is not journal acceptance or delivery.

### G7 — Submission-stage author gate

Maps to R2e-9 and the author part of R1E-03. Deferred to submission readiness; not a numerical revision prerequisite.

- [ ] Confirm actual access to the repository named in the availability statement and to the ignored evidence attachment, or adjust the wording to the real route.
- [ ] Confirm final scientific interpretation, declarations/AI disclosure, metadata and approval separately from local checks.
- [ ] Record actual external delivery/submission only when performed with the author's instruction. Never push to GitHub or query remote Actions as part of this plan.

Completion: author decisions and actual access/delivery status are accurately recorded. No DOI/public deposit is imposed solely by these reviews.

## Complete reviewer crosswalk

| Source request | Consolidated work |
| :--- | :--- |
| R1E-01 — recovery budget | G1, G3 |
| R1E-02 — chamber interception | G4 |
| R1E-03 — prose/rebuild/response | G3, G5, G6; author gate G7 |
| R2e-1 — both steering headlines | G1, G3 |
| R2e-2 — regime and scan | G1, G2, G3 |
| R2e-3 — companion consistency | G1, G3 |
| R2e-4 — abstract wording/length | G3 |
| R2e-5 — point labels/date | G5 |
| R2e-6 — recovery/tuning scope | G3, G5 |
| R2e-7 — status documents | G6 |
| R2e-8 — evidence/build/response | G6 |
| R2e-9 — access/approval | G7 |
| Reviewer 2 question 1 — quarter-jitter gap | G2, response in G6 |
| Reviewer 2 question 2 — identical BTS settings? | G1, response in G6 |
| Reviewer 2 question 3 — foreseen vertical correction? | G1 (record supplied information or unknown), G5, response in G6 |

Execution order: **G1 → G2 → G3**, with **G4 and G5** able to proceed independently of the scan, then **G6**. **G7** remains a submission-stage gate. Planning and consolidation do not mark any source-review checkbox complete.
