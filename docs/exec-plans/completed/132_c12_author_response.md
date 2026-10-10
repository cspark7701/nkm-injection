# Milestone 132 — C12: Point-by-point response and final gate

Completed: 2026-10-11. Consolidated task C12 (closing the consolidated reviewer revision C1–C12).

**Response.** `docs/paper/reviews/author_response.md` (commit d83904a) answers both reports. It covers:
- Reviewer 1, M1–M8, and the presentation table;
- Reviewer 2, M1–M8, minor comments m1–m14 and questions 1–4;
- the acceptance checklist.

Each entry gives the action, results, location in the revised manuscript and evidence (artifact and milestone).

Final edits:
- **M4 (both reviewers) rewritten.** It now reports the two treatments of the static transfer-line errors:
  - no correction: 40.5 % mean;
  - ideal static correction: 44.4 % mean;
  - dipole control: 61.4 / 65.6 %;
  - the jitter curves for both, the drivers by partial rank correlation and the conditions for 80 % capture.
  It no longer claims a single jitter requirement: no jitter reduction alone reaches a mean of 80 %.
- **M6.** The table now separates the kick-spread growth from the total emittance ratio after filamentation (1 + A²/2
  + Δε/ε). It adds the 1000-turn tracked check: 0.10 / 1.47 σ and emittance ratios 1.01 / 2.23 at 0.2 / 0.5 mm.
- **Numbering.** Section and figure numbers follow the compiled manuscript:
  - robustness §7, error budget §7.1, pulsed magnet §8, discussion §9;
  - DA figure 1, NKM geometry figure 2, mechanism figure 3.
- **Corrections.** The position-scan step unit is fixed (0.20 mm). All `{{…}}` placeholders are filled.

**Final gate.**

| Check | Result |
| :--- | :--- |
| Revision manifest | 46 artifacts, none missing (`--require-all`) |
| Isolated manuscript build | 13 pages; no errors, undefined references/citations, BibTeX warnings or overfull boxes |
| Figures | all eight inspected; legends clear of data |
| Full test suite | 663 passed (`OMP_NUM_THREADS=1 python -m pytest -q`) |
| Evidence bundle at d83904a | `results/journal_campaign_02/evidence_bundle_rev2`; `uncommitted: false`; rebuild macros byte-identical; SHA256SUMS verified |
| Protected files | unchanged |

**Commits of the revision campaign:** C1–C4 (… d3e1e7a); C5 5b878a3, 5b7e63e; C7 9c7b9ed; C6 d0a819c; C10 f44d9f0;
C11 3b98ea0, 95edc17; C12 d83904a and this milestone. Nothing was pushed.

**Open author actions** (also in `submission_checklist.md`):
- choose the journal and adapt the class, bibliography style and cover letter;
- create a persistent archive (DOI);
- confirm the AI-assistance disclosure, funding statement and referee suggestions;
- review and sign the response and the cover letter.
