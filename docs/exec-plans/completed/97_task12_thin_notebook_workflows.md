# Milestone 97 — Task 12: Configured notebook study workflows

Completed: 2026-10-07  
Task: [Extract remaining notebook simulation logic into reusable workflow functions](../../05_refactor_tasks/12_thin_notebook_workflows.md)

## Problem and outcome

Notebook 01 contained local geometry, objectives, constraints and tracking loops
with hidden cross-cell state and implicit root-file result fallbacks. Notebooks
02/03 duplicated path/configuration summaries, depended on generated lattice
files or wrote to a fixed relative output directory. Retained MOGA plots used a
nonexistent result field and inferred representative strengths ambiguously.

Notebooks now select complete configurations, execute reusable studies and plot
returned results. Notebook 01 has nine code cells and 84 code lines, down from
79 code cells and approximately 1,619 lines. Notebook 02 and optional notebook
03 execute independently. Notebook 04 continues using the shared production
runner and now shares repository/fresh-output resolution.

## Implementation

- Added `NotebookBTSConfig` and its constructor, preserving the original
  exploratory geometry, 36-element order, 108-element aperture layout, entrance
  optics and fixed q34. This remains distinct from canonical production BTS.
  Repeated dipoles are independent instances with unchanged initial transport.
- Added configured Gaussian beam, main and injection studies, structured returned
  `NotebookStudyResult` data, read-only repository/path selection and fresh-run
  execution with source hashes, strict configuration JSON and completion/failure
  reports. Existing destinations and outputs inside checkout sources are rejected.
- Reused shared normalized residuals and optimization with an optional lattice
  argument and subclass-aware residual evaluation. The notebook objective retains
  raw beta/alpha squared errors plus optional horizontal dispersion, omitting its
  derivative; endpoint beta margins are distinct from full physical feasibility.
- Saved effective ring/matching configurations. Ring generation uses the original
  protected MAT input and writes only into the new run, with no root-generated
  lattice or previous notebook dependency. Caller configurations remain unchanged.
- Extracted BTS single-pass tracking, preserving finite coordinates and original
  particle loss identity, with explicit unknown loss element locations.
- Replaced handwritten NKM/ring loops with shared validated symplectic/RK4 and
  multi-turn tracking APIs. Thick output is a separate comparison; injection
  uses a first-turn-only kick and configured one-turn map/apertures.
- Added reproducible, explicitly limited nine-quadrupole relative-gradient error
  studies. Each sample reconstructs the configured geometry; invalid evaluations
  retain diagnostics with null merit. Full production error studies remain in 04.
- Retained optional native AT acceptance with explicit grid/amplitudes/turns and
  returned/saved run-local arrays; removed cached-root/synthetic-zero fallback.
- Wrapped independent optional MOGA execution with complete settings, actual
  constraint diagnostics, termination/feasibility reports and archived populations.
  Fixed plots to use `envelope_risk` and returned representative strength arrays.
- Preserved phase-space, field, optics, survival, stored-centroid and Pareto plots.
  Figures save before inline display can close them. Notebook source outputs are
  cleared; executed smoke copies are separate artifacts.
- Added `scripts/smoke_notebook_workflows.py`: separate clean kernels using the
  invoking interpreter, reduced settings, fresh outputs and a saved smoke report.
- Documented scientific assumptions, migration and units in
  [notebook workflows](../../NOTEBOOK_WORKFLOWS.md) and linked from README.

## Compatibility and scientific limits

Existing canonical package APIs/default algorithms remain unchanged; the
optimizer's lattice argument is optional. Notebook 01's previously implicit
pickle/JSON fallback is replaced by configured strengths and optional explicit
optimization. Its original target/handoff scaling remains exploratory, with
complete settings recorded. Nine bounds [-5, 5] m^-2 accommodate nominal q32.

The former first-order loop labelled RK4 used the opposite kick sign and updated
delta from ct. The shared validated integrators intentionally replace it;
equivalence to that loop is not claimed. Multi-turn 01 now follows 02's shared
linear-map/first-turn-kick convention, replacing repeated kicks and negative
backtracking. The separate native acceptance diagnostic now observes the
configured NKM ring entrance, rather than the old after-NKM cache. These model
changes and the limited gradient-error scope are explicit in documentation.

MOGA retains its scientific algorithm/schema; wrapper diagnostics distinguish
active hardware/peak-beta inequalities from evaluator-only constraints. The
wrapper does not activate previously unused configuration fields.

## Validation

Environment: project `pyat-dev`, Python 3.11, single-thread BLAS/OMP.

- Original notebook characterization was captured before extraction into
  `tests/fixtures/notebook_bts_characterization.json`: element order, length,
  transfer matrix, two candidate objective/endpoint-beta evaluations, and
  single-pass particle coordinates/losses.
- Original raw objective and endpoint beta margins agree at rtol/atol 1e-10.
  Transfer matrix agrees at rtol/atol 1e-10; lattice length at atol 1e-12 m.
  Finite transport coordinates agree at rtol 1e-10, atol 1e-12. Loss indices
  are exact; lost columns are normalized to shared all-NaN markers.
- Notebook 02 extracted tracking agrees with direct shared calls at rtol/atol
  1e-12, including exact histories and loss logs. Repeated seeded main/MOGA
  results are exact, excluding wall-clock runtime.
- Focused notebook/optimization suite: **70 passed** before four additional
  coverage/loss/notebook-boundary/acceptance regressions were added.
- Final full suite: **600 passed in 74.80 s**, with no warnings.
- All four maintained notebooks executed in separate clean kernels from source
  with saved outputs discarded. Main/injection: 16 particles and two turns;
  main: four slices and two gradient samples; MOGA: population four and two
  generations. Notebook 04 remained a read-only production preview.
- Final smoke artifacts: `/tmp/nkm-task12-clean-kernels-verified/`, including
  executed notebook copies, summaries, configurations, arrays and **5/4/4 saved
  figures** for notebooks 01/02/03. No prior notebook outputs were required.
- Optional native acceptance parameter routing is covered by a focused regression;
  full native acceptance and production-size studies were not executed.
- All **nine protected files** match HEAD by SHA-256. Repository results
  snapshot: **79 files and directory membership unchanged**. All generated
  study artifacts are inside new temporary run directories.
- `git diff --check` passed. Backlog status/manifest and completed archive index
  updated in numerical sequence. No commits, pushes or remote GitHub calls.

Public interfaces document m, rad, eV, T, T m and m rad; the existing thick-tracker
GeV conversion and display mm/mrad conversions are explicit. No protected source
input or historical simulation result was regenerated or migrated.
