# Explicit inputs for tolerance studies

The tolerance CLI requires one of two input selections:

```bash
python scripts/run_publication_tolerances.py \
  --optimization-summary path/to/bts_optimization_summary.json \
  --samples 100 --seed 42 --oat-samples 30 --workers 4 \
  --output-dir results/new_tolerance_run

python scripts/run_publication_tolerances.py --reference \
  --samples 2 --oat-samples 2 --seed 17 --output-dir results/new_reference_run
```

The production runner supplies its current optimization summary automatically. The CLI never searches older runs, compares timestamps or substitutes default optics after missing/malformed input. `--reference` explicitly selects canonical BTS geometry, entrance/target optics and constraint settings, and labels the result as a reference study. Omission of both modes is a command-line error.

## Optimization contract

The selected summary and its adjacent `config.json` are read without modification. Both absolute paths and full SHA-256 hashes are recorded. Input validation completes before output creation or sampling.

The summary must declare `success=true` and `constraints_satisfied=true`, have no declared violations, and contain exactly nine finite numerical `optimized_strengths_raw` values in q11, q12, q13, q21, q22, q23, q31, q32, q33 order. Booleans, numeric strings, missing/nonfinite strengths and wrong lengths are rejected. Values must lie inside the saved per-quadrupole bounds (or saved global bounds where no individual bound exists).

The adjacent configuration must declare `publication_input_schema_version=1` and contain complete BTS, target and constraint configurations plus increasing finite global quadrupole bounds. Missing settings are rejected instead of being filled from defaults. All consumed numeric fields are finite; beam energy must be positive and agree between lattice and constraints. Target and entrance beta functions must be positive. Saved hardware bounds must carry consistent quadrupole names.

New optimizer outputs also save `quadrupole_names`, canonical `units`, and `optimized_strengths_by_name_m_minus2`. Named strengths must agree exactly with the ordered raw values. Complete schema-1 files from Task 01 without these extra annotations retain schema 1's documented canonical units and fixed order; contradictory annotations are rejected. Files predating the complete schema require verified metadata in a new copy, as described in [publication inputs](PUBLICATION_INPUTS.md).

Reported final beta/mismatch metrics are checked when present. The optimizer's feasibility conventions permit 0.01 m above its beta limit and 0.05 above its total-mismatch limit. These checks verify consistency with declared feasibility; loading does not rerun the optimization or certify every historical hardware/beam constraint.

## Configuration propagation and units

Optimized quadrupoles replace only the nine nominal strengths. Saved magnet/drift geometry, bending/edge angles, energy and apertures are retained during error application. Energy errors scale energy and quadrupole rigidity as before. Monte Carlo and OAT propagation both start from the selected entrance Twiss configuration. OAT reference optics use the same entrance as its perturbed samples.

Canonical units are positions, beta and dispersion in m; angles in rad; energy in eV; quadrupole strengths in m^-2; alpha and dispersion derivatives dimensionless. The existing kick evaluator returns rad and stored-kick diagnostics use mrad. Input configuration field suffixes identify additional units, including field in T and error angles in rad/mrad.

The tolerance CLI supplies the saved peak-beta limit and total mismatch limit with the optimizer's existing 0.01 m/0.05 tolerances. The low-level robustness API keeps its historical per-plane mismatch default of 0.5 and zero threshold tolerances for callers that omit these options. The summary records the actual threshold definition and tolerances under `robustness_statistics.evaluation_thresholds`. The Monte Carlo evaluator still assesses its existing beta/mismatch/capture criteria; recording the full optimizer constraint configuration does not add tracking or aperture/envelope checks to that evaluator.

## Sampling and output reconstruction

`--error-config` optionally selects a complete ErrorBudgetConfig JSON. All standard deviations must be finite and nonnegative; omitted fields are rejected. Without this option the default error budget is recorded in full. The same budget is used for Monte Carlo and OAT, and OAT labels show its actual standard deviations.

`--samples` controls Monte Carlo count, `--oat-samples` controls samples per OAT category, and `--seed` controls Monte Carlo sampling. `--oat-seed` selects a separate seed or defaults to `--seed`. Counts must be positive and seeds nonnegative. Bootstrap defaults remain seed 42 and 1000 replicates. Select `--bootstrap-count`, `--bootstrap-seed`, `--ci-level`, `--convergence-sizes SMALL LARGE`, `--convergence-tolerance` and `--invalid-sample-policy` explicitly as needed. Sampling/statistical metadata saves these settings; see [statistical summaries and prefix stability](STATISTICAL_CONVERGENCE.md).

The summary adds `tolerance_input_schema_version=1`, `nominal_bts_config`, `nominal_strengths_by_name_m_minus2`, `target_config`, `constraint_config`, `error_config`, `initial_twiss`, `target_twiss`, `units`, `sampling`, and input provenance. Reconstruct the nominal lattice with `BTSConfig.from_dict(summary["nominal_bts_config"])`; reconstruct samples with the saved ErrorBudgetConfig, Monte Carlo count and seed. The saved OAT budget/count/seed and entrance optics define its ensemble. Error input files have their own path/hash provenance.

Output directories must be new or empty, allowing the production runner's empty stage directory while preventing overwritten results. Invalid evaluations retain the full handoff metadata in their saved diagnostics and stop the CLI; [evaluation outcomes](EVALUATION_OUTCOMES.md) defines those statuses and publication rejection rules.

## Compatibility and verification

Standalone commands that previously omitted inputs must supply an optimization summary or explicitly choose reference mode. Existing summary fields remain available. Results can change for previously discarded custom geometry/entrance optics and because the CLI now uses the selected optimizer's total-mismatch feasibility settings rather than a fixed per-plane threshold. No historical outputs are migrated or regenerated.

Tests select one of two synthetic runs irrespective of timestamps, reject malformed/infeasible inputs, reconstruct configurations and seeds, preserve source bytes, and verify geometry/entrance/threshold propagation in serial and process-worker evaluation. Zero-error OAT checks use absolute tolerance 1e-12; fresh mismatch comparisons use absolute tolerance 1e-12. Existing numerical tolerances and source-map hashes remain unchanged.
