# Round 2 revision execution through D14

Started: 2026-10-12. Authorized scope: D1–D14 of the consolidated round-2 plan, using `docs/paper/dependent_answers.md`; stage-by-stage local commits in the established format. Push is explicitly authorized only after D14 passes. D15 remains outside this task.

Initial working tree: clean, HEAD `279a880`. Protected scientific inputs must retain their initial hashes. New results belong under `results/journal_campaign_03/`.

## Progress

- D1: complete; title, lattice version, preliminary NKM design and assumed septum distinguished from the KLS baseline. Isolated 13-page build and 3 submission-package tests pass.
- D2: complete. Fixed the duration macro; 4000-turn survival is 89.5% [87.4, 91.3], 1000 particles, seeds 1001/1002. Corrected quarter-minus-zero jitter is +0.30 points [-1.50, +2.15], 50 pairs, 10000 bootstrap resamples, seed 1729; a one-point margin is not established. All jitter levels analyzed; partial correlations Holm-adjusted. Clean 13-page build and 9 focused tests pass. Selected summary restored from the hash-verified bundle; adjacent config.json still requested for later simulations.
- D3–D14: pending. Independent D3 validation and D4 budget work can proceed while evidence is located. D3 must pass before new ring/capture simulations.

## Verification

Run status/diff checks before and after every stage, relevant tests and clean isolated builds. Archive each completed stage sequentially starting at 141 and update the completed index. Do not declare D14 complete or push while any required stage, numerical gate or evidence check remains incomplete.
