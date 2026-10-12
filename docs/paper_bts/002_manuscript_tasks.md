# Ordered tasks for the BTS journal paper

Created 2026-10-13. All tasks below are **pending**. Creating this outline and plan does not execute any simulation or complete any scientific task. Execute tasks in numerical order except for the explicitly optional MOGA branch.

## Execution rules

Read AGENTS.md and the [outline](001_manuscript_outline.md) first. Use current `src/nkm_injection/` modules rather than the obsolete `src/nkm/` paths in historical reports. Keep protected inputs, the NKM manuscript and prior reviews unchanged. Archive each executed task under the next established milestone number in `docs/exec-plans/completed/`, update its index, and use the requested formatted git commit message. Never push.

Create a new `results/bts_journal_campaign_*` directory for each campaign and never overwrite archived evidence. Track configurations, source code and publication assets; keep generated raw results ignored and supply them separately. Every claim must identify its observable, selected run, units, input/code hashes, seed, validation tolerance and limitations. Invalid evaluations are diagnostic failures, not successful or physically lost particles.

## B01 — Fix the scientific question, novelty and evidence inventory [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 163).
**Dependencies:** none.

Read relevant BTS matching, beam-envelope control and correction papers, including JKPS accelerator work. Identified closest studies (PLS-II, RAON, MAX IV, Sirius, ESRF-EBS) and physical results added (multi-start topology feasibility separation, 550,000-sample tail failure analysis, and normalized SVD knobs). Audited the selected optimization (`fe107589...`), config (`382e23dd...`), candidate table (`398be628...`), and four tolerance summaries (`62062629...`, `d1f381f7...`, `353c1986...`, `fa3c0b82...`). Verified raw sample counts (550,000 total), zero invalid evaluations, and audited all five failure records (samples 4158, 159294, 160916, 258351, 372486) all caused by $\beta_{y,\text{max}} > 60\text{ m}$.

**Deliverables:**
- [`article_scope.md`](article_scope.md): Principal question, NKM overlap disclosure, candidate claims, and predeclared tolerances.
- [`literature_comparison.md`](literature_comparison.md): Regional (JKPS) and international DLSR transfer line literature survey.
- [`evidence_inventory.md`](evidence_inventory.md): Traceable file paths, hashes, software environment, and failure audit.
- [`claim_evidence.csv`](claim_evidence.csv): Full claim ledger mapping all draft claims to verified artifacts.

**Acceptance:** Distinct BTS question stated; overlap with NKM paper disclosed; every numerical value has traceable evidence; older README/report inconsistencies reconciled; numerical and statistical criteria predeclared.

## B02 — Establish the physical line and observation boundaries [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 164).
**Dependencies:** B01.

Confirm the provenance of the 21.789 m, nine-quadrupole AT model, magnet order, bend/edge conventions and two aperture stations. Reconcile the preliminary ten-quadrupole `bts.madx` sequence. Obtain the source and location of the entrance and target Twiss/dispersion values; propagate any ring-derived target to the same BTS-exit boundary. Do not substitute NKM-centre optics without the intervening transport.

**Deliverables:**
- [`lattice_geometry.md`](lattice_geometry.md): Complete 36-element sequence table, geometry, aperture limits, and MAD-X vs AT reconciliation.
- [`author_inputs.md`](author_inputs.md): Boundary Twiss provenance, verified hardware specs vs working assumptions, non-substitution rule for NKM-center optics.
- [`figures/fig1_bts_layout.png`](figures/fig1_bts_layout.png) & [`figures/fig1_bts_layout.pdf`](figures/fig1_bts_layout.pdf): Multi-panel layout diagram with magnet blocks, baseline vs matched $\beta_{x,y}$, $\beta_{max} \le 60\text{ m}$ limit, and dispersion $D_x(s)$.

**Acceptance:** exact element order and length are validated; both boundaries and coordinate systems are unambiguous. An AT/MAD-X comparison uses equivalent sequences and pass-method assumptions, or its non-equivalence is explicitly documented.

## B03 — Justify beam, magnet and aperture constraints [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 165).
**Dependencies:** B02.

Confirm booster emittance, vertical ratio/coupling, momentum spread, centroid and extraction Twiss. Separate the historical 100/10 nm rad case from the later author-sourced 7.67 nm rad horizontal design beam. Confirm family-specific gradient/power-supply limits, polarity, bore and vacuum clearances. Explain why the 60 m beta limit was chosen; relate it to beam size rather than label it a measured aperture.

