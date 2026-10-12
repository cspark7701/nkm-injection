# Reviewer 1 — third-round manuscript assessment

Date: 2026-10-12  
Manuscript: *Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design lattice*  
Author: Chong Shik Park  
Reviewed commit: `868d14cb600ab79e4b5ec1b42db31950a3887eb7`  
Recommendation: **Focused major revision. I do not recommend acceptance of the present version.**

This is a pre-submission referee-style assessment, not an actual journal editorial decision. It reviews the current 19-page article following D1–D14, together with the [round-two author response](author_response_round2.md). The [second-round report](reviewer1_round2_20261011_report.md) and all earlier reviews and responses remain unchanged. The actionable follow-up is [Third-round revision tasks](reviewer1_round3_20261012_revision_tasks.md).

## 1. Overall judgment

The manuscript has moved substantially beyond a technical report. It now states a physical question, compares approximation levels, validates the stated equations independently, distinguishes design inputs from assumptions, and reports unfavorable robustness results honestly. In particular, it no longer treats a wrong vertical-map sign as an intrinsic defect of vector maps or a tiny sampled centroid as evidence of extraordinary transparency. These improvements deserve recognition rather than another blanket request to redo the campaign.

The current paper is potentially publishable as a conditional accelerator-physics study. My remaining major concerns are concentrated in **scientific positioning, access to the final evidence, and interpretation of the robustness hierarchy**. An omitted directly related paper already uses much of the underlying modelling machinery. The authors must make the distinct new physical result clear. Also, the numerical attachment described by the manuscript is unavailable in this checkout, preventing independent checking of its newest results. The striking difference between nominal and error-ensemble capture needs a clearer physical synthesis, rather than only a sequence of statistics and qualifications.

I therefore recommend focused major revision, not rejection. Most requested work is literature reconciliation, existing-data analysis or presentation. There is no blanket requirement for prototype measurements, a new global optimizer, a larger arbitrary number of ring seeds, or another full production campaign. If the missing attachment verifies and the distinct contribution is demonstrated, the next review should be much narrower. Completion of a software/revision checklist is helpful but is not itself a journal acceptance criterion.

