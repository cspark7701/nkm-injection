# Milestone 276 — R4-BTS-10: steering assumptions, layouts and vertical exit centroid

Completed: 2026-10-31. Round-4 task R4-BTS-10 (Reviewer 2 R2C-05; Reviewer 1 R3-BTS-06).

**Computation.** `results/bts_round4_campaign_20261030/layouts_b`, tracked, on the round-3 steering realizations
(seeds 91001–91005).
- **Layouts:** full (11 readings, 6 trims); reduced monitors (exits of q13, q23 and q33, the septum entrance and the
  line end); series bends (b1–b3 as one knob, kicks proportional to bending angle); and both.
- **Reading errors:** each candidate point has one, seeded per setting as in round 3.
- **Retained run:** a first `layouts/` run stopped with the old scan; it holds only its configuration.

**Results.**
- **Reproduction.** The full layout reproduces round 3 exactly: 20 100 lost particles, and the same prediction.
- **Reduced monitors.** The losses are unchanged to 0.01 percentage point.
- **Series bends.** The exit-angle spread grows from 0.37 to 0.44 mrad (matched reference), and the loss-based
  setting's loss rises from 0.23 % to 0.31 %.
- **Vertical exit centroid,** uncorrected: 1.12 mm / 0.10 mrad rms for the matched reference, and
  0.77 mm / 0.094 mrad for the loss-based setting.

**Article.**
- **Section 2.4.**
  - The eleven readings are assumed instrumentation (no monitor elements in the lattice), and the six trims are
    assumed to be independently powered.
  - Magnet errors, shots and particles are shared between settings, but the reading errors are drawn per setting
    (`[bpm_seed, realization, design_index]`).
- **Section 3.3.** The objective uses the nominal beta functions and the error-free line, without static residuals
  or beta fluctuations, so the error-free prediction and the test describe different populations.
- **Section 4.2.**
  - The angle spread "stays at" 367 µrad (364 µrad uncorrected) rather than "falls".
  - The vertical exit centroid is reported as the static vertical injection error passed to the injection
    calculation.
  - New layout paragraph and Table 5 (`generated/round4_layout_rows.tex`).
  - "Same error realizations" becomes "same magnet errors".

The isolated build is clean (19 pages). Protected files are unchanged. The layouts stage started before the
`edge_best` runner edit of milestone 274; that edit did not touch the layouts code path. The source hash in the
stage's `configuration.json` is therefore the pre-edit file, and the one in `layouts.json` is post-edit.
