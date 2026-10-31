# Reviewer 1 — BTS manuscript, review round 6

Date: 2026-10-31. Assessment: internal pre-submission scientific review.

**Recommendation: accept the scientific content within its stated conditional-model scope. No mandatory scientific revision remains from this assessment.** This is a referee recommendation, not a journal's acceptance decision. The deferred author decisions are separate from this scientific judgement.

## Material assessed

The manuscript is *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*, by Chong Shik Park. This review assesses the scientific files selected at commit `fd16b2a3a823a9d662de6dee299c79c3f1da4978`, after implementation round 7: the 19-page [article](../paper.pdf), its [source](../paper.tex), and the 10-page [supplement](../supplement.pdf). Review round 6 here is Reviewer 1's sequence; it does not rename the historical implementation cycles or Reviewer 2's earlier report bodies.

Selected SHA-256 identities:

| File | SHA-256 |
| :--- | :--- |
| `paper.tex` | `c104f180a476c63f31b74aadc54a2cb3e2df818bf519353013f3db1974b83644` |
| `paper.pdf` | `31db583223793bd5aba1db081d2055ba8dfe529c733156a5e73630df7686bdf5` |
| `supplement.tex` | `7080d250c5dbebf8b63f63f69979724d423a6abc29b887ef109d0d4db658f3b0` |
| `supplement.pdf` | `04c94cf1a89ef3a3994815a0a5bce25a13deeea9c025d54dba37be098a7a2dbf` |

The assessment considers all ten author-response documents. The three restored branch responses concern older manuscript versions and provide history, rather than validation of the current article:

- [Historical branch response 1](historical_branch_review_round_01_author_response_to_reviewer_01.md).
- [Historical branch response 2](historical_branch_review_round_02_author_response_to_reviewer_02.md).
- [Historical branch response 3](historical_branch_review_round_03_author_response_to_reviewer_03.md).
- [Main response to Reviewer 1, round 1](review_round_01_author_response_to_reviewer_01.md).
- [Main response to Reviewer 1, round 2](review_round_02_author_response_to_reviewer_01.md).
- [Main response to Reviewer 2, retained round-2 filename](review_round_02_author_response_to_reviewer_02.md).
- [Joint round-3 response](review_round_03_author_response_to_reviewers_01_02.md).
- [Joint round-4 response](review_round_04_author_response_to_reviewers_01_02.md).
- [Round-5 response to Reviewer 2](review_round_05_author_response_to_reviewer_02.md).
- [Latest joint response to the filename-round-5 reports](review_round_05_author_response_to_reviewers_01_02.md).

The latest response is checked against the current article, selected records and reproduction material, rather than accepted solely on its completion statements. The [previous Reviewer 1 report](review_round_05_reviewer_01_report.md) already recommended scientific acceptance; this assessment tests whether the subsequent changes preserve that conclusion and close its two follow-ups.

## Scientific judgement

The paper now presents a coherent applied accelerator-physics result. Optical matching fixes the nominal exit beam, but transport of injection jitter depends on the matched phase advance. A lower beam envelope alone is therefore insufficient to predict blade losses. The controlled comparison identifies a lower-loss phase-edge setting and quantifies the cost in exit-angle jitter. The study also identifies the inherited dispersion-slope target as a constraint on the accessible matched range. These are useful design findings even though the optimization and tracking methods themselves are established.

The strongest evidence is the independent shared-reading test, now Table 5. Across 200 error realizations, three shots each and 2000 particles per shot, the reference loses 11673 particles, low beta 10104 and the loss-based setting 942. The paired low-beta contrast is −0.13 [−0.24, −0.04] percentage points. Unlike the older per-setting-reading comparison, this result controls the reading-error draw. The article explicitly labels the older 0.21-percentage-point contrast as confounded and retains it in the supplement. The response has satisfactorily corrected the interpretation without manufacturing a new campaign.

The headline gain, 4.48 [4.33, 4.63], is a ratio of mean jitter-integrated losses predicted by the linearized Gaussian model at the assumed jitter. The interval resamples error realizations, with jitter integrated and nominal beam covariance fixed. It excludes model and input uncertainty. This scope is now stated clearly enough that the ratio need not be mistaken for a measured transmission improvement or an unconditional prediction for a commissioned beam line.

