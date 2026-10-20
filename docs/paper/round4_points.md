# Round 4 (F3): paired operating-point test and adopted-point decision

Script: `scripts/analyze_round4_points.py`; output: `results/journal_campaign_05/f3_points.json`; ensembles
`results/journal_campaign_05/f3_{earlier,extremum}_{zero,full}` (driver `scripts/run_round4_campaign.py --stage
points_test`). The current point reuses the bitwise-reproduced E7 ensembles `e7_jitter_0` and `e7_seed42`.

**Candidates** (F1, `results/journal_campaign_05/points/points.json`; every candidate passes the septum-clearance and
matched-root checks):

| Point | x_inj | S | x′ | Centroid at NKM | Control k0 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Current | −19.478 mm | 0.95 | 5.319 mrad | −7.443 mm | −5.319 mrad |
| Earlier | −19.5 mm | 0.85 | 4.853 mrad | −8.521 mm | −4.853 mrad |
| Extremum-centred | −20.751 mm | 0.95 | 5.415 mrad | −8.500 mm | −5.415 mrad |

**Design.** Each point is run at the zero-jitter and full budgets, on the same 50 seed-42 realizations, particles and
corrected rings (pairing verified per realization). The dipole control is recalibrated to the 3-D centroid response
at each point.

**Intervals.** Central 95 % percentile bootstrap over realizations (10 000 resamples, seed 1729).

**Declared rule** (`round4_protocol.json`). A candidate replaces the current point only if both hold:
- its full-budget NKM gain over the current point has a paired lower endpoint above 0;
- its zero-jitter NKM paired lower endpoint is above −1 point (a conservative 97.5 % one-sided bound).

## Capture (%) and paired differences from the current point (points)

| Point | Budget | NKM | Dipole | NKM − dipole | NKM / dipole zero-capture |
| :--- | :--- | ---: | ---: | :--- | :--- |
| Current | zero jitter | 40.1 | 68.5 | −28.3 [−35.5, −21.1] | 0.18 / 0.02 |
| Current | full | 19.5 | 48.2 | −28.8 [−37.7, −20.1] | 0.46 / 0.12 |
| Earlier | zero jitter | 39.1 | 45.7 | −6.6 [−9.7, −3.7] | 0.14 / 0.02 |
| Earlier | full | 22.4 | 30.4 | −8.0 [−12.2, −4.1] | 0.34 / 0.18 |
| Extremum | zero jitter | 37.8 | 46.0 | −8.2 [−11.6, −5.1] | 0.16 / 0.04 |
| Extremum | full | 21.6 | 31.0 | −9.4 [−13.9, −5.2] | 0.34 / 0.18 |

| Candidate − current | NKM, zero | NKM, full | Dipole, zero | Dipole, full | Gap, zero | Gap, full |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Earlier | −1.0 [−6.8, +4.9] | +2.9 [−4.7, +10.4] | −22.8 [−28.9, −16.8] | −17.8 [−23.3, −12.5] | +21.8 [+14.8, +28.9] | +20.8 [+12.3, +29.7] |
| Extremum | −2.3 [−8.2, +3.6] | +2.1 [−5.7, +9.7] | −22.5 [−28.4, −16.6] | −17.2 [−22.6, −11.9] | +20.1 [+13.4, +27.0] | +19.4 [+10.7, +28.4] |

## Decision

**The current point is retained.** Neither candidate meets the rule:
- neither full-budget NKM gain is resolved (lower endpoints −4.7 and −5.7 points);
- neither zero-jitter interval excludes a loss larger than the 1-point margin.

The test was run on the seed-42 population. A change would have been a selection on that population, not a held-out
optimum, and retaining the point needs no such qualification.

## Reading

- **NKM capture is flat across the three points.** Every NKM difference is within ±3 points, and each interval
  spans zero.
- **The dipole control is not flat.** It loses 17–23 points at both candidates, so the NKM-minus-dipole gap shrinks
  from about 28 points to 7–9 points.
- **The gap is therefore point-dependent.** Most of the 28-point gap at the current point is a dipole-control
  advantage at that point, not a fixed NKM deficit. The manuscript must report the gap together with its point
  identity (F8).
- **Interpretation (not tested here).** Both candidates put the centroid about 1.1 mm farther from the stored orbit
  at the NKM: 8.5 mm against 7.44 mm.
  - The control is a uniform kick k0 that leaves the matched centroid with zero angle, so the injected beam
    oscillates with roughly that larger offset as its amplitude. A larger amplitude costs a dipole-kicked beam
    dynamic aperture.
  - The NKM's zero-jitter loss is set instead by the uncorrected vertical centroid (F2) and occurs on the first turn
    (F5). That would not depend on the horizontal offset.
  - The current point was chosen in E6 for the NKM. It sits on the steep inner flank of the kick (local slope
    +0.32 mrad/mm), whereas both candidates sit near the extremum (−0.09 and −0.11 mrad/mm).
- **Consequence for F7.** F7 is evaluated at the current point and S = 0.95.
