# Task 010 — Verify references and prepare scholarly metadata

Status: completed 2026-10-09 (milestone 113). Created: 2026-10-09.
Dependencies: 001, 008; 009 for data/software citations.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Audit every entry in `paper.bib` against original publisher/JACoW records: title, authors, publication, year, pages and DOI. Existing entries are candidates, not verified authority. Check that cited statements are actually supported; add directly relevant nonlinear-kicker implementations, accelerator tracking/optimization methodology and the closest comparable designs. Explain the distinction from previous work rather than expanding a generic introduction.

Apply the selected journal's citation style and official keyword list, using current author instructions cited in Task 001. Correct author affiliation/email/funding; document author contributions and acknowledgments accurately. Add data/software availability identifying immutable inputs, derived results and a permanent repository/DOI only when it actually exists. Do not invent measurements, approvals, collaborator contributions, public archives or DOI records.

Prepare a short cover-letter draft stating the scientific question, principal supported findings, closest prior work and relevance to the journal. Describe the final actual manuscript rather than this planning history. Check journal-specific disclosure/availability requirements with the author before finalizing the submission package.

## Deliverables and acceptance

Verified bibliography and in-text citations, consistent authorship/metadata, honest availability/disclosure statements and a publication-focused cover-letter draft. All DOI and archive links are verified; no fabricated citations or uncreated deposits are presented as existing.

## Files and evidence

`paper.bib`, `paper.tex` metadata/acknowledgments/availability, proposed `cover_letter.md` and bibliography audit.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