For PRAB, the decisive question is whether the paper adds a substantive result beyond existing nonlinear-kicker modelling and optimization, consistent with its [official contribution criteria](https://journals.aps.org/prab/about). A simulation-only study is within the journal's stated accelerator-physics scope. The absence of hardware measurements should limit operational claims, not automatically disqualify the study.

## 2. Review basis and verification limits

I read the current LaTeX source and PDF text, the round-two response, author-input documentation, and the supporting notes on scaling, corrected rings, robustness, errors, transparency, validation and evidence packaging. I visually inspected the current mechanism/scaling, corrected-ring, chamber and final robustness figures. I also inspected the independent ODE implementation and selected statistical and analysis drivers.

The active manifest contains **205 artifacts**. In this checkout:

- **48 artifacts are present and match their recorded SHA-256 hashes**;
- **157 are absent**, predominantly the campaign-03 results, configurations and corrected lattices;
- **no hash mismatch was found among the present artifacts**.

`results/journal_campaign_03/` and `round2_evidence_bundle.tar.gz` were not found locally, including a search for relocated bundle and key result filenames within the repository. The completed D13/D14 records state that the bundle and 205-artifact verification previously succeeded. I acknowledge those historical records, but cannot repeat their verification here. Missing ignored outputs do not establish corruption, failed simulations or scientific misconduct; they limit the evidence available to this review. Reported campaign-03 numbers below are read from the installed macros/PDF, not independently recomputed raw results.

No tracking campaign, manuscript rebuild or numerical test suite was run during this review. A small analytic check confirmed that the scaling driver's negative-lobe width definition selects a connected lobe for the two default transverse families; it does not validate the entire missing scaling campaign.

| Reviewed file | SHA-256 |
| :--- | :--- |
| `paper.tex` | `1292bf4d66c684e87b1afa1aa73980646076d017d8284710bc95e8f6ad82f159` |
| `paper.pdf` | `f5cac24d1a9dafc77f97800031bab2a546f95899f1ba976aa8a7d1d5d20fbeb1` |
| `generated/journal_macros.tex` | `3478086c37f45ca7d42a54439d87cba7a03a444399595cf9e32c940fda44ef51` |
| `revision_manifest_round2.json` | `db9aa7fa6ef92fece85a0b3925438a88a757484d0f9cfd391cbaa7680e873727` |

## 3. Closure of the previous Reviewer 1 requests

The following is an assessment of the revised manuscript and available implementation, with raw-evidence confirmation reserved where needed.

| Second-round task | Current assessment |
| :--- | :--- |
| R1B-01: survival duration and estimand | Addressed in the manuscript. The duration/percentage macro error is corrected. Design-beam 97.0%/96.1% survival is separated from the larger-emittance 93.0%/89.5% case. Nominal, edge and degraded-ring long-turn checks are reported. |
| R1B-02: off-midplane independent validation | Addressed in method and reporting. DOP853 independently integrates the stated paraxial equations; eight launches include final edges, vertical motion and momentum offsets. The table reports both-plane discrepancies. Raw slice/span records still require the attachment. |
| R1B-03: correction and stochastic estimand | Addressed. The x/px translation is explicit; vertical errors, optics distortion and shot terms remain. The joint distribution is conditioned on ten saved rings. Small Twiss mismatch is no longer presented as capture robustness. |
| R1B-04: jitter inference | Addressed in interpretation. The final paired quarter-minus-zero result is +2.2 points, interval −1.5 to +6.1; it does not establish the one-point loss margin. The previous zero-cost and universal quarter-jitter specification claims are removed. |
| R1B-05: pulse assumptions | Addressed for the declared ideal single-pass scope. Native nominal return positions, finite-support peak-phase formulas, a compatible pulse example and timing/train qualifications are present. Time-dependent capture is not claimed. |
| R1B-06: map and control claims | Largely addressed. Vertical sign and focusing are correctly qualified; thin controls are not treated as optimized systems or a unique decomposition of nonlinearity. The remaining literature-positioning issue is C1 below. |
| R1B-07: transparency observable | Addressed in scope. Centroid cancellation, finite moments, first-50-turn amplitudes and turn-1000 emittance are separated. New geometry/current sensitivities are explicitly local single-error limits. One remaining unit definition needs clarification. |
| R1B-08: presentation and uncertainty | Substantially addressed. Captions describe sampling and deterministic quantities, and the control panel has a paired inset. The article can still be streamlined. |
| R1B-09: usable evidence | Packaging is documented and previously verified according to the archive, but the actual attachment is unavailable to this review. Not independently closed here. |
| R1B-10: reconciliation and response | A new point-by-point response and D14 verification record exist. Earlier reviews were retained. Their reported 702-test and build results were not rerun in this review. |

## 4. Required substantive revisions

### C1 — Establish the contribution relative to directly overlapping literature

The introduction and bibliography omit [Sun et al., PRAB 23, 010702 (2020)](https://journals.aps.org/prab/pdf/10.1103/PhysRevAccelBeams.23.010702). Its section II.D describes segmented drift–kick–drift tracking and Runge–Kutta integration. Its section III also validates an infinite-conductor approximation with a finite three-dimensional Biot–Savart conductor model including return loops. Thus finite-field tracking itself is established work, not the new contribution here.

Adding a citation alone is insufficient. Identify what the present analysis adds: for example, a resolved matching-angle/error-sensitivity change, a quantitative approximation-error comparison, or a useful domain of validity organized by the sagitta ratio. Compare the questions and assumptions before contrasting outcomes. Different geometries and launch conditions can explain different conclusions; do not infer that the earlier model was invalid. The present study need not reproduce ALS or claim a universal law to be publishable, but its incremental physical result must be explicit.

### C2 — Supply the numerical attachment actually needed to evaluate the revision

The new central claims depend on absent campaign-03 evidence. Restore or supply the existing frozen attachment, confirm its archive hash and internal inventory, then check the selected artifacts against the active manifest and regenerate the reported macros in an isolated directory. In particular, verify the final ODE/spans, nominal and edge first-loss records, corrected-ring diagnostics, joint-error pairings and held-out tuning inputs.

This is an evidence-access requirement, not a demand for new simulation data or a mandatory public DOI. A real referee attachment is sufficient. If the existing bundle is simply stored elsewhere, document its usable location and access. Do not silently regenerate a different campaign under the same manifest or report the historical checks as checks performed now.

### C3 — Explain the robustness hierarchy without conflating populations

The reported progression is scientifically consequential:

| Condition | Reported capture descriptor |
| :--- | :--- |
| Ideal design lattice, design beam and reference chamber | 97.0% at 500 turns; 96.1% at 4000 |
| Ten corrected rings, otherwise chamber study conditions | Mean 61.7%; range 2.7–87.4% |
| Final assumed joint budget, 150 machine/shot draws | NKM mean 14.8%, interval 11.2–18.8% |
| Zero booster jitter, 50 paired seed-42 joint draws | Mean 34.1% |
| Ideal-observable tuning, zero / quarter jitter | Means 45.7% / 41.8% |

The paper correctly qualifies these values, but the discussion mostly restates their conditional nature. Explain what these results teach about the injection design. Is the selected operating point mainly limited by corrected-ring acceptance, residual BTS vertical motion, a centroid displaced from the kick maximum, or the conjunction of several effects? Where the existing data permit, summarize loss categories and capture by corrected-ring identity, and compare paired zero/full-jitter cases. Avoid claiming causal attribution from partial rank correlations alone.

The 61.7% ring-only mean and 14.8% joint mean are from different sampling designs; their subtraction is not an isolated effect of BTS/shot errors. Likewise, the 19.8% full-jitter seed-42 subset and 14.8% pooled mean are not conflicting results. Explain the population/sample distinctions near the relevant figure. The failed 20 micrometre correction target and adopted 100 micrometre scenario should remain visible. A weak practical design can still yield useful physics, but high nominal capture should not dominate the interpretation of its low robust capture.

### C4 — Turn the sagitta plot into an assessable approximation-error result

The current scaling figure shows horizontal momentum differences versus eta across 30 centroid configurations. It supports a finite-length trend and much closer agreement of the sliced map in the tested family. However, absolute momentum differences change with kick strength as well as geometry. They do not establish that eta alone controls the error.

Define K and w precisely in the main text, state the initial centroid recipe from the supporting note, and provide a compact summary of absolute and relative discrepancies for the thin and sliced models. A normalized error such as absolute delta-p_x divided by the nominal kick, together with the existing raw configuration labels, would clarify what the ratio organizes and what scatter remains. Explain the rationale for the sagitta factor and its reference path rather than treating it as a new universal formula. Relate the nominal discrepancy to a stated angular-response accuracy requirement, while retaining the restriction to the tested family and centroid launches.

Do not enlarge this into an arbitrary multi-facility study. Replotting or tabulating the already saved scaling data and narrowing the claim may be enough. This task is particularly useful for establishing the distinct contribution requested in C1.

## 5. Clarifications and editorial revisions

### C5 — State the units of the aligned moment changes

Section 6 says projected emittance changes are 4.5e−7 horizontally and 1.6e−7 vertically without explicitly identifying them as fractional changes. The method note and analytic covariance calculation indicate dimensionless increments in the emittance ratio, rather than absolute emittances in m rad or percentages. Write the observable as delta-epsilon/epsilon and distinguish it from beam-size change and the later filamented-emittance estimate.

Keep the 0.29–2.04 micrometre wire limits as one-error, ideal-observable sensitivities. They do not demonstrate that a complete magnet can be manufactured within a simultaneous budget. No shimming/compensation demonstration is required if that qualification is maintained.

### C6 — Label the jitter-margin inference as noninferiority, not equivalence

The implementation assesses whether the lower 95% paired-difference endpoint exceeds minus one percentage point. That is a one-sided acceptable-loss/noninferiority question, not two-sided equivalence. The present interval fails that criterion, so the manuscript's cautious conclusion is appropriate. Use consistent terminology in supporting documents and responses. If “predeclared” is retained, identify the dated plan/configuration where the one-point margin was fixed before inspecting the final results; otherwise simply call it the declared analysis margin. No extra sampling is required merely to replace an unsupported equivalence claim with an inconclusive finding.

### C7 — Make the main article easier to read without removing scientific limits

The article is now 19 pages and contains a large number of assumptions, historical diagnostics and numerical checks. Length alone is not a rejection reason. Nonetheless, the physical argument is harder to follow because design-beam conclusions are interleaved with the 100 nm sensitivity case and extensive wire derivative tables.

Consider moving full derivative arrays, the secondary sensitivity-case acceptance plot and procedural details to supplementary material. Keep a concise main-text summary of the model validation, finite-length mechanism, final chamber results, robustness hierarchy and transparency sensitivity. Explain “first failed grid” versus a stable acceptance edge clearly. Long captions can retain sample definitions while moving repeated bootstrap settings to a common methods paragraph.

### C8 — Keep the submission package consistent with the chosen scope

Update the cover letter and claim-to-evidence table around the demonstrated finite-length result and conditional robustness limitations. Provide the actual numerical attachment with a verified entry point. Preserve the statement that deterministic radiation is used without stochastic excitation, and that pulse evolution, local septum leakage, actual IVU/chamber geometry and newer KLS lattice versions are not validated. Select a journal and apply its format only after the author decides; this review does not authorize publication or change the manuscript's scientific inputs.

## 6. Conditions for acceptance in a subsequent review

I would reassess favorably after the manuscript establishes its distinct contribution relative to the overlapping literature, the existing final evidence can be inspected and rebuilt, and the robustness/scaling results are synthesized into a clear physical conclusion. C5–C8 are limited clarifications or submission preparation. No general hardware-efficiency or complete-transparency claim should be reintroduced.

If the evidence verifies and the literature comparison establishes a substantive incremental result, I see no reason to reopen the resolved second-round issues merely to increase the size of the study. If the novelty comparison shows that the claimed new result is already established, the contribution would need reframing or additional justified analysis; journal formatting alone would not solve that issue.
