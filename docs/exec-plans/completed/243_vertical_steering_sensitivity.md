# Milestone 243 — Two-plane steering sensitivity

Completed: 2026-10-20. Author-approved post hoc sensitivity following F2 (the round-4 plan, row F2v). Declared and
committed before running (0b2e6ed); note: [round4_vertical_steering.md](../../paper/round4_vertical_steering.md).

**Code.**
- `nkm_injection.steering.subtract_static_reference(beam, reference, planes)` with `'x'` (production) or `'xy'`.
- `run_capture_robustness.py --static-steering-planes`.
- Driver stage `vertical`.
- Production x-only jobs keep their identity and reproduce E7 realization 0 bitwise.

**Runs.**
- `results/journal_campaign_05/f2v_xy_{zero,full}`: 50 seed-42 realizations each at the current point.
- Paired with `e7_jitter_0` and `e7_seed42`.

**Results** (NKM / dipole / gap, points):
- Zero jitter: 40.1 / 68.5 / −28.3 → 76.6 / 82.6 / −6.1, with no zero-capture events. NKM capture equals the F2
  value with BTS magnet errors off, so the whole BTS-magnet effect is the uncorrected vertical centroid.
- Full budget: 19.5 / 48.2 / −28.8 → 33.9 / 57.2 / −23.3.
- Jitter cost, paired:
  - x-only steering: −20.7 / −20.2 (gap −0.5);
  - two-plane steering: −42.7 / −25.4 (gap −17.2 [−25.4, −9.2]).
- The static vertical error and the booster jitter remove largely the same NKM shots. The NKM-specific attribution
  therefore depends on which one is corrected; the abstract must state both (F8).

**Files.**
- `scripts/analyze_round4_vertical.py`;
- `docs/paper/round4_vertical_steering.md`;
- the round-4 plan, new row F2v.
