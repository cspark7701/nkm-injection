# Round 4 (F5): where the beam is lost

Script: `scripts/run_round4_loss_locations.py`. Outputs:
- `results/journal_campaign_05/f5_loss_locations.json`;
- `results/journal_campaign_05/f5_ring5501_chamber_check.json`.

**Cases.** Unchanged physics with loss records:
- the first NKM zero-capture realization on each of 8 rings, from the full-budget seed-42 ensemble (both models);
- the selected point on corrected ring 5501 without injection errors (bunch seed 1001, 500 particles).

Every rerun reproduces the stored E7 capture and loss-category counts exactly. The per-particle ring-loss records
sum to the `ring` category in every case.

## Loss categories inside the 3-D NKM

| Condition | Kind | Definition |
| :--- | :--- | :--- |
| chamber | physical | flat in-magnet chamber, 16 × 3.8 mm half-apertures, over the magnet length |
| conductor | numerical guard | within 1 mm of a wire, anywhere in the ±0.45 m integration span |
| domain | numerical | outside \|x\|, \|y\| ≤ 50 mm (field-model domain) |

- Over the magnet length, the chamber removes a particle before either numerical limit can: the lowest wires sit at
  |y| = 5.3 mm.
- The numerical limits apply only in the fringe span beyond the magnet ends.
- In all selected cases no particle was removed inside the magnet (the stored `outside_field_map` counts are zero
  there).
- A test confirms that the classifying copy of the kicker is physically identical to the production kicker.

## NKM zero-capture realizations (8 rings, 1 500 NKM losses)

- **Timing.** 1 491 of the 1 500 NKM losses occur on the **first turn**, 7 on turns 1–9 and 2 later.
- **Planes.** 955 vertical and 545 horizontal; the plane is assigned at the element aperture where the particle was
  lost.
- **Locations.** Spread round the ring: LM21, D21U, sextupoles S31/S32, D25U, LC12, Q11.
- **Septum.** Three cases also lose 4–85 particles at septum creation.

On the same realizations the dipole control loses later (mostly turns 10–500; in two cases it also loses everything
on the first turn). The NKM's zero-capture events are therefore single-pass losses of a beam whose centroid leaves
the kicker with a large betatron amplitude (F4: the post-kick amplitude organises capture). They are not slow
dynamic-aperture erosion. Horizontal amplitude couples into the vertical plane within the first turn through the
sextupoles and the uncorrected skew errors; these data do not separate the two routes.

## Ring 5501 without injection errors

- **Losses.** NKM 29.8 % and dipole 33.2 % capture. The losses are almost all vertical (333/351 and 327/334) and
  occur late (turns 10–500).
- **Locations.** The NKM magnet's ring elements NKM_H1/NKM_H2 (the 3.8 mm in-magnet chamber), then D25U, L31 and Q31.
- **Diagnostic.** Opening the in-magnet chamber to 15 mm, which is infeasible with the wires and used only as a
  diagnostic, raises capture only to 33.2 % (NKM) and 37.6 % (dipole). The vertical losses move to L31, Q31 and D25U.
- **Reading.** The in-magnet chamber is not what limits ring 5501. Vertical motion grows over many turns for both
  kickers, consistent with coupling that the correction chain cannot correct (no skew correctors). The mechanism is
  not isolated here.

## Chromaticity inference

The round-3 ring-level association with residual chromaticity is weak:
- 10 rings and 16 unadjusted tests;
- a chromaticity range of only 5.9–6.9;
- the highest-chromaticity ring captures 87 %.

The claim is reduced to "the ring-to-ring spread is common to both kickers". No chromaticity correction was run.
That is a controlled extension outside the round-4 scope.
