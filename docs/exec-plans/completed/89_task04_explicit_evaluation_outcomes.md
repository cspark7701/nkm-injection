# Milestone 89 — Task 04: Explicit evaluation outcomes

Completed: 2026-10-07  
Task: [Replace silent model substitutions with explicit evaluation outcomes](../../05_refactor_tasks/04_explicit_evaluation_failures.md)

## Problem and outcome

Robustness always used a hard-coded linear surrogate because its field-map factory call omitted the map. Setup/query exceptions and other evaluation errors were hidden as alternate physics or large mismatches. Normalized objectives and optimizer wrappers caught programming errors as penalties, and failed loss-position queries fabricated zero positions.

Evaluation now preserves selected model provenance and distinguishes valid physics, physical infeasibility and invalid numerical evaluations. Unexpected/configuration errors propagate with context. Missing positions remain explicit.

## Implementation

- Added JSON-compatible EvaluationOutcome records with status, sample/candidate identity, physical failure reasons, exception type/message/phase and model provenance. Nonfinite numerical identities serialize as null.
- Made robustness load the actual selected field map, with SHA-256 and metadata provenance. Used evaluate_kicks in rad before converting stored-kick diagnostics to mrad. Alternate linear/ideal/off models require explicit selection; setup/query failures never change models.
- Added all applicable physical threshold reasons. Invalid sample metrics are null and excluded from percentiles/bootstrap intervals; physical failure probability uses valid evaluations, while feasible fraction uses all requested samples. Invalid counts, fractions, sample results and schema version are saved separately.
- Added normalized-objective outcomes and retained penalties only for expected floating-point/linear-algebra failures. Validated target configuration, candidate shape and finite numerical optics/residual outputs. Programming/configuration errors and ambiguous pyAT errors propagate.
- Updated optimizer wrappers so they cannot turn those propagated errors back into penalties. Added structured candidate outcomes with restart index/seed and retained final-evaluation exceptions in candidate records. Robust candidates with invalid samples receive explicit invalid penalties.
- Added sample/category context and finite optics checks to OAT failures without inventing rankings.
- Added explicit model/path options to the tolerance CLI. Invalid ensembles save diagnostic summaries, skip OAT and exit unsuccessfully; publication validation rejects declared invalid tolerance evaluations.
- Replaced fabricated loss positions with null values and coverage/exception metadata. Retained supplied zero positions and allowed programming errors to propagate.
- Documented units, thresholds, statistical denominators, additive fields and historical model migration in [evaluation outcomes](../../EVALUATION_OUTCOMES.md); updated README and the ignored Task 04 backlog status/manifest.

## Verification

- Existing optimization/error-model checks: **76 passed** in 18.91 s.
- Focused failure-injection, aperture, production-runner and publication checks: **78 passed** in 16.52 s before the final serialization regression was added.
- Final full suite: **332 passed** in 47.38 s in the existing pyat-dev Python 3.11 environment, with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1.
- Serial/process-worker tests cover missing maps, out-of-domain coordinates, singular optics and unexpected callback errors, asserting sample identity, exception phase and unchanged model selection.
- Additional tests cover explicit alternate models, valid/infeasible/invalid aggregate separation, normalized penalties and unexpected error propagation through optimizer wrappers, candidate restart diagnostics, nonfinite identities, unknown loss positions and CLI/publication rejection.
- A fresh Python process evaluated a fixed-seed two-sample ensemble sequentially and with two process workers. Results were identical; a subsequent outside-domain sample was identified as invalid. Strict JSON output was saved only under `/tmp/nkm-task04-evaluation-20261007/`.
- SHA-256 comparisons against HEAD confirm all nine protected source/input files are byte-for-byte unchanged. Final git status/diff, whitespace and new documentation-link checks pass. No full production study, source regeneration, external installation changes, remote GitHub interaction or push occurred.

## Compatibility and scientific interpretation

Successful-result fields remain available, with additive outcome/candidate metadata. Partial/all-invalid evaluations introduce null metrics and explicit counts; consumers must check validity before using physics statistics. Physical threshold values and existing numerical test tolerances are unchanged; failure-mode counts now include overlapping reasons.

Previous field-map robustness results need regeneration to claim field-map provenance because the old path always used a linear surrogate. Corrected stored-beam kick values can differ. Legacy summaries without validity counts remain readable; historical validity is not inferred. Broader configuration handoff and convergence-method work remain Tasks 06 and 10.
