# Source-labelled BTS model and beam

All dimensions and strengths below are model values frozen from the archived configuration, not a dated mechanical survey or verified hardware settings. Entrance m1 (s=0) and exit m4 (s=21.789 m, downstream of sept_ex) use local AT coordinates. No intervening transport to the NKM centre has been established; the m4 target remains parametric.

## Beam and constraints

The 4 GeV and 7.67 nm rad horizontal design input / 0.106% spread follow the author-sourced booster study in [dependent answers](../paper/dependent_answers.md), TUPC12 Table1. Vertical 0.767 nm rad (10% ratio), zero initial transverse coupling and Gaussian independence are assumptions. The full covariance includes entrance dispersion and momentum correlations; ct is fixed for this single-pass, RF-free calculation. Gaussian particles are untruncated. Historical 100/10 nm rad, 0.11% spread ensembles are separate.

Five-sigma projected clearance is a chosen metric, not an absolute enclosure of a Gaussian. At each model aperture: c = half_width - |centroid| - 5 sqrt(Sigma_uu). Roll-induced coupling is included through full covariance transport. Four discrete square limits do not represent the unknown continuous vacuum chamber; these clearances and transmission are conditional on those stations.

K bounds [-2.5,2.5] for q11/q33 and [-3,3] otherwise, 19.35 mm bore, 1.2 T pole limit and 60 m beta ceiling are assumptions. At 4 GeV B rho=13.34256 T m; G=K B rho and Bpole=|G| r. Bounds imply |G|<=33.356/40.028 T/m and Bpole<=0.645/0.775 T; neither proves magnet feasibility.

## AT / MAD-X non-equivalence

The legacy bts.madx line uses q11–q13, q21–q23, q31–q34 (ten active quadrupoles; Q4 is defined but unused), different bend signs, lengths, edge angles and drifts. It is not an independent implementation of this nine-quadrupole model. No cross-code numerical comparison is claimed. R1-BTS-05 uses an independent hard-edge map of the identical AT element sequence.

## Actual element boundaries

| Index | Element | Entrance [m] | Exit [m] | Model aperture [m] |
| :--- | :--- | ---: | ---: | :--- |
| 0 | m1 | 0.000 | 0.000 | — |
| 1 | ap_rect | 0.000 | 0.000 | [-0.01935, 0.01935, -0.01935, 0.01935] |
| 2 | kext | 0.000 | 0.310 | — |
| 3 | sept_in | 0.310 | 1.310 | — |
| 4 | dr1 | 1.310 | 3.155 | — |
| 5 | q11 | 3.155 | 3.355 | — |
| 6 | dr_q11_12 | 3.355 | 3.705 | — |
| 7 | q12 | 3.705 | 3.905 | — |
| 8 | dr_q12_13 | 3.905 | 4.255 | — |
| 9 | q13 | 4.255 | 4.455 | — |
| 10 | dr2 | 4.455 | 6.833 | — |
| 11 | m2 | 6.833 | 6.833 | — |
| 12 | ap_rect2 | 6.833 | 6.833 | [-0.03, 0.03, -0.03, 0.03] |
| 13 | b1 | 6.833 | 8.233 | — |
| 14 | dr3 | 8.233 | 9.806 | — |
| 15 | q21 | 9.806 | 10.006 | — |
| 16 | dr_q21_22 | 10.006 | 10.356 | — |
| 17 | q22 | 10.356 | 10.556 | — |
| 18 | dr_q22_23 | 10.556 | 10.906 | — |
| 19 | q23 | 10.906 | 11.106 | — |
| 20 | dr4 | 11.106 | 11.761 | — |
| 21 | m3 | 11.761 | 11.761 | — |
| 22 | ap_rect2 | 11.761 | 11.761 | [-0.03, 0.03, -0.03, 0.03] |
| 23 | b2 | 11.761 | 13.161 | — |
| 24 | dr4 | 13.161 | 13.816 | — |
| 25 | q31 | 13.816 | 14.016 | — |
| 26 | dr_q31_32 | 14.016 | 14.366 | — |
| 27 | q32 | 14.366 | 14.566 | — |
| 28 | dr_q32_33 | 14.566 | 14.916 | — |
| 29 | q33 | 14.916 | 15.116 | — |
| 30 | dr3 | 15.116 | 16.689 | — |
| 31 | b3 | 16.689 | 18.089 | — |
| 32 | dr5 | 18.089 | 20.789 | — |
| 33 | sept_ex | 20.789 | 21.789 | — |
| 34 | ap_rect | 21.789 | 21.789 | [-0.01935, 0.01935, -0.01935, 0.01935] |
| 35 | m4 | 21.789 | 21.789 | — |
