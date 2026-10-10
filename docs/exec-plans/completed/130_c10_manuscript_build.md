# Milestone 130 — C10: Revised manuscript build (KLS, exact 3-D NKM)

Completed: 2026-10-11. Consolidated task C10 (manuscript rewrite and gated build for all reviewer items).

**Build chain.**
1. `scripts/make_revision_manifest.py --require-all --output docs/jinst-paper/revision_manifest.json` records 46
   campaign-02 and supporting artifacts (key → repository-relative path, SHA-256). None is missing.
2. `scripts/build_revision_figures.py --manifest docs/jinst-paper/revision_manifest.json --install-dir
   docs/jinst-paper/generated` writes eight figures, `journal_macros.tex`, `figure_provenance.csv` and
   `consumed_artifacts.json`. The builder verifies the digest of every artifact it reads. The campaign-01 figures
   (fig1_kick_geometry … fig7_bts_tolerance) are removed from `generated/`; `campaign_manifest.json` is kept for history.
3. `scripts/build_submission_package.py --output-dir results/journal_campaign_02/submission_package_rev1 --install-pdf`
   compiles in isolation (pdflatex → bibtex → pdflatex ×2). Result: 13 pages; no LaTeX errors, undefined references or
   citations, BibTeX warnings or overfull boxes. The supplement now carries `revision_manifest.json`.

**Manuscript (`docs/jinst-paper/paper.tex`).** Fully rewritten for the revision:
- Title: "Finite-length and vertical effects in nonlinear-kicker injection into the Korea Light Source". The facility is
  named KLS throughout; the lattice file name K4GSR_HBIv4-1 is unchanged.
- Sections: system and model; finite-length and vertical effects; operating window; survival, acceptance and
  sensitivity; stored-beam transparency; robustness and tolerances; pulsed-magnet considerations; discussion and
  limitations; conclusions. Every number is a builder macro.
- Robustness reports both ensembles (no correction / ideal static orbit correction) and the jitter tolerance curves. The
  final wording was checked against the macros:
  - "about two points without errors to about twenty with them" (92.5 vs 94.5 %; −20.9 and −21.2 points);
  - "jitter below a quarter costs nothing measurable" (70.0 vs 69.7 %);
  - partial rank correlations for both ensembles (booster angle −0.45/−0.68 uncorrected, −0.52/−0.75 corrected;
    booster position −0.24 once corrected);
  - the abstract states that a quarter of the assumed jitter raises the corrected mean to 70.0 %.
- A nested math-mode error (`$c_3=\CubicCoeff$`, the macro carries its own `$…$`) was found by the package gate and
  fixed. Earlier quick compiles did not report it because their log filter missed `!` lines.

**Figures checked visually.**
- Fig. 1: legend moved to the lower right, clear of the kick peak.
- Fig. 8 centre: compact three-column legend above the data (corrected mean, p10, uncorrected mean, x-only and x′-only).
  The caption states solid = corrected, dashed = uncorrected (left), dotted = uncorrected mean (centre).
- Figs. 2–7: no overlaps or clipping.

**Support documents.**
- `claim_evidence.csv`: new rows C0–C16 map every headline claim of the revised paper to a revision-manifest key and
  macro. Row C0 marks A1–B18 (campaign 01) as superseded.
- `submission_checklist.md`: rewritten for the revision build chain, findings → evidence → milestone, gate and author
  actions. The journal is undecided; the text stays venue-neutral.
- `cover_letter.md`: rewritten for KLS and the 3-D findings, venue-neutral.

**Code changes.**
- `build_revision_figures.py`: legend placements (figs. 1 and 8). It now loads `build_journal_figures.py` with
  `importlib` instead of inserting into `sys.path`, which `tests/test_package_imports.py` forbids; the regenerated
  macros are byte-identical.
- `build_submission_package.py`: supplement and recorded commands use the revision manifest. Its test now expects eight
  referenced figures.
- `build_evidence_bundle.py`: new `--builder journal|revision` option used by C11 (milestone 131).

**Checks.**
- Protected files unchanged.
- Full test suite: 663 passed (`OMP_NUM_THREADS=1 python -m pytest -q`).
