# Milestone 127 — C5: Combined-error robustness with the 3-D NKM

Completed: 2026-10-10. Consolidated task C5 (R1-07, R2-5, R2-6).
- Driver: `scripts/run_capture_robustness.py` (S7) with `--kicker-models fieldmap_3d dipole`, error budget of journal
  campaign 01 at scale 1, static orbit correction.
- Pooling: `scripts/analyze_capture_robustness.py --model fieldmap_3d --stored-model fieldmap` and `--model dipole`
  (partial rank correlations added in this milestone; unit test in `tests/test_capture_robustness_driver.py`).
- Raw data: `results/journal_campaign_02/c5_errors_seed{42,123,777}/`; pooled summaries in
  `results/journal_campaign_02/c5_pooled/` (not committed).
- Ensemble: 3 seeds × 50 realizations, 200 particles each, 500 turns; selected point x_inj = −19.5 mm, S = 0.85,
  x′ = 4.853 mrad; the dipole is the 3-D-calibrated control with the same centroid kick.

**Capture, pooled (150 paired realizations).** Intervals are cluster-bootstrap 95 % of the mean.

| Kicker | Mean | Median | 10th percentile | ≥ 80 % | ≥ 90 % | Zero capture |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 3-D NKM | 40.5 % [35.6, 45.5] | 39.0 % | 1.0 % | 11 % | 2.7 % | 7.3 % |
| dipole control | 61.4 % [56.8, 65.9] | 70.0 % | 12.5 % | 36 % | 14.7 % | 0.7 % |

Paired difference NKM − dipole: −20.9 points [−24.1, −17.7]. The NKM is lower in 91 % of realizations.
Per seed (NKM / dipole): 42 → 46.4 / 63.2 %, 123 → 36.3 / 61.5 %, 777 → 38.9 / 59.4 %. The seed spread is within the
bootstrap interval.

Without errors (seed 42 reference realization) the NKM captures 92.5 % and the dipole 94.5 %. The errors therefore
widen the gap from 2 to 21 points.

**Drivers** (Spearman ρ against per-realization capture; 150 realizations):

| Variable | NKM ρ | Dipole ρ |
| :--- | ---: | ---: |
| abs. exit centroid x | −0.54 | −0.50 |
| abs. exit centroid x′ | −0.49 | −0.74 |
| booster angle jitter | −0.42 | −0.66 |
| any magnet, septum, timing or ring error | \|ρ\| ≤ 0.13, p ≥ 0.12 | \|ρ\| ≤ 0.13, p ≥ 0.12 |

Because the exit centroid is a consequence of the sampled errors, the sampled inputs were also ranked by partial
Spearman correlation, each controlling for all other sampled inputs (`partial_spearman_sampled_inputs`, R2-13/m14):

| Sampled input | NKM partial ρ (p) | Dipole partial ρ (p) |
| :--- | ---: | ---: |
| booster angle jitter | −0.45 (5×10⁻⁸) | −0.68 (1×10⁻¹⁹) |
| booster position jitter | −0.16 (0.06) | −0.14 (0.10) |
| every other input | \|ρ\| ≤ 0.15, p ≥ 0.09 | \|ρ\| ≤ 0.15, p ≥ 0.09 |

Only the booster angle jitter is a significant independent driver. The errors are sampled independently, so this is
an association with an independently varied input, not an intervention; C6 supplies the intervention (paired jitter
scaling).

The exit centroid has an rms spread of 0.91 mm and 0.33 mrad. Capture binned by exit angle:

| Exit Δx′ [mrad] | N | NKM | Dipole |
| :--- | ---: | ---: | ---: |
| < −0.4 | 16 | 18.9 % | 21.7 % |
| −0.4 to −0.2 | 24 | 35.4 % | 55.9 % |
| −0.2 to 0 | 31 | 51.7 % | 79.3 % |
| 0 to 0.2 | 39 | 52.9 % | 79.5 % |
| 0.2 to 0.4 | 22 | 45.8 % | 67.0 % |
| > 0.4 | 18 | 13.9 % | 27.1 % |

**Interpretation.** The ensemble is limited by the transfer-line exit centroid, which is driven by booster extraction
jitter. The NKM loses most where the dipole holds up, for exit-angle deviations of 0.2–0.4 mrad: the NKM kick falls
off on both sides of its extremum, so its angular window (C3: −0.54 to +0.20 mrad at 80 %) is narrower than that of a
uniform kick.

These numbers supersede the thin-model robustness of journal campaign 01. Both kickers are now evaluated on identical
realizations with the exact 3-D field. C6 (jitter scaling) quantifies the jitter reduction needed.

**Loss accounting.** The categories reconcile in every realization. NKM: 2039 created outside the septum aperture
(identical for both kickers), 1187 at the septum on later turns, 14 617 elsewhere in the ring; none outside the
field-map domain.

**Stored beam under errors** (thin bicubic map with sampled NKM offsets; 20 000 equilibrium particles):

| Quantity | Median | 95th percentile | Max |
| :--- | ---: | ---: | ---: |
| Amplitude / σ | 0.10 | 1.75 | 6.4 |
| Filamented emittance growth | 0.2 % | 5.4 % | 29 % |

These are dominated by the sampled NKM–orbit offset (C7).

**Manuscript.** In §6, the macros RobMean…RobPairN are filled by `build_revision_figures.py`. One sentence was added
on the growth of the NKM-to-dipole deficit and on the drivers, with the new macro `RobZeroErrDip`.
