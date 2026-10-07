# Milestone 93 — Task 08: Canonical package imports

Completed: 2026-10-07  
Task: [Standardize imports and reduce package initialization coupling](../../05_refactor_tasks/08_canonical_package_imports.md)

## Problem and outcome

Maintained scripts/tests/notebooks mixed `src.nkm_injection` and the installed
`nkm_injection` namespace, allowing duplicate module and class identities.
Package initialization eagerly loaded tracking, optimization, plotting and
optional MOGA even when only units or serialization were requested.

All maintained callers now use the installed namespace. The package root lazily
resolves its existing public exports to their canonical submodule objects. The
legacy namespace fails before loading submodules, preventing duplicate classes.

## Implementation

- Converted scripts, tests and notebooks 01–04 to canonical imports, including
  local shell/workflow embedded Python. Removed per-file `sys.path` mutations;
  existing source-root variables still locate scientific inputs.
- Added lazy export lookup/caching and public `__all__`/`__dir__` while preserving
  every previously imported root API object. Package-only import loads no
  subsystems; units and configuration imports avoid AT, SciPy, Matplotlib and
  optional pymoo. Requested subsystems still load their own dependencies.
- Added the installed `nkm-production` console entry point and shared CLI
  adapter. Its `--repo-root` selects source inputs/scripts and defaults to the
  current directory. The existing script adapter defaults to its own checkout.
  Production routing, options, dry-run behavior and physics remain unchanged.
- Documented editable/wheel installation, script/notebook execution, lazy
  behavior and migration in [package imports](../../PACKAGE_IMPORTS.md), linked
  from README and installation guidance. Legacy pickle paths require explicit
  recovery in their original environment; JSON structure is unchanged.
- Added fresh-process tests for dependency isolation, export/class identity,
  explicit legacy-name rejection, maintained-source imports and all four
  notebooks' package imports. Updated the ignored backlog and task manifest.

## Verification

- Existing suite after canonical migration: **408 passed** in 50.15 s.
- Focused import regressions: **8 passed** in 5.68 s.
- Final full suite: **416 passed** in 55.11 s using the existing pyat-dev Python
  3.11 environment with `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`.
- Built and installed both editable and wheel copies offline in separate
  temporary venvs sharing the existing scientific dependencies. Wheel build
  used a temporary source snapshot; no dependency downloads or base-environment
  installation changes were needed.
- From outside the checkout, both installs verified actual package origins,
  lightweight import isolation and shared class identities. Each passed
  **11 script --help checks**, **four notebook package-import checks**, console
  entry-point help and a complete read-only production preview. Wheel imports
  came from its venv's site-packages rather than the checkout.
- Temporary installation/build artifacts are under
  `/tmp/nkm-task08-install-0lt5sy6q/`. Preview output directories were not created.
  Existing full-suite tests also execute notebook 04's complete dry-run workflow
  and small production stages from fresh processes.
- Notebook changes are limited to imports and import-path setup. All four
  notebooks' outputs, metadata and non-source content match HEAD. Notebook 01
  changes are necessary to integrate the canonical namespace; no protected
  root notebook was edited or executed.
- SHA-256 comparisons confirm all nine protected scientific/source files match
  HEAD byte-for-byte. Final git status/diff, whitespace and new documentation
  links were checked. Only local shell/workflow source was edited; no remote
  GitHub endpoint, full production study, push or source regeneration occurred.

## Compatibility and numerical interpretation

Install into the interpreter/kernel used for execution. The legacy namespace
and ad hoc uninstalled path bootstrapping are intentionally unsupported; update
imports and restart running processes. Direct scripts remain supported after
installation. Wheel production execution requires `--repo-root` pointing at a
source checkout because scientific data and orchestration scripts are not
bundled in the wheel.

Existing public exports and class identity are checked exactly. This task
introduces no numerical tolerance, unit conversion, seed change or physics
algorithm change. Interfaces retain m, rad, eV, T and T m and existing explicit
GeV/mm conversions. Import smoke checks do not claim to rerun full scientific
notebook studies; existing numerical tests retain their established tolerances.
