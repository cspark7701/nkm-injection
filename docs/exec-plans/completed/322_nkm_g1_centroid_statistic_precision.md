# Milestone 322 — NKM G1 centroid-statistic precision

Completed: 2026-11-01.

The detailed source audit found that the NKM ablation's 0.90 mm / 77 microradian labels come from population standard deviations, whereas the companion quotes root-mean-square centroids. Added an exact final audit with both means, standard deviations and rms values. NKM rms values are 0.902756 mm / 77.7185 microradians; BTS zero-jitter rms values are 1.072772 mm / 96.2907 microradians. Populations, correlation models and steering still differ, so no sampling-only attribution is made.

Updated the reproducible audit and comparison note. Kept the original declaration-time audit and frozen protocol unchanged; no tracking input or physics implementation changed. The manuscript's in-progress G3 wording will identify the statistic explicitly. Numerical identity is checked through the actual audit command and the shared-strength/geometry assertions. The G2 scan continues independently.
