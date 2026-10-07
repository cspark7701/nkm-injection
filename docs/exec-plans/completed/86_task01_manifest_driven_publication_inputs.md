# Milestone 86 — Task 01: Manifest-driven publication inputs

Completed: 2026-10-07  
Task: [Make publication artifacts consume selected simulation runs](../../05_refactor_tasks/01_manifest_driven_publication.md)

## Problem and resulting behavior

Previously, the paper pipeline validated a manifest but generated tables and figures from default BTS optics. It now loads exact named artifacts from all six selected stages into validated typed publication inputs. Selected strengths, saved entrance/target optics, per-quadrupole bounds and beam settings control optics tables and plots. Injection, tolerance, MOGA, field-validation and slicing metrics feed additional tables and figures.

## Implementation

- Added `src/nkm_injection/publication_inputs.py`: read-only stage adapters, complete saved configuration requirements, finite/range/shape checks, explicit legacy mm/mrad-to-SI conversions and resolved artifact paths/full SHA-256 hashes.
- Updated `paper.py`: selected inputs passed to both generators; seven tables, four figures, numerical figure data and upstream provenance. Existing filenames and two-argument nominal-reference generators remain supported with explicit reference labels.
- Updated the optimization producer to save the complete lattice, target and constraint configuration plus schema version 1.
- Added temporary publication fixtures and regression tests. Changed existing pipeline tests to consume isolated complete inputs rather than repository baseline directories.
- Documented schemas, assumptions, units, behavior changes and historical-run migration in `docs/PUBLICATION_INPUTS.md`; linked it from README.

## Validation

Full-suite verification passed: **222 tests** in 231.17 s. Final focused publication verification passed: **43 tests** in 17.90 s, including the additional mismatch-roundoff and fresh-process checks. An earlier full-suite run also passed (221 tests before the final regression additions). `git diff --check` and completion-link validation passed. The publication regression suite checks two different manifests, exact table values, plotted aperture boundaries, changed optical functions and envelopes, source byte preservation, upstream hashes, missing/malformed inputs, unavailable zero-survivor perturbation, documented mismatch roundoff and execution in a fresh Python process. Values use atol 1e-12; optical-function/envelope differences use rtol 1e-8 and atol 1e-10. Dimensionless mismatches between -1e-12 and zero normalize to zero, with that tolerance recorded in provenance.

The `pyat-dev` Python 3.11 environment was used. Publication CLI `--help` executes successfully. No full production study, historical-result rewrite, notebook edit, protected-file modification, remote GitHub interaction or push was performed.

## Compatibility and remaining scope

Incomplete legacy optimization metadata or a manifest pointing at baseline directories now fails clearly; the pipeline cannot silently replace missing selected results with nominal calculations. Historical metadata must be verified before copying it into a new result bundle. Existing protected source files and generated historical results remain untouched.

Production stage handoffs (Tasks 02/06), read-only manifest initialization and PDF build isolation (Task 11) remain separate tasks. Provenance shows which artifacts were consumed but does not assert that independently selected stages share an upstream optimization. The AP1 plot reference is a saved half-aperture, not element-resolved acceptance. Publication PDF compilation behavior is unchanged.
