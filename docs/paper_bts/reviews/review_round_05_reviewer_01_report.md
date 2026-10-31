# Reviewer 1: BTS manuscript, round 5

Date: 2026-10-31. Internal pre-submission referee assessment from the perspective of transfer-line optics, injection beam dynamics and numerical validation. This is a recommendation, not a journal decision.

Manuscript: *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*, Chong Shik Park.

Reviewed repository checkpoint: `79dce1959bea10c3dd34dd0bad4f139b4d84f303`. The current BTS scientific/reporting revision was completed at `db9d9f6`; the subsequent commit edits the separate NKM paper. I assessed the current **20-page article and 10-page supplement**, including the round-6 corrections. This is **Reviewer 1 review round 5**, not a retrospective assessment of the superseded 19-page version that Reviewer 2 reviewed in round 5.

## Recommendation and answer on acceptance

**Accept the scientific content within its stated conditional-model scope. I request no further mandatory scientific revision.** The outstanding scientific and reporting objections in my round-4 report have received satisfactory answers. Optional shortening and a technical evidence-package update are recorded separately below; neither changes this scientific recommendation.

The paper is now a defensible accelerator-design study. Its contribution is a quantified comparison of matched transfer-line settings under explicit aperture, jitter and correction assumptions. The boundary-optics result and the phase-advance representation are established beam-optics relations; the value of this article is their application to the active septum restriction, the controlled design comparisons, and the demonstration that the useful design criterion changes with the assumed jitter level. A new optimizer or a proof of global optimality is unnecessary for that contribution.

Scientific acceptability does not establish submission readiness. At the author's instruction, **R5-BTS-09 remains deferred until the submission-ready stage**. Journal choice, access wording, companion access, any supplied jitter specification and final author approval are not reopened as tasks in this assessment. No real journal acceptance, approval or delivery is inferred.

## Material considered and version identity

I considered all nine author-response documents, including the three restored branch records:

| Response sequence | Document |
| :--- | :--- |
| Historical branch, response 01 | [Author response 01](historical_branch_review_round_01_author_response_to_reviewer_01.md) |
| Historical branch, response 02 | [Author response 02](historical_branch_review_round_02_author_response_to_reviewer_02.md) |
| Historical branch, response 03 | [Author response 03](historical_branch_review_round_03_author_response_to_reviewer_03.md) |
| Main branch, Reviewer 1 round 1 | [Response](review_round_01_author_response_to_reviewer_01.md) |
| Main branch, Reviewer 1 round 2 | [Response](review_round_02_author_response_to_reviewer_01.md) |
| Main branch, Reviewer 2 round 2 | [Response](review_round_02_author_response_to_reviewer_02.md) |
| Joint response to review round 3 | [Response recording revision round 4](review_round_03_author_response_to_reviewers_01_02.md) |
| Joint response to review round 4 | [Response recording revision round 5](review_round_04_author_response_to_reviewers_01_02.md) |
| Response to Reviewer 2 review round 5 | [Response recording revision round 6](review_round_05_author_response_to_reviewer_02.md) |

The restored branch responses concern another manuscript version. Their acceptance statements, beam inputs and aperture assumptions are historical; they are not evidence of acceptance or validity of the current article. Later responses supersede earlier claims about optical identity, percentage denominators, the exclusive cause of the phase edge and steering limitations. Those superseded statements have not been treated as current conclusions.

I examined the current article and supplementary TeX, extracted text from both PDFs, inspected the rendered primary comparison and residual pages, and checked the previous Reviewer 1 report, Reviewer 2's round-5 report, the executed consolidated register, protocols, reproduction guides, generated tables and selected stage records. I also examined the current incremental packaging recipe to distinguish a local verification from a verified current delivery bundle.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `c185307080f621377ad67af824be88704eb5577d4a31d3fb50254f611de8c4d8` |
| `paper.pdf` | `735366a50e508694afa5c80dc479f57c29b411492ac27529cbdad036af79affc` |
| `supplement.tex` | `9faa2a3bad9b4214d081e518f818c06082fe2d4a29664f009b3d12e55b3c0e20` |
| `supplement.pdf` | `8817fb6a94fae353ef0afe5e390ac4a88e98ba994e00764c02a18142ac98a399` |
| `paper.bib` | `f70c675c47c1e0103a8f5b8bf333eab1fd8caf26b05ab499f1c15429ad753d55` |

