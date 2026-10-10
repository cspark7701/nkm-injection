# Task 004 — Establish fair controls and a coupled injection operating region

Status: completed 2026-10-09 (milestone 108). Created: 2026-10-09.
Dependencies: 002, 003.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Implement `scripts/run_injection_operating_region.py` with S6 options. Transport the same booster distribution through baseline and selected optimized BTS optics, then apply an explicit frame/offset transformation into the storage-ring injection point. Save before/after phase-space data and actual handoff configuration. Do not assume the current independent injection script consumes BTS optimization.

Explain the current off=100%, ideal=100%, linear=0%, fieldmap=99.776% comparison. Check whether the initial beam is already inside modeled acceptance, whether the first-turn aperture admits artificial survival, and whether the hard-coded linear/ideal controls have comparable reference strengths. Calibrate ideal and linear models against the same reference kick/expansion point while retaining clearly labeled historical controls if useful.

Apply paired beam realizations, timing, aperture/septum definitions and observation points to every model. Map initial x/xp acceptance at nominal field scale, then refine field scale at boundaries using S6. Include stored-beam excitation and losses alongside injected capture. Use explicit field-domain rejection and keep all failed cases. No initial-condition adjustment may be applied to one control solely to improve the comparison.

## Deliverables and acceptance

A reproducible operating-region dataset with paired controls, baseline/optimized optics and coupled handoff; an explanation or corrected interpretation of the original control results; a physical operating region supporting the central claim without selecting only favorable cases.

## Files and evidence

Proposed operating-region script, handoff configuration/functions and tests; `paper.tex` injection methods/results/discussion.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
