# Milestone 241 — F2: paired error-class ablation at zero booster jitter

Completed: 2026-10-20. Round-4 task F2 (R1D-01, R2d-1) of the
[round-4 plan](../../paper/reviews/consolidated_revision_plan_round4.md); note:
[round4_ablation.md](../../paper/round4_ablation.md).

**Runs.** 15 ensembles (`results/journal_campaign_05/f2_*`; not committed):
- all-off, plus each of the 7 declared classes alone and omitted;
- each 50 seed-42 realizations × 200 particles × 500 turns, paired with the E7 full zero-jitter reference
  `e7_jitter_0`.

**Interruption.** The machine rebooted on 2026-10-19 (memory exhausted with 8 workers). The driver resumed with 6
workers under the `pyat-dev` interpreter. Completed ensembles were skipped and the partial one passed the
checkpoint input/code signature. The worker count does not enter the results.

**Results** (NKM / dipole, points):
- All-off: 79.5 / 84.5. Full zero-jitter budget: 40.1 / 68.5.
- BTS magnet errors alone: −39.2 / −14.5, gap −24.7; when omitted: −36.4 / −14.1. Every other class is ≤ 1.7 points
  either way.
- Non-additivity: +3.5 (NKM), +0.2 (dipole).
- About 5 points of the 28-point gap are already present at all-off.

**Post hoc.**
- The horizontal-only ideal steering leaves a 0.90 mm / 77 µrad rms vertical centroid at the septum.
- NKM capture falls with |y| (ρ −0.88; dipole −0.52), consistent with F5's first-turn vertical losses.

**Consequence for F8.** The claim that the loss is "chiefly booster angle jitter" is withdrawn. BTS magnet errors,
acting through the uncorrected vertical centroid, drive the zero-jitter loss and the NKM-specific gap. Booster jitter
is a separate effect of about 20 points that costs both kickers equally.

**Files.**
- `scripts/analyze_round4_ablation.py` (with the post hoc exit-state check);
- `tests/test_round4_protocol.py`, new test of the estimands and the pairing guard (9 tests pass);
- `docs/paper/round4_ablation.md`;
- the round-4 plan, F2 marked Done.
