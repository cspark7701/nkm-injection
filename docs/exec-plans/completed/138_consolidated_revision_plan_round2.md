# Milestone 138 — Consolidated round-2 revision plan

Completed: 2026-10-11. User request: read the round-2 reviewer reports and revision tasks, and decide the
consolidated execution tasks and their order.

**Inputs.**
- Reviewer 1, round 2: `reviewer1_round2_20261011_report.md` and its register (R1B-01 to R1B-10). Recommendation:
  focused major revision.
- Reviewer 2, round 2: `reviewer2_report_round2.md` (R2b-1 to R2b-15). Recommendation: major revision.

**Output.**
- `docs/paper/reviews/consolidated_revision_plan_round2.md`, containing:
  - agreement and differences between the reviewers;
  - an adopted-resolution table;
  - author inputs A1–A6;
  - tasks D1–D15 with coverage, acceptance and cost;
  - the dependency order.
- A new link row in the reviews `README.md`.
- The round-1 plan and response are unchanged.

**Key decisions.**
- **Realism tasks.** The realism tasks are adopted in reduced, feasible form:
  - corrected ring-error scenario (10 seeds, 120 HVC correctors, BPM markers);
  - chamber model with loss map;
  - reduced beam-based tuning (seed 42, 50 realizations).

  They are labelled as scenarios, as Reviewer 1 asks.
- **Ensemble reruns.** The expensive robustness ensembles run once (D8), after the budget (D4), the corrected ring
  (D5) and the chamber (D6) are fixed.
- **Integrator validation first.** The independent trajectory validation (D3) gates every new simulation.
- **Cheap independent tasks.** D7 (generality and claims), D9 (transparency tolerances) and D10 (pulse) run in
  parallel with the compute queue.
- **Author decisions.** The chamber profile, lattice version, NKM powering, booster data, coupling target and target
  journal are requested as A1–A6, with defaults.

**Feasibility checks (read only).**
- The lattice has 120 correctors (HVC), BPM markers in every cell and 140 girders, so the corrected-error study is
  feasible.
- There are no aperture elements and no chamber or booster specification in the repository.
- The compute estimates are scaled from the round-1 logs: about 40 min per combined-error seed and 19 min per jitter
  level with 8 workers.

**Status.** No manuscript, code or result files changed. Protected files are unchanged.