The adverse evidence is retained. For the loss-based setting, the shot-conditional expectation is 880.4533 lost particles against 942 observed. The prediction is approximately 6.5% below the observed count. Saved records show **16**, rather than the earlier review's 20, loss-bearing shots. Machine 116, shot 2 contributes 454 observed losses against 410.8915 expected, accounting for about 70% of the aggregate excess. The correction to the review's count is supported and should stand. The cause remains unresolved because a nonlinear-moment calculation was not performed. The diagnostic deviation does not validate a general accuracy tolerance, and the manuscript does not claim one.

The probability bracket is also correctly restricted to the linearized Gaussian event model. Bounds on model probabilities are not hard bounds on finite sampled particle counts. This distinction removes the previous conceptual ambiguity without concealing the discrepancy between tracking and the surrogate.

The remaining limitations are acceptable for the stated contribution: the chamber/aperture and jitter assumptions are not commissioning measurements; the aperture checks do not certify a continuous physical chamber; phase-edge searches do not prove a global optimum; the low-jitter regime has negligible blade loss but retains steering residuals; and the model has no vertical corrector. The very small dispersion-free loss count cannot establish precise tail accuracy. Ring capture, hardware tolerances and operational transmission remain outside the demonstrated result. None of these limitations is presented as a completed validation.

## Disposition of the responses and prior follow-ups

All six R2F-BTS corrections are satisfactory for this assessment: controlled low-beta interpretation, probability-bound scope and loss localization, interval scope, residual wording and figure labels, bounded shortening, and reconciliation of the selected evidence. This does not turn the optional nonlinear diagnostic into a required new study. Leaving its cause unresolved is scientifically defensible at the present claim level.

**R1E-BTS-01 is closed.** The older steering table has moved to supplement Section 5 with its noise caveat. The article is shorter, while retaining baseline plots, literature context, paired uncertainty and negative findings. The primary comparison is Table 5, layouts Table 4 and residuals Table 7. No additional arbitrary length reduction is required by this review.

**R1E-BTS-02 is closed.** The current local increment includes both post-processing audit scripts and the selected scientific files. Its inventory and current scientific identities agree with the verified extraction. The recorded isolated checks reproduce the selected audit records. Earlier packages remain historical attachments; they are not represented as containing this revision. Adding the present review does not change those scientific files or require another package solely to carry this report.

Reviewer 2's separate [round-6 report](review_round_06_reviewer_02_report.md) also recommends acceptance and offers optional suggestions. Those suggestions remain that reviewer's register. They do not create additional mandatory tasks in Reviewer 1's assessment.

## Verification and limits of this review

Checks performed for this assessment:

- The evidence audit passed 80 claim checks against 50 selected artifact identities; current asset verification passed 90 selected hashes.
- The seven relevant BTS test modules passed: **46 tests**.
- Fresh runs of the round-6 and round-7 post-processing audits reproduced their selected JSON records exactly, under `results/bts_reviewer1_round6_audit_20261031/`.
- The current increment's archive digest and all 547 inventory entries were verified. Current article, supplement and evidence/selection files match the existing verified extraction. Its recorded evidence, asset and two isolated post-processing jobs all exited successfully. This review checked that extraction and its records; it did not create another extraction or rerun its isolated jobs.
- Both current PDFs were read through extracted text; the primary comparison page was also inspected visually.

No tracking or optimization campaign, fresh TeX compilation, complete repository test suite, or new bibliographic audit was performed during this review. These checks support consistency and reproducibility of the selected evidence; they do not independently establish the realism of assumed machine inputs.

## Decision and revision status

I would recommend acceptance of the scientific content at this stage. The paper's contribution is bounded but supported, and the responses have resolved the substantive interpretation and evidence issues. There is no further mandatory scientific revision list. The companion [closure checklist](review_round_06_reviewer_01_tasks.md) records the verified follow-ups rather than opening another revision cycle.

R5-BTS-09 remains deferred to submission readiness and is excluded from that checklist. Journal selection, access/delivery choices and final author approval remain author responsibilities. This review neither executes those decisions nor guarantees an editor's or another referee's acceptance.
