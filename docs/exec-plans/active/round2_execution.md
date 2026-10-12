# Round 2 revision execution through D14

Started: 2026-10-12. Authorized scope: D1–D14 of the consolidated round-2 plan, using `docs/paper/dependent_answers.md`; stage-by-stage local commits in the established format. Push is explicitly authorized only after D14 passes. D15 remains outside this task.

Initial working tree: clean, HEAD `279a880`. Protected scientific inputs must retain their initial hashes. New results belong under `results/journal_campaign_03/`.

## Progress

- D1: complete; title, lattice version, preliminary NKM design and assumed septum distinguished from the KLS baseline. Isolated 13-page build and 3 submission-package tests pass.
- D2: complete. Fixed the duration macro; 4000-turn survival is 89.5% [87.4, 91.3], 1000 particles, seeds 1001/1002. Corrected quarter-minus-zero jitter is +0.30 points [-1.50, +2.15], 50 pairs, 10000 bootstrap resamples, seed 1729; a one-point margin is not established. All jitter levels analyzed; partial correlations Holm-adjusted. Clean 13-page build and 9 focused tests pass. Selected summary restored from the hash-verified bundle; adjacent config.json still requested for later simulations.
- D3: complete. Independent DOP853 reference, 8 cases, two-plane slice/span refinement and steering audit pass. Maximum momentum discrepancy 5.1e-10 rad; 11 focused tests and clean 13-page build pass.
- D4: complete. Separate septum-strength, RF-phase and arrival-time terms added with independent reproducible sampling, documented units and explicit assumptions. Design beam and final budget saved in campaign 03. 64 focused tests and clean 13-page build pass.
- Selected BTS config.json recovered from `evidence_bundle_test`, with matching recorded SHA-256; the complete feasible handoff is available.
- D5: complete. Ten seeded staged SVD orbit/tune correction scenarios pass their declared gates; residuals and native DA grids saved. The initial unattainable 20 µm trial is preserved; selected scenario acceptance is 100 µm, half the assumed 200 µm residual-orbit scale. 9 focused tests and clean 15-page build pass.
- D6: ideal-ring full 3 m IVU chamber-bracket and aperture scans running; corrected-ring extension follows D5.
- D7: complete. Thirty single-centroid scaling cases, second wire family and physical vector-map comparison; 8 focused tests and clean 14-page build pass.
- D8: pending final D5/D6 scenario.
- D9: complete. Both-plane wire/current sensitivities, 0.29–2.04 µm single-wire centroid limits, independent-loop relative limit 1.15e-4, finite-beam moment changes and 2 x 300-particle native tracking through 1000 turns. Amplitudes use ends of turns 1–50; emittance uses end of turn 1000. No tracked losses.
- D10: complete. Native observations replace linear rotation. Peak-phase maximum under the historical window allowance is 5.84 µs; no-return maximum is 5.332 µs, with a compatible 5.3 µs example. Timing, train variation and hypothetical eddy-current estimates are consistent. 9 focused tests and clean 15-page build pass.
- D11–D14: pending.

## Verification

Run status/diff checks before and after every stage, relevant tests and clean isolated builds. Archive each completed stage sequentially starting at 141 and update the completed index. Do not declare D14 complete or push while any required stage, numerical gate or evidence check remains incomplete.
