# Statistical summaries and prefix stability

Robustness statistics and convergence evidence are separate operations in
`nkm_injection.statistics`. `StatisticalPolicy` configures the summary/bootstrap
and ordered-prefix diagnostic passed to `evaluate_robustness_statistics`.
Mismatch/efficiency are dimensionless, beta remains in m, and stored kicks remain
in mrad at their existing interfaces. No physics algorithms or thresholds change.

```python
from nkm_injection.statistics import StatisticalPolicy

policy = StatisticalPolicy(
    bootstrap_count=1000,
    bootstrap_seed=42,
    ci_level=0.95,
    convergence_sizes=(50, 100),
    convergence_tolerance=0.05,
    invalid_sample_policy='exclude',
)
policy.validate()
# evaluate_robustness_statistics(..., statistical_policy=policy)
```

## Descriptive summaries and excluded computations

Valid and physically infeasible evaluations enter numerical summaries; invalid
computations never contribute penalty values to percentiles or bootstrap draws.
Results report requested, valid, invalid, physically feasible and physical-failure
counts. Physical failure probability divides by valid evaluations; feasible
fraction divides by requested evaluations. Overlapping physical failure reasons
are retained. These denominator definitions and the invalid-sample policy are
saved in `statistical_settings`.

`exclude` retains conditional summaries and invalid diagnostics; invalid samples
still block prefix-stability claims. `raise` raises
`InvalidStatisticalSamplesError`, whose `summary` contains rejected-ensemble
diagnostics. The tolerance CLI archives these diagnostics without rerunning
physics and exits unsuccessfully under either policy whenever computations are
invalid. Publication validation still rejects invalid ensembles.

An empty requested ensemble returns structured null statistics and insufficient
evidence, rather than an empty dictionary. With zero valid evaluations, failure
probability and physics summaries are null. With zero requested evaluations,
feasible and invalid fractions are also null. Summary population standard
deviation uses `ddof=0`; percentile interpolation uses the linear method.

## Exact-size prefix checks

Default stability compares the median horizontal mismatch of the first 50 ordered
samples with the first 100. Both distinct required prefixes must exist; counts
0, 9, 10, 49, 50 and 99 yield `insufficient_evidence`. Samples beyond the larger
required size enter full descriptive summaries but do not change this configured
prefix comparison. Choose larger sizes explicitly when needed.

`convergence_check` saves sizes, available valid count, invalid count, estimand,
method, strict comparison rule and dimensionless tolerance. Its statuses are:

| Status | Meaning | `converged` |
| --- | --- | --- |
| `insufficient_evidence` | At least one required prefix is unavailable | `null` |
| `blocked_invalid_evaluations` | A requested computation was invalid | `null` |
| `within_tolerance` | Absolute median difference is strictly below tolerance | `true` |
| `outside_tolerance` | Difference meets or exceeds tolerance | `false` |

Unavailable differences/estimates are null, never a synthetic zero. The legacy
`N_50_to_100_diff` alias is present only for the default sizes, with null when
unavailable. Custom sizes use `absolute_difference` and `sample_sizes`.

This diagnostic checks one ordered, overlapping pair of median prefixes. A
`within_tolerance` result is evidence of that specific stability criterion; it
is not proof that tail probabilities, particle/turn/slice convergence or the
physical model have converged. It is not an independent-sample significance test.

## Bootstrap estimands and reproducibility

The shared percentile-bootstrap helper accepts an explicit `mean` or `median`
estimator and saves count, seed, confidence level, method, interpolation method,
resampling unit and generator type. Finite one-dimensional observations are
required. Empty inputs have null estimates/intervals; a singleton has a collapsed
interval with `descriptive_only` status, which does not establish uncertainty
across independent observations.

Robustness bootstraps the **median horizontal mismatch** across valid error
realizations. Default seed/count/level remain 42/1000/0.95. Generic interval
endpoints are `bootstrap_ci_median`; `bootstrap_95ci_median` remains available
only when the selected confidence level is actually 0.95.

`bootstrap_capture_ci` bootstraps **mean capture efficiency across seed runs**,
not pooled particles and not the median. Survivors must be integer counts between
zero and the positive particle denominator. Defaults remain seed 0, 5000 draws
and level 0.95; standard deviation across runs uses `ddof=1`. It saves these
settings, denominator and evidence status. A supplied NumPy Generator records
its initial state and a null seed, permitting replay without inventing a seed.
`run_ensemble_study` exposes `n_bootstrap`, `bootstrap_seed` and `ci_level` as
keyword options and saves them in its capture result. Single-run legacy standard
deviation remains zero but the evidence status is descriptive only.

## CLI and migration

```bash
python scripts/run_publication_tolerances.py --reference \
  --samples 100 --seed 42 --bootstrap-count 1000 --bootstrap-seed 42 \
  --ci-level 0.95 --convergence-sizes 50 100 --convergence-tolerance 0.05 \
  --invalid-sample-policy exclude
```

All selected policy fields are saved in the summary's `statistical_policy`,
bootstrap sampling metadata and robustness `statistical_settings`. The console
reports prefix status, selected sizes and nullable difference instead of printing
false zero differences. Invalid ensembles retain this metadata in diagnostics.

Consumers must handle nullable `converged`/differences and use status before
interpreting a convergence claim. Consumers selecting a non-95% confidence level
must use the generic interval key. Capture result annotations now permit nested
settings; existing well-typed JSON remains loadable. Legacy history is not
rewritten or retrospectively declared converged.

Determinism tests replay the same generator and synthetic bootstrap draws;
exact structured equality is required for repeated settings. Independent
synthetic percentile/mean comparisons use absolute tolerance `1e-14` and zero
relative tolerance. Existing physics tolerances and sampling seeds remain intact.
