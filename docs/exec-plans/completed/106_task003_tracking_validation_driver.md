# Milestone 106 — Journal Task 003: tracking-backend validation (S5)

Completed: 2026-10-09. Task: [003](../../jinst-paper/tasks/003_tracking_validation_driver.md).

Implemented `scripts/run_tracking_backend_validation.py` (S5 CLI as in strategy 023 plus `--da-turns` and
`--chamber-half-x-mm`) and coupled-BTS helpers in `injection_study.py` (`booster_beam`, `track_bts`,
`beam_moments`, process ring cache, Wilson interval). Ran S5 into `results/journal_campaign_01/backend_validation/`
(39 jobs, 1045 s, 4 workers). Results and supported scope: [`model_validation.md`](../../jinst-paper/model_validation.md).

Key results: on-momentum DA −12…+13 mm at the NKM centre (500 turns); the linear one-turn map overestimates
capture by 19–43 percentage points on identical beams; capture converges in turns (500 vs 2000 within 1 point)
and particles (200 vs 1000 overlapping intervals); zero field equals kicker-off exactly; uniform-kick stored
response matches β·Δx′ within 3.7 %. Native tracking costs ≈ 2.5–3 ms per particle-turn per core, so production
budgets are 200 particles × 500 turns per point instead of 10⁴ × 10³ (justified by the convergence checks).

Tests: `tests/test_campaign_drivers.py` (parser contracts, job matrices, paired controls, post-processing bounds).
Protected inputs unchanged; all outputs under `results/`.
