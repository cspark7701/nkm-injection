# Reviewer 2 — BTS manuscript, round 5

**Date:** 2026-10-31. Internal pre-submission assessment; this recommendation is not a journal decision.

**Manuscript:** *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*, Chong Shik Park.

**Reviewed version:** `main` at `50d46991ca91290a500c7c3b50ca85f297dec6c7`: the 19-page [article](../paper.pdf), its [TeX source](../paper.tex), the 10-page [supplement](../supplement.pdf), supplementary source and bibliography. The revision cycle is round 5; its latest joint response answers **review round 4**.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `6354005e0c5846c2513b3e019b25b94cf62604d61efcfeb4d5309cf4a03a575b` |
| `paper.pdf` | `315add56394a78edef721e4a243f341bbe71f25f1ab66b736c6c20460f138064` |
| `supplement.tex` | `9faa2a3bad9b4214d081e518f818c06082fe2d4a29664f009b3d12e55b3c0e20` |
| `supplement.pdf` | `2ff3418e64744099a6a5a6f228e319486fa1779c0da1b87c9fb1a9dd4781ff10` |
| `paper.bib` | `f70c675c47c1e0103a8f5b8bf333eab1fd8caf26b05ab499f1c15429ad753d55` |

## Recommendation and acceptability

**Minor revision. The scientific study is acceptable in principle, but I would request the bounded corrections below before recommending acceptance of the revised text.** My round-4 recommendation of major revision is no longer warranted. The three required scientific remedies in that report have been addressed: the two jitter regimes are distinguished, the primary comparisons share reading errors, and the headline statistic is a defined jitter-integrated gain with uncertainty.

The paper now supports a coherent accelerator-physics result. With matched boundary optics, reducing interior peak beta does not improve the nominal clearance at the limiting blade. Horizontal phase advance changes how entrance jitter reaches that blade, at a cost in exit angle. At much smaller betatron jitter, blade loss becomes negligible within this model and residual trajectory correction becomes the more relevant limitation. This is a useful parametric simulation article, with a stated model, controlled comparisons and an identifiable physical mechanism. It does not establish operating transmission, ring-capture efficiency or hardware tolerances.

The remaining issues concern numerical wording, evidence scope and consistency. They do not require a new large campaign, measured KLS jitter, vertical correction, a new lattice, or a global optimization proof. Shortening remains desirable but is not a scientific acceptance condition.

**Deferred scope:** the user's “RS-BTS09” is interpreted as the existing **R5-BTS-09** author-decision item. Its journal/access/approval and associated submission-stage decisions remain deferred until the submission-ready stage. They are excluded from the [round-5 revision checklist](review_round_04_reviewer_02_tasks.md) and do not drive this scientific recommendation. No such decision is inferred or marked complete here.

## Author responses and evidence considered

I read all eight preserved author-response documents:

- Historical BTS-branch responses [01](historical_branch_review_round_01_author_response_to_reviewer_01.md), [02](historical_branch_review_round_02_author_response_to_reviewer_02.md) and [03](historical_branch_review_round_03_author_response_to_reviewer_03.md).
- Main-branch responses to Reviewer 1 [round 1](review_round_01_author_response_to_reviewer_01.md) and [round 2](review_round_02_author_response_to_reviewer_01.md), and to [Reviewer 2 round 2](review_round_02_author_response_to_reviewer_02.md).
- Joint responses to [review round 3](review_round_03_author_response_to_reviewers_01_02.md) and [review round 4](review_round_04_author_response_to_reviewers_01_02.md).

The historical branch's acceptance language and its older aperture, emittance and engineering claims do not establish acceptance or validity for the current model. The later main-branch revisions explicitly supersede several of those claims. I assessed the current article and evidence, rather than combining incompatible historical campaigns.

