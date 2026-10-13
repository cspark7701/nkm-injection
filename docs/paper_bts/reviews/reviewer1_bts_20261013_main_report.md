# Reviewer 1 — BTS manuscript assessment (main-branch version)

Date: 2026-10-13. Proposed journal: **Journal of the Korean Physical Society (JKPS), Research Article**.

**Recommendation: major revision; do not accept the manuscript in its present form.** This is an internal pre-submission referee assessment, not a journal editorial decision. The subject is potentially suitable for JKPS, but the reviewed version remains an incomplete design-study draft.

Revision register: [ten ordered tasks, R1-BTS-01–10](reviewer1_bts_20261013_main_revision_tasks.md).

## 1. Exact manuscript and review scope

The workspace was on `main` at commit `bee78914caa16945ef63dba8bf5205c434d0415c`. I reviewed `docs/paper_bts/paper.tex`, its eight-page `paper.pdf`, installed result tables, bibliography, draft provenance, B01 scope/literature/inventory/claim documents, and the existing B01–B12 plan. B01 is marked completed in that plan; B02–B12 have no completed results in this reviewed version.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `d19f7e41a72f94a23065ed271a82d4d050477d0cfcdff4d46e743a66d5783a2b` |
| `paper.pdf` | `039dab2d02ddba41f15481be3115afe2ebf625338ab15655555fe9fc30c3ab7b` |
| `paper.bib` | `60905279d299cb5f2e793af1bf82641763e57da033d91122e05354bcbe2573f2` |

**Version qualification:** the local `bts` branch at `466fca5` contains a substantially revised manuscript and later review records. Its abstract differs from this draft. Those later results and assessments are not evaluated here, and this report must not be represented as a rejection of that later manuscript. No branches were switched or merged for this review. A review of the latest BTS article must identify and inspect that separate version and its evidence.

I checked all nine scientific source-file hashes listed in the main draft's provenance; all matched. I inspected all three optimization candidates, the pooled and per-run summary statistics, OAT values, and the five actual infeasible records in the two runs containing failures. I inspected current optimizer, sensitivity and error-evaluation code to interpret the evidence. I did not rerun optimization or tracking, independently reproduce every sample, or establish equivalence between current code and every generating historical commit. Hash consistency establishes file identity, not physical validity.

## 2. Overall assessment

The manuscript clearly separates optical mismatch, BTS transmission and ring capture. It reports floating-point matching as numerical precision, retains the failed 50k prefix checks, qualifies the five rare failures, and openly states that several error mechanisms are inactive. These are good scientific practices. The selected nominal peak beta values and the pooled mismatch/failure statistics are traceable.

However, the paper currently delivers a matched linear model and a conditional error summary, while the planned independent transport validation, physical margin comparison and correction-knob demonstration remain prospective. Standard matching and a large Monte Carlo sample alone do not demonstrate a new accelerator-physics contribution. The physical target boundary, hardware assumptions and design-beam relevance are still unresolved. The supporting B01 documents also contain incorrect or unsupported claims despite their verification labels. These are scientific and provenance revisions, not merely editorial polishing.

A focused JKPS design paper could be publishable if it explains and validates a useful physical result: for example, a reproducible correction range or an envelope-margin improvement under realistic constraints. A negative comparison can also be useful if supported and interpreted. Measurements are not an absolute prerequisite for a simulation paper, and a new optimizer or MOGA campaign is not mandatory.

## 3. Major comments

### M1 — Complete and establish the physical contribution

**Locations:** Introduction; Sections 4–6; `article_scope.md` §1/§3; `literature_comparison.md` §3.

The text proposes correction and design comparisons without reporting them. The scope documents sometimes describe these proposed results as already established. Reframe the article around a completed physical question and one adequately validated comparison. Explain how the result changes an actual BTS design or operating choice. Do not treat nine variables for six residuals, the use of SLSQP, or sample count as novelty by themselves. Integrate the closest literature and disclose overlap with the NKM study without reproducing its principal results.

### M2 — Establish the boundary model and hardware relevance

**Locations:** Section 2; Table 1; scope document boundary declarations; claim ledger BC09/BC11.

The declared exit beta values 2.336495/4.256241 m are not the NKM-centre ring Twiss. A configuration value is not proof that these are the physical storage-ring injection boundary optics. Show the source/reference point, coordinate convention and intervening transport. Supply a dated, source-confirmed layout and reconcile the nine-quadrupole AT sequence with the preliminary ten-quadrupole MAD-X sequence before using the latter for validation.

