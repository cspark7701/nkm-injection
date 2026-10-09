# Milestone 110 — Journal Task 007: role of Pareto optimisation (S8 not run)

Completed: 2026-10-09. Task: [007](../../jinst-paper/tasks/007_design_comparison_and_moga_evidence.md).

Decision recorded in [`moga_decision.md`](../../jinst-paper/moga_decision.md): MOGA is omitted from the main-text claims
and the S8 campaign is not run. Reasons, traced to code and the selected run: the objectives are BTS-optics quantities
that do not address the capture/transparency question; f₃ adds metres and dimensionless dispersion in quadrature;
finalist re-evaluation used the uncalibrated `ideal` kicker for 10 turns; seed 42 reached only 20 % feasibility. The
deterministic matched optics already reach zero mismatch inside the β limit and are the single design used by S4–S7;
the S7 results show the injection window is limited by injected-orbit jitter, not by BTS optics quality. No code or
simulation changed.
