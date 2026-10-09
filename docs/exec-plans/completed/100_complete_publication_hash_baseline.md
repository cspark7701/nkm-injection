# Milestone 100 — Complete publication hash baseline

Completed: 2026-10-09

## Cause and fix

The default publication manifest selected the legacy
`results/baseline/protected_files_manifest.json`, which omitted
`K4GSR_HBIv4-1.mat`. Two fresh inventories generated on 2026-10-09 included
that required input, but inventory generation did not update the selected manifest.
All ten entries of the newer inventory and all nine legacy entries matched
current file bytes.

Added versioned `config/publication_input_hashes.json` with the five canonical
scientific SHA-256 digests, verified against that complete inventory. Updated
the default manifest to select it, preserving all stage selections. This baseline
does not depend on an ignored timestamped inventory directory. It records current
source bytes, not proof of unrecorded historical simulation inputs.

Added `reproduce_paper.py --input-hash-manifest` to explicitly select another
baseline during validation, initialization or generation. Relative paths resolve
under the source checkout; absolute paths also work. The override is saved in
publication provenance without editing the supplied manifest or old baseline.

Incomplete-baseline diagnostics now include the missing input names, selected
baseline path and explicit recovery instructions. Strict hash verification remains:
incomplete baselines and mismatched digests are still rejected. Normal generation
continues to report missing manifest paths through its existing error handler.

## Validation

- Complete regression suite: **614 passed in 88.43 seconds**.
- Final publication lifecycle regressions: **27 passed in 4.46 seconds**, including
  the additional versioned-baseline regression added after full-suite collection.
- Regression cases cover missing MAT diagnostics, read-only validation, relative
  and absolute baseline overrides, successful publication generation, rejected
  mismatched digests, missing manifest handling and default baseline completeness.
- Fresh-process reproduction using real complete smoke artifacts generated seven
  tables and four figures with verified manifest/input hashes in
  `/tmp/nkm_versioned_baseline_paper_20261009`. PDF generation was explicitly skipped.
- Nine protected inputs matched HEAD by SHA-256; all 81 existing repository result
  files, including both legacy and fresh inventories, remained unchanged.
- `git diff --check` passed. No protected inputs were regenerated or modified.

## Remaining legacy artifact requirements

The bundled legacy manifest still selects stage directories without the complete
modern publication artifacts. After the baseline correction, validation correctly
reports missing `results/field_validation/fieldmap_validation_metrics.json`.
A complete run's emitted `publication_manifest.json` must be selected for paper
reproduction; a baseline update cannot fabricate missing results or metadata.

No physics algorithms, units or numerical tolerances changed. Required scientific
inputs remain the field maps, original storage-ring MAT file and two spreadsheets;
public physics interfaces retain m, rad, eV, T and T m conventions.
