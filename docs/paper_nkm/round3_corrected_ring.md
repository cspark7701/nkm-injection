# Round 3: corrected ring population (E5)

**Why the change (Reviewer 2, round 3).** The round-2 population stopped its orbit correction at a declared 100 µm
rms criterion and applied no optics correction. It left 3–11 % rms β-beat, up to 103 µm closed orbit at the NKM, and
one outlier ring (5501) whose first unstable horizontal launch was −7.5 mm. Its round-2 log shows that a 20 µm target
had already floored at 65–80 µm with unsaturated correctors. That floor came from steering to the design axis at the
BPM markers while the magnets are displaced.

**Same error draws.** `apply_errors` is called with seeds 5501–5510 and the same staged ten-step ramp, so the ring
identities and the per-magnet errors equal round 2:
- 30 µm girder and 30 µm magnet offsets;
- 100 µrad rolls;
- 0.05 % gradient and 0.1 % sextupole errors;
- 10⁻⁴ skew components.

**Correction chain** (`scripts/run_round3_corrected_ring.py`, `ring_error_scenario.py`):
1. **BPM references.** Each BPM reads the orbit relative to its nearest quadrupole centre along s, as after
   beam-based alignment, with a 10 µm rms Gaussian residual per plane (declared assumption).
2. **Orbit.** Truncated-SVD orbit correction with the 120 HVC correctors (cutoff 10⁻³ of the largest singular value,
   ±1 mrad bound), iterated until the larger-plane rms improves by less than 1 % per iteration.
3. **Optics.** β-beat (x, y) and weighted horizontal-dispersion correction at the BPMs, using all 344 individual
   quadrupole gradients. The method is Gauss–Newton on a fixed forward-difference Jacobian (step 10⁻⁴ m⁻²), with SVD
   cutoff 10⁻² and changes bounded to 1 % of each gradient per step. Three steps are taken, each accepted only if the
   rms observable decreases.
4. **Tunes and final orbit.** Bounded Q11/Q12 tune correction to the ideal tunes, then a final converged orbit
   correction.
5. **Coupling.** Not corrected: the lattice has no skew correctors (author input B1, default).

**Results** (all ten seeds pass: no saturated corrector, tune fit within tolerance):

| Quantity | Round 2 (orbit only, 100 µm rule) | Round 3 (full chain) |
| :--- | :--- | :--- |
| rms β-beat at BPMs, larger plane | 4.3–10.5 % | ≤ 2.0 % |
| β_x at the NKM | 15.1–17.7 m | 15.8–16.3 m |
| Closed orbit at the NKM (x) | up to 103 µm | ≤ 56 µm |
| BPM orbit rms rel. quadrupoles (x / y) | — | 69–83 / 49–63 µm |
| First unstable launch (septum only, 500 turns) | −10.0 to −7.5 mm | −11.0 to −9.5 mm |
| Ring 5501 | −7.5 mm | −10.5 mm |

The orbit floor of 70–80 µm relative to the quadrupole references persists with unsaturated correctors. It reflects
the 120-corrector system of the supplied file, about four per cell for 288 BPMs, not a stopping rule. If the KLS
design has additional correctors, such as sextupole trim windings, the floor would be lower.

The final fractional-tune residuals after the last orbit pass are below 3.5×10⁻⁵, slightly above the 10⁻⁵ tolerance
of the tune fit that precedes the final orbit correction.

**Ring 5501 diagnosis.** Its round-2 collapse came from uncorrected optics: β-beat 5.6/6.1 % rms, 19/22 % peak. With
optics correction it reaches −10.5 mm like the others. The remaining DA differences between rings are within about
1.5 mm.

**Scope.** This is a declared scenario with an explicit correction model, not an as-built or commissioned KLS
prediction. It replaces the round-2 population for all round-3 capture studies (E6, E7).

Reproduction:

```bash
python scripts/run_round3_corrected_ring.py --study-config results/journal_campaign_03/operating_point_design_beam.json \
  --output-dir results/journal_campaign_04/<new> --bba-residual-um 10 --workers 5
```
