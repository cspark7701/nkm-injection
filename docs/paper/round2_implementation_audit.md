# Round 2 trajectory and static steering audit

## Independent trajectory reference

The adaptive DOP853 solver integrates the stated paraxial equations using the exact filament field, independently of the sliced map. Input/output AT coordinates are referred to the NKM centre. Positions and ct are m, canonical momenta rad, delta dimensionless. Both the reference and sliced tracker use x′=p_x/(1+delta), y′=p_y/(1+delta); this is not validation against the full nonparaxial Lorentz equations.

Reference rtol is 2e-11, componentwise atol 2e-13, maximum step 0.01 m. A tenfold tighter reference confirms solver convergence. Nominal, lower/upper angular window, y=1 mm, y′=0.2 mrad, their combination and delta=±0.002 are included. Slices 160, 320, 640 and 1280 and spans ±0.45, ±0.65 and ±0.9 m are compared in both planes. The slice update first changes p_x and uses that updated p_x in the longitudinal-field contribution to p_y; the adaptive reference evaluates both derivatives at the same state.

At 640 slices, maximum absolute discrepancies are 3.9e-11 m in x, 4.0e-10 rad in p_x, 2.9e-11 m in y and 5.1e-10 rad in p_y. Span refinement changes the four coordinates by at most 3.1e-14 in their canonical units. These pass the declared gate of 1% of a 0.1-sigma response in either plane (beta_x/y=16.27/5.60 m, emittance_x/y=61.6/6.16 pm rad); the momentum discrepancy is also far below 1% of the 0.74 mrad window. The integrator need not be changed. All cases, exit-coordinate differences, refinements and tolerances are saved in `results/journal_campaign_03/d3_trajectory.json`.

Reproduce with `.venv/bin/python scripts/validate_round2_trajectory.py --study-config results/journal_campaign_02/operating_point_3d.json --output results/journal_campaign_03/<new>.json`.

## Ideal static steering

For a perturbed BTS map T_e and its zero-input reference r_e=T_e(0), the algorithm transports every particle and then applies `(x, p_x, y, p_y, delta, ct) -> (x - r_x, p_x - r_px, y, p_y, delta, ct)`. Here `r_x` and `r_px` denote the first two components of the transported reference, not a fitted bunch centroid. This is an ideal downstream horizontal translation, not correction by actual BTS magnets. A lost reference now raises an explicit error.

The algorithm preserves shot-dependent booster position, angle and energy offsets, the beam covariance, vertical orbit offsets and static optics distortion. Kicker-to-orbit and septum offsets also remain. It does not remove the finite-sample bunch centroid or re-fit injection knobs. Small Twiss mismatch alone does not establish small capture loss.

Static machine draws: BTS gradient, dipole-field, transverse alignment and roll errors; Twiss mismatch; NKM placement; ring orbit offset; septum position. Shot-dependent draws: booster position/angle/energy, emittance and energy-spread variations, NKM amplitude and equivalent timing. D4 adds septum strength, RF phase and arrival time as separate shot-dependent draws. Each realization samples both classes once; the bootstrap estimates this joint distribution, not repeated shots on a fixed machine. Rank associations are conditional on that model.
