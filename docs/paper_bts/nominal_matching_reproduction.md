# Matching reproduction — R1-BTS-06

Raw results: `results/bts_journal_campaign_r1_20261013/matching/`. [Selected optics/candidates](generated/matching.json). Reproduce using `python scripts/run_bts_journal_revision.py --stage matching --output-dir results/<new>/matching`.

The frozen archived 10-step model, seed42, 100-iteration/evaluation budget and nominal plus two uniform random box starts reproduce the original outcomes. Both stages have box bounds; beta, dispersion, pole-field and physical constraints are checked after search, not imposed as nonlinear constraints. Three descriptive starts are not a search reliability or volume estimate.

| Start | Optimizer success | Historical feasible | J | Peak beta x/y [m] | Termination |
| :--- | :--- | :--- | ---: | :--- | :--- |
| 0 | True | True | 1.2906e-13 | 31.4368/50.7459 | Optimization terminated successfully |
| 1 | True | False | 1.21461e-12 | 25.3292/62.5564 | Optimization terminated successfully |
| 2 | False | False | 1284.86 | 69.9212/65.0433 | The maximum number of function evaluations is exceeded. |

The installed raw and six-decimal archived settings are reevaluated using the independent hard-edge map and 40-step AT optics. Maximum absolute normalized optical residuals: raw 0.000117661; rounded 0.000407039. The declared engineering tolerance is each residual below its scale (beta .05 m, alpha .01, Dx .002 m, Dpx .001). Both meet that criterion, assumed K/peak-beta bounds, and positive five-sigma model-station clearance. Raw beta peaks are [31.43679621722258, 50.74589283947586]; raw minimum clearance 17.4546 mm. Six-decimal K values are numerical settings, not magnet calibration precision.

[Optics figure](figures/optics.pdf) shows beta, dispersion and full projected RMS size at element boundaries. These samples are not a continuous maximum-beta certificate inside every magnet. No sign/polarity hardware restriction beyond the stated symmetric bounds has been verified. Successful matching does not imply ring capture or measured chamber feasibility.
