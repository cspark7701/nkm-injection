# Milestone 277 — R4-BTS-07: framing, baseline provenance and title

Completed: 2026-10-31. Round-4 task R4-BTS-07 (Reviewer 2 R2C-02 and R2C-08, title; Reviewer 1 R3-BTS-07, strength
labels and TDR prominence).

**Article changes.**
- **Title.** *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker
  injection at the Korea Light Source*. It names the studied design version's purpose and says
  "booster-to-storage-ring"; the supplement title follows it. The date is October 31, 2026.
- **Abstract.** It is rewritten around the results that carry the paper:
  - boundary-fixed nominal clearance at the blade;
  - the phase-advance partition of the jitter;
  - the loss depending on μ_x alone, smallest at the lower edge;
  - the best-found setting's 3- to more than 10-fold tracked reduction;
  - the jitter regime (a stress level of 1.3/2.2 beam sizes; negligible loss at 0.1–0.2 of it);
  - the dispersion-free extension.

  The unmatched baseline no longer leads.
- **Introduction, goal paragraph.** The goal is what controls the loss among matched settings. The baseline is the
  starting point, and setting names are defined once: baseline, optimized low-beta (low beta), matched reference,
  loss-based.
- **Section 4.1, baseline provenance.** The baseline strengths are those supplied with the BTS configuration
  before this study; they have been in the repository since milestone 01 (`record_baseline_metrics.py`,
  2026-07-23). No record states their design exit target, and they miss the present one. Their blade overlap is
  expected, because d_b is defined from the matched exit beam.
- **Discussion, first paragraph.** Matching is a prerequisite rather than a result; the questions start from the
  matched settings.
- **Figures 2–3 and Table 3.** These keep the author-requested baseline-versus-optimized comparison (commit
  `cfb23de`). The label "Baseline setting (reference)" became "Baseline setting", so that "reference" names only
  the matched reference. They were regenerated with `export_bts_at_figures.py` and
  `export_bts_round3_assets.py --clearance-figure-dir` (`results/bts_round4_figures_r407`); the plotted values are
  unchanged, and `layout.pdf` is byte-identical.

**Not changed.** The difference from the TDR line stays in the Introduction, unchanged.

The isolated article (18 pages) and supplement builds are clean. Protected files are unchanged.
