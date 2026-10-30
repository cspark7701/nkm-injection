# Milestone 278 — R4-BTS-09: reconciliation, joint response and referee increment

Completed: 2026-10-31. Round-4 task R4-BTS-09 (Reviewer 1 R3-BTS-08; Reviewer 2 R2C-10).

**Evidence.**
- **Claim ledger.** 14 new claims, BR4-01 to BR4-14, with artifact identities in `claim_evidence.csv` and
  `evidence_manifest.json`. `audit_bts_evidence.py` verifies all 63 claims.
- **Asset hashes.** The `revision_selection.json` field `final_assets_sha256` now covers 75 assets, including the
  round-4 protocol, reproduction guide, generated files and figures. The round-3 values are kept in
  `round3_final_assets_sha256`, and a `round4` block points to the reviews, tasks, response, campaign and build.
  `package_bts_revision.py --verify` passes.
- **Float order.** The layout table now follows the steering table, and the scan figure follows the jitter-transfer
  figure. Final numbering: Tables 1–9 (Table 5 steering layouts, Table 7 second test, Table 9 jitter sweep) and
  Figures 1–6 (Figure 5 phase scan, Figure 6 blade distance). The claim locations follow this numbering. Earlier
  round-4 milestones cite the numbering current when they were written.
- **Accuracy fix.** The article now says that the dispersion-free lower edge of 187.2° comes from searches stopped at
  their iteration limit; the converged search ends at 187.6° on the vertical 60 m limit.

**Article.** Built clean in `results/bts_round4_final_build` (19 pages, with a 9-page supplement) and installed as
`paper.pdf` and `supplement.pdf`.

**Documents.**
- `round4_reproduction.md`, with stage commands, measured run times and retained runs.
- `reviews/author_response_round4_20261031.md`, a joint point-by-point response mapping every R3-BTS and R2C item.
  It records the changes made after the earlier Reviewer 2 response and answers Reviewer 2's questions 1–5.
- Updates to `docs/paper_bts/README.md` and `reviews/README.md`.

**Referee increment.** `scripts/package_bts_round4_increment.py` packages, into
`results/bts_referee_attachment_round4_20261031` (git-ignored; not sent or deposited):
- the current sources and PDFs;
- the evidence files;
- the round-3/4 code and tests;
- the selected round-4 stage outputs;
- the R4-BTS-03 comparison.

The script then extracts the round-3 attachment and the increment into a new directory and runs the audit there with
an isolated interpreter. The archive hash is in `increment_sha256.txt`.

**Tests.** The full suite gave 767 passed and 1 failed: `test_package_imports` flagged a `sys.path` insertion in
the round-4 exporter. That insertion was removed, and the re-exported assets are byte-identical. The final full suite gives
768 passed.

**Open author decisions:** the target journal, data-availability wording, a booster-jitter source and final
approval. Protected files are unchanged.
