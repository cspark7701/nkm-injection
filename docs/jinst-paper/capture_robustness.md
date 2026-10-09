# Combined-error capture robustness (Task 006, campaign S7)

Driver `scripts/run_capture_robustness.py`; pooled analysis `scripts/analyze_capture_robustness.py`. Operating point
`results/journal_campaign_01/operating_point_study_config.json` (x_inj = −20 mm, S = 0.85, x′ = 4.869 mrad); frozen
error budget `error_budget.json`; selected optimisation; 200 particles per realization, 500 turns, native tracking.
Per realization: perturbed BTS (gradient, offset, roll, dipole-field errors), booster centroid jitter, β mismatch,
energy offset, emittance and energy-spread variation, septum position, NKM scale/offset/timing, closed-orbit offset.
Realizations are the resampling unit (cluster bootstrap, 10,000 draws, seed 1729). Out of scope: quadrupole
longitudinal placement, power-supply quantisation, ring optics errors, ring magnet errors.

## Results (field-map NKM)

| Ensemble | Realizations | Mean capture [95 % CI] | Median | ≥ 90 % capture |
| :--- | ---: | :--- | ---: | ---: |
| full budget, seed 42 | 50 | 42.8 % [34.7, 50.7] | 54.5 % | 2 % |
| full budget, seed 123 | 50 | 33.8 % [25.7, 42.2] | 26.0 % | 2 % |
| full budget, seed 777 | 50 | 36.9 % [28.6, 45.1] | 36.3 % | 4 % |
| **pooled (3 seeds)** | **150** | **37.8 % [33.1, 42.7]** | 34.5 % | 2.7 % |
| static trajectory ideally corrected at septum exit (seed 42) | 50 | 43.9 % [35.8, 52.2] | 40.8 % | 2 % |
| no booster centroid jitter (seed 42, first 30) | 30 | 54.5 % [43.7, 64.6] | 64.5 % | 3 % |
| 3× all errors (seed 9) | 10 | 2.4 % [0, 6.8] | 0 % | 0 % |
| zero-error realization | 1 | 88 % | — | — |

Paired with the uniform-dipole control (seed 42, identical beams): dipole 59.3 %, field map −16.5 percentage points
[−22.2, −11.1]. Paired against the full-budget seed-42 realizations: static-orbit correction +1.1 ± 2.8 points;
removing booster jitter +11.2 ± 4.1 points.

## Drivers

Spearman rank correlation with capture (pooled 150): |injected-orbit x error at septum| ρ = −0.50, |angle error|
ρ = −0.50, |booster angle jitter| ρ = −0.42 (all p < 10⁻⁷); magnet strength errors, NKM scale and septum position are
not significant. The BTS transmits the booster jitter (0.5 mm, 0.2 mrad rms) into 0.65 mm and 0.33 mrad rms at the
septum exit (static orbit corrected), comparable to the ≈ ±0.5 mrad angular window of the operating point; capture
falls from 56 % for |Δx′| < 0.25 mrad to 13 % for 0.5–1 mrad (seed 42).

## Stored beam under errors (bicubic map, recomputed per realization)

Centroid amplitude: median 0.10 σ_x, p95 1.75 σ_x, max 6.4 σ_x; filamented emittance growth median 0.2 %, p95 5.4 %
(pooled 150). Dominated by NKM–orbit offsets (σ = 0.2 mm each). The values recorded during the runs with bilinear
interpolation (median 0.58 σ_x) are an upper bound.

## Conclusion for the article

At the selected operating point the NKM window is too narrow for the assumed booster extraction jitter: mean capture
≈ 38–44 % with or without static orbit correction. Static magnet errors are secondary; the injected-orbit jitter is
the limiting tolerance. The NKM remains far more transparent than a uniform kicker under the same errors.
