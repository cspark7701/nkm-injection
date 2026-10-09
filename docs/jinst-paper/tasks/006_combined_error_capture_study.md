# Task 006 — Implement and run combined-error capture robustness

Status: planned. Created: 2026-10-09.
Dependencies: 003, 004; audited error coverage from 002.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Implement `scripts/run_capture_robustness.py` with S7 options. For each error realization, perturb the relevant transfer optics, beam distribution, ring/field/alignment/timing settings, transport the beam and perform actual validated multi-turn particle tracking. The current tolerance script has no capture distribution; it cannot be renamed to satisfy this task.

Begin with 100 realizations, 2,000 particles and 1,000 turns using paired controls. Benchmark runtime, then progress to 500 realizations, 5,000 particles, 1,000 turns for seeds 42/123/777 and representative operating points. Save latent errors and common beam realizations so controls are paired. Reuse a genuinely fixed ring only when physical errors allow it; ring edits must not reuse a stale one-turn map.

Measure per-realization capture, stored centroid/emittance excitation, transmission through BTS/septum, loss location and turn. Distinguish particle statistics, independent error realizations and seed replicates. Add hierarchical uncertainty and paired differences. Classify actual physical loss separately from invalid computation; archive diagnostic failures instead of favorable-only reruns. Record which specified errors are modeled and which remain out of scope.

## Deliverables and acceptance

Validated coupled capture ensembles with hierarchical uncertainty, paired model comparison, reproducible error configurations and an operating tolerance region. Small zero-error recovery and deliberately excessive-error/loss cases pass. Main capture-robustness claims are derived from these artifacts, not optics-only failure counts.

## Files and evidence

New capture driver, shared error/beam/transport/tracking helpers and tests; `paper.tex` results/discussion and error budget figures.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
