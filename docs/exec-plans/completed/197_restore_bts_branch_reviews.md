# Milestone 197 — Restore BTS branch review history

## Request and recovery

Recover reviewer reports and revision tasks developed on the local `bts` branch that were absent from `main`. Restore all nine missing review records, including the three corresponding author responses, from commit `466fca5376c76ab1ceb587c801a696b6613a66f4` without replacing existing main-branch reviews or manuscript assets.

## Restored records

- `docs/paper_bts/reviews/historical_branch_review_round_01_author_response_to_reviewer_01.md`
- `docs/paper_bts/reviews/historical_branch_review_round_02_author_response_to_reviewer_02.md`
- `docs/paper_bts/reviews/historical_branch_review_round_03_author_response_to_reviewer_03.md`
- `docs/paper_bts/reviews/historical_branch_review_round_01_report.md`
- `docs/paper_bts/reviews/historical_branch_review_round_02_report.md`
- `docs/paper_bts/reviews/historical_branch_review_round_03_report.md`
- `docs/paper_bts/reviews/historical_branch_revision_round_01_tasks.md`
- `docs/paper_bts/reviews/historical_branch_revision_round_02_tasks.md`
- `docs/paper_bts/reviews/historical_branch_revision_round_03_tasks.md`

## Index and scope

The [BTS review index](../../paper_bts/reviews/README.md) now links all three recovered rounds and distinguishes their historical manuscript scope from the later main-branch review. Original claims, recommendations and task completion labels are preserved as historical records, without asserting actual journal acceptance. References to manuscript sections and generated packages retain their original branch context. No branch merge or rebase was performed.

## Validation

- All nine restored files match their original Git blobs byte for byte.
- New relative Markdown links in the review index and completion archive resolve locally.
- Existing tracked files remain unchanged except the two documentation indexes; the current manuscripts, scientific source inputs and existing review reports are unchanged.
- Git status and diff were checked before and after recovery. This documentation-only restoration requires no simulation rerun.
