# Milestone 234 — BTS round 3 rerun on the unchanged lattice (no added correctors)

Completed: 2026-10-15. Author instruction: remove the added correctors; the BTS lattice must not be changed.

**Model change** (`src/nkm_injection/bts_round3.py`).
- **Lattice.** `aperture_lattice` returns the unchanged 36-element line, with names and types identical to
  `lattice_for`. Apertures are attributes of the existing elements (checked at element entrances) and the end marker
  m4 carries the blade; the legacy aperture elements are kept.
- **No slicing.** Interior envelopes for the nominal profile come from `observation_copy`, an observation-only copy
  that is never tracked.
- **Steering.** Horizontal field trims of the six existing dipoles (kext, sept_in, b1–b3, sept_ex), applied like the
  dipole field errors. Readings at existing element boundaries: quadrupole exits, septum entrance and end. No
  corrector or monitor element is added; the vertical plane is not corrected.
- **Removed.** `elementwise_lattice` and the corrector layouts. The protocol (revision 2) records the superseded
  layouts and the reason.

**Rerun.** All stages, in `results/bts_journal_campaign_r3b_20261015`. The added-corrector campaign
`results/bts_journal_campaign_r3_20261015` is superseded and kept on disk only.

| Quantity | Corrector version | Unchanged lattice |
| :--- | ---: | ---: |
| Active restriction (septum channel) | 0.648 mm | 0.648 mm |
| Steered loss, reference / low beta | 1.60 / 1.56 % | 1.68 / 1.47 % |
| Steered exit x / x′ rms | 0.68 mm / 0.34 mrad | 0.68 mm / 0.37 mrad |
| Prediction vs tracking (steering) | 0.6 % | 0.4 % |
| Fresh test: reference / low beta / loss-based | 2.32 / 2.15 / 0.66 % | 2.30 / 2.27 / 0.69 % |
| Loss-based minus reference | −1.66 [−2.42, −0.99] | −1.61 [−2.33, −0.96] |
| Loss ratio | 3.5 | 3.3 |
| Sensitivity population ratio | 8.4 | 5.6 |

- Unchanged: phase-advance pools (349 solutions, 200.2–232.0°), the loss-based setting (μx 200.2°), the
  dispersion-free result (65-fold), and the absent roll sensitivity.

**Manuscript and records.**
- Sections 2.3, 2.4 and 4.2, the discussion, the appendix path and the abstract numbers are updated; all round-3
  macros, tables and figures are regenerated.
- Claims BR3-01 to BR3-13 are re-pointed to the new campaign (49 claims verify).
- Updated: `round3_reproduction.md`, the Reviewer 2 response (M2, M3, M4 and the minor points), the reviews README
  and the final asset hashes (`--verify` passes).

**Tests.**
- Round-3 tests: the line is identical to the original in names, types and transport; every element has an
  aperture; trim steering reduces the exit offset with trims ≤ 1 mrad; zero trims leave the line unchanged.
- Full suite: 743 passed. Protected files are unchanged.
