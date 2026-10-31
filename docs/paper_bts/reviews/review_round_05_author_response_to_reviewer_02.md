# Response to Reviewer 2: BTS review round 5

Date: 2026-10-31. This response records revision round 6 against the
[Reviewer 2 report](review_round_05_reviewer_02_report.md) and
[R2E-BTS checklist](review_round_05_reviewer_02_tasks.md), through the
[consolidated register](revision_round_06_plan_for_review_round_05.md).
Earlier reports, responses and source task lists are preserved.

## C1 and R2E-BTS-01: count-discrepancy denominator

Completed as R6-BTS-01, milestone [295](../../exec-plans/completed/295_r6_bts_01_validation_percentage.md).
The manuscript now says that the prediction is **6.5% below the observed count**.
The calculation is 100 × (942 − 880.4533242328341) / 942 = 6.533617385%.
The exporter names the denominator, stores the reporting convention and generates
the corresponding macro. The observed count, conditional expectation and
integrated gain remain unchanged.

Section 4.3 identifies the 2.1-standard-deviation figure as the diagnostic Poisson
approximation (observed − expected) / sqrt(expected), excluding model-systematic
uncertainty. The unresolved-discrepancy caveat remains in Results and Discussion.
No general 1% accuracy claim is made for this row. The dispersion-free count is
still one loss against 0.51 conditionally expected; it does not certify the
integrated tail, whose expected-count equivalent is about 76.

## C2 and R2E-BTS-02: scope of the phase-edge and steering conclusions

Completed as R6-BTS-02, milestone [296](../../exec-plans/completed/296_r6_bts_02_claim_scope.md).
At fixed exit D = 0.080868 m, all three starts give matched candidates at
D′ = 0.032 and 0.016. At D′ = 0, two pass the declared matching test; the
`dispersion_free_best` start fails it. The matched changed-slope searches stop at
their iteration limits. The manuscript reports best-found phases and describes
their D′ dependence within these local searches. It makes no exclusive
binding-cause or globally certified-edge claim.

The endpoint-weighting conclusion is restricted to the tested weights, 3 and 10,
with the assumed 50 µm reading errors. It no longer states that position readings
generally cannot improve angle or that a direct angle measurement is necessary.
The abstract and Discussion scope jitter dominance to the assumed stress level;
the low-jitter residual conclusion refers to the tested settings and correction
scheme. The vertical trajectory remains explicitly uncorrected. No new search,
steering run or hardware capability is claimed.

## C3 and R2E-BTS-03: populations and cross-references

Completed as R6-BTS-03, milestone [297](../../exec-plans/completed/297_r6_bts_03_populations.md).
Section 4.2 now attributes the unresolved low-beta result to the earlier fresh
test in supplement Section 5. The primary test instead gives a resolved change
of **−0.13 [−0.24, −0.04] percentage points**. The population-dependent conclusion
is preserved.

The jitter and blade-distance sweeps are labelled as retained sensitivities using
the earlier loss-based setting and reading errors drawn separately for each
setting. The primary test uses the converged edge setting and shared readings.
The residual table is identified as coming from the earlier jitter sweep.
Exported metadata records these conventions. The compiled primary comparison is
Table 6; the residual table is Table 8. No old result directory was overwritten.

## R2E-BTS-04: response and verification

Completed as R6-BTS-04, milestone [298](../../exec-plans/completed/298_r6_bts_04_reconciliation.md).
The [reproduction guide](../round6_reproduction.md) records the commands and the
scope of the checks. A reviewed source/PDF snapshot is retained under
`results/bts_round6_revision_20261031/reviewed_snapshot`; the original round-5
asset hash table is preserved as `round5_final_assets_sha256` in
`revision_selection.json`.

The post-processing audit reconstructs the count rows, discrepancy, two matched
zero-slope starts and the paired-bootstrap headline, **4.48037334
[4.32593473, 4.62891107]**, from frozen outputs. All 76 claim pointers and selected
current asset hashes verify. The 46 relevant BTS tests pass. Article and
supplement build without layout/reference warnings in new directories; the
installed PDFs contain 20 and 10 pages, respectively. Changed table/text pages
were inspected. The humanizer skill was used for manuscript prose, with
scientific notation and supported numerical claims preserved.

R5-BTS-09 remains deferred to the submission-ready stage, outside the active
scientific checklist. No journal choice, access decision, final author approval,
external delivery or journal acceptance is recorded by this response.
