# Task 008 — Rewrite the manuscript around a scientific argument

Status: completed 2026-10-09 (milestone 111). Created: 2026-10-09.
Dependencies: 001, 002; scientific results from 003-007 before finalizing claims.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Replace the framework inventory with: (1) introduction and unresolved question, (2) physical system/assumptions, (3) models and validation, (4) comparative design/operating results, (5) uncertainty/robustness, (6) discussion and limitations, (7) conclusions. Merge repetitive lattice/optimizer explanations and move long parameter tables, implementation details, command lists and SHA/test descriptions to supplementary material.

Use a focused provisional title such as "Robustness of nonlinear-kicker injection with realistic field maps and matched transfer optics", revising it to match the demonstrated scope. Write the abstract last: problem, method scope, one or two physically meaningful quantified findings with uncertainty, and bounded implication. Remove unsupported "zero perturbation", "proves", "transparent under all errors" and "rigorous 6D symplectic" language.

Explain why reduced-model and element tracking agree or disagree, what each control establishes and how results compare with previous designs. Discuss measurement/calculation uncertainty and omitted effects. A simulation-only article may be appropriate, but do not describe it as experimental or operational validation. Align conclusions with the evidence matrix, including unmet numerical targets.

## Deliverables and acceptance

A coherent research-article draft with one principal question, explicit novelty, methods accurate to the implementation, defensible results and limitations. Abstract/conclusion claims map to validated artifacts. Technical-report-style module and tool inventories no longer dominate the paper.

## Files and evidence

`docs/jinst-paper/paper.tex`; proposed supplement and outline documents.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
