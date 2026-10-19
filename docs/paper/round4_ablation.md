# Round 4 (F2): paired error-class ablation at zero booster jitter

Script: `scripts/analyze_round4_ablation.py`; output: `results/journal_campaign_05/f2_ablation.json`; ensembles
`results/journal_campaign_05/f2_*` (driver `scripts/run_round4_campaign.py --stage ablation`).

**Design.** 15 new ensembles plus the E7 reference `e7_jitter_0` (the full zero-jitter budget):
- all-off;
- each of the 7 classes alone;
- each class omitted.

The error classes are declared in `docs/paper/round4_protocol.json`.

**Pairing.** Every ensemble uses the same 50 seed-42 realizations, the same 200-particle bunches and the same
corrected rings (verified per realization: beam seed and ring identity).
- A disabled class has its standard deviations set to zero, so its draws are still consumed and every other draw is
  unchanged (tested).
- All-off still contains the corrected ring errors, the ideal horizontal static steering at the septum exit and the
  nominal model.

**Estimands.**
- Alone effect = alone − all-off.
- Omitted effect = full − omitted.
- Non-additivity = (full − all-off) − Σ alone effects.

**Intervals.** Central 95 % percentile bootstrap over realizations (10 000 resamples, seed 1729), pointwise and not
multiplicity-adjusted. Units: percentage points of capture.

## Ensemble means

| Ensemble | NKM | Dipole | NKM − dipole | NKM / dipole zero-capture |
| :--- | ---: | ---: | :--- | :--- |
| All-off | 79.5 | 84.5 | −5.0 [−6.0, −4.0] | 0.00 / 0.00 |
| BTS magnets alone | 40.2 | 70.0 | −29.7 [−37.0, −22.4] | 0.20 / 0.00 |
| Full budget except BTS magnets | 76.6 | 82.6 | −6.0 [−8.7, −3.7] | 0.00 / 0.00 |
| Full zero-jitter budget (E7) | 40.1 | 68.5 | −28.3 [−35.5, −21.1] | 0.18 / 0.02 |

All other alone ensembles lie within 1.7 points of all-off. All other omitted ensembles lie within 0.7 points of the
full budget.

## Class effects (points)

| Class | Alone, NKM | Alone, dipole | Alone, gap | Omitted, NKM | Omitted, dipole | Omitted, gap |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| BTS magnets | −39.2 [−48.0, −30.5] | −14.5 [−21.7, −8.3] | −24.7 [−31.7, −17.7] | −36.4 [−45.0, −28.1] | −14.1 [−20.8, −8.4] | −22.3 [−28.7, −16.1] |
| Beam shape | −0.2 [−0.6, +0.3] | +0.1 [−0.3, +0.4] | −0.2 [−0.8, +0.4] | +0.2 [−0.4, +0.7] | +0.0 [−0.6, +0.6] | +0.1 [−0.7, +1.0] |
| Mean energy | −1.0 [−2.6, +0.2] | −0.7 [−1.4, −0.0] | −0.3 [−1.9, +1.1] | +0.3 [−1.3, +1.9] | +0.1 [−1.3, +1.4] | +0.2 [−2.0, +2.7] |
| NKM amplitude | −0.6 [−1.2, −0.1] | −0.2 [−0.6, +0.1] | −0.4 [−1.1, +0.2] | +0.1 [−0.6, +0.8] | −0.6 [−1.3, +0.0] | +0.7 [−0.1, +1.6] |
| NKM orbit and alignment | −1.6 [−3.1, −0.2] | −0.4 [−1.0, +0.2] | −1.2 [−2.6, +0.2] | −0.3 [−2.6, +2.0] | −0.5 [−1.8, +0.7] | +0.2 [−2.2, +2.7] |
| Septum | +0.1 [−0.6, +0.7] | −0.4 [−0.8, −0.0] | +0.5 [−0.3, +1.2] | +0.4 [−0.2, +1.0] | −0.1 [−0.7, +0.5] | +0.5 [−0.3, +1.3] |
| Longitudinal timing | −0.2 [−0.6, +0.2] | +0.0 [−0.2, +0.3] | −0.2 [−0.7, +0.2] | +0.5 [+0.0, +1.0] | +0.2 [−0.3, +0.8] | +0.2 [−0.4, +0.9] |

**Non-additivity.**

| Model | Total (full − all-off) | Σ alone | Difference |
| :--- | :--- | :--- | :--- |
| NKM | −39.3 [−48.2, −30.5] | −42.8 [−52.2, −33.4] | +3.5 [+0.8, +6.0] |
| Dipole | −16.0 [−22.9, −10.0] | −16.2 [−23.5, −9.7] | +0.2 [−1.7, +2.0] |
| Gap | −23.3 [−30.3, −16.5] | −26.6 [−34.2, −19.1] | +3.3 [−0.1, +6.6] |

The small NKM interaction (+3.5 points) is reported, not forced into an additive decomposition. Alone and omitted
effects agree for every class.

## Reading

- **BTS magnet errors cause the loss at zero jitter.** Errors in BTS quadrupole strength, offset and roll, and in
  dipole strength, remove 39 points of NKM capture and 14.5 of dipole capture. Together the other six classes change
  either model by at most about 2 points.
- **The same class causes most of the NKM-specific gap.** It explains 22–25 of the 28-point full-budget gap. The
  remaining ≈5 points are already present at all-off. That residual is a property of the corrected rings and the
  nominal model, not of any injection error.
- **Booster jitter is a separate effect.** It is excluded from this design and adds about 20 points of loss to both
  kickers (F4 jitter rows, full budget). Neither the zero-jitter loss nor the NKM-specific gap is "chiefly booster
  angle jitter"; the abstract must change (F8).

## Exit state left by BTS magnet errors (post hoc, exploratory)

This section is labelled exploratory: it is not part of the declared estimands, it is unadjusted, and it is an
association within one ensemble, not a causal split of the class.

The steering is ideal but horizontal only, so the horizontal static trajectory is removed.

| Septum-exit state (rms over realizations) | All-off | BTS magnets alone |
| :--- | ---: | ---: |
| Centroid x, x′ | 11 µm, 6 µrad | 11 µm, 6 µrad |
| Centroid y, y′ | 3.5 µm, 1.1 µrad | **0.90 mm, 77 µrad** |
| β_x, β_y, D | 0.14 m, 0.32 m, 10 mm | 0.14 m, 0.33 m, 11 mm |

- **The class acts through the vertical centroid.** Within the BTS-alone ensemble, capture falls with the vertical
  offset |y|:
  - NKM: Spearman ρ −0.88;
  - dipole: ρ −0.52;
  - |y′|: ρ −0.65 (NKM) and −0.37 (dipole).
- **Not through the horizontal plane or the optics.** The exit optics are unchanged within the 200-particle sampling
  noise, and |x|, |x′| and β_x show no association.
- **Consistent with F5.** F5 found that NKM zero-capture losses are first-turn and mostly vertical. A static vertical
  steering step, or a vertical alignment tolerance tighter than the present 0.1 mm quadrupole offset, is therefore
  the indicated remedy. It has not been simulated here, and no capture gain is claimed.
