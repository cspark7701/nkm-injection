# Reviewer 2 — BTS manuscript, review round 6

**Manuscript:** *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker
injection at the Korea Light Source* (C. S. Park).
**Version reviewed:** the revision-round-6 article at `79dce19`: `docs/paper_bts/paper.tex`, `paper.pdf`
(20 pages), `supplement.tex` and `supplement.pdf` (10 pages). This version answers my
[round-5 report](review_round_04_reviewer_02_report.md) through the
[round-6 register](revision_round_05_plan_for_review_round_05.md).

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `c185307080f62137` |
| `paper.pdf` | `735366a50e508694` |
| `supplement.tex` | `9faa2a3bad9b4214` |
| `supplement.pdf` | `8817fb6a94fae353` |
| `paper.bib` | `f70c675c47c1e010` |

**Read first:**
- all main-branch author responses, including the
  [round-5 response to Reviewer 2](review_round_05_author_response_to_reviewer_02.md);
- my reports of rounds 2–5 and Reviewer 1's round-4 report;
- the round-5 and round-6 stage outputs I cite below.

**Date:** 2026-10-31. Internal pre-submission assessment, not a journal decision.

**Naming.** The request was to review the BTS paper "round 5". The round-5 report already exists and is preserved
unchanged. This assessment of the manuscript revised in response to it therefore uses the next review-round number.

**Scope.** The R5-BTS-09 submission decisions remain deferred to the submission-ready stage and are not assessed
here. They cover the journal, data-availability wording, companion access, the jitter source and final approval.

## Recommendation

**Minor revision: acceptable after the small corrections below. I do not need to see the paper again; the editor
or the author can verify them.**

The round-6 revision did what the round-5 checklist asked:
- the count-discrepancy percentage has a named denominator, and the 2.1σ is labelled a Poisson diagnostic;
- the phase-edge, angle-weighting and jitter-dominance claims are scoped to their local searches, tested weights
  and stress level;
- the test populations and cross-references are reconciled, and the retained sensitivities are labelled with
  their reading-noise convention.

The scientific result is sound, conditional and clearly bounded:
- matched ends fix the nominal blade clearance;
- in the nominal model the blade loss depends on μ_x alone;
- the optics-based loss reduction is a stress-level property;
- at low jitter, the steering residual and the uncorrected vertical trajectory dominate the delivered beam.

Three substantive points from my own round-5 assessment were not in the committed round-5 checklist, so the
revision did not address them. Each is a few sentences or a short post-processing step, and none changes the
paper's conclusions. They make the text consistent with the paper's own controlled evidence.

## Status of the round-5 checklist

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2E-BTS-01 count-discrepancy denominator | Resolved | "The prediction is 6.5 % below the observed count", with the Poisson diagnostic labelled and model-systematic uncertainty excluded. |
| R2E-BTS-02 claim scope | Resolved | The D′ = 0 start accounting is corrected (two matched starts), iteration limits are retained, angle weighting is restricted to weights 3 and 10, and jitter dominance is scoped to the stress level. |
| R2E-BTS-03 populations and references | Resolved | The stale Section 4.3 reference is fixed, and the sensitivities are labelled with their setting and reading-noise convention. |
| R2E-BTS-04 response and verification | Resolved | 76 claims verify. The reviewed snapshot is retained, and the round-5 hashes are preserved. |

## Remaining comments

### M1. The low-beta effect is still quoted from a population with per-setting reading errors

The Discussion says "low beta loses 0.21 and 0.13 percentage points less than the matched reference in the
steering comparison and the second test". Section 4.2 quotes the 0.21 [−0.39, −0.06] from Table 4 as a resolved
result.

Section 2.4 states that Table 4 used reading errors drawn separately for each setting. The paper's own controlled
experiment (Section 4.2) shows that per-setting reading errors alone change a tracked loss by more than half: the
loss-based setting gives 0.23 % with its own readings and 0.38 % with shared readings. The 0.21 is therefore not a
controlled low-beta effect. Only the 0.13 from the shared-reading primary test is.

