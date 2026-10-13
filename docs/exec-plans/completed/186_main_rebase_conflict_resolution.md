# Milestone 186 — Resolve the main-branch review rebase conflicts

Completed 2026-10-13 at the author's request.

Resolved the in-progress rebase of `main` onto `f078a4f` without skipping either review commit. Combined the archive entries for milestone 164 and milestone 184, preserved the corrected D1–D15 completion and pending third-round scientific-task status in the NKM review index, and retained the BTS review additions. Resolved the following relocation commit by removing only the BTS section from the NKM index while preserving its updated manuscript status.

The replayed commits are `990ddc4` (BTS review) and `59ea8a8` (BTS review relocation). BTS reports and revision tasks remain in `docs/paper_bts/reviews/`; milestones 184 and 185 and their index links remain intact.

Validation: confirmed no unmerged entries or active rebase, verified review and new archive links, compared the NKM review index byte-for-byte with the updated upstream version and BTS review files with the original relocation commit, and verified unchanged protected-file hashes. An existing archive-index link to `../../../05_refactor_tasks/README.md` is broken in the upstream version and was left unchanged. Documentation-only conflict resolution required no simulations. No remote operations were performed.
