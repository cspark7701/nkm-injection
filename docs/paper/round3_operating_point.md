# Round 3: operating point re-selected for the design beam (E6)

> Status 2026-10-16: Selection/validation is complete for the no-injection-error objective. Robust optimality and a preference for a wider-window point remain untested; F3 will address the paired comparison.
> See the [pending follow-up](reviews/consolidated_revision_plan_round4.md).

**Why.** The round-2 point (x_inj = −19.50 mm, S = 0.85, x′ = 4.853 mrad) had been selected on the ideal ring with
the 100 nm rad sensitivity beam and was never re-selected (Reviewer 2, round 3, M1).

**Declared rule** (`scripts/run_round3_operating_point.py`, fixed before any run):
- **Clearance.** x_inj ≤ septum edge − blade − 3σ_x. The design-beam σ_x at the septum is 159 µm, which gives limits
  of −18.48 mm for the 2 mm blade (primary) and −17.48 mm for the 1 mm KLS thin septum (alternative).
- **Knobs.** x_inj at the limit and 0.25, 0.5 and 1.0 mm further out; S = 0.80–1.00. x′ is the inner matched root of
  the 3-D magnet. All 40 candidates had a root, with the centroid inside the DA.
- **Objective.** Tenth percentile of capture over the ten E5 corrected rings (mean as tie-break), with the E4 chamber,
  no injection errors, 100 particles per ring (seed 3001), 500 turns.
- **Validation.** Fresh 2 × 500-particle bunches (seeds 1001/1002) on the ideal ring and all ten rings.

**Selected.**
- **2 mm blade (primary).** x_inj = −19.48 mm, S = 0.95, x′ = 5.319 mrad, centroid at the NKM −7.44 mm.
- **1 mm blade.** x_inj = −17.48 mm, S = 0.80, x′ = 4.455 mrad, centroid −7.40 mm.

The selection ranking is flat within its noise: the top candidates span p10 0.67–0.71 and mean about 0.78, for both
blades.

**Validation** (fresh particles; NKM; corrected rings with chamber, no injection errors):

| Point | Ideal ring | Ring mean | Ring p10 | Ring min |
| :--- | ---: | ---: | ---: | ---: |
| Round-2 point (−19.50 mm, S 0.85) | 97.0 % | 68.9 % | 43.3 % | 41.3 % |
| Selected, 2 mm blade (−19.48 mm, S 0.95) | 98.4 % | 78.0 % | 65.7 % | 31.0 % |
| Selected, 1 mm blade (−17.48 mm, S 0.80) | 98.5 % | 78.8 % | 66.3 % | 34.8 % |

**What it shows.**
- **Gain.** Re-selection adds about 9 points to the mean and 22 to the tenth percentile on the corrected rings.
- **Mechanism.** The gain comes from a smaller injected amplitude. The kicked centroid moves from −8.52 to −7.4 mm,
  through a stronger kick and a larger angle rather than by moving the septum.
- **Clearance alone.** Moving x_inj up to the 3σ clearance limit at fixed S does not help, and the thinner blade adds
  little.

This answers Reviewer 2's round-3 M1: re-selection matters, through the injected amplitude, but the septum position
was not the binding knob.

**Correction to the validation run.** The dipole control was calibrated once at the round-2 point and applied
unchanged at the new point, so its first validation rows (5.5 % mean) are invalid. The driver now calibrates the
controls at each validated point. The dipole rows are recomputed with `--redo-validation`, and the superseded rows are
kept in the artifact. The NKM rows are unaffected.

**Follow-up at the selected point** (`scripts/run_round3_point_studies.py`): the window, angular-edge offsets, the
independent trajectory check, 500/4000-turn validation and the chamber study are rerun at the new point, so that the
manuscript uses a single operating point.

## Follow-up studies at the selected point (completed)

Run with `scripts/run_round3_point_studies.py`. All of them include the in-magnet NKM chamber.

| Study | Selected point | Round-2 point |
| :--- | :--- | :--- |
| Angular window at 80 % | −0.32 to +0.12 mrad (width 0.44) | 0.76 mrad |
| Position window at 80 % | −1.87 to +0.53 mm (width 2.40) | 1.99 mm |
| Nominal native capture, 500 / 4000 turns | 98.4 % / 97.8 % | 97.0 % / 96.1 % |
| Affine element-map reference, 500 turns | 99.5 % | 100 % |
| Angular-edge candidates, 4000 turns | 82.1 % / 80.3 % | 79.4 % / 84.7 % |
| Lowest-capture corrected ring (5501), 500 / 4000 turns | 32.1 % / 27.5 % | 3.0 % / 1.4 % (round-2 ring) |
| Chamber study: ideal ring, NKM / dipole | 98.4 % / 100 % | 97.0 % / 97.3 % |
| Chamber study: corrected rings, mean / p10 / min | 78.0 / 65.7 / 31.0 % | 61.7 / 52.3 / 2.7 % (round-2 rings) |
| Rectangular arc scan, 10 / 12 / 15 mm half-width | 92.7 / 98.5 / 99.4 % | 81.7 / 97.0 / 99.7 % |

The selected point trades angular width (0.44 against 0.76 mrad) for position width (2.40 against 1.99 mm). Its
declared accuracy allowance (one tenth of the angular window) falls to 0.044 mrad. The nominal thin-map error,
0.069 mrad, is now 155 % of it, and η* is 0.025. At this point a single thin map is therefore not adequate.

**Dipole validation, recomputed** with the control calibrated at the selected point: 100 % on the ideal ring, ring
mean 82.2 % (p10 68.8 %). The superseded rows are kept in the artifact.

**Not yet updated.** The robustness section (joint-error ensembles, jitter, tuning) still reports the round-2
population and point until the E7 rerun.
