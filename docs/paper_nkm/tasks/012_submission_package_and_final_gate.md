# Task 012 — Assemble a complete regular-article submission package

Status: completed 2026-10-09 (milestone 115; author confirmation pending). Created: 2026-10-09.
Dependencies: 011; author final scientific review.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Prepare one clean source package containing `paper.tex`, verified `paper.bib`, required style files and only referenced final figures/tables; include any journal-required compiled bibliography. Prepare the final PDF, supplement, cover letter, selected metadata/keywords and availability information. Build in an isolated directory using the current journal template, with no missing/undefined references or bibliography errors.

Create a final checklist linking each headline finding to its artifact/configuration and the resolved review record. Preserve a versioned evidence manifest, source/result hashes, software environment and reproducible commands. Confirm that all reported simulations actually ran, planned studies are not described as completed, and statistical/model limitations appear in the article.

Use the current JINST author instructions if JINST remains selected. A scientific research article designation requires the contribution established in Task 001 and supported by subsequent evidence; format alone cannot achieve it. Record author confirmation of final title, authorship, journal/category and claims. This task prepares a reviewable submission package; actual submission is a subsequent author action.

## Deliverables and acceptance

A locally reproducible, reviewed submission source archive and PDF with supplement/cover letter/metadata, no unverified principal claims and a completed final checklist. No remote submission, push or source-input regeneration is required by this task.

## Files and evidence

Final manuscript/bibliography/figures, supplement, `cover_letter.md`, proposed `submission_checklist.md`, isolated build and submission archive.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
