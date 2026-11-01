# Final operating-point validation (D11)

The final validation uses the design booster beam, the matched BTS handoff,
the declared reference chamber and the fixed selected NKM point. Capture is
survival after a stated finite number of turns, not an operational efficiency.

## Ring backend and survival

`run_round2_validation.py` compares native nonlinear tracking with local affine
element maps at 500 turns. Each map is the native tangent about the six-dimensional
closed orbit. Closed-orbit entrance/exit translations, physical element lengths
and family order are retained. Because AT's `M66Pass` ignores aperture attributes,
zero-length drift checks explicitly enforce the physical apertures at map
boundaries. The incoming transport and 3-D NKM remain the same for both backends.
The comparison isolates nonlinear ring dynamics and is not a second production
capture model.

The small-perturbation one-turn check uses coordinates
`[1e-8, 2e-9, 1e-8, 2e-9, 1e-8, 1e-8]` relative to the closed orbit, in
`[m, rad, m, rad, relative momentum, m]`. The maximum measured discrepancy is
1.3635e-14, below the 1e-10 componentwise numerical gate; circumference agrees
within 1e-10 m. Synthetic rectangle/ellipse tests additionally establish that
the affine backend actually loses out-of-aperture particles.

Nominal native tracking extends seeds 1001/1002, 500 particles each, to 4000
turns. Its 500-turn particle masks must exactly match the D6 chamber result.
Shorter survival counts are reconstructed from the same first-loss records:
AT loss index t means loss during turn t+1. Upstream and creation losses remain
outside all survival counts. Counts at 100, 500, 1000, 2000 and 4000 turns are
therefore paired prefixes, not independent runs.

The two angular 80% crossings use offsets −0.517037 and +0.241277 mrad, from
linear interpolation of the refined design-beam scan. Fresh seeds 2001/2002
(500 particles each) test both edges and corrected ring 5501 through 4000 turns.
The degraded case is a saved corrected ring at nominal injection, not a
combined BTS/shot-error realization. It tests one degraded ring scenario.
The evidence is `d11_validation/validation_summary.json`; particle Wilson
intervals are conditional on each specified ring and configuration.

## Window and independent trajectory

The design-beam angle/position scan fixes the selected knobs. It initially
covers ±1.2 mm/mrad at 0.2 spacing, then extends any boundary still above 80%
in the same fixed steps, up to ±3.0. Crossing cells are refined once to 0.1
spacing. The initial positive position boundary did not bracket the threshold;
its extension reuses all completed cases and is recorded in the final summary.
No operating-point reselection occurs. The scan's particle intervals are not
confidence intervals for an interpolated crossing.

The independent DOP853 check was repeated at the final angular edges, with the
same nominal, vertical-offset/angle and energy-offset cases as D3. All eight
cases passed. Maximum 640-slice coordinate discrepancies are approximately
3.26e-11 m, 5.08e-10 rad, 2.90e-11 m and 5.06e-10 rad in x, px, y and py.
`d11_trajectory_final_edges.json` retains the adaptive-solver settings and
slice/span comparisons; `d11_edge_offsets.json` retains the scan-file hashes
and interpolation rule. The approximation remains paraxial even though the
filament field is evaluated in closed form.
