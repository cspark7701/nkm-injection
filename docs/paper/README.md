# NKM manuscript — current review and revision status

Updated: 2026-11-01. Target: Physical Review Accelerators and Beams (PRAB).

Both fifth-round reviewers recommend minor revision. The [consolidated round-5 plan](reviews/revision_round_05_plan_for_review_round_05.md) is now the single execution queue: G1–G6 cover model identity, a paired two-plane jitter scan, headline/budget wording, chamber interception, editorial scope and final reconciliation; G7 remains a submission-stage author gate. G1–G6 are complete; the verified evidence attachment and final response are recorded in the round-5 reproduction guide. The [Reviewer 1 report/checklist](reviews/review_round_05_reviewer_01_evidence_report.md) and [Reviewer 2 report/checklist](reviews/review_round_05_reviewer_02_report_and_tasks.md) remain preserved with their original requirements. Execution was authorized after consolidation; milestones 318–327 record the completed audit, wording and implementation checks.

- [One-column article](paper.pdf), [two-column preview](paper_twocolumn.pdf) and [supplement](supplement.pdf): 36, 18 and seven pages.
- [Review history](reviews/README.md) and [the round-5 joint response](reviews/review_round_05_author_response_to_reviewers_01_02.md), alongside all four earlier responses.
- [Completed round-4 plan](reviews/revision_round_04_plan_for_review_round_04.md): F1–F9 executed in milestones 236–246; [response](reviews/review_round_04_author_response_to_reviewers_01_02.md).
- [Current submission checklist](submission_checklist.md), [PRAB layouts](prab_submission.md) and [round-5 reproduction guide](round5_reproduction.md).

The round-4 evidence is selected by `revision_manifest_round4.json`: all 250 artifact keys were locally hash-verified for the fifth-round review. Fresh saved-output analyses reproduce the ablation, steering and point-comparison records exactly; the full figure/macro rebuild reproduces installed macros byte for byte. The existing frozen attachment's 258 inventory entries verify. Twenty-six relevant protocol, packaging and figure tests pass. Those checks describe the review-time round-4 snapshot. Round-5 execution has since added gated G4/G5 builds, 30 targeted test passes and a final 775-test full-suite pass; the new jitter scan is complete.

The earlier attribution chiefly to booster angle jitter is superseded. Paired evidence identifies an uncorrected static vertical injection error under the model's horizontal-only steering; ideal two-plane steering exposes the remaining jitter sensitivity. Capture comparisons remain conditional on the stated model, assumed budget, operating point and finite ring population. The new minor corrections concern the recovery's error-budget label and the physical location of chamber interceptions.

The October-31 Humanizer prose edit is recorded in [milestone 299](../exec-plans/completed/299_nkm_manuscript_humanizer.md). Earlier reports, responses, protocols and frozen campaigns retain their historical dates, numbers and recommendations. Current status here supersedes obsolete pending-F statements in older status snapshots. The [cover letter](cover_letter.md) remains an author-review draft. Final scientific approval and actual referee delivery/submission remain separate; no journal acceptance or external submission has occurred through this workflow.

The consolidated plan adopts Reviewer 2's targeted scan while preserving Reviewer 1's narrower reporting corrections. Its crosswalk records all source tasks and questions; the reviewers' historical recommendations are not rewritten.

Round-5 results: [five-level scan](round5_jitter.md), [272-key manifest](revision_manifest_round5.json), [companion audit](round5_companion_comparison.md) and [source/PDF identities](round5_final_identity.json). No nonzero tested jitter scale passes the declared one-point loss test.
