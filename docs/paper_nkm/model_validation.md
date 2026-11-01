# Tracking-model validation and supported scope (Task 003, campaign S5)

Run: `results/journal_campaign_01/backend_validation/` (git-ignored), produced by
`scripts/run_tracking_backend_validation.py` with `config/injection_study_v1.json`, the selected
optimisation (coupled BTS beam), backends element/map, models off/fieldmap/dipole/linear,
200/1000 particles, 100/500/2000 turns, seeds 42/123/777, DA 500 turns, 4 workers, 1045 s.

## Dynamic aperture at the NKM centre (native, 500 turns, x′ = 0 relative to the closed orbit)

| δ | −3 % | −2 % | −1 % | 0 | +1 % | +2 % | +3 % |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| stable x range [mm] | −3…+3 | −9…+10 | −14…+14 | −12…+13 | −12…+13 | −6…+10 | −6…+8 |

1 mm grid; edge = last stable point before the first unstable one. The x–x′ scan (41×13 points)
has 130/533 stable points. At β_x = 16.27 m the on-momentum horizontal acceptance is ≈ 9 µm·rad.

## Native versus linear one-turn map (identical beams)

Provisional point x_inj = −20 mm, x′_inj = 5.75 mrad, field scale 1, 200 particles, 500 turns:

| Model | Native capture [95 % Wilson] | Linear-map capture | Discordant particles |
| :--- | :--- | :--- | ---: |
| off | 0 [0, 0.019] | 0 | 0 |
| fieldmap (seeds 42/123/777) | 0.440 / 0.440 / 0.415 | 0.625 / 0.630 / 0.615 | 37–40 |
| dipole (calibrated) | 0.415 | 0.845 | 86 |
| linear (calibrated) | 0.415 | 0.610 | 39 |

The linear map overestimates capture by 19–43 percentage points because it has no dynamic aperture;
it is therefore **not** used for capture claims. Small-amplitude agreement: after 1/10/100 turns the
relative x residual is ≤ 0.05 %/1.8 %/1.3 % for amplitudes ≤ 1 mm (chromatic and nonlinear detuning).

## Numerical convergence and limits

* Turns (1 seed, 200 particles): capture 0.565 / 0.495 / 0.46 / 0.44 / 0.44 / 0.43 after
  50 / 100 / 200 / 500 / 1000 / 2000 turns; 500 turns is within 1 percentage point of 2000.
* Particles: 0.440 [0.373, 0.509] with 200 versus 0.402 [0.372, 0.433] with 1000 (overlapping intervals).
* Chamber aperture ±12 × ±6 mm at every element: 0.405 versus 0.44 without (one-sided sensitivity).
* Zero field scale reproduces kicker-off exactly (coordinates and survival, zero tolerance).
* Stored beam: a 1 µrad uniform kick gives a tracked centroid of 15.68 µm versus β·Δx′ = 16.27 µm
  (3.7 % from turn sampling and chromatic decoherence). For the field map the paired tracked
  difference (0.70 µm) is dominated by finite-sample noise β·σ_k/√N; the analytic 10⁵-particle
  estimate (4.7 nm) is used.

## Supported model scope

Capture, loss and acceptance claims use native element-by-element tracking (6D, RF, radiation pass
methods, no ring errors), 500 turns, a thin NKM kick at the magnet centre and the septum blade as the
only ring aperture. Not established: a full momentum-acceptance study, chamber apertures of the
real machine, thick-NKM tracking in the ring, collective effects, and ring optics errors.
