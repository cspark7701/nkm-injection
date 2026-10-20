# Milestone 246 — F9: final reconciliation of the round-4 revision

Completed: 2026-10-20. Round-4 task F9 (R1D-08; final reconciliation of R2d-1–7). It completes the round-4 plan
F1–F9 (milestones 236–246, together with 243 for the two-plane sensitivity and 240 for the NRF acknowledgement).

**Author decisions (2026-10-20):**
- rebuild every figure with matplotlib 3.11.1;
- ignore page growth;
- close error-inclusive point selection and the coupling question as disclosed limitations;
- accept the tuning range as is (boundary fraction kept visible);
- scientific approval of the new claims is reserved by the author and pending.

**Documents** (commit `ce2998d`):
- `reviews/author_response_round4.md`: new. Maps R1D-01–08, R2d-1–7 and Reviewer 2's three questions to evidence
  or to a stated disposition. Earlier responses are unchanged.
- `claim_evidence.csv`: rows F0–F9. F0 records the withdrawal of the round-3 "booster angle jitter" attribution.
- `cover_letter.md`: round-4 results; not sent.
- `round2_reproduction.md`: round-4 section.
- Reviews `README.md`: response link.
- `build_submission_package.py`: the supplement list includes the round-4 manifest, protocol and response; the
  recorded commands use the round-4 manifest.
- `make_round4_manifest.py`: an operating-point identity check (injection position and field scale) for every
  current-point artifact, tested.

**Answer to Reviewer 2's question 2.** It was corrected after checking the BTS optimisation: the septum dispersion
is part of the declared BTS exit target (D, D′ matched to a 4×10⁻¹¹ m residual), not left free.

**Figures.** All eleven are regenerated in one environment, matplotlib 3.11.1 (conda env `pyat-dev`). Only Figs. 1,
2, 4 and 6 were still on 3.8.3. The macros are unchanged by the rebuild.

**Builds** (commit `8215a48`).
- One-column 33 pages, two-column 17 pages, Supplemental Material 7 pages.
- All are clean under the gate (no errors, undefined references, BibTeX warnings, overfull boxes or stuck floats).
- `paper.pdf`, `paper_twocolumn.pdf` and `supplement.pdf` are installed.
- The package manifests record commit `ce2998d`, clean.

**Tests.** Full suite: 757 passed (`OMP_NUM_THREADS=1 python -m pytest -q`). Protected files are unchanged.

**Evidence manifest.** `revision_manifest_round4.json`:
- 250 artifacts: the round-3 manifest, 10 round-4 keys, and 5 builder keys re-pointed to the current point, with the
  S = 0.85 originals as `historical_*`;
- every hash and the point identity are rechecked.

**Round-4 frozen attachment.**
- `results/journal_campaign_05/round4_evidence_bundle.tar.gz`: 20.1 MB, SHA-256
  `dbe3a7a82f138c9709a14950ca45cdd678033a71de03e55b1ca3dde02c9dab67`.
- Built from commit `8215a48` with `uncommitted: false`; 250 artifacts, 258 inventoried files.
- `--verify` rebuilt the macros from the archived source on the bundled evidence alone: byte-identical.
- `sha256sum -c SHA256SUMS` passes for all 258 entries.
- It is git-ignored; no DOI or upload.

**Round-4 outcome in one paragraph.**
- The round-3 attribution of the NKM-specific loss to booster angle jitter is withdrawn.
- A paired ablation without booster jitter traces it to BTS magnet errors. They leave a 0.90 mm rms static vertical
  injection error that the modelled horizontal-only steering does not remove.
- Ideal two-plane steering, a declared sensitivity, restores the NKM to 76.6 % without jitter. Booster position and
  angle jitter then become comparably NKM-specific.
- The paired point test retains the current point. The NKM–dipole gap is point-dependent, because the uniform kick
  loses 17–23 points at the alternatives.
- The pulse and transparency are recomputed at S = 0.95. A 0.2 mm offset now slightly exceeds the 0.1 σ criterion.
