# 207 — Use native Accelerator Toolbox plotting for BTS figures

Request: use Accelerator Toolbox plotting functions for paper figures.

Implemented native `at.plot.plot_linear` rendering of the two-plane reference
and refined low-beta profiles and `at.plot.plot_synopt` for the main lattice
sequence. The full asset exporter calls the same renderer; a standalone CLI
creates new output directories. Updated captions, reproduction instructions,
validation records, article/supplement PDFs and final asset hashes. Statistical
plots and historical supplement figures retain their campaign-based rendering.

Validation: explicit entrance Twiss and 64 finite-element subdivisions; native
computed and rendered curves match frozen independent maps within 2.76e-11 m
(1e-4 m tolerance). Both isolated TeX builds pass strict checks. All 20 BTS tests
pass and all 32 evidence claims audit successfully. Figures inspected visually.
Protected inputs, numerical summaries, campaigns and previous reviews unchanged.
No remote operations or journal submission. Frozen older attachments retained;
updated rendering distributed in a separate newly generated local attachment.
