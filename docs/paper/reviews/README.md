# Manuscript referee reviews

Current round-5 execution register (consolidated 2026-11-01): [G1–G7](revision_round_05_plan_for_review_round_05.md). It answers [Reviewer 1](review_round_05_reviewer_01_evidence_report.md) and [Reviewer 2](review_round_05_reviewer_02_report_and_tasks.md), both recommending minor revision. G1–G6 combine the paired jitter scan, companion identity, headline/budget wording, chamber interception, point labels and final reconciliation. G7 is deferred to submission readiness. G1, G4 and G5 are complete; G2 tracking and G3/G6 reconciliation are in progress following execution authorization. Both source reports/checklists remain unchanged. The plan explicitly records their different views on the need for a scan and adopts Reviewer 2's request.

## Review document filenames

Filenames now state the round, reviewer and document role, with two-digit numbers:

- `review_round_04_reviewer_01_report.md`: Reviewer 1's round-4 report.
- `review_round_04_reviewer_01_tasks.md`: the corresponding reviewer task list.
- `review_round_03_author_response_to_reviewers_01_02.md`: response to the round-3 reviews.
- `revision_round_04_plan_for_review_round_04.md`: the round-4 revision plan answering round-4 reviews.

**Review round** is the review being written or answered; **revision round** identifies the implementation cycle.
They can differ. Dates, task IDs, decisions and author statements remain in the documents. A
`report_and_tasks` suffix means the original report contains its own task register; it was not split or discarded.
The [rename map](document_rename_map.json) records every old/new path and before/after digest. Old snapshot paths
and hashes identify the original Git/attachment contents; they are not rewritten to pretend those bytes are new.

The earlier Task-011 assessment is [pre_submission_assessment_2026_10_09.md](../pre_submission_assessment_2026_10_09.md);
it is a preliminary scientific assessment, rather than a numbered referee round.


These are pre-submission assessments, not journal editorial decisions. Review
recommendations and scientific tasks remain distinct from software checks.

| Review | Recommendation | Revision register |
| :--- | :--- | :--- |
| [Reviewer 1](review_round_01_reviewer_01_report.md), 2026-10-10 | Major revision; no acceptance in present form | [12 ordered tasks](review_round_01_reviewer_01_tasks.md) |
| [Reviewer 2](review_round_01_reviewer_02_report_and_tasks.md), 2026-10-10 | Major revision | Included in the report |
| [Reviewer 1, round 2](review_round_02_reviewer_01_report.md), 2026-10-11 | Focused major revision; do not accept the present version | [10 ordered tasks](review_round_02_reviewer_01_tasks.md) |
| [Reviewer 2, round 2](review_round_02_reviewer_02_report_and_tasks.md), 2026-10-11 | Major revision; no acceptance in present form | 15 tasks R2b-1 to R2b-15, included in the report |
| [Reviewer 1, round 3](review_round_03_reviewer_01_report.md), 2026-10-12 | Focused major revision | [8 ordered tasks](review_round_03_reviewer_01_tasks.md) |
| [Reviewer 2, round 3](review_round_03_reviewer_02_report_and_tasks.md), 2026-10-13 | Major revision focused on robustness; no acceptance in present form | 9 tasks R2c-1 to R2c-9, included in the report |
| [Reviewer 1, round 4](review_round_04_reviewer_01_report.md), 2026-10-16 | Focused major revision; no acceptance in present form | [8 R1D tasks](review_round_04_reviewer_01_tasks.md), addressed in the round-4 response |
| [Reviewer 2, round 4](review_round_04_reviewer_02_report_and_tasks.md), 2026-10-15 | Major revision of limited scope; no acceptance in present form, acceptance expected after R2d-1 to R2d-3 | 7 tasks R2d-1 to R2d-7, included in the report |
| [Reviewer 1, round 5 evidence assessment](review_round_05_reviewer_01_evidence_report.md), 2026-11-01 | Minor revision; scientific content acceptable after bounded reporting corrections | [Three open R1E tasks](review_round_05_reviewer_01_evidence_tasks.md) |
| [Reviewer 2, round 5](review_round_05_reviewer_02_report_and_tasks.md), 2026-11-01 | Minor revision; acceptable in principle after R2e-1 to R2e-3 (headline under both steering assumptions, two-plane jitter scan, companion consistency) | 9 tasks R2e-1 to R2e-9, included in the report |

Consolidated execution order: [revision_round_01_plan_for_review_round_01.md](revision_round_01_plan_for_review_round_01.md) (tasks C1–C12).
Round 2: [revision_round_02_plan_for_review_round_02.md](revision_round_02_plan_for_review_round_02.md) (tasks D1–D15, author inputs A1–A6).
Round 3: [revision_round_03_plan_for_review_round_03.md](revision_round_03_plan_for_review_round_03.md) (tasks E1–E11, author inputs B1–B5).
Round-3 response: [review_round_03_author_response_to_reviewers_01_02.md](review_round_03_author_response_to_reviewers_01_02.md) (E1–E11 complete; milestones 211–222).
Round 4: [revision_round_04_plan_for_review_round_04.md](revision_round_04_plan_for_review_round_04.md) (tasks F1–F9; split from the round-3 plan on 2026-10-19).
Round-4 response: [review_round_04_author_response_to_reviewers_01_02.md](review_round_04_author_response_to_reviewers_01_02.md) (F1–F9 complete; milestones 236–246; author's scientific approval pending).

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

Round-2 revision response: [review_round_02_author_response_to_reviewers_01_02.md](review_round_02_author_response_to_reviewers_01_02.md).
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

## Consolidated round-5 plan

[The seven-package register](revision_round_05_plan_for_review_round_05.md) is the single execution queue and includes a complete crosswalk for R1E-01–03, R2e-1–9 and Reviewer 2's three questions. It keeps the one-point jitter-loss test separate from the NKM–dipole gap, preserves paired versus pooled population labels, and retains the chamber-interception correction. Older descriptions of separate queues record the state before consolidation. F1–F9 remain completed history.

Round-5 execution response: [joint response to Reviewers 1 and 2](review_round_05_author_response_to_reviewers_01_02.md). G1–G6 are complete; original reviewer-time checklists remain unchanged and G7 is deferred.