Use sigma_x² = beta_x epsilon_x + D_x² sigma_delta² (and the appropriate vertical/coupled covariance), including centroid and a declared beam coverage. Convert K [m^-2] to gradient G = K B rho [T/m] and check pole-tip field against the documented bore. Label assumptions, including distributions and error correlations, individually.

**Deliverables:**
- [`beam_and_constraints.md`](beam_and_constraints.md): Beam parameter matrix, envelope clearance proof, quadrupole pole-tip saturation audit, and error budget table.

**Acceptance:** each constraint has a physical justification or an explicit parametric-study label. No inherited constraint emittance is silently described as the design booster beam.

## B04 — Validate the transport and optics evaluator independently [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 166).
**Dependencies:** B02–B03.

Check transfer matrices, symplecticity where appropriate, Twiss and dispersion propagation, momentum dependence and particle coordinate shape. Compare linear optics with element-by-element particle transport for zero-error and perturbed cases. Model physical apertures at their declared locations and report first-loss positions. Use an equivalent independent matrix implementation or reconciled MAD-X model as a cross-check.

**Deliverables:**
- [`transport_validation.md`](transport_validation.md): Symplecticity error quantifications, covariance and envelope comparisons, off-momentum dispersion tracking checks, and aperture loss accounting.
- Regression tests in `tests/test_bts_lattice.py`: `test_matrix_and_particle_tracking_envelope_consistency` and `test_physical_aperture_station_loss_accounting`.

**Acceptance:** predeclared absolute/relative tolerances are met and documented. Tracking states particle count, distribution/truncation, emittance, energy spread, seed, apertures, loss definition and observation points. Coupling is treated consistently; uncoupled Twiss agreement cannot validate roll-error transport.

## B05 — Reproduce nominal matching and compare fair baselines [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 167).
**Dependencies:** B04.

Reproduce the archived selected strengths and recompute its metrics with its frozen configuration. Run baseline and constrained least-squares/SLSQP designs using the same entrance beam and exit target. Include at least five independent outer seeds and all starts; record failed or infeasible starts, wall time and evaluation counts. Increase the search budget if candidate feasibility or selected observables remain unstable.

Use dimensionless residuals. The historical normalizations are beta/0.05 m, alpha/0.01, D/0.002 m and D'/0.001. Distinguish numerical scaling from a physical tolerance. Report family bounds, active constraints, both dispersion residuals, peak beta, termination and independent feasibility; exact zero printed mismatch is finite precision, not proof of a global optimum.

**Deliverables:**
- [`nominal_matching_reproduction.md`](nominal_matching_reproduction.md): Exact numerical reproduction of nominal strengths, multi-start feasibility matrix over 5 seeds, discovery of low-beta topology, and baseline vs matched optics comparison.

**Acceptance:** results are independently feasible and not selected only by optimizer success. The one-feasible-of-three historical outcome is preserved. Add configuration/iteration/start controls if required; the present CLI only exposes seed, tier and output, so a production tier is not a converged-search guarantee.

## B06 — Derive interpretable correction knobs [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 168).
**Dependencies:** B05.

Form a Jacobian of exit beta, alpha and dispersion with respect to nine quadrupoles. Scale rows by declared optics tolerances and columns by meaningful allowed strength changes; state the dimensionless matrix definition. Check central finite differences over several step sizes, rank and singular values. Separate well-conditioned correction combinations from null-space freedoms and strength saturation.

Test correction predictions with finite perturbations and nonlinear reevaluation. Quantify reachable target changes within the family bounds and the impact on envelope margin.

**Deliverables:**
- [`correction_knobs.md`](correction_knobs.md): Dimensionless Jacobian formulation, condition number reconciliation ($\kappa = 57.78$), 6 orthogonal correction knobs, 3-mode null space analysis, and finite perturbation validation.
- [`figures/fig2_svd_knobs.png`](figures/fig2_svd_knobs.png) & [`figures/fig2_svd_knobs.pdf`](figures/fig2_svd_knobs.pdf): Singular value spectrum and orthogonal knob participation heatmap.

