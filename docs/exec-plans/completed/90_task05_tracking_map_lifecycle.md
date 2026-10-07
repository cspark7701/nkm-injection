# Milestone 90 — Task 05: Call-local one-turn tracking maps

Completed: 2026-10-07  
Task: [Remove hidden stale one-turn-map caching](../../05_refactor_tasks/05_tracking_map_cache_lifecycle.md)

## Problem and outcome

Multi-turn injection cached M66 on a function attribute keyed by lattice identity. In-place changes to a ring could silently reuse its old map, and callers shared implicit state. Tracking now computes one map per call outside the turn loop, ensuring each call uses current lattice physics without sharing Python cache state.

## Implementation

- Removed the identity-based function cache and computed `ring.find_m66(dp=0.0)` once for each positive-turn call. Reused the local map only across that call's turns.
- Preserved zero-turn behavior, public signatures, result schemas, kicker timing, reference momentum, apertures and loss accounting.
- Documented particle units, the requirement to leave a lattice unchanged during a call, compatibility and benchmark cost in [tracking map lifecycle](../../TRACKING_MAP_LIFECYCLE.md). No prepared context or replacement cross-call cache was added.
- Reviewed error application: perturbed lattice factories already construct new lattices and need no invalidation API.
- Updated README and the ignored Task 05 backlog status/manifest.

## Verification

- Initial focused lifecycle/injection/paper/convergence run: **43 passed** in 6.20 s.
- Ten lifecycle regressions cover same-ring quadrupole, drift-length and roll mutations, observed energy changes, alternating rings, shared/independent concurrent calls, one map per call, ignored legacy cache attributes, zero turns, input preservation and loss identities.
- Fresh-map coordinate comparisons use zero relative tolerance and absolute tolerance `1e-14`. Existing physics and convergence tolerances are unchanged.
- A fresh Python process checked same-ring quadrupole mutation against a freshly computed map. It also compared unchanged-ring results before/after the refactor: final coordinates were identical (maximum absolute difference zero).
- A five-call warm benchmark on the source ring used 20 Gaussian particles, ten turns, seed 42 and an off kicker. Old cached median: **0.001436 s/call**; new call-local median: **0.167295 s/call**, about **0.166 s** additional map setup. All particles survived. Detailed beam units, apertures, loss definition and observation point are recorded in the lifecycle guide and temporary benchmark JSON.
- Benchmark outputs and the previous implementation copied for comparison remain under `/tmp/nkm-task05-map-lifecycle-20261007/`; scientific inputs were not overwritten or regenerated.
- Final focused lifecycle tests: **10 passed** in 0.92 s. Final full suite: **342 passed** in 51.37 s, without warnings, in the existing pyat-dev Python 3.11 environment with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1.
- SHA-256 checks confirm all nine protected source/input files match HEAD byte-for-byte. Final git status/diff, whitespace and new documentation-link checks pass.

## Assumptions and remaining scope

A ring is unchanged during an individual call, and each call retains the existing linear one-turn approximation. Concurrent regressions use controlled map providers to isolate function state; backend process-worker policy is unchanged. Recomputing costs an extra map setup per call, measured above on a small ensemble rather than a full production run.

No notebook integration, result-schema migration, full production study, remote GitHub interaction or push was required.
