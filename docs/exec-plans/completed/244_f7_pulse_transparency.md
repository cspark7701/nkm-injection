# Milestone 244 — F7: pulse and transparency at the current point

Completed: 2026-10-20. Round-4 task F7 (R1D-03/07, R2d-3/7) of the
[round-4 plan](../../paper/reviews/consolidated_revision_plan_round4.md); note:
[round4_pulse_transparency.md](../../paper/round4_pulse_transparency.md).

**Recomputed** at the retained point (x_inj −19.478 mm, S = 0.95; outputs in `results/journal_campaign_05/f7/`):
- the pulse: native turn 1–3 coordinates and kicks, allowance and pulse limits;
- the analytic 3-D transparency;
- the per-wire and per-loop sensitivities;
- the simultaneous wire-error Monte Carlo;
- the 1000-turn stored-beam tracking (2 seeds × 300 particles × 3 offsets).

**Single convention.** The allowance is one tenth of the current 0.443 mrad window, i.e. 0.044 mrad, the same as the
thin-map accuracy allowance; the round-2 pulse used 0.076 mrad.

**Pulse limits.** 5.76 µs (peak-phase) and 5.33 µs (no-return); the 5.3 µs example still satisfies both.

**Transparency.**
- It scales by 0.95/0.85 for single-pass quantities.
- A 0.2 mm offset now gives 0.11–0.12 σ, slightly above the 0.1 σ criterion, and the text says so.
- Wire limits are 0.26–1.82 µm; the 10 µm wire Monte Carlo median is 2.9σ / 5.4σ.

**Manifest.**
- `scripts/make_round4_manifest.py` writes `docs/paper/revision_manifest_round4.json`: round 3, plus 10 round-4
  artifacts, plus 5 builder keys re-pointed.
- The S = 0.85 originals are kept as `historical_*`, and all hashes are rechecked.
- The generated macros are installed from it. Only the intended macros changed.
- Fig. 7 is regenerated; figures with unchanged inputs keep their earlier files (matplotlib 3.8.3, while the
  available env has 3.11.1).
- A check compile gives 30 pages and no LaTeX errors.

**Files.**
- `scripts/make_round4_manifest.py`;
- `docs/paper/revision_manifest_round4.json`;
- `docs/paper/generated/*` (macros, provenance, Fig. 7);
- `docs/paper/paper.tex` (pulse point identity, allowance convention, transparency at the selected S);
- `docs/paper/round4_pulse_transparency.md`;
- `tests/test_round4_protocol.py` (manifest test; 14 tests pass with the steering tests);
- the round-4 plan.
