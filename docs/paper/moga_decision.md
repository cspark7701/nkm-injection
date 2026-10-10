# Role of Pareto (NSGA-II) optimisation in the article (Task 007)

Decided 2026-10-09: **MOGA is omitted from the main-text claims; no new S8 campaign is run.**
The deterministic SLSQP matching (feasible, M_x = M_y = 0 to numerical precision, β_max 31.4/50.7 m)
is the single BTS design used by the injection, tolerance and capture studies.

## Reasons (traceable to code and selected artifacts)

1. **No distinct physical design question.** The principal question (article_scope.md) concerns the
   NKM capture/transparency window. The MOGA objectives — M_x+M_y, max β along the BTS, and
   f₃ = √(ΔD_x² + ΔD′_x²) — are BTS-optics quantities; none measures capture or stored-beam disturbance.
   The deterministic optimum already reaches zero mismatch with peak β inside the 60 m limit.
2. **Dimensionally inconsistent objective.** f₃ adds metres (D_x) and dimensionless D′_x in quadrature
   (`moga.py`, `BTSMOGAProblem`), so its Pareto ordering depends on an arbitrary unit choice.
3. **Finalist evaluation is not a physical capture measurement.** `reevaluate_pareto_finalists` runs the
   legacy end-to-end pipeline with `kicker_model="ideal"` for 10 turns (selected run: 1000 particles,
   2 MC seeds), i.e. the uncalibrated control and a turn count below the 200–500 turns needed for
   capture convergence (model_validation.md).
4. **Repeatability is unestablished at the archived budget.** Population 40 × 20 generations; seed 42
   reached only 20 % feasible fraction and 4 Pareto points versus 21–40 for the other seeds
   (`moga/multi_seed_moga_summary.json`), with knee-point strength spread 1.27 m⁻² across seeds.
   Establishing a converged front (≥ 100 × 100 budgets, common hypervolume reference) would not change
   the article's conclusions because the design used downstream is the deterministic optimum.

## Consequence for the manuscript

Remove the MOGA formulation, knee-point tables, hypervolume numbers and the claim of a "61.5×"
improvement (claim_evidence.csv A6–A8). MOGA may be mentioned only as available software
(data/software availability statement) without performance claims. If a future article targets BTS
design trade-offs, Task 007's extended campaign (corrected f₃ normalisation, injection-aware objectives,
native finalist tracking) is the prerequisite.