I also examined both round-4 referee reports, the [executed revision plan](revision_round_04_plan_for_review_round_04.md), [round-5 protocol](../round5_protocol.json), [reproduction guide](../round5_reproduction.md), generated tables and `generated/round5.json`, and the selected raw final-test and edge-study records. I read extracted text of both PDFs and inspected the rendered primary comparison table on article page 13.

## Disposition of the previous requests

| Previous request | Round-5 assessment |
| :--- | :--- |
| R2D-01: low-jitter residuals and two regimes | Resolved in substance. Table 8 and the abstract report approximately 0.18 mrad horizontal residual and 1.07 mm uncorrected vertical centroid. A few absolute statements still need qualification, below. |
| R2D-02: shared monitor errors | Resolved. The protocol keys static reading noise by realization and monitor. Shared readings replace per-setting noise in the main test and layout comparison; older comparisons are disclosed. |
| R2D-03: defined headline estimator | Resolved. The gain is a ratio of mean jitter-integrated losses, with paired realization-bootstrap uncertainty, on a declared primary population. |
| R2D-04: lower phase edge | Substantially resolved by a targeted dispersion study. This establishes sensitivity within the searched family; it does not prove a unique binding mechanism. |
| R2D-05 and R2D-11: consolidation | Partly resolved. The earlier fresh test and sampled sensitivity table moved to the supplement, and the jitter figure was simplified. Nineteen pages remain, but the scientific evidence need not be enlarged or removed to satisfy an arbitrary page target. |
| R2D-06: angle-aware weighting | Resolved as a sensitivity test. The reported 0.413 to 0.411 mrad change supports a limited conclusion about that weighting, not a general impossibility result. |
| R2D-07 and R2D-08: consistency and formatting | Substantially resolved. Remaining denominator and cross-reference corrections are identified below. |
| R2D-09: citations | The response records removal of the unsupported stability generalization and correction of the conference-record description. No new independent literature audit was performed in this review. |
| R2D-10: submission decisions | Deferred as instructed; not a revision-checklist item. |
| R2D-12: point-by-point response | Resolved by the new joint response. A response to this review should accompany the next revision. |

The latest response also addresses Reviewer 1's distinctions between conditional predictions, integrated predictions and observed counts. I agree with those distinctions and with restricting phase-only statements to the nominal matched model; this does not substitute for Reviewer 1's own reassessment.

## Evidence checks and their limits

The evidence audit passes all **73 claim pointers** and the selected manuscript/asset hash verification passes. The **25 round-3/round-4 tests** pass. These checks establish consistency of selected records, not universal physical validity, and I did not rerun the production simulations or the full repository suite.

From the 200 raw primary-test records, I independently reconstructed:

- Mean integrated losses of **0.0132259606661** and **0.00295197735933** as fractions for the matched reference and edge setting. Their ratio is **4.48037334**; the declared 10,000 paired resamples with seed 97005 reproduce **[4.32593473, 4.62891107]**. The abstract's **4.48 [4.33, 4.63]** is supported within the stated nominal-covariance, linearized Gaussian surrogate.
- Observed counts of **11,673**, **10,104**, **942** and **1**, against shot-conditional expectations of **11,705.22**, **10,153.74**, **880.45** and **0.5092**. The integrated dispersion-free expected-count equivalent is about **75.73**, which is a differently conditioned quantity.
- The same per-shot lost counts for the original loss-based setting, its duplicate and the edge setting. The stronger particle-identity statement is recorded by the response; aggregate raw counts alone do not independently prove individual particle identities or equivalence of every perturbed map.

The roughly 2.1-Poisson-standard-deviation excess in the edge row remains disclosed. I do not require a fresh campaign merely to eliminate this fluctuation. It should remain an unresolved validation discrepancy, with the standard-deviation calculation identified as a diagnostic approximation rather than a model-accuracy certificate. The single dispersion-free loss likewise cannot validate the unconditional tail at stated relative precision.

## Required minor corrections

### C1. Define the denominator of the validation discrepancy

