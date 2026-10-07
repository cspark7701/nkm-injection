# Full production simulation and analysis

The shell launcher and notebook 04 share the installed `nkm_injection.production` runner. It executes eight stages in order, routes each artifact into one fresh run directory and records the selected inputs for publication. See [runner configuration and workload tiers](012_PRODUCTION_RUNNER.md) for the complete contract.

## Installation and commands

Install the project in the interpreter used by the launcher. See [installation](007_INSTALLATION.md) for Accelerator Toolbox setup.

```bash
python -m pip install -e ".[dev]"

# Read-only preview with explicit workers and a fresh destination.
./scripts/run_full_production_simulation.sh --dry-run --workers 4 \
    --output-dir results/new_production --no-color

# Reduced execution check; choose another fresh destination for every run.
./scripts/run_full_production_simulation.sh --tier smoke --workers 2 \
    --output-dir results/new_smoke --quiet

# Full production workload. PDF compilation is optional.
./scripts/run_full_production_simulation.sh --tier production --workers 4 \
    --output-dir results/new_full_run --compile-pdf
```

`NKM_PYTHON=/path/to/python` selects an interpreter; otherwise the shell uses `python3`. The shell can be invoked from another directory and supplies its source checkout explicitly. The installed CLI is `python -m nkm_injection.cli --repo-root /path/to/checkout`. `--help` lists all options, including seeds, tolerance/OAT counts and statistical policy. Quiet mode preserves per-stage logs and prints stage status.

Notebook [04_full_production_simulation.ipynb](../notebooks/04_full_production_simulation.ipynb) defaults to a read-only preview. Its `ProductionRunConfig` selects the same stage routing and defaults. Notebook 03 remains independently executable.

## Stages and artifacts

| Order | Stage | Main artifacts |
| :--- | :--- | :--- |
| 1 | Protected source inventory | `baseline/protected_files_manifest.json` |
| 2 | Field-map validation | `fieldmap/fieldmap_validation_metrics.json`, comparison plot |
| 3 | Symplectic slicing study | `convergence/tracking_convergence_summary.json` |
| 4 | Injection model comparison and convergence scans | `multiturn/config.json`, `injection_metrics_summary.json`, run-local lattice and plots |
| 5 | Deterministic nine-quadrupole BTS matching | `optimization/config.json`, `bts_optimization_summary.json`, candidate table |
| 6 | Selected-optics tolerance budget | `tolerances/publication_tolerances_summary.json` |
| 7 | Multi-seed NSGA-II | `moga/multi_seed_moga_summary.json`, per-seed artifacts and run-local lattice |
| 8 | Publication | `summary/metrics.json`, `upstream_artifacts.json`, `figures/figure_data.json`, tables and figures |

Only injection ensembles and tolerance Monte Carlo/OAT dispatch use `--workers`. Slicing, BTS matching and MOGA remain sequential. Production slicing uses 1000 beam particles and slice counts 10, 20, 40, 80, 160. Production injection uses 10000 particles, 1000 turns and five seeds. Production tolerances use 100 Monte Carlo samples and 30 OAT samples per category. Production MOGA uses population 40, 20 generations and five seeds. Smoke and pilot reduce workloads without changing canonical physics settings; they are execution checks, not production evidence.

## Output and failure behavior

Each production destination must be new. It contains `production_config.json`, `production_status.json`, `publication_manifest.json`, `logs/<stage>.log` and the eight stage directories above. Outputs inside the source checkout must be under `results/`. Generated lattices and all figures stay inside the new run.

Tolerances consume the feasible BTS summary from the current run. Before publication, the runner validates the protected-source baseline and loads all selected artifacts. Child errors, missing or empty outputs, invalid publication inputs and changed hashes stop later stages and leave diagnostic logs and failed status intact.

PDF builds are opt-in, operate under `summary/build/` and require fresh nonempty `summary/paper.pdf` plus `summary/pdf_build.json`. Manuscript sources remain unchanged. See [publication validation and builds](021_PUBLICATION_LIFECYCLE.md).
