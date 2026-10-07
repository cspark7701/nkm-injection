# Configured notebook study workflows

Notebooks 01–03 select complete configurations, execute package workflows and plot
returned study data. They require an installed `nkm_injection` package; they do
not modify `sys.path` or the working directory. Repository discovery works from
the checkout or its `notebooks/` directory. From elsewhere, set
`NKM_NOTEBOOK_REPO_ROOT` to the checkout.

| Notebook | Configuration | Workflow | Scientific model |
| :--- | :--- | :--- | :--- |
| 01 main Steps 1–5 | `MainNotebookConfig` | `run_main_notebook_study` | Original exploratory BTS geometry; configured optics, field/tracking comparisons, injection and quadrupole-gradient errors |
| 02 injection validation | `InjectionStudyConfig` | `run_injection_notebook_study` | Original notebook Gaussian beam/model choices and shared one-turn-map tracking |
| 03 optional MOGA | `BTSMOGAConfig` | `run_moga_notebook_study` | Canonical package BTS geometry and existing NSGA-II implementation |
| 04 production | `ProductionRunConfig` | `run_production` | Shared staged production runner; notebook defaults to read-only preview |

Notebook 03 remains optional and independently executable, without outputs from
notebook 01 or 02. Notebook 02 reconstructs the ring from the original protected
MAT file, so a missing root `storage_ring_lattice_nkm.mat` is no longer an implicit
request to generate files in the repository root.

## Explicit configuration and results

Configurations and workflow functions live in `nkm_injection.notebook_workflows`;
notebook 01's geometry is `NotebookBTSConfig` in `notebook_lattice`. Its complete
drift/dipole/quadrupole definitions, element order and aperture limits are saved.
It differs from the canonical production `BTSConfig`; the refactor preserves
that distinction rather than substituting a different geometry.

`BeamStudyConfig` records particle count, beta/alpha, geometric emittances,
bunch length, relative energy spread, all transverse offsets and seed.
`InjectionStudyConfig` supplies both beam distributions, models, turn count,
source filenames and the full ring configuration. In the main workflow the
injected distribution instead comes from the configured BTS entrance beam,
transport and declared handoff scaling/offset; its actual count and origin are
reported separately. The stored distribution comes from the injection settings.

Each workflow returns `NotebookStudyResult(run_dir, summary, data)` with arrays,
raw tracking results, histories and/or the MOGA result needed for plots. No
scientific result is discovered from a global, pickle, cached root array or
another notebook. Main-workflow ring-derived target optics are saved separately
as `effective_matching_config.json`; the caller's configuration is unchanged.

All public coordinates are `(6, N)` in AT order: x [m], px [rad], y [m], py [rad],
delta [fraction], ct [m]. Energy is eV, field T, integrated field T m,
quadrupole K m^-2 and geometric emittance m rad. The thick tracker receives the
explicit conversion `energy_eV * 1e-9` for its legacy GeV argument. Plot labels
convert m/rad to mm/mrad explicitly. Undefined lost-beam metrics become JSON
null; saved particle arrays retain NaN loss markers.

## Fresh output directories

`notebook_run_directory` selects a timestamped directory under
`results/notebooks/<study>/`, without creating it. Set `NKM_NOTEBOOK_RUN_DIR` for
an exact destination. Workflows reject any existing destination, even an empty
one. Outputs inside the checkout must be under `results/`; external temporary
run directories are supported. Notebook 04 uses the same directory selection,
while retaining the production runner's validation and preview semantics.

Runs save `study_config.json`, input SHA-256 provenance, an execution status,
summary JSON, NPZ arrays, histories/loss logs and the modified ring lattice when
needed. Effective ring configuration points to that run-local generated lattice.
Figures are saved into the returned run directory. Failures leave an explicit
failed execution report and propagate the exception. Source hashes are checked
again on successful completion; protected source data are never regenerated.

## Characterized behavior and migration

The preserved notebook 01 matching objective sums squared beta and alpha errors
in both planes and, optionally, horizontal dispersion error. It omits the
horizontal dispersion derivative. Default normalization scales are all 1,
preserving the original raw sum. `NotebookMatchingObjective` reuses the shared
residual/feasibility machinery. `exit_beta_margins` preserves the original
endpoint beta constraints, while physical feasibility additionally reports
shared peak-beta, hardware, envelope and mismatch checks.

