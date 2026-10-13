# Clearance accuracy — R2-BTS-03

[Summary](generated/round2_accuracy.json), reproducible by `python scripts/run_bts_round2.py --stage accuracy --output-dir results/<new>/accuracy`. All600 original shots and both settings are compared at each aperture, using uncensored AT central-difference Jacobians expanded about actual shot centroids. Small probes are not discarded at station limits.

The maximum station affine-versus-centred discrepancy is78.433 micrometres, but the paired mean changes only -0.1553 micrometres. Centred mean14.4549 micrometres,95% interval[-17.8772,+48.0961] micrometres, retains the original unresolved benefit. Active stations change in8 reference and3 low-beta shots: scalar agreement alone would conceal these switches. Both results are preserved; new comparisons use centred AT maps.

Four actual extreme/representative shots, both designs, check probe steps1e-6/1e-7/1e-8 and40/80 integration steps. Maximum station changes are1.85e-6 and4.12e-6 micrometres respectively. Product Gauss-Hermite quadrature orders3/5/7 tracks the unrestricted complete five-dimensional Gaussian through nonlinear AT. Orders5/7 converge in centroid-plus-five-RMS clearance to3.32e-11 micrometres; maximum centred-versus-nonlinear-moment discrepancy is0.606 micrometres on these cases. This finite-case accuracy check is far below the approximate33-micrometre half-interval and the declared100-micrometre decision scale, not a universal bound on arbitrary machines or loss tails.

Offset/dipole affine maps reproduce translation/forcing accurately but omit momentum-dependent derivatives about displaced trajectories. Excellent orbit agreement and nominal maps therefore do not imply identical perturbed Jacobians. All map mixed-unit norms remain diagnostics; the assessment uses clearance in micrometres. Covariance predictions remain local linearizations; representative nonlinear-moment checks and stated limitations accompany their use.

The original scientific environment was located for execution: Python3.11.9,pyAT0.7.2.dev26+g4701d48c.d20260831,NumPy2.4.6,SciPy1.17.1. This extends the review's saved-record checks with fresh tracking without altering any historical report.
