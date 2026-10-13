# Historical statistical reconstruction — R1-BTS-09

Fresh audit: `results/bts_journal_campaign_r1_20261013/statistics/`; [selected summary](generated/historical_statistics.json). Reproduce `python scripts/audit_bts_statistics.py --output-dir results/<new>/statistics`. Digests and all550,000 sample records are checked, not only the archived aggregates.

Pooling compatibility is exact across model/strengths, entrance/target optics, constraints, error configuration, units and failure thresholds. The operative rule is beta_x or beta_y >60.01 m OR Mx+My >2.05. Reconstructed failures:5; invalid evaluations:0. All five exceed vertical beta only. The full failure register and actual values are in the selected summary. No physical particle losses are inferred from these optics-only exceedances.

Exact95% failure limits: [2.95179981385505e-06, 2.1215020626606803e-05]; Wilson: [3.883099029961521e-06, 2.1283013962961002e-05]. Asymmetric limits are retained. Pooled median and95th/99th quantile intervals reconstructed by order statistics match the archived analysis to1e-12 relative tolerance; they are not pooled-bootstrap intervals. The generating per-run median bootstrap settings (20000 resamples,seed1729) remain distinct from the pooled order-statistic analysis.

| Seed | Samples | Optical failures | Ordered median-prefix change | 1e-5 target |
| :--- | ---: | ---: | ---: | :--- |
| 42 | 50000 | 0 | 2.082976e-05 | not met |
| 123 | 50000 | 1 | 1.143611e-05 | not met |
| 777 | 50000 | 0 | 1.056744e-05 | not met |
| 2026 | 400000 | 4 | 2.39484e-06 | met |

Three50k runs miss the median-prefix target; the400k follow-up passes. Neither median stability nor increased N establishes tail convergence or a realistic hardware-error model. The archival follow-up stopping policy is not documented as predeclared; fixed-N intervals are descriptive and no sequential/optional-stopping coverage is promised.

OAT ranks beta-only entrance perturbations (.0089037402), quadrupole gradients (.0008611217), and energy (.0001063357) under the seed42 amplitudes. Its estimator is mean absolute change of Mx+My, distinct from normalized least-squares J. Alpha is fixed. Independent Gaussian sampling and the archived five-category configuration do not mean every error affects this mismatch estimator; the new model's active-error table and particle transport are separate.

No engineering tolerance specification is retained, so no amplitude scan is presented as a hardware prescription. The new frozen-design study uses200 machine clusters to report a paired clearance interval, rather than targeting a1e-5 rare-failure rate. Its interval crossing zero means no resolved benefit at that precision. Further sampling could narrow that conditional interval but cannot supply missing chamber/target provenance. New-model and historical observations are never pooled.
