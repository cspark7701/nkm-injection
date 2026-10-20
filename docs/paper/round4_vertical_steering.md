# Round 4 sensitivity: ideal static steering in both planes

**Declaration.** Declared in `docs/paper/round4_protocol.json` (`vertical_steering_sensitivity`) and committed before
the runs (0b2e6ed).

**Files.** Script: `scripts/analyze_round4_vertical.py`; output:
`results/journal_campaign_05/f2v_vertical_sensitivity.json`; ensembles `results/journal_campaign_05/f2v_xy_{zero,full}`
(driver stage `vertical`).

**Change.** At the septum exit, the static trajectory of the perturbed BTS is removed in both planes (x, p_x, y, p_y)
instead of only horizontally.
- Like the production steering, this is an ideal downstream translation, not a magnet. The BTS lattice is unchanged.
- The production horizontal-only jobs still reproduce E7 bitwise.
- Point: the current point (retained by F3).
- Pairing: the same 50 seed-42 realizations, particles and corrected rings as `e7_jitter_0` and `e7_seed42`.

**Intervals.** Central 95 % percentile bootstrap over realizations (10 000 resamples, seed 1729). Units: percentage
points of capture.

**Role.** This is a sensitivity. The production x-only steering remains the headline model, and no capture gain is
claimed for the line as built.

## Capture (%)

| Budget | Steering | NKM | Dipole | NKM − dipole | NKM / dipole zero-capture | Exit y, y′ rms |
| :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| Zero jitter | x only (production) | 40.1 | 68.5 | −28.3 [−35.5, −21.1] | 0.18 / 0.02 | 0.90 mm, 78 µrad |
| Zero jitter | x and y | 76.6 | 82.6 | −6.1 [−8.9, −3.6] | 0.00 / 0.00 | 5 µm, 1 µrad |
| Full | x only (production) | 19.5 | 48.2 | −28.8 [−37.7, −20.1] | 0.46 / 0.12 | 0.90 mm, 78 µrad |
| Full | x and y | 33.9 | 57.2 | −23.3 [−31.7, −15.0] | 0.28 / 0.10 | 22 µm, 2 µrad |

## Paired effects (points)

| Contrast | NKM | Dipole | Gap |
| :--- | :--- | :--- | :--- |
| Two-plane gain, zero jitter | +36.4 [+28.1, +45.0] | +14.2 [+8.4, +20.8] | +22.3 [+16.0, +28.6] |
| Two-plane gain, full budget | +14.5 [+8.5, +21.4] | +9.0 [+5.4, +13.2] | +5.5 [−0.8, +11.9] |
| Jitter cost (full − zero), x-only steering | −20.7 [−28.2, −13.6] | −20.2 [−28.6, −12.7] | −0.5 [−8.8, +7.8] |
| Jitter cost (full − zero), two-plane steering | −42.7 [−51.4, −33.8] | −25.4 [−34.8, −16.6] | −17.2 [−25.4, −9.2] |
| Interaction (gain at full − gain at zero) | −22.0 [−30.3, −14.4] | −5.2 [−10.5, −0.8] | −16.8 [−22.7, −11.1] |

The full-budget jitter and the remaining error draws are those of `e7_seed42`. The zero- and full-budget ensembles
share their realizations, particles and rings, so the jitter costs are paired.

## Reading

- **The F2 attribution is confirmed.** At zero jitter, two-plane steering restores NKM capture to 76.6 %, which is
  exactly the value with the BTS magnet errors switched off (F2 `omit_bts_magnets`, 76.6 %). It also removes every
  zero-capture event. The whole BTS-magnet effect therefore acts through the static vertical centroid at the septum
  exit, which the production horizontal-only steering leaves uncorrected.
- **The remaining zero-jitter gap.** The gap of −6.1 points is close to the all-off value of −5.0. It belongs to the
  corrected rings and the nominal model.
- **The two NKM-specific losses overlap.** With production steering, booster jitter costs both kickers about 20
  points (gap −0.5). With the vertical error removed, it costs the NKM 43 points and the dipole 25 (gap −17.2
  [−25.4, −9.2]). The static vertical error and the booster jitter largely remove the same NKM shots: in the
  production model the vertical error already eliminates the shots that jitter would also eliminate.
- **Consequences for the attribution.** Each mechanism alone is NKM-specific, and the attribution depends on which
  is corrected:
  - in the production model, the uncorrected vertical centroid dominates;
  - once the vertical centroid is corrected, booster jitter is the dominant NKM-specific loss.

  The abstract must state both, with the steering model named (F8). These runs do not separate the position and
  angle components of the jitter. Under x-only steering, the F4 jitter rows give position-only jitter as the more
  NKM-specific term (NKM −8.9 against dipole −2.6 points).

## Jitter components under two-plane steering (declared extension, 8e8f628)

**Runs.** `f2v_xy_x_only` (booster position jitter 0.5 mm only) and `f2v_xy_xp_only` (angle jitter 0.2 mrad only).
- They are paired with `e7_jitter_x_only` and `e7_jitter_xp_only` on the same realizations.
- Costs are relative to `f2v_xy_zero`; under x-only steering they are relative to `e7_jitter_0`.

| Jitter | Steering | NKM | Dipole | Gap |
| :--- | :--- | :--- | :--- | :--- |
| Position only | x and y | −17.4 [−23.9, −11.2] | −2.6 [−5.8, −0.0] | −14.7 [−21.8, −8.2] |
| Angle only | x and y | −33.7 [−43.7, −24.3] | −20.5 [−29.4, −12.3] | −13.2 [−21.2, −5.8] |
| Position only | x only (production) | −8.9 [−13.6, −4.6] | −2.6 [−5.4, −0.1] | −6.3 [−12.0, −0.7] |
| Angle only | x only (production) | −16.8 [−24.0, −10.2] | −18.0 [−25.8, −11.0] | +1.2 [−5.7, +8.1] |

**Reading.**
- With the vertical error removed, both components are NKM-specific by similar amounts (gap −14.7 and −13.2 points).
- Position jitter acts almost on the NKM alone. Its kick depends on where the centroid crosses the magnet (steep
  inner flank at the current point), so a position error leaves the kicker as an angle error. The uniform kick has
  no such dependence.
- Angle jitter costs both kickers and the NKM more.
- Under production steering the angle component shows no NKM-specific cost, because the static vertical error
  already removes the affected NKM shots.
