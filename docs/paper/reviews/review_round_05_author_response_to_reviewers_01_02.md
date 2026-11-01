# Author response — NKM round 5, Reviewers 1 and 2

Date: 2026-11-01. Target: Physical Review Accelerators and Beams.

This response follows the [consolidated G1–G7 register](revision_round_05_plan_for_review_round_05.md). Original reports and earlier responses are preserved. G1–G5 are complete. All 150 new tracking realizations finished, and the installed article layouts and supplement pass clean-log checks. G6 is complete, including the frozen-source attachment verification below. G7 remains a submission-stage author gate.

## Reviewer 1

### R1E-01 — Recovery budget

The abstract and conclusions now name horizontal-only steering beside the 150-realization 16.1/44.1% NKM/uniform-kick headline. The separate 50-realization ideal two-plane sensitivity gives 33.9/57.2% under the full assumed budget. The 76.6% NKM recovery is explicitly without booster jitter; its paired horizontal-only baseline is 40.13%, not the pooled 16.1%. No paired gain is calculated across those populations. The new scan uses the same two-plane steering and paired population throughout.

### R1E-02 — Chamber interception

The physical chamber statement has been corrected. For ring 5501 the records contain 133 NKM and 154 uniform-kick interceptions at `NKM_H1/H2`. Widening the half-height from 3.8 to an infeasible 15 mm raises capture from 29.8 to 33.2% for the NKM and from 33.2 to 37.6% for the uniform kick. Interceptions occur at the chamber, although widening alone does not remove the slow-loss limitation. Later physical aperture losses are distinguished from numerical injection-pass domain/conductor rejection. “None inside the magnet” is restricted to the selected first-zero-capture cases supporting it.

### R1E-03 — Reconciliation and response

The shared-source one-column article, two-column preview and supplement rebuild to 36/18/7 pages with no unresolved references, citations, overfull boxes or float failures. The 250-word abstract and changed table/figure pages were inspected. The claim ledger and 272-key round-5 manifest include the audited corrections and scan. Final source/PDF identities are recorded in `round5_final_identity.json`; frozen-attachment verification is recorded below. Local execution does not constitute scientific approval, external evidence delivery or journal acceptance.

## Reviewer 2

### R2e-1 — Headlines under both steering assumptions

The population and budget qualifications described under R1E-01 are applied in both the abstract and conclusions. The horizontal-only deficit is associated with the uncorrected vertical injection error in the modelled transfer line. Ideal static removal in both planes is a separate sensitivity, without a fitted BPM/corrector system.

### R2e-2 — Jitter regime and targeted scan

The 0.5 mm / 0.2 mrad extraction jitter is labelled an assumed stress level. Including dispersion and energy spread, it is 1.3 / 2.2 nominal extraction rms beam sizes. The protocol was recorded before new tracking. It specifies scales 0, 0.1, 0.25, 0.5 and 1, 50 paired seed-42 realizations, 200 Gaussian particles per realization, 500 native turns, the selected operating point and the existing corrected-ring population. The zero/full endpoints are reused after explicit configuration, source and pairing checks; the three missing scales use new result directories.

The declared one-point test compares NKM(scale) with NKM(zero) under the same two-plane steering. The lower central-95% paired bootstrap endpoint must exceed −1 percentage point. This is a conservative 97.5% one-sided interpretation, with 10,000 resamples and seed 1729. The NKM-minus-uniform-kick gap, each model's jitter cost and the change of the gap are separate estimands. Intervals are pointwise, and a largest passing sampled scale would not establish a continuous threshold or hardware tolerance. No nonzero tested scale passes. At 0.1 the paired NKM change is −2.35 points (95% CI −4.32 to −0.66); at 0.25 it is −11.32 (−16.55 to −6.58). Thus the scan demonstrates no nonzero acceptable-loss regime among the tested levels. Levels below 0.1 remain untested. See [the complete results](../round5_jitter.md), main Table VII/Figure 10 and supplemental Table S4.

