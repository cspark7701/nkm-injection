# BTS optics manuscript

First manuscript draft, 2026-10-13. Proposed target: **Journal of the Korean Physical Society (JKPS), Research Article**.

- [One-column LaTeX draft](paper.tex) and [compiled PDF](paper.pdf)
- [Manuscript outline and campaign evidence](001_manuscript_outline.md)
- [Ordered preparation tasks and acceptance criteria](002_manuscript_tasks.md)
- [Article scope, question, and candidate claims](article_scope.md) (Task B01)
- [Literature survey and regional/global comparison](literature_comparison.md) (Task B01)
- [Scientific evidence inventory and failure audit](evidence_inventory.md) (Task B01)
- [Claim evidence ledger](claim_evidence.csv) (Task B01)

The proposed paper asks how nine quadrupoles can match the booster-to-storage-ring transfer line while preserving beam-envelope margin and tolerating specified errors. The existing deterministic and optics-tolerance campaigns provide starting evidence. Correction-knob analysis, physical transport validation and an independent design comparison are proposed new work.

The NKM manuscript remains in [docs/paper/](../paper/). Its finite-length kicker, storage-ring capture and stored-beam transparency results are outside this paper's main scope. The draft contains archived matching and tolerance results, four data tables and explicit revision notes. The planned scientific tasks B01–B12 remain pending; the article is not submission-ready. No new simulation campaign was executed.

Use SI units internally: position and beta in m, angle in rad, energy in eV, quadrupole strength in m^-2, gradient in T/m; alpha, relative momentum offset and dispersion derivative are dimensionless. Save future numerical outputs under new `results/bts_journal_campaign_*` directories and select them through a separate BTS evidence manifest. Keep ignored raw outputs out of git.


## Build the first draft

The generic one-column `article` class is used for editing. Final conversion to the current JKPS format remains task B11. The six planned scientific figures are pending; no fabricated plots are included. Bibliography entries are selected from the existing audited references in `docs/paper/`, with a new BTS literature review still needed.

From the repository root, compile in a new ignored output directory:

```bash
bts_build_dir=$(mktemp -d "$PWD/results/bts_draft_XXXXXX")
cp docs/paper_bts/paper.tex docs/paper_bts/paper.bib "$bts_build_dir/"
cp -r docs/paper_bts/generated "$bts_build_dir/"
(
  cd "$bts_build_dir" || exit 1
  pdflatex -interaction=nonstopmode -halt-on-error paper.tex &&
  bibtex paper &&
  pdflatex -interaction=nonstopmode -halt-on-error paper.tex &&
  pdflatex -interaction=nonstopmode -halt-on-error paper.tex
)
# After checking the build log and rendered pages:
cp "$bts_build_dir/paper.pdf" docs/paper_bts/paper.pdf
```

Requires pdflatex, BibTeX and the standard packages listed in `paper.tex`. The installed publication values allow a clean document build without ignored campaign files. Numerical reproduction requires those raw files and is separate from PDF compilation. [draft_provenance.json](draft_provenance.json) records the selected source hashes and the exported table digest. Re-export values only after verifying a new evidence selection; do not mix configurations or edit numbers to improve the results.