## Disposition of my round-4 requests

| Previous item | Assessment of the current revision |
| :--- | :--- |
| R1D-BTS-01: validation and rare loss | Resolved. Section 3.3 distinguishes the nominal objective, nominal-covariance integrated surrogate, shot-conditional prediction and observed count. The second test discloses the edge-row discrepancy, and the dispersion-free count is not presented as precise validation of the integrated tail. |
| R1D-BTS-02: transfer equivalence and attribution | Resolved. The nominal phase-only statement is qualified; the manuscript uses nominal horizontal transfer equivalence. Shared reading errors now support the controlled comparison, and the low-jitter residuals are retained. |
| R1D-BTS-03: consistency of conclusions | Resolved. The low-beta benefit is small and population-dependent, with its associated horizontal phase change distinguished from vertical peak-beta reduction. The analytic dispersion-free study is distinguished from its sparse tracked test. |
| R1D-BTS-04: provenance, legend and current status | Resolved for the reviewed scientific files. The selected test path exists; the jitter figure uses found ranges; current status identifies the 20/10-page assets and preserves historical review-time states. |
| R1D-BTS-05: author/submission decisions | Deferred as instructed. Not marked complete and not used to demand another scientific revision. |
| R1D-BTS-06: final reconciliation | Local scientific reconciliation is satisfactory: current claims, selected hashes, source/PDF identity and relevant tests pass. Preparation of a new portable bundle for these latest files remains a technical delivery-stage follow-up, discussed below. |
| R1D-BTS-07: shortening | Partly adopted: older tables are in the supplement and the duplicated jitter figure panel was removed. Further editing is optional. The current length does not invalidate the scientific argument. |

Reviewer 2's round-5 corrections also improve the present files. The count discrepancy now has an explicit observed-count denominator. Only two zero-slope starts are reported as matched; iteration-limit flags remain visible. The effect of changing endpoint weights is limited to the tested weighting, and the retained jitter/blade sensitivities are distinguished from the new shared-reading primary comparison. These are appropriate bounded corrections.

## Scientific assessment

### Physical question and interpretation

The active restriction is specified rather than inferred from a peak-beta plot. For the nominal, exactly matched line, the boundary covariance fixes the blade envelope. Reducing interior beta therefore cannot be credited with a nominal blade-clearance gain. Under errors, the centroid and covariance depend on the setting, and the manuscript allows those effects in the numerical comparison.

The phase-advance representation then explains the remaining design trade in the nominal matched model: a setting can move assumed booster jitter between exit position and angle. The blade responds to position, while the downstream injection calculation must assess angle. The result is conditional on the supplied line, boundary targets and aperture geometry; the paper now keeps that scope visible. The unmatched baseline is a documented starting point, not a competing optimized design.

### Estimands, pairing and inference

The primary result is now a ratio of mean jitter-integrated losses over steered realizations, not the largest tracked gain among several finite-shot populations. The fresh post-processing check reproduces the reference and edge means of **0.0132259606661** and **0.00295197735933** as fractions, their ratio **4.48037334**, and the paired-bootstrap interval **[4.32593473, 4.62891107]**. The reported **4.48 [4.33, 4.63]** is supported for the stated linearized Gaussian, nominal-covariance surrogate. It is not a measured machine-efficiency improvement or an exact nonlinear average over the test's beta-factor mixture.

The primary count rows are also consistent with the recorded source values:

| Setting | Observed losses / 1,200,000 | Conditional expected losses |
| :--- | ---: | ---: |
| Matched reference | 11,673 | 11,705.22 |
| Low beta | 10,104 | 10,153.74 |
| Loss-based edge | 942 | 880.45 |
| Dispersion-free | 1 | 0.5092 |

The edge prediction is **6.5336% below observation** using observation as the denominator. The roughly 2.1-Poisson-standard-deviation diagnostic excludes model-systematic uncertainty, as the text now says. This unresolved discrepancy limits an accuracy claim; it does not, on the inspected evidence, justify reopening the whole design comparison or demanding more particles until a preferred agreement is obtained.

