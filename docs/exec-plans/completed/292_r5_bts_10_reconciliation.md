# Milestone 292 — R5-BTS-10: final reconciliation and joint response (round 5)

Completed: 2026-10-31. Round-5 task R5-BTS-10 (Reviewer 1 R1D-BTS-06; Reviewer 2 R2D-12), plus the status-document
part of R5-BTS-08.

**Evidence.**
- **Claims:** BR5-01 to BR5-10 are added, so 73 claims verify (`audit_bts_evidence.py`).
- **Asset hashes:** `revision_selection.json` `final_assets_sha256` covers 83 assets, now including the round-5
  protocol, reproduction guide, generated files and figure. The round-4 set is kept as
  `round4_final_assets_sha256`, with a `round5` block. `--verify` passes.
- **Final build:** `results/bts_round5_final_build`, a 19-page article and 10-page supplement, both clean and
  installed. The changed pages (Tables 5–8, Figures 4–6) were checked visually.
- **Tests:** the full suite gives 771 passed.

**Documents.**
- `round5_reproduction.md`, with commands, measured run times and retained failed runs.
- `reviews/review_round_04_author_response_to_reviewers_01_02.md`, a joint response mapping every R1D-BTS and R2D
  item and answering Reviewer 2's questions.
- Status updates in `docs/paper_bts/README.md`, `reviews/README.md` and `submission_checklist.md`.
- The round-5 plan's checkboxes: 01–08 and 10 ticked, 09 open.

**Referee increment.** `scripts/package_bts_round5_increment.py` reuses the round-4 packager. Its archive keeps the
round-4 file name `bts_referee_round4_increment.tar.gz` inside the round-5 directory. The increment
(`results/bts_referee_attachment_round5_20261031`, git-ignored; not sent or deposited) holds:
- the current sources and PDFs;
- the evidence files;
- the round-3/4/5 code and tests;
- the selected round-4 and round-5 stage outputs;
- the round-4 and round-5 milestones.

Extracted over the round-3 attachment, it verifies all claims with an isolated interpreter. The archive hash is in
its `increment_sha256.txt`.

**Open.** R5-BTS-09 author decisions: journal, data availability, companion access, jitter source and final
approval. Protected files are unchanged.
