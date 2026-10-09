# Milestone 108 — Journal Task 004: calibrated controls and coupled operating region (S6)

Completed: 2026-10-09. Task: [004](../../jinst-paper/tasks/004_calibrated_controls_and_coupled_injection.md).

Implemented `scripts/run_injection_operating_region.py` (S6): coupled booster→BTS→septum handoff (matched and baseline
BTS), angle matching per (x_inj, field scale) with inner-root selection and explicit infeasible points, paired
`fieldmap`/`off`/`dipole`/`linear` models on identical particles, linear-map cross-check, replicate stage. Added a bicubic
kick-map option used for the stored-beam response (bilinear interpolation overstates the cubic near-axis field) and tests
(`tests/test_operating_region_driver.py`, `tests/test_injection_study.py`). Results: [`operating_region.md`](../../jinst-paper/operating_region.md).

Findings: kicker off captures 0 %; best capture where the matched centroid sits at the kick-map extremum; operating point
x_inj = −20 mm, S = 0.85, x′ = 4.869 mrad: 91.1 % mean over four 500-particle bunches versus 94.6 % (dipole) and 96.3 %
(linearised) with the identical beam; stored-beam centroid 5×10⁻⁶ σ_x aligned (0.10 σ_x at 0.2 mm, 1.5 σ_x at 0.5 mm
magnet offset) versus 2.5×10³ σ_x for the dipole; baseline BTS optics 26.9 %; angle window ≈ ±0.5 mrad, asymmetric.
The original off/ideal/linear/fieldmap results are explained as artifacts of the linear map and uncalibrated controls.
