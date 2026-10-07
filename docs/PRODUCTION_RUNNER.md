# Shared production runner

The shell entry point and notebook 04 use `ProductionRunConfig` and `run_production` from `src/nkm_injection/production.py`. The Python CLI is a thin adapter. Stage order, output destinations, worker routing and publication manifest construction are defined once.

## Preview and execution

```bash
# Read-only preview: no simulations, output directories, logs or bytecode.
NKM_PYTHON=/path/to/project/python ./scripts/run_full_production_simulation.sh \
    --dry-run --workers 4 --output-dir /path/to/new/run --no-color

# Execute with the active project's python3; choose a new run directory.
./scripts/run_full_production_simulation.sh --workers 4 --output-dir results/my_new_run

# PDF compilation is opt-in and builds inside the run directory.
./scripts/run_full_production_simulation.sh --workers 4 --compile-pdf
```

`NKM_PYTHON` selects the shell interpreter; otherwise the wrapper uses `python3` from PATH. Every child stage uses the same interpreter as the driver. The direct equivalent is `python scripts/run_production_simulation.py`. Quiet mode (`-q`) saves child stdout/stderr in stage logs while keeping stage status visible; `-v` also streams child output. `--color` and `--no-color` control status colors.

Notebook 04 defaults to `DRY_RUN = True`. Its configuration cell creates a configuration object without creating a directory. The execution cell calls the same runner. Set `DRY_RUN = False` to run the selected tier; notebook 03 remains independent.

## Configuration and preflight

| Setting | Default | Meaning |
| :--- | :--- | :--- |
| `output_dir` / `-o` | `results/production_run_<timestamp_with_microseconds>` | Exact new run root; an existing path is rejected |
| `workers` / `-w` | 90% of detected CPU cores, minimum 1 | Positive integer, used by injection and tolerance stages |
| `tier` / `--tier` | `production` | Existing injection preset: smoke, pilot or production |
| `seed` / `--seed` | 42 | Slicing beam, deterministic optimizer and tolerance seed |
| `tolerance_samples` / `--samples` | 100 | Positive Monte Carlo sample count |
| `compile_pdf` / `--compile-pdf` | false | Enable the existing publication compilation step in a run-local build directory |

Injection keeps its preset seed list, and MOGA keeps [42, 101, 202, 303, 404]. These are recorded in the stage artifacts. This change routes jobs; it does not change integrators, aperture definitions, optimizer bounds or study algorithms. Physics interfaces retain m, rad, eV, T and T m, with existing explicit mm/mrad conversions at report boundaries. A smoke injection tier reduces only injection workload; it does not turn the whole pipeline into a short smoke study.

Preflight validates job settings, interpreter availability, required scientific/reference input files, a fresh output path and each stage script's syntax using in-memory compilation. It does not run stage imports or simulations, create a hash baseline, make directories, save logs or compile `.pyc` files. CLI contracts are covered by tests against the actual stage argument parsers. Preflight establishes input availability and syntax, not numerical convergence or scientific validity.

## Stage routing

| Order | Output subdirectory | Execution | Handoff |
| :--- | :--- | :--- | :--- |
| 1 | `baseline/` | Sequential | Protected hash inventory, including the original storage-ring MAT input |
| 2 | `fieldmap/` | Sequential | Field validation metrics and plots |
| 3 | `convergence/` | Sequential | Slicing results and supplied seed |
| 4 | `multiturn/` | Injection ensemble workers | Tier, study artifacts and generated lattice under this directory |
| 5 | `optimization/` | Sequential | Optimization summary and complete saved configuration |
| 6 | `tolerances/` | Monte Carlo/OAT workers | Explicit `optimization/bts_optimization_summary.json` from this run |
| 7 | `moga/` | Sequential | Per-seed outputs and run-local lattice for finalist tracking |
| 8 | `summary/` | Sequential | Explicit validated `publication_manifest.json` from this run |

Every stage command receives `--output-dir`. Only stages that actually use worker dispatch receive `--workers`; unsupported stages are reported as sequential. The slicing and deterministic optimizer loops are currently sequential.

The runner checks expected artifacts after each successful child process. Before publication, it verifies input hashes and loads the complete selected publication bundle. Only then does it save the manifest and launch reproduction. Missing files, malformed publication inputs, changed scientific hashes and child failures stop later stages. The run is left intact for diagnosis; it is never reused or automatically overwritten.

The tolerance CLI requires this run's explicit optimization summary (or explicitly selected reference mode for standalone studies). It validates saved strengths/configurations and records summary/config hashes, nominal geometry and entrance/target optics, error settings and Monte Carlo/OAT seeds and counts. See [tolerance inputs](TOLERANCE_INPUTS.md). Injection is still the existing independently configured study, not a newly coupled BTS-to-ring simulation.

## Saved job records

- `production_config.json`: supplied settings, interpreter, output root and resolved worker count.
- `production_status.json`: ordered commands, destinations, actual execution modes and completed/failed/planned stage statuses, including the error and failed stage when applicable.
- `logs/<stage>.log`: command plus child stdout/stderr.
- `publication_manifest.json`: actual selected run directories and run-local protected-input hash manifest.
- Stage outputs and optional `summary/build/` compilation artifacts remain inside the new root.

Direct stage CLIs retain their old default destinations when `--output-dir` is omitted. `run_paper_pipeline(output_dir=...)` also supports an exact publication destination; with PDF compilation enabled, it copies manuscript inputs into `build/` and leaves manuscript sources unchanged. PDF command failures are reported with run-local logs; standalone validation is read-only and initialization is explicit. See [publication lifecycle](PUBLICATION_LIFECYCLE.md). PDF output is deliberately opt-in for the shared runner; the standalone reproduction CLI retains its `--no-pdf` option.

## Verification

Tests use mocked stage executors with valid temporary artifacts to verify routing, workers, current-run handoffs, publication provenance and stop-on-failure behavior without a full production study. They test a source-preserving PDF build, local generated lattice paths, invalid arguments, absent inputs, script syntax failures and byte-for-byte dry-run immutability. CLI contracts and invocation from another working directory are covered. Small hash, field-validation and slicing stages run in temporary output directories; notebook preview is checked in a fresh process and a fresh Jupyter kernel. Existing scientific regression tolerances remain unchanged.
