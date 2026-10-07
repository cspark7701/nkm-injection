# Milestone 92 — Task 07: Strict configuration serialization

Completed: 2026-10-07  
Task: [Harden the existing configuration serialization contract](../../05_refactor_tasks/07_strict_configuration_deserialization.md)

## Problem and outcome

The shared mixin silently ignored unknown fields, treated `"false"` as true,
truncated fractional integer inputs, suppressed annotation failures and encoded
unsupported objects as strings. JSON also permitted NaN/Infinity. Configuration
loading now validates declared types with field/index paths and rejects these
unsafe conversions. Explicit compatibility loading only ignores unknown fields.

## Implementation

- Moved the existing mixin implementation into `configuration.py`, preserving
  imports from `results_schema` and the package root. Publication hashing and
  manifest utilities remain in `results_schema.py`.
- Added strict-by-default loading for dictionaries, JSON and files; nested
  dataclasses retain defaults, validate supplied types and run domain hooks.
  Unresolved annotations and missing required fields are reported explicitly.
- Added explicit boolean parsing, finite/integral integer conversion without
  truncation, precision checks for numeric-to-float conversion, optional/general
  unions, type-sensitive literals, paths, typed collections and NumPy arrays.
- Reject unsupported values, nonfinite scalars/array elements, duplicate JSON
  keys and mapping-key collisions. Integer loss-histogram keys retain existing
  string encoding; typed integer mappings restore them on load. JSON values
  inside `Any` metadata retain JSON types.
- Encode only constructor fields; derived fields are recomputed. Serialization
  validates before opening a destination, preserving existing files on errors.
- Represent the two undefined no-loss distribution statistics as `None`/JSON
  `null` instead of NaN so valid no-loss ensemble results remain serializable.
  Other nonfinite results are still rejected rather than silently sanitized.
- Documented behavior, units, migration and compatibility in
  [configuration serialization](../../CONFIGURATION_SERIALIZATION.md), linked
  from README. Updated the ignored backlog and its task manifest.

## Verification

- Focused configuration/publication/convergence checks: **65 passed** in 5.91 s.
- Full suite after no-loss compatibility correction: **408 passed** in 53.41 s;
  final verification after the mapping-key collision safeguard: **408 passed**
  in 56.50 s.
- Used the existing pyat-dev Python 3.11 environment with
  `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`.
- Regression checks cover boolean strings, fractional/lossy numeric inputs,
  unknown/nested fields, tuples, paths, NumPy scalars/arrays, unions/literals,
  annotation failures, nonfinite/duplicate JSON, semantic round trips and
  preservation of existing destination bytes on encoding failure.
- A fresh Python process saved and reloaded BTS, MOGA, hardware-constraint and
  production configurations with exact dataclass equality. Generated config
  files reside only in `/tmp/nkm-task07-8a4c3ylv/`.
- Conversion and round-trip comparisons are exact; no numerical tolerance or
  unit conversion was introduced. Physics/domain tolerances remain unchanged.
- SHA-256 checks confirm all nine protected files match HEAD byte-for-byte.
  Git status/diff, whitespace and documentation-link checks completed. No full
  production simulation, protected input regeneration, remote interaction or
  push occurred.

## Compatibility

Existing correctly typed saved configurations retain their structure. Loading
legacy extras requires `strict=False`; unsafe values must be corrected explicitly.
Only dataclass configurations are supported; there are no repository users of
non-dataclass mixin subclasses. Unsupported annotations must be replaced with
supported types. Float strings retain ordinary binary floating-point parsing.
NumPy dtype is inferred on JSON loading, and metadata does not recover arbitrary
Python object types. No-loss statistic consumers must handle null explicitly.
Other NaN/Inf study outputs must be resolved by their producer before saving.
