# Milestone 121 — C1: Exact 3-D NKM field, kicker-model validation and vertical-sign fix

Completed: 2026-10-10. Consolidated task C1 (R1-02, R2-1a, R2-14). Record:
[`kicker_model_validation.md`](../../jinst-paper/kicker_model_validation.md) §§1–4, 6.

- **`src/nkm_injection/wire_field.py`:** a closed-form Biot–Savart field of the four RADIA filament loops (geometry read
  from the protected notebook source, nothing executed), and a sliced tracker in AT canonical coordinates.
  - Reproduces both kick-map components to 7×10⁻¹² rad over 3,657 nodes.
  - Converged at 640 slices to 7×10⁻¹¹ rad.
  - δ effect: 0.37 µrad per 10⁻³.
- **Vertical-sign bug fixed** in `KickModelEvaluator`. The map stores (∫B_y, +∫B_x); the physical pair uses −∫B_x. The
  legacy sign remains available via `vertical_sign=+1`. The linearised control gains −k₁y.
- **Capture on identical bunches** (4 × 500 particles):

| Model | Capture |
| :--- | ---: |
| legacy thin | 91.05 % |
| physical thin | 89.70 % |
| 3-D, thin angle | 84.8 % |
| 3-D, re-matched angle | 81.75 % |

- **Vertical diagnostic:** suppressing the 3-D vertical kick restores 87.8 % (1-D thick model 87.4 %), so the NKM's
  vertical defocusing of the off-axis injected beam costs about 5 points.
- **Model choice:** the exact 3-D model becomes the principal model.

Drivers: `scripts/validate_kicker_models.py`. Tests: `tests/test_wire_field.py`, 7 tests. Full suite: 660 passed.
