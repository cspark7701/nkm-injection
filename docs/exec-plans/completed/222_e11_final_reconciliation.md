# Milestone 222 — E11: Final reconciliation of the round-3 revision

Completed: 2026-10-15. Round-3 task E11 (R1C-08). Completes the round-3 plan E1–E11 (milestones 211–222).

**Documents** (commit `90dc8d3`):
- `reviews/author_response_round3.md`: new; maps R1C-01–08 and R2c-1–9 to evidence or to an explicitly narrowed
  claim. Earlier responses are unchanged.
- `claim_evidence.csv`: rows E0–E11.
- `cover_letter.md`: round-3 results.
- `round2_reproduction.md`: round-3 section.
- Reviews `README.md`: response link.
- `build_submission_package.py`: the supplement list includes the round-3 manifest and response; recorded commands
  use the round-3 manifest.

**Builds.**
- One-column: 30 pages. Two-column: 15 pages. Supplemental Material: 6 pages.
- All are clean under the gate (no errors, undefined references, BibTeX warnings, overfull boxes or stuck floats).
- `paper.pdf`, `paper_twocolumn.pdf` and `supplement.pdf` are installed.

**Tests.** Full suite: 730 passed (`OMP_NUM_THREADS=1 python -m pytest -q`). Protected files are unchanged.

**Evidence manifest.** `revision_manifest_round3.json`:
- 235 artifacts recorded;
- all 37 round-2 builder keys re-pointed to campaign-04 runs, with none missing (`--require-all` satisfied).

**Round-3 frozen attachment.**
- `results/journal_campaign_04/round3_evidence_bundle.tar.gz`: 20.0 MB, SHA-256
  `e65a86c0f4014cb12ed5ede5753ea62c4ba54139c01557ef41e4108047b76fc7`.
- Built from commit `90dc8d3` with `uncommitted: false`; 235 artifacts, 243 inventoried files.
- `--verify` rebuilt the macros from the archived source on the bundled evidence alone: byte-identical.
- `sha256sum -c SHA256SUMS` passes for all 243 entries.
- It is git-ignored; no DOI or upload.

**Round-3 outcome in one paragraph.** The finite-length result is strengthened: the thin-map error scales as
η^1.46 and exceeds a tenth of the angular window at the selected point. The robustness section is rebuilt on
corrected rings, a feasible NKM chamber and a re-selected operating point. Nominal capture is 98.4 %, the
corrected-ring mean 78.0 % and the joint-error mean 16.1 % (dipole 44.1 %). The synthesis attributes the NKM-specific
loss to injection angle errors on a 0.44 mrad window. Two of Reviewer 2's round-3 expectations were not borne out:
the gain did not come from the septum position, and capture is not organised by the DA margin. The manuscript reports
the evidence as found.
