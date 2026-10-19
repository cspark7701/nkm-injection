# Milestone 238 — F6: Septum dispersion budget and thin-map accuracy scope

Completed: 2026-10-19. Round-4 task F6 (R1D-06; R2d-6/7). Note: `docs/paper/round4_dispersion_scope.md`.

**Dispersion budget at the septum** (D 80.868 mm, D′ 47.472 mrad, σ_δ 1.06e-3):
- Betatron/dispersive size 134/86 µm and divergence 57/50 µrad (76 µrad total).
- Shot energy jitter adds 81 µm and 47 µrad.
- The companion dispersion-free BTS exit is cited as a BTS-only analytic alternative, not imported into NKM capture.

**Accuracy scope.** The η^1.46 fit is labelled a synthetic diagnostic launch. Along the production matched
trajectories the thin-map error is:

| Point | y = 0 | y = 1 mm |
| :--- | ---: | ---: |
| Current | +161 µrad | +148 µrad |
| Earlier | −35 µrad | −54 µrad |
| Extremum-centred | −47 µrad | −69 µrad |

- At the current point that is 2.3 times the synthetic-launch value and 3.7 times the 0.044 mrad allowance.
- The sliced vector map is below 10⁻⁷ rad at every point.
- The allowance at an adopted point other than the current one follows its window (F7).

**Tests** (`tests/test_round4_protocol.py`): the budget terms, and sliced ≪ thin on the production trajectory.
