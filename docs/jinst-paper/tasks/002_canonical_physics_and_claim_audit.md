# Task 002 — Freeze the canonical physical model and audit existing claims

Status: completed 2026-10-09 (milestone 105). Created: 2026-10-09.
Dependencies: 001.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Audit `paper.tex` against the selected run configuration and all consumed artifacts. Create `claim_evidence.csv` with claim, manuscript location, artifact/JSON key, source hash, actual value/units, model and correction decision. Include every abstract and conclusion number.

Resolve grid +/-50 mm versus manuscript +/-25 mm, spacing, source kick at -16 mm versus its peak near -8.5 mm, production offset -20 mm, NKM length 0.31 versus 0.525 m, BTS length/element list, emittances, entrance/target optics and coordinate frames. Evaluate kick signs using the AT coordinate convention and energy normalization. Different physical scenarios need separate labels; never combine notebook exploratory geometry and canonical production results as one machine.

Document the actual M66 plus thin-kicker approximation, RF/radiation choices, off-momentum treatment, kicker timing and aperture/septum/observation definitions. Trace every ErrorBudgetConfig field through sampling and application: list effective, ignored and unsupported errors for optics, kick and capture, plus gaps in the 11-category OAT ranking. Resolve mismatch/dispersion objective normalization and dimensional consistency.

Freeze a complete injection study configuration and error budget before implementing the new drivers. State which tolerances have design/measurement justification and which are assumptions. Resolve any inconsistency by changing the derived model or claim, never protected scientific inputs.

## Deliverables and acceptance

`claim_evidence.csv`, `physics_model.md`, a versioned complete study-config schema/example and an effective-error coverage table. No disputed number remains unqualified in the proposed article outline; all geometry/units/signs and loss/observation conventions are explicit.

## Files and evidence

`paper.tex`; selected production artifacts; `src/nkm_injection/` configuration, field/kick and tracking interfaces; proposed model/configuration documents.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
