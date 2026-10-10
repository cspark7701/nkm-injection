# Milestone 133 — Introduction expanded with verified references

Completed: 2026-10-11. User request: improve the Introduction with more references.

**Changes to `docs/jinst-paper/paper.tex` (Introduction).**
- **New opening paragraph:**
  - multibend-achromat rings and their small DA (Hettel2014, Raimondi2021);
  - top-up operation (Emery1999);
  - the alternatives to off-axis injection: on-axis swap with an accumulator (Emery2003) and longitudinal injection
    (Aiba2015).
- **Pulsed-multipole paragraph:**
  - adds the pulsed-quadrupole demonstration at the KEK PF-AR (Harada2007);
  - adds MAX IV's single dipole kicker for commissioning (Leemann2012).
- **Kick-map paragraph:** adds integration through s-dependent fields (Wu2003).
- **Scope paragraph:** introduces the KLS lattice (4 GeV, 28 HMBA cells, about 800 m, 62 pm; Kim2025).
- **Wording fix:** "dynamic aperture (DA)" is now defined only once.

**Verification.** All nine references were checked against Crossref or the JACoW reference database. Emery2003 was also
checked in its full text, which describes swapping the beam with an accumulator. Records are in
`bibliography_audit.md`.

**Build.**
- `build_submission_package.py` now repeats pdflatex, up to four passes, while LaTeX still reports "Rerun to get".
  The extra citations moved labels after the second pass.
- Result: `results/journal_campaign_02/submission_package_rev2`, 14 pages, clean. The installed `paper.pdf` is this
  build.
- `tests/test_submission_package.py` and `tests/test_package_imports.py` pass.
