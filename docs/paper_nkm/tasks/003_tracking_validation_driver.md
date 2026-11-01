# Task 003 — Implement independent tracking and numerical validation drivers

Status: completed 2026-10-09 (milestone 106). Created: 2026-10-09.
Dependencies: 002.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Implement `scripts/run_tracking_backend_validation.py` with the exact S5 CLI contract in the strategy. Reuse `track_multiturn_injection` and `track_element_resolved_injection`; characterize how their initial frames, NKM locations, aperture/septum losses and observations differ before comparison. Do not describe native AT as experimental ground truth. Expose complete configuration, paired seeds, particle/turn counts and fresh outputs.

Use small zero-kick, linear-lattice and zero-error limits first. Compare matched tracking configurations at 1,000/10,000/50,000 particles and 100/1,000/5,000 turns for selected cases. Distinguish one-turn linearization error, element apertures, nonlinear ring effects, momentum dependence and NKM integration approximations. Implement thin/thick/RK4 comparisons with explicit source units and interpolation bounds where supported. An isolated By.txt slice scan is not proof of full storage-ring symplectic tracking.

Save coordinate residuals, capture differences with sampling uncertainty, stored centroid/emittance differences, first-loss particle identities/elements/turns and numerical tolerances. Predeclare the allowable numerical contribution to each scientific performance claim. Benchmark runtime before large grids. Extend the existing field cross-validation CLI to accept source/output and controlled sampling settings if used; currently it has none.

## Deliverables and acceptance

The S5 command parses and runs from a fresh process; tests cover limiting cases, shapes, losses, source preservation and matched comparisons. `backend_validation_summary.json` quantifies relevant discrepancies and states the supported model scope. The main article's tracking claim agrees with demonstrated accuracy.

## Files and evidence

Proposed validation script, reusable package helpers and tests; `paper.tex` methods and validation figures.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
