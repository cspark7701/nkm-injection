# Milestone 219 — E10: Supplemental Material and presentation fixes

Completed: 2026-10-14. Round-3 task E10 (R1C-07, R2c-9). Done while the E7 rerun was computing. It is independent of
E7's numbers.

**Supplemental Material** (`docs/paper/supplement.tex`; REVTeX, same macros and figures; 6 pages):
- **S1.** The independent trajectory check (table S1, moved from the main text).
- **S2.** Wire-position and loop-current sensitivity tables (S2 and S3, moved from the main text).
- **S3.** The larger-emittance (100/10 nm rad) sensitivity case: its survival, the vertical-kick diagnostic and
  Figure S1 (formerly Figure 6), moved from section 5.
- **S4.** Statistical methods:
  - particle Wilson intervals, realization bootstrap and ring-cluster bootstrap;
  - paired differences;
  - partial Spearman correlations with Holm adjustment;
  - the acceptable-loss test, stated as one-sided **noninferiority** against the *declared analysis margin* (not
    "predeclared"; R1C-06 wording).
- **S5.** Procedures: the corrected-ring chain, operating-point selection, window scan and matched-knob tuning.

**Main text.**
- Section 2.1 defines the "first unstable launch" once.
- Section 2.3 points to S4 for the statistical definitions.
- Section 2.2 and section 6 cite the supplemental tables.
- Section 5 keeps a one-sentence pointer to S3.
- The open-IVU half-gap of 9 mm is justified against the sourced 8 mm (Seok et al. 2024): at β_y ≤ 3.6 m both give a
  normalised aperture ≥ 4.2 mm m^-1/2, against 1.81 in the arcs.
- The wire-table number format (no "−0.000") is fixed in the builder.

**Build.**
- `build_submission_package.py` stages and compiles `supplement.tex` under the same log gate. It archives it, installs
  `supplement.pdf` with `--install-pdf`, and records the supplement page count.
- Both layouts now build clean. This resolves the two-column "float is stuck" warning noted in milestone 213.
- One-column: 29 pages. Supplement: 6 pages.

**Moved to E8.** The abstract's population wording and the robust capture in the comparison table depend on the E7
results.

**Checks.** The submission-package tests pass (9, including a new supplement-staging test).
