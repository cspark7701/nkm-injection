# Milestone 209 — Reviewer 2, third-round report on the PRAB manuscript

Completed: 2026-10-13. User request: review `docs/paper/` again as Reviewer 2, decide on acceptance, and write a report
with revision tasks without overwriting previous reviews.

**Output.**
- `docs/paper/reviews/reviewer2_report_round3.md`: new file.
- The reviews `README.md` gains a new row and a summary.
- Earlier reports and responses are unchanged.

**Recommendation.** Major revision, focused on the robustness section; no acceptance in the present form.
- All 15 round-2 tasks received substantive answers and are not reopened.
- New tasks R2c-1 to R2c-9: five A, three B, one C, with an order and coordination with Reviewer 1's round-3
  register.

**Checks run by the reviewer (read only; nothing in `results/`, `src/` or the manuscript changed).**
- **Evidence.** All 205 artifacts of `revision_manifest_round2.json` are present and match their hashes. The bundle
  hash `0e07de5f…3f3d` matches the D13 record.
- **Corrected rings** (`d5_selected_scenario`, `d6_chamber_da.json`, `d6_corrected_chamber`):
  - SVD correction stops after 1–2 iterations at 66–85 µm (x) and 47–56 µm (y) rms;
  - there is no optics correction, and β_x at the NKM ranges from 15.1 to 17.7 m;
  - the closed orbit at the NKM reaches 103 µm;
  - the first unstable DA point is −9.0 to −10.0 mm, and −7.0 mm for ring 5501, which captures 2.7 %;
  - the ring-only mean is 68.3 % without ring 5501, against 61.7 % with it.
- **Tuning** (`d8_tuning`): 33 of 50 machines accepted the single step toward the septum (x_inj −19.0 mm).
- **Septum clearance.** σ_x at the septum is 0.16 mm for the design beam and 0.49 mm for the 100 nm beam, so the
  −19.5 mm point keeps 9.4σ of clearance with the design beam.
- **NKM chamber.** The 30 × 15 mm half-aperture contains the wires at (±5.3, ±5.3) mm. A feasible half-height is
  ≤ 4.3 mm, i.e. a normalised aperture ≤ 1.82 mm/√m, against 1.80 (arc) and 2.64 (centre bend), from β_y computed
  with pyAT.

**Status.** No simulations were run and the protected files are unchanged.
