# Manuscript referee reviews

These are pre-submission assessments, not journal editorial decisions. Review
recommendations and scientific tasks remain distinct from software checks.

| Review | Recommendation | Revision register |
| :--- | :--- | :--- |
| [Reviewer 1](reviewer1_report.md), 2026-10-10 | Major revision; no acceptance in present form | [12 ordered tasks](reviewer1_revision_tasks.md) |
| [Reviewer 2](reviewer2_report.md), 2026-10-10 | Major revision | Included in the report |
| [Reviewer 1, round 2](reviewer1_round2_20261011_report.md), 2026-10-11 | Focused major revision; do not accept the present version | [10 ordered tasks](reviewer1_round2_20261011_revision_tasks.md) |
| [Reviewer 2, round 2](reviewer2_report_round2.md), 2026-10-11 | Major revision; no acceptance in present form | 15 tasks R2b-1 to R2b-15, included in the report |
| [Reviewer 1, round 3](reviewer1_round3_20261012_report.md), 2026-10-12 | Focused major revision | [8 ordered tasks](reviewer1_round3_20261012_revision_tasks.md) |
| [Reviewer 2, round 3](reviewer2_report_round3.md), 2026-10-13 | Major revision focused on robustness; no acceptance in present form | 9 tasks R2c-1 to R2c-9, included in the report |
| [Reviewer 1, round 4](reviewer1_round4_20261016_report.md), 2026-10-16 | Focused major revision; no acceptance in present form | [8 pending R1D tasks](reviewer1_round4_20261016_revision_tasks.md) |
| [Reviewer 2, round 4](reviewer2_report_round4.md), 2026-10-15 | Major revision of limited scope; no acceptance in present form, acceptance expected after R2d-1 to R2d-3 | 7 tasks R2d-1 to R2d-7, included in the report |

Consolidated execution order: [consolidated_revision_plan.md](consolidated_revision_plan.md) (tasks C1–C12).
Round 2: [consolidated_revision_plan_round2.md](consolidated_revision_plan_round2.md) (tasks D1–D15, author inputs A1–A6).
Round 3: [consolidated_revision_plan_round3.md](consolidated_revision_plan_round3.md) (tasks E1–E11, author inputs B1–B5).
Round-3 response: [author_response_round3.md](author_response_round3.md) (E1–E11 complete; milestones 211–222).
Round 4: [consolidated_revision_plan_round4.md](consolidated_revision_plan_round4.md) (tasks F1–F9; split from the round-3 plan on 2026-10-19).
Current queue: [round-4 plan, F1–F9](consolidated_revision_plan_round4.md), all pending; no revision execution authorized by the 2026-10-16 review request.

Reviewer 1 records the manuscript/source hashes and qualifies several proposals
in Reviewer 2: canonical momentum must be distinguished from slope before adding
chromatic scaling; arbitrary reference counts, ring-seed counts and DA reductions
are not acceptance rules; and accessible evidence is required without asserting a
DOI is mandatory. Both reports are retained for an author response.

The second-round Reviewer 2 report reviews the revised manuscript (commit `03b8fe9`) and the
author response. It records the status of every first-round task. Its new major points are:
- the missing vacuum chamber in the headline capture;
- the absence of corrected ring errors;
- manufacturing tolerances of the transparency (checked with the filament model);
- the pulse length;
- beam-based injection tuning;
- lattice identity;
- generality.

Round-2 revision response: [author_response_round2.md](author_response_round2.md).
It maps all R1B and R2b tasks to the final evidence and explicit scope restrictions;
D1–D15 are complete as of 2026-10-12. The author selected PRAB, and
[D15](../../exec-plans/completed/160_prab_manuscript_formats.md) records the
REVTeX 4.2 conversion, clean 28-page one-column and 14-page two-column builds,
and 37 passing relevant tests. See [PRAB submission status](../prab_submission.md).
The first-round response is preserved.

The third-round scientific work was executed through E1–E11 and reconciled in milestone 222.
The earlier report's 48-present/157-missing audit described its review-time checkout;
it is superseded as a current access statement. On 2026-10-16, Reviewer 1 checked all
235 selected round-3 artifact keys locally and found matching hashes. This does not
replace actual evidence delivery or a final archived-source rebuild after new revisions.

The third-round Reviewer 2 report verifies all 205 round-2 artifacts and the evidence-bundle hash
locally, so R1C-01 can be closed by documenting access. Its new points concern the robustness section:
- an operating point not re-selected for the design beam (33 of 50 tuned machines moved toward the septum);
- corrected rings that stop at a 100 µm orbit criterion without optics correction;
- an assumed NKM chamber that encloses the magnet's own conductors.

The fourth-round Reviewer 2 report accepts the round-3 answers and the finite-length core. It finds, from the
campaign-04 per-realization records, that booster jitter costs the NKM and the dipole the same ~20 points, so the
~28-point NKM-specific gap exists at zero jitter and is not "chiefly the booster angle jitter". It asks for a paired
error-class ablation, a paired test of wider-window operating points, and a pulse section recomputed at the selected
point (it still uses the round-2 point).

Reviewer 1's round-4 assessment independently checks the paired zero/full-jitter arithmetic and the mixed pulse
allowances, requests physical loss/domain diagnostics and scoped approximation-error claims, and retains the
completed E tasks. Neither report grants acceptance. The new report and task register preserve all previous reports.
