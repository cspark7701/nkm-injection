# NIM A manuscript format and local submission package

Prepared 2026-11-01 for *Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment*.

The primary [source](paper.tex) and [PDF](paper.pdf) now use Elsevier's `elsarticle` class in a one-column preprint layout. This is a review manuscript, not a publisher typeset proof. The separately numbered [supplement](supplement.pdf) remains a supporting document. Both use the numbered `elsarticle-num` bibliography style.

The title block uses the class's author, affiliation, corresponding-author and email fields. The abstract is shortened to below 250 words, preserving the model qualification, assumed jitter, uncertainty scope and ring-capture exclusion. It has six keywords. The [four proposed highlights](highlights.txt) are supplied separately in editable text; each is below 85 characters, including its bullet prefix. The Humanizer skill was applied to the abstract without changing the reported results. Main-text scientific prose, equations, tables, figures and bibliography data are unchanged.

## Build and package

Use a TeX Live installation containing `elsarticle`, `elsarticle-num`, `latexmk`, `pdflatex` and `bibtex`. The builder uses Python's standard library and does not run simulations.

From the repository root:

```bash
python scripts/build_bts_nima_submission.py \
  --output-dir results/bts_nima_submission_new \
  --install-pdfs
```

Choose a new output directory every time. Omit `--install-pdfs` to build without replacing the tracked article and supplement PDFs. The builder rejects an existing output directory, missing inputs, conflicting flattened filenames, compilation failures, layout warnings and unresolved references.

The output directory contains:

| File or directory | Use |
| :--- | :--- |
| `paper.pdf` | Main review manuscript |
| `supplement.pdf` | Supplementary material |
| `source/highlights.txt` | Separate editable highlights upload |
| `bts_nima_sources.zip` | Editable LaTeX sources, bibliography, generated tables/macros, figures, `.bbl` files and numbered bibliography style |
| `source/` | The exact flat source files in that archive |
| `build/` | Local compilation logs and auxiliary files; excluded from the archive |
| `build_manifest.json` | SHA-256 identities for repository inputs, exported files and final outputs |

The archive places all files at its root. References to `generated/` and `figures/` are rewritten only in the exported sources, because Elsevier's Editorial Manager guidance requires a flat source directory. The repository retains its existing directory structure. Standard TeX Live classes/packages are not copied into the archive. The generated macros preserve the selected numerical values.

The verified conversion build is `results/bts_nima_submission_20261101_v4/`: 19 article pages and 10 supplement pages. Earlier unsuccessful formatting builds remain diagnostic outputs. They are not the selected package. The final archive was extracted into a fresh directory and both documents were rebuilt there, with layout and reference checks. No simulation outputs are bundled into this manuscript-source archive; the separately verified scientific referee attachment retains that role.

## Submission status

NIM A is now the selected target, as instructed by the author. This closes the journal-selection part of the earlier deferred author decisions. It does not constitute manuscript approval, journal submission or acceptance.

The remaining author-dependent matters continue in the [submission checklist](submission_checklist.md): final scientific approval, data-availability wording/access in the submission interface, and the access route for the companion NKM study. The manuscript's existing funding, competing-interest and pending-approval statements are retained. No data-availability or generative-assistance statement previously removed at the author's request has been restored by this formatting task. The booster jitter remains an assumed stress level; no machine specification has been invented.

Upload the manuscript PDF, supplement PDF, separate highlights and editable source archive under the corresponding item types offered by the journal. Supply any declarations requested in the actual portal. No cover letter, external upload or submission has been performed. Older referee attachments and dated reviews identify the pre-conversion scientific files; their hashes remain historical records. The current selection record preserves those identities and separately identifies this formatting conversion.

## Publisher guidance

- [Elsevier LaTeX instructions](https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions), checked 2026-11-01: official article class, editable source files, numbered bibliography options and flat Editorial Manager source structure.
- [NIM A guide for authors](https://www.sciencedirect.com/journal/nuclear-instruments-and-methods-in-physics-research-section-a-accelerators-spectrometers-detectors-and-associated-equipment/publish/guide-for-authors): the live page returned HTTP 403 during this task. This conversion does not claim verification of every current journal-specific portal requirement.

The preprint layout, abstract length, six keywords and separate highlights are conservative preparation choices. The exact upload fields and any additional journal-specific requirements should be checked in the submission interface.
