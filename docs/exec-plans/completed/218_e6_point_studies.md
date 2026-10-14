# Milestone 218 — E6 follow-up: window, validation and chamber study at the selected point

Completed: 2026-10-14. Completes round-3 task E6 (R2c-3).

**Runs** (`scripts/run_round3_point_studies.py`; all with the in-magnet NKM chamber; outputs in
`results/journal_campaign_04/e6_*`):
- angle and position window;
- edge offsets;
- independent DOP853 trajectory check at the new edges;
- 500/4000-turn validation: native and affine references, both edges, and the lowest-capture corrected ring (5501);
- declared chamber study: ideal ring with all profiles and the arc scan, and corrected rings with the elliptic open
  and closed-IVU profiles. Rectangles bracket the octagon corners and are run on the ideal ring only, which halves
  the cost.
- **Dipole revalidation.** The selected-point dipole validation was re-run with the control calibrated at that point
  (`--redo-validation`).

**Results at the selected point** (x_inj −19.48 mm, S 0.95):
- **Windows.** Angular 0.44 mrad (round-2 point 0.76) and position 2.40 mm (1.99).
- **Nominal capture.** 98.4 % / 97.8 % at 500/4000 turns; edges 82.1 / 80.3 % at 4000 turns.
- **Corrected rings.** Mean 78.0 %, p10 65.7 %, min 31.0 % (ring 5501).
- **Dipole control.** 100 % on the ideal ring and 82.2 % on the ring mean.
- **Accuracy allowance.** It shrinks with the window, to 0.044 mrad. The nominal thin-map error is 155 % of it
  (η* = 0.025), so a single thin map is not adequate at this point.

**Manuscript.**
- **Section 4.** Rewritten for the declared selection rule and validation, with the round-2 point kept as a
  reference. The window paragraph states the angle/position trade-off.
- **Section 3.** The scaling sentence states the thin-map inadequacy at the selected point.
- **Section 5.** The chamber-scan sentence is qualified as evaluated at the earlier point.
- **Section 6.** Transparency values are at S = 0.85 and scale linearly with S (factor 1.12).
- **Figures.** 3, 5, 9 and 11 are regenerated. Figures with unchanged data keep their committed bytes.

**Manifest.** `revision_manifest_round3.json` now re-points `round2_window`, `round2_edge_offsets`,
`round2_trajectory_final`, `round2_validation`, `round2_backend_contract`, `round2_chamber_ideal` and
`round2_chamber_corrected` to the campaign-04 runs. It adds `round3_reference_window`, which keeps the round-2 window
for comparison.

**Status.**
- The gated one-column build is clean.
- **Not done.** The E7 robustness rerun was not started (execution stopped after E6 at the author's request). The
  robustness section, Figure 8 and the abstract and conclusion numbers still come from the round-2 population and
  point, so the manuscript is internally mixed until E7 and E8 run.
