# Fixed-optics tolerance replication and uncertainty (Task 005, campaign S4)

Runs (git-ignored): `results/journal_campaign_01/tolerances_seed{42,123,777}/` with the frozen selected
optimisation (summary/config SHA-256 in `source_optimization_hashes.txt`) and frozen error budget
(`error_budget.json`); 50,000 Monte Carlo samples and 5,000 one-at-a-time (OAT) samples per category per
seed; field-map stored-kick model; bootstrap 20,000 replicates, seed 1729, 95 %; prefix sizes 25,000/50,000,
target 1e−5; invalid-sample policy `raise`. Post-processing of the saved per-sample observations (no
physics re-run): `scripts/analyze_tolerance_replicates.py` →
`results/journal_campaign_01/tolerance_replicates/tolerance_replicate_analysis.json`.
Observables are BTS-exit optics only (physics_model.md §7); capture is studied in Task 006.

## Results

| Quantity | seed 42 | seed 123 | seed 777 | pooled (150,000) |
| :--- | :--- | :--- | :--- | :--- |
| median M_x [×10⁻³] (order-statistic 95 % CI) | 2.103 [2.064, 2.144] | 2.079 [2.042, 2.123] | 2.103 [2.060, 2.139] | 2.095 [2.070, 2.119] |
| p95 / p99 M_x [×10⁻³] | 16.4 / 28.6 | 16.7 / 29.5 | 16.3 / 28.6 | 16.4 / 28.9 |
| median M_y [×10⁻³] | 2.497 | 2.513 | 2.507 | 2.506 [2.475, 2.535] |
| p99 β_x,max / β_y,max [m] | 37.45 / 55.22 | 37.64 / 55.28 | 37.54 / 55.27 | — |
| median / p99 stored kick [µrad] | 1.31 / 14.4 | 1.34 / 14.7 | 1.33 / 14.6 | — |
| physical failures | 0 / 50,000 | 1 / 50,000 | 0 / 50,000 | 1 / 150,000 |

* The single failure (seed 123, sample 4158) has β_y,max = 60.23 m against the 60 m limit (+0.01 m
  tolerance); M_x+M_y = 0.113. Failure probability 6.7×10⁻⁶ with exact 95 % interval
  [1.7×10⁻⁷, 3.7×10⁻⁵] (Wilson [1.2×10⁻⁶, 3.8×10⁻⁵]).
* Bootstrap endpoints of the median M_x for bootstrap seeds 1729/2718/31415 agree to < 10⁻⁶ (resampling
  noise is negligible); bootstrap and order-statistic intervals agree.
* Prefix stability (25k → 50k): absolute changes 2.08/1.14/1.06×10⁻⁵ (relative 0.99/0.55/0.50 %); the
  predeclared 1×10⁻⁵ target is **not met** in any run. The independent-seed standard deviation of the
  median is 1.35×10⁻⁵ and the CI half-width ≈ 4×10⁻⁵ per run, so a 1×10⁻⁵ precision would require
  roughly 10⁶ samples. The established precision is ±2.4×10⁻⁵ (pooled 95 % half-width), i.e. ≈ 1.2 % of the median.
* OAT ranking is identical across seeds: booster β mismatch 5 % (ΔMerit 0.0086–0.0089), quadrupole gradient
  0.1 % (8.2–8.6×10⁻⁴), energy 0.1 % (1.06×10⁻⁴), quadrupole roll (3.6–4.0×10⁻⁹); the remaining seven
  categories are zero by construction because those errors do not act on the optics observables.

## Statement for the article

The matched BTS optics are robust in the implemented optics error model: the median exit mismatch is
M_x ≈ 2.1×10⁻³ (±1.2 %) and one realization in 1.5×10⁵ exceeds the 60 m β limit. These ensembles do not
include injection capture; capture robustness is quantified separately (Task 006).
