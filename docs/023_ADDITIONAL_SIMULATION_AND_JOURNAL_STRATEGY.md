# Additional simulations and strategy for a journal research article

Prepared: 2026-10-09. Status: execution plan; additional studies have not been run.

This plan connects additional evidence to a scientific question: **what injection
operating region provides high capture and acceptably small stored-beam disturbance,
and how robust is that region to realistic errors after BTS matching?** A software
framework, successful test suite or generated PDF is supporting infrastructure;
the article must establish a physical result and its limitations.

The provisional venue is JINST, consistent with the existing manuscript template.
Its scope includes accelerator modelling and simulation, and its regular-paper
criteria include originality, scientific quality and relevance. The target and
novelty argument are finalized in [Task 001](jinst-paper/tasks/001_research_question_and_journal_fit.md).
[JINST scope and editorial policy](https://jinst.sissa.it/jinst/help/JINST/JINST_about.jsp).

## 1. Evidence already available and unresolved issues

The selected existing run is `results/production_statistical_01/`. All eight stages
completed, the optimizer was feasible, five MOGA seeds succeeded, and a PDF was
built. These facts establish execution, not independent physical validation.

| Evidence | Current result | Publication consequence |
| :--- | :--- | :--- |
| Tolerance ensemble | 20,000 valid evaluations, zero observed physical failures | Supports the implemented optics/error model; capture distribution is absent |
| Median horizontal mismatch | 0.0020926505; 95% bootstrap interval approximately [0.00203407, 0.00216464] | Report uncertainty, not only a point value |
| Prefix stability | Difference 1.71447e-5 between 10,000 and 20,000; target 1e-5 failed | Additional checks required; do not loosen the target just to pass |
| Injection comparison | Off: 100%; ideal: 100%; linear: 0%; fieldmap: 99.776% | Explain initial conditions, kick calibration and aperture semantics before claiming NKM improves capture |
| Production injection budget | 10,000 particles, 1,000 turns, five seeds | Finite-time survival under this model; not a beam-lifetime measurement |
| Tracking model | Linear one-turn M66 plus explicit thin kicker | Do not label it full nonlinear element-by-element storage-ring tracking |
| Native comparison API | `track_element_resolved_injection` exists | Needs a reproducible comparison driver and common loss/observation conventions |

The manuscript `jinst-paper/paper.tex` mixes historical numbers and models. Examples
requiring correction against selected provenance:

- It places a -5.749 mrad kick at x=-16 mm. Direct evaluation of the protected map
  gives approximately -2.10459 mrad at -16 mm; -5.74907 mrad occurs at -8.5 mm.
  The production injection configuration instead uses an offset of -20 mm.
- It describes a 201x201 grid over +/-25 mm at 0.25 mm spacing. The selected field
  summary reports +/-50 mm, implying 0.5 mm spacing for 201 points.
- It mixes 0.31 m and 0.525 m magnet lengths, 29.8 m BTS claims and historical
  lattice definitions. Resolve these from the authoritative configuration.
- It claims 500 seeds, zero stored-beam perturbation, and rigorous 6D symplectic
  tracking without qualifying the current models, observed residuals or sampling.
- The standalone thick study and the kick-map injection study are different
  models. An integer named `n_slices` in saved tier metadata does not establish
  that the multi-turn kicker was tracked with that many slices.

These are manuscript/model reconciliation issues, not proposed source-data edits.

## 2. Execution order and study availability

| Study | Driver today | Status and prerequisites |
| :--- | :--- | :--- |
| S1: characterize protected maps | `validate_nkm_fieldmap.py` | Runnable; units/domain validated, no experimental validation implied |
| S2: standalone thick-slice convergence | `run_tracking_convergence.py` | Runnable with fixed production slice grid; not multi-turn backend validation |
| S3: reproduce existing injection controls | `run_multiturn_injection.py` | Runnable; budgets and beam offsets fixed by its tier/configuration |
| S4: fixed-optics MC/OAT replication | `run_publication_tolerances.py` | Runnable; hold optimization summary and complete error config fixed |
| S5: one-turn/native tracking comparison | Proposed `run_tracking_backend_validation.py` | NOT implemented; Task 003 must supply the driver |
| S6: calibrated controls and operating region | Proposed `run_injection_operating_region.py` | NOT implemented; Tasks 002-004 must define the shared configuration |
| S7: combined-error capture ensembles | Proposed `run_capture_robustness.py` | NOT implemented; Task 006 must implement actual coupled particle tracking |
| S8: larger, validated MOGA campaign | Publication MOGA driver needs additional flags | Task 007; not a prerequisite if MOGA is removed from the principal claim |

Run S1-S3 to characterize the existing models. Complete Tasks 002-004 before
expensive S4/S7 campaigns if the audit changes the model, selected optics or error
coverage. Existing S4 results cannot automatically be transferred to revised physics.
Do not regenerate or edit protected RADIA notebooks, spreadsheets or original MAT input.

## 3. Common environment and frozen inputs

Run commands from the repository root, using the installed project interpreter.
Every destination below must be new. The following setup is performed once per
campaign; `mkdir` deliberately fails if the campaign already exists.

```bash
set -euo pipefail
export NKM_PYTHON="$(command -v python)"
export SOURCE_RUN="$PWD/results/production_statistical_01"
export CAMPAIGN="$PWD/results/journal_campaign_01"
export WORKERS=8
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
mkdir "$CAMPAIGN"

"$NKM_PYTHON" -B scripts/reproduce_paper.py \
  --manifest "$SOURCE_RUN/publication_manifest.json" --validate-only

"$NKM_PYTHON" -B scripts/inventory_protected_hashes.py \
  --repo-root "$PWD" --output-dir "$CAMPAIGN/inputs"

"$NKM_PYTHON" -B - <<'PYCODE'
import json, os
from pathlib import Path
from nkm_injection.errors import ErrorBudgetConfig
source = Path(os.environ['SOURCE_RUN'])
campaign = Path(os.environ['CAMPAIGN'])
summary = json.loads((source/'tolerances/publication_tolerances_summary.json').read_text())
config = ErrorBudgetConfig.from_dict(summary['error_config'])
with (campaign/'error_budget.json').open('x') as handle:
    handle.write(config.to_json() + '\n')
PYCODE
```

The source optimization summary must have its adjacent complete `config.json`.
Freeze both hashes and the selected beam, energy, Twiss, dispersion, aperture,
RF/radiation and error distributions in the campaign record. Record all software
versions and the commit. Use a distinct campaign for a revised physical model.
Change WORKERS for available physical cores and memory; it is not a convergence parameter.

## 4. Commands supported by the current repository

### S1: map characterization

```bash
"$NKM_PYTHON" -B scripts/validate_nkm_fieldmap.py \
  --repo-root "$PWD" --output-dir "$CAMPAIGN/fieldmap"
```

Keep the JSON and plot. Add field normalization, on-axis gradient and measurement/
independent-calculation checks through Tasks 002-003. Do not describe a software
sign test as magnet measurements. `validate_nkm_kick.py` has no CLI options and
uses its own fixed sampling grid/output path; extend and characterize it before
using it as a controlled journal campaign command.

### S2: standalone thick integration

```bash
"$NKM_PYTHON" -B scripts/run_tracking_convergence.py \
  --repo-root "$PWD" --tier production --seed 42 \
  --output-dir "$CAMPAIGN/thick_convergence_seed42"
```

The supported production grid is 10,20,40,80,160 slices with 1,000 beam particles.
There is currently no `--slices`, `--particles` or `--turns` flag on this driver.
Compare the last refinements, interpolation choices, sign conventions and limiting
cases. Establish an error budget for capture and stored-beam perturbation, not
only the exit angle of one reference particle.

### S3: reproduce the four-model injection comparison with independent seeds

```bash
for SEED in 42 123 777; do
  "$NKM_PYTHON" -B scripts/run_multiturn_injection.py \
    --repo-root "$PWD" --tier production --seed "$SEED" --workers "$WORKERS" \
    --output-dir "$CAMPAIGN/injection_base_seed${SEED}"
done
```

Each invocation runs all four models with 10,000 particles and 1,000 turns. Its
five tier seeds are offset by `SEED-42`; these three resulting seed lists do not
overlap. The seed-42 campaign repeats the archived study and tests reproducibility.
Other seeds supply new beam realizations. Preserve paired realizations across
models and report the actual seed lists, not just the three base seeds.

This script does not consume an optimization summary. It cannot establish a
coupled optimized BTS-to-ring result. It also cannot vary turns/particle counts
beyond tier presets. Tasks 003-004 provide those capabilities before deeper claims.

### S4: larger tolerance ensembles with the same optimized optics

```bash
for SEED in 42 123 777; do
  "$NKM_PYTHON" -B scripts/run_publication_tolerances.py \
    --repo-root "$PWD" \
    --optimization-summary "$SOURCE_RUN/optimization/bts_optimization_summary.json" \
    --error-config "$CAMPAIGN/error_budget.json" \
    --kicker-model fieldmap --kickmap-path "$PWD/kickmap_file.txt" \
    --samples 50000 --oat-samples 5000 \
    --seed "$SEED" --oat-seed "$SEED" --workers "$WORKERS" \
    --bootstrap-count 20000 --bootstrap-seed 1729 --ci-level 0.95 \
    --convergence-sizes 25000 50000 --convergence-tolerance 1e-5 \
    --invalid-sample-policy raise \
    --output-dir "$CAMPAIGN/tolerances_seed${SEED}"
done
```

These are 50,000 joint-error evaluations plus 5,000 OAT evaluations per each of
11 categories (55,000 additional evaluations per seed). OAT is diagnostic;
it omits interactions, and not every ErrorBudgetConfig field is necessarily
represented or applied to each observable. Trace effective coverage in Task 002.

This bootstrap interval applies only to the horizontal mismatch median. The
prefix criterion also tests only that median and does not automatically stop the
production runner. Capture efficiency is absent from this tolerance summary.
Zero failures therefore concerns the implemented optics constraints, not injection
capture under combined errors. Implement S7 rather than relabelling this result.

Hold the bootstrap seed fixed for principal comparisons; assess endpoint stability
with other bootstrap seeds on the same saved observations. Do not rerun expensive
physics solely to change a bootstrap seed. Task 005 supplies that postprocessing.
The bootstrap confidence level is not a control on all injection confidence intervals.

### Full pipeline, only if the scientific configuration changes

```bash
./scripts/run_full_production_simulation.sh \
  --tier production --workers "$WORKERS" --seed 42 \
  --samples 50000 --oat-samples 5000 \
  --bootstrap-count 20000 --bootstrap-seed 1729 --ci-level 0.95 \
  --convergence-sizes 25000 50000 --convergence-tolerance 1e-5 \
  --invalid-sample-policy raise \
  --output-dir "$CAMPAIGN/revised_full_production" --quiet
```

This repeats optimization and MOGA, so it does not replace fixed-optics S4.
PDF compilation is optional (`--compile-pdf`) and does not validate the article's
scientific content or guarantee its manuscript references the selected new figures.

## 5. Studies requiring new drivers: exact proposed CLI contracts

**The three scripts in this section do not exist yet. These commands are design
specifications, not runnable commands.** Implement the linked tasks, validate their
parsers and run small limiting-case checks before using the publication budgets.
The shared `injection_study.json` must define beams, geometry/hand-off, kick
calibration, source paths/hashes, apertures, RF/radiation and observation points.

### S5: backend and turn/particle validation (Task 003)

```bash
# PLANNED: run only after Task 003 implements this CLI and Task 002 freezes the config.
"$NKM_PYTHON" -B scripts/run_tracking_backend_validation.py \
  --study-config "$CAMPAIGN/injection_study.json" \
  --optimization-summary "$SOURCE_RUN/optimization/bts_optimization_summary.json" \
  --backends map element --kicker-models off ideal linear fieldmap \
  --particles 1000 10000 50000 --turns 100 1000 5000 \
  --seeds 42 123 777 --workers "$WORKERS" \
  --output-dir "$CAMPAIGN/backend_validation"
```

Pair initial coordinates, optics and field map across backends. Start with 1,000
particles/100 turns; use the full grid for selected reference and boundary cases,
not blindly every expensive Cartesian combination. Match aperture/septum placement
and observation points or separately quantify differences; native tracking is an
independent numerical comparison, not experimental ground truth.

### S6: calibrated controls and operating region (Task 004)

```bash
# PLANNED: after Tasks 002-004.
"$NKM_PYTHON" -B scripts/run_injection_operating_region.py \
  --study-config "$CAMPAIGN/injection_study.json" \
  --optimization-summary "$SOURCE_RUN/optimization/bts_optimization_summary.json" \
  --tracking-backend element --kicker-models off ideal linear fieldmap \
  --x-offset-mm -22 -20 -18 -16 -14 -12 \
  --xp-offset-mrad -1 -0.5 0 0.5 1 \
  --field-scale 0.9 0.95 1.0 1.05 1.1 \
  --particles 10000 --turns 1000 --seeds 42 123 777 \
  --workers "$WORKERS" --output-dir "$CAMPAIGN/operating_region"
```

Use a staged design: a coarse nominal-scale x/xp map, then field-scale refinements
near the acceptance boundary. Calibrate the ideal and linear controls against the
same reference kick/expansion point. Save inherited physical defaults and the
actual evaluated grid. Require field-domain checks; no silent extrapolation.

### S7: actual capture robustness (Task 006)

```bash
# PLANNED: after validated coupled tracking and error application.
for SEED in 42 123 777; do
  "$NKM_PYTHON" -B scripts/run_capture_robustness.py \
    --study-config "$CAMPAIGN/injection_study.json" \
    --optimization-summary "$SOURCE_RUN/optimization/bts_optimization_summary.json" \
    --error-config "$CAMPAIGN/error_budget.json" \
    --tracking-backend element --kicker-models off ideal linear fieldmap \
    --samples 500 --particles 5000 --turns 1000 --seed "$SEED" \
    --workers "$WORKERS" \
    --output-dir "$CAMPAIGN/capture_errors_seed${SEED}"
done
```

Start with 100 error realizations and 2,000 particles using the same turns and
paired controls. Advance only after checks pass; 500x5,000x1,000 is 2.5 billion
particle-turns per model per seed. Benchmark first. Count uncertainty across error
realizations separately from particle-count uncertainty; do not treat all particle
tracks as independent magnet-error realizations. Save physical losses and invalid
computations separately with first-loss locations and turn distributions.

### S8: MOGA when it supports the scientific question (Task 007)

Current `run_publication_moga.py` exposes only tier, base seed, source and output;
production fixes population=40, generations=20 and five seeds. The alternative
`run_bts_moga.py` has `--pop-size`, `--n-gen`, `--mc-seeds`, `--workers`, `--seed`
and `--output-dir`, but its output schema/finalist evaluation are not interchangeable
with the selected publication handoff. Do not treat its `--mc-seeds` as evidence
of coupled capture tracking without tracing its implementation.

Task 007 should extend the publication driver with explicit population, generation
and finalist settings, then compare 100/100 and 200/200 population/generation
budgets over at least five seeds. Save bounds, constraints, reference point,
termination, feasibility and validated physical finalist metrics. If the article
has no distinct Pareto-design conclusion, place MOGA in supplementary material.

## 6. Acceptance rules and statistical reporting

Predeclare scientific performance thresholds and numerical error tolerances in
a study configuration before looking at the new results. Values below are
planning targets; they require justification from operating requirements.

| Claim | Required evidence and decision |
| :--- | :--- |
| High capture | Paired controls at a genuinely injection-limited condition; confidence intervals across seeds and errors; no reliance on an off-kicker case already inside acceptance |
| Small stored disturbance | Centroid and emittance metrics in m/rad with noise/background controls; on-axis zero field alone is insufficient |
| Backend agreement | Matched definitions and a documented coordinate/capture/perturbation discrepancy budget; refine or restrict claims if disagreement matters |
| Robust optics | Stable p50/p95/p99 and failure bounds across independent seeds; every sampled uncertainty traced to an effective model term |
| Stable median | Report absolute and relative prefix changes, bootstrap interval width and independent-seed variation; a passing prefix is not proof of global convergence |
| Useful Pareto solution | Repeatable front with consistent objective units/normalization and finalist tracking, not optimizer success alone |

Retain 1e-5 as the declared horizontal-median prefix target unless physical
requirements justify a documented revision. The current median CI half-width is
about 6.53e-5: 50,000 samples do not guarantee a 1e-5 uncertainty half-width.
A rough 1/sqrt(N) projection would require approximately 850,000 samples for
that precision; this is a planning estimate, not a demonstrated requirement.
Distinguish uncertainty of the median from median-prefix stability.

Report a binomial upper bound for zero observed failures rather than claiming
zero failure probability. With 20,000 independent valid realizations, the one-sided
95% zero-failure bound `1 - 0.05**(1/N)` is approximately 0.015%. Independence,
fixed error distributions and the actual failure definition are prerequisites.
Use separate intervals for tail quantiles and state the hierarchical resampling
unit for capture studies. More bootstrap replicates cannot repair a missing model.

## 7. Publication assembly and selected evidence

After Task 009 registers the selected runs and any new artifact schema, create
`$CAMPAIGN/publication_manifest.json` explicitly; do not select the newest folder
by timestamp. Preserve the original full-run manifest. Select one MC ensemble
as the principal tolerance artifact and cite seed comparison results separately;
do not merge replicates into a pretend single run or discard unsuccessful outcomes.

```bash
# AFTER Task 009 produces a complete selected manifest with registered artifacts.
"$NKM_PYTHON" -B scripts/reproduce_paper.py \
  --manifest "$CAMPAIGN/publication_manifest.json" --validate-only
"$NKM_PYTHON" -B scripts/reproduce_paper.py \
  --manifest "$CAMPAIGN/publication_manifest.json" \
  --no-pdf --output-dir "$CAMPAIGN/publication_data"
# Build after manuscript references and bibliography have been revised.
"$NKM_PYTHON" -B scripts/reproduce_paper.py \
  --manifest "$CAMPAIGN/publication_manifest.json" \
  --output-dir "$CAMPAIGN/submission_build"
```

A successful PDF build may still contain copied historical figures if manuscript
references were not updated. Require an explicit claim-to-artifact and
figure-to-file hash audit. Revise the article through the ordered
[journal tasks](jinst-paper/tasks/README.md), then check the selected journal's
current author requirements again before submission. This plan does not submit,
publish, push, contact editors or regenerate protected source data.
