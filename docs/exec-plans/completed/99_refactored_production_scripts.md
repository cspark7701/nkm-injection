# Milestone 99 — Production scripts after refactoring

Completed: 2026-10-07

## Outcome

Updated `scripts/run_full_production_simulation.sh` to invoke the installed
`nkm_injection.cli` with an explicit source checkout and the selected interpreter.
The compatible Python source adapter and notebook 04 continue to use the shared
production configuration and orchestration.

All eight stages accept the selected checkout. Shared stage helpers select fresh
microsecond destinations, reject occupied/source destinations and calculate full
source SHA-256 digests. Generated injection and MOGA lattices use the selected
original MAT source and stay inside their stage outputs. Missing injection maps
stop execution instead of silently choosing an ideal fallback. The explicit
comparison models and production physics defaults remain unchanged.

The runner routes tier workloads, the base seed, Monte Carlo/OAT counts and the
complete statistical policy. Default production budgets remain 1000 slicing
particles, five injection seeds with 10000 particles/1000 turns, three BTS starts,
100 Monte Carlo samples, 30 OAT samples per category, and five MOGA seeds with
population 40/generations 20. Smoke and pilot reduce budgets; default seed 42
preserves existing seed lists. The seed also controls finalist beam sampling.

Strict result serialization exposed undefined NaN observations in the injection
producer. A result-only adapter saves those as JSON null while rejecting infinity;
configuration validation remains strict. Publication treats explicit stored-beam
absence independently of injected capture. Missing knee observations remain null.
BTS summaries record the optimizer termination message. Field-map plot units now
correctly identify the source kick map as mrad.

The runner persists running/completed/failed status and requires nonempty outputs.
Requested PDF builds additionally require paper.pdf and pdf_build.json. The
publication stage retains strict selected-run validation and isolated compilation.
Updated README and production guides document the actual budgets and contracts.

## Validation

- Focused routing, configuration and selected-optics regressions passed (62 tests).
- Complete regression suite: **609 passed in 77.74 seconds**.
- `bash -n scripts/run_full_production_simulation.sh` and `git diff HEAD --check` passed.
- All eight stages ran with real reduced workloads in a fresh directory:
  `/tmp/nkm_refactored_production_smoke_20261007_v2` (seed 42).
- Final scripts also completed all eight stages using independently copied sources
  in `/tmp/nkm_copied_source_checkout_20261007` and seed 7, with outputs in
  `/tmp/nkm_refactored_copied_sources_smoke_20261007`.
- Each successful smoke publication verified its manifest/input hashes and generated
  seven tables and four figures. Injection/MOGA saved the supplied seed 7 in the
  independent-source run. Four-sample tolerance ensembles correctly reported
  insufficient evidence for the default (50,100) prefix-stability comparison.
- A source-symlink experiment was correctly stopped by baseline validation because
  resolved scientific paths escaped the selected checkout. Validation was retained;
  the independent-source check used copies instead.
- Nine protected files matched HEAD by SHA-256; all 79 existing repository result
  files remained unchanged. All validation output stayed under fresh /tmp paths.

## Limits and scientific conventions

These runs verify integration, not production-scale convergence or Pareto quality.
No full production study or real PDF compilation was run. Existing PDF lifecycle
regressions verify isolated builds and failure handling. Public physics quantities
retain m, rad, eV, T and T m, with explicit mm/mrad reporting conversions. Injection
remains its independently configured comparison study, not a new coupling to the
BTS optimization handoff. The latter is explicitly consumed by tolerance studies.
