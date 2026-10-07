# Milestone 98 — Chronological numbering of top-level Markdown documentation

Completed: 2026-10-07

## Outcome and scope

Renamed all 22 Markdown files directly in `docs/` with three-digit prefixes
001–022. The user explicitly selected top-level files only; subfolder filenames,
including the completed-plan numerical sequence and README indexes, remain
unchanged. This task is archived as the next milestone, 98.

Chronology uses the author timestamp of each document's first addition found by
`git log --follow --diff-filter=A`. Files introduced in the same commit are
ordered alphabetically by original filename. Filesystem modification times are
not used. Original filename stems and capitalization are retained.

## Chronological document map

| Prefix | Current document | First-added author timestamp | Commit |
| :--- | :--- | :--- | :--- |
| 001 | [001_paper_results.md](../../001_paper_results.md) | 2026-07-24T10:24:14+09:00 | `707c961` |
| 002 | [002_reproducibility.md](../../002_reproducibility.md) | 2026-07-24T10:24:14+09:00 | `707c961` |
| 003 | [003_simulation_steps.md](../../003_simulation_steps.md) | 2026-07-24T10:38:33+09:00 | `6ebcc24` |
| 004 | [004_paper_result_provenance.md](../../004_paper_result_provenance.md) | 2026-07-25T08:45:58+09:00 | `5951b2d` |
| 005 | [005_release_checklist.md](../../005_release_checklist.md) | 2026-07-25T09:07:37+09:00 | `6079165` |
| 006 | [006_SIMULATION_PROCEDURE_AND_PUBLICATION_WORKFLOW.md](../../006_SIMULATION_PROCEDURE_AND_PUBLICATION_WORKFLOW.md) | 2026-07-25T09:10:16+09:00 | `19d87e7` |
| 007 | [007_INSTALLATION.md](../../007_INSTALLATION.md) | 2026-07-30T12:04:45+09:00 | `bae6479` |
| 008 | [008_FULL_PRODUCTION_SIMULATION.md](../../008_FULL_PRODUCTION_SIMULATION.md) | 2026-07-30T17:47:53+09:00 | `51c7b5f` |
| 009 | [009_STEP_BY_STEP_INSTALLATION_WITH_PATCHED_AT.md](../../009_STEP_BY_STEP_INSTALLATION_WITH_PATCHED_AT.md) | 2026-08-31T16:18:06+09:00 | `928fe29` |
| 010 | [010_repo_review.md](../../010_repo_review.md) | 2026-09-02T17:24:17+09:00 | `2242b01` |
| 011 | [011_PUBLICATION_INPUTS.md](../../011_PUBLICATION_INPUTS.md) | 2026-10-07T14:07:50+09:00 | `4af82e1` |
| 012 | [012_PRODUCTION_RUNNER.md](../../012_PRODUCTION_RUNNER.md) | 2026-10-07T14:27:24+09:00 | `dc71be1` |
| 013 | [013_FIELDMAP_CONTRACTS.md](../../013_FIELDMAP_CONTRACTS.md) | 2026-10-07T14:40:39+09:00 | `7c90a35` |
| 014 | [014_EVALUATION_OUTCOMES.md](../../014_EVALUATION_OUTCOMES.md) | 2026-10-07T15:35:03+09:00 | `b54f7c6` |
| 015 | [015_TRACKING_MAP_LIFECYCLE.md](../../015_TRACKING_MAP_LIFECYCLE.md) | 2026-10-07T16:02:06+09:00 | `b9eafb7` |
| 016 | [016_TOLERANCE_INPUTS.md](../../016_TOLERANCE_INPUTS.md) | 2026-10-07T16:17:46+09:00 | `e78a7b9` |
| 017 | [017_CONFIGURATION_SERIALIZATION.md](../../017_CONFIGURATION_SERIALIZATION.md) | 2026-10-07T16:27:08+09:00 | `d38b11a` |
| 018 | [018_PACKAGE_IMPORTS.md](../../018_PACKAGE_IMPORTS.md) | 2026-10-07T16:36:20+09:00 | `1a419d9` |
| 019 | [019_TRACKING_INPUT_CONTRACTS.md](../../019_TRACKING_INPUT_CONTRACTS.md) | 2026-10-07T16:59:50+09:00 | `e6d9585` |
| 020 | [020_STATISTICAL_CONVERGENCE.md](../../020_STATISTICAL_CONVERGENCE.md) | 2026-10-07T17:12:06+09:00 | `97b22aa` |
| 021 | [021_PUBLICATION_LIFECYCLE.md](../../021_PUBLICATION_LIFECYCLE.md) | 2026-10-07T17:23:46+09:00 | `44891af` |
| 022 | [022_NOTEBOOK_WORKFLOWS.md](../../022_NOTEBOOK_WORKFLOWS.md) | 2026-10-07T17:52:11+09:00 | `e6f412e` |

## Reference updates

Updated README guidance, inter-document links, historical completed-plan
references and maintained notebook Markdown cells. Ignored local planning files
were updated without adding them to version control. Simulation data/results,
protected root inputs, notebook executable cells and website source contents
remain unchanged where no references required updating.

Renamed document contents are preserved except for replacement of references to
other renamed Markdown filenames. Future top-level documents can continue the
sequence at 023. Archived milestone numbers are a separate existing sequence.

## Validation

- Verified all 22 names, sequential three-digit prefixes and Git creation order.
- Compared each renamed document against HEAD with only the intended filename
  reference substitutions allowed.
- Verified 44 tracked links to renamed documents; checked affected links across
  local documentation without finding missing targets.
- Confirmed maintained notebook executable cells remain exactly equal to HEAD.
- Notebook structure regression: **1 passed in 0.97 s**.
- All **nine protected files** match HEAD by SHA-256.
- `git diff --check` passed; git status/diff inspected before and after work.
- No simulation/production execution, protected-input regeneration, commits,
  pushes or remote GitHub interactions occurred. A full physics suite rerun was
  unnecessary for filename/reference-only changes; prior numerical behavior,
  units and tolerances are unaffected.
