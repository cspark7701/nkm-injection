# Milestone 288 — R5-BTS-05: origin of the lower phase-advance edge

Completed: 2026-10-31. Round-5 task R5-BTS-05 (Reviewer 2 R2D-04).

**Study.** `results/bts_round5_campaign_20261031/edge_study`, declared in `round5_protocol.json`.
- **Search:** SLSQP minimising μ_x subject to the six exit equalities, the K bounds and both peak betas ≤ 60 m.
- **Starts:** three per target — the configured edge solution, the dispersion-free best and the round-3 robust
  setting.
- **Targets:** the configured Courant–Snyder parameters with these exit (D, D′):

| D [mm] | D′ [mrad] | Lowest matched μ_x | Status |
| ---: | ---: | ---: | :--- |
| 80.9 | 47.5 | 200.17° | converged; no bound or peak limit active |
| 80.9 | 32 | 194.94° | iteration limit; same value from all starts; nothing active |
| 80.9 | 16 | 189.52° | same |
| 80.9 | 0 | 184.14° | same (one start unmatched) |
| 0 | 47.5 | 203.23° | converged; vertical 60 m limit active |
| 0 | 0 | 187.21° | iteration limit; nothing active |

**Finding.** Within these local searches, the lower edge is set by the exit dispersion slope D′: about 5.3° per
16 mrad. Removing D at the configured D′ raises the edge.

**Article.**
- **Section 4.3:** the edge study, with its termination caveats.
- **Section 4.4:** the inherited D′ also limits how far the loss-based setting can move jitter from the blade.
- **Discussion:** the edge is attributed to the inherited exit dispersion slope, replacing "which no strength bound
  or peak-beta limit sets".

No global proof is claimed. The prose follows the humanizer rules. The isolated build is clean. Protected files are
unchanged.