**Requested.** Choose one:
- run low beta through the shared-reading layout stage on the Table 4 realizations, a few minutes, and quote that
  paired difference; or
- in Section 4.2 and the Discussion, label the 0.21 as confounded by per-setting reading errors, and base the
  low-beta conclusion on the primary test.

### M2. The per-shot "bracket" is contradicted by the tracked loss-based count; characterize the excess

Section 3.3 states that "per shot, the line loss is bracketed by the largest of these exact event probabilities and,
as an upper bound, by their sum". In the primary test, the loss-based setting loses 942 particles, while the sum
bound gives 880.7. The tracked count lies above the stated upper bound. This is a statement about the Gaussian,
linearized model, which the tracking does not obey for these shots, so the sentence needs that qualification.

The saved per-shot output (`results/bts_round5_campaign_20261031/final_test_b/raw_machines.json`) also shows where
the excess comes from:
- all 942 losses occur in 20 of the 600 shots;
- one shot contributes 454 lost particles against 410.9 expected, which is 43 of the 61.5-particle excess and
  about 2.4σ under its own binomial variance.

A shot losing about a fifth of its particles has its centroid within about one beam size of the blade, which is
where linearization about the centroid is weakest.

**Requested.**
- Qualify the Section 3.3 sentence as holding within the linearized Gaussian model.
- Add one sentence to Section 4.3 saying that the excess comes mainly from one near-blade shot.
- A nonlinear-moment check of that shot, with the round-2 Gauss–Hermite propagation applied to existing data, would
  let the paper say whether the cause is linearization or a fluctuation. I recommend it, but do not require it if
  the excess is reported as unresolved and localized.

### M3. Say what the headline interval covers

The abstract reports a "mean jitter-integrated loss 4.48 times smaller … (95 % interval 4.33–4.63)". Section 3.3
defines the estimator correctly, but the interval is narrow because only the static-error realizations are
resampled. The jitter enters analytically, and the value is close to the error-free ratio of about 4.7. A reader
of the abstract alone may take it as a measured gain with full uncertainty.

**Requested.** In the abstract or Section 4.3, add a short clause: the gain is a prediction of the linearized
Gaussian model at the assumed jitter, and the interval reflects the sampling of error realizations only.

## Minor comments

1. **Vertical residual.** The abstract and Discussion state that the vertical plane is uncorrected. Add that this is
   because the modelled line has no vertical corrector, so the 1.07 mm is not read as a property of the matched
   optics. The Discussion's instrumentation conclusion is otherwise well put.
2. **Section 4.5.** "For each steered realization we therefore also evaluate …": the "therefore" has no antecedent
   since the sampled roll table moved to the supplement.
3. **Section 3.2.** "The larger tracked losses of some test populations" is right for the earlier populations, but
   in the primary test the tracked loss (0.97 %) is below the integrated one (1.32 %). Write "different".
4. **Figures 5 and 6.** The legends still say "Loss-based (R3)", while the text and Table 6 use "Loss-based" for the
   converged edge setting. The two are equivalent, so use one name (`SHORT['robust']` in
   `export_bts_round4_assets.py`).
5. **Length.** The article grew to 20 pages, about 10,100 tokens before the references. This is advisory and not a
   condition of acceptance. Table 4 could move to the supplement once M1 is resolved through Table 5.

## Assessment

The paper is a careful parametric study with a correct mechanism, controlled comparisons and honestly stated
limits. The items above are text corrections and at most one short rerun. They bring two remaining statements into
line with the paper's own evidence, and say what the headline number is.

**I recommend acceptance after these minor corrections**, subject to the deferred submission decisions.

## Confidential comments to the editor

Across five rounds the author has repeatedly let new evidence overturn earlier statements. The round-5
shared-reading control is a good example.

I checked M1 against Sections 2.4 and 4.2, and M2 against the saved per-shot output. Neither affects the main
conclusions.
