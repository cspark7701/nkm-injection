# Peer Review Revision Tasks & Execution Ledger

**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Based on Reviewer Report:** [`reviewer_report_01.md`](reviewer_report_01.md)  
**Date:** October 13, 2026  
**Status:** Open / In Progress  

---

## 1. Summary of Review Outcome

- **Recommendation:** **Minor Revisions**
- **Core Strengths Recognized:**
  - Robust physical grounding over routine optimizer benchmarking.
  - Discovery and quantification of the low-$\beta$ margin design (16.47 m envelope stay-clear buffer gain).
  - Dimensionless SVD Jacobian formulation resolving condition number ambiguity ($\kappa = 57.78$).
  - High-statistics tail resolution ($N = 550,000$, Clopper–Pearson 95% CI $[2.95 \times 10^{-6}, 2.12 \times 10^{-5}]$).
  - Complete particle tracking validation ($100.00\% \pm 0.00\%$ transmission) and decoupling of static retuning from dynamic shot jitter.

---

## 2. Actionable Revision Task List

### Task R1 — Clarify Vacuum Chamber and Discrete Aperture Modeling [COMPLETED]
- **Status:** Completed 2026-10-13.
- **Location:** Section 2.1 (`paper.tex`).
- **Resolution:** Added details on continuous stainless steel chamber ($r_p \ge 18.25\text{ mm}$), 19.35 mm septum channel clearance, and conservative bounding methodology.

### Task R2 — State Orbit Correction and Centroid Offset Assumptions [COMPLETED]
- **Status:** Completed 2026-10-13.
- **Location:** Section 6.1 (`paper.tex`).
- **Resolution:** Clarified that raw multi-particle tracking evaluated the line without active dipole trajectory steering, demonstrating that the $> 18.5\sigma$ stay-clear headroom provides sufficient passive clearance to accommodate uncorrected centroid orbit deviations under design errors.

### Task R3 — Add Note on Second-Order Dispersion and Chromatic Envelope Growth [COMPLETED]
- **Status:** Completed 2026-10-13.
- **Location:** Section 2.2 (`paper.tex`).
- **Resolution:** Documented that without sextupoles in the 21.789 m line, chromatic broadening remains negligible ($< 2\%$) under design momentum spread ($\sigma_\delta = 0.0008$).

### Task R4 — Frame Multi-Start Optimization Scope [COMPLETED]
- **Status:** Completed 2026-10-13.
- **Location:** Section 3.2 (`paper.tex`).
- **Resolution:** Reframed the 15-start search as a multi-start diagnostic audit exploring local basin attractors.

### Task R5 — Polish Figure Captions & Bibliography Metadata [COMPLETED]
- **Status:** Completed 2026-10-13.
- **Location:** `paper.tex` and `paper.bib`.
- **Resolution:** Audited all captions and verified ISO4 bibliography metadata.

### Task R6 — Recompile and Formulate Author Response to Reviewer [COMPLETED]
- **Status:** Completed 2026-10-13.
- **Location:** `docs/paper_bts/reviews/author_response_to_reviewer_01.md`.
- **Resolution:** Successfully recompiled `paper.pdf` with `pdflatex`, updated `draft_provenance.json`, verified 5/5 asset regression tests, and prepared the complete point-by-point Author Response letter.

