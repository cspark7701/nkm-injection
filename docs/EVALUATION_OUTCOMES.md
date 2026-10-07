# Evaluation outcomes and failure reporting

Robustness and optimization diagnostics distinguish a physics result that violates constraints from an evaluation that produced no usable physics. Kicker models never change in response to exceptions.

## Status and identity

`EvaluationOutcome` records `status`, `identity`, `model_provenance`, `physical_failure_reasons` and optional `exception` (type, message, phase).

| Status | Meaning | Statistical treatment |
| --- | --- | --- |
| `valid` | Usable numerical result satisfying the evaluator's thresholds | Included in physics statistics |
| `infeasible` | Usable numerical result violating physical thresholds | Included in physics statistics and physical failure counts |
| `invalid` | Domain/numerical failure prevents evaluation | Null sample metrics; excluded from physics statistics |

Sample identity includes `sample_id` and nominal candidate quadrupole strengths in m^-2. Optimizer outcomes include candidate strengths; saved candidate records add restart index and seed. Model provenance includes selected kicker name, beam energy in eV, map path, SHA-256 and kick-map metadata when applicable. Nonfinite numerical identity values serialize as null in outcome diagnostics. Missing capture callbacks are not reported as a measured capture efficiency.

The low-level robustness defaults are beta maxima above 60 m and dimensionless mismatch above 0.5; the tolerance CLI explicitly supplies the selected optimization constraint limits. Capture failures use a supplied capture efficiency below 0.8. Every applicable reason is recorded, so failure-mode counts can overlap. `failure_mode` retains the first reason for legacy consumers. Invalid results have `failed=False` because that flag describes physical infeasibility; consumers must inspect `outcome.status` and aggregate invalid counts.

## Explicit kicker selection and units

`evaluate_robustness_statistics(..., kicker_model="fieldmap", kickmap_path=None)` now loads the protected repository `kickmap_file.txt` by default. An explicit path selects another input without overwriting it. Missing/malformed maps are configuration errors and stop the evaluation. There is no fallback after setup or query failure.

Alternate `linear`, `ideal` and `off` models require explicit selection. `RobustMonteCarloObjective` accepts the same model/path options. The tolerance CLI exposes `--kicker-model` and `--kickmap-path`; selected model provenance is saved in its robustness results.

Queries use positions in m. Evaluators' `evaluate_kicks` methods return rad; robustness converts the absolute scaled stored-beam kick to mrad for its existing output interface. Map angle metadata remains authoritative. Quadrupole strengths use m^-2, beta and dispersion use m, alpha and mismatch are dimensionless, and capture efficiencies are fractions.

Previously, every robustness sample selected a hard-coded linear surrogate because the factory was called without a field map. Field-map statistics produced by this path before Task 04 need regeneration to claim field-map provenance. Corrected stored-beam kicks can differ from historical results. The source maps and tracking sign conventions are unchanged.

## Numerical failures and unexpected exceptions

Expected numerical failures are `FloatingPointError` (including explicit nonfinite-output checks) and `numpy.linalg.LinAlgError`. Robustness also records `OutOfDomainError` as invalid. Invalid optics outputs include nonfinite values and nonpositive final beta functions. These conditions can receive optimizer penalties; they are not physical mismatch measurements.

Normalized objectives retain the six-element penalty vector of 1e4 for expected numerical failures and expose `last_outcome`. Successful evaluation resets that diagnostic to valid. Deterministic evaluation saves an invalid outcome with its existing penalty metrics. Candidate tables now add `evaluation_outcome`, including restart identity. Programming/configuration errors, including ordinary ValueError, TypeError, KeyError, RuntimeError and ambiguous pyAT AtError, propagate rather than becoming penalties. Worker errors include sample, selected model and phase with the original exception chained; process dispatch preserves this context. OAT evaluation stops with sample/category context if a ranking cannot be computed.

## Aggregate and saved-result semantics

Robustness results add `evaluation_schema_version=1`, `n_valid_evaluations`, `n_invalid_evaluations`, `invalid_evaluation_fraction`, `sample_results` and `model_provenance`.

- Percentiles and bootstrap intervals use valid and physically infeasible samples only. The fixed bootstrap seed remains 42.
- `failure_probability` is physical failures divided by valid evaluations, or null when no evaluation is valid.
- `feasible_fraction` is physically feasible samples divided by all requested samples; invalid samples cannot increase this fraction.
- When all evaluations are invalid, physics summaries and interval endpoints are null. No synthetic large mismatches enter statistics.
- The legacy convergence diagnostic is omitted if any evaluation is invalid. Broader convergence-method changes remain Task 10.

A robust optimizer candidate with any invalid sample is invalid and penalized. The tolerance CLI saves an incomplete ensemble's diagnostics, skips OAT and exits unsuccessfully. Publication input validation rejects summaries reporting any invalid evaluation, preventing conditional statistics from being published as complete-ensemble results.

The changes are additive for successful legacy result consumers. New consumers must handle null metrics and check invalid counts. Legacy summaries without invalid counts remain readable; their absence does not establish that the historical evaluations used the intended model.

## Loss positions

Element-resolved tracking records unknown `s_position_m` as null, retaining particle, turn and element identity. Missing/not-implemented position providers and expected numerical failures produce explicit `loss_position_exception` metadata. Short/nonfinite position arrays also leave individual positions unknown; `loss_positions_complete` reports coverage. Programming/configuration errors in a position provider propagate. Real zero positions remain zero when supplied by the lattice.

## Verification

Failure-injection tests cover missing maps, out-of-domain queries, singular optics, nonfinite outputs, unexpected exceptions, explicit alternate models, mixed invalid/infeasible ensembles, candidate diagnostics, unknown loss positions and publication/CLI rejection. Serial and process-worker tests verify sample identity and model provenance. Existing physics/optimizer numerical tolerances remain unchanged.
