# Milestone 230 — R2B-06: Sensitivity to the roll and energy-jitter levels

Completed: 2026-10-15. Reviewer 2 BTS task R2B-06.

**Run** (stage `sensitivity`).
- 200 fresh machines × 3 shots (seeds 93001–93004), amended steering.
- Reference, low-beta and loss-based settings.
- Rolls of 0.1, 0.2 and 0.5 mrad rms × shot energy jitter of 0.05 and 0.1 %.
- Analytic Gaussian loss and five-sigma clearance (validated against tracking within 1 % in R2B-03/04).

**Result.**
- The roll level changes the predicted loss by 0.000 percentage points. Rolls couple a small part of x into y (blade
  rms size changes by 3×10⁻⁶ relative) and the vertical restrictions keep millimetres of clearance.
- Halving the energy jitter lowers the reference loss from 1.47 % to 1.44 %; its exit term (81 µm) is small next to
  the betatron jitter.
- The ranking is unchanged at every level.
- The loss-based gain varies between populations: a factor of 8.4 here against 3.5 on the tracked test. Its sign does
  not change.
- On the tracked test, the five worst of 200 machines carry 39 % of the reference loss. The worst loses 51 % per shot,
  through single shots with 2–3σ entrance jitter, not steering failures.

**Manuscript.**
- New Results 4.5 with Table 6.
- Heavy-tail statement in 4.3.
- Section 2.4 now cross-references the sensitivity section.

**Tests** (13 pass): with an exit centroid 0.3 mm inside the blade, the horizontal blade loss probability is the same
within 5 % for 0.1- and 0.5-mrad roll draws.