On page 13, Section 4.3 says 942 losses against 880 expected is “6.5 % more”; the Discussion repeats the percentage. The exporter computes `(observed − expected) / observed`. Using the unrounded edge expectation:

\[
100(942-880.453324)/942=6.5336\%,\qquad
100(942-880.453324)/880.453324=6.9903\%.
\]

Thus the model prediction is **6.5% below the observed count**, or the observed count is **7.0% above the prediction**. Either convention is acceptable if named consistently. Correct the text and the generating convention or label; retain the actual counts and the unresolved-discrepancy caveat. This is a reporting correction, not a change to the headline gain. When retaining the 2.1 figure, call it the reported Poisson approximation; it does not include model-systematic uncertainty or constitute a general validation tolerance.

### C2. Keep conclusions within what the tests establish

Three small qualifications are needed:

1. **Dispersion and the phase edge (Sections 4.3, 4.4 and 5).** The D′ sweep strongly supports the inherited dispersion conditions as an important restriction on the phase range found. However, the selected 32, 16 and 0 mrad searches stop at their iteration limits. At D′ = 0, only two of the three starts meet the driver's matching test: the `dispersion_free_best` start is recorded as `matched=false`. Correct the statement that all three starts establish the same matched edge. Carry the existing local-search qualification into Section 4.4 and the Discussion; describe a best-found phase shifting with D′, rather than an established exclusive cause. A new global search or proof is unnecessary.
2. **Steering (Section 4.2).** Changing one endpoint weight from 3 to 10 with negligible improvement establishes that this tested reweighting does not materially improve the exit-angle rms. It does not establish that every scheme using position readings is incapable of improving angle, or that a direct angle measurement is necessary. The paper itself uses two separated position readings to constrain angle indirectly. Restrict the remedy statement to this instrumentation/error model and this weighting test; other estimators or layouts were not exhausted.
3. **Regime and residuals (abstract and Discussion).** Attach “at the assumed stress-level jitter” to the opening statement that jitter dominates. Replace “the choice of μ_x does not reduce” the residual by a statement about the tested settings and correction scheme. Changing strengths also changes error response; the nominal transfer theorem does not prove invariance of corrected static residuals. Keep the low-jitter practical conclusion, which is supported.

### C3. Remove a stale primary-test statement and clarify retained populations

Section 4.2 states that the low-beta loss change is unresolved on the fresh test of Section 4.3. The current primary test there instead gives **−0.13 [−0.24, −0.04] percentage points**, resolving a decrease on that population. The unresolved result belongs to the earlier test now in supplement Section 5. Name the earlier test explicitly and link it correctly, preserving the population-dependent conclusion already stated in the Discussion.

Label the inherited jitter/blade-sweep predictions sufficiently clearly to distinguish their earlier loss-based setting and reading-noise convention from the new shared-reading primary comparison. Their source files are already retained; no rerun is required merely to keep them as labelled sensitivity results. Remove ambiguous table-generation numbers from current status/response descriptions when they no longer match the compiled article; the primary test is now Table 6 and the residual table is Table 8.

## Editorial advice and final assessment

The article remains longer than its central argument needs. A further edit could compress repeated descriptions of the baseline, Gaussian surrogate and historical campaigns. Keep the author-requested baseline plots and literature discussion if desired; do not omit adverse outcomes or necessary assumptions to hit a page target. I do not make shortening a condition of scientific acceptance.

The revised manuscript has moved beyond a technical campaign report: it explains a constrained design trade, tests it on paired held-out machines and states where that trade ceases to matter. Its scope remains a study of the specified design version and assumed errors. After C1–C3 and a consistent response/evidence update, **I would recommend acceptance on scientific grounds**. Formal submission readiness and the deferred author decisions are separate stages.

The executable checklist for this review is [Reviewer 2 round-5 revision tasks](review_round_04_reviewer_02_tasks.md). No manuscript revision was executed by this review; earlier reports and responses are preserved.