### R2e-3 — Companion consistency

The [model audit](../round5_companion_comparison.md) verifies identical nominal nine-quadrupole strengths, geometry and bend strengths. The studies differ in error correlations: the NKM campaign uses one common relative dipole-field error across all bends, while the companion BTS campaign draws independent errors per bend. Integration steps, steering and population summaries also differ. Neither lattice was changed to force agreement.

The NKM's quoted 0.90 mm / 77 microradian values are population standard deviations across 50 finite-bunch BTS-magnet-error realizations. Their exact rms values are 0.903 mm / 77.72 microradians. The companion's 1.07 mm / 0.096 mrad values are rms analytic centroids over 200 machines with three shots each at zero jitter. The manuscript identifies these definitions and cross-references the companion. A sampling-only explanation is unsupported by this comparison and has been removed.

### R2e-4 — Abstract

The allowance is written explicitly as 0.044 mrad, with the 161 microradian thin-map error equal to 3.7 times that allowance. The abstract is shortened while retaining population, steering and stress-level qualifications. The final extracted abstract contains 250 whitespace-delimited words; approximately 250 words is an editorial target here.

### R2e-5 — Point labels and date

Tables I–II label historical peak-kick values as S = 0.85 and distinguish the adopted S = 0.95 quantities. The article and supplement carry the same November 1, 2026 date. Historical review dates remain unchanged.

### R2e-6 — Recovery and tuning scope

The two-plane translation is described as an optimistic benchmark for ideal static centroid removal without BPM or actuator errors. It does not prove that every practical or optimized correction must capture less, so we have not adopted a universal capture-upper-bound claim. The companion's horizontal residual alone does not quantify a vertical hardware penalty. The approximately +11.9-point tuning gain is explicitly under horizontal-only steering and without booster jitter. The 28% outer-bound fraction, held-out particles and ideal observable remain stated; the author-selected tuning range is unchanged.

### R2e-7 — Current status documents

Current indexes and the submission checklist record G1–G6 complete and installed 36/18/7 page counts. Dated reports, original reviewer checklists and earlier responses retain their historical contents.

### R2e-8 — Evidence and rebuild

The new 272-key manifest retains all 250 inherited round-4 artifact identities and adds the scan, pairing analysis, protocol, precise and declaration-time companion audits, identified BTS references and input spreadsheets. Figure provenance and generated macros are regenerated by the full builder. Thirty relevant pairing, inference, protocol, figure and packaging tests pass; the final full suite passed 775 tests. Both source layouts and the supplement pass the clean-log gate. The frozen archive from clean source `3c981c2` passes all 280 inventory entries and the archived full figure/macro rebuild. Macros and portable saved-output analysis are byte-identical to the selected records. The exact archive digest and scientific source/PDF hashes are in [the identity and verification receipt](../round5_final_identity.json) and [reproduction guide](../round5_reproduction.md). The frozen checkpoint precedes these verification results; current completion receipts follow it without changing its scientific assets. Earlier frozen attachments remain identifiable historical versions.

### R2e-9 — Submission access and approval

Deferred as G7. Public repository access, actual delivery of ignored evidence, final scientific interpretation and declarations require the author's submission-stage confirmation. No remote API checks, uploads, pushes or journal submission are performed by these revisions.

## Reviewer 2's questions

1. **Quarter-jitter gap under two-plane steering:** −15.74 percentage points, with paired 95% interval −21.25 to −10.59, at quarter jitter. This gap is distinct from the NKM self-baseline jitter-cost test.
2. **Identical BTS settings?** Nominal strengths and geometry agree; error-draw definitions are not identical. In particular, the dipole-field error is common across bends here and independent per bend in the companion. The audit records the remaining numerical/population differences.
3. **Vertical correction foreseen?** No supplied author input specifies planned vertical correction hardware for this modelled BTS version. The manuscript therefore retains an ideal sensitivity interpretation and does not describe it as an implemented or representative hardware correction.
