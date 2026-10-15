# Milestone 228 — R2B-04: Jitter transfer, Gaussian loss and the loss-based setting

Completed: 2026-10-15. Reviewer 2 BTS task R2B-04 (M4).

**Physics** (`bts_round3.jitter_transfer`, `phase_advance`, `shot_averaged_loss`).
- With both ends matched, M = B₄ R(μx) B₁⁻¹. The quadrupoles act on the exit jitter only through the horizontal phase
  advance.
- The booster jitter (0.5 mm, 0.2 mrad) reaches the exit with 0.26–0.95 mm position and 0.12–0.41 mrad angle
  spread, in opposite phase.
- The Gaussian loss probability per aperture, and its shot average (summed beam-plus-jitter covariance, exact for
  linear transport), give a smooth loss-relevant objective.

**Reachable phase advance** (stage `phase`).
- 349 matched settings from 360 bounded random starts.
- μx spans only 200.2–232.0°; the reference sits at 211.8° and low beta at 210.8°.
- Shot-averaged blade loss falls monotonically towards the lower edge.

**Loss-based setting** (stage `robust`).
- SLSQP from three starts, all at the 200-iteration limit; only the pool-best start is feasible, improving it by 1 %.
- Selected: μx 200.2°, shot-averaged loss 0.27 % (reference 1.28 %).
- Exit jitter 0.506 mm against 0.643 mm, but exit-angle jitter 0.368 against 0.327 mrad (+13 %).
- Frozen before the test.

**Fresh test** (stage `test`, 200 steered machines, amended layout, seeds 92001–92004):

| Setting | Tracked loss | Change vs reference |
| :--- | ---: | :--- |
| Reference | 2.32 % | — |
| Low beta | 2.15 % | −0.17 [−0.38, +0.02] (unresolved) |
| Loss-based | 0.66 % | −1.66 [−2.42, −0.99] percentage points (factor 3.5) |

- Predictions are within 1 %.
- The mean minimum clearance changes by −0.013 [−0.030, +0.005] mm, unresolved: the earlier metric cannot see the
  loss reduction.

**Manuscript.**
- New Sections 3.2 (jitter transfer, Eq. 3) and 3.3 (Gaussian loss and design, Eq. 4).
- Results 4.3 with Table 4 and Fig. 4 (exit jitter versus μx with reachable intervals; predicted and tracked loss).

**Tests** (11 pass): the jitter transfer equals the map result for the reference, low-beta and loss-based settings;
the shot-averaged loss equals the mean over 400 sampled shots within 15 %.
