# Revision Tasks Ledger — Round 2 (JKPS Manuscript)

**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Based on:** [`reviewer_report_02.md`](reviewer_report_02.md)  
**Date:** October 13, 2026  
**Status:** Completed / Verified  

---

## 1. Summary of Round 2 Review

- **Recommendation:** **Accept with Minor Editorial & Clarification Adjustments**
- **Evaluation:** Scientific depth, methodology, and numerical precision are verified to be sound. Round 2 tasks focus on quantitative substantiation of engineering claims (power dissipation, null space physical basis, particle loss plane, and commissioning recommendations).

---

## 2. Round 2 Actionable Tasks

### Task R2-1 — Quantify Integrated Gradient & Power Dissipation Reduction [COMPLETED]
- **Location:** Section 4.1 (`paper.tex`).
- **Goal:** Quote the numerical reduction in integrated gradient squared $\sum K_i^2$ ($19.78\ \text{m}^{-4}$ for nominal matched vs. $16.14\ \text{m}^{-4}$ for low-$\beta$ margin design, an 18.4% reduction) to substantiate lower power dissipation.
- **Deliverables:** Updated text in `docs/paper_bts/paper.tex`.

### Task R2-2 — Detail Physical Composition of Null-Space Modes [COMPLETED]
- **Location:** Section 4.2 (`paper.tex`).
- **Goal:** Detail how the 3-mode null space physically operates through internal triplet-2 focusing adjustments coupled with balanced counter-trims between triplets 1 and 3.
- **Deliverables:** Updated text in `docs/paper_bts/paper.tex`.

### Task R2-3 — Specify Loss Plane at 6× Jitter Breakdown Threshold [COMPLETED]
- **Location:** Section 6.2 (`paper.tex`).
- **Goal:** Clarify that initial particle scraping at $6\times$ jitter occurs primarily in the horizontal plane due to combined betatron oscillation, dispersion excursion, and orbit steering.
- **Deliverables:** Updated text in `docs/paper_bts/paper.tex`.

### Task R2-4 — Strengthen Commissioning & Hardware Procurement Discussion [COMPLETED]
- **Location:** Section 7 (`paper.tex`).
- **Goal:** Note in Section 7 that standard magnet machining tolerances ($\Delta K/K \le 10^{-3}$) are readily achieved, and that prioritizing multi-screen profile monitors at the booster interface provides greater operational gain than over-specifying magnet tolerances.
- **Deliverables:** Updated text in `docs/paper_bts/paper.tex`.

### Task R2-5 — Polish Caption 5 & Bounding Box Annotation [COMPLETED]
- **Location:** Section 6.1, Figure 5 caption (`paper.tex`).
- **Goal:** Explicitly clarify in Figure 5 caption that the dashed bounding box indicates the $19.35 \times 19.35$ mm aperture limit.
- **Deliverables:** Updated caption in `docs/paper_bts/paper.tex`.

### Task R2-6 — Recompilation, Provenance Update, and Author Response Document [COMPLETED]
- **Location:** `paper.pdf`, `draft_provenance.json`, and `docs/paper_bts/reviews/author_response_to_reviewer_02.md`.
- **Goal:** Recompile PDF cleanly, update cryptographic hashes, verify tests, rebuild submission bundle, and prepare point-by-point response letter.
- **Deliverables:** `author_response_to_reviewer_02.md`, recompiled `paper.pdf`, updated `draft_provenance.json`.
