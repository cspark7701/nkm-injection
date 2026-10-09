# Milestone 107 — Journal Task 005: tolerance replication and uncertainty (S4)

Completed: 2026-10-09. Task: [005](../../jinst-paper/tasks/005_tolerance_replication_and_uncertainty.md).

Ran S4 exactly as specified in strategy 023 (three seeds 42/123/777, 50,000 MC + 5,000 OAT per category, bootstrap
20,000 at seed 1729, prefixes 25k/50k, tolerance 1e−5, invalid policy raise; ~23 min per seed with 4 workers) against
the frozen selected optimisation and error budget. Added `scripts/analyze_tolerance_replicates.py` (order-statistic
quantile CIs, multi-seed bootstrap endpoints, exact/Wilson failure intervals, prefix and seed comparison, OAT
agreement) and `tests/test_tolerance_replicates.py`. Results: [`tolerance_uncertainty.md`](../../jinst-paper/tolerance_uncertainty.md).

Findings: pooled median M_x 2.095×10⁻³ [2.070, 2.119]×10⁻³; 1 physical failure in 150,000 (β_y,max 60.23 m),
95 % exact interval [1.7×10⁻⁷, 3.7×10⁻⁵]; the 1e−5 prefix target is not met (1.06–2.08×10⁻⁵, seed spread 1.35×10⁻⁵)
and is reported as unmet rather than loosened; OAT ranking identical across seeds. Capture is not part of S4.
No invalid evaluations; protected inputs unchanged; outputs only under results/.
