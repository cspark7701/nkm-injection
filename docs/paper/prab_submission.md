# PRAB manuscript formats and submission metadata

Updated 2026-10-16. D15 completed for **Physical Review Accelerators and Beams (PRAB)** at the author's request; E1–E11 subsequently completed the round-3 revision. Both round-4 reviews now request focused further work; [F1–F9 remain pending](reviews/consolidated_revision_plan_round3.md#round-4-follow-up-to-the-round-3-manuscript). The main draft is one column; the additional two-column PDF is a layout preview. Both use the same scientific text, bibliography, numerical macros and figures.

## Manuscript entry points

- `paper.tex` → `paper.pdf`: REVTeX 4.2 with `aps,prab,preprint` (primary draft).
- `paper_twocolumn.tex` → `paper_twocolumn.pdf`: a three-line wrapper selects `aps,prab,reprint` (two columns).

The one-column draft uses APS preprint styling with double spacing and a separate title/abstract page (30 pages in the installed round-3 build). The two-column preview uses the journal reprint layout (15 pages in the installed round-3 build). Wide multi-panel figures and tables use full-width floats in both layouts. Edit the scientific text only in `paper.tex`; the wrapper contains no duplicate manuscript. APS author, email, affiliation, abstract and acknowledgment structures are used, with `apsrev4-2` bibliography formatting and article titles.

The [APS REVTeX documentation](https://journals.aps.org/revtex) identifies `prab` as the journal option. The [REVTeX FAQ](https://journals.aps.org/revtex/revtex-faq) explains reprint styling. The [PRAB author guidance](https://journals.aps.org/prab/authors) identifies the Research Article type and submission requirements. The rendering is a draft/preview, not the final publisher typesetting.

## Rebuild from installed manuscript assets

Use separate new directories:

```bash
python scripts/build_submission_package.py   --layout one-column --output-dir results/prab_one_new --install-pdf
python scripts/build_submission_package.py   --layout two-column --output-dir results/prab_two_new --install-pdf
```

Omitting `--layout` selects one column. `--install-pdf` updates only the PDF for the selected layout. Each package includes both TeX entry points, the shared bibliography/macros/figures, the compiled layout-specific `.bbl`, provenance and supplements. The package manifest records journal, layout, compilation entry point, pages, hashes and environment. The builds reject LaTeX errors, undefined references/citations, bibliography data warnings, overfull boxes and stuck/oversized floats.

Direct local compilation is also possible with pdflatex, BibTeX and two further pdflatex passes, using `paper` or `paper_twocolumn` as the BibTeX job name. The isolated builder is preferred because auxiliary files remain under ignored results directories.

The installed macros and figures suffice for document compilation. Regenerating those assets from raw numerical evidence is a different operation described in [round2_reproduction.md](round2_reproduction.md). D15 does not regenerate the scientific campaign or refresh its frozen bundle.

## Suggested PhySH metadata

Select suitable subjects in the APS submission portal, using its current [PhySH taxonomy](https://physh.aps.org/). Proposed descriptors, also used on related APS paper pages, are:

- Beam injection, extraction & transport
- Beam code development & simulation techniques
- Beam loss

These are proposed subject headings, not legacy PACS codes. They are submission metadata; no invented identifier or unsupported LaTeX PhySH command is added. The keyword list remains as REVTeX metadata; PhySH headings are selected separately in the portal, and no obsolete PACS list is inserted.

## Submission status

PRAB is the confirmed target and the layout conversion is complete. E1–E11 subsequently executed the third-round revision, including evidence access and an archived-source rebuild (milestone 222). All 235 selected round-3 artifact keys matched local hashes in the 2026-10-16 review. Both round-4 assessments now require the pending F1–F9 follow-up; a new final reconciliation must follow that work. Review history is preserved. No external submission, upload or push is recorded here.

The native apsrev4-2 author-control notice (`jnrlst (dependency: not reversed) set 1`) is permitted; all other BibTeX warnings remain build failures. Native REVTeX controls enable article titles via `longbibliography`.

Current page counts are 30/15 plus a six-page supplement, checked 2026-10-16. D15's 28/14-page record remains
historical. Compilation does not close the round-4 scientific issues; see the [current checklist](submission_checklist.md).
