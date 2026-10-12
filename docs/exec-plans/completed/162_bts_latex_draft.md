# Milestone 162 — Create the first BTS LaTeX manuscript draft

Completed 2026-10-13 at the author's request. Created `docs/paper_bts/paper.tex` and an independently compiled eight-page `paper.pdf`, using a generic one-column article format for drafting toward JKPS.

## Content

The draft includes an abstract, introduction, transfer-line model and boundary conditions, matching and uncertainty methods, archived matched settings, tolerance distributions, sensitivity interpretation, discussion, conclusions, declarations and an evidence appendix. Four tables cover boundary optics, quadrupole strengths, pooled quantiles and independent-seed prefix checks. A separate six-entry bibliography draws from the existing audited references.

Exported numerical macros and tables from the selected archived optimization/config and pooled 550,000-sample tolerance analysis into `generated/archived_results.tex`. Verified the two selected optimization hashes and all four raw tolerance-summary hashes recorded by the analysis. `draft_provenance.json` records nine scientific source hashes, the publication export hash, draft asset hashes and compilation metadata.

Described the current bounded least-squares/SLSQP implementation accurately: nonlinear physical criteria are checked independently for feasibility-first selection, rather than supplied as SLSQP constraint functions. Reported finite-precision matching, one feasible start of three, five optical feasibility failures, uncertainty intervals and both unmet 50k and met 400k median-prefix targets. Kept optical feasibility separate from physical transmission and ring capture.

## Pending scientific work

The existing tasks B01–B12 remain pending. Draft creation is not completion of the scientific tasks or B11's final writing/formatting deliverable. Explicit revision notes identify the missing closest-literature comparison, boundary/hardware confirmation, design-beam reconciliation, active-error audit, independent transport validation, correction knobs and margin comparisons. The six planned figures remain pending; no artificial scientific plots were inserted. Funding, contributions and conflicts await author input; final JKPS template conversion remains future work.

## Validation

Compiled from copied manuscript/bibliography/export files in a fresh ignored `results/bts_draft_*` directory using pdflatex, BibTeX and two further pdflatex passes. The final build has no errors, warnings, overfull boxes or unresolved references/citations; BibTeX has no warnings. Visually checked title/abstract, results tables and bibliography pages. Checked abstract length, citation keys, new local links, source/export digests and whitespace. Existing NKM manuscript and protected-input hashes were verified unchanged (108 files).

No physics simulations or new executable code were introduced. Validation consisted of the clean isolated document build and evidence/content checks; no unrelated test suite was rerun. Updated both documentation indexes and preserved all previous plans/reviews.
