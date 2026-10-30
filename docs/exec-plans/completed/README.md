# NKM Project Milestone Summaries & Executive Execution Plans

This directory (`docs/exec-plans/completed/`) contains the complete, ordered record of all refactoring, simulation, and publication milestones achieved in the NKM (Nonlinear Kicker Magnet) Booster-to-Storage Ring (BTS) project.

> **Project Policy**: All newly completed milestones, tasks, or execution plan documentation must be recorded and archived in this directory (`docs/exec-plans/completed/`) following strict numeric ordering.

---

## Completed Milestones Index (In Order)

1. [**Milestone 01 — Baseline Repository Safeguards & Inventory**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/01_baseline_repository_inventory.md)
   - Established protected input scientific data SHA256 manifest, internal physics unit conventions, and unoptimized reference baseline optics/field metrics.

2. [**Milestone 02 — BTS Lattice Construction & Optics Propagation Validation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/02_bts_optics_validation.md)
   - Implemented modular pyAT BTS lattice constructor (`src/nkm/lattice.py`), linear transfer matrix propagation, symplecticity verification ($\max |M^T J M - J| < 10^{-14}$), and uncoupled 2D phase-space mismatch metric formulation ($\mathcal{M}_u$).

3. [**Milestone 03 — RADIA Magnetic Field Map Ingestion & Validation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/03_nkm_fieldmap_ingestion.md)
   - Created 1D/2D field map evaluators (`NKMFieldMap1D`, `NKMKickMap2D`), enforced strict domain bounds with zero silent extrapolation, verified odd symmetry in $x$ ($\text{residual} < 10^{-12}$), and confirmed Lorentz kick sign ($\Delta x' = -5.749\text{ mrad}$ at $x = -16.0\text{ mm}$).

4. [**Milestone 04 — Deterministic Constrained BTS Optics Matching**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/04_bts_deterministic_optimization.md)
   - Developed single-objective SLSQP/trust-constr optics optimization (`src/nkm/optics_optimizer.py`), reducing vertical peak beta $\beta_{y,\max}$ from $242.61\text{ m}$ down to $59.25\text{ m}$ (satisfying $\le 60.0\text{ m}$ constraint) and lowering vertical mismatch to $\mathcal{M}_y = 4.5790$.

5. [**Milestone 05 — NKM Particle Tracking & 6D Injection Dynamics**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/05_nkm_injection_tracking.md)
   - Implemented 6D Gaussian particle distribution generator (`src/nkm/beam.py`), thin-kick and RK4 integration (`src/nkm/tracking.py`), confirming $100.0\%$ injected beam transmission and $< 0.05\text{ }\mu\text{rad}$ stored beam kick perturbation.

6. [**Milestone 06 — Robustness, Tolerances, and Error Budget Analysis**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/06_robustness_tolerances.md)
   - Built 200-seed Monte Carlo error budget evaluator (`src/nkm/errors.py`) covering quad gradient errors ($0.1\%$), misalignments ($100\text{ }\mu\text{m}$), roll tilts ($0.5\text{ mrad}$), and energy errors ($0.1\%$). MOGA knee-point solution achieved $100.0\%$ feasibility.

7. [**Milestone 07 — NSGA-II Multi-Objective Genetic Algorithm (MOGA) Optimization**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/07_moga_pareto_optimization.md)
   - Implemented 3-objective NSGA-II Pareto optimization (`src/nkm/moga.py`), identifying a knee-point design that achieves a $61.5\times$ reduction in total exit mismatch ($\mathcal{M}_x + \mathcal{M}_y = 0.6061$) and reduces peak beta to $25.14\text{ m}$.

8. [**Milestone 08 — Publication-Quality Validation, Paper Reproduction & Release**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/08_publication_release.md)
   - Built automated paper table/figure generator (`src/nkm/paper.py`), one-command reproduction runner (`scripts/reproduce_paper.py`), regression test suite (`tests/test_paper_regression.py`), and authored/compiled Journal of Instrumentation (JINST) paper manuscript.

9. [**Milestone 09 — Unit-Safe Field Map & Kick Map Ingestion**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/09_unit_safe_kickmap.md)
   - Standardized unit conversion guarantees and range-checked spline interpolation across field maps.

10. [**Milestone 10 — Field-Kick Cross Validation & Lorentz Sign Consistency**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/10_field_kick_cross_validation.md)
    - Validated line integrals of 1D longitudinal field maps against 2D transverse kickmaps.

11. [**Milestone 11 — Symplectic Thick Element Tracking Engine**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/11_thick_element_tracking.md)
    - Verified symplectic slicing convergence for particle trajectory propagation through thick NKM fields.

12. [**Milestone 12 — Multi-Turn Storage Ring Injected Beam Capture**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/12_multiturn_storage_ring_capture.md)
    - Modeled 1,000-turn storage ring dynamics, physical vacuum apertures, and top-up injection efficiency.

13. [**Milestone 13 — Deterministic BTS Optics Optimization Pipeline**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/13_deterministic_bts_optimization.md)
    - Refined 8-quad family SLSQP matching with hardware gradient constraints.

14. [**Milestone 14 — Error Model & Robust Optics Optimization**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/14_error_model_and_robust_optimization.md)
    - Implemented 5-category Monte Carlo error distributions and sensitivity evaluations.

15. [**Milestone 15 — MOGA Feasibility & Pareto Reproducibility**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/15_moga_feasibility_reproducibility.md)
    - Validated multi-seed NSGA-II Pareto optimization reproducibility and constraint handling.

16. [**Milestone 16 — Data-Driven Publication Pipeline**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/16_data_driven_paper_pipeline.md)
    - Automated creation of figure graphics, LaTeX tables, and benchmark metric JSON files.

17. [**Milestone 17 — Reproducible Publication Release & CI Integration**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/17_reproducible_publication_release.md)
    - Added CITATION.cff, MIT License, reproducibility docs, and GitHub Actions CI regression workflows.

18. [**Milestone 18 — Task 01: Remove GitHub Action Failures (Local Repo Workflow Validation)**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/18_task01_remove_github_action_failures.md)
    - Audited local GitHub Actions CI workflows, enforcing 100% local operation without remote pushes or remote API checks.

19. [**Milestone 19 — Task 02: Environment Setup & Installation Guide**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/19_task02_environment_set_up.md)
    - Created comprehensive setup instructions (`007_INSTALLATION.md`) and package installation verification workflows.

20. [**Milestone 20 — Task 03: Consolidated Technical Document & GitHub.io Project Webpage**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/20_task03_consolidated_document_and_website.md)
    - Authored consolidated LaTeX report (`docs/nkm_consolidated_report.tex` / `.pdf`) and built modern github.io webpage (`docs/index.html`) featuring author Chong Shik Park and Korea University affiliation.

21. [**Milestone 21 — Task 04: Full Production Simulation Script, Parity Notebook, & Documentation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/21_task04_full_simulation_script.md)
    - Constructed unified full production shell script (`scripts/run_full_production_simulation.sh`), matching Jupyter notebook (`notebooks/04_full_production_simulation.ipynb`), and documentation (`docs/008_FULL_PRODUCTION_SIMULATION.md`), with 90% CPU parallelization option and screen verbosity toggle. Held dry run execution per user signal.

22. [**Milestone 22 — Task 04: Production Simulation Dry-Run & Quiet-Mode Progress Enhancements**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/22_task04_dry_run_and_quiet_mode_enhancements.md)
    - Implemented `-d` / `--dry-run` pre-flight syntax and parameter validation, enhanced `--quiet` mode real-time step notifications (`[RUNNING]` / `[COMPLETED]`), and updated `docs/008_FULL_PRODUCTION_SIMULATION.md`.

23. [**Milestone 23 — Task 03a: Read the Docs (Sphinx / Wyrm) Project Webpage Style**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/23_task03a_readthedocs_website_style.md)
    - Converted `docs/index.html` into a Read the Docs (Sphinx / Wyrm / WarpX) style documentation webpage featuring sidebar search, TOC tree, breadcrumb bar, admonition boxes, Wyrm data tables, theme switcher, and author Chong Shik Park attribution.

24. [**Milestone 24 — Task 03a: SynapticTrack Style Read the Docs Webpage Integration**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/24_task03a_synaptictrack_style.md)
    - Updated `docs/index.html` and `docs/style.css` to adopt the exact Read the Docs style specification from `/home/cspark/Work/simulation_codes-working/synapticTrack/docs/site/style.css`.

25. [**Milestone 25 — Task: Complete Removal of Facility Reference Metadata**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/25_task_remove_pohang_references.md)
    - Audited and sanitized all facility-specific naming references across source code, scripts, documentation, and configuration files.

26. [**Milestone 26 — Task: Full Production Simulation Web Documentation Integration**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/26_task_website_production_pipeline_docs.md)
    - Integrated full production simulation pipeline documentation, 1-to-1 parity mapping, command-line flag table, 8-step execution breakdown, and output folder layout into `docs/index.html`.

27. [**Milestone 27 — Refactor #1: BaseFieldMap Unified Abstract Base Class**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/27_refactor_base_fieldmap.md)
    - Created `BaseFieldMap` abstract base class in `src/nkm/fieldmap.py` encapsulating domain bounds checking, metadata handling, and file SHA-256 cryptographic verification. Refactored `NKMFieldMap1D` and `NKMKickMap2D` to inherit from `BaseFieldMap`.

28. [**Milestone 28 — Refactor #2: Standardized Particle Tracking Containers (`TrackingResult`)**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/28_refactor_tracking_result_dataclass.md)
    - Implemented `@dataclass` `TrackingResult` container in `src/nkm/tracking.py` and updated `track_multiturn_injection()` in `src/nkm/storage_ring_injection.py`, unifying tracking output interfaces while preserving dictionary subscripting parity.

29. [**Milestone 29 — Refactor #3: Optics Optimizer Strategy Pattern (`OpticsOptimizer`)**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/29_refactor_optics_optimizer_strategy.md)
    - Implemented `BaseOpticsObjective` strategy interface, `DeterministicObjective`, `RobustMonteCarloObjective`, and `OpticsOptimizer` engine, decoupling objective evaluation from optimization execution.

30. [**Milestone 30 — Refactor #4: Centralized Publication Plotting Theme (`set_publication_style`)**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/30_refactor_publication_plotting_theme.md)
    - Implemented `set_publication_style()` function and `PUBLICATION_COLORS` color dictionary in `src/nkm/paper.py`, enforcing consistent Matplotlib typography, DPI, line styles, and color palettes across generated graphics.

31. [**Milestone 31 — Refactor #5: Type Aliases & Physics Unit Validation Guards**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/31_refactor_unit_types_and_validation_guards.md)
    - Introduced physical `NewType` unit aliases (`Meters`, `Radians`, `TeslaMeters`, `ElectronVolts`) and explicit validation guard functions (`validate_positive`, `validate_non_zero`, `validate_finite`) across `src/nkm/units.py`.

32. [**Milestone 32 — Task 01: Fix NKM Kick Component and Sign Conventions**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/32_task01_fix_kick_component_sign_conventions.md)
    - Implemented unified, component-aware `integrated_field_to_transverse_kicks()` and `transverse_kicks_to_integrated_field()` functions in `src/nkm/units.py`, updated 2D kick map interpolators and thick integrators, verified electron vs. positron charge sign flipping, and validated thin vs. thick integrator agreement.

33. [**Milestone 33 — Task 02: Validate True Longitudinal RADIA Field Integration**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/33_task02_validate_longitudinal_radia_integration.md)
    - Implemented direct 1D numerical quadrature functions (`integrate_longitudinal_field` in `src/nkm/fieldmap.py`), performed grid resolution convergence scans ($N_z = 21 \dots 1001$), generated 3 publication figures, and validated direct quadrature against 2D kick map, analytical 4-wire model, and thick tracking.

34. [**Milestone 34 — Task 03: Add Two-Plane Thin/Thick NKM Validation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/34_task03_two_plane_thin_thick_kick_validation.md)
    - Validated two-plane transverse particle tracking ($x, y$) across 6 field configurations and 4 tracking formulations, performed a 7-point slice count convergence scan ($N_{\text{slices}} = 5 \dots 320$), generated 3 publication figures, and quantitatively justified $N_{\text{slices}} = 40$ as the production setting.

35. [**Milestone 35 — Task 04: Implement Element-Resolved Aperture and Septum Losses**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/35_task04_element_resolved_aperture_and_septum_losses.md)
    - Implemented element-by-element physical loss detection (`track_element_resolved_injection` in `src/nkm/storage_ring_injection.py`), `SeptumModel`, and `ElementAperture`, recording exact particle index, turn number, element index, $s$-coordinate, cause of loss, and transverse coordinates at the precise moment of loss.

36. [**Milestone 36 — Task 05: Couple Optimized BTS Output to Storage-Ring Injection**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/36_task05_end_to_end_bts_to_storage_ring_coupling.md)
    - Established an end-to-end simulation pipeline (`run_end_to_end_pipeline` in `src/nkm/end_to_end.py`), passing actual BTS exit 6D particle distributions into storage-ring element-resolved tracking and exporting machine-readable handoff artifacts (`bts_exit_distribution.npz`, `config.yaml`, `handoff_validation.json`).

37. [**Milestone 37 — Task 06: Converged Multi-Turn Injection Studies**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/37_task06_converged_multiturn_injection_studies.md)
    - Implemented smoke/pilot/production simulation tier separation (`InjectionStudyTierConfig`), bootstrap capture efficiency confidence intervals, particle-count and turn-count convergence scans, and ensemble multi-seed runner. Fixed critical physics bugs: replaced `ring.track()` with AT linear one-turn map (M66) to avoid false losses from 4GSR internal apertures, corrected ideal kick to Courant-Snyder-optimal value from Twiss at NKM injection point, added `injection_aperture_x_m`. Updated `run_full_production_simulation.sh` to use `set -euo pipefail`.
    - **[37a — Task 06 Detailed Execution Log](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/37a_task06_execution_log.md)**: Step-by-step record of all attempts, debugging investigations, physics analyses, and root causes for all 7 bugs found and fixed during implementation.

38. [**Milestone 38 — Task 07: Repair Deterministic BTS Optimization Constraints and Candidate Selection**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/38_task07_repair_deterministic_optimization_constraints.md)
    - Introduced `ConstraintRecord` dataclass (unit/tolerance/value/violation metadata), element-specific per-quad bounds (`q11`, `q33` tightened to ±2.5 m⁻²), new hard constraints for aperture margin (3σ beam envelope vs. pipe), injection orbit/angle surrogate, septum clearance, and Courant–Snyder mismatch limit. Implemented **feasibility-first candidate selection** in `OpticsOptimizer` (feasible always beats infeasible regardless of merit), distinct seeds per multi-start restart, `CandidateRecord` candidate table in `BTSOptimizationResult`, and exception preservation. 48 new tests across 14 test classes in `tests/test_task07_constrained_optimization.py`; all pre-existing optimization tests continue to pass.

39. [**Milestone 39 — Task 08: Apply Physical Error Model and Robustness Analysis**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/39_task08_apply_physical_error_model_and_robustness.md)
    - Audited error sampling (`src/nkm/errors.py`), eliminated duplicate booster jitter draws, added `nkm_timing_mrad`, and enforced energy rigidity scaling ($K_{\text{eff}} = K / (1 + \Delta p/p)$). Structured `apply_sample_errors()` outputs into explicit `centroid_offset`, `nkm_errors`, and `ring_errors` sub-dictionaries. Enhanced `evaluate_robustness_statistics` (`src/nkm/robust_optimization.py`) with stored beam kick perturbation calculations, capture efficiency evaluation, failure mode breakdown, and Monte Carlo sample size convergence metrics. Added `nominal_vs_robust_comparison()` using common random numbers and comprehensive test suite (`tests/test_task08_error_model.py`).

40. [**Milestone 40 — Task 09: MOGA Pareto Optimization Enhancements & Reproducibility**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/40_task09_moga_pareto_enhancements.md)
    - Integrated non-dominated sorting filtering on Pareto front solutions (`src/nkm/moga.py`), implemented multi-seed finalist re-evaluation via end-to-end tracking, added Pareto front visualization (`plot_moga_summary`), and updated publication script. Verified with 100% test pass rate across all 152 test cases in the test suite.

41. [**Milestone 41 — Task 10: Finalize and Compile JINST Journal Manuscript**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/41_task10_jinst_manuscript_compilation.md)
    - Compiled publication-grade Journal of Instrumentation (JINST) manuscript [`docs/paper/paper.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/paper/paper.pdf) with author Chong Shik Park (Korea University) attribution, incorporating RADIA 2D field map validation, single-objective SLSQP matching, NSGA-II multi-objective optimization, and Monte Carlo 6D robust particle tracking.

42. [**Milestone 42 — Task 10: Build Validated Manifest-Driven Paper Pipeline**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/42_task10_validated_manifest_driven_paper_pipeline.md)
    - Implemented `PublicationManifest` dataclass and `validate_publication_manifest` in `src/nkm/results_schema.py`. Updated `run_paper_pipeline` (`src/nkm/paper.py`) and `scripts/reproduce_paper.py` `--manifest` CLI flag to fail fast if upstream run directories or cryptographic input data hashes mismatch. Verified with 100% test pass rate across all 157 test cases in the test suite.

43. [**Milestone 43 — Task 11: Publication Regression Tests & Repository Cleanup**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/43_task11_publication_regression_repository_cleanup.md)
    - Added physics-level regression tests (`tests/test_paper_regression.py`) covering 2-plane kicks, thin/thick agreement, aperture and septum losses, individual uncertainty responses, and capture metrics. Fixed 6D symplecticity pass logic in `validate_bts_lattice`, sanitized README links, aligned Python versions, and verified 100% test pass rate across 161 test cases.

44. [**Milestone 44 — Task: Fix GitHub Actions Release Workflow**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/44_task_fix_github_actions_workflow.md)
    - Corrected the inline Python file-hash verification snippet in `.github/workflows/release-zenodo.yml` to import and call `compute_input_data_hashes(Path('.'))` from `src.nkm.results_schema`. Verified locally that all workflow steps and paper regression tests pass cleanly.

45. [**Milestone 45 — Task: Update Jupyter Notebook Kernelspec Metadata**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/45_task_update_notebook_kernelspecs.md)
    - Updated kernelspec metadata to `pyat-dev` across non-protected Jupyter notebooks in the repository, maintaining protected source notebook integrity per `AGENTS.md` guidelines.

46. [**Milestone 46 — Task: Update Kernel of All Jupyter Notebooks to pyat-dev**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/46_task_update_all_notebook_kernels.md)
    - Updated kernelspec metadata to `pyat-dev` across all 30 Jupyter notebooks in the repository per explicit user directive and refreshed protected file hash manifest.

47. [**Milestone 47 — Task: Fix Remote GitHub Actions Workflow Failures**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/47_task_fix_remote_github_actions.md)
    - Resolved remote CI failures by enabling `create_if_missing` in `validate_publication_manifest` for clean checkouts and adjusting quick MOGA test constraint limits. Verified 100% test pass rate across 161 test cases.

48. [**Milestone 48 — Task: Fix MOGA Pareto Fallback for Remote GitHub Actions**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/48_task_fix_moga_pareto_fallback.md)
    - Updated `run_bts_moga()` in `src/nkm/moga.py` to populate representative solutions from `least_infeasible_x` when `pareto_x` is empty on short test runs. Verified 100% test pass rate across 161 test cases.

49. [**Milestone 49 — Task: Fix plot_moga_summary Fallback for Empty Pareto Fronts**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/49_task_fix_plot_moga_summary_fallback.md)
    - Updated `plot_moga_summary()` in `src/nkm/moga.py` to fall back to `least_infeasible_f` when `pareto_f` is empty, ensuring figure generation on un-converged short test runs. Verified 100% test pass rate across 161 test cases.

50. [**Milestone 50 — Task: Fix Paper Regression Workflow Protected Hash Manifest Auto-Generation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/50_task_fix_paper_regression_workflow.md)
    - Updated `validate_publication_manifest()` in `src/nkm/results_schema.py` to automatically calculate and save `results/baseline/protected_files_manifest.json` on clean checkouts when missing. Verified 100% test pass rate across 161 test cases.

51. [**Milestone 51 — Task: Standardize Worker Option to -w, --workers Across All Scripts**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/51_task_standardize_worker_option_across_scripts.md)
    - Replaced `--parallel` with `-w, --workers W` ("Number of parallel CPU worker cores") across shell and Python execution scripts (`run_full_production_simulation.sh`, `run_bts_moga.py`, `run_multiturn_injection.py`, `reproduce_paper.py`).

52. [**Milestone 52 — Task: Integrate Full Production Simulation Results & Manuscript Artifacts**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/52_task_integrate_full_production_simulation_results.md)
    - Integrated production run metrics from `results/production_run_20260814_011634/` across 1,000-turn injection tracking, SLSQP/MOGA optics optimization, tolerance budgets, and manifest paper pipeline `reproduce_paper.py`. Verified 100% test pass rate (161/161 tests).

53. [**Milestone 53 — Task: Fix End-to-End Pipeline and MOGA Exception-Masking Bug**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/53_refactor_fix_end_to_end_and_moga_exceptions.md)
    - Fixed storage ring lattice unpacking bug in `run_end_to_end_pipeline` (`src/nkm/end_to_end.py`), ensuring multi-turn tracking executes through the genuine 4GSR storage ring lattice. Fixed MOGA Pareto finalist re-evaluation signature bug in `src/nkm/moga.py` by constructing proper `BoosterExtractionConfig` instances. Vectorized aperture and septum loss checking in `src/nkm/storage_ring_injection.py` for significant performance gains. Verified 100% test pass rate across all modified test suites.

54. [**Milestone 54 — Task: Unify Analytical Kicker Models Across Tracking Modes**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/54_refactor_unify_kicker_models.md)
    - Created single-source-of-truth `get_kicker_evaluator()` in `src/nkm/storage_ring_injection.py` for all 4 kicker models (`off`, `ideal`, `linear`, `fieldmap`). Unified kicker evaluation across `track_multiturn_injection`, `track_element_resolved_injection`, and `simulate_nkm_models`, eliminating legacy unphysical `-5.7491 mrad` values. Vectorized aperture loss checks and verified 100% test pass rate across 163 tests.

55. [**Milestone 55 — Task: Parameterize Matched Twiss in Convergence Studies**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/55_refactor_parameterize_matched_twiss.md)
    - Parameterized injected beam and circulating stored beam Twiss parameters in `StorageRingInjectionConfig` (`src/nkm/storage_ring_injection.py`). Refactored convergence scanning functions in `src/nkm/convergence_study.py` to pull matched optics directly from configuration, eliminating hardcoded placeholder values. Verified 100% test pass rate across 22 convergence and injection tests.

56. [**Milestone 56 — Task: Unify Beam Envelope and Septum Clearance Calculations**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/56_refactor_unify_beam_envelope_and_septum_clearance.md)
    - Implemented unified `compute_beam_envelope()` in `src/nkm/optics.py` supporting `rms_quadrature` and `conservative_linear` methods. Standardized envelope evaluations across `results_schema.py`, `constraints.py`, and `moga.py`. Updated `check_septum_clearance()` to evaluate local Twiss at the injection septum instead of global peak beta. Verified 100% test pass rate across all related test suites.

57. [**Milestone 57 — Task: Centralize Canonical Twiss Parameters and Enforce DRY**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/57_refactor_centralize_canonical_twiss.md)
    - Created frozen `TwissParameters` dataclass and single-source-of-truth constants `DEFAULT_BTS_ENTRANCE_TWISS` and `DEFAULT_BTS_TARGET_TWISS` in `src/nkm/optics.py`. Replaced duplicated literal dictionaries across `objectives.py`, `errors.py`, `robust_optimization.py`, `paper.py`, and `validate_bts_optics.py`. Verified 100% test pass rate.

58. [**Milestone 58 — Task: Clean Unit Naming, Legacy Integrator Wrappers, and Thread Safety**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/58_refactor_clean_unit_naming_and_integrator_wrappers.md)
    - Added canonical SI geometric emittance keys `emittance_x_m_rad` and `emittance_y_m_rad` in `src/nkm/beam.py` and `src/nkm/tracking.py` while preserving backward-compatible aliases. Updated `BoosterExtractionConfig` and `BTSMOGAConfig`. Added `track_nkm_symplectic` alias, clarified `track_nkm_rk4` documentation, and enabled thread-safe lattice copying in `BTSNormalizedObjectives`. Verified 100% test pass rate.

59. [**Milestone 59 — Task: Fix Remote GitHub Actions CI PyAT Element Tracking Energy Bug**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/59_fix_remote_ci_pyat_energy_tracking.md)
    - Identified and fixed `ValueError: Energy needs to be defined` in PyAT element-resolved tracking on Python 3.11 GitHub Actions runners by passing `energy=config.energy_eV` into `elem.track()` in `src/nkm/storage_ring_injection.py`. Verified 100% test pass rate.

60. [**Milestone 60 — Task: Update JINST Paper and Site with Production Simulation Results**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/60_update_jinst_paper_and_site_with_production_results.md)
    - Synchronized `docs/paper/paper.tex`, `docs/paper/paper.pdf`, and `docs/index.html` with full production simulation results (`results/production_run_20260815_153100`). Updated multi-turn metrics ($430\times$ stored beam perturbation reduction to $4.76\,\mu\text{m}$), SLSQP converged optics ($\beta_{x,\max}=30.66\,\text{m}, \beta_{y,\max}=52.54\,\text{m}$, mismatch $< 10^{-6}$), OAT error sensitivity rankings, and verified 100% test pass rate across 174 tests.

61. [**Milestone 61 — Task: Refactor Fix Quadrupole Roll Symplectic Rotation Matrix**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/61_refactor_fix_quadrupole_roll_symplectic_rotation.md)
    - Fixed a physics defect in quadrupole roll error coordinate transformations in `src/nkm/errors.py` by rotating both transverse spatial coordinates $(x, y)$ and momenta angles $(x', y')$ simultaneously in `R1` and `R2`. Added symplectic condition unit tests in `tests/test_errors.py` and verified 100% pass rate.

62. [**Milestone 62 — Task: Refactor Unify 4-Model Injection Tracking and Stored-Beam Closed-Orbit Kick**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/62_refactor_unify_four_model_injection_and_stored_beam_kick.md)
    - Upgraded `simulate_nkm_models` in `src/nkm/injection.py` to evaluate all 4 canonical models (`off`, `ideal`, `linear`, `fieldmap`), exposed stored-beam dipole deflection under the ideal kicker model, and corrected the closed-orbit stored beam kick calculation in `src/nkm/robust_optimization.py` to evaluate physical field map deflections. Verified 100% pass rate across 175 tests.

63. [**Milestone 63 — Task: Refactor Centralize Kicker Model Types and Optimize Multi-Turn Tracking Memory**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/63_refactor_centralize_kicker_model_types_and_in_place_tracking.md)
    - Centralized canonical `KickerModelType`, `CANONICAL_KICKER_MODELS`, and `validate_kicker_model()` in `src/nkm/units.py`. Enforced validation across `storage_ring_injection.py` functions and optimized multi-turn tracking by eliminating per-turn full-array copies with in-place matrix updates. Verified 100% test pass rate.

64. [**Milestone 64 — Task: Refactor Isolate RNG Generators for Thread Safety and Reproducibility**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/64_refactor_isolate_rng_generators_for_thread_safety.md)
    - Replaced global `np.random.seed(...)` mutations in `generate_6d_beam` with isolated `np.random.default_rng(seed)` and direct Cholesky factorizations. Added RNG isolation tests in `tests/test_units.py` and verified 100% pass rate across 177 tests.

65. [**Milestone 65 — Task: Update Documentation, JINST Paper, and Project Site for All Refactors**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/65_update_documentation_paper_and_site_for_all_refactors.md)
    - Updated `README.md` and `docs/index.html` with the 177-test verification suite, updated `docs/paper/paper.tex` with symplectic roll rotation and isolated RNG notes, and recompiled `docs/paper/paper.pdf`. Verified 100% test pass rate.

66. [**Milestone 66 — Task: Bump Framework Version to v0.2.0**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/66_bump_version_to_v0_2_0.md)
    - Incremented repository version from `0.1.0` to `0.2.0` across `pyproject.toml`, `src/nkm/__init__.py`, `CITATION.cff`, and `docs/index.html`. Reinstalled editable package and verified 100% test pass rate.

67. [**Milestone 67 — Task: Isolate Website Files in docs/site/ for GitHub Pages Deployment**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/67_isolate_website_in_docs_site_for_github_pages.md)
    - Created isolated static website bundle in `docs/site/` (`index.html`, `style.css`, `.nojekyll`, reports, and documentation) and created `scripts/sync_site.sh` for syncing with standalone `nkm-injection.github.io` repository. Verified 100% test pass rate.

68. [**Milestone 68 — Task: Update Repository Name and URLs to nkm-injection**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/68_rename_repo_to_nkm_injection.md)
    - Updated repository and package names across `pyproject.toml` (`nkm-injection`), `CITATION.cff`, `README.md`, `docs/007_INSTALLATION.md`, `docs/002_reproducibility.md`, `scripts/setup_environment.sh`, and documentation website links (`https://github.com/nkm-injection/nkm-injection`). Verified 100% test pass rate.

69. [**Milestone 69 — Task: Update Workspace Directory Paths to nkm-injection**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/69_update_workspace_paths_to_nkm_injection.md)
    - Realigned workspace and documentation markdown links, file URIs, and script paths across 46 files in `docs/` and `scripts/` from `Work/projects/nkm/` to `Work/projects/nkm-injection/`. Verified 100% test pass rate.

70. [**Milestone 70 — Task: Rename Source Package Directory to src/nkm_injection**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/70_rename_src_nkm_to_nkm_injection.md)
    - Renamed source package directory from `src/nkm` to `src/nkm_injection` adhering to Python package naming standards. Updated all import statements across `tests/`, `scripts/`, `notebooks/`, and workflows. Reinstalled editable package and verified 100% pass rate across 177 tests.

71. [**Milestone 71 — Task: Create accelerator-toolbox Patch and Automated Installer**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/71_add_accelerator_toolbox_patch_and_installer.md)
    - Created unified patch `patches/accelerator_toolbox_nkm.patch`, standalone extension sources in `patches/pyat_extensions/`, and helper script `scripts/install_accelerator_toolbox.sh` to build `accelerator-toolbox` with OpenMP and NKM extensions (`pyNKMPass`, `NonlinearKicker`). Verified 100% test pass rate.

72. [**Milestone 72 — Task: Comprehensive Repository Review and Documentation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/72_nkm_repository_comprehensive_review.md)
    - Conducted a full review of the `nkm-injection` repository architecture, physics modeling, multi-turn injection tracking, deterministic and MOGA optimization, error models, and publication generation pipelines. Created [`docs/REPOSITORY_REVIEW.md`](file:///home/cspark/Work/projects/nkm-injection/docs/REPOSITORY_REVIEW.md). Verified 100% test pass rate across 177 tests.

73. [**Milestone 73 — Task: Add Blank Lines Between Simulation Steps and Iterations in Verbose Mode**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/73_add_blank_lines_between_simulation_steps_and_iterations.md)
    - Formatted simulation runner script `scripts/run_full_production_simulation.sh` and individual analysis scripts (`run_multiturn_injection.py`, `run_publication_moga.py`, `run_tracking_convergence.py`, `run_publication_tolerances.py`, `optimize_bts_publication.py`, `validate_nkm_fieldmap.py`, `reproduce_paper.py`) with blank lines separating steps, sections, and iterations in verbose output. Verified 100% test pass rate across 177 tests.

74. [**Milestone 74 — Task: Improve Simulation Convergence and Satisfaction Parameters (Steps 4–7)**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/74_improve_simulation_convergence_and_satisfaction_parameters.md)
    - Resolved non-convergence in Step 4 by updating nominal injection position to $x_{\text{inj}} = -20.0\text{ mm}$ (achieving 100% capture and $\Delta = 0.0000$ convergence). Formally resolved optimizer convergence in Step 5 (`Optimization success: True`). Evaluated Step 6 error budget on matched quadrupole strengths (0.0% failure rate). Resolved Step 7 MOGA feasibility and Pareto convergence (`pop_size=40, n_gen=20`, 100% feasible, 31 Pareto solutions). Verified 100% test pass rate across 177 tests.

75. [**Milestone 75 — Task 11: Unify Configuration Serialization and Validation Framework**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/75_refactor_unify_configuration_serialization_and_validation.md)
    - Implemented `SerializableConfigMixin` in `src/nkm_injection/results_schema.py` providing unified `.to_dict()`, `.to_json()`, `.save()`, `.from_dict()`, `.from_json()`, `.load()`, and physical domain validation hooks. Adopted the mixin across `PublicationManifest`, `BTSConfig`, `StorageRingInjectionConfig`, `BTSMOGAConfig`, `ErrorBudgetConfig`, `OpticsTargetConfig`, `BTSOptimizationConfig`, `BTSConstraintConfig`, and `QuadrupoleHardwareBounds`. Added comprehensive round-trip and validation unit tests. Verified 100% pass rate across all 181 tests.

76. [**Milestone 76 — Task 12: Standardize Parallel Execution and Worker Dispatch Utility**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/76_refactor_standardize_parallel_execution_and_worker_dispatch.md)
    - Created dedicated concurrency module `src/nkm_injection/concurrency.py` providing `parallel_map` with OpenMP-safe multiprocessing (`forkserver`/`spawn`), deterministic independent worker seed generation (`generate_worker_seeds`), CPU worker count resolution (`resolve_workers`), and graceful sequential fallback. Integrated parallel worker dispatch across `robust_optimization.py`, `errors.py`, `convergence_study.py`, and `paper.py`. Aligned CLI argument `-w, --workers` across analysis and reproduction scripts (`run_tolerance_study.py`, `run_publication_tolerances.py`, `run_multiturn_injection.py`, `reproduce_paper.py`, `run_bts_moga.py`). Added concurrency unit tests in `tests/test_optimization.py`. Verified 100% pass rate across all 187 tests.

77. [**Milestone 77 — Task 13: Structure Convergence and Dynamic Acceptance Return Types**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/77_refactor_structure_convergence_and_acceptance_return_types.md)
    - Replaced untyped dictionary return structures in `src/nkm_injection/convergence_study.py` with strongly typed dataclasses (`ConvergenceScanResult`, `AcceptanceResult`, `EnsembleStudyResult`) inheriting from `SerializableConfigMixin`. Added runtime profiling, statistical summary methods (`mean_efficiency`, `std_efficiency`), dynamic acceptance window calculators (`acceptance_window_mm`), pandas DataFrame exports (`to_dataframe()`), and backwards-compatible sequence and dictionary indexing. Verified 100% pass rate across all 190 tests in the test suite.

78. [**Milestone 78 — Task 14: Formalize Kicker and Field Map Evaluator Protocols**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/78_refactor_formalize_kicker_and_fieldmap_evaluator_protocols.md)
    - Defined runtime-checkable `FieldMap3DProtocol` and `KickerEvaluatorProtocol` in `src/nkm_injection/units.py`. Created mock field maps (`ZeroFieldMap3D`, `UniformFieldMap3D`, `LinearGradientFieldMap3D`) for zero-I/O testing, updated `NKMKickMap2D` and created typed kicker evaluator classes (`OffKickerEvaluator`, `IdealKickerEvaluator`, `LinearKickerEvaluator`) in `storage_ring_injection.py`. Updated `SymplecticSplitIntegrator` and `LorentzRK4Integrator` type annotations. Added unit tests in `tests/test_nkm_integrators.py` and verified 100% pass rate across all 192 tests in the test suite.

79. [**Milestone 79 — Task 15: Vectorized 3D Field Map Interpolation and PyNKMPass Optimization**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/79_refactor_vectorized_fieldmap_interpolation_and_pynkmpass_optimization.md)
    - Vectorized 3D field map interpolation and inverted tracking loops in `pyNKMPass` to process all macro-particles simultaneously with continuous trilinear interpolation weights. Added `interpolate_3d_field_vectorized` and `NKMFieldMap3D` to `src/nkm_injection/fieldmap.py`, updated `patches/pyat_extensions/pyat/at/integrators/pyNKMPass.py` and regenerated `patches/accelerator_toolbox_nkm.patch`. Added unit tests in `tests/test_fieldmap.py` verifying $< 10^{-14}$ agreement between vectorized and sequential tracking. Verified 100% pass rate across all 195 tests in the test suite.

80. [**Milestone 80 — Task 16: Automated LaTeX Table and Macro Publication Builder**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/80_refactor_automated_latex_table_and_macro_builder.md)
    - Refactored manual LaTeX string formatting into modular `LaTeXTableBuilder` and `LaTeXMacroBuilder` in `src/nkm_injection/paper.py`. Added `escape_latex`, `format_scientific`, and `format_uncertainty` utilities for robust character escaping and uniform number representation. Refactored `generate_paper_tables` to emit synchronized `.tex` and `.md` tables and macros (`paper_macros.tex`). Added unit tests in `tests/test_paper_pipeline.py`. Verified 100% pass rate across all 199 tests in the test suite.

81. [**Milestone 81 — Task: Create cleanup.sh Script to Clean Output Folders**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/81_cleanup_script.md)
    - Created `scripts/cleanup.sh` to safely remove generated simulation outputs, caches, and build artifacts. Implemented strict protection guards for baseline references (`results/baseline/`) and immutable scientific source data (`By.txt`, `kickmap_file.txt`, `K4GSR_HBIv4-1.mat`, etc.), along with dry-run (`-d`) and non-interactive (`-y`) execution modes.

82. [**Milestone 82 — Task: Create Pre-Push GitHub Actions Validation Script**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/82_check_github_actions_script.md)
    - Created `scripts/check_github_actions.sh` to locally validate all GitHub Actions CI workflows (`ci.yml`, `paper-regression.yml`, `release-zenodo.yml`) before pushing to remote. Implemented workflow YAML linting, protected file hash verification, paper reproduction validation, test suite regression checks, and post-run file immutability guards.

83. [**Milestone 83 — Task: Create Antigravity Session Resume Script**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/83_resume_session_script.md)
    - Created `scripts/resume_agy_session.sh` to seamlessly resume an Antigravity (`agy`) CLI session for this repository upon quitting. Supports automatic repo-scoped conversation discovery, pinned conversation resumption (`7dcb6418-14dc-4479-9d1c-ded46901bfcf`), historical session listing (`--list`), and custom conversation IDs.

84. [**Milestone 84 — Task: Production Simulation Run Archival & Key Convergence Findings**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/84_production_simulation_run_20260915.md)
    - Completed full end-to-end production simulation run (`results/production_run_20260915_175049/`), archiving quantitative convergence findings across all 8 simulation stages: thick symplectic convergence at $N_{\text{slices}}=40$, $99.78\%$ 1,000-turn multi-turn capture with $<5.8\,\mu\text{m}$ stored beam perturbation, exact SLSQP optics matching ($\mathcal{M} < 10^{-15}$, $\beta_{x,\max}=30.2\text{ m}, \beta_{y,\max}=44.5\text{ m}$), 100% Monte Carlo tolerance feasibility, multi-seed MOGA Pareto reproducibility, and JINST manuscript compilation.


















85. [**Milestone 85 — Repository Refactoring Opportunity Review**](85_repository_refactor_opportunity_review.md)
    - Reviewed the current package, scripts, notebooks, tests and prior refactors; saved 12 numbered proposed tasks with source evidence, priorities, dependencies and acceptance criteria in [05_refactor_tasks](../../../05_refactor_tasks/README.md). Recorded dependency-related test collection limits.

86. [**Milestone 86 — Task 01: Manifest-Driven Publication Inputs**](86_task01_manifest_driven_publication_inputs.md)
    - Made tables and figures consume validated selected-run artifacts, saved full upstream SHA-256 provenance and figure data, added complete optimizer metadata and isolated regression fixtures, and documented schema/migration requirements.

87. [**Milestone 87 — Task 02: Shared Production Run Orchestration**](87_task02_shared_production_run_orchestration.md)
    - Unified shell/notebook execution with a validated configuration and stage runner; routed outputs, workers, current-run optimization and publication manifests explicitly, added read-only previews and run-local lattice/PDF builds, and verified 249 tests plus a clean Jupyter-kernel preview.

88. [**Milestone 88 — Task 03: Strict Shared Field-Map Validation**](88_task03_strict_fieldmap_validation.md)
    - Enforced finite grid/axis and section agreement checks, closed domains and NumPy broadcasting; shared 3-D interpolation with the standalone pyAT extension, documented explicit boundary policies and verified 306 tests plus clean-process source-map validation.

89. [**Milestone 89 — Task 04: Explicit Evaluation Outcomes**](89_task04_explicit_evaluation_outcomes.md)
    - Removed silent kicker substitutions, saved sample/candidate identity and model provenance, separated invalid evaluations from physical failure statistics, propagated unexpected errors and retained unknown loss positions explicitly; verified 332 tests, serial/process-worker failure diagnostics and clean-process reproducibility.

90. [**Milestone 90 — Task 05: Call-Local One-Turn Tracking Maps**](90_task05_tracking_map_lifecycle.md)
    - Removed the shared identity-based map cache, verified in-place lattice edits and concurrent-call independence, preserved loss accounting, verified 342 tests and measured repeated-call setup cost against the previous implementation.

91. [**Milestone 91 — Task 06: Explicit Optimization Inputs for Tolerance Studies**](91_task06_explicit_optimization_handoff.md)
    - Required validated optimization/reference selection, preserved saved geometry and entrance optics, recorded complete configurations and source/sampling provenance, and verified 372 tests plus a fresh-process tolerance CLI run.

92. [**Milestone 92 — Task 07: Strict Configuration Serialization**](92_task07_strict_configuration_serialization.md)
    - Added strict typed loading with explicit compatibility mode, finite/lossless conversion checks and nested field paths; preserved supported round trips and safe file writes, represented undefined no-loss statistics as null, and verified 408 tests plus clean-process configuration I/O.

93. [**Milestone 93 — Task 08: Canonical Package Imports**](93_task08_canonical_package_imports.md)
    - Unified maintained callers under the installed namespace, preserved root exports through lazy loading, added the production console command, and verified 416 tests plus editable/wheel imports, CLI help and notebook import smoke checks outside the checkout.

94. [**Milestone 94 — Task 09: Shared Tracking Input Contracts**](94_task09_tracking_input_contracts.md)
    - Shared validated integrator parameters, particle/loss boundaries and drift; required positive counts and finite coordinates, preserved original loss identities including native AT losses, documented migration, and verified 520 tests plus a fresh-process drift/aperture smoke check.

95. [**Milestone 95 — Task 10: Statistical Summaries and Convergence Evidence**](95_task10_statistical_convergence.md)
    - Extracted explicit statistical policies and estimand-aware bootstrap helpers, required distinct available prefixes before stability claims, preserved invalid/physical outcome separation and saved settings/diagnostics, and verified 558 tests plus a fresh two-worker tolerance CLI run.

96. [**Milestone 96 — Task 11: Read-only Publication Validation and Isolated PDF Builds**](96_task11_publication_validation_and_builds.md)
    - Separated explicit initialization from strict artifact/hash validation, isolated all PDF builds with logs and return-code checks, rejected stale/occupied outputs, and verified 579 tests plus fresh-process CLI generation with unchanged protected inputs and repository results.

97. [**Milestone 97 — Task 12: Configured Notebook Study Workflows**](97_task12_thin_notebook_workflows.md)
    - Extracted configured geometry/objectives/tracking/studies into reusable workflows, preserved characterized optics and independent MOGA execution, routed artifacts to fresh runs, documented tracking model changes, and verified 600 tests plus four independent clean-kernel notebook executions.

98. [**Milestone 98 — Chronological Markdown Document Names**](98_chronological_markdown_document_names.md)
    - Prefixed the 22 top-level Markdown documents with three-digit chronological numbers, updated repository references while preserving subfolder filenames and notebook code, and verified document links, structure and protected-file hashes.

99. [**Milestone 99 — Production Scripts After Refactoring**](99_refactored_production_scripts.md)
    - Migrated the launcher and eight stages to explicit source/output contracts, tier budgets, seeds and statistical settings; preserved production defaults, verified real complete smoke runs and protected hashes, and documented strict result/artifact handling.

100. [**Milestone 100 — Complete Publication Hash Baseline**](100_complete_publication_hash_baseline.md)
    - Fixed the missing storage-ring MAT baseline entry with a versioned verified baseline, added explicit baseline overrides and precise diagnostics, and verified 614 full-suite tests plus real paper generation without changing protected inputs or existing results.

101. [**Milestone 101 — Isolated Local Workflow Checks**](101_isolated_local_workflow_checks.md)
    - Removed historical result dependencies from local/checked-in publication checks, isolated baseline and lattice outputs, preserved strict validation and diagnostics, and verified execution from a checkout without results.

102. [**Milestone 102 — Additional Simulation and Journal-Article Strategy**](102_additional_simulation_and_journal_article_strategy.md)
    - Documented selected-run limitations, exact supported simulation commands and proposed drivers; prepared twelve ordered research-article revision tasks, verified command options, shell syntax, links and protected hashes, and left future studies explicitly planned.

103. [**Milestone 103 — Campaign S1–S3 and Step 1 Physics Checks**](103_campaign_s1_s3_and_step1_physics_checks.md)
    - Reproduced S1–S3 exactly, found overlapping S3 seed lists, established kick-map units and sign mismatch, and showed with native nonlinear tracking that the linear-map injection model hides a ~12–16 mm dynamic aperture, invalidating the off/fieldmap capture comparison.

104. [**Milestone 104 — Journal Task 001: Research Question and Journal Fit**](104_task001_article_scope.md)
    - Defined the principal capture/transparency question for a small-DA lattice, bounded claims, verified closest literature and recorded JINST requirements.

105. [**Milestone 105 — Journal Task 002: Canonical Physics Model and Claim Audit**](105_task002_canonical_physics_and_claim_audit.md)
    - Audited manuscript claims, froze the injection-study model (geometry, polarity, controls, beams, observables), quantified error-model coverage and added the versioned study configuration with tests.

106. [**Milestone 106 — Journal Task 003: Tracking-Backend Validation (S5)**](106_task003_tracking_validation_driver.md)
    - Implemented and ran the S5 driver: native dynamic aperture, native vs linear-map discrepancy on paired beams, turn/particle convergence, limiting cases and stored-beam response validation.

107. [**Milestone 107 — Journal Task 005: Tolerance Replication and Uncertainty (S4)**](107_task005_tolerance_replication.md)
    - Ran three 50k-sample fixed-optics tolerance ensembles, added saved-observation post-processing, and reported quantile intervals, failure bounds and the unmet 1e-5 prefix target.

108. [**Milestone 108 — Journal Task 004: Calibrated Controls and Operating Region (S6)**](108_task004_operating_region.md)
    - Mapped the native-tracking injection window with paired calibrated controls and coupled BTS handoff, selected the operating point by a predeclared rule, quantified transparency versus alignment and explained the original control results.

109. [**Milestone 109 — Journal Task 006: Combined-Error Capture Robustness (S7)**](109_task006_capture_robustness.md)
    - Ran coupled combined-error capture ensembles with diagnostic scenarios and identified injected-orbit jitter at the septum as the limiting tolerance.

110. [**Milestone 110 — Journal Task 007: Role of Pareto Optimisation**](110_task007_moga_decision.md)
    - Decided, with code and artifact evidence, to omit MOGA from the article's claims and not to run S8.

111. [**Milestone 111 — Journal Task 008: Research Article Rewrite**](111_task008_research_article.md)
    - Rewrote the manuscript around the capture/transparency/robustness question with macro-driven results, explicit limitations and no unsupported claims.

112. [**Milestone 112 — Journal Task 009: Selected Evidence, Figures and Provenance**](112_task009_publication_evidence.md)
    - Added the hashed campaign manifest and figure/macro builder, regenerated all manuscript figures and numbers with provenance, and extended the claim-evidence table.

113. [**Milestone 113 — Journal Task 010: Verified References and Metadata**](113_task010_references_and_metadata.md)
    - Verified every reference against publisher/DOI records, removed unverifiable entries, and prepared availability, AI-declaration and cover-letter drafts.

114. [**Milestone 114 — Journal Task 011: Independent Scientific Review**](114_task011_scientific_review.md)
    - Recomputed headline numbers, quantified the thin-versus-thick NKM approximation (−4 points), corrected wording and ran the full local check suite.

115. [**Milestone 115 — Journal Task 012: Submission Package and Final Gate**](115_task012_submission_package.md)
    - Built a reproducible, gated submission package (archive, PDF, supplement, hashes, environment) and the final checklist; author confirmation pending.

116. [**Milestone 116 — Repair Failing GitHub CI Test Collection**](116_ci_test_collection_fix.md)
    - Fixed bare-`pytest` import failures with a pytest `pythonpath` setting, unified workflow commands and updated actions; verified in clean Python 3.10/3.11 environments.

117. [**Milestone 117 — Follow-up Campaigns: Thick-Magnet Robustness, Three-Seed Diagnostics, 400k Tolerances**](117_followup_thick_diagnostic_tolerance.md)
    - Thick NKM raises combined-error capture to 47.4 % (magnet-model effect, confirmed by cross-runs); diagnostics confirmed on three seeds; 400k-sample tolerance run meets the prefix-stability target; manuscript updated.

118. [**Milestone 118 — Reviewer 2 Referee Report**](118_reviewer2_report.md)
    - Major-revision referee report with 8 major and 14 minor comments and 20 prioritised revision tasks and venue-specific guidance for an undecided target journal (docs/paper/reviews/reviewer2_report.md).

119. [**Milestone 119 — Reviewer 1 Manuscript Report and Revision Register**](119_reviewer1_manuscript_report.md)
    - Assessed the current scientific argument and selected evidence, recommended major revision, prepared twelve ordered tasks with acceptance criteria, and verified local evidence hashes, capture summaries and documentation without changing the manuscript.

120. [**Milestone 120 — Consolidated Revision Plan**](120_consolidated_revision_plan.md)
    - Merged both referee registers into tasks C1–C12 with resolved disagreements and execution order.

121. [**Milestone 121 — C1: Exact 3-D NKM Field and Kicker-Model Validation**](121_c1_kicker_model_validation.md)
    - Biot–Savart field of the RADIA filament geometry reproduces the kick map to 1e-10; vertical-sign bug fixed; 3-D model (vertical defocusing, self-deflection) selected as principal model.

122. [**Milestone 122 — C2: Finite-Length Mechanism**](122_c2_finite_length_mechanism.md)
    - Self-deflection inside the magnet (sagitta 0.32 mm), not path averaging or field details, explains the thin/thick reversal; magnet-length design trade-off quantified.

123. [**Milestone 123 — C9: Contribution and Verified Comparison**](123_c9_novelty_and_comparison.md)
    - Stated four demonstrated contributions, a caveated NLK/MIK comparison table and four newly verified references; lattice identity flagged for author confirmation.

124. [**Milestone 124 — C8: Pulsed-Magnet and Timing Requirements**](124_c8_pulse_and_timing.md)
    - Claims restricted to an ideal single-pass field; residual-field, on-axis residual and timing requirements derived from the measured window and exact-field transparency.

125. [**Milestone 125 — C3: Operating Window with the 3-D NKM**](125_c3_operating_window_3d.md)
    - Declared-rule selection validated on fresh seeds (93.0 %); asymmetric 0.74 mrad angular window at 80 % capture; acceptance map; offset and emittance scans.

126. [**Milestone 126 — C4: Survival, Loss Accounting and Bounded Sensitivities**](126_c4_survival_and_sensitivity.md)
    - 4000-turn survival 89.5 % (500-turn capture 3.5 points optimistic); vertical-aperture loss traced to ring coupling, not the NKM; uncorrected ring errors bound the sensitivity.

127. [**Milestone 127 — C5: Combined-Error Robustness with the 3-D NKM**](127_c5_combined_errors_3d.md)
    - 150 paired realizations: 3-D NKM 40.5 % vs dipole 61.4 % (−20.9 points); the gap grows from 2 points without errors; limited by the transfer-line exit centroid (booster jitter).

128. [**Milestone 128 — C6: Booster-Jitter Tolerance Curves With and Without Static Orbit Correction**](128_c6_tolerance_curves.md)
    - Jitter below a quarter of the assumed value costs nothing; without correction, removing jitter reaches only 58.6 %; with ideal static correction 69.7 % (median 80 %); no single static driver; corrected combined errors 44.4 % vs dipole 65.6 %.

129. [**Milestone 129 — C7: Stored-Beam Transparency from the Exact Field**](129_c7_transparency_3d.md)
    - Aligned centroid kick exactly zero by symmetry; 0.2 mm offset gives 0.10 σ and ≈1 % emittance; 1000-turn 6-D tracking reproduces the single-pass estimates (2.23 vs 2.22 at 0.5 mm).

130. [**Milestone 130 — C10: Revised Manuscript Build (KLS, Exact 3-D NKM)**](130_c10_manuscript_build.md)
    - Revision manifest (46 artifacts) → eight figures and macros → gated 13-page build; robustness text checked against final values; claim table rows C0–C16, checklist and cover letter rewritten (venue-neutral).

131. [**Milestone 131 — C11: Frozen Evidence Bundle for the Revised Manuscript**](131_c11_evidence_bundle.md)
    - 46 manifest artifacts + scientific inputs + code snapshot; `--builder revision --verify` rebuild reproduces the manuscript macros byte for byte.

132. [**Milestone 132 — C12: Point-by-Point Response and Final Gate**](132_c12_author_response.md)
    - Response to both reviewers completed (both robustness ensembles, tracked transparency); 663 tests pass; final evidence bundle at a clean commit rebuilds the macros byte for byte.

133. [**Milestone 133 — Introduction Expanded with Verified References**](133_introduction_references.md)
    - Nine verified references (DLSR overview, ESRF-EBS, top-up, swap-out, longitudinal injection, pulsed quadrupole, MAX IV dipole kicker, s-dependent integrator, KLS lattice); gated build 14 pages.

134. [**Milestone 134 — Journal Fit for the Revised NKM Manuscript**](134_journal_fit_recommendation.md)
    - Read the revised physics-focused paper, checked official journal scopes, and recommended PRAB followed by JINST and NIM A, with venue-specific framing and unchanged manuscript/scientific inputs.

135. [**Milestone 135 — General Article Format and Manuscript Directory**](135_general_article_and_paper_directory.md)
    - Renamed the manuscript directory to docs/paper, converted the LaTeX source to a standard article, migrated build/package paths and links, and verified a clean 12-page PDF, 90 focused tests and unchanged scientific content/protected inputs.

136. [**Milestone 136 — Reviewer 2, Second-Round Report on the Revised Manuscript**](136_reviewer2_round2_report.md)
    - Major revision: missing chamber in the headline, uncorrected ring errors, micrometre-level wire tolerance for transparency (checked), pulse-length inconsistency, beam-based tuning, lattice version, generality; tasks R2b-1 to R2b-15.

137. [**Milestone 137 — Reviewer 1 Second-Round Manuscript Report**](137_reviewer1_round2_manuscript_report.md)
    - Assessed the revised 3-D NKM manuscript, recommended focused major revision, wrote ten ordered tasks, verified 46 evidence hashes and paired jitter uncertainty, and preserved all previous reviews and scientific/manuscript inputs.

138. [**Milestone 138 — Consolidated Round-2 Revision Plan**](138_consolidated_revision_plan_round2.md)
    - Reconciled Reviewer 1 (R1B-01–10) and Reviewer 2 (R2b-1–15) round-2 tasks into D1–D15 with author inputs A1–A6; realism tasks reduced to feasible scenarios, ensembles rerun once after budget/ring/chamber are fixed; integrator validation gates new simulations.

139. [**Milestone 139 — Repository Orientation**](139_repository_orientation.md)
    - Read repository instructions and README, inspected package and workflow layout, and identified current revision priorities and documentation discrepancies; scientific inputs and code unchanged.

140. [**Milestone 140 — Commit Message Format**](140_commit_message_format.md)
    - Reviewed recent local commits and adopted their imperative subject, explanatory body and status-prefixed Files section for future commit messages.

141. [**Milestone 141 — Identify the lattice and preliminary NKM design (D1)**](141_d1_lattice_and_design_identity.md)
    - Names the supplied IPAC 2025 design lattice, distinguishes the study NKM and septum from the KLS baseline, and narrows the title to the design version.

142. [**Milestone 142 — Repair survival reporting and paired jitter inference (D2)**](142_d2_existing_evidence_statistics.md)
    - Fixes the survival duration, reports conditional Wilson uncertainty, analyzes all paired jitter levels and applies Holm correction to sampled-error partial correlations.

143. [**Milestone 143 — Validate the trajectory integrator and static steering (D3)**](143_d3_trajectory_and_steering.md)
    - Checks the sliced map against an independent adaptive reference in both planes and documents precisely which static reference coordinates ideal steering removes.

144. [**Milestone 144 — Separate injection shot errors and source the beam budget (D4)**](144_d4_beam_and_error_budget.md)
    - Adds independent septum-strength, RF-phase and arrival-time terms, records the 7.67 nm rad design beam, and labels every unsupported error scale as a sensitivity assumption.

145. [**Milestone 145 — Scale finite-length effects and narrow map claims (D7)**](145_d7_generality_and_map_scope.md)
    - Adds length and strength scaling for two wire families and compares a sliced vector map with the 3-D field while distinguishing trajectory approximation from the historical vertical-sign input error.

146. [**Milestone 146 — Quantify a corrected ring-error scenario (D5)**](146_d5_corrected_ring_scenario.md)
    - Saves ten seeded girder and magnet error realizations, bounded SVD orbit and tune correction, actual residuals and native dynamic-aperture grids without claiming an as-built machine.

147. [**Milestone 147 — Reconcile pulse phase and native return-pass estimates (D10)**](147_d10_native_pulse_requirements.md)
    - Replaces illustrative linear-return coordinates with native observations, identifies the assumed residual allowance, and supplies a compatible half-sine example with timing, train and eddy-current estimates.

148. [**Milestone 148 — Quantify two-plane transparency tolerances (D9)**](148_round2_transparency.md)
    - Resolve wire and independent-loop sensitivities, finite-beam moment changes, and paired native stored-beam observations at ends of turns 1–50 and 1000. State symmetry as a centroid property and retain the assumed coupling ratio.

149. [**Milestone 149 — Separate RF phase from pulse-relative timing (D4)**](149_round2_timing_audit.md)
    - Correct the pre-campaign timing audit: the 2 ns pulse-relative error changes the NKM amplitude, while the RF-phase term alone shifts the bunch longitudinal coordinate. Preserve the earlier smoke run and make the assumption explicit before any final ensemble.

150. [**Milestone 150 — Apply a declared chamber and report corrected-ring losses (D6)**](150_round2_chamber.md)
    - Apply the author-sourced arc and centre-bend dimensions with declared NKM and IVU assumptions. Compare ideal and ten corrected rings, paired controls, aperture scans and chamber-limited acceptance; nominal capture is 97.0%, while corrected-ring capture ranges from 2.7% to 87.4%.

151. [**Milestone 151 — Prepare checkpointed final ensembles and held-out tuning (D8)**](151_round2_final_campaign_driver.md)
    - Add the gated campaign driver, paired jitter analysis and bounded seven-evaluation tuning search. Freeze realization inputs and source hashes for strict resume; pair corrected-ring and particle seeds, move the return septum consistently, and validate tuned knobs on held-out particles. This milestone completes implementation; the D8 numerical campaign is running and is not yet complete.

152. [**Milestone 152 — Validate chamber operating point and long-turn boundaries (D11)**](152_round2_operating_validation.md)
    - Replace provisional validation with native and affine backend comparisons, refine the connected operating window, and track the nominal point, two interpolated edge candidates and a degraded corrected ring for 4000 turns. Nominal survival falls from 97.0% at 500 turns to 96.1%; fresh edge samples qualify the interpolated 80% boundaries. Reconcile the pulse allowance and independent trajectory checks with the final window.

153. [**Milestone 153 — Report final joint-error ensembles and held-out tuning (D8)**](153_round2_final_robustness.md)
    - Complete nine paired ensembles and 50 bounded tuning studies with the design beam, declared chamber and ten corrected rings. The 150-draw NKM mean is 14.8%; quarter-minus-zero jitter is +2.19 points with a -1.51 to +6.12 interval, so the one-point loss margin is not established. Held-out tuning gains are 11.58 and 5.55 points at zero and quarter jitter, yielding means of 45.66% and 41.82%. Preserve the conditional scope and distinguish all capture summaries.

154. [**Milestone 154 — Reconcile the manuscript with final evidence and scope (D12)**](154_round2_manuscript_reconciliation.md)
    - Rewrite the abstract, comparison table, parameter table, mechanism interpretation, captions and conclusions around the final design-beam evidence. Separate 100 nm sensitivity studies, nominal survival, joint-error capture and held-out tuning. Add sourced system comparisons and conditional septum leakage estimates, clarify deterministic radiation and control-calibration limits, and retain the author-gated generic article format.

155. [**Milestone 155 — Freeze the round-two evidence selection and source snapshot (D13)**](155_round2_evidence_snapshot.md)
    - Select 205 hash-verified artifacts in a new campaign-03 manifest, refresh 17 current D claim rows while preserving historical claims, and package current verification and reproduction notes. Reject dirty source snapshots and changed rebuild macros; include the verification summary in the final inventory. This checkpoint prepares the committed source required for bundle verification; the bundle gate follows.

156. [**Milestone 156 — Verify the frozen referee evidence bundle (D13)**](156_round2_evidence_verification.md)
    - Freeze results/journal_campaign_03/round2_evidence_bundle.tar.gz from committed source 9028978e8f4627efc18a21d6a58f625e7e4b4c2d. The local referee attachment contains 205 selected artifacts and 213 inventoried files; archive size is 15,215,692 bytes and SHA-256 is 0e07de5f2b49a9b9e6087af9f8b9969e9687b0aa537939b77b2325d1d8ec3f3d. No DOI or external upload is implied.

157. [**Milestone 157 — Complete the round-two response and final validation (D14)**](157_round2_final_reconciliation.md)
    - Add a new point-by-point response covering all ten R1B and fifteen R2b tasks, with direct evidence links, final numerical results and explicit claim restrictions. Preserve earlier reviews and the first-round response. The authorized D1-D14 revision is complete; journal selection and conversion remain the separate D15 step.

158. [**Milestone 158 — Journal Recommendation After Round-Two Revision**](158_journal_recommendation_after_round2.md)
    - Read the updated 19-page article and author inputs, checked journal scopes and related publications, and recommended PRAB followed by NIM A and JINST. Identified the missing Sun et al. comparison and preserved D15 as the author’s venue-selection step.

159. [**Milestone 159 — Reviewer 1 Third-Round Manuscript Report**](159_reviewer1_round3_manuscript_report.md)
    - Reviewed the D1–D14 article, recognized resolved second-round concerns, and wrote a new focused-major-revision report with eight tasks. Verified 48 available hashes, documented 157 absent artifacts, and checked directly overlapping PRAB modelling literature while preserving all earlier reviews and manuscript files.

160. [**Milestone 160 — Convert the manuscript to PRAB formats (D15)**](160_prab_manuscript_formats.md)
    - Adopt REVTeX 4.2, compile the primary 28-page one-column draft and 14-page two-column preview from shared scientific text, document PhySH and PRAB submission metadata, and validate both isolated builds with 37 relevant tests.

161. [**Milestone 161 — Plan a standalone BTS optics paper**](161_bts_manuscript_outline.md)
    - Draft a JKPS-oriented manuscript outline and twelve ordered preparation tasks from the selected matching solution and hash-verified 550,000-sample optics campaign, with correction/transport work and optional MOGA requirements clearly marked as pending.

162. [**Milestone 162 — Create the first BTS LaTeX manuscript draft**](162_bts_latex_draft.md)
    - Write and compile an eight-page one-column BTS article draft with four exported archived-data tables, six audited references, provenance and explicit pending revisions; preserve all NKM files and scientific inputs.

163. [**Milestone 163 — Fix scientific question, novelty, and evidence inventory (B01)**](163_b01_scientific_question_novelty_and_evidence_inventory.md)
    - Established article scope, distinct BTS research questions, NKM overlap disclosures, JKPS/DLSR literature comparisons, full evidence audit of optimization (`fe107589...`) and 4 tolerance runs (`62062629...`, `d1f381f7...`, `353c1986...`, `fa3c0b82...`), individual audits of all 5 physical feasibility failures across 550,000 samples, and a comprehensive claim ledger mapping 12 claims to verified artifacts.

164. [**Milestone 164 — Reconcile manuscript status through D15**](164_manuscript_status_reconciliation.md)
    - Correct stale D15 status, link completed PRAB formatting and pending third-round scientific tasks, and record the separate BTS B01 completion with B02 next.

184. [**Milestone 184 — Review the BTS manuscript on main**](184_bts_main_manuscript_review.md)
    - Assess the version-identified eight-page BTS draft, verify selected hashes/failure records, recommend major revision and create ten ordered tasks while preserving prior reviews and distinguishing the later BTS-branch article.

185. [**Milestone 185 — Move BTS reviews into the BTS manuscript directory**](185_bts_review_directory.md)
    - Move the BTS report and revision register into their dedicated review directory, repair links and separate the BTS and NKM review indexes while preserving review content and scientific inputs.

186. [**Milestone 186 — Resolve the main-branch review rebase conflicts**](186_main_rebase_conflict_resolution.md)
    - Complete both review commits on the updated main base, preserve corrected NKM manuscript status and separate BTS reviews, and verify links and protected inputs.

187. [**Milestone 187 — R1-BTS-01: Freeze BTS reviewer revision identity**](187_r1_bts_01.md)
    - Select the main-branch draft, preserve baseline asset hashes and reopen the B01 audit while distinguishing the later BTS article.

188. [**Milestone 188 — R1-BTS-02: Correct BTS claims and artifact provenance**](188_r1_bts_02.md)
    - Audit twelve BC claims with exact JSON pointers, repair restart, Jacobian, OAT, failure and boundary interpretations, and record artifact-specific metadata.

189. [**Milestone 189 — R1-BTS-03: Establish the BTS physical question and primary literature**](189_r1_bts_03.md)
    - Replace unsupported regional and global comparisons with checked primary passages and define a paired physical-clearance design question.

190. [**Milestone 190 — R1-BTS-04: Specify BTS boundaries beam and model constraints**](190_r1_bts_04.md)
    - Freeze the source-labelled model, full design-beam covariance and assumed hardware limits; record actual aperture positions and legacy MAD-X non-equivalence.

191. [**Milestone 191 — R1-BTS-05: Validate independent BTS transport and active errors**](191_r1_bts_05.md)
    - Implement hard-edge affine transport, coupled covariance and fixed-geometry active errors; validate against AT particle maps and Gaussian transport.

192. [**Milestone 192 — R1-BTS-06: Reproduce BTS matching and all search outcomes**](192_r1_bts_06.md)
    - Replay all three historical starts and independently verify raw and rounded settings with optical, family-bound and model-clearance checks.

193. [**Milestone 193 — R1-BTS-07: Normalize BTS response and withdraw operational knob claims**](193_r1_bts_07.md)
    - Define dimensionless row and actuator scaling, verify finite-difference convergence and local finite response, and withdraw unsupported practical correction claims.

194. [**Milestone 194 — R1-BTS-08: Evaluate frozen BTS designs on held-out machines**](194_r1_bts_08.md)
    - Complete constrained low-beta design and paired physical-clearance/particle comparisons on 200 held-out machines with independent shots.

195. [**Milestone 195 — R1-BTS-09: Reconstruct BTS statistics and qualify tolerance claims**](195_r1_bts_09.md)
    - Audit all 550000 historical observations and pooling fields, reconstruct quantile/failure intervals and preserve missed prefixes while separating new physical transport.

196. [**Milestone 196 — R1-BTS-10: Prepare the revised BTS article and referee evidence package**](196_r1_bts_10.md)
    - Prepare the eight-page article, seventeen-claim ledger, point-by-point response and portable raw-evidence package; author-confirmed declarations and actual submission delivery remain pending.

197. [**Milestone 197 — Restore BTS branch review history**](197_restore_bts_branch_reviews.md)
    - Recover three historical rounds of reports, revision tasks and author responses verbatim from local bts, preserving current reviews and documenting their manuscript scope.

198. [**Milestone 198 — Second review of the revised BTS main-branch article**](198_bts_main_round2_review.md)
    - Assess the revised eight-page article, independently reconstruct paired statistics and add a major-revision report with eight ordered tasks while preserving all previous reviews.

199. [**Milestone 199 — R2-BTS-01: Freeze BTS round-two evidence and physical protocol**](199_r2_bts_01.md)
    - Preserves the reviewed article and original campaign; corrects beta-versus-clearance attribution and declares independently seeded parametric comparisons.

200. [**Milestone 200 — R2-BTS-02: Resolve the BTS limiting-station mechanism**](200_r2_bts_02.md)
    - Reconstructs all original station clearances and shows that every exact shot tie is entrance-limited; exports variance decomposition and gain/loss heterogeneity.

201. [**Milestone 201 — R2-BTS-03: Validate BTS clearance at actual shot centroids**](201_r2_bts_03.md)
    - Compares affine and centred transport across all original shots, measures the paired model shift and checks nonlinear Gaussian moments with converged quadrature.

202. [**Milestone 202 — R2-BTS-04: Refine BTS beta extrema inside magnets**](202_r2_bts_04.md)
    - Measures interior maxima, preserves original boundary values and reoptimizes the low-beta alternative with a converged spatial observation mesh.

203. [**Milestone 203 — R2-BTS-05: Compare BTS clearance strategies on independent machines**](203_r2_bts_05.md)
    - Freezes nominal clearance settings and evaluates all nine regime/design combinations on new machines, demonstrating beneficial and adverse beta-reduction regimes.

204. [**Milestone 204 — R2-BTS-06: Reconstruct BTS inference and define finite loss events**](204_r2_bts_06.md)
    - Verifies all new paired intervals, separates clearance from transmission and defines sampled three-shot block losses with exact finite-sample uncertainty.

205. [**Milestone 205 — R2-BTS-07: Recast the BTS article around active restrictions**](205_r2_bts_07.md)
    - Integrates the physical mechanism, refined strategies and independent tests into a ten-page article with a three-page supplement, five figures and reconciled source-labelled evidence.

206. [**Milestone 206 — R2-BTS-08: Prepare declarations and portable referee evidence**](206_r2_bts_08.md)
    - Confirm no competing interests and verify portable evidence reproduction; funding, acknowledgments, scientific approval and external referee delivery remain pending author actions.

207. [**Milestone 207 — Native Accelerator Toolbox BTS figures**](207_bts_native_at_figures.md)
    - Draws main optics and lattice figures with native pyAT functions, verifies frozen-profile agreement and rebuilds the manuscript with refreshed asset identities.

208. [**Milestone 208 — BTS entrance and exit phase-space distributions**](208_bts_phase_space_figures.md)
    - Adds reproducible particle clouds and native AT covariance ellipses in both planes, updates article interpretation and extends portable evidence.

209. [**Milestone 209 — Reviewer 2, Third-Round Report on the PRAB Manuscript**](209_reviewer2_round3_report.md)
    - Major revision focused on robustness: operating point not re-selected for the design beam, orbit-only ring correction stopped at 100 µm, NKM chamber enclosing its conductors; evidence bundle verified; tasks R2c-1 to R2c-9.

210. [**Milestone 210 — Consolidated Round-3 Revision Plan**](210_consolidated_revision_plan_round3.md)
    - Reconciled R1C-01–08 and R2c-1–9 into E1–E11 with author inputs B1–B5; one robustness rerun after fixing the NKM chamber, ring correction and design-beam operating point; synthesis and noninferiority wording on the rerun.

211. [**Milestone 211 — E1: Evidence Access and Re-verification**](211_e1_evidence_access.md)
    - Round-2 bundle hash, 213-entry inventory and an isolated archived-source macro rebuild all verify; 205/205 manifest artifacts match; access route documented.

212. [**Milestone 212 — E2: Positioning Against Sun et al. (2020)**](212_e2_literature_positioning.md)
    - Established tools (segmented tracking, finite conductors) credited to Sun et al.; contribution restated as a quantified thin-map error in an angle-cancelling, large-sagitta geometry; ALS row added; clean gated builds.

213. [**Milestone 213 — E3: Normalised Finite-Length Approximation Error**](213_e3_normalised_scaling.md)
    - Thin-map |Δp_x|/|K| = 1.95 η^1.46 (3.4 % scatter, both families); sliced map < 2e-5 |K|; declared 0.1-window allowance reached at η* ≈ 0.036 (nominal 0.034 uses 91 %).

214. [**Milestone 214 — E4: Feasible NKM Vacuum Chamber**](214_e4_nkm_chamber.md)
    - Flat 16 x 3.8 mm in-magnet chamber below the wires (1.5 mm allowance, Sun et al.), applied on the injection pass and every turn; normalised vertical aperture 1.61 (tightest with open IVUs); ideal-ring design-beam capture unchanged at 97.0 % for 3.0-4.3 mm.

215. [**Milestone 215 — E9: Transparency Units, Simultaneous Construction Errors and Septum Leakage**](215_e9_transparency_tolerances.md)
    - Aligned moments stated as Δε/ε; 10 um rms wire placement already gives median 2.6/4.8 sigma (x/y), so compensation is required; septum leakage must be ≲0.07 G at the stored orbit, 50x below the published bumped-orbit value.

216. [**Milestone 216 — E5: Corrected Ring Population With Optics Correction**](216_e5_corrected_ring.md)
    - Same ten error draws with BPM references, converged orbit, beta-beat/dispersion and tune correction: beta-beat ≤ 2 %, NKM orbit ≤ 56 um, first unstable launch −11.0 to −9.5 mm; ring 5501 recovered (−7.5 → −10.5 mm); 70–80 um orbit floor set by the 120 correctors.

217. [**Milestone 217 — E6: Operating Point Re-selected for the Design Beam**](217_e6_operating_point.md)
    - Declared clearance/knob/objective rule over the corrected rings: x_inj −19.48 mm, S 0.95 (2 mm blade); ring mean 78.0 % vs 68.9 % at the round-2 point (p10 65.7 vs 43.3 %); gain from a 1.1 mm smaller injected amplitude; control-calibration defect fixed.

218. [**Milestone 218 — E6 Follow-up: Window, Validation and Chamber Study at the Selected Point**](218_e6_point_studies.md)
    - Selected point: windows 0.44 mrad / 2.40 mm, nominal 98.4/97.8 % (500/4000 turns), corrected-ring mean 78.0 % (p10 65.7 %); thin map no longer within the accuracy allowance (155 %); robustness section awaits E7.

219. [**Milestone 219 — E10: Supplemental Material and Presentation Fixes**](219_e10_supplement_presentation.md)
    - Supplement (trajectory table, wire/loop tables, 100 nm sensitivity case, statistical methods with noninferiority wording, procedures); first-unstable-launch definition; open-IVU gap justified; both layouts build clean.

220. [**Milestone 220 — E7: The Single Robustness Rerun**](220_e7_robustness_rerun.md)
    - At the E6 point on E5 rings with the chamber: NKM joint mean 16.1 % (ring-cluster [10.9, 21.5]) vs dipole 44.1 %; zero jitter 40.1 %; quarter jitter now costs 5.7 points; matched tuning +11.9 points; booster angle the only significant driver.

221. [**Milestone 221 — E8: Physical Synthesis and Manuscript Rewrite**](221_e8_synthesis.md)
    - Hierarchy table; ring errors cost NKM and dipole alike (chromaticity/beta-beat), the on-axis DA margin does not organize capture, and the NKM-specific loss is injection angle errors on a 0.44 mrad window; abstract, discussion and conclusions rewritten; noninferiority wording.

222. [**Milestone 222 — E11: Final Reconciliation of the Round-3 Revision**](222_e11_final_reconciliation.md)
    - Round-3 response, claim rows E0–E11, cover letter; clean 30/15-page PRAB builds and 6-page supplement; 730 tests pass; round-3 bundle (e65a86c0…) verified by byte-identical archived-source rebuild.

223. [**Milestone 223 — Reviewer 2, Round-4 Report**](223_reviewer2_round4_report.md)
    - Major revision of limited scope: booster jitter costs NKM and dipole alike, so the 28-point NKM-specific gap arises at zero jitter; ablation, paired wider-window points and a pulse section at the selected point requested (R2d-1 to R2d-7).

224. [**Milestone 224 — Reviewer 2 Report on the BTS Manuscript**](224_reviewer2_bts_report.md)
    - Major revision: nominal end clearances are analytically K-independent, positive results rest on hypothetical m2/m3 restrictions, the exit septum blade and element apertures are missing, no trajectory correction, and mean clearance is not loss-relevant (R2B-01 to R2B-07).

225. [**Milestone 225 — R2B-02: Boundary-Fixed End-Station Clearances**](225_r2b_02_boundary_clearances.md)
    - Analytic proof and test that the BTS end-station clearances are independent of the quadrupole settings; Section 3.1 and abstract rewritten.

226. [**Milestone 226 — R2B-01: Element-Wise Aperture Model**](226_r2b_01_elementwise_apertures.md)
    - Apertures on every element with the companion-derived septum blade; the blade channel (0.648 mm) is active and independent of the quadrupoles, interior margins ≥ 9 mm; four-station study moved to the supplement.

227. [**Milestone 227 — R2B-03: Trajectory Correction**](227_r2b_03_trajectory_correction.md)
    - Steering cuts BTS loss from 10 % to 1.6 % (amended layout controlling exit angle; declared layout reported too); the residual is booster jitter; Gaussian loss prediction matches tracking within 0.6 %.

228. [**Milestone 228 — R2B-04: Jitter Transfer and Loss-Based Setting**](228_r2b_04_loss_based_design.md)
    - Matched ends make exit jitter a function of μx only; reachable μx 200–232°; the loss-based setting at 200.2° cuts tracked loss on fresh steered machines from 2.32 % to 0.66 % (−1.66 [−2.42, −0.99] pp) at +13 % exit-angle jitter, while mean clearance sees nothing.

229. [**Milestone 229 — R2B-05: Exit Target and Dispersion-Free Exit**](229_r2b_05_exit_target.md)
    - m4 equals the companion injected beam; divergence 76 µrad (50 dispersive); a dispersion-free exit is feasible (115/120 starts, peaks < 60 m), widens μx to 188–214° and cuts predicted blade loss 65-fold at higher exit-angle jitter.

230. [**Milestone 230 — R2B-06: Error-Level Sensitivity**](230_r2b_06_error_sensitivity.md)
    - Roll level (0.1–0.5 mrad) has no effect on the horizontal blade loss and energy jitter (0.05–0.1 %) little; the ranking is unchanged; the loss is heavy-tailed over machines (top 5 of 200 carry 39 %).

231. [**Milestone 231 — R2B-07: Re-Framed BTS Article and Records**](231_r2b_07_article_reframing.md)
    - New title, abstract, introduction and conclusions around septum loss and jitter transfer; KLS naming; claim ledger BR3-01–13, final asset hashes, reproduction guide and Reviewer 2 response; 743 tests pass.

232. [**Milestone 232 — BTS Spatial-Subdivision Test Tolerance**](232_bts_spatial_test_tolerance.md)
    - Platform-dependent exact comparison of mathematically equal boundary peak betas replaced by a 1e-12 relative tolerance.

233. [**Milestone 233 — BTS Article Title Reverted**](233_bts_title_reverted.md)
    - Title restored to "Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line" at the user's request.

234. [**Milestone 234 — BTS Round 3 on the Unchanged Lattice**](234_bts_unchanged_lattice_rerun.md)
    - Added correctors removed at the author's instruction; steering by trims of the existing dipoles; all round-3 stages rerun (steered loss 1.68 %, fresh-test loss-based 0.69 % vs 2.30 %); records reconciled; 743 tests pass.

235. [**Milestone 235 — Reviewer 1 round 4 and current revision planning**](235_reviewer1_round4_and_revision_status.md)
    - Records focused major revision, consolidates both round-4 reports into pending F1–F9 under the round-3 plan and refreshes stale status documents without executing scientific tasks.

235. [**Milestone 235 — Round-4 Plan Split**](235_round4_plan_split.md)
    - F1–F9 moved from the round-3 plan into `consolidated_revision_plan_round4.md`; stub keeps old anchors; working links updated; review records untouched.

236. [**Milestone 236 — F1: Round-4 Protocol**](236_f1_round4_protocol.md)
    - Protocol, seven error classes and the F3 decision rule declared; E7 realization 0 reproduced bitwise; earlier and extremum-centred (x_inj −20.751 mm, S 0.95) candidates checked.

237. [**Milestone 237 — F4: Signed and Physical Associations**](237_f4_associations.md)
    - Post-kick centroid amplitude organises capture for both kickers; NKM-specific signed offset term; zero-capture 51 % vs 10 %; angle jitter costs the dipole as much as the NKM.

238. [**Milestone 238 — F6: Septum Dispersion and Accuracy Scope**](238_f6_dispersion_scope.md)
    - Septum dispersion budget (50 of 76 µrad divergence dispersive); η fit labelled synthetic; production thin-map error 161 µrad at the current point (3.7× allowance), 35–47 µrad near the extremum; sliced map < 1e-7 rad.

239. [**Milestone 239 — F5: Where the Beam Is Lost**](239_f5_loss_locations.md)
    - NKM zero-capture events are first-turn losses (1491/1500), mostly vertical, none in the magnet; ring 5501 loses vertically over many turns for both kickers, not because of the in-magnet chamber; chromaticity claim reduced.

240. [**Milestone 240 — NRF Funding Acknowledgement**](240_nrf_acknowledgement.md)
    - NRF grant RS-2022-00143178 acknowledged in both papers (NKM acknowledgments; BTS Funding and Acknowledgments); PDFs rebuilt.

241. [**Milestone 241 — F2: Error-Class Ablation**](241_f2_error_class_ablation.md)
    - Paired zero-jitter ablation (15 ensembles): BTS magnet errors remove 39 points of NKM and 14.5 of dipole capture and explain most of the 28-point gap; all other classes ≤ 1.6 points; post hoc, the uncorrected vertical centroid (0.90 mm rms) tracks NKM capture.

242. [**Milestone 242 — F3: Operating-Point Test**](242_f3_operating_point_test.md)
    - Paired earlier/extremum-centred versus current point at zero and full budget: no candidate meets the declared rule, so the current point is retained; NKM capture is flat across points while the dipole control loses 17–23 points, so the NKM-dipole gap is point-dependent.

243. [**Milestone 243 — Two-Plane Steering Sensitivity**](243_vertical_steering_sensitivity.md)
    - Declared sensitivity with ideal static steering in both planes: at zero jitter NKM capture rises 40.1 → 76.6 % (gap −28.3 → −6.1); at full budget booster jitter becomes NKM-specific (gap −17.2 points), so the vertical error and the jitter overlap.

244. [**Milestone 244 — F7: Pulse and Transparency at the Current Point**](244_f7_pulse_transparency.md)
    - Pulse and transparency recomputed at S = 0.95 with one allowance convention (0.044 mrad); pulse limits 5.76/5.33 µs keep the 5.3 µs example valid; a 0.2 mm offset now gives 0.11–0.12 σ; round-4 manifest re-points the pulse/transparency keys and keeps S = 0.85 as history.

245. [**Milestone 245 — F8: Manuscript Rewrite from the Round-4 Evidence**](245_f8_manuscript_rewrite.md)
    - Abstract, new attribution subsection (ablation, vertical mechanism, two-plane sensitivity with jitter components, point test), robustness, discussion and conclusions rewritten from F2–F7; round-4 numbers generated by `round4_reporting.py`; import-policy test fixed; 756 tests pass; both layouts compile cleanly.

246. [**Milestone 246 — F9: Round-4 Reconciliation**](246_f9_round4_reconciliation.md)
    - Round-4 response, claim rows F0–F9, point-identity check, all figures rebuilt with matplotlib 3.11.1, clean builds (33/17/7 pages), 757 tests pass, verified round-4 evidence bundle (SHA-256 dbe3a7a8…); author's scientific approval pending.

247. [**Milestone 247 — BTS Availability Wording and Referee Attachment**](247_bts_availability_attachment.md)
    - BTS paper cites the round-4 companion result (jitter once the vertical error is removed; vertical correction left to future work), final data-availability statement installed, verified 826-file referee attachment (SHA-256 92b1fb21…); author approval pending.

248. [**Milestone 248 — Clean-checkout round-four CI tests**](248_fix_clean_checkout_round4_ci.md)
    - Reproduces seven remote failures caused by ignored campaign inputs and replaces those dependencies with temporary fixtures while preserving physics and manifest checks.

249. [**Milestone 249 — Clarify the BTS abstract boundary conditions**](249_bts_abstract_boundary_wording.md)
    - State the injection-optics requirement and qualify endpoint size invariance by fixed beam parameters and prescribed matching; rebuild the 12-page PDF and verify current asset hashes.

250. [**Milestone 250 — Use siunitx for BTS quantities**](250_bts_si_unit_formatting.md)
    - Format explicit main/supplement quantities with siunitx, rebuild both PDFs through the layout gate and refresh verified asset hashes.

251. [**Milestone 251 — Strengthen the BTS introduction and scientific presentation**](251_bts_introduction_editorial_revision.md)
    - Develop the introduction and section roadmap, adopt American English, clarify dipole/lattice terminology, remove revision-oriented wording, and cite the companion manuscript as in preparation; rebuild both PDFs and verify asset hashes.

252. [**Milestone 252 — Clarify BTS methods, add accuracy tables and improve figures**](252_bts_methods_accuracy_and_figures.md)
    - Define quadrupole labels, use Courant–Snyder terminology, simplify numerical-method prose, add SLSQP and accuracy/convergence tables, and improve Figures 2–3 with validated regeneration; 26 relevant tests and both manuscript builds pass.

253. [**Milestone 253 — Explain the BTS septum geometry and field treatment**](253_bts_septum_geometry_explanation.md)
    - Distinguish the centroid-to-blade distance from thickness and reference-orbit offsets, state the dipole/aperture field model and inherited assumptions, and rebuild the verified main PDF.

254. [**Milestone 254 — Simplify the BTS manuscript title**](254_bts_manuscript_title.md)
    - Retitle the article “Optical matching and beam loss in a booster-to-storage-ring transfer line,” update its README and rebuild the verified PDF without changing the scientific body.

255. [**Milestone 255 — Identify Korea Light Source in the BTS title**](255_bts_korea_light_source_title.md)
    - Add Korea Light Source to the manuscript title, synchronize its README and rebuild the verified PDF while preserving the scientific body.

256. [**Milestone 256 — Use Booster-to-Storage in the BTS title**](256_bts_booster_to_storage_title.md)
    - Apply the requested Booster-to-Storage title wording, synchronize the current README and rebuild the verified PDF.

257. [**Milestone 257 — Make the BTS abstract qualitative, expand the review and add the layout**](257_bts_qualitative_abstract_literature_layout.md)
    - Remove abstract numbers, expand the primary-source literature comparison, add a shared-coordinate BTS magnet layout below Figure 3, and validate both builds, current assets and 14 relevant tests.

258. [**Milestone 258 — Update the BTS manuscript keywords**](258_bts_manuscript_keywords.md)
    - Set the requested beam dynamics, error analysis, Korea Light Source and transfer line keywords; rebuild the verified PDF without changing the scientific text.

259. [**Milestone 259 — Use the original BTS setting as the optimization reference**](259_bts_original_setting_reference.md)
    - Replace the reference in Figures 2–3 with original BTSConfig strengths, expose negative original clearance, add a nominal optimization table and reframe the study; preserve matched-only ensemble identities, with 15 tests and both builds passing.

260. [**Milestone 260 — Rewrite setup.sh as a sourced environment loader**](260_setup_environment_loader.md)
    - Model setup.sh on mobo-linac: sourcing guard, PROJECT_ROOT, conda activation of pyat-dev with override and warnings, and a check that nkm_injection is the editable install from this checkout.

261. [**Milestone 261 — BTS author wording revision, KLS TDR citation and split affiliations**](261_bts_author_wording_revision.md)
    - Apply the author's BTS wording list (baseline/matched reference, error realizations, units, Tikhonov, Eq. 2), cite the Korea-4GSR TDR, label Figure 1, revise Tables 1–2, remove the AI, availability and appendix sections, and split affiliations in both papers.

262. [**Milestone 262 — Reviewer 2 round-3 report on the BTS manuscript**](262_reviewer2_bts_round3_report.md)
    - Major revision: the 0.5 mm / 0.2 mrad booster jitter (about five beam sizes) drives every loss number and is not varied, and the baseline-versus-optimized headline is circular. Ten tasks, R2C-01 to R2C-10.

263. [**Milestone 263 — Reviewer 1 BTS round-3 report**](263_bts_reviewer1_round3_report.md)
    - Assesses all three main-branch author responses, credits the held-out loss result and records focused major revision with eight pending tasks; previous reviews and scientific assets are preserved.

264. [**Milestone 264 — Consolidated round-4 BTS revision tasks**](264_bts_round4_consolidated_tasks.md)
    - Merge the Reviewer 1 (R3-BTS-01 to 08) and Reviewer 2 (R2C-01 to 10) round-3 registers into fourteen R4-BTS tasks, with source mapping, reviewer-difference resolutions and a computation summary.

265. [**Milestone 265 — R4-BTS-03: exact round-aperture loss and valid bounds**](265_r4_bts_03_round_aperture_loss.md)
    - Exact 2-D Gaussian loss outside round/elliptical apertures and a valid max/union bracket. The isotropic 5σ counterexample is tested. The rerun reproduces all 66 selected round-3 numbers bitwise.
