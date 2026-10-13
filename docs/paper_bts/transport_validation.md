# Independent transport validation — R1-BTS-05

Fresh numerical output: `results/bts_journal_campaign_r1_20261013/validation_02/`. [Selected results](generated/transport_validation.json) retain environment, code hashes, seed, tolerances and all checks. Reproduce with `python scripts/run_bts_journal_revision.py --stage validation --output-dir results/<new>/validation`.

The independent hard-edge map implements exact thick quadrupoles, sector curvature and edge focusing, translations, roll rotations and fixed-geometry dipole field perturbations, without AT matrix/optics calls. AT central-difference particle tracking is the independent numerical check. The comparison applies to small deviations about delta=0; it excludes nonlinear chromatic transport and longitudinal path-length claims.

The default 10-step AT integrator missed the declared 2e-6 map tolerance (4.0534e-6 maximum absolute discrepancy). Step convergence at 20/40/80 gives 2.5316e-7 / 1.5820e-8 / 9.8863e-10. New studies use 40 integration steps; historical studies retain their original settings. The failed first validation directory is preserved. The independent transverse symplectic error is 1.221e-15; the convention-sensitive 6D longitudinal block is not certified here.

Exit beta/dispersion and 50,000 Gaussian particles (seed71000, complete covariance in journal_config.json) agree within declared 1e-5 m beta, 2e-6 dispersion and 2% RMS tolerances. RMS tracking/linear ratios are [0.9989597266475145, 1.0015517060877375]. At delta +/-0.001, horizontal linearization errors are approximately 0.19 micrometres. A deliberately out-of-aperture particle first disappears after element1 at s=0, while the reference particle survives; (6,N) shapes and nonfinite first-loss accounting are checked.

| Isolated static error | Map discrepancy | Orbit discrepancy [m] | Exit x,y orbit [m] | Coupling norm |
| :--- | ---: | ---: | :--- | ---: |
| gradient | 1.58e-08 | 0 | [0.0, 0.0] | 0 |
| offset | 0.000139 | 8.2e-14 | [-5.83426264915482e-06, 0.0] | 0 |
| roll | 1.58e-08 | 0 | [0.0, 0.0] | 0.000302 |
| dipole | 0.000536 | 3.74e-13 | [0.00023183719266252575, 0.0] | 0 |

## Observable coverage

Gradient errors change optics and covariance. Translations drive orbit even when uncoupled Twiss mismatch is insensitive. Rolls couple planes; projected sizes use full covariance rather than separate Twiss alone. Dipole field error acts through PolynomB[0] at fixed design curvature; reference energy stays 4 GeV. Momentum jitter is a particle delta and includes bending response without double-rescaling K. Entrance beta errors change covariance with alpha fixed. Independent centroid jitter changes clearance/trajectory, not the betatron mismatch definition. New-model particle tracking tests nonlinear momentum dependence; linear maps are used for local clearance estimates only.

The historical evaluator does not activate every sampled source for every observable; its near-zero alignment/roll mismatch does not establish hardware tolerances. Longitudinal magnet placement, supply quantization, emittance jitter and downstream NKM/ring terms are excluded from the new parametric comparison and no tolerance claim is made for them. No source is silently counted as a physical benefit. Invalid map/particle evaluations fail the new driver rather than enter successful statistics.

Regression verification: 13 BTS lattice/journal tests passed, including independently implemented maps, translations, coupling, zero fields, covariance, shapes and first-loss accounting.
