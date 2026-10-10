# Milestone 126 — C4: Survival, loss accounting and bounded sensitivities

Completed: 2026-10-10. Consolidated task C4 (R1-06, R2-3, R2-4, R2-12).
- Driver: `scripts/run_survival_validation.py`.
- Raw data: `results/journal_campaign_02/c4_survival/` and `c4_aperture_diag_*` (not committed).
- Operating point: x_inj = −19.5 mm, S = 0.85; exact 3-D NKM.

**Precision.** A single 2000-particle bunch gives 92.4 % [91.2, 93.5], consistent with the four 500-particle
validation bunches (93.0 %). Losses: 17 at the septum on later turns, 135 elsewhere in the ring, none at creation or in
the magnet. Every category reconciles with N in every stage.

**Long-term survival** (2 × 500 particles, 4000 turns ≈ one damping time): 93.0 % at turn 500, 89.6 % at 2000 and 89.5 %
at 4000. 3.5 % are lost after turn 500, and losses saturate by about turn 2000. The 500-turn capture is therefore
≈ 3.5 points optimistic, which the manuscript states.

**Chamber aperture** (uniform rectangle at every element; parameterised, since no chamber is specified):

| Half-width × half-height | Capture |
| :--- | ---: |
| 15 × 5 mm | 86.3 % |
| 12 × 5 mm | 83.8 % |
| 11 × 5 mm | 76.0 % |
| 10 × 5 mm | 47.9 % |

The plane diagnostic (seeds 1001/1002) shows the loss is vertical:

| Case | Capture |
| :--- | ---: |
| 15 × 10 mm | 92.4 % |
| open × 5 mm | 86.3 % |
| no aperture, without NKM vertical kick | 94.8 % |
| open × 5 mm, without NKM vertical kick | 88.0 % |
| no aperture, with the vertical kick (paired reference) | 93.0 % |

The 5 mm half-height costs 6.7 points with and 6.8 points without the NKM vertical kick, so it is the ring's x–y
coupling of the large horizontal oscillation. At the selected point the NKM vertical kick costs ≈ 1.8 points, against
≈ 5 at the earlier point, because the linear vertical defocusing −∂Δx′/∂x vanishes at the kick extremum. The manuscript
abstract, §3 and the discussion were qualified accordingly.

**Ring errors.** Seeded random relative gradient errors on all 344 quadrupoles and 1 × 10⁻³ on all 168 sextupoles; no
misalignment and no correction; 10 seeds per level:

| Quadrupole σ | Mean capture | Range | Negative DA edge |
| :--- | ---: | :--- | :--- |
| 5 × 10⁻⁴ | 85.6 % | 77.6–89.6 % | −13 … −11 mm |
| 1 × 10⁻³ | 69.9 % | 58.0–80.0 % | −12 … −9.5 mm |

This is a bounded sensitivity, not a corrected-machine model. The DA of the corrected KLS lattice is identified as the
decisive input for an operational estimate.

**Code.** `--no-vertical-kick` diagnostic option; loss locations in `track_injection` (septum return or elsewhere).
