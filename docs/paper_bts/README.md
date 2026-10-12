# BTS optics manuscript

Planning draft, 2026-10-13. Proposed target: **Journal of the Korean Physical Society (JKPS), Research Article**.

- [Manuscript outline and campaign evidence](001_manuscript_outline.md)
- [Ordered preparation tasks and acceptance criteria](002_manuscript_tasks.md)

The proposed paper asks how nine quadrupoles can match the booster-to-storage-ring transfer line while preserving beam-envelope margin and tolerating specified errors. The existing deterministic and optics-tolerance campaigns provide starting evidence. Correction-knob analysis, physical transport validation and an independent design comparison are proposed new work.

The NKM manuscript remains in [docs/paper/](../paper/). Its finite-length kicker, storage-ring capture and stored-beam transparency results are outside this paper's main scope. This directory currently contains an outline and execution plan, not a submission-ready article or a completed new simulation campaign.

Use SI units internally: position and beta in m, angle in rad, energy in eV, quadrupole strength in m^-2, gradient in T/m; alpha, relative momentum offset and dispersion derivative are dimensionless. Save future numerical outputs under new `results/bts_journal_campaign_*` directories and select them through a separate BTS evidence manifest. Keep ignored raw outputs out of git.
