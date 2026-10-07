# Milestone 94 — Task 09: Shared tracking input contracts

Completed: 2026-10-07  
Task: [Centralize integrator and particle-array input contracts](../../05_refactor_tasks/09_tracking_boundary_contracts.md)

## Problem and outcome

Integrator constructors duplicated setup and divided by unchecked slice counts.
Tracking/statistics assumed coordinate shape and treated any NaN in x as loss,
without distinguishing malformed coordinates. Integer beams failed during float
updates, and element-backend losses were omitted from the explicit loss log.

Tracking now shares validated parameters, array boundaries, component checks and
transverse drift. The split and RK4 algorithms remain separate. Valid lost
columns retain original indices/coordinates; invalid coordinates and numerical
corruption raise errors rather than becoming silent physical losses.

## Implementation

- Added immutable `TrackingParameters`, requiring positive integer slice counts,
  finite nonnegative length/scale, positive energy and nonzero finite charge.
  Existing GeV interfaces explicitly convert to eV and require finite positive
  rigidity in T m. Both charge signs remain supported.
- Centralized `(6,N)` float64 particle validation for thin/thick/ring tracking,
  `TrackingResult.from_beam` and beam statistics. Integer inputs are converted;
  complex/object/bool storage, wrong shapes, Inf and malformed partial NaNs fail.
  Empty beams and all-lost beams remain supported.
- Defined all-NaN and NaN-x/five-finite-coordinate loss markers, preserving
  their values and column order. Tracking does not mutate caller inputs.
- Shared integrator constructor setup and transverse drift with thin tracking;
  field/kick components must be finite real values with compatible broadcasting.
  Zero scale performs pure drift without evaluating fields; zero thick-element
  length returns an independent copy.
- Required positive integer turn counts before lattice access and validated ring
  energy, length, charge, scale and apertures. One-turn maps must be finite 6x6
  arrays. Numerical overflow in active coordinates raises explicitly.
- Tracked only active columns through individual elements. Normalized the native
  AT aperture pass's backend-only `ct=+Inf` sentinel to all-NaN, recorded new AT
  losses once with original particle/turn/element identities, and preserved
  initial lost indices in result metadata. Backend event x/y coordinates are the
  last finite element-entrance values; no internal impact point is inferred.
- Allowed zero NKM geometric length in configuration domain validation. Updated
  zero-turn/configuration regressions and current map-lifecycle documentation.
- Documented units, accepted loss markers, limits, numerical tolerances and
  migration in [tracking input contracts](../../019_TRACKING_INPUT_CONTRACTS.md),
  linked from README. Updated ignored backlog completion records.

## Verification

- Initial affected integration/injection/aperture/map checks: **29 passed** in
  3.10 s. Focused contracts/integrator/configuration/map checks subsequently
  passed; final verification includes all added cases and corrections.
- Final full suite: **520 passed** in 62.25 s using the existing pyat-dev Python
  3.11 environment with `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`.
- Added 104 contract regression cases covering shape/transposition, integer
  inputs, empty/lost beams, Inf/partial NaNs, count/parameter rejection, finite
  field components, native AT loss identity, overflow and zero-length configs.
- Drift/uniform-field/charge-sign checks use zero relative tolerance and absolute
  1e-14. Linear-field analytic focusing at 4 GeV, length 0.5 m and 80 slices uses
  absolute 1e-9 for split and 1e-14 for RK4, with zero relative tolerance.
  Existing nonlinear convergence and two-plane kick tolerances remain unchanged.
- A fresh Python process tracked a 16-particle Gaussian beam (seed 23) with
  beta_x/beta_y=10/5 m, alpha=0, emittances=1e-8/1e-9 m rad, rms relative energy
  spread=1e-3 and bunch length=0.01 m at 4 GeV. Both zero-field integrators matched
  a 0.3 m transverse drift within 1e-14.
- The same smoke process inserted one initially lost column and one particle
  outside a +/-0.01 m AT aperture, observed after each pass for two turns with
  the kicker off. Fourteen survived; exactly one new loss was logged with its
  original index. Validation settings/results are saved only in
  `/tmp/nkm-task09-53cwkicn/validation.json`.
- All nine protected source/data files match HEAD byte-for-byte by SHA-256.
  Final git status/diff, whitespace and documentation links were checked. No
  notebook, protected input, full production study, remote interaction or push
  was involved.

## Compatibility and limitations

Zero-turn calls now fail; use initial beam statistics or
`TrackingResult.from_beam` instead. Integral float counts require explicit
verified conversion to integers. Negative scales are rejected. JSON result
metadata adds initial lost indices and logs previously omitted backend losses;
no saved historical artifacts are rewritten.

This refactor retains existing transverse integration models, longitudinal
coordinates and aperture/observation conventions. It does not implement new
error mechanisms, finite-energy longitudinal dynamics or statistical treatment
of undefined emittance. Those numerical models and convergence interpretation
remain separate work.
