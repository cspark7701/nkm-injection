# Round 4 (F6): septum dispersion and the scope of the thin-map accuracy result

Script: `scripts/analyze_round4_dispersion_scope.py`; output: `results/journal_campaign_05/f6_dispersion_scope.json`.

## Dispersion at the septum exit (adopted model)

The injected beam carries D = 80.868 mm and D′ = 47.472 mrad, with σ_δ = 1.06 × 10⁻³. The ring dispersion at the
kicker is about 0.3 mm.

| Term | Size | Divergence |
| :--- | ---: | ---: |
| Betatron (ε_x = 7.67 nm rad) | 134 µm | 57 µrad |
| Dispersive (within bunch, D σ_δ and D′ σ_δ) | 86 µm | 50 µrad |
| Total rms | 159 µm | 76 µrad |
| Shot energy jitter 0.1 % (centroid, per shot) | 81 µm | 47 µrad |

- The dispersive term is two thirds of the within-bunch angular spread, and the energy jitter adds a 47 µrad
  shot-to-shot angle.
- Both are set by the inherited BTS exit target, not by the ring.
- The companion BTS study finds a dispersion-free exit feasible on the unchanged BTS lattice: 115 matched solutions,
  peaks below 60 m, μx 187.7–214.2°.
- Its best setting lowers the predicted blade loss but raises the exit-angle jitter to 0.39 mrad.
- That result is BTS-only and analytic. It is **not** imported into NKM capture here; validating it would require
  rerunning the capture study with that injected beam.

## Scope of the thin-map accuracy result

The round-3 fit |Δp_x|/|K| ≈ 1.95 η^1.46 uses a **synthetic diagnostic launch**:
- centroid at the kick extremum, with momentum opposite to the kick;
- y = 1 mm, y′ = 0.2 mrad;
- S = 0.85 family scan over two wire families.

It is an empirical description of that launch, not a universal law, and not the error along a production
trajectory. Along the **production** matched trajectories (centroid launched on its straight-line chord at the magnet
centre, exact 640-slice filament reference):

| Point | Centroid at centre | Thin − 3-D Δp_x, y = 0 | Thin − 3-D Δp_x, y = 1 mm | Sliced − 3-D |
| :--- | ---: | ---: | ---: | ---: |
| Current (S 0.95) | −7.443 mm | +161 µrad | +148 µrad | 8×10⁻⁸ rad |
| Earlier (S 0.85) | −8.521 mm | −35 µrad | −54 µrad | 1×10⁻⁸ rad |
| Extremum-centred (S 0.95) | −8.500 mm | −47 µrad | −69 µrad | 9×10⁻⁹ rad |

**Reading.**
- At the current point the matched centroid crosses the steep inner flank. There the production thin-map error
  (161 µrad) is 2.3 times the synthetic-launch value (69 µrad) and 3.7 times the declared allowance of 0.044 mrad
  (one tenth of that point's angular window).
- Near the extremum the production error is smaller (35–47 µrad). The allowance there depends on the window at that
  point (F3/F7).
- The sliced vector map agrees with the exact field to better than 10⁻⁷ rad at every point.
- The finite-length conclusion therefore holds more strongly at the current point than the fit suggests. Its size is
  point- and launch-dependent, and statements must name the launch.
