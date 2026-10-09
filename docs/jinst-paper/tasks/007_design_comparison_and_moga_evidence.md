# Task 007 — Decide and validate the role of Pareto optimization

Status: planned. Created: 2026-10-09.
Dependencies: 001, 002, 004; 006 for robustness-ranked finalists.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Keep MOGA in the main article only if it answers a distinct physical design question. Compare nominal optics, deterministic feasible matching and preselected Pareto representatives with identical beams, apertures and uncertainty settings. Explain why a representative is preferred in operating terms rather than only geometric knee distance.

If retained, extend `run_publication_moga.py` with explicit population, generations, seed list, finalist particle/turn counts and validated backend/handoff options. It currently fixes 40/20/five seeds in production. Define/parser-test the new contract before writing runnable commands. Compare 100/100 and 200/200 budgets across at least five seeds with a common hypervolume reference/normalization and termination criteria. Record bounds, feasibility, evaluation counts, all seed outcomes and runtime.

Verify what finalist evaluation actually computes; a configured MC-seed count is not proof of capture tracking. Resolve dispersion objective units and compare finalists using Tasks 004/006 physical outputs. Move optimizer implementation details and extra fronts to supplementary material if they distract from the principal result.

## Deliverables and acceptance

A repeatable physical design comparison and justified selection rule, or an explicit decision to omit main-text MOGA claims. Objective units, feasibility and uncertainty are auditable; success flags alone are not evidence of superior injection.

## Files and evidence

Publication MOGA CLI/configuration if retained; selected-run artifacts and tables; `paper.tex` optimization/results; supplement.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
