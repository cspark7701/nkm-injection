# Response to the BTS filename-round-5 reviews

Date: 2026-10-31. This response addresses the current files named
[Reviewer 1 round 5](review_round_05_reviewer_01_report.md) and
[Reviewer 2 round 5](review_round_05_reviewer_02_report.md), with task IDs
R1E-BTS and R2F-BTS. Reviewer 2's retained report body calls its assessment review
round 6; its filename was subsequently shifted down one number. This execution
is implementation round 7. No earlier response is replaced.

## Reviewer 2

### R2F-BTS-01: controlled low-beta evidence

Completed in milestone [303](../../exec-plans/completed/303_r2f_bts_01_controlled_low_beta.md).
We adopted the offered wording alternative. Section 4.2 and the Discussion label
the older 0.21-percentage-point contrast as confounded by reading errors drawn
separately for each setting. The physical interpretation instead uses the
controlled shared-reading primary result, −0.13 [−0.24, −0.04] percentage points.
The historical comparison and its uncertainty remain available. No new steering
campaign was needed.

### R2F-BTS-02: model bounds and localization of the excess

Completed in milestone [304](../../exec-plans/completed/304_r2f_bts_02_shot_losses.md).
Section 3.3 now defines the max/sum bracket as bounds on probabilities within the
linearized Gaussian model. These probability bounds do not bound realized finite
particle counts; nonlinear tracking can also differ from the linearized model.

The saved primary-test records give **16 loss-bearing shots out of 600**, not
the 20 stated in the review. The 942 observed losses and 880.4533 expected losses
are unchanged. Machine 116, shot 2 loses 454 particles against 410.8915 expected;
its excess of about 43.1 particles accounts for about 70% of the aggregate excess
of 61.55. Section 4.3 reports these reconstructed values using generated macros.

The new post-processing audit records the exact inputs, per-shot values and
diagnostic binomial deviation. We did not perform the recommended nonlinear-moment
calculation. The manuscript therefore keeps the cause unresolved; it attributes
the excess to neither linearization nor sampling alone. The review and original
raw records are preserved.

### R2F-BTS-03: headline interval scope

Completed in milestone [305](../../exec-plans/completed/305_r2f_bts_03_interval_scope.md).
The abstract identifies the gain as a linearized Gaussian-model prediction at
the assumed jitter. Results state that the interval resamples error realizations
only, with Gaussian jitter integrated and nominal beam covariance fixed. Model
and input uncertainty are excluded. The gain remains 4.48 [4.33, 4.63].

### R2F-BTS-04: wording and labels

Completed in milestone [306](../../exec-plans/completed/306_r2f_bts_04_wording_figures.md).
The abstract and Discussion state that the modelled line has no vertical
corrector. Section 3.2 says “different tracked losses”; the dangling “therefore”
in the sensitivity passage is removed. Phase and blade-distance figures now use
“Loss-based” consistently, regenerated from the existing selected outputs.
The labels change; the underlying numerical data do not.

### R2F-BTS-05: optional shortening

Completed in milestone [307](../../exec-plans/completed/307_r2f_bts_05_shortening.md),
also addressing R1E-BTS-01. The older steering table has moved to supplement
Section 5 with its per-setting-noise caveat. Main-text references point to that
section, and repeated baseline and limitation passages are shorter. The article
is 19 pages and the supplement 10. Baseline plots, literature context, assumptions,
adverse results, paired intervals and the ring-capture limitation remain.

### R2F-BTS-06: reconciliation

Completed in milestone [308](../../exec-plans/completed/308_r2f_bts_06_reconciliation.md).
The current primary comparison is Table 5, layouts Table 4 and residuals Table 7.
Affected claim locations are updated; superseded per-setting-noise test claims
are labelled historical. Four saved-output diagnostic claims bring the evidence
audit to 80 claims. Current hashes select the final files, while the prior
86-asset table is preserved as `round6_final_assets_sha256`.

Both PDFs build without warnings in new directories. The 46 relevant BTS tests
pass. Changed tables and figures were inspected. The Humanizer skill was used
for manuscript prose, with scientific claims and notation preserved except for
the explicitly documented review corrections. No tracking or optimization
campaign was rerun.

## Reviewer 1

R1E-BTS-01 is addressed by the bounded shortening pass above. For R1E-BTS-02,
the new `package_bts_round7_increment.py` includes the round-6 and round-7 audit
scripts, current sources/PDFs, responses, selected records and milestone archive.
It uses a properly labelled round-7 inventory and archive, leaving previous
attachments intact.

A fresh extraction over the selected round-3 base verifies the increment's
inventory, all 80 evidence claims and current asset hashes. Both documented
post-processing audits run under an isolated interpreter using the extracted
scripts and reproduce the selected check records exactly. The package and its
verification record remain local; see the [reproduction guide](../round7_reproduction.md).

R5-BTS-09 remains deferred to submission readiness. No journal choice, access
decision, final author approval, public deposit, external delivery or acceptance
decision is made by this revision.
