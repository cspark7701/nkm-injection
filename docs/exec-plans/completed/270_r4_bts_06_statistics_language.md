# Milestone 270 — R4-BTS-06: mean clearance and statistics language

Completed: 2026-10-31. Round-4 task R4-BTS-06 (Reviewer 1 R3-BTS-04; Reviewer 2 R2C-05, "indistinguishable";
R2C-08, clustering method).

**Existing-data arithmetic.** `export_bts_round4_assets.py --part statistics` writes
`generated/round4_statistics.json`, computed from the round-3 steering raw data: 600 shots, with the bootstrap seed
91005 and 10 000 resamples.
- **Mean exit x:** −68.50 µm uncorrected and +8.77 µm corrected (matched reference). The spread is 1.20 mm and
  0.68 mm.
- **Low beta minus matched reference, corrected:**
  - tracked loss −0.209 percentage points [−0.391, −0.062], resolved;
  - clearance −0.0013 mm [−0.0093, +0.0066], unresolved.

**Article changes.**
- **Section 4.2, mean clearance.** The explanation no longer implies survivor censoring: all 600 shots enter both
  means, and the moments are uncensored. The static offset of −68.5 µm away from the blade raises the mean
  clearance while the spread grows. At a one-sided edge, E[c] = a − E[ū] − 5σ does not depend on τ, whereas the
  mean loss grows with it.
- **Section 4.2, low beta.** "Indistinguishable in every column" is replaced by the paired evidence. On the steering
  population the loss is lower and resolved; on the fresh test the change is unresolved (−0.03 [−0.23, +0.17]).
  The difference follows the phase advance, not the peak beta.
- **Section 3.3, intervals.** The method is stated once: a realization-cluster percentile bootstrap with 10 000
  resamples. It does not certify convergence of the heavy loss tail.

The isolated build is clean; the installed PDF is rebuilt in R4-BTS-09. Protected files are unchanged.
