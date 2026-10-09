# Task 011 — Review the article as a referee before freezing it

Status: planned. Created: 2026-10-09.
Dependencies: 008, 009, 010; all included simulation tasks complete.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Review independently against the evidence matrix: what is new, are controls fair, does the validated model support the claim, is the chosen geometry consistent, are limits meaningful, are sampling precision and failure bounds adequate, and are conclusions narrower than the data? Record major/minor issues and their disposition in a review checklist. Do not treat unit-test success as referee approval.

Require explanation of the original off/ideal/linear/fieldmap outcomes and any remaining model discrepancy. Recompute a selection of table values directly from raw outputs. Inspect confidence intervals, excluded/invalid data, ineffective errors, unsuccessful seeds and uncertainty hierarchy. Ensure novel physics statements have external or independent numerical support as appropriate.

Run `./scripts/check_github_actions.sh --fast` and the full checker with the project interpreter for software validation; they use synthetic fixtures and do not establish paper results. Validate the final explicit campaign manifest separately using the strategy commands. Build from a fresh directory and inspect the actual PDF for stale/missing figures, citations and broken symbols.

## Deliverables and acceptance

A resolved review record, reproducible claim/figure audit, successful local software checks and a scientifically consistent reviewed PDF. Any unresolved issue affecting the principal claim blocks the ready-for-submission designation.

## Files and evidence

Proposed `scientific_review.md`, claim/figure audit records, explicit campaign artifacts and fresh PDF build.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