The 60 m beta ceiling, square aperture elements, family bounds and pole-tip limit need source/assumption labels. Beta margin in metres is not vacuum stay-clear in metres. Convert strength to gradient and pole-tip field consistently, and compute beam clearance with centroid, dispersion, coupling and declared coverage. Keep the historical 100/10 nm rad case distinct from the later 7.67 nm rad horizontal design specification.

### M3 — Validate active errors, coupling and physical transport

**Locations:** Sections 3.3, 4.1 and Discussion.

The manuscript correctly acknowledges missing optical response to several sampled errors. It still needs an error-to-observable coverage table and independent checks of the effects that do act. In a linear quadrupole model, translations principally affect orbit; negligible Twiss mismatch under offsets does not establish alignment tolerance. Rolls require coupled covariance/transport checks; energy perturbations must treat rigidity and bending consistently. The historical OAT offset response is about 4e-17 in its mismatch estimator, so any asserted peak-beta effect needs its own quantitative demonstration.

Use zero-error, single-error and combined-error tests against an equivalent independent matrix model or reconciled second code. If transmission or engineering tolerances are claimed, evaluate particles through declared aperture locations and report beam generation, loss positions, seeds and uncertainty. Keep absent chamber information parametric. No ring capture study is required for a paper whose claims stop at the BTS exit.

### M4 — Reconcile the B01 claim ledger and inventory with actual evidence

**Locations:** `claim_evidence.csv`, `article_scope.md`, `literature_comparison.md`, `evidence_inventory.md`; corresponding manuscript sections.

The following discrepancies are directly verifiable and should be corrected before these documents are used as publication evidence:

| Supporting claim | Checked evidence | Required correction |
| :--- | :--- | :--- |
| Three independent random restarts; feasible search-space fraction 33% | Start 0 is nominal, followed by two random starts. One successful feasible result, one successful infeasible result, and one evaluation-budget failure | Describe exactly these outcomes. Three starts, including a deterministic start, do not estimate feasible volume or prove topology. |
| Two infeasible starts both converge to small residual merit | Candidate 1 has merit 1.2146e-12 and optimizer success; candidate 2 has merit 1284.86 and optimizer failure | Separate termination, matching and feasibility. Preserve the successful-but-infeasible counterexample without extending it to the failed start. |
| BC05: condition number 1421.636 is from a normalized residual Jacobian and supports decoupled knobs | `compute_sensitivity_matrix` differentiates raw beta/alpha/dispersion observables and performs SVD directly; the archived matrix matches that mixed-unit definition | Reclassify it as a raw sensitivity diagnostic. Produce an explicitly normalized matrix and finite-correction validation before a physical knob claim. The manuscript's proposed Eq. (5) does not retrospectively normalize this archive. |
| BC06: energy is ahead of gradient; beta/alpha jitter; stated OAT values | Seed 42 ranks beta mismatch 0.00890374, gradient 0.000861122, energy 0.000106336. The sampled entrance alpha is held fixed | Correct labels/order and estimator. OAT is mean absolute change of Mx+My, not the six-residual least-squares J. Specify which beta planes are varied. |
| BC07: two dipoles; evidence examples for target provenance | The line has three main bends b1–b3, in addition to kicker/septa; the target exists in config but its physical source is unresolved | Correct the element count and distinguish a configured target from a source-validated target. |
| BC03: pooled median interval under `pooled.median_mx_bootstrap` | The reported interval is under `pooled.quantiles.mismatch_x.p50_ci` and is the order-statistic interval | Use actual JSON paths and the correct interval method. |
| Inventory assigns one generating commit and inaccurate artifact byte sizes | Optimization config records `f2ac6e27f60dd19d0dfbc74419df585b6f0a8748`; `environment.txt` records another checkpoint, `8b62bcd4037031551a1787aabae0bd5dae708046`. Summary/config/candidate sizes are 3200/4286/4330 bytes | Give artifact-specific generation/checkpoint provenance and regenerate file metadata; do not assert one generating commit for everything. |

The archived numerical matching and pooled statistics need not be discarded because of these documentation errors. They must be linked to correct definitions and claims. Reopen the completed B01 audit where necessary.

### M5 — Repair and verify the closest-literature comparison

**Locations:** Introduction; six-entry bibliography; `literature_comparison.md` §2.

The main text still has a literature TODO. The supporting survey asserts comparative beta limits, sample budgets and target provenance without source passages. Its MAX IV entry gives an incorrect title for Phys. Rev. ST Accel. Beams 15, 050705 (2012): the publisher identifies it as S. C. Leemann's *Pulsed sextupole injection for Sweden's new light source MAX IV*. See the [APS article record](https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.15.050705). This is a verified mismatch in the supporting survey, not a claim that the present six-entry manuscript bibliography contains that entry.

