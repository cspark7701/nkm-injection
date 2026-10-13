# Revision Tasks Ledger — Round 3 (Camera-Ready Polish)

**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Based on:** [`reviewer_report_03.md`](reviewer_report_03.md)  
**Date:** October 13, 2026  
**Status:** Completed / Verified  

---

## 1. Summary of Round 3 Review

- **Recommendation:** **Accept for Publication (Camera-Ready Polish)**
- **Evaluation:** The paper has met all physics, engineering, and statistical requirements for publication. Minor items focus on eliminating a 30.97 pt overfull `\hbox` in Section 2.1 and adding a formal citation for PLS-II in the Introduction.

---

## 2. Round 3 Actionable Tasks

### Task R3-1 — Eliminate Overfull `\hbox` in Section 2.1 [COMPLETED]
- **Location:** Section 2.1 (`paper.tex`, line 50).
- **Goal:** Rephrase or break the coordinate vector $(x, p_x, y, p_y, \delta, ct)$ so that it fits within column margins without triggering an overfull `\hbox` (30.97 pt overflow in `paper.log`).
- **Deliverables:** Updated paragraph in `docs/paper_bts/paper.tex`.

### Task R3-2 — Add Formal Citation for PLS-II in Introduction [COMPLETED]
- **Location:** Section 1 (`paper.tex`) and `paper.bib`.
- **Goal:** Add a formal citation for the Pohang Light Source II (PLS-II) design and performance (e.g. Choi et al., 2014 or Kim et al., 2013) to ensure all named domestic light sources are referenced.
- **Deliverables:** New bib entry in `paper.bib`, citation in `paper.tex`.

### Task R3-3 — Recompile, Provenance Verification, and Author Response Document [COMPLETED]
- **Location:** `paper.pdf`, `draft_provenance.json`, `docs/paper_bts/reviews/author_response_to_reviewer_03.md`.
- **Goal:** Recompile PDF cleanly, ensure zero overfull box warnings on text, update SHA-256 digests in `draft_provenance.json`, rebuild submission bundle, pass regression tests, and prepare author response.
- **Deliverables:** Updated `paper.pdf`, `draft_provenance.json`, `bts_jkps_submission.tar.gz`, and `author_response_to_reviewer_03.md`.
