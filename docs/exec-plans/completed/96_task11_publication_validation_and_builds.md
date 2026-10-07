# Milestone 96 — Task 11: Read-only publication validation and isolated PDF builds

Completed: 2026-10-07  
Task: [Separate read-only publication validation from initialization and PDF builds](../../05_refactor_tasks/11_isolated_publication_validation_and_build.md)

## Problem and outcome

Manifest validation previously created missing directories and hash baselines,
and empty directories could count as verified runs. Standalone PDF compilation
wrote into manuscript sources, ignored command failures and accepted an existing
PDF as success. Validation now checks complete input provenance and stage
artifacts without writing; initialization and PDF building have separate lifecycles.

## Implementation and compatibility

- Added explicit `initialize_publication_manifest` and CLI `--initialize`.
  Missing directories/baselines are created only by initialization; existing
  baselines must match and are never silently replaced. Initialization does not
  claim scientific validity or stage completion.
- Added read-only CLI `--validate-only`; invalid inputs exit nonzero. Validation
  verifies the five canonical scientific inputs plus additional baseline entries,
  rejects incomplete/malformed hashes and consumes all seven selected JSON
  artifacts before reporting the six runs as verified.
- Default `create_if_missing` is false; true now raises a migration error.
  Pipeline validation failures consistently raise `ValueError` with filenames
  and diagnostics. Direct artifact-loader exceptions remain unchanged. Manifest
  fields and publication schema version 1 are preserved.
- Extracted `publication_build.py`. Both default and explicit destinations copy
  manuscript inputs, generated tables and figures into a fresh run-local build.
  Source paper.pdf and auxiliary files are excluded; legitimate PDF figures remain.
- All four TeX/BibTeX commands must succeed and produce a new nonempty PDF.
  Failures stop subsequent commands, preserve combined-output logs and return
  codes, and never archive a PDF. Build reports include copied-input SHA-256
  hashes; metrics retain `pdf_compiled` and add detailed `pdf_build` evidence.
- The reproduction CLI exits nonzero on requested compilation failure. Python
  callers receive generation metrics and build diagnostics for inspection.
- Reused/occupied output directories and destinations inside manuscript/selected
  source runs are rejected before publication writes. Empty production-stage
  destinations remain supported. Pipeline negative tests use temporary bundles.
- Documented commands, migration and build reports in
  [publication lifecycle](../../021_PUBLICATION_LIFECYCLE.md), with updated README,
  publication-input and production-runner guidance.

## Validation

Environment: installed project in `pyat-dev`, Python 3.11; single-thread BLAS/OMP.

- Focused publication/production suite: **76 passed** before the final four
  output/default-build regressions were added.
- Full suite: **579 passed in 59.31 s** (558 existing plus 21 new regressions).
- Final lifecycle regression suite: **21 passed in 0.94 s**.
- Fresh Python CLI processes validated an isolated complete synthetic bundle
  read-only, then generated seven tables and four figures into a separate fresh
  output directory with `--no-pdf`; upstream bytes remained unchanged.
- Read-only snapshots include file bytes/mtime and directory membership. Covered
  missing/empty baselines, bad digests, missing/malformed stage artifacts,
  explicit initialization, missing scientific sources and baseline mismatch.
- Mocked failures at each TeX/BibTeX pass, missing tools and zero-return commands
  without output cannot accept the stale source PDF. Success requires the fresh
  artifact; default-destination builds and source/output collisions are covered.
- Repository results snapshot: **79 files and directory membership unchanged**
  across the suite. All **nine protected files** match HEAD by SHA-256.
- `git diff --check` passed; task backlog and completed-plan index updated.

## Assumptions and limits

No physics formulas, units or numerical policies change. Public scientific
interfaces retain m, rad, eV, T and T m; legacy conversions remain documented
in publication inputs. Existing mismatch roundoff tolerance is 1e-12. Lifecycle
hashes, file preservation and command-result assertions are exact.

TeX command behavior was tested with mocks; no full production studies or real
manuscript compilation were performed. Copied manuscript references still
control which assets enter the PDF; this change does not rewrite manuscript
content or retarget legacy figure references. No protected input or historical
simulation result was regenerated or migrated. No commits, pushes or remote
GitHub interactions were performed.
