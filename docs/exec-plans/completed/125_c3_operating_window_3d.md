# Milestone 125 — C3: Operating window with the exact 3-D NKM

Completed: 2026-10-10. Consolidated task C3 (R1-04, R2-2, R2-9, R2-7/M7).
- Driver: `scripts/run_operating_window_3d.py`.
- Raw data: `results/journal_campaign_02/c3_operating_window/` (not committed).
- Figures: 5–7 of the revised manuscript (`scripts/build_revision_figures.py`).

**Grid.** x_inj −19.5…−22 mm × S 0.80…1.10; one 200-particle bunch per point.
- 27 matched points; 15 combinations have no inner matched root.
- A ridge of 90–92 % capture where the matched centroid sits at the kick extremum.
- Declared rule: largest Wilson lower bound. Selected point x_inj = −19.5 mm, S = 0.85, x′ = 4.853 mrad, centroid at
  −8.52 mm; 92.5 % on the grid.

**Validation on fresh seeds** (4 × 500 particles, seeds 1001–1004, not used for selection):

| Model | Capture | Paired vs 3-D |
| :--- | ---: | :--- |
| 3-D NKM | 93.0 % [91.7, 94.0] | — |
| linear | 97.8 % | −4.8 ± 0.3 |
| dipole | 97.0 % | −4.1 ± 0.5 |
| off | 0 % | — |

The controls are calibrated to the 3-D response. Selection is not inflated by grid noise.

**Window at the declared 80 % threshold** (two seeds × 500 particles per value):

| Scan | Window | Width | Best | Step |
| :--- | :--- | :--- | :--- | :--- |
| angle | −0.54 … +0.20 mrad (crossings ± 0.04) | 0.74 mrad | 95.1 % at −0.10 mrad | 0.1 mrad |
| septum position | −0.60 … +0.83 mm | 1.44 mm | — | 0.2 mm |

Zero exit angle is 0.1 mrad from the capture optimum.

**Acceptance.** A single-particle survival map in septum phase space (3,692 particles, δ = 0, 500 turns) is drawn with
the injected-beam 1σ/2σ ellipses (σ_x = 0.50 mm, σ_x′ = 0.21 mrad, including dispersion) and the blade.

**Nominal-condition tolerance scans for C6:**
- NKM–orbit offset −0.6 … +0.6 mm: capture 87.0–93.6 %.
- Injected ε_x 25/50/100/150/200 nm rad: 98.9 / 97.4 / 93.1 / 87.2 / 81.1 %.
