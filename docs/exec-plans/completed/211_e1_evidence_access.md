# Milestone 211 — E1: Evidence access and re-verification

Completed: 2026-10-13. Round-3 task E1 (R1C-01).

**Work.** The round-2 frozen attachment was re-verified from scratch rather than relying on the D13 record:
- **Archive.** `results/journal_campaign_03/round2_evidence_bundle.tar.gz` has SHA-256 `0e07de5f…3f3d`, equal to the
  D13 record.
- **Inventory.** All 213 `SHA256SUMS` entries verify after unpacking.
- **Isolated rebuild.** The archived source (commit `9028978`, unpacked from `code.tar.gz`) was run on the bundled
  evidence only, in a scratch directory. It reproduces `journal_macros.tex` byte-identically to the archived macros
  and to the macros installed at `cdc71bf`.
- **Manifest.** All 205 artifacts of `revision_manifest_round2.json` are present in the checkout and match their
  hashes.

**Documentation.** `docs/paper/round2_reproduction.md` gains a section with the referee entry point, the commands
used, the outcomes and the environment (Python 3.11.9, pyAT 0.7.2.dev26, NumPy 2.4.6, SciPy 1.17.1,
Matplotlib 3.11.1).

**Scope.** Nothing was regenerated in campaign 03. The scratch rebuild is outside the repository. No manuscript,
code or results changed.
