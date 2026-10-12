# Milestone 173 — Write Standalone JKPS Article and Generate Assets (B11)

Completed: 2026-10-13. User request: Execute the BTS manuscript tasks, track repo status, and git commit after each task.

## 1. Summary of Work Completed

Task B11 of `docs/paper_bts/002_manuscript_tasks.md` was executed to complete the standalone research article targeted for the *Journal of the Korean Physical Society* (JKPS):

1. **Full Manuscript Modernization (`docs/paper_bts/paper.tex`)**:
   - Upgraded from the preliminary 8-page working draft to a comprehensive, publication-ready 11-page manuscript.
   - Removed all provisional draft notes and prospective placeholders.
   - Replaced preliminary summaries with verified findings from Tasks B01–B10:
     - Multi-start feasibility topology (4 of 15 starts fail envelope ceilings despite mathematical convergence);
     - Discovery of the low-$\beta$ margin design ($\beta_{x,\max} = 29.65\text{ m}, \beta_{y,\max} = 36.12\text{ m}$), gaining a $16.47\text{ m}$ vertical stay-clear buffer;
     - Dimensionless SVD Jacobian condition number $\kappa = 57.78$, 6 active tuning knobs, and 3-mode null space;
     - Tail failure rate $9.09 \times 10^{-6}$ with exact 95% Clopper--Pearson interval $[2.95 \times 10^{-6}, 2.12 \times 10^{-5}]$ across 550,000 Monte Carlo samples, driven 100% by vertical envelope blowup;
     - Multi-seed tracking of 50,000 particles across 5 independent seeds with $100.00\% \pm 0.00\%$ physical transmission under design errors, robust survival up to $5\times$ jitter, and clear decoupling of static machine retuning from random shot-to-shot jitter.
   - Preserved full author attribution (Chong Shik Park, Korea University), funding, conflict-of-interest declarations, and repository code availability.

2. **Integration of High-Resolution Figures**:
   - Figure 1: Transfer line mechanical layout and nominal optical profiles ($\beta_x, \beta_y, D_x$).
   - Figure 2: Dimensionless SVD singular value spectrum ($\kappa = 57.78$) and $V^{\mathsf T}$ correction knob loadings.
   - Figure 3: Nominal matched vs.\ low-$\beta$ margin design profile comparison displaying the $16.47\text{ m}$ stay-clear gain.
   - Figure 4: Tolerance scaling curves and OAT sensitivity rankings.
   - Figure 5: Exit transverse phase-space distribution and transmission jitter stress survival curve.

3. **Audited Bibliography (`docs/paper_bts/paper.bib`)**:
   - Expanded and verified BibTeX references including Korean synchrotron and beam transport literature (PLS-II, RAON in JKPS), 4th-generation light sources (K4GSR, MAX IV), and classical statistical methods (Clopper--Pearson, Wilson).

4. **PDF Compilation and Validation (`docs/paper_bts/paper.pdf`)**:
   - Compiled with `pdflatex` and `bibtex` with zero errors and clean output formatting (11 pages, 608~KB).

5. **Regression and Test Integrity**:
   - Executed full test suite (`pytest tests/`), passing all 709 test cases in 132 seconds.

---

## 2. Deliverables Produced

- [`docs/paper_bts/paper.tex`](../../paper_bts/paper.tex)
- [`docs/paper_bts/paper.bib`](../../paper_bts/paper.bib)
- [`docs/paper_bts/paper.pdf`](../../paper_bts/paper.pdf)
- [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md)

---

## 3. Verification and Acceptance Checks

- `pdflatex` compilation succeeds cleanly with zero unresolved citations or broken references.
- All 709 tests pass in `pytest tests/`.
- Scientific source files remain unmodified (`git status`).
- Next task: **B12 — Review, freeze evidence and prepare submission**.
