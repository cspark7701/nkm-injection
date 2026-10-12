# Reviewer 1 — third-round revision tasks

Date: 2026-10-12  
Basis: [Third-round report](reviewer1_round3_20261012_report.md)  
Recommendation: focused major revision  
Status: **Proposed tasks; manuscript revisions not executed by this review.**

Preserve all previous review reports, plans and author responses. These tasks follow D1–D14 rather than repeating them. P1 denotes a substantive acceptance condition; P2 denotes a clarification or submission-quality requirement. Journal conversion remains the author's separate decision.

| Order / ID | Priority | Report concern | Output | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 01 / R1C-01 | P1 | C2 | Accessible verified final evidence | None |
| 02 / R1C-02 | P1 | C1 | Explicit literature/contribution comparison | None |
| 03 / R1C-03 | P1 | C4 | Quantified scaling-error interpretation | R1C-01, R1C-02 |
| 04 / R1C-04 | P1 | C3 | Robustness hierarchy and physical synthesis | R1C-01 |
| 05 / R1C-05 | P2 | C5 | Defined transparency observable and units | None |
| 06 / R1C-06 | P2 | C6 | Consistent margin terminology and provenance | R1C-01 |
| 07 / R1C-07 | P2 | C7 | Streamlined main article and supplements | R1C-02 through R1C-06 |
| 08 / R1C-08 | P1 | C8 and final gate | Consistent build, attachment and new response | All preceding tasks |

## 01 — R1C-01: make the frozen evidence available and verify it

Locate and supply the existing campaign-03 referee bundle or its complete selected files. The current checkout has 48 matching manifest artifacts and 157 absent artifacts, with no hash mismatch among the present files. This review could not locate campaign 03 or its tarball. The D13 archive records the earlier bundle hash as `0e07de5f2b49a9b9e6087af9f8b9969e9687b0aa537939b77b2325d1d8ec3f3d`.

**Acceptance criteria:** verify the actual archive and inventory, all 205 selected artifact hashes, and a byte-identical macro rebuild in an isolated new directory. Include final trajectory/spans, first-loss records, corrected lattices and residuals, actual paired draws, and training/held-out records. Record the environment, source snapshot and access entry point. If the bundle is elsewhere, document that location and ensure the intended referee can access it. Preserve historical evidence and do not relabel regenerated results as the original campaign. A journal attachment is sufficient; no mandatory public DOI or fresh full simulation campaign is imposed.

## 02 — R1C-02: establish the incremental contribution

Read and cite Sun et al., PRAB 23, 010702 (2020), particularly the field/tracking methods and finite-conductor comparison. Compare the study questions, approximations, geometry and observables with the present paper. Revise the introduction, abstract, discussion and cover letter around the distinct demonstrated result.

**Acceptance criteria:** a short comparison identifies established modelling tools versus the new physical result. Do not claim invention of sliced tracking, finite-field integration or nonlinear-kicker optimization. Explain why the current quantified finite-length sensitivity/accuracy result adds useful knowledge, without inferring that different published geometries are invalid. If overlap removes the proposed novelty, reframe honestly or justify a narrowly targeted new analysis; do not simply add a citation and keep the same implication.

## 03 — R1C-03: quantify what the sagitta ratio predicts

Use the existing 30-configuration scaling data after restoring access. Define K, negative-lobe FWHM w, reference trajectory and the initial centroid recipe. Tabulate or plot absolute and relative thin/sliced-map discrepancies, identify configuration families, and state the residual spread at comparable eta.

**Acceptance criteria:** readers can assess the nominal discrepancy against a declared angular-response accuracy criterion, distinguish changing kick strength from approximation quality and see the limits of a one-parameter organization. Include both-plane information when necessary for the stated vertical-field claim. Retain the family/centroid scope and avoid a universal capture threshold. Existing-data postprocessing is sufficient if it supports the narrowed claim; no arbitrary second facility or large particle campaign is required.

## 04 — R1C-04: explain the nominal-to-robustness loss hierarchy

Add a compact comparison identifying beam, aperture, ring population, additional errors, particle/realization counts and duration for each reported condition. Explain the difference between the ring-only mean 61.7%, final pooled mean 14.8%, seed-42 full-jitter mean 19.8%, zero-jitter mean 34.1%, and held-out tuned means 45.7%/41.8%.

**Acceptance criteria:** use saved ring identities, loss categories and valid paired zero/full-jitter data to describe supported mechanisms. Report the physical lesson of the low robust capture, not only a list of limitations. Do not subtract unpaired population means as causal effects or interpret partial correlations as causal rankings. Keep the failed 20 micrometre correction attempt and selected 100 micrometre scenario visible. No successful 80% design or causal decomposition must be invented; acknowledge what the existing data cannot isolate.

## 05 — R1C-05: define transparency moment changes precisely

Label the aligned 4.5e−7/1.6e−7 projected emittance changes explicitly as dimensionless delta-epsilon/epsilon if that is the artifact definition. Reconcile the analytic observable, generated macro, caption and prose. Keep centered emittance, filamented coherent contribution and tracked turn-1000 emittance separate.

**Acceptance criteria:** every moment-growth number has an equation or explicit unit/normalization; centroid amplitudes retain their first-50-turn observation definition. One-wire/current limits remain local single-error sensitivities, not simultaneous construction specifications. No new manufacturing or compensation campaign is required for this clarification.

## 06 — R1C-06: reconcile the acceptable-loss margin and inference

Use noninferiority/acceptable loss for the lower-endpoint test against minus one percentage point. Reserve equivalence for an actual two-sided equivalence condition. Identify evidence of the margin's declaration before final-result inspection if calling it predeclared; otherwise remove that chronology claim.

**Acceptance criteria:** manuscript, method note, response and statistical labels describe the same test and direction. The +2.2-point estimate with −1.5 to +6.1 interval remains inconclusive for the one-point acceptable-loss criterion. Do not increase sample counts merely to obtain a desirable conclusion; the existing inconclusive result is publishable when stated accurately.

## 07 — R1C-07: simplify presentation around the scientific argument

Decide which full derivative tables, historical larger-emittance diagnostics and procedural material belong in supplementary material. Preserve essential assumptions and uncertainty definitions in the article. Keep a main-text chain from finite-length mechanism through accuracy, chamber acceptance, robust capture and transparency limitations.

**Acceptance criteria:** main and supplementary figures/table references resolve; design-beam and 100 nm sensitivity cases are unmistakable. Important limitations remain visible in the abstract/discussion/conclusion. Streamlining is an editorial choice, not a demand to meet an invented page limit or remove unfavorable results.

## 08 — R1C-08: final submission reconciliation and new response

After resolving the scientific tasks, rebuild from the verified evidence and inspect the article/supplement. Update claim-to-evidence mapping and cover letter. Write a new dated round-three response rather than modifying the previous reports or responses. Apply journal format only when the author has selected the venue.

**Acceptance criteria:** source/PDF/supplement/attachment agree on values, units, scope and new contribution. Existing evidence reproduces the macros and required publication checks pass. Run numerical tests appropriate to any actual code changes; no numerical test campaign is needed for pure editorial changes. Protected sources remain unchanged; results stay separate. Archive each executed revision and report its actual verification. Do not submit, upload externally or push without explicit authorization.

## Scope of this register

R1B-01 through R1B-08 are substantially addressed by the revised manuscript, subject to inspecting their final raw evidence. Do not reopen them by default. These new tasks target literature significance, missing review access and remaining interpretation, with conditional follow-up only if verification uncovers a real inconsistency. Their completion enables another assessment; it does not predetermine acceptance by a journal.
