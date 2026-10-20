# Round2 numerical and article reproduction

Use the recorded Python3.11.9,pyAT0.7.2.dev26+g4701d48c.d20260831,NumPy2.4.6,SciPy1.17.1 environment with this package installed. Paths below are relative to the repository or extracted referee root; each output directory must be new. The selected original R1 and new R2 raw records are supplied in the local attachment.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python scripts/audit_bts_evidence.py
python scripts/run_bts_round2.py --stage stations --output-dir results/new_r2/stations
python scripts/run_bts_round2.py --stage accuracy --output-dir results/new_r2/accuracy
python scripts/run_bts_round2.py --stage spatial --output-dir results/new_r2/spatial
python scripts/run_bts_round2.py --stage designs --spatial-file results/new_r2/spatial/spatial.json --output-dir results/new_r2/designs
python scripts/run_bts_round2.py --stage comparison --design-file results/new_r2/designs/designs.json --output-dir results/new_r2/comparison
python scripts/audit_bts_round2_inference.py --output-dir results/new_r2/inference
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/new_r2/article --supplement-build-dir results/new_r2/supplement
python -m pytest tests/test_bts_round2.py tests/test_bts_journal.py tests/test_bts_lattice.py tests/test_bts_evidence_audit.py -q
```

Thread limits above avoid oversubscription; assess numerical agreement at declared tolerances rather than assuming bitwise identity across runtime threading configurations.

The inference command defaults to reconstruction of the selected archived campaign, whose exact arrays are supplied. To audit a fresh campaign, pass `--campaign-dir results/new_r2`. The comparison defaults to the selected frozen designs if no `--design-file` is supplied; use the explicit argument above to route fresh optimization into fresh evaluation. Spatial/design stages preserve original matching inputs and require the supplied R1 records. Different numerical library versions require validating tolerances rather than assuming bitwise identity.

`python scripts/export_bts_round2_assets.py` explicitly regenerates selected numerical tables and figures from installed summary exports and the selected spatial records. It does not overwrite source physics inputs. Exact stage source snapshots distinguish the original stage bytes from later CLI additions. `round2_identity.json` identifies the pre-review article and full original campaign; invalid shared-aperture outputs are retained separately and excluded from evidence claims.

No public deposition or submission is implied by local reproduction. Funding, acknowledgments and competing interests are supplied. The availability wording is final and the referee attachment is prepared (milestone 247); final scientific approval remains pending.

## Accelerator Toolbox figure rendering

The main article optics and lattice sequence use native `at.plot.plot_linear`
and `at.plot.plot_synopt`. Render only these assets into a new directory:

```bash
python scripts/export_bts_at_figures.py --output-dir results/new_at_figures
```

The renderer builds the frozen reference/refined designs, supplies the documented
entrance Twiss parameters to `linopt2`, and subdivides every finite element 64
times. It checks both the native optics and plotted curves against the selected
independent-map profiles (absolute beta tolerance 0.0001 m, coordinate tolerance
1e-10 m). `at_plot_validation.json` records input hashes, pyAT version and measured
errors. The selected run agrees within 3e-11 m in beta. Native periodic-stability
and noninteractive-display warnings are filtered specifically for this open
transfer-line rendering; other warnings remain visible. Statistical and clearance
figures remain Matplotlib plots because their inputs are campaign estimates.
The historical supplement figures and all numerical campaign inputs are retained.

To install a validated rendering, copy its two PDFs and validation JSON into
`docs/paper_bts/figures/`, rebuild in new directories and refresh final asset hashes.
The full `export_bts_round2_assets.py` also calls this renderer when regenerating
all selected assets. Earlier frozen referee attachments preserve their original
figures; a new attachment is required to distribute this revised rendering.

## Nominal phase-space distributions

```bash
python scripts/export_bts_phase_space.py --output-dir results/new_phase_space --particles 20000 --seed 83001
```

The selected run is `results/bts_phase_space_20261013_final/`. It contains
`particles.npz` (initial/final AT coordinates and geometric slopes), summary,
configuration/source hashes, exact generating script and the figure. The
installed summary is `generated/phase_space.json`. Tracking uses both frozen
baseline settings, the complete JournalBeam covariance, zero static errors and
zero shot jitter. All original aperture stations remain active. Slopes use
normalized longitudinal momentum, rather than labelling canonical momenta as
angles. Native `at.plot.plot_sigma` draws the two-RMS sample covariance ellipses;
Matplotlib draws the individual particle clouds with common scales by plane.

Both settings retain all 20,000 particles. The maximum tracked-versus-independent
linear-map RMS relative difference is 8.56e-5 (declared tolerance 0.02). A second
fresh-process run reproduces all arrays and scientific summaries exactly.
This diagnostic illustrates the nominal boundary match; it adds no machines
to the independent robustness campaign and does not change its estimates.
Copy the validated PDF to `figures/phase_space.pdf` and summary to
`generated/phase_space.json`, then rebuild and refresh final asset hashes.
The evidence manifest includes all raw diagnostic inputs/outputs needed in
a fresh portable attachment. Earlier attachments and reviews are retained.
