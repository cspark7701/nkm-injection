# Milestone 115 — Journal Task 012: submission package and final gate

Completed: 2026-10-09 (package prepared; author confirmation pending). Task: [012](../../jinst-paper/tasks/012_submission_package_and_final_gate.md).

Added `scripts/build_submission_package.py` (isolated pdflatex/bibtex build with a strict log gate, source archive with
compiled `paper.bbl` and only referenced figures, PDF, supplement, SHA-256 package manifest, software environment and
commands) with tests `tests/test_submission_package.py`, and [`submission_checklist.md`](../../jinst-paper/submission_checklist.md)
linking each headline finding to its artifact, claim row and review result. Reference build
`results/journal_campaign_01/submission_package_v1`: 10 pages, no errors, undefined references, BibTeX warnings or overfull
boxes; the committed `docs/jinst-paper/paper.pdf` is that build. Open author items: title/authorship/category confirmation,
JINST keywords, funding, JHEP.bst, persistent archive DOI, cover-letter sign-off. No submission, push or source regeneration.
