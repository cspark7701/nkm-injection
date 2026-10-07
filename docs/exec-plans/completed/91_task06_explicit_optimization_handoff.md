# Milestone 91 — Task 06: Explicit optimization inputs for tolerance studies

Completed: 2026-10-07  
Task: [Make tolerance studies use an explicit optimization input](../../05_refactor_tasks/06_explicit_optimization_handoff.md)

## Problem and outcome

Standalone tolerance studies discovered the lexicographically latest global optimization and silently substituted default strengths/targets. The production runner already supplied its own summary, but configuration validation/provenance was incomplete. Error application also discarded selected geometry and entrance optics, and OAT used a hidden default budget/count.

The CLI now requires a selected summary or explicit reference mode. Both summary/configuration files are validated and hashed. Monte Carlo and OAT retain the selected lattice, entrance/target optics, error budget and recorded seeds/counts.

## Implementation

- Added a read-only optimization handoff validating complete schema-1 BTS/target/constraint configurations, nine finite named/ordered strengths, positive consistent beam energy, canonical units, bounds and declared final feasibility. Contradictory reported final beta/total-mismatch values are rejected using the optimizer's existing tolerances.
- Removed global run discovery and fallback strengths/target literals. Added explicit `--reference`; missing selection is a CLI error. Production routing continues to pass its current optimization summary.
- Added complete optional `--error-config`, configurable `--oat-samples` and `--oat-seed`, and saved summary/config/error-file hashes plus complete nominal/error/target/constraint configurations, named strengths, entrance optics, units and sampling metadata.
- Preserved magnet/drift geometry, bends, apertures and energy during error application by replacing strengths/energy on the selected configuration. Both Monte Carlo and OAT propagation use the selected entrance Twiss values; OAT reference propagation uses the same entrance.
- Passed saved peak-beta/total-mismatch limits with the optimizer's 0.01 m/0.05 feasibility tolerances. Low-level robustness defaults remain backward compatible; actual definitions/tolerances are recorded in evaluation metadata. OAT labels now reflect its selected budget.
- Added explicit units/names and a named raw-strength mapping to new optimization outputs. Complete existing schema-1 outputs remain supported through their documented units/order; older incomplete metadata requires a verified new copy.
- Required new/empty tolerance output directories, retained complete handoff metadata for invalid evaluation diagnostics, and updated affected test adapters for the explicit API contract.
- Documented input selection, reconstruction, units and migration in [tolerance inputs](../../TOLERANCE_INPUTS.md); updated README, production/procedure/evaluation guidance and ignored backlog status/manifest.

## Verification

- Existing error/optimization/evaluation/production checks: **79 passed** in 26.86 s.
- Focused handoff/evaluation checks after feasibility consistency work: **56 passed** in 8.33 s.
- Final full suite: **372 passed** in 66.68 s in the existing pyat-dev Python 3.11 environment, with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1.
- Tests select an explicit older synthetic run despite newer names/timestamps, preserve input bytes, reject malformed/nonfinite/infeasible strengths and incomplete/inconsistent configurations, and reconstruct nominal/error configurations and Monte Carlo/OAT seeds.
- Real serial/process-worker checks verify custom entrance optics and thresholds; zero-error OAT checks use absolute tolerance 1e-12, as do fresh mismatch comparisons. Existing physics tolerances remain unchanged.
- A fresh-process CLI run used explicit reference mode, two Monte Carlo samples (seed 17), two OAT samples per category (seed 19) and two workers, writing only beneath `/tmp/nkm-task06-reference-20261007/`. It completed with zero invalid evaluations and two physically infeasible samples, preserving the distinction. Saved configurations and sampling metadata were checked for reconstruction.
- SHA-256 checks confirm all nine protected source/input files match HEAD byte-for-byte. Final git status/diff, whitespace and new documentation-link checks pass. No protected input regeneration, full production study, remote GitHub interaction or push occurred.

## Compatibility and interpretation

Standalone no-input commands must choose a summary or reference mode. Results may change when custom geometry/entrance optics were previously dropped and when the selected optimizer's total-mismatch criteria differ from the legacy fixed per-plane threshold. No historical results are migrated or regenerated.

The handoff checks consistency of declared feasibility; it does not rerun an optimization or independently certify all historical hardware/beam constraints. Monte Carlo retains its existing beta/mismatch/capture assessment scope, rather than adding missing error mechanisms or full envelope/aperture tracking. General configuration deserialization remains Task 07; convergence methodology remains Task 10.
