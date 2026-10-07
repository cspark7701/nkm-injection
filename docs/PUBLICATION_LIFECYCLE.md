# Publication validation, initialization and PDF builds

Publication validation is read-only. `validate_publication_manifest(manifest,
repo_root)` checks the complete scientific-input SHA-256 baseline, the six
selected run directories and the seven required stage artifacts described in
[publication inputs](PUBLICATION_INPUTS.md). Missing baselines, empty runs,
malformed consumed metrics and mismatched hashes fail validation; failed runs
are not reported as verified. Validation records the selected artifact hashes
in its report without writing files.

```bash
python scripts/reproduce_paper.py --manifest config/publication_manifest.json --validate-only
```

This command prints the validation report and exits with status 1 on invalid
inputs. A supplied manifest path must exist. Legacy example runs may lack the
complete metadata required by the selected-run contract.

Initialization is a separate, explicit action:

```bash
python scripts/reproduce_paper.py --manifest config/publication_manifest.json --initialize
```

`initialize_publication_manifest` creates missing run directories and, only
when absent, the scientific-input hash baseline. It requires all five canonical
scientific inputs and checks an existing baseline instead of replacing it.
Initialization does not generate stage results or establish scientific validity;
empty initialized directories still fail validation. An existing baseline may
also include other protected inputs, all of which are verified.

## Generation and migration

`run_paper_pipeline` validates before creating outputs. Its default
`create_if_missing` is now false; passing true raises `ValueError` directing the
caller to explicit initialization. Invalid manifest inputs raise `ValueError`
with the validation errors, including missing-artifact filenames. Direct
`load_publication_inputs` calls retain their existing exception contracts.
Manifest fields and publication input schema version 1 remain unchanged.

Use a fresh run ID or a new/empty `--output-dir`. Generation rejects occupied
outputs and outputs inside the source manuscript or selected upstream runs.
The production runner may still supply its precreated empty stage directory.

```bash
python scripts/reproduce_paper.py --manifest config/publication_manifest.json --no-pdf --output-dir results/paper/new_run
```

Without `--no-pdf`, the CLI requests PDF compilation and exits nonzero if it
fails. The Python pipeline returns generation metrics with `pdf_compiled: false`
and build diagnostics, allowing callers to inspect otherwise generated tables
and figures.

## PDF artifacts and failure evidence

Every PDF build, including the default destination, copies manuscript inputs
from `docs/jinst-paper/` into the publication run's fresh `build/` directory.
Source `paper.pdf` and TeX auxiliary/log files are excluded. Referenced PDF
figures are retained; generated figures and tables are copied into the build,
with generated LaTeX tables/macros also available at its root. The copied
manuscript's existing references determine which assets appear in the PDF;
this refactor does not rewrite manuscript content or retarget legacy figures.

The build runs `pdflatex`, `bibtex`, then two `pdflatex` passes. Each command's
return code and combined output log are preserved. Failure stops subsequent
commands. Success requires all four commands to return zero and a nonempty
new `build/paper.pdf`; only then is it archived as the run's `paper.pdf`.
A stale source PDF never establishes success.

`pdf_build.json` and `metrics.json.pdf_build` record status, errors, command
arguments, return codes, log paths and the successful archived PDF path. The
build report also hashes copied inputs before compilation. Missing executables
and failed commands leave their diagnostics available in the run directory.

## Verification and numerical conventions

Tests use temporary source/result trees and compare bytes, file modification
times and directory entries before/after read-only operations. They cover
explicit baseline creation, missing scientific inputs, incomplete/malformed
artifacts, output collisions, each failed TeX/BibTeX pass, missing tools,
successful commands without a PDF and default-destination isolation. A separate
existing test generates seven tables and four figures in a fresh Python process.
Repository results are checked separately around the full suite.

Hash/file/command assertions are exact. No physics calculations, unit conversions
or numerical tolerances change: public selected-run inputs retain m, rad, eV,
T and T m conventions, and the documented mismatch roundoff tolerance remains
1e-12. Full production studies and protected-input regeneration are unnecessary
for this lifecycle refactor.
