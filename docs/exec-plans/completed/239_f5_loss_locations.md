# Milestone 239 — F5: Loss plane, location and turn

Completed: 2026-10-19. Round-4 task F5 (R1D-04; R2d-5). Note: `docs/paper/round4_loss_locations.md`.

**Work.**
- `scripts/run_round4_loss_locations.py` reruns 8 NKM zero-capture realizations (first per ring, full budget, seed 42)
  and ring 5501 without injection errors.
- It keeps the per-particle loss records and classifies in-magnet losses (chamber, conductor guard, domain).
- All reruns reproduce the E7 counts exactly, and the records reconcile with the categories.

**Findings.**
- **NKM zero-capture losses** are first-turn losses: 1 491 of 1 500 on turn 0, 955 vertical and 545 horizontal,
  spread round the ring.
  - None occur inside the magnet; the numerical guards never act inside the chamber region.
  - The dipole control loses later on the same realizations.
- **Ring 5501** loses vertically over many turns for both models.
  - Opening the in-magnet chamber (diagnostic) changes little (29.8 → 33.2 %), so vertical motion growth, consistent
    with uncorrected coupling, limits it.
- **Chromaticity claim** reduced to "common to both kickers".

**Tests:** the classifying kicker is identical to the production kicker (losses and coordinates), and its reason
counts reconcile.
