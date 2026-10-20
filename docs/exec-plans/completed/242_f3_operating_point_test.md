# Milestone 242 — F3: paired operating-point test; current point retained

Completed: 2026-10-20. Round-4 task F3 (R1D-02, R2d-2) of the
[round-4 plan](../../paper/reviews/consolidated_revision_plan_round4.md); note:
[round4_points.md](../../paper/round4_points.md).

**Runs.** 4 ensembles (`results/journal_campaign_05/f3_*`; not committed):
- the earlier point (S 0.85) and the extremum-centred point (S 0.95);
- each at zero jitter and at the full budget, 50 seed-42 realizations each;
- paired with the E7 current-point ensembles, with the dipole control recalibrated at each point.

**Decision.** The current point (x_inj −19.478 mm, S 0.95) is retained under the declared rule:
- neither candidate's full-budget NKM gain is resolved: +2.9 [−4.7, +10.4] and +2.1 [−5.7, +9.7];
- both fail the 1-point zero-jitter margin.

**Finding.**
- NKM capture is flat across points, within ±3 points.
- The dipole control loses 17–23 points at both candidates, so the NKM-minus-dipole gap falls from about 28 to 7–9
  points. The gap is point-dependent and must be quoted with its point.
- A plausible reason, not tested: the centroid amplitude in the ring after the kick is 8.5 mm at the candidates
  against 7.44 mm at the current point.

**Files.**
- `scripts/analyze_round4_points.py` (decision rule as `meets_rule`);
- `tests/test_round4_protocol.py`, new rule test (10 tests pass);
- `docs/paper/round4_points.md`;
- the round-4 plan, F3 marked Done.

**Next.**
- The declared vertical-steering sensitivity (two-plane ideal static steering) at the current point.
- Then F7 at S = 0.95.
