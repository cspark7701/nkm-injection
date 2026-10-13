# Milestone 210 — Consolidated round-3 revision plan

Completed: 2026-10-13. User request: create a consolidated revision plan for round 3.

**Inputs.**
- Reviewer 1, round 3 (R1C-01 to R1C-08).
- Reviewer 2, round 3 (R2c-1 to R2c-9).

**Output.**
- `docs/paper/reviews/consolidated_revision_plan_round3.md`, containing:
  - how the two reviews relate;
  - an adopted-resolution table;
  - author inputs B1–B5 with defaults;
  - tasks E1–E11 with coverage, acceptance and cost;
  - the dependency order.
- A link from the reviews `README.md`. Earlier plans and responses are unchanged.

**Key decisions.**
- **One robustness rerun (E7).** It comes only after the three model defects are fixed: a feasible NKM chamber (E4),
  converged orbit plus β-beat correction of the same ten seeds (E5), and design-beam operating-point re-selection on
  that model (E6). Population sizes are unchanged, which respects Reviewer 1's restriction.
- **Synthesis on the rerun.** The robustness-hierarchy synthesis (R1C-04 / R2c-5) runs on the rerun results (E8).
- **Work that does not wait.** Evidence access (E1), literature positioning against Sun et al. 2020 (E2) and the
  normalised scaling error (E3) need no new runs. The transparency items (E9) run during the compute wait.
- **Results directory.** New results go to `results/journal_campaign_04/`; campaign 03 stays frozen as round-2
  evidence.

**Feasibility checks (read only).**
- The lattice has 120 HVC correctors, no skew elements, 168 sextupoles and 344 individually addressable quadrupoles.
  Coupling correction therefore needs author input B1.
- From the round-2 logs, D5–D8 took about 4 h with 8 workers.

**Status.** No manuscript, code or result files changed. Protected files are unchanged.