The original 36-element order, 108-element aperture layout, magnet parameters,
entrance Twiss and fixed q34 are preserved. Repeated dipole instances are
independent copies; their initial numerical transport is unchanged. Nine matching
strengths are explicit, with bounds [-5, 5] m^-2 accommodating the original
q32=4.13. Optimization is disabled by default, as before; enabling it uses the
shared optimizer and saves bounds, seed, termination, candidates and feasibility.
Numerical optimizer success is reported separately from physical feasibility.

The old implicit root-pickle/JSON fallback is removed. To study historical
strengths, assign verified values to `config.bts.strengths_m_minus2`; do not infer
that a canonical production solution belongs to this different geometry.
The exploratory 0.1 horizontal target scaling and 0.3 handoff scaling remain
explicit defaults, not claims of a physically matched injection interface.

The former handwritten tracking loop was a first-order update despite its RK4
label, used the opposite kick sign and updated delta using ct. It is replaced
by the shared symplectic and genuine RK4 integrators, with validated charge/sign,
coordinate and field-boundary conventions. `By.txt` is consumed through the
established 1-D transverse field interface and treated as uniform along the NKM
for this comparison, not as a reconstructed 3-D field. No silent extrapolation
or zero-field fallback occurs.

Multi-turn injection now consistently uses the shared model already used by
notebook 02: a linear one-turn map, declared apertures and a first-turn-only kick.
It replaces notebook 01's negative-length backtracking and repeated-kick loops.
Thick-field output is a separate comparison, not an extra kick before the ring
model. This is an intentional model change; equivalence to those legacy loops
or full nonlinear native AT multi-turn tracking is not claimed.

Optional native AT acceptance remains available through
`config.compute_acceptance=True`, with explicit grid, amplitudes and turn count.
It is observed at the configured NKM ring entrance, with no extra kick; this
replaces the old after-NKM ring observation/cache. It saves `acceptance.npz`
inside the run. When disabled, there is no synthetic zero acceptance or cached
root-file lookup.

The main notebook's error section is a reproducible study of independent
relative gradient errors for the nine matching quadrupoles. Each sample rebuilds
its configured geometry; invalid samples retain diagnostics and null merit.
It is not the full five-category production error budget or a statistical
convergence claim. Use notebook 04 for the staged production study.

MOGA retains its existing scientific implementation and saved summary schema.
The new report distinguishes the active default hardware checker and peak-beta
inequalities from evaluator diagnostic constraints. MOGA configuration fields
such as `mismatch_max_limit` are not newly activated by this wrapper. Plots now
use the existing `envelope_risk` result key and each returned representative's
actual strengths, fixing the former nonexistent `peak_beta` lookup and ambiguous
nearest-mismatch selection.

## Verification and reduced clean-kernel execution

Install the development and MOGA extras, select the project Python environment,
then run:

```bash
python scripts/smoke_notebook_workflows.py --output-dir /tmp/nkm-notebook-smoke-new
```

The script creates a fresh directory, discards saved outputs and executes every
notebook in a separate kernel using the invoking Python interpreter. Notebook 01
uses 16 injected/stored particles, two turns, four slices and two gradient
samples; notebook 02 uses 16 particles and two turns; notebook 03 uses population
4 and two generations. These are execution checks, not production results or
feasibility claims. Notebook 04 remains a read-only production preview. Executed
notebook copies, figures, study artifacts and the smoke report stay in the new
directory; notebook source files remain unexecuted and output-free.

Characterization was captured from notebook 01 before extraction and saved in
`tests/fixtures/notebook_bts_characterization.json`. Element order and loss
identity assertions are exact. Lattice length uses absolute tolerance 1e-12 m;
transfer matrix, objective and endpoint-beta comparisons use rtol/atol 1e-10;
finite single-pass coordinates use rtol 1e-10 and atol 1e-12. Lost AT columns are
normalized to all-NaN markers while preserving their original indices.
Notebook 02's extracted tracker comparisons use rtol/atol 1e-12. Repeated seeded
study arrays and summaries are compared exactly (excluding wall-clock runtime).
Additional tests cover complete strict configuration round trips, invalid
settings before output creation, immutable caller configs, separate lattice
instances, field coverage failures, reused outputs and returned plot inputs.
