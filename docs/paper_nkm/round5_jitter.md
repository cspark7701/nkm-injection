# Round-5 paired two-plane booster-jitter scan

Completed: 2026-11-01. [Protocol](round5_protocol.json); [manifest](revision_manifest_round5.json).

All five levels use 50 paired seed-42 realizations, 200 Gaussian particles each and 500 native turns, with ideal static centroid removal in both planes. Three missing levels (150 realizations, both models) were newly tracked; verified zero/full endpoints were reused. Sample IDs, particle seeds, corrected-ring identities, all non-jitter latent errors, calibration and scientific job fields match. Particle losses and capture counts reconcile for each model and realization. The frozen protocol identifies the distribution, Twiss/dispersion, energy spread, aperture and observation conventions.

| Jitter scale | NKM mean [%] | Uniform mean [%] | NKM change from zero [points; 95% CI] | NKM − uniform [points; 95% CI] | One-point test |
| :--- | ---: | ---: | :--- | :--- | :--- |
| 0 | 76.57 | 82.64 | +0.00 [+0.00, +0.00] | -6.07 [-8.89, -3.64] | reference |
| 0.1 | 74.22 | 82.86 | -2.35 [-4.32, -0.66] | -8.64 [-12.53, -5.39] | not demonstrated |
| 0.25 | 65.25 | 80.99 | -11.32 [-16.55, -6.58] | -15.74 [-21.25, -10.59] | not demonstrated |
| 0.5 | 51.54 | 74.30 | -25.03 [-33.12, -17.18] | -22.76 [-29.93, -15.96] | not demonstrated |
| 1 | 33.91 | 57.22 | -42.66 [-51.39, -33.84] | -23.31 [-31.74, -14.99] | not demonstrated |

No nonzero tested scale passes the declared one-point acceptable-loss test. At 0.1, the NKM change is −2.35 points (−4.32 to −0.66); the lower endpoint does not exceed −1. At quarter jitter, the model gap is −15.74 points (−21.25 to −10.59). Neither statement is a formal NKM-versus-uniform-kick noninferiority test. No level below 0.1 was evaluated, and no continuous threshold or hardware tolerance is inferred.

Intervals are pointwise paired realization bootstraps (10,000 resamples, seed 1729), conditional on the ten corrected rings. The strict test uses the unrounded lower central-95% endpoint and treats an exact-margin numerical tie as failure. Its central interval has the declared conservative 97.5% one-sided interpretation. The zero-jitter reference cannot demonstrate a usable nonzero tolerance.

At scales 0, 0.1, 0.25, 0.5 and 1 the NKM zero-capture fractions are 0, 0, 0, 8 and 28%; the uniform-kick fractions are 0, 0, 0, 0 and 10%. Each model’s cost, gap changes and mean intervals are retained in the selected analysis, with additional summaries in the supplement. The assumed full stress level is 0.5 mm / 0.2 mrad at extraction; both coordinates scale together. Ideal static removal does not remove shot jitter.

Tracking implementation at launch: `65bf56d`, recorded with script hashes in the selected implementation identity. Later portability/reporting checks are committed as `fd4b96b`; the tracking physics and actual launched commands are unchanged. Old protocols, selections and scientific source data remain unchanged.
