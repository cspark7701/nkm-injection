# Milestone 180 — Execution of All Peer Review Revision Tasks and Package Verification

Completed: 2026-10-13. User request: Execute the revision tasks.

## 1. Summary of Work Completed

All actionable revision tasks specified in the peer review report ([`docs/paper_bts/reviews/reviewer_report_01.md`](../../paper_bts/reviews/reviewer_report_01.md)) and ledger ([`docs/paper_bts/reviews/revision_tasks.md`](../../paper_bts/reviews/revision_tasks.md)) were systematically executed and verified:

1. **Task R1 (Aperture & Chamber Model):**
   - Added description in Section 2.1 of `docs/paper_bts/paper.tex` establishing that the 21.789 m line connects booster extraction to ring injection via a continuous stainless steel chamber ($r_p \ge 18.25\text{ mm}$), and defined the 19.35 mm boundary apertures as conservative clearances within the extraction/injection septum vacuum channels.

2. **Task R2 (Orbit Correction Clarification):**
   - Documented in Section 6.1 that raw multi-particle tracking evaluated the lattice without active dipole trajectory steering, proving that the $> 18.5\sigma$ physical aperture clearance passively absorbs uncorrected centroid orbit deviations induced by $100\ \mu\text{m}$ quadrupole offsets under design errors.

3. **Task R3 (Higher-Order Dispersion & Chromaticity):**
   - Added confirmation in Section 2.2 that without chromatic correction sextupoles in the 21.789 m line, second-order dispersion and chromatic envelope broadening remain negligible ($< 2\%$) under design momentum spread ($\sigma_\delta = 0.0008$).

4. **Task R4 (Framing of Multi-Start Sample Size):**
   - Reframed the 15-start multi-start study in Section 3.2 as an illustrative diagnostic audit of local basin attractors.

5. **Task R5 (Figure & Reference Polishing):**
   - Updated Figure 1 caption to explicitly label bending dipoles B1–B3, the three matching triplets ($\mathrm{q11}$–$\mathrm{q13}$, $\mathrm{q21}$–$\mathrm{q23}$, $\mathrm{q31}$–$\mathrm{q33}$), and individual line styles ($\beta_x$ solid blue, $\beta_y$ dashed red, $D_x$ dash-dotted green).
   - Added the Courant–Snyder 1958 foundational reference (`Courant1958`) in `paper.bib` and cited it in the definition of the mismatch parameter $\mathcal{M}_u$ (Eq.~3).

6. **Task R6 (Compilation, Bundle Packaging & Author Response):**
   - Successfully recompiled [`docs/paper_bts/paper.pdf`](../../paper_bts/paper.pdf) (12 pages, 612 KB, zero warnings/errors).
   - Updated cryptographic SHA-256 digests in [`docs/paper_bts/draft_provenance.json`](../../paper_bts/draft_provenance.json).
   - Rebuilt and verified the standalone submission bundle (`results/bts_submission/bts_jkps_submission.tar.gz`).
   - Finalized point-by-point author response in [`docs/paper_bts/reviews/author_response_to_reviewer_01.md`](../../paper_bts/reviews/author_response_to_reviewer_01.md).

---

## 2. Deliverables Produced

- [`docs/paper_bts/paper.tex`](../../paper_bts/paper.tex)
- [`docs/paper_bts/paper.bib`](../../paper_bts/paper.bib)
- [`docs/paper_bts/paper.pdf`](../../paper_bts/paper.pdf)
- [`docs/paper_bts/draft_provenance.json`](../../paper_bts/draft_provenance.json)
- [`docs/paper_bts/reviews/author_response_to_reviewer_01.md`](../../paper_bts/reviews/author_response_to_reviewer_01.md)
- [`docs/paper_bts/reviews/revision_tasks.md`](../../paper_bts/reviews/revision_tasks.md)

---

## 3. Verification and Acceptance Checks

- All 5 publication asset regression tests pass (`pytest tests/test_bts_paper_assets.py` in 0.02s).
- Standalone reproduction check passes with 100% SHA-256 match (`python scripts/reproduce_bts_paper.py --verify`).
- Isolated submission bundle extraction and PDF build succeed cleanly.
- Protected scientific source files remain unmodified (`git status`).
