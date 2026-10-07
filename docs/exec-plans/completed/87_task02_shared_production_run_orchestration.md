# Milestone 87 — Task 02: Shared production run orchestration

Completed: 2026-10-07  
Task: [Unify production configuration and stage output routing](../../05_refactor_tasks/02_production_run_orchestration.md)

## Problem and outcome

The shell runner accepted output/worker settings but forwarded them incompletely, and notebook 04 duplicated the pipeline using several nonexistent function imports. Both now use one configuration and stage runner. Every stage receives an exact output directory under a new run root. Injection and tolerance receive workers; unsupported stages are explicitly sequential. Publication receives a validated manifest built from this run's actual artifacts.

## Implementation

- Added `ProductionRunConfig`, ordered stage specifications and `run_production` with read-only preflight, fresh-output enforcement, injected test executors, per-stage logs, saved configuration/status and stop-on-failure behavior.
- Replaced the large shell implementation with an interpreter-selectable adapter and added a thin Python CLI. Notebook 04 uses the same runner and defaults to preview; notebooks 01–03 and protected notebooks remain unchanged.
- Added compatible output-directory options to inventory, field validation, slicing, optimization, MOGA and publication CLIs. Existing standalone defaults remain available.
- Passed the current optimization summary explicitly to tolerance analysis, including its saved targets, and recorded source provenance. The legacy standalone fallback remains Task 06 work.
- Routed generated injection/MOGA finalist lattices beneath their stage directories. Added an optional ring configuration to finalist reevaluation without changing other callers.
- Added an exact publication output option. When supplied, PDF compilation copies manuscript inputs into the run-local build directory and leaves sources unchanged; PDF compilation is opt-in in the shared runner.
- Added the original storage-ring MAT file to protected hash inventory.
- Documented job defaults, units, handoffs, compatibility and remaining scope in `docs/012_PRODUCTION_RUNNER.md`, and updated publication guidance and README.

## Verification

- Focused orchestration/publication/MOGA checks: **54 passed** in 20.97 s.
- Full suite in the existing pyat-dev Python 3.11 environment: **249 passed** in 47.82 s, with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1.
- Notebook preview executed successfully in a fresh Jupyter kernel without rewriting the notebook or creating a production run.
- CLI preview and shell invocation from another directory passed, including paths with spaces and explicit worker counts.
- Tests cover byte-for-byte dry-run/source preservation, invalid settings, missing inputs, script syntax failures, stage errors, missing outputs, invalid publication bundles, worker/CLI contracts, current-run tolerance strengths/targets, generated lattice paths and source-preserving PDF builds.
- Small inventory, field-validation and slicing stages executed under temporary output directories. No full production injection, optimizer, tolerance or MOGA study was launched for this task.
- Final git status/diff and whitespace/link checks confirm protected files remain unchanged and edits stay within development/documentation locations. No remote GitHub interaction or push occurred.

## Assumptions and remaining scope

Physics algorithms and their existing numerical tolerances are unchanged. Job seed controls slicing, deterministic optimization and tolerance; injection/MOGA retain their saved preset seed lists. A smoke injection tier does not reduce every pipeline stage. Production output directories cannot be reused.

Task 06 still covers the full tolerance configuration contract and removal of legacy standalone discovery. Task 11 still covers read-only standalone manifest initialization and strict PDF compiler error handling. This runner guarantees explicit artifact selection/output routing, not newly coupled BTS-to-ring physics or independent convergence validation.
