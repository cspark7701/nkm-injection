# Milestone 128 — C6: Booster-jitter tolerance curves with and without static orbit correction

Completed: 2026-10-11. Consolidated task C6 (R1-04, R2-4/R2-11).
- Driver: `scripts/run_capture_robustness.py` (exact 3-D NKM, 640 slices; calibrated dipole control on the
  combined-error seeds). Analysis: `scripts/analyze_capture_robustness.py` (cluster bootstrap, Spearman and partial
  Spearman rank correlation).
- Raw data (not committed): `results/journal_campaign_02/c6_jitter_*` and `c5_errors_seed*` (no correction);
  `c6c_jitter_*` and `c5c_errors_seed*` (with `--correct-static-orbit`); pooled analyses in `c5_pooled/`.
- Queues: `logs/run_c3_c6.sh`, `logs/run_c6_corrected.sh`.
- Setup: operating point x_inj −19.5 mm, S 0.85, x′ 4.853 mrad. Each realization tracks 200 particles for 500 turns.
  The error budget is that of milestone 127. Only the booster centroid jitter is scaled; all other errors keep their
  draw, and the realizations are paired by (seed, sample_id). The jitter scan uses 50 realizations (seed 42) per level.
- Static orbit correction: ideal steering at the septum exit removes the static trajectory of each perturbed
  transfer line (reference particle without jitter); the shot-to-shot jitter is kept.

**Why the correction was added.** Without correction, removing the jitter raised the mean capture only from 46.4 to
58.6 %. The static transfer-line errors still displace the exit centroid by 0.71 mm rms, more than the position window,
so no jitter reduction reaches 80 %. A draft claim of the form "80 % requires jitter below X" was therefore wrong and
has been removed. The corrected ensemble separates the jitter from the static errors.

**Tolerance curves (3-D NKM, seed 42, 50 paired realizations per level).**

| Jitter scale | Uncorrected mean | median | p10 | ≥ 80 % | Corrected mean | median | p10 | ≥ 80 % |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 58.6 % | 68.2 % | 11.8 % | 34 % | 69.7 % | 80.0 % | 26.8 % | 50 % |
| 0.25 | 58.0 % | 69.8 % | 14.6 % | 28 % | 70.0 % | 81.2 % | 38.4 % | 56 % |
| 0.5 | 55.0 % | 65.5 % | 10.2 % | 22 % | 63.6 % | 69.0 % | 27.6 % | 36 % |
| 0.75 | 51.6 % | 62.3 % | 6.8 % | 18 % | 55.8 % | 58.5 % | 19.5 % | 24 % |
| 1 | 46.4 % | 55.8 % | 5.1 % | 14 % | 47.3 % | 48.5 % | 5.8 % | 18 % |
| x only (1) | 55.3 % | 67.8 % | 12.4 % | 20 % | 64.6 % | 76.0 % | 19.4 % | 38 % |
| x′ only (1) | 48.1 % | 54.0 % | 2.4 % | 18 % | 52.3 % | 54.5 % | 6.4 % | 24 % |

Scale 1 is the assumed jitter (0.5 mm, 0.2 mrad rms). Bootstrap 95 % intervals of the means are about ±7 points.
- Below a quarter of the assumed amplitude (0.125 mm, 0.05 mrad) the jitter costs nothing measurable in either
  ensemble (corrected 70.0 vs 69.7 %).
- The angle jitter costs more than the position jitter (corrected 52.3 vs 64.6 %).
- At the full assumed jitter the correction gains little (seed 42: 46.4 → 47.3 %), because the jitter, not the static
  offset, then sets the exit centroid. With correction, removing the jitter gains 22 points; without it, 12 points.
- No level reaches a mean of 80 %. The macros `Jit{,C}ScaleForEighty` therefore print "none".

**What limits capture at zero jitter with correction.** The exit centroid spread drops to 0.20 mm and 0.017 mrad rms.
The median is 80 %, but the mean is 69.7 % and the 10th percentile 26.8 %.
- No sampled error is a significant driver (partial Spearman, 13 sampled inputs; all p > 0.13).
- The strongest marginal correlations are the energy offset (ρ = −0.26, p = 0.07) and the BTS dipole-field error
  (ρ = −0.26, p = 0.07).
- The worst realizations combine several small offsets of NKM, ring orbit and septum with an NKM scale error.

So the remaining loss is the combined static error budget, not one tolerance. A mean of 80 % under this budget needs:
- orbit correction;
- booster jitter of at most a quarter of the assumed value;
- tighter static tolerances, or a wider window, for example from sextupole optimisation for the injection DA.

**Combined errors with correction (three seeds, 150 paired realizations).**

| Kicker | Mean | 95 % CI (cluster bootstrap) | Median | p05 |
| :--- | ---: | ---: | ---: | ---: |
| 3-D NKM | 44.4 % | 39.7–49.3 % | 42.8 % | 0.0 % |
| Dipole control | 65.6 % | 61.3–69.8 % | 73.8 % | 12.5 % |

- Per seed (NKM / dipole): 42 → 47.3 / 66.9 %; 123 → 40.2 / 62.3 %; 777 → 45.8 / 67.7 %.
- Paired NKM − dipole per seed: −19.6, −22.1, −21.9 points.
- The uncorrected ensemble gives 40.5 % (NKM) and 61.4 % (dipole), so correction adds about 4 points at full jitter.
- Partial Spearman, corrected NKM: booster x′ ρ = −0.52 (p < 10⁻³) and booster x ρ = −0.24 (p = 0.006).
  For the dipole: booster x′ −0.75, quadrupole dy −0.25, booster x −0.24, energy −0.20.
- With the static offset removed, the position jitter also becomes a significant driver.

**Manuscript and builder.**
- §6.2 reports both ensembles: `RobC*` macros for the combined errors and `JitC*` macros for the jitter scan.
  New macros are the per-level median and the fraction of realizations at or above 80 %:
  `Jit{,C}{Zero,Quarter,Half,ThreeQ,Full}{Median,FracEighty}`.
- Figure 8 (centre) shows the corrected curve with its bootstrap band and p10, the uncorrected mean (dotted) and the
  corrected x-only and x′-only points.
- The abstract, discussion and conclusions no longer claim that jitter reduction alone reaches 80 %.

**Checks.**
- Every raw artifact records its seed, CLI and input SHA-256.
- The particle loss categories reconcile with the particle count.
- The zero-error realization is identical in both ensembles (NKM 92.5 %, dipole 94.5 %), as it must be: the
  correction is a no-op without errors.
