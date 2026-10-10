# Milestone 122 — C2: Mechanism of the thin/finite-length difference

Completed: 2026-10-10. Consolidated task C2 (R1-03, R2-1c). Record:
[`kicker_model_validation.md`](../../jinst-paper/kicker_model_validation.md) §5.

`scripts/analyze_finite_length_mechanism.py` compares the thin, straight-path, bent-path and exact 3-D models at their
own matched angles.
- **Bent path vs exact 3-D:** the bent-path model reproduces the 3-D result (matched angle 4.6476 vs 4.6475 mrad;
  amplitudes within 0.01 mm). Straight-path averaging does not.
- **Mechanism:** the beam's own deflection inside the magnet, with a sagitta |K|L/8 = 0.32 mm. It holds
  positive-angle-error trajectories on the outer side of the kick extremum, near the kick maximum, instead of letting
  them cross onto the weaker inner flank.
- **Length scan at fixed integrated kick:** a longer magnet lowers the sensitivity to positive errors but raises the
  nominal amplitude; there is no matched solution for L ≥ 0.75 m.

Output: `results/journal_campaign_02/c2_mechanism/finite_length_mechanism.json` (not committed).
