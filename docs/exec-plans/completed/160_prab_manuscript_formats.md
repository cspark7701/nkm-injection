# Milestone 160 — Convert the manuscript to PRAB formats (D15)

Completed 2026-10-12 at the author’s explicit request to target Physical Review Accelerators and Beams, with a one-column primary draft and a two-column side version.

## Changes

- Converted the shared manuscript to REVTeX 4.2 with native APS author, affiliation, email, abstract, acknowledgments and apsrev4-2 bibliography formatting.
- Built the primary preprint draft, `docs/paper/paper.pdf` (28 pages), and the wrapper-selected reprint preview, `docs/paper/paper_twocolumn.pdf` (14 pages). Wide figures and tables span the available page width. A title-page break prevents front-matter clipping in the review draft.
- Added layout selection and job-specific BibTeX/log/PDF handling to the isolated submission builder. Initial LaTeX failures and oversized/stuck floats now fail the build.
- Documented build commands and proposed PhySH portal subjects; targeted the cover letter and submission checklist to PRAB. Preserved all existing reviews.

## Verification and limits

Both isolated builds completed pdflatex, BibTeX and two further pdflatex passes without errors, undefined references/citations, bibliography data warnings, overfull boxes or stuck/oversized floats. Visually inspected the rendered title pages and representative figure, table and bibliography pages. The relevant submission, publication-build and reporting tests pass (37 tests).

Hash checks preserve all 36 snapshotted scientific assets, protected inputs and review documents. The scientific manuscript body remains unchanged after normalizing layout-only edits. No scientific simulations were rerun. Build outputs and auxiliary files are under new ignored `results/prab_d15_*` directories.

D15 completes venue selection and formatting only. Third-round scientific revision tasks remain pending. Campaign-03 raw evidence is unavailable locally, so these installed-asset builds do not repeat the historical evidence-bundle verification. No external submission, upload or git push was performed.

The native apsrev4-2 author-control notice (`jnrlst (dependency: not reversed) set 1`) is permitted; all other BibTeX warnings remain build failures. Native REVTeX controls enable article titles via `longbibliography`.
