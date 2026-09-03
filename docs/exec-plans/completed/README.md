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
    - Created comprehensive setup instructions (`INSTALLATION.md`) and package installation verification workflows.

20. [**Milestone 20 — Task 03: Consolidated Technical Document & GitHub.io Project Webpage**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/20_task03_consolidated_document_and_website.md)
    - Authored consolidated LaTeX report (`docs/nkm_consolidated_report.tex` / `.pdf`) and built modern github.io webpage (`docs/index.html`) featuring author Chong Shik Park and Korea University affiliation.

21. [**Milestone 21 — Task 04: Full Production Simulation Script, Parity Notebook, & Documentation**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/21_task04_full_simulation_script.md)
    - Constructed unified full production shell script (`scripts/run_full_production_simulation.sh`), matching Jupyter notebook (`notebooks/04_full_production_simulation.ipynb`), and documentation (`docs/FULL_PRODUCTION_SIMULATION.md`), with 90% CPU parallelization option and screen verbosity toggle. Held dry run execution per user signal.

22. [**Milestone 22 — Task 04: Production Simulation Dry-Run & Quiet-Mode Progress Enhancements**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/22_task04_dry_run_and_quiet_mode_enhancements.md)
    - Implemented `-d` / `--dry-run` pre-flight syntax and parameter validation, enhanced `--quiet` mode real-time step notifications (`[RUNNING]` / `[COMPLETED]`), and updated `docs/FULL_PRODUCTION_SIMULATION.md`.

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
    - Compiled publication-grade Journal of Instrumentation (JINST) manuscript [`docs/jinst-paper/paper.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/jinst-paper/paper.pdf) with author Chong Shik Park (Korea University) attribution, incorporating RADIA 2D field map validation, single-objective SLSQP matching, NSGA-II multi-objective optimization, and Monte Carlo 6D robust particle tracking.

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
    - Synchronized `docs/jinst-paper/paper.tex`, `docs/jinst-paper/paper.pdf`, and `docs/index.html` with full production simulation results (`results/production_run_20260815_153100`). Updated multi-turn metrics ($430\times$ stored beam perturbation reduction to $4.76\,\mu\text{m}$), SLSQP converged optics ($\beta_{x,\max}=30.66\,\text{m}, \beta_{y,\max}=52.54\,\text{m}$, mismatch $< 10^{-6}$), OAT error sensitivity rankings, and verified 100% test pass rate across 174 tests.

61. [**Milestone 61 — Task: Refactor Fix Quadrupole Roll Symplectic Rotation Matrix**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/61_refactor_fix_quadrupole_roll_symplectic_rotation.md)
    - Fixed a physics defect in quadrupole roll error coordinate transformations in `src/nkm/errors.py` by rotating both transverse spatial coordinates $(x, y)$ and momenta angles $(x', y')$ simultaneously in `R1` and `R2`. Added symplectic condition unit tests in `tests/test_errors.py` and verified 100% pass rate.

62. [**Milestone 62 — Task: Refactor Unify 4-Model Injection Tracking and Stored-Beam Closed-Orbit Kick**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/62_refactor_unify_four_model_injection_and_stored_beam_kick.md)
    - Upgraded `simulate_nkm_models` in `src/nkm/injection.py` to evaluate all 4 canonical models (`off`, `ideal`, `linear`, `fieldmap`), exposed stored-beam dipole deflection under the ideal kicker model, and corrected the closed-orbit stored beam kick calculation in `src/nkm/robust_optimization.py` to evaluate physical field map deflections. Verified 100% pass rate across 175 tests.

63. [**Milestone 63 — Task: Refactor Centralize Kicker Model Types and Optimize Multi-Turn Tracking Memory**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/63_refactor_centralize_kicker_model_types_and_in_place_tracking.md)
    - Centralized canonical `KickerModelType`, `CANONICAL_KICKER_MODELS`, and `validate_kicker_model()` in `src/nkm/units.py`. Enforced validation across `storage_ring_injection.py` functions and optimized multi-turn tracking by eliminating per-turn full-array copies with in-place matrix updates. Verified 100% test pass rate.

64. [**Milestone 64 — Task: Refactor Isolate RNG Generators for Thread Safety and Reproducibility**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/64_refactor_isolate_rng_generators_for_thread_safety.md)
    - Replaced global `np.random.seed(...)` mutations in `generate_6d_beam` with isolated `np.random.default_rng(seed)` and direct Cholesky factorizations. Added RNG isolation tests in `tests/test_units.py` and verified 100% pass rate across 177 tests.

65. [**Milestone 65 — Task: Update Documentation, JINST Paper, and Project Site for All Refactors**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/65_update_documentation_paper_and_site_for_all_refactors.md)
    - Updated `README.md` and `docs/index.html` with the 177-test verification suite, updated `docs/jinst-paper/paper.tex` with symplectic roll rotation and isolated RNG notes, and recompiled `docs/jinst-paper/paper.pdf`. Verified 100% test pass rate.

66. [**Milestone 66 — Task: Bump Framework Version to v0.2.0**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/66_bump_version_to_v0_2_0.md)
    - Incremented repository version from `0.1.0` to `0.2.0` across `pyproject.toml`, `src/nkm/__init__.py`, `CITATION.cff`, and `docs/index.html`. Reinstalled editable package and verified 100% test pass rate.

67. [**Milestone 67 — Task: Isolate Website Files in docs/site/ for GitHub Pages Deployment**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/67_isolate_website_in_docs_site_for_github_pages.md)
    - Created isolated static website bundle in `docs/site/` (`index.html`, `style.css`, `.nojekyll`, reports, and documentation) and created `scripts/sync_site.sh` for syncing with standalone `nkm-injection.github.io` repository. Verified 100% test pass rate.

68. [**Milestone 68 — Task: Update Repository Name and URLs to nkm-injection**](file:///home/cspark/Work/projects/nkm-injection/docs/exec-plans/completed/68_rename_repo_to_nkm_injection.md)
    - Updated repository and package names across `pyproject.toml` (`nkm-injection`), `CITATION.cff`, `README.md`, `docs/INSTALLATION.md`, `docs/reproducibility.md`, `scripts/setup_environment.sh`, and documentation website links (`https://github.com/nkm-injection/nkm-injection`). Verified 100% test pass rate.

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















