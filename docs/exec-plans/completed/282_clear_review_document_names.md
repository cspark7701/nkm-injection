# 282 — Clear manuscript review-document names

Date: 2026-10-31. Renamed 49 review, task, response and consolidated-plan documents
in docs/paper_nkm and docs/paper_bts. Filenames now identify review round, reviewer
and role; consolidated plans identify both the revision cycle and the review
round they answer. Dates remain in the bodies. Restored BTS-branch records have
an explicit historical_branch prefix. The preliminary Task-011 scientific
assessment is named separately rather than given an invented referee round.

Updated repository links, the NKM submission packager's response paths, current
BTS selection paths and current asset digests affected only by link maintenance.
Each review directory has a complete old/new-path map with before/after SHA-256.
No report, task list or response is removed or substantively rewritten; only
filename references in its body are changed. Task IDs, checkboxes, conclusions
and scientific values are preserved. Same-directory renames preserve relative
parent paths. The old round2_identity.json remains byte-identical because it
identifies a frozen reviewed snapshot; its original paths resolve in that
snapshot, with the rename map providing current locations. Frozen results,
source snapshots, archives and earlier-round digest tables are unchanged.

Verification: all 49 renamed documents match their original contents exactly
except filename-reference substitutions; both rename maps and their hashes pass.
No stale live filename references or newly broken relative Markdown links remain.
The historical round-2 identity is byte-identical. The BTS package identity
verification passes, and the evidence audit validates all 63 claims and artifacts.
The 22 targeted submission-package, BTS evidence, evidence-bundle and package-import
tests pass. Staged whitespace checks pass with existing Markdown hard-break
spaces excluded (core.whitespace=-blank-at-eol); those original spaces are
preserved to avoid changing document formatting. No scientific simulation or journal
submission is part of this task. Protected scientific inputs and manuscript
TeX/PDF assets are unchanged.
