# Milestone 221 — E8: Physical synthesis and manuscript rewrite

Completed: 2026-10-15. Round-3 task E8 (R1C-04, R1C-06, R2c-5; also the E10 items deferred to here).

**Analysis.** `scripts/analyze_round3_synthesis.py` produces `results/journal_campaign_04/e8_synthesis.json`
(manifest key `round3_synthesis`). It covers the margin hypothesis over 400 candidate–ring pairs and the ring-level
correlates at the selected point. The builder step `round3_synthesis` emits the `Syn*` macros and the hierarchy table.

**Findings.**
- Corrected ring errors cost both kickers about equally: 78.0 against 82.2 %, correlated with residual chromaticity
  and β-beat.
- The on-axis DA margin does not organize capture (ρ −0.23). The weakest ring has a large margin, which rejects the
  margin hypothesis.
- The NKM-specific loss comes from injection errors acting on its 0.44 mrad angular window. Booster angle jitter is the
  only significant driver.
- The operating point was selected without injection errors; including them would favour a wider window. This is
  stated as a next step, not tested.

**Manuscript.**
- **Robustness section.** Ring-cluster interval and leave-one-ring-out range added; the quarter-jitter result restated
  as a failed one-sided noninferiority test with a resolved loss; the tuning paragraph rewritten for matched knobs,
  including evaluations and the outer-bound fraction.
- **New material.** Table V (hierarchy) and a synthesis paragraph.
- **Rewrites.** The abstract, the discussion (mechanism paragraph, limitations including the corrector system) and
  the conclusions.
- **Comparison table.** Gives the robust mean next to the nominal value.

**Checks.** Both layouts build clean: one-column 30 pages, two-column 15, supplement 6.