**Acceptance:** numerical rank is stable, condition numbers are dimensionally meaningful, and finite corrections reproduce claimed changes without constraint violation. Do not interpret the historical mixed-unit raw Jacobian condition number as a hardware tolerance.

## B07 — Audit and complete the BTS error model [COMPLETED]

**Status:** Completed 2026-10-13 (Milestone 169).
**Dependencies:** B04, B06.

For every sampled error, perturb one physical quantity and demonstrate its effect on optics, orbit, coupling, envelope or transmission. Distinguish static gradient/alignment/roll/dipole errors from shot-to-shot energy, centroid and input-Twiss jitter. Explain independent versus common power-supply errors. Implement missing effects when necessary for the claims, especially dipole and alignment errors for orbit/dispersion and roll for coupled transport. Longitudinal placement errors must be implemented or excluded explicitly.

Remove NKM field scale, timing, map offsets, ring orbit and stored-kick observations from the central BTS study. The existing tolerance driver can support historical comparisons but is not a complete BTS transport tolerance model. Introduce a BTS-only configurable driver if needed; this is proposed implementation work.

**Deliverables:**
- [`error_model_audit.md`](error_model_audit.md): Machine-readable coverage matrix, single-parameter physical perturbation demonstrations, power-supply error classification, and disclosure of inactive historical channels.

**Acceptance:** no sampled inactive category is interpreted as physical insensitivity. Zero-noise cases reproduce B05, injected test errors produce their expected responses, and invalid outcomes are separately recorded.

## B08 — Compare matching with a design chosen for operating margin

**Dependencies:** B05–B07.

Compare baseline, nominal matched and a newly selected margin/robust design. Choose a physical metric such as worst envelope clearance or a quantile of mismatch under a declared training error set. Keep target, constraints and simulation budget comparable. Search deterministic null-space/multistart solutions or an epsilon-constrained scan first; evaluate all selected designs on a common held-out error ensemble.

**Deliverables:** objective definition, fair comparison table, trade-off figure and selected design with feasibility/termination records.

**Acceptance:** the comparison answers whether nominal matching alone sacrifices a useful margin; quantify any benefit with uncertainty and strength cost. A negative result is reportable. Do not force an improvement or equate merit reduction with capture gain.

**Optional MOGA branch:** only for a substantive unresolved trade-off. Replace the archived dimensionally inconsistent dispersion objective with a stated dimensionless form, e.g. sqrt[(Delta D/s_D)² + (Delta D'/s_D')²]. Use a common hypervolume reference and objective normalization across seeds. Compare at least five seeds at 100×100 population/generation budget and a larger budget, preserving all infeasible results. These are proposed starting budgets, not convergence certificates. Validate finalists with the same BTS physics and held-out errors as the deterministic controls. Extend the driver to expose required budgets; `run_publication_moga.py --tier production` currently uses only 40×20 and ten-turn ideal-kicker finalist tracking and must not supply new physical BTS claims unmodified.

## B09 — Qualify tolerance distributions and engineering requirements

**Dependencies:** B07–B08.

Reuse the 550,000 historical observations only for their frozen model and beam assumptions. Independently verify pooling compatibility and reproduce quantiles, exact failure intervals and per-seed prefix outcomes. For a new evaluator or design, generate independent ensembles rather than pooling incompatible data. Begin with three 50,000-sample seeds and 5,000 OAT samples per active category; increase sample count according to the predeclared precision and tail requirements. Twenty thousand bootstrap replicates at seed 1729 and 95% confidence provide continuity with the historical study; cross-check bootstrap endpoints with seeds 2718/31415 and distribution-free quantile intervals.

Scan relevant error amplitudes, including correlations, to find conditional limits for mismatch, clearance and transmission. Report confidence intervals and zero-failure upper bounds. OAT rank depends on error amplitudes and is not a universal magnet priority. Historical 50k prefixes missed 1e-5; the 400k prefix passed, while rare-event precision remains a separate question.

**Deliverables:** tolerance curves, uncertainty table, seed/prefix report and practical specification recommendations with explicit assumptions.

**Acceptance:** sample precision meets predeclared needs or its limitation is reported; invalid rates, denominators and exact physical criteria are explicit. Five optics-feasibility failures are not labeled five lost bunches or a measured machine failure rate.

## B10 — Validate held-out correction and physical transmission

**Dependencies:** B06, B08–B09.

