# Milestone 229 — R2B-05: Exit target, divergence budget and a dispersion-free exit

Completed: 2026-10-15. Reviewer 2 BTS task R2B-05 (M5).

**Identity.** The m4 target equals the companion NKM study's injected beam (campaign-04 `study_config.injected_beam`,
all six values identical). m4 is the injection-septum exit; the companion transports this beam 2.26 m to the kicker.
The nonzero D/D′ (80.9 mm, 47.5 mrad) is inherited from the configuration, not derived from the ring (≈ 0.3 mm at
the kicker).

**Budget** (stage `exit`).
- Exit divergence: 57 µrad betatron plus 50 µrad dispersive (76 µrad total).
- Shot energy jitter adds 47 µrad and 81 µm; both are fixed by the target.

**Dispersion-free exit (D = D′ = 0, same Twiss).**
- All 115 matched solutions from 120 bounded starts keep both peak betas below 60 m (smallest larger peak 26.3 m).
- Reachable μx widens to 187.7–214.2°.
- Best setting (μx 187.7°, peaks 31.4/48.2 m): shot-averaged blade loss 4.1×10⁻⁵ on the full element-wise line,
  65 times below the configured-target loss-based setting.
- Its exit jitter is 0.350 mm and 0.394 mrad; the divergence falls to 57 µrad.
- The trade: angle jitter at the kicker (0.394 against 0.327 mrad) versus blade loss, to be decided with the ring.
- These figures are analytic; the dispersion-free settings were not tracked.

**Manuscript.**
- Section 2.1 and the Table 1 caption state the m4 identity and the inherited dispersion.
- New Results 4.4; Fig. 4 shows the dispersion-free reachable band.

**Tests** (12 pass): the selected dispersion-free setting matches the Twiss to 5e-5 and D, D′ to 2e-6, has
μx < 190°, and its blade loss is below 1 % of the reference's.
