# Round 4 (F4): signed and physical associations, zero-capture summaries and two-model jitter rows

Exploratory; the causal contrasts are F2. Script: `scripts/analyze_round4_associations.py`; output:
`results/journal_campaign_05/f4_associations.json`.

**Inputs.** No new tracking:
- the 150 full-budget E7 realizations (seeds 42, 123, 777), for the associations;
- the paired seed-42 jitter ensembles, for the jitter rows.

**Conventions.**
- Spearman rank correlation, asymptotic two-sided p, Holm adjustment within each response over the 11 listed
  predictors.
- Intervals: central 95 % percentile bootstrap over realizations (10 000 resamples, seed 1729). A one-sided test at
  its lower endpoint is a conservative 97.5 % bound.

**Physical predictor.** The centroid's betatron amplitude just after each kicker [m^1/2], normalised with the drawn
ring's NKM Twiss. It is computed from the realization's septum-exit centroid (after ideal static steering), every
shot error and the kicker itself, using the same geometry as the tracking. With all errors zero, the NKM centroid
leaves with zero angle (tested).

| Predictor | NKM ρ (p_Holm) | Dipole ρ (p_Holm) | NKM − dipole ρ (p_Holm) |
| :--- | :--- | :--- | :--- |
| Amplitude after the NKM | −0.60 (<10⁻¹⁴) | −0.43 (<10⁻⁶) | +0.04 (1) |
| Amplitude after the dipole | −0.37 (<10⁻⁴) | −0.70 (<10⁻²¹) | +0.52 (<10⁻¹⁰) |
| Signed NKM − orbit offset | **+0.26 (0.011)** | +0.17 (0.38) | +0.08 (1) |
| Signed booster x′ | +0.21 (0.073) | −0.02 (1) | +0.13 (0.90) |
| Signed booster x | +0.19 (0.10) | −0.12 (1) | **+0.28 (0.005)** |
| Energy, NKM scale, septum x/strength, β mismatch | |ρ| ≤ 0.14, not significant | | |

**Interpretation within the exploratory scope.**
- Capture follows the post-kick centroid amplitude for both models.
- The NKM spreads that amplitude more: mean 3.7 against 2.2 (×10⁻³ m^1/2), median 2.5 against 2.1, with a heavy
  tail.
- The excess correlates with the signed booster angle (ρ = −0.64 with the amplitude difference) and position
  (−0.42). Booster jitter in one direction pushes the centroid onto the inner flank of the kick.
- The NKM-specific signed offset term (+0.26) is invisible to the magnitude-based analysis of round 3.

**Zero capture** (150 realizations):

| | Zero-capture fraction | Mean | Conditional mean (capture > 0) |
| :--- | ---: | ---: | ---: |
| NKM | 51 % | 16.1 % | 33.0 % |
| Dipole | 10 % | 44.1 % | 49.0 % |

**Jitter rows** (seed 42, paired; differences from zero jitter in points, central 95 % intervals):

| Scale | NKM mean | NKM Δ | Dipole mean | Dipole Δ | NKM − dipole | NKM / dipole zero-capture |
| :--- | ---: | :--- | ---: | :--- | :--- | :--- |
| 0 | 40.1 | — | 68.5 | — | −28.3 [−35.5, −21.1] | 0.18 / 0.02 |
| 0.25 | 34.4 | −5.7 [−9.4, −2.5] | 66.9 | −1.5 [−3.0, −0.2] | −32.5 [−40.2, −24.8] | 0.28 / 0.00 |
| 0.5 | 28.8 | −11.4 [−17.0, −6.0] | 61.6 | −6.9 [−11.1, −3.4] | −32.8 [−40.9, −24.9] | 0.34 / 0.00 |
| 0.75 | 24.0 | −16.2 [−22.8, −9.6] | 54.9 | −13.5 [−20.2, −7.6] | −31.0 [−39.6, −22.6] | 0.44 / 0.06 |
| 1 | 19.5 | −20.7 [−28.2, −13.6] | 48.2 | −20.2 [−28.6, −12.7] | −28.8 [−37.7, −20.1] | 0.46 / 0.12 |
| x only | 31.2 | −8.9 [−13.6, −4.6] | 65.8 | −2.6 [−5.4, −0.1] | −34.6 [−42.2, −27.1] | 0.30 / 0.00 |
| x′ only | 23.3 | −16.8 [−24.0, −10.2] | 50.5 | −18.0 [−25.8, −11.0] | −27.1 [−35.4, −19.1] | 0.40 / 0.10 |

**Reading.**
- Full booster jitter costs both kickers about 20 points, and angle-only jitter costs the dipole at least as much as
  the NKM. Booster angle jitter is therefore **not** the NKM-specific loss.
- Position-only jitter costs the NKM more (−8.9 against −2.6).
- The NKM–dipole gap of about 28 points exists at zero jitter. Its causes are tested in F2.
