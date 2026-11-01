# Finite length scaling and map scope

The dimensionless parameter eta = |K| L / (8 w) compares the uniform-kick sagitta with the negative horizontal lobe's full width at half maximum w. Small eta is a heuristic criterion for neglecting trajectory displacement; it is not a universal capture law. The deterministic scan covers L=0.2, 0.35, 0.525, 0.75 and 1.0 m, integrated-strength scales 0.5, 1.0 and 1.5, and transverse wire scales 1.0 and 1.25. The second family is a scaled version of this filament geometry, not an independently optimized magnet design.

At every point, the centroid starts at the straight-line kick extremum with momentum opposite its horizontal kick, y=1 mm times the wire-family scale and y′=0.2 mrad. The comparisons are a single thin vector map, a 1280-slice vector map uniformly distributed over the wire length, and the 1280-slice exact 3-D filament field. Both maps include the physical vertical component. The vector kernel is independently tested against longitudinal integration of the exact field and the curl-free identity.

`results/journal_campaign_03/d7_generality/generality_scaling.json` records all six-coordinate exits, differences, widths, eta values and geometries. Figure 9 shows the horizontal momentum differences; the raw data contain both planes. A sliced vector map can retain self-deflection. A thin map approximates the path, and the original vertical sign was an input-convention error, not a limitation of vector maps. The sign of local vertical focusing depends on which flank of the horizontal kick lobe is sampled.

Capture controls are paired comparisons of model responses on identical particles, not optimized competing injection systems. The chamber diagnostic suggests transfer from horizontal oscillation to the vertical plane; without a resonance or normal-mode diagnosis this remains an interpretation rather than identification of a unique coupling mechanism.

## Round 3: normalised approximation error (task E3)

These are definitions, not new runs:
- **K** is the peak straight-line kick of each configuration.
- **w** is the FWHM of its negative horizontal kick lobe (9.4 mm for the nominal wires, 11.7 mm for the 1.25 family).
- **η = |K|L/(8w).** For a trajectory deflected uniformly by K over L, |K|L/8 is the sagitta of the circular arc
  relative to its chord, and the chord through the kick extremum is the thin-map reference path. The launch recipe is
  unchanged (above).

`build_revision_figures.py` (step `generality`) normalises each exit-momentum error by |K| and fits the thin-map
horizontal error over all 30 configurations. The fit gives |Δp_x|/|K| = 1.95 η^1.46, with a log-rms scatter of 3.4 %
and a largest deviation of 11 %. Fitted per wire family, the exponents are 1.47 and 1.45.

The vertical thin-map error scales as η^0.81, with 7 % scatter. It depends also on the vertical launch, so η
organises it less well. The 1280-slice vector map stays below 2×10⁻⁵ |K| in both planes.

**Declared accuracy allowance.** The allowance is one tenth of the 80 % angular-window width, the same convention as
the pulse allowance: 0.076 mrad for the round-2 window.
- At the nominal kick the fitted thin-map error reaches the allowance at η* ≈ 0.036.
- The nominal magnet (η = 0.034) uses 91 % of it: |Δp_x| = 0.069 mrad per pass, and |Δp_y| = 0.129 mrad at the
  stated vertical launch.
- The allowance follows the window, so the builder recomputes it when the window changes (E6/E7).

**Scope.** The statement covers this filament family and launch recipe; it is not a universal capture criterion.

Generated macros: `Gen*`. Figure 9 now plots normalised errors in both planes on log axes.
