# Milestone 236 — F1: Round-4 protocol, point candidates and reproduction check

Completed: 2026-10-19. Round-4 task F1 (supports R1D-01/02/03/05/08 and R2d-1/2/3/4).

**Protocol.** `docs/paper/round4_protocol.json`, declared before any F2–F7 run. It fixes:
- **Model:** the adopted E7 model (filament NKM 640 slices, recalibrated dipole control, round-3 chamber, E5
  corrected rings, ideal static steering, 500 turns, 200 particles, 50 realizations, seed 42). The BTS lattice is
  unchanged; the companion BTS alternatives are not imported.
- **Current point:** retained until an explicit F3 decision.
- **Error classes:** seven physical classes (BTS magnets, beam shape, mean energy, NKM amplitude, NKM–orbit
  alignment, septum, longitudinal timing) and the not-applied terms.
- **Disabling rule:** σ = 0, which keeps every other draw.
- **Estimands, bootstrap and the F3 decision rule** (a change requires a full-budget NKM gain with a paired interval
  excluding zero and no zero-jitter loss beyond the declared 1-point margin).

**Driver.** `scripts/run_round4_campaign.py`, stages reproduce, points, ablation and points_test. Ensembles reuse the
E7 command line with only the error or study configuration changed.

**Reproduction** (`results/journal_campaign_05/f1_reproduction.json`).
- Realization 0 of `e7_jitter_0` rerun with the current code is bitwise identical: models, loss records and BTS exit
  moments (NKM 29.5 %, dipole 94.5 %).
- Only `bts_round3.py` was added to `src/nkm_injection` since E7.
- The E7 zero-jitter and full-budget seed-42 ensembles are therefore valid paired references.

**Points** (`results/journal_campaign_05/points/points.json`; kick-map extremum at −8.500 mm, −5.749 mrad):

| Point | x_inj | S | x′ | Centroid at NKM |
| :--- | ---: | ---: | ---: | ---: |
| Current | −19.478 mm | 0.95 | 5.319 mrad | −7.443 mm |
| Earlier | −19.500 mm | 0.85 | 4.853 mrad | −8.521 mm |
| Extremum-centred | −20.751 mm | 0.95 | 5.415 mrad | −8.500 mm |

All roots are reproduced, and all points are inside the septum-clearance limit (−18.478 mm).

**Tests.** `tests/test_round4_protocol.py` (4 pass): the classes cover every applied term; disabling a class zeroes
only its terms and leaves every other draw identical; the all-off and alone configurations are correct; the point
checks are recorded.

**Started.** The F2 (15 ensembles) and F3 (4 ensembles) runs in `results/journal_campaign_05/`.
