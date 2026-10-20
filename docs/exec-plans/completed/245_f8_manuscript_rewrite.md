# Milestone 245 — F8: abstract, attribution, discussion and conclusions rewritten from F2–F7

Completed: 2026-10-20. Round-4 task F8 (R1D-01/06/07, R2d-1/2/5/6/7) of the
[round-4 plan](../../paper/reviews/consolidated_revision_plan_round4.md).

**Jitter components** (declared extension, 8e8f628). Ensembles `f2v_xy_x_only` and `f2v_xy_xp_only`, with two-plane
steering, paired with E7. Costs (NKM / dipole / gap, points):
- position-only jitter: −17.4 / −2.6 / −14.7;
- angle-only jitter: −33.7 / −20.5 / −13.2.

Both components are NKM-specific once the vertical error is removed. Recorded in
[round4_vertical_steering.md](../../paper/round4_vertical_steering.md).

**Generated numbers.** `scripts/round4_reporting.py` (builder step `round4`) turns the F2–F6 and two-plane artifacts
into macros and three tables: error-class ablation, operating points, two-model jitter. Every new number in the text
is hash-checked through `revision_manifest_round4.json`.

**Manuscript** (`paper.tex`):
- **Abstract.** It no longer says "chiefly booster angle jitter". The new version gives:
  - the production-trajectory thin-map error (161 µrad, 3.7 × the allowance);
  - the zero-capture fraction (51 %);
  - the attribution: BTS magnet errors leave a 0.90 mm rms vertical injection error; two-plane steering raises the
    NKM to 76.6 %; booster position and angle jitter then become comparably NKM-specific;
  - the operating-point dependence (the dipole loses 17–23 points at the alternatives).
- **New subsection "Attribution of the NKM-specific loss".** It covers the ablation (table), the vertical mechanism,
  the first-turn loss locations, the two-plane sensitivity and its jitter components, the operating-point test (table;
  current point retained) and ring 5501.
- **Robustness section:**
  - bimodal summaries for both models;
  - a two-model jitter table with zero-capture columns;
  - signed and physical associations;
  - the acceptable-loss bound described as a conservative 97.5 % one-sided bound;
  - the chromaticity claim reduced, and the margin fit stated as degenerate (width on the 5 mm bound);
  - the "which this study does not test" sentence removed.
- **Model sections:**
  - septum dispersion (Table II and text) with its angular contribution;
  - physical versus numerical loss boundaries;
  - the thin-map launch scope and an empirical-fit caveat;
  - the coupling promise of section 5 closed.
- **Labels.** Historical S = 0.85 labels on Tables I/II and the Fig. 1/Fig. 7 captions.
- **Discussion and conclusions.** Rewritten around the attribution. The limitations now say the modelled transfer
  line has no vertical correction.
- **Date.** October 20, 2026.

**Supplement** (`supplement.tex`):
- date;
- the acceptable-loss bound definition;
- the signed-association method;
- the ablation definition;
- the S = 0.95 label on the wire tables.

**Test hygiene.** The round-4 scripts and tests used `sys.path.insert`, which `test_package_imports` forbids; that
test had failed since F1. They now use script/package import fallbacks and `from scripts import …`. The full suite
passes (756 tests); every edited script runs directly.

**Build check** (scratch; the final PDF install is F9):
- one-column 33 pages, two-column 17 pages, supplement 7 pages;
- no errors, undefined references or overfull boxes under the submission gate.

**Notes.**
- F2 archive: the other classes' largest effect is corrected to 1.6 points.
- The F5 note has a dated update: its first-turn vertical losses are a direct vertical injection error.