Verify the PLS-II, RAON, Sirius and ESRF references individually against primary records and full relevant passages. Papers not verified in this review are unresolved, not proven nonexistent. Remove unsupported comparisons such as a universal 100–1000-sample norm, a 33% feasible search-space proof, or a statement that the cited KLS papers establish these particular BTS boundary values unless their text does so. The analysis uses two transverse mismatch quantities and dispersion; calling it a demonstrated full six-dimensional phase-space mismatch also requires correction.

### M6 — Demonstrate usable correction or margin benefit

**Locations:** Section 5.2; Discussion; outline Figures 3–4.

Normalize both observable rows and strength columns before interpreting SVD, specify finite-difference convergence and rank, and test finite corrections within bounds. A local singular vector is not automatically a practical actuator combination or an independently decoupled dispersion knob. Compare nominal and alternative designs with identical beam and boundary definitions. Evaluate static-error corrections on held-out machines, then add independent shot jitter; do not assume every shot's error is known and retunable.

Use uncertainty to qualify any claimed improvement in mismatch, clearance or transmission. A scalar beta reduction alone is not a measured stay-clear benefit. MOGA is optional; if used, normalize its mixed-unit dispersion objective and validate its finalists with the same BTS physics.

### M7 — Interpret statistics using the actual failure rule

**Locations:** Abstract; Eq. (3); Tables 3–4; B01 failure narrative.

The manuscript's exact interval and Eq. (3) are appropriate. The raw runs confirm the operative beta threshold is 60.01 m and the sum-mismatch threshold is 2.05. All five infeasible records have only `beta_exceeded`, with vertical peaks approximately 60.230, 61.639, 61.609, 60.604 and 60.260 m. This is a threshold-exceedance mechanism under the implemented model, not evidence of physical loss. Keep the correct Eq. (3) definition consistently in the supporting inventory: a horizontal-only Mx<0.05 criterion is not the failure rule.

Replace the survey/scope's symmetric `(9.09 ± 9.1)e-6` shorthand with the asymmetric exact interval `[2.95e-6, 2.12e-5]`. Correct the inventory's Wilson interval to the selected analysis values `[3.8831e-6, 2.1283e-5]` if reporting it. State distributions, correlations and whether any follow-up stopping decision was adaptive. One passing median prefix is not tail convergence. More samples should be motivated by the precision of a physical claim, not by an arbitrary requirement to exceed 550,000.

### M8 — Supply reproducible evidence and a finished article

**Locations:** Declarations; data availability; appendix; all draft revision notes.

The local hashes are useful, but paths in ignored results directories do not supply a referee with the raw evidence. Prepare a separate selected-output attachment, artifact-specific configurations/code versions, environment and a numerical rebuild procedure. Include an isolated publication build. A DOI is not demanded by this review; accessible, versioned evidence sufficient for the claims is.

Complete the scientific content before removing the revision notes. Add a layout figure, optics/dispersion and physical-envelope profiles, sensitivity/correction evidence and distributions where needed to explain the argument. Not every one of the six planned figures is mandatory, and cosmetic figure additions cannot remedy missing physics. Confirm authorship, funding, conflicts and assistance disclosures. Align the title, abstract, scope, ledger and conclusions with the results actually completed.

## 4. Presentation and journal requirements

The eight-page one-column layout is readable. Tables use appropriate units and the abstract is within the 150–250-word range. The current generic article class is not itself a scientific objection, and JKPS accepts LaTeX for mathematical manuscripts. Final source formatting must follow its current guidance.

The [official JKPS guidance](https://link.springer.com/journal/40042/submission-guidelines), checked 2026-10-13, recommends a concise Research Article of approximately no more than 4,000 main-text words including abstract/captions, up to six figures with captions at most 200 words, and a title at most 20 words. It states that word/page limits are not strict. It requests relevant declarations and no PACS codes. The [journal scope](https://link.springer.com/journal/40042/aims-and-scope) supports considering a well-founded applied-physics article; it does not lower the evidence standard for this paper.

## 5. Required outcome before reconsideration

Address the ten tasks in the linked register with a point-by-point response and a frozen revised manuscript/evidence selection. The decisive requirements are a physically established boundary model, trustworthy claim/provenance documents, independent validation and at least one completed useful design/correction comparison. A larger Monte Carlo campaign, adding MOGA, or journal-template conversion alone would not change this recommendation.

**Acceptance answer:** no for the exact main-branch draft reviewed here. A substantially revised, validated BTS paper may be a credible JKPS candidate, but acceptance cannot be inferred from a completed task list or transferred from a review of another branch/version.
