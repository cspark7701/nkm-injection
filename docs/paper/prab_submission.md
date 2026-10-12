# PRAB manuscript formats and submission metadata

D15 completed for **Physical Review Accelerators and Beams (PRAB)** at the author's request. The main draft is one column; the additional two-column PDF is a layout preview. Both use the same scientific text, bibliography, numerical macros and figures.

## Manuscript entry points

- `paper.tex` → `paper.pdf`: REVTeX 4.2 with `aps,prab,preprint` (primary draft).
- `paper_twocolumn.tex` → `paper_twocolumn.pdf`: a three-line wrapper selects `aps,prab,reprint` (two columns).

The one-column draft uses APS preprint styling with double spacing and a separate title/abstract page (28 pages in this build). The two-column preview uses the journal reprint layout (14 pages). Wide multi-panel figures and tables use full-width floats in both layouts. Edit the scientific text only in `paper.tex`; the wrapper contains no duplicate manuscript. APS author, email, affiliation, abstract and acknowledgment structures are used, with `apsrev4-2` bibliography formatting and article titles.

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

PRAB is the confirmed target and the layout conversion is complete. Third-round review tasks remain separate and unexecuted by D15. The manuscript's missing campaign-03 evidence still needs to be supplied for independent verification; an installed-asset PDF build does not validate that numerical evidence. Review history is preserved, and no external submission, upload or push occurs here.

The native apsrev4-2 author-control notice (`jnrlst (dependency: not reversed) set 1`) is permitted; all other BibTeX warnings remain build failures. Native REVTeX controls enable article titles via `longbibliography`.
