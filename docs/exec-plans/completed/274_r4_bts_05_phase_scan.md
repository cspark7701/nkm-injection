# Milestone 274 — R4-BTS-05: phase-advance scan, edges and fresh test

Completed: 2026-10-31. Round-4 task R4-BTS-05 (Reviewer 1 R3-BTS-05; Reviewer 2 R2C-03).

**Computation.** `results/bts_round4_campaign_20261030/phase_scan_b` and `final_test_b`.
- **Protocol amendments,** recorded before the outputs they affect:
  - the first scan (16 starts, 3000 evaluations each) was stopped after 26 minutes because unreachable grid points
    exhaust the budget on every start. The rerun uses 6 pool starts plus 4 random starts and 600 evaluations;
  - `edge_best` was added to the test before the test ran.
- **Scan.** μ_x in 2° steps as a seventh matching condition, for both exits; per grid point, the matched solution
  with the lowest peak beta.
- **Edges.** SLSQP minimising and maximising μ_x subject to the six exit equalities, the strength bounds and both
  peak betas ≤ 60 m, from five pool starts per edge.

**Results.**
- **Configured exit, scan.** Matched settings are found from 202° to 232° on the grid.
- **Configured exit, lower edge.** 200.169°, reached by three converged searches with no strength bound and neither
  peak limit active, so it is set by the matching conditions within the bounds, as far as local searches show.
- **Configured exit, upper edge.** 232.03°, set by the 60 m limit in both planes.
- **Dispersion-free exit.** The edges are 187.2° and 214.5°; the upper edge is q22 at its upper bound.
- **Loss and phase.** The error-free blade loss depends on the setting through μ_x alone (Eq. 6): 0.37 % at 202°,
  4.1 % at 232° and 0.27 % at the edge. The peak beta varies independently (23–60 m).
- **Round-3 loss-based setting.** It is optically identical to the converged edge solution (Δμ_x ≈ 8 × 10⁻⁷°,
  peak within 0.02 m). It is now described as the best-found feasible setting at the lower edge.
- **Second fresh test** (200 realizations, seeds 96001–96005, tracked):

  | Setting | Tracked loss | Change from matched reference [pp] |
  | :--- | ---: | :--- |
  | Matched reference | 0.97 % | — |
  | Low beta | 0.86 % | −0.11 [−0.24, −0.01] |
  | Round-3 loss-based | 0.085 % | −0.89 [−1.47, −0.42] |
  | Grid best (202°) | 0.25 % | −0.73 [−1.20, −0.35] |
  | Edge | 0.13 % | −0.84 [−1.39, −0.40] |
  | Dispersion-free | 1 of 1.2 million particles | −0.97 [−1.64, −0.45] |

- **Reading-error effect.** The edge and round-3 settings have the same jitter-integrated loss (0.29 % and
  0.28 %). Their tracked difference comes from the reading errors seeded per setting and from the sampled jitter
  tail.

**Article.**
- Section 4.3 is renamed "Phase advance of the matched settings" and reports the found ranges, the edges and their
  constraints, the μ_x-only dependence of the loss, the best-found wording, and the second test.
- New Table 6 and Figure 5 (`figures/round4_phase_scan.pdf`, checked visually).
- The Figure 4 caption says "ranges found".
- The Discussion states the found range, the edge without an active bound, and a gain of 3 to more than 10 between
  populations.
- "Pins", "reach only" and "reachable" are removed.

The isolated build is clean (18 pages). Protected files are unchanged.
