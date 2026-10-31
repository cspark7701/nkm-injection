# Milestone 285 — R5-BTS-02: headline estimator and rare-loss validation

Completed: 2026-10-31. Round-5 task R5-BTS-02 (Reviewer 2 R2D-03; Reviewer 1 R1D-BTS-01; R2D-08, sparse counts).

**Estimator,** declared in `round5_protocol.json` before the shared-noise runs:
- **Estimand:** the gain is the ratio of the population means of the jitter-integrated loss (matched reference over
  loss-based).
- **Interval:** a paired realization bootstrap, with 10 000 resamples, the same realization indices for both
  settings, and seed 97005.
- **Population:** the second fresh test, rerun with shared reading errors.
- **Zero denominators:** none occurred.

**Results.**
- **Primary population:** 1.32 % against 0.295 %, so G = 4.48 [4.33, 4.63].
- **Layout population:** G = 4.59 [4.46, 4.72].

**Validation,** tracked counts against the Gaussian prediction conditional on the sampled shots, as Poisson z:

| Setting | Observed | Expected | z |
| :--- | ---: | ---: | ---: |
| Matched reference | 11 673 | 11 705 | −0.3 |
| Low beta | 10 104 | 10 154 | −0.5 |
| Loss-based | 942 | 880.5 | +2.1 (6.5 % excess; above even the union bound of 880.7; cause not resolved) |
| Dispersion-free | 1 | 0.51 | — |

For the dispersion-free row, the jitter-integrated loss corresponds to 76 particles.

**Article.**
- **Section 3.3** defines the four loss quantities and their conditioning: the error-free objective, the
  jitter-integrated loss (linearized transport, nominal covariance, max-event surrogate), the shot-conditional
  prediction, and the tracked count. It also defines the estimator and the primary population.
- **Abstract and Discussion.** The factor-of-3-to-10 headline is replaced by 4.48 (4.33–4.63).
- **Section 4.3** reports both gains and the validation. The earlier tracked gains (3.3–11) are attributed to
  sampling of the jitter tail.
- **The 1 % claim** is restricted to the steering and first-test rows, and the second-test loss-based excess is
  stated.
- **Dispersion-free result.** The count is reported with its denominator and conditional expectation. The test is
  stated not to check the integrated tail. Non-Gaussian tails are "could", not "would dominate".
- **"Averaged exactly"** is qualified as Gaussian averaging within the linearized transport and the nominal
  covariance.

The prose follows the humanizer rules. The isolated build is clean. Protected files are unchanged.
