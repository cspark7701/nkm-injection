# Task 001 — Define the scientific question, novelty and journal fit

Status: completed 2026-10-09 (milestone 104). Created: 2026-10-09.
Dependencies: None.
Strategy: [additional simulations and journal strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md).

## Work

Select one principal question about the capture/stored-disturbance operating region and its sensitivity after transfer-line matching. Produce a claim and evidence matrix with the closest experimental and simulation literature; software organization, SHA-256 checks and use of NSGA-II are supporting methods, not sufficient novelty. Decide whether Pareto optimization supports this question or belongs in a supplement.

Use JINST regular research papers as the provisional route, subject to the demonstrated contribution. Its scope includes accelerator simulations and its editorial policy distinguishes scientific research from technical achievements. Review [JINST scope](https://jinst.sissa.it/jinst/help/JINST/JINST_about.jsp). Record the selected journal, article category, comparison literature, author metadata and final scope. Do not promise first demonstration, operational readiness or experimental validation without evidence.

For JINST, check its [author instructions](https://jinst.sissa.it/jinst/help/helpLoader.jsp?pgType=author): use its template, select official keywords, keep the abstract concise, provide numbered references and a data/software availability statement, and declare applicable AI-assisted manuscript preparation. Recheck these requirements at submission. Verify the author's full name, institutional affiliation (including the Center for Accelerator Research), corresponding email and funding from authoritative records.

## Deliverables and acceptance

`docs/jinst-paper/article_scope.md`: principal question, bounded candidate claims, literature comparison and journal requirements with access date. A clear scientific finding beyond a software workflow is identified, or the article scope is narrowed before further large runs.

## Files and evidence

`docs/jinst-paper/paper.tex` front matter/introduction; `paper.bib`; proposed `article_scope.md`.

## Execution safeguards

Keep protected source inputs unchanged and write simulation/build outputs to new
result directories. Record sources, assumptions, SI units, seeds, numerical
checks and tolerances. Mark this task complete only after its acceptance criteria
are met, and archive its actual execution under the next sequential milestone in
`docs/exec-plans/completed/`. This task list does not mark planned science as completed.
