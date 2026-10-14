# Milestone 220 — E7: The single robustness rerun

Completed: 2026-10-15. Round-3 task E7 (R2c-4, R2c-8). Compute about 9 h with 8 workers.

**Run.** Joint ensembles (3 seeds × 50), the jitter scan (0–1 scale, plus x and x′ only) and matched-knob tuning at
the E6 point, on the E5 rings with the E4 chamber and the round-2 budget. Populations are unchanged from round 2.

**Results.**
- **Joint errors.** NKM mean 16.1 % [12.0, 20.4] (ring-cluster [10.9, 21.5]; leave-one-ring-out 14.9–17.4 %), median
  0 %. Dipole 44.1 %. Paired difference −28.0 [−32.5, −23.5].
- **Jitter.** Zero jitter gives 40.1 %. Quarter jitter −5.7 [−9.4, −2.5] (not noninferior), angle only −16.8,
  position only −8.9. Only booster angle is Holm-significant (ρ −0.38).
- **Tuning.** +11.9 [+8.0, +16.3] at zero jitter (52.1 %) and +11.0 at quarter jitter. 28 % of the machines end on the
  outer x_inj bound: the optimum lies further from the septum than the declared range.

**Code.**
- New: `scripts/run_round3_campaign.py`, `scripts/run_round3_tuning.py`.
- `src/nkm_injection/injection_tuning.py`: `iterated_coordinate_search`, with tests.
- `scripts/analyze_round2_robustness.py`: `--prefix`, ring-cluster bootstrap, leave-one-ring-out.
- `scripts/round2_reporting.py`: macros for the ring-cluster interval and the tuning bound/evaluation counts; Figure 8
  legend placement.
- `scripts/analyze_round3_synthesis.py` (E8 input; run on E5/E6 data).

**Manifest.** `revision_manifest_round3.json` now overrides every round-2 robustness key with the E7 artifacts
(37 overrides, none missing).

**Manuscript.**
- Macros and Figure 8 are regenerated; the robustness text is rewritten in E8.
- The one-column gated build is clean.

**Checks.** The tuning, robustness and reporting tests pass (25). Method note: `docs/paper/round3_robustness.md`.