Similarly, the dispersion-free integrated expected-count equivalent is about **75.73**, distinct from the 0.5092 expectation conditional on the sampled shots. One observed loss does not determine the unconditional rare tail at a useful relative precision. The manuscript states that limitation. The line-event max/sum treatment and discrete aperture checks also remain explicit, so the Gaussian calculation is not presented as continuous-chamber transmission certification.

### Jitter regime and correction limitations

The stress-level result is useful because the jitter magnitude is stated and swept. At reduced betatron jitter, the negligible predicted blade loss does not establish a well-centred beam for injection. Table 8 retains the approximately **0.179 mrad** horizontal exit-angle RMS and **1.073 mm** uncorrected vertical centroid RMS at scale 0.1; the nominal horizontal angle jitter is only about **0.057 mrad**. Momentum jitter remains present even at zero betatron-jitter scale. The correction and instrumentation priorities follow from these residuals, not from the nominal phase partition alone.

The earlier per-setting-reading sensitivities are now labelled separately. They do not silently become shared-reading results. The conclusion about endpoint reweighting is limited to the tested weights and assumed reading errors. The absence of vertical correction is a declared model limitation; adding a new vertical correction system or an end-to-end ring study is not required to publish the present scoped result.

### Search scope and novelty

The constrained scans and local searches establish useful best-found settings. Their termination records prevent a global-reachability or unique binding-cause claim. In particular, the zero-slope failed start is no longer counted as a matched edge solution. A narrower search result is sufficient for the reported comparison.

The paper remains modest in novelty: it applies known optics and probability tools rather than introducing a new physical law or optimization method. The combination of a declared limiting blade, paired error studies, correction residuals and a regime-dependent design interpretation is enough to support the scientific article assessed here. A new generality campaign or commissioned hardware result would broaden it, but is not a condition of this recommendation.

## Remaining follow-up

**Optional editorial improvement.** The 20-page main article repeats parts of the model scope, baseline explanation and historical-comparison history. A focused edit could shorten those repetitions and leave one definition for each loss quantity. Retain the literature context and baseline plots the author wishes to keep. No page-count threshold, removal of unfavorable evidence or new numerical work is requested.

**Conditional technical preparation before evidence delivery.** The latest local checks verify the current files; they do not verify an extracted current referee bundle. The recorded round-5 increment predates the round-6 response and changed manuscript. Moreover, `scripts/package_bts_round5_increment.py` explicitly adds the round-5 runner/exporter/packager but does not add the new `scripts/audit_bts_round6_revision.py`, which the current reproduction guide invokes. A fresh bundle should include that script and the current records, then be checked from its extracted root before it is described as the portable evidence for this version. This is a concrete packaging issue, not a defect in the inspected calculations. It can be handled when technical delivery materials are prepared; no delivery is authorized by this review.

These follow-ups are separated in the [checkbox register](review_round_05_reviewer_01_tasks.md). There are **no mandatory scientific revision tasks**. R5-BTS-09 decisions remain deferred and are excluded from that queue.

## Verification performed for this assessment

- The evidence audit verifies **76 claim pointers and 49 selected artifact identities**; these artifacts are not all protected scientific source inputs.
- `package_bts_revision.py --verify` verifies **86 selected current asset hashes**.
- The seven relevant BTS test files give **46 passed**.
- A fresh run of `audit_bts_round6_revision.py` reproduces the selected post-processing checks exactly, including the paired-bootstrap headline, count rows, shortfall and match flags. Its output is retained at `results/bts_reviewer1_round5_audit_20261031/round6_checks.json`.
- The current article and supplement PDF text was reviewed, and article pages 13 and 16 were inspected as rendered images. No new production tracking, optimization, full-suite run, TeX rebuild or referee-bundle extraction was performed for this assessment.

I therefore recommend **acceptance on scientific grounds for the stated conditional study**, with optional presentation improvements and a separately identified technical delivery check. This recommendation does not predict or replace an editor's decision. No manuscript revision was executed in writing this report, and earlier review records remain preserved.
