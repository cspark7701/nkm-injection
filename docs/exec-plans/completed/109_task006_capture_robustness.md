# Milestone 109 — Journal Task 006: combined-error capture robustness (S7)

Completed: 2026-10-09. Task: [006](../../jinst-paper/tasks/006_combined_error_capture_study.md).

Implemented `scripts/run_capture_robustness.py` (coupled per-realization BTS tracking with optics, alignment, dipole-field,
beam, septum, NKM and closed-orbit errors; paired controls; zero-error, stress and ideal static-orbit-correction options)
and `scripts/analyze_capture_robustness.py` (pooled cluster statistics, Spearman ranking, bicubic stored-beam
recomputation). Ran 3×50 full-budget realizations, 50 static-corrected, 30 without booster jitter and 10 at 3× errors
(200 particles, 500 turns). Budgets reduced from the strategy's 500×5000 because native tracking costs ≈ 2.5 ms per
particle-turn; turn and particle convergence are documented in milestone 106. Tests: `tests/test_capture_robustness_driver.py`
(end-to-end tiny run with fixture `tests/fixtures/s7_optimization/`). Results: [`capture_robustness.md`](../../jinst-paper/capture_robustness.md).

Findings: pooled mean capture 37.8 % [33.1, 42.7] (zero-error 88 %); static-orbit correction does not help (43.9 %);
removing booster jitter raises capture to 54.5 %; 3× errors give 2.4 %. The injected-orbit jitter at the septum
(0.65 mm, 0.33 mrad rms from 0.5 mm/0.2 mrad booster jitter) against the ±0.5 mrad window is the limiting tolerance.
Stored-beam centroid under errors: median 0.10 σ_x (bicubic). Protected inputs unchanged; outputs under results/.
