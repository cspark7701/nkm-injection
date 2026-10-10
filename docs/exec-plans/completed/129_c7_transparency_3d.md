# Milestone 129 — C7: Stored-beam transparency from the exact field

Completed: 2026-10-10. Consolidated task C7 (R1-07, R2-8).
- Drivers: `scripts/analyze_transparency_3d.py` (deterministic, single pass) and `scripts/track_stored_beam_3d.py`
  (multi-turn tracking).
- Raw data: `results/journal_campaign_02/c7_transparency/transparency_analytic.json` and
  `stored_beam_tracked.json` (not committed).
- Stored beam: ring equilibrium ε_x = 61.6 pm rad and σ_δ at the NKM centre, with ε_y = 0.1 ε_x assumed.
  Field scale S = 0.85; exact filament field.

**Symmetry.** On the midplane the kick is odd in x, and its near-axis expansion is purely cubic, with
c₃ = 2.4×10⁴ rad m⁻³. For an aligned kicker and a centred Gaussian beam the centroid kick is therefore exactly zero:
Gauss–Hermite quadrature gives 9×10⁻¹⁶ σ. The 5×10⁻⁶ σ quoted in campaign 01 equals the Monte Carlo standard error of
its 10⁵-particle sample. The bicubic map interpolation agrees with the exact field to 9×10⁻¹¹ rad near the axis;
bilinear interpolation errs by 10⁻⁶ rad and overstates the 0.1 mm response 19-fold.

**Offset response.** Single pass, deterministic. The three response quantities are reported separately:
- A/σ is the centroid amplitude;
- Δε/ε is the growth from the kick spread about the displaced centroid;
- the total is 1 + A²/2 + Δε/ε once the centroid oscillation has filamented.

| NKM–orbit offset | A_x/σ_x | Δε/ε (kick spread) | Total (filamented) |
| ---: | ---: | ---: | ---: |
| 0.1 mm | 0.016 | 9.4×10⁻⁵ | 1.000 |
| 0.2 mm | 0.10 | 1.2×10⁻³ | 1.007 |
| 0.5 mm | 1.54 | 4.2×10⁻² | 2.22 |
| 0.2 mm vertical | A_y/σ_y = 0.17 | — | — |

**Tracked check.** 300 particles, seeds 11 and 12, 1000 turns, 6-D ring with RF and radiation, one passage through the
3-D magnet. The particles are paired with an unperturbed reference run, so the sampling noise of the centroid cancels.

| Offset | A_x/σ_x | ε_x ratio at turn 1000 | ε_y ratio | Lost |
| ---: | ---: | ---: | ---: | ---: |
| 0 | ≤ 1×10⁻⁴ | 1.000 | 1.000 | 0 |
| 0.2 mm | 0.098 | 1.009 | 1.001 | 0 |
| 0.5 mm | 1.47 | 2.23 | 1.009 | 0 |

Tracking agrees with the single-pass estimates:
- the amplitudes are 4–6 % lower, because the thick magnet path differs from the straight-line integral;
- the 0.5 mm emittance ratio, 2.23, matches the predicted 2.22, so the oscillation has filamented within 1000 turns;
- at 0.2 mm the ratio of 1.009 is within 0.002 of the prediction;
- the aligned residual, ≤ 10⁻⁴ σ, is the finite-sample cubic moment of 300 particles, not a physical kick.

**Conclusion and tolerance.** The NKM–orbit alignment decides transparency. With 0.2 mm the disturbance is about 0.1 σ
and the emittance grows by about 1 %; at 0.5 mm the kicker is not transparent. Combined with C8, the pulsed-magnet
requirements are the alignment, the on-axis residual field and the pulse length.

**Manuscript.**
- §5 now separates centroid, kick-spread and filamented emittance, and states the tracked check.
- New builder macros: `Transp{One,Two,Five}Total` and `Tracked{Two,Five}{Amp,EmitRatio}`.
- Figure 7 (right) shows the tracked amplitudes.
- The controls remain labelled as hypothetical linear estimates.

**Builder and manifest changes in the same commit.** The robustness step of `build_revision_figures.py` now handles
two ensembles: without (`c5_*`, `c6_*`) and with ideal static orbit correction (`c5c_*`, `c6c_*`, macros `RobC*`,
`JitC*`). `make_revision_manifest.py` lists the corrected artifacts. Results follow in milestone 128.
