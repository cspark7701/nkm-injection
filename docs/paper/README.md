# NKM manuscript — current review and revision status

Updated: 2026-11-01. Target: Physical Review Accelerators and Beams (PRAB).

Both fifth-round reviewers recommend minor revision. The [consolidated round-5 plan](reviews/revision_round_05_plan_for_review_round_05.md) is now the single execution queue: G1–G6 cover model identity, a paired two-plane jitter scan, headline/budget wording, chamber interception, editorial scope and final reconciliation; G7 remains a submission-stage author gate. All are pending. The [Reviewer 1 report/checklist](reviews/review_round_05_reviewer_01_evidence_report.md) and [Reviewer 2 report/checklist](reviews/review_round_05_reviewer_02_report_and_tasks.md) remain preserved with their original requirements. No manuscript revision or new simulation is executed by consolidation.

- [One-column article](paper.pdf), [two-column preview](paper_twocolumn.pdf) and [supplement](supplement.pdf): 34, 17 and seven pages.
- [Review history](reviews/README.md) and all four preserved joint author responses.
- [Completed round-4 plan](reviews/revision_round_04_plan_for_review_round_04.md): F1–F9 executed in milestones 236–246; [response](reviews/review_round_04_author_response_to_reviewers_01_02.md).
- [Current submission checklist](submission_checklist.md), [PRAB layouts](prab_submission.md) and [reproduction/evidence guide](round2_reproduction.md).

The round-4 evidence is selected by `revision_manifest_round4.json`: all 250 artifact keys were locally hash-verified for the fifth-round review. Fresh saved-output analyses reproduce the ablation, steering and point-comparison records exactly; the full figure/macro rebuild reproduces installed macros byte for byte. The existing frozen attachment's 258 inventory entries verify. Twenty-six relevant protocol, packaging and figure tests pass. No new tracking or TeX compilation was performed by this review.

The earlier attribution chiefly to booster angle jitter is superseded. Paired evidence identifies an uncorrected static vertical injection error under the model's horizontal-only steering; ideal two-plane steering exposes the remaining jitter sensitivity. Capture comparisons remain conditional on the stated model, assumed budget, operating point and finite ring population. The new minor corrections concern the recovery's error-budget label and the physical location of chamber interceptions.

The October-31 Humanizer prose edit is recorded in [milestone 299](../exec-plans/completed/299_nkm_manuscript_humanizer.md). Earlier reports, responses, protocols and frozen campaigns retain their historical dates, numbers and recommendations. Current status here supersedes obsolete pending-F statements in older status snapshots. The [cover letter](cover_letter.md) remains an author-review draft. Final scientific approval and actual referee delivery/submission remain separate; no journal acceptance or external submission has occurred through this workflow.

The consolidated plan adopts Reviewer 2's targeted scan while preserving Reviewer 1's narrower reporting corrections. Its crosswalk records all source tasks and questions; the reviewers' historical recommendations are not rewritten.
