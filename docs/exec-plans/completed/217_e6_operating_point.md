# Milestone 217 — E6: Operating point re-selected for the design beam

Completed: 2026-10-14. Round-3 task E6 (R2c-3; author inputs B3 and B4 at their defaults: both blades, 3σ clearance).

**Rule** (declared in the driver before running):
- 3σ_x septum clearance (σ_x = 159 µm);
- x_inj at the limit and 0.25/0.5/1.0 mm further out, S = 0.80–1.00, with the 3-D matched angle;
- objective: p10, then mean, of capture over the ten E5 rings with the E4 chamber;
- 100-particle selection bunches, then fresh 2 × 500-particle validation.

**Result.**
- **2 mm blade (primary).** x_inj −19.48 mm, S 0.95, x′ 5.319 mrad, centroid −7.44 mm. Validated: ideal 98.4 %, ring
  mean 78.0 %, p10 65.7 %.
- **Round-2 point on the same rings.** 68.9 % mean, 43.3 % p10.
- **1 mm blade.** About equal (78.8 % mean).

The gain comes from a 1.1 mm smaller injected amplitude, reached through kick strength and angle, not septum
position. The selection ranking is flat within its noise.

**Defect found and fixed.**
- **Cause.** The validation's dipole control used the round-2 calibration, so its selected-point rows are invalid.
- **Fix.** The driver now calibrates controls per validated point, and `--redo-validation` recomputes them, keeping
  the superseded rows.
- **Scope.** The NKM results are unaffected, and the E7 ensembles calibrate at their own point.

**Code.**
- `scripts/run_round3_operating_point.py`;
- `scripts/run_round3_point_studies.py` (follow-up studies at the new point);
- `run_round2_validation.py` and `run_round2_chamber.py` pass the in-magnet chamber
  (`--nkm-magnet-half-mm`);
- `make_round3_manifest.py`: E6 keys and round-2-key overrides to the campaign-04 reruns, each applied only when its
  file exists;
- `build_revision_figures.py`: step `round3_operating_point` (`RThreeOp*`, `RThreeVal*` macros).

**Evidence.** `results/journal_campaign_04/e6_operating_point/` (selection, validation, selected configs).

**Follow-up.** The window, trajectory check, validation and chamber study at the new point run next. The manuscript
text of sections 4–5 is updated with them (milestone 218).
