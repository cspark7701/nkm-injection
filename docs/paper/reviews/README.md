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

Consolidated execution order: [consolidated_revision_plan.md](consolidated_revision_plan.md) (tasks C1–C12).
Round 2: [consolidated_revision_plan_round2.md](consolidated_revision_plan_round2.md) (tasks D1–D15, author inputs A1–A6).

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

The eight third-round scientific tasks remain pending. The
[third-round audit](../../exec-plans/completed/159_reviewer1_round3_manuscript_report.md)
recorded 48 hash-matching artifacts and 157 absent artifacts out of 205;
D15 did not repeat the historical evidence-bundle verification. Round-2 completion
does not establish submission readiness or scientific acceptance.

The third-round Reviewer 2 report verifies all 205 round-2 artifacts and the evidence-bundle hash
locally, so R1C-01 can be closed by documenting access. Its new points concern the robustness section:
- an operating point not re-selected for the design beam (33 of 50 tuned machines moved toward the septum);
- corrected rings that stop at a 100 µm orbit criterion without optics correction;
- an assumed NKM chamber that encloses the magnet's own conductors.
