# Calibrated controls and coupled injection operating region (Task 004, campaign S6)

Runs (git-ignored): `results/journal_campaign_01/operating_region_grid/` (grid stage, 120 points, 3156 s) and
`.../operating_region_replicate/` (replicate stage, 8 points, 4033 s), produced by
`scripts/run_injection_operating_region.py` with `config/injection_study_v1.json` and the selected optimisation.
Every point tracks a booster bunch through the BTS (matched or baseline), shifts it to the septum with
(x_inj, x′_inj) and tracks it natively for 500 turns. All kick models at a point share the same particles.

## Explanation of the original control results (selected run `production_statistical_01`)

| Original result | Explanation |
| :--- | :--- |
| off = 100 % | The beam started at the NKM with x′ = 0 at −20 mm, inside the ±30 mm check of a linear one-turn map; the map has no dynamic aperture (DA). Native tracking loses a particle at −20 mm within 4 turns. |
| ideal = 100 % | The "ideal" kick was the Courant–Snyder optimum −α x/β = −0.127 mrad, not a kick of the NKM's strength; it barely changes the amplitude. |
| linear = 0 % | Taylor expansion about −20 mm of a map whose slope there is large and whose sign was opposite to the electron Lorentz sign used elsewhere; it increased the amplitude. |
| fieldmap = 99.8 % | Kick of −0.93 mrad at −20 mm applied to a beam already inside the linear acceptance. |

None of these comparisons was injection-limited; they are retained only as historical results.

## Operating-region map (grid stage; 200 particles, 500 turns, seed 42)

Angle matching: for each (x_inj, S) the injection angle cancels S·K at the nominal NKM-centre centroid
(inner root). Four combinations have no inner root inside |x| ≤ 12 mm and are reported as infeasible
(x_inj = −22 mm with S = 0.85–0.95; −21 mm with 0.85).

* Kicker off: 0 % at every point.
* Field-map capture at the matched angle ranges from 54 % to 89.5 %; it is highest when the matched centroid
  lies near the kick-map extremum (−8.5 to −9 mm) and decreases monotonically with S at fixed x_inj because
  the centroid moves inwards where |dK/dx| across the ≈ 0.7 mm bunch is larger.
* The angle window is narrow and asymmetric: +0.5 mrad gives 13–64 %, −0.5 mrad gives 15–85 %.
* The linear-map cross-check overestimates capture at every point (e.g. 99.5 % vs 89.5 % at the optimum).
* Selected operating point (predeclared rule: maximum Wilson lower bound; ties → smallest offset):
  x_inj = −20 mm, S = 0.85, x′_inj = 4.869 mrad, capture 89.5 % [84.5, 93.0] %.

## Replicates at the operating point (4 independent bunches × 500 particles; paired models)

| Model | Capture per bunch [%] | Mean | Stored centroid A/σ_x (bicubic map) |
| :--- | :--- | :--- | :--- |
| field map | 90.6, 91.4, 92.0, 90.2 | 91.1 | 5.2×10⁻⁶ (aligned); 0.10 at 0.2 mm, 1.5 at 0.5 mm magnet offset |
| linearised (calibrated) | 94.6, 97.0, 97.0, 96.4 | 96.3 | 2.97×10³ |
| dipole (calibrated) | 94.2, 93.8, 95.4, 95.0 | 94.6 | 2.50×10³ |
| off | 0, 0, 0, 0 | 0 | — |
| field map, baseline BTS optics | 29.2, 24.6, 27.2, 26.6 | 26.9 | — |

The NKM loses ≈ 3.5 percentage points of capture relative to a uniform kick of the same strength at the
centroid (kick variation across the bunch) and is transparent for the aligned stored beam; the calibrated
controls would displace the stored beam by thousands of rms sizes. Matching the BTS is a prerequisite
(27 % with baseline optics).

The bilinear interpolation of the kick map between the 0 and 0.5 mm nodes overstates the near-axis kick
(the wire field is cubic, K ≈ 2.78×10⁴ rad m⁻³ · x³); the stored-beam response therefore uses a bicubic
spline through the same nodes (identical at nodes, exact cubic law near the axis). The bilinear values
(A/σ_x = 1.3×10⁻⁴ aligned) are an upper bound. Capture tracking at |x| ≈ 9 mm is unaffected.
