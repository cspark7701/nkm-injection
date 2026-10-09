# Task 005 — Replicate fixed-optics tolerances and report defensible uncertainty

Status: planned. Created: 2026-10-09.
Dependencies: 002; repeat after 003-004 if the physical model changes.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Execute S4 with 50,000 samples, 5,000 OAT samples/category, seeds 42/123/777, 20,000 bootstrap replicates, bootstrap seed 1729, confidence 0.95, prefixes 25,000/50,000 and tolerance 1e-5. Keep the feasible optimization/configuration hashes and full error budget fixed. Preserve the original 20,000-sample run. These commands are supported today but do not validate combined-error capture.

Implement postprocessing of saved per-sample results for independent-seed comparisons, p50/p95/p99 intervals, median uncertainty and exact/Wilson binomial failure intervals. Specify estimands and valid/invalid denominators. Retain failures and invalid diagnostics. Add a saved-observation bootstrap CLI rather than repeating physics just to change bootstrap seed; compare endpoints with seeds 1729/2718/31415.

Report absolute and relative prefix changes, interval widths and seed variation. Decide the scientifically needed precision before adapting the sample budget; do not run until a stochastic prefix happens to pass. The existing interval half-width is about 6.53e-5, so 50,000 samples cannot be assumed to yield 1e-5 median uncertainty. Bootstrap count controls resampling noise, not independent physical information. Separate per-category OAT ranking stability from joint-error interactions.

## Deliverables and acceptance

Three frozen-config tolerance runs plus a machine-readable replicate comparison and uncertainty table. The publication states the precision actually established and any unmet target. Zero observed failures have an upper confidence bound; no unsupported statement of zero probability or capture robustness remains.

## Files and evidence

Existing tolerance script/statistics helpers; proposed postprocessing CLI and uncertainty tests; new result directories; `paper.tex` robustness subsection.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
