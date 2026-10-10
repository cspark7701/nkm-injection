# Milestone 136 — Reviewer 2, second-round report on the revised manuscript

Completed: 2026-10-11. User request: review `docs/paper/` again as Reviewer 2, decide on acceptance, and write a report
with revision tasks without overwriting previous reviews.

**Output.**
- `docs/paper/reviews/reviewer2_report_round2.md`: new file. The round-1 report is unchanged.
- The reviews `README.md` gains a new row and a summary.

**Recommendation.** Major revision; no acceptance in the present form. The report records the status of all 20
round-1 tasks: 11 resolved, 7 partly, 2 not yet.

New major points:
- M1: the headline capture has no vacuum chamber. The manuscript's own scan gives 47.9 % at ±10 mm and 76.0 % at
  ±11 mm.
- M2: ring errors are only uncorrected.
- M3: manufacturing tolerances of transparency.
- M4: the pulse-length inconsistency.
- M5: beam-based injection tuning and the unsourced budget.
- M6: generality and novelty framing (sliced kick map, dimensionless criterion; vertical sign as a consistency check).
- M7: lattice version versus the KLS baseline.
- M8: the 500-turn headline and the provisional validation figure.

Revision tasks: R2b-1 to R2b-15, with priorities, acceptance criteria and an execution order.

**Checks run by the reviewer.** All are read-only; nothing in `results/` or `src/` was changed.
- **Wire tolerance.** The filament model (`nkm_injection.wire_field`) was integrated on axis with one inner wire
  displaced by 1, 10 and 50 µm, and with one loop's current raised by 0.1 %.
  - A 1 µm displacement gives an on-axis vertical kick of 7.3×10⁻⁵ of the peak kick. This exceeds the manuscript's
    4×10⁻⁵ limit and corresponds to A_y ≈ 0.3 σ_y.
  - The current imbalance gives 1.9×10⁻⁴ in both planes.
- **Pulse length.** For a half-sine injected at its peak, r on the next turn = |cos(πT_rev/T)|, and r ≤ 0.19 requires
  T ≤ 6.07 µs. The manuscript's 8 µs gives r = 0.50.
- **Jitter statistics.** From the `c6c_jitter_*` raw artifacts, the paired differences against zero jitter are:
  - quarter jitter: +0.3 points (95 % bootstrap −1.5 to +2.1);
  - half jitter: −6.1 points (−9.9 to −2.4).

**Status.** The manuscript, code and protected files are unchanged. No simulations were run.
