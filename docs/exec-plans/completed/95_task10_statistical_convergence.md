# Milestone 95 — Task 10: Statistical summaries and convergence evidence

Completed: 2026-10-07  
Task: [Separate statistical summaries from defensible convergence checks](../../05_refactor_tasks/10_statistical_convergence_contract.md)

## Problem and outcome

The robustness convergence diagnostic compared identical shortened prefixes for
10–49 samples, reporting zero difference and convergence without distinct
required sample sizes. Bootstrap settings and tolerance were hardcoded.
Task 04 had already excluded invalid evaluation penalties from summaries; this
refactor preserves that separation and makes the evidence policy explicit.

Reusable helpers now separate descriptive summaries, bootstrap intervals and
ordered-prefix stability. Insufficient or invalid data never yield a stability
claim; settings, estimands, denominators and counts are recorded.

## Implementation

- Added `StatisticalPolicy` with validated bootstrap count/seed/confidence level,
  distinct increasing prefix sizes, dimensionless tolerance and explicit invalid
  policy. Defaults retain 1000/42/0.95 bootstrap settings and 50/100 prefixes with
  strict absolute median difference below 0.05.
- Extracted descriptive summaries and outcome aggregation. Numerical summaries
  include valid and physically infeasible computations, exclude invalid metrics,
  and report requested/valid/invalid/feasible/physical-failure counts. Existing
  failure probability and feasible-fraction denominators are saved explicitly.
- Added structured empty-ensemble summaries with null metrics/fractions when
  their denominators are unavailable, replacing the previous empty dictionary.
- Added explicit insufficient/blocked/within/outside evidence statuses. Missing
  prefix estimates and differences are null. The legacy 50-to-100 alias remains
  only for those actual sizes. Additional samples still enter full summaries.
- Shared percentile-bootstrap resampling with explicit median vs mean estimands.
  Robustness estimates median horizontal mismatch; capture estimates mean
  efficiency across seed runs. Capture counts are validated and bootstrap seed,
  count, level, denominator, resampling unit and evidence status are saved.
  External generators save their initial state for replay; singletons are
  descriptive only and empty capture inputs have null estimates.
- Exposed capture bootstrap options through `run_ensemble_study` and allowed
  nested settings in its result annotation. Existing default draw order remains
  sequential for reproducibility.
- Added tolerance CLI policy options and saved all settings in sampling/policy
  metadata and statistics. Console output reports nullable evidence rather than
  synthetic zeros. Generic CI aliases avoid falsely labeling non-95% intervals.
- Under the explicit raise policy, rejected statistics carry diagnostics; the
  CLI saves them and stops without rerunning physics or OAT. Existing invalid
  ensemble publication rejection remains intact.
- Documented interpretation/migration in
  [statistical summaries and prefix stability](../../020_STATISTICAL_CONVERGENCE.md),
  linked from README and updated evaluation/tolerance guidance. Updated the
  ignored backlog and manifest.

## Verification

- Affected workflow tests: **118 passed** in 20.75 s.
- Initial focused statistical cases: **36 passed** in 0.85 s; two additional CLI
  persistence/rejection cases are included in final verification.
- Final full suite: **558 passed** in 58.97 s in the existing pyat-dev Python 3.11
  environment with `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`.
- New cases cover 0/9/10/49/50/99/100/150 samples, distinct custom prefixes,
  threshold equality, known synthetic distributions, deterministic draws,
  invalid/physical outcomes, missing statistics, singleton/empty capture,
  integer survivor counts, external generator replay and saved CLI settings.
- Repeated bootstrap records require exact equality. Independent synthetic
  interval/mean comparisons use absolute tolerance 1e-14 and zero relative
  tolerance. Existing physics and optimizer tolerances are unchanged.
- A fresh-process tolerance CLI run used explicit reference/off-kicker mode,
  three Monte Carlo samples (seed 7), two OAT samples per category (seed 9), two
  workers, 17 bootstrap draws (seed 11), confidence level 0.8, prefixes 2/4 and
  tolerance 0.02. It saved all settings and reported insufficient evidence.
  All three computations were valid and all three were physically infeasible;
  invalid count was zero. Outputs are isolated beneath
  `/tmp/nkm-task10-uihj4ud0/tolerances/`, including complete configurations,
  units, sampling provenance and source selection from the existing handoff.
- SHA-256 checks confirm all nine protected source/data files match HEAD.
  Final git status/diff, whitespace and documentation links were checked. No
  protected input, notebook, full production study, remote interaction or push
  was involved.

## Compatibility and interpretation

Consumers must handle nullable evidence flags/differences and structured empty
summaries. The generic median CI key supports custom levels; the 95% alias exists
only at 0.95. Capture JSON gains nested settings; historical well-typed JSON is
still loadable and existing default seeds/counts remain unchanged. No historical
artifacts are rewritten or retrospectively certified.

Within-tolerance means stability of the configured ordered median prefixes. It
is not proof of tail, particle, turn or slice convergence and is not an
independent-sample significance test. Bootstrap mechanics are shared only with
an explicit matching estimand; capture and mismatch retain different estimators,
resampling interpretations and standard-deviation conventions.
