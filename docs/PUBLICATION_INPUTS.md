# Manifest-driven publication inputs

The paper pipeline loads a validated `PublicationInputs` bundle from the exact run directories named in `PublicationManifest`. It does not discover the latest run or substitute nominal settings for missing results. Relative run paths resolve against the supplied repository root; absolute paths are accepted.

## Required upstream artifacts

| Manifest field | Filename | Required consumed data |
| :--- | :--- | :--- |
| `field_validation_run` | `fieldmap_validation_metrics.json` | `1d_fieldmap_validation`: passing `valid`, finite nonnegative `peak_by_T` and `odd_symmetry_residual_T`; `2d_kickmap_validation`: finite nonnegative `grid_interpolation_max_err`, passing `lorentz_kick_test.sign_verified` |
| `tracking_convergence_run` | `tracking_convergence_summary.json` | Positive integer `recommended_production_slices`; nonempty `results` with strictly increasing integer `n_slices`, finite `ref_xp_exit_mrad`, and `inj_survival_fraction` in [0, 1] |
| `bts_optimization_run` | `config.json` | `publication_input_schema_version: 1`, complete `bts_config`, `target_config`, `constraint_config`, and ordered `quad_bounds_global` |
| `bts_optimization_run` | `bts_optimization_summary.json` | Passing `success` and `constraints_satisfied`; nine finite `optimized_strengths_raw` in q11, q12, q13, q21, q22, q23, q31, q32, q33 order; finite nonnegative `final_mismatch_x`, `final_mismatch_y` |
| `injection_run` | `injection_metrics_summary.json` | Nonempty array of distinct known `kicker_model` rows; positive integer `n_particles`, `n_turns`, `n_seeds`; `capture_mean`, `capture_ci_lo`, `capture_ci_hi` in [0, 1] with ordered CI containing the mean; `capture_ci_level` in (0, 1); nonnegative finite `stored_centroid_osc_mm` |
| `tolerance_run` | `publication_tolerances_summary.json` | Matching positive `n_samples` at top level and in `robustness_statistics`; `failure_probability` in [0, 1]; nonnegative finite `mismatch_x.p50_median`, `mismatch_y.p50_median` |
| `moga_run` | `multi_seed_moga_summary.json` | Distinct nonnegative integer `seeds`; corresponding `seed_metrics.seed_<seed>` entries containing boolean `success`, `feasible_fraction` in [0, 1], and nonnegative integer `pareto_count` |

These are adapters for the documented producer formats, not permission to invent missing results. Unused diagnostic keys are retained upstream but are not rendered or validated by this bundle. For example, first-loss statistics can be undefined if nothing was lost. A zero-capture row with an unavailable stored oscillation (`null`, or legacy `NaN`) is represented as unavailable and labelled “no survivors”; it is never converted to a zero perturbation. Other nonfinite consumed metrics are rejected. Failed MOGA seeds remain visible in the tables and count plot.

`bts_config`, `target_config` and `constraint_config` contain the complete `.to_dict()` output of `BTSConfig`, `OpticsTargetConfig` and `BTSConstraintConfig`. Lattice and constraint energies must agree. Bounds follow the optimizer: a per-quadrupole hardware bound overrides the global fallback. Selected strengths must lie inside these saved bounds.

## Units and scientific interpretation

The bundle uses positions, beta functions and dispersion in m; angles in rad; energy in eV; field in T; quadrupole strengths in m^-2; geometric emittance in m rad; energy spread and capture as fractions. Legacy `ref_xp_exit_mrad` and `stored_centroid_osc_mm` convert to rad and m on loading. Field-map grid interpolation error is in the producer's raw kick-angle unit, mrad, and is explicitly labelled that way.

Selected BTS optical functions are recomputed from the saved lattice configuration, optimized strengths and saved entrance Twiss. Tables use saved target optics and bounds. Beam envelopes use saved geometric emittances and energy spread, including both transverse dispersions. The plotted horizontal reference lines show the saved AP1 half-aperture, not an element-by-element acceptance claim. Envelope plots use 3-sigma RMS quadrature.

Mismatch values down to -1e-12 are accepted as floating-point roundoff and normalized to zero; larger negative values fail. The tolerance is recorded in provenance.

Capture, tolerance, field validation, slicing and MOGA metrics are read from their selected summaries without rerunning those studies. Publication provenance identifies which results were used; it does not establish that independently selected stages share the same upstream optimization. Explicit stage handoffs remain Task 02/06 work.

## Artifacts and compatibility

Under `results/paper/<run_id>/`, generation saves:

- Seven Markdown/LaTeX tables for selected BTS optics, strengths, injection, tolerances, MOGA and validation; optics macros retain their existing filename.
- Four figures, retaining `fig1_bts_optics.png` and `fig2_beam_envelopes.png`, plus selected-study metrics and slicing convergence.
- `figures/figure_data.json` containing the numerical inputs used for the plots, with units and source labels.
- `upstream_artifacts.json` containing schema version, units, resolved upstream paths and full SHA-256 hashes of the seven JSON artifacts actually read.
- The existing manifest, scientific-input hashes, environment and metrics files. `metrics.json` also includes upstream artifact provenance.

Direct two-argument `generate_paper_tables` and `generate_paper_figures` calls remain supported for nominal-reference output, labelled explicitly. `run_paper_pipeline` always supplies the selected bundle and cannot fall back to those reference calculations.

The updated `scripts/optimize_bts_publication.py` saves all three configurations and the publication schema version. Older optimization `config.json` files and the repository's legacy example manifest do not contain a complete selected-run bundle. They now fail clearly instead of producing apparently selected results from defaults. Supply a manifest pointing to complete artifacts. For historical runs, add metadata only to a new copy after verifying the exact original settings; do not infer missing targets or overwrite source results. No historical results were migrated or regenerated for this change.

Use a new run ID for each publication generation. The shared production runner constructs its manifest from actual stage outputs and supplies an exact `output_dir` for publication. With that option, PDF compilation builds in the output directory instead of manuscript sources. Standalone default-destination PDF behavior, compilation error reporting and read-only manifest initialization remain Task 11 work. See [production routing](PRODUCTION_RUNNER.md).

## Validation

Regression fixtures use two independent temporary bundles with different strengths, targets and study metrics. They check exact table values, plotted AP1 boundaries, figure data, changed optical functions/envelopes, SI conversion, source byte preservation and SHA-256 provenance. Expected floating-point values use absolute tolerance 1e-12; optics/envelope differences are tested at rtol 1e-8 and atol 1e-10. Negative tests reject missing artifacts, incomplete configs, invalid probabilities, nonfinite values, malformed strength arrays and inconsistent slice grids.
