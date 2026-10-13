# Round 3: feasible NKM vacuum chamber (E4)

**Why the change.** The round-2 chamber assumed a 30 × 15 mm half-aperture for the whole injection straight,
including the magnet. Inside the four-loop magnet the inner wires sit at (±5.3, ±5.3) mm, so that rectangle would
enclose the conductors. The round-2 kicker only removed particles within 1 mm of a wire centre.

**Declared chamber.** The chamber is flat, with conductors outside, over the magnet length (|s| ≤ 0.2625 m):
- **Allowance.** The wall plus conductor radius between the aperture and a conductor centre is 1.5 mm, the value used
  for the eight-conductor ALS NLK (Sun et al., PRAB 23, 010702, 2020). The largest admissible half-height is
  therefore 5.3 − 1.5 = 3.8 mm.
- **Width.** The half-width is 16 mm (32 mm full width, as on the ALS prototype). Horizontally the chamber is not
  constrained by the wires, which lie above and below it.
- **Reference chamber.** 16 × 3.8 mm (half). A scan covers half-heights of 3.0, 3.4 and 3.8 mm, with the 1.5 mm
  allowance, and 4.3 mm as an optimistic bound with a 1.0 mm allowance.
- **Validation.** `ChamberProfile.validate_against_wires` rejects any chamber that reaches a wire; the round-2
  30 × 15 mm rectangle is rejected.
- **Configuration.** `docs/paper/round3_chamber_config.json` (`nkm_magnet_half_x_m`, `nkm_magnet_half_y_m`).

**Where it acts.**
- **Injection pass.** The sliced 3-D kicker (`FilamentNKMKicker`) checks the chamber at every slice inside the magnet.
- **Later turns.** The ring's two magnet halves, `NKM_H1` and `NKM_H2`, carry it as their aperture.
- **Thin controls.** The dipole and linearised controls are checked at the magnet centre, so paired comparisons see
  the same aperture.

Outside the magnet the injection straight keeps the assumed 30 × 15 mm rectangle. The arcs, centre bends and IVUs
are unchanged from round 2. Defaults of `None` keep the round-2 model reproducible.

**Normalised apertures.** Half-aperture divided by √β, minimum over each region, ideal ring
(`e4_aperture_normalisation.json`):

| Region | Vertical (mm m^-1/2) | Horizontal (mm m^-1/2) |
| :--- | ---: | ---: |
| NKM chamber (16 × 3.8 mm) | 1.61 | 3.97 |
| Arcs (12 × 9 mm) | 1.81 | 2.99 |
| Centre bends (4.87 mm vertical) | 2.64 | — |
| Open IVUs (9 mm) | 4.72 | 4.64 |
| Closed IVUs (2.5 mm, stress case) | 1.31 | — |
| Injection straight outside the magnet | 3.57 | 7.42 |

With open IVUs, the NKM chamber is the tightest vertical restriction in the ring.

**Capture sensitivity.** Ideal ring, design beam, round-2 operating point, two 500-particle bunches (seeds
1001/1002), 500 native turns (`e4_nkm_chamber_scan`):

| In-magnet half-height | NKM capture | Dipole capture | Particles lost in the magnet |
| :--- | ---: | ---: | ---: |
| none (round-2 model) | 97.0 % | 97.3 % | 0 |
| 3.0 mm | 97.0 % | 97.3 % | 0 |
| 3.4 mm | 97.0 % | 97.3 % | 0 |
| 3.8 mm (reference) | 97.0 % [95.7, 97.9] | 97.3 % | 0 |
| 4.3 mm (1 mm allowance) | 97.0 % | 97.3 % | 0 |

On the ideal ring with the design beam, the chamber is not limiting: the injected vertical size is about 60 µm. The
concern that it might be (Reviewer 2, round 3) is therefore answered for the ideal ring. Whether coupling on the
corrected rings uses the margin is tested in the robustness rerun (E7).

**Section 8.** The eddy-current estimate now uses the flat chamber's half-gap (3.8 mm), giving:
- 2.4 ns for a 1 µm coating at 10⁶ S/m;
- about 46 ns for an 8 µm titanium coating (as on the ALS chamber);
- 0.12 ms for a 1 mm metal wall, which is excluded.

Reproduction:

```bash
python scripts/run_round3_nkm_chamber.py --study-config results/journal_campaign_03/operating_point_design_beam.json \
  --optimization-summary backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json \
  --chamber-config docs/paper/round3_chamber_config.json --output-dir results/journal_campaign_04/<new> --workers 8
python scripts/analyze_round3_chamber.py --study-config results/journal_campaign_03/operating_point_design_beam.json \
  --chamber-config docs/paper/round3_chamber_config.json --work-dir <tmp> --output <new>.json
```
