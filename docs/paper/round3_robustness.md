# Round 3: the single robustness rerun (E7)

> Review-status annotation, 2026-10-16: these are the executed E7/E8 records. Their attribution of the
> NKM-specific deficit chiefly to booster angle jitter is challenged by both round-4 reviews: the paired
> NKM–dipole gap is already 28.33 points without jitter and 28.79 points with full jitter (seed 42).
> No individual non-jitter cause is established by this annotation. The original numerical records and
> interpretation below are retained pending [F2/F8](reviews/consolidated_revision_plan_round3.md#round-4-follow-up-to-the-round-3-manuscript);
> neither scientific revision has been executed.

**Inputs.**
- the selected operating point (E6; x_inj −19.48 mm, S 0.95);
- the corrected ring population (E5);
- the declared chamber with the in-magnet NKM chamber (E4);
- the round-2 error budget, unchanged.

The populations are unchanged from round 2:
- 3 seeds × 50 joint machine/shot realizations;
- 200 particles, 500 native turns;
- a jitter scan on the 50 seed-42 realizations, with paired sample, particle and ring identities;
- tuning on the same 50 static machines.

Ring identities per realization equal round 2 (same seeded draw).

Drivers:
- `scripts/run_round3_campaign.py`;
- `run_capture_robustness.py` (chamber passed to both models; controls calibrated at the point);
- `analyze_round2_robustness.py --prefix e7` (ring-cluster bootstrap and leave-one-ring-out added);
- `run_round3_tuning.py` (matched knobs).

**Joint errors (150 realizations).**

| | 3-D NKM | Dipole control |
| :--- | ---: | ---: |
| Mean (realization 95 % CI) | 16.1 % [12.0, 20.4] | 44.1 % [38.7, 49.6] |
| Ring-cluster 95 % CI | [10.9, 21.5] | [35.1, 52.9] |
| Leave-one-ring-out range | 14.9–17.4 % | 42.2–46.8 % |
| Median / p10 | 0.0 / 0.0 % | 50.8 / 0.5 % |
| Realizations ≥ 80 % | 5.3 % | 20.7 % |

The paired NKM − dipole difference is −28.0 [−32.5, −23.5] points. In round 2 (orbit-only rings, round-2 point) the
values were NKM 14.8 % and dipole 22.5 %: the corrected rings and new point doubled the dipole result but barely
moved the NKM.

**Booster jitter** (paired against zero jitter; one-sided noninferiority against the declared 1-point margin):

| Jitter scale | NKM mean | Paired difference [95 %] | Noninferior |
| :--- | ---: | :--- | :---: |
| 0 | 40.1 % | — | — |
| 0.25 | 34.4 % | −5.7 [−9.4, −2.5] | no |
| 0.5 | 28.8 % | −11.4 [−17.0, −6.0] | no |
| 0.75 | 24.0 % | −16.2 [−22.8, −9.6] | no |
| 1 | 19.5 % | −20.7 [−28.2, −13.6] | no |
| position only | 31.2 % | −8.9 [−13.6, −4.6] | no |
| angle only | 23.3 % | −16.8 [−24.0, −10.2] | no |

The dipole falls from 68.5 % to 48.2 % over the same range. Even quarter jitter now costs a resolved 5.7 points.
Booster angle is the only Holm-significant partial association (ρ = −0.38, p_Holm = 3×10⁻⁴).

**Matched tuning** (50 machines, 100 training particles, held-out 200):
- **Gain.** +11.9 [+8.0, +16.3] points at zero jitter (tuned mean 52.1 %) and +11.0 [+7.0, +15.4] at quarter jitter
  (45.4 %).
- **Search.** Median 13 evaluations per machine.
- **Bounds.** 28 % of the machines end on the outer x_inj bound, 1.5 mm beyond the clearance limit. They prefer a
  larger injection offset, away from the septum, and the declared range truncates them. No machine ends on the
  angle-trim or field-scale bounds.

**Interpretation** (developed in E8). Without injection errors, the NKM and dipole capture alike on the corrected
rings (E6 validation: 78.0 % against 82.2 %). Under the joint budget the NKM loses far more, because its 80 % angular
window at this point is only 0.44 mrad, comparable to the 0.2 mrad rms booster angle jitter plus the other angle
errors. The E6 objective excluded injection errors and so favoured a point with a narrow angular window.

Evidence: `results/journal_campaign_04/e7_*`, `e7_final_statistics.json`, `e7_tuning/`.
