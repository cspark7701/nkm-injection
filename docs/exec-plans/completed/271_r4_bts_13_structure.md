# Milestone 271 — R4-BTS-13: length and structure

Completed: 2026-10-31. Round-4 task R4-BTS-13 (Reviewer 2 R2C-07).

**Changes.**
- **Section 3.4 to the supplement.** Section 3.4 and Tables 3–4 (accuracy checks and spatial convergence) moved to
  the new supplement Section "Numerical accuracy and spatial observation resolution". That section includes the
  affine-map audit of the earlier four-station campaign.
- **Summary in the article.** One paragraph remains:
  - maps agree with AT within 1.6 × 10⁻⁸;
  - finite-case clearance checks agree within 0.69 µm (`\BtsNewMomentError`);
  - peak beta changes by less than 0.35 mm between 32 and 64 subdivisions;
  - q32 sits at its lower bound.
- **Historical ensembles.** The last sentence of Section 2.2 (the historical optics-only ensembles and their beam)
  moved to the supplement's historical-statistics section.
- **Eq. (5).** It now has the one-sided form at the blade, c = a₊ − ū − 5σ. The sign of ū enters only at a
  symmetric aperture.
- **Table 8.** The roll rows, identical at the printed precision, are collapsed into one row per energy jitter.
  `export_bts_round3_assets.py --only sensitivity` checks that they are identical before collapsing; the macros
  are unchanged.

The isolated article (17 pages) and supplement (9 pages) builds are clean; the article gains Figure 5 and Table 9
from R4-BTS-01/02. The installed PDFs are rebuilt in R4-BTS-09. Protected files are unchanged.