Evaluate uncorrected and corrected designs on fresh static-error realizations, then add independently drawn shot jitter. Use paired realizations and common input particles for design comparisons, but separate training and validation seeds. Begin with at least five particle seeds and 10,000 particles per seed for selected validation cases; justify larger counts from the transmission uncertainty sought. Record covariance, emittance, orbit, dispersion, aperture clearance and first losses. Test finite correction ranges and repeatability under plausible beam changes.

**Deliverables:** held-out correction/transport report and uncertainty-qualified comparison figures.

**Acceptance:** optical feasibility and measured-in-simulation BTS transmission are reported separately. Correction does not retune every unobservable shot error as though it were a known static machine error. No storage-ring capture is claimed without a separate native ring study; such an extension is outside the core plan.

## B11 — Write the standalone JKPS article and generate assets

**Dependencies:** B01–B10.

Draft the outline sections using the verified claim ledger; rewrite the provisional abstract in past/present tense with completed results only. Generate all figures/tables from selected BTS artifacts. Use up to six main figures and concise captions; detailed matrices, bounds, candidate/seed tables and validation go in supplementary material. Create a one-column review draft and journal formatting only after checking current JKPS guidance. A BTS-specific build must not change `docs/paper/paper.tex` or its PDFs.

**Deliverables:** `paper.tex`, bibliography, generated assets/provenance, `paper.pdf`, reproducible build instructions and declarations based on author inputs.

**Acceptance:** main content follows the current approximately 4,000-word recommendation, abstract is 150–250 words, references are verified, and every conclusion answers the BTS question. No unsupported optimizer novelty, capture claim or duplicated NKM results section remains.

## B12 — Review, freeze evidence and prepare submission

**Dependencies:** B11.

Conduct a manuscript review covering novelty, model provenance, equivalent-code checks, hardware assumptions, units, statistical denominators, reproducibility and overlap with the companion paper. Resolve the resulting tasks. Build the paper from a clean isolated directory, run affected tests, verify protected inputs and prepare a BTS-specific evidence manifest, source archive and referee attachment with raw selected outputs and hash inventory.

**Deliverables:** reviewer report/response, final claim ledger, evidence attachment, cover letter and completed submission checklist.

**Acceptance:** LaTeX builds without unresolved references/citations or layout errors; figures are visually checked; all relevant validation tests pass; another reader can reproduce selected numerical and publication outputs from the attachment. Author identity, funding, conflicts, data availability and submission declarations are confirmed. Submission remains an explicit author action; do not upload, send or push automatically.

## Existing command starting points

These are supported current CLI examples for historical-model reproduction, **not commands executed by this planning task**. Run from the repository root in the project environment. Each destination must be new. New main-claim runs require the validated B02–B07 configuration and may need the proposed BTS-only driver. None of the following substitutes for physical transport validation.

```bash
PYTHONPATH=src python scripts/optimize_bts_publication.py \
  --tier production --seed 42 \
  --output-dir results/bts_journal_campaign_01/optimization_seed42

PYTHONPATH=src python scripts/run_publication_tolerances.py \
  --optimization-summary backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json \
  --error-config results/journal_campaign_01/error_budget.json \
  --samples 50000 --seed 42 --oat-samples 5000 --oat-seed 42 \
  --bootstrap-count 20000 --bootstrap-seed 1729 --ci-level 0.95 \
  --convergence-sizes 25000 50000 --convergence-tolerance 1e-5 \
  --invalid-sample-policy raise --kicker-model fieldmap --workers 2 \
  --output-dir results/bts_journal_campaign_01/legacy_tolerances_seed42
```

The second command intentionally preserves the historical evaluator, including its field-map stored-kick diagnostic; exclude that diagnostic from BTS claims. It requires the ignored archived optimization/config and error budget; record verified hashes before execution. Do not silently substitute a current default if those files are unavailable. Repeat independent seed choices in distinct directories and record unmet convergence targets.

Historical summary post-processing is available in `scripts/analyze_tolerance_replicates.py` (`--summaries`, `--labels`, `--bootstrap-seeds`, `--bootstrap-count`, `--ci-level`, `--output`). Large bootstrap ensembles consume substantial memory; use a suitably sized chunked implementation before scaling. Reuse the existing pooled analysis when only an evidence audit is required. New BTS-only tolerance, correction and publication driver names/options must be documented when implemented rather than presented as existing commands.
