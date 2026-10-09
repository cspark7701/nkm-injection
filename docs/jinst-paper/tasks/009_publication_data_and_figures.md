# Task 009 — Connect the article to selected evidence and journal-quality figures

Status: planned. Created: 2026-10-09.
Dependencies: 002-007 for included claims; 008 outline.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Select explicit source runs and preserve their manifests/hashes. Register new backend/operating/capture/replicate artifacts in a validated campaign evidence schema; do not insert incompatible JSON into old publication slots. Produce the campaign publication manifest used by the final strategy commands. The current schema has one tolerance slot: select a principal run and separately register replicate comparisons.

Create a concise main-text figure plan: physical injection geometry/frames; kick profile at actual offsets; model-validation residuals; capture/stored-disturbance operating region with paired controls; uncertainty/tolerance envelope; design comparison only if it answers the question. Use SI units consistently, vector plots where practical, readable axes and error bars. Captions state beams, particles, turns, seeds, backend, error settings, apertures and uncertainty meaning.

Replace historical hard-coded numerical tables with selected-data imports/macros or a reproducible generator. Maintain `figure_provenance.csv` containing manuscript label, generated filename, study/config/input hashes and data columns. Audit every includegraphics/input path: successful PDF building can copy old figures and is not proof that new data were used. Preserve raw arrays and loss diagnostics as supporting data.

## Deliverables and acceptance

Every numerical claim and figure in the submission draft traces to an explicit validated artifact. New study schemas are covered by focused tests. Rebuilding selected data yields the same tables/figures within declared numerical tolerances; no stale asset silently substitutes for current evidence.

## Files and evidence

`paper.tex`, `figures/`, publication schema/generators if needed; `claim_evidence.csv`, `figure_provenance.csv`, campaign manifest and supplementary tables.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
