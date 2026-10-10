# Milestone 137 — Reviewer 1 second-round manuscript report

Date: 2026-10-11

## Request and outcome

Re-reviewed the revised manuscript in `docs/paper/` and wrote a new referee-style report and ordered revision register without overwriting previous reviews. Recommended focused major revision: the revised three-dimensional model and scientific mechanism are stronger, but trajectory validation, survival reporting, jitter inference, correction definitions and pulse/claim scope still need work.

- [New Reviewer 1 report](../../paper/reviews/reviewer1_round2_20261011_report.md)
- [Ten ordered second-round tasks](../../paper/reviews/reviewer1_round2_20261011_revision_tasks.md)

## Evidence and verification

Read project instructions and README, current LaTeX/PDF, earlier reviews/response and selected field, tracking and evidence-generation implementations. Visually inspected the current control/transparency and robustness figure pages. Verified all 46 selected revision artifacts against their manifest hashes.

Reanalyzed the existing 50 paired corrected quarter/zero-jitter realizations: quarter minus zero is +0.30 percentage points with percentile 95% bootstrap interval −1.50 to +2.15 (10,000 resamples, seed 1729). Verified the survival paragraph mistakenly uses the percentage macro as a turn count, while the actual duration is 4000 turns. Checked peak-phase half-sine timing and first-return estimates analytically.

This task created review documents only. No simulation, code change, manuscript rebuild, or numerical test run was performed. The report distinguishes local evidence consistency from independent numerical reproduction. Proposed revision tasks remain unexecuted.

## Preservation

Previous manuscript/review files were snapshotted before writes. During the review, an independent commit (`0eaaa5e`) added Reviewer 2 round two and updated the reviews index; that concurrent update was preserved. All other previously snapshotted manuscript/review files remained byte-for-byte unchanged, and tracked manuscript/review files match the final HEAD. Milestone 137 follows that commit’s milestone 136. Protected files were checked against HEAD. Working-tree status and changed-path checks were performed before and after; final documentation validation checked local links, ordered task IDs and whitespace. The completed-task index was updated for milestone 137.
