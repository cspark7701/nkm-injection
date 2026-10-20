# Milestone 247 — BTS paper: companion update, final availability wording and referee attachment

Completed: 2026-10-20. Author instructions:
- cite the round-4 companion result with the vertical injection error removed, and say that it will be addressed in
  a future study;
- finalize the data-availability wording;
- prepare the referee attachment.

Scientific approval is reserved by the author.

**Manuscript** (`docs/paper_bts/paper.tex`, commit `3b05020`).
- **Companion sentence.** The withdrawn "booster angle jitter is the only significant driver" claim is replaced. The
  text now says that once the static vertical injection error left by transfer-line magnet errors is removed, booster
  position and angle jitter are the dominant kicker-specific capture losses. It adds that this line has no vertical
  correction, and that correcting that error will be addressed in a future study.
- **Data and code availability (final).** Code, configurations and scripts are in the public repository. Selected raw
  data, generating-source snapshots, environment identities, hashes and reproduction commands are provided to the
  referees as a supplementary attachment, and are available on reasonable request. No public deposit.
- **Build.** Rebuilt clean under the packager's gate, 12 pages. `revision_selection.json` final hashes refreshed;
  `package_bts_revision.py --verify` passes.
- **Records updated.** README, declarations, R2-BTS-08 status, submission checklist, reproduction note, reviews
  index. The attachment's REPRODUCE text no longer lists delivery as pending.

**Referee attachment.**
- `results/bts_referee_attachment_20261020/bts_referee_attachment.tar.gz`: 100.7 MB, SHA-256
  `92b1fb21851b3a52b0e13f0183fdedce7ce54399bce70a7bdc92359071dddd37`.
- Packaging commit `3b05020`. Inventory: 826 files, all matching `SHA256.json`.
- Running `audit_bts_evidence.py` inside the extracted attachment, with `-I` and its own `src`, verifies every claim
  (BC01–17, BRC01–15, BPS01–04, BR3-01–13) on the bundled data alone.
- It is git-ignored. It has not been sent or deposited; the author uploads it with the submission.

**Tests.** `test_bts_round3`, `test_bts_evidence_audit` and `test_package_imports` pass (23). Protected files are
unchanged.

**Remaining author action.** Final scientific approval of the BTS article. R2-BTS-08 closes with it.
