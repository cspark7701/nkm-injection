# Round 3: transparency observables, simultaneous construction errors and septum leakage (E9)

> Status 2026-10-16: The E9 results remain recorded. Point/strength consistency (earlier S=0.85 versus adopted S=0.95) is a pending F7 issue; no uniform rescaling of all moment observables is assumed here.
> See the [pending follow-up](reviews/consolidated_revision_plan_round4.md).

## Units of the aligned moment change

The aligned-beam moment changes reported in section 6 are **fractional** single-pass changes of the centred projected
emittance:

- Δε/ε = ε_after/ε_before − 1 = 4.5×10⁻⁷ (x) and 1.6×10⁻⁷ (y).
- They come from the kick spread across a centred Gaussian beam at the NKM. The method is Gauss–Hermite quadrature of
  orders 20, 40 and 60, using the exact one-pass determinant em² + em β Var(k) − Cov(q,k)².
- They are not absolute emittances and not beam-size changes.

They are also distinct from two other quantities:
- the filamented coherent contribution (1 + A²/2 + Δε/ε at an offset);
- the tracked turn-1000 emittance ratio. The tracked centroid amplitude is the maximum paired centroid difference over
  turns 1–50.

## Simultaneous wire-placement and loop-current errors

`scripts/analyze_round3_transparency.py` displaces all eight longitudinal wires simultaneously, with independent
Gaussian offsets in x and y of rms 10, 25 and 50 µm. The loop currents receive independent relative errors of rms 0
(series powering), 10⁻⁴ or 10⁻³. For each of 4000 deterministic-seed draws per case, the on-axis integrated kick
(exact filament kernel) gives the stored-beam centroid amplitude A/σ = |k| β/σ. This uses the NKM optics, ε_x =
61.6 pm rad and ε_y = 0.1 ε_x.

| Wire rms | Powering | A_x/σ median (p90) | A_y/σ median (p90) | Both planes ≤ 0.1σ |
| ---: | :--- | :--- | :--- | ---: |
| 10 µm | series | 2.6 (6.2) | 4.8 (11.7) | 0.03 % |
| 25 µm | series | 6.4 (15.8) | 11.9 (28.9) | 0 % |
| 50 µm | series | 13.2 (31.9) | 23.2 (57.1) | 0 % |

Independent loop-current errors of 10⁻⁴–10⁻³ change these values by a few percent at most; wire placement dominates.

**Consequence.** A four-loop magnet built to realistic tolerances is not transparent by geometry. Its static on-axis
dipole residual is several to tens of rms beam sizes and must be measured and compensated, for example by a trim
winding or a pulsed dipole corrector. SOLEIL needed active compensation for the same reason. No compensation design
is attempted here; the single-wire derivative tables (supplement) give its requirements.

## Septum leakage allowance

At the septum, 2.26 m upstream of the NKM centre, β_x = 15.9 m. A stored-beam centroid amplitude of 0.1 σ_x
corresponds to a dipole kick of 0.1 √(ε_x/β_x) = 197 nrad. Over the 0.4 m thin septum this is a uniform leakage field
of 0.066 G.

The published KLS baseline leakage, 3.3 G at the bumped orbit about 5 mm from the blade (Hahn et al. 2024), is 50
times larger. In the NKM scheme the stored orbit is about 16 mm from the blade, where the leakage has not been
published. The requirement, of order 0.07 G at the stored orbit, therefore has to be met by distance or shielding.
Measured against this allowance, the thick-septum shielded value of 0.3 ± 0.1 G over 1.7 m would also be too large if
it acts on the stored beam.

Evidence: `results/journal_campaign_04/e9_transparency_mc.json` (manifest key `round3_transparency_mc`).
