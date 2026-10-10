# Milestone 135 — General article format and manuscript directory

Completed: 2026-10-11.

## Changes

Renamed `docs/jinst-paper/` to [docs/paper/](../../paper/) and updated maintained
script/package paths, publication-output guards, tests, README, manuscript metadata
and documentation links. Historical task references now resolve to the relocated
documents; their scientific findings and recorded hashes were retained.

Converted [paper.tex](../../paper/paper.tex) to a standard A4, 11 pt LaTeX article
with 2.5 cm margins, standard author/affiliation and corresponding-author footnote,
an abstract environment, a keywords paragraph, numbered sections, line numbers,
hyperlinks, acknowledgments and the existing numbered bibliography. Removed the
unused JINST style and journal-specific front matter. The abstract and scientific
body are preserved, apart from the manuscript path and acknowledgments command.

Submission packaging now stages only standard article inputs and creates
`nkm_article_submission_source.tar.gz` with the `nkm_article_submission/` prefix.
Publication builds and source-directory protection now use `docs/paper/`; cleanup
and evidence-bundle paths were updated. Evidence bundles still archive committed
code through `git archive`, so a fresh committed snapshot is required to include
the directory migration; no evidence bundle was rebuilt during this task.

## Validation

- Built the source package in the fresh `results/article_conversion_20261011/`
  directory and installed the clean 12-page [paper.pdf](../../paper/paper.pdf).
  BibTeX and LaTeX gates passed without undefined citations/references or overfull
  boxes. The staged build contains no JINST template.
- Passed 90 focused tests across submission packaging, journal macros, publication
  validation/build isolation, production routing and paper pipelines/regressions.
- Inspected PDF text and the rendered first page.
- Verified 38 manuscript Markdown links and no old directory references in
  maintained tracked text after relocation.
- Verified that every relocated input exists except the intentionally removed
  style, and that figure assets and numerical macros are byte-identical.
- Verified the original abstract/scientific body and all nine protected source
  hashes. No scientific simulation was rerun.
- Final git status/diff and whitespace checks confirm only the requested migration,
  formatting, related paths and execution archive changes. Build outputs remain
  under the ignored results directory.
