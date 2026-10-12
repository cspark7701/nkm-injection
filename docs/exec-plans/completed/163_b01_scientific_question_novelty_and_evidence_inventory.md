# Milestone 163 — Fix scientific question, novelty, and evidence inventory (B01)

Completed: 2026-10-13. User request: Execute the BTS manuscript tasks, track repo status, and git commit after each task.

## 1. Summary of Work Completed

Task B01 of `docs/paper_bts/002_manuscript_tasks.md` was executed to establish the scientific foundation, novelty boundaries, and full evidence audit for the standalone BTS optics paper:

1. **Scientific Question and Overlap Disclosure (`docs/paper_bts/article_scope.md`)**:
   - Formulated the principal question focusing on 4 GeV 9-quadrupole matching under envelope ceilings ($\beta \le 60\text{ m}$) and error sensitivity.
   - Disclosed relationship and shared assets with the companion NKM paper (`docs/paper/`).
   - Stated boundary distinctions: optical mismatch is not transmission; transmission is not storage-ring capture; beta ceilings are optics constraints, not measured apertures.
   - Defined 6 bounded candidate claims (BC01–BC06) and predeclared matching tolerances ($M_{x,y} < 10^{-4}$), envelope limits, prefix stability ($1.0 \times 10^{-5}$), and zero-invalid evaluation criteria.
   - Reconciled historical report inconsistencies ($21.789\text{ m}$ vs legacy $29.8\text{ m}$; constrained $\beta$ peaks $31.44/50.75\text{ m}$ vs older $30.23/44.52\text{ m}$; $100\text{ nm}\cdot\text{rad}$ conservative sensitivity case vs $7.67\text{ nm}\cdot\text{rad}$ design beam).

2. **Literature Survey and Physical Novelty (`docs/paper_bts/literature_comparison.md`)**:
   - Surveyed Korean accelerator studies in JKPS (PLS-II, RAON, KHIMA, K4GSR) and international 4th-generation light source transfer lines (MAX IV, Sirius, ESRF-EBS, TPS).
   - Clarified the paper's physical contributions beyond standard numerical optimizer benchmarking: (1) multi-start feasibility topology showing only 1 in 3 restarts is physically feasible; (2) large-scale ($N = 550,000$) tail failure analysis uncovering that 100% of failures are vertical beta envelope overshoots ($\beta_y > 60\text{ m}$); (3) dimensionless SVD correction knob decomposition; (4) separation of incoming beam jitter from static machine errors.

3. **Complete Evidence Inventory (`docs/paper_bts/evidence_inventory.md`)**:
   - Audited the selected optimization summary (`fe107589...`), config (`382e23dd...`), and candidate table (`398be628...`).
   - Audited all 4 tolerance runs (`seed42`: `62062629...`, `seed123`: `d1f381f7...`, `seed777`: `353c1986...`, `seed2026_400k`: `fa3c0b82...`) and pooled analysis (`5d11a050...`).
   - Documented generating environment: commit `8b62bcd4037031551a1787aabae0bd5dae708046`, Python 3.11.9, NumPy 2.4.6, SciPy 1.17.1, pyAT 0.7.2.dev26.
   - Audited all 5 physical feasibility failures individually with sample IDs, beta peaks, and mismatch values. Verified zero invalid evaluations across all 550,000 runs.
   - Documented prefix stability outcomes: three 50k runs missed $1.0 \times 10^{-5}$ ($\Delta \in [1.06, 2.08] \times 10^{-5}$), 400k run achieved $\Delta = 2.39 \times 10^{-6}$.

4. **Claim Ledger (`docs/paper_bts/claim_evidence.csv`)**:
   - Created a comprehensive CSV ledger mapping 12 specific manuscript claims (BC01–BC12) to exact artifact files, JSON keys, actual numerical values, models, and decision statuses.

5. **Task Tracking (`docs/paper_bts/002_manuscript_tasks.md`)**:
   - Updated B01 status to completed with deliverable links and verified acceptance criteria.

---

## 2. Verification and Acceptance Checks

- All SHA-256 hashes verified on local disk against recorded values.
- All 5 physical failures verified in raw JSON artifacts.
- Zero invalid evaluations confirmed across all 550,000 samples.
- Protected scientific source files verified unmodified (`git status`).
- Next pending task: **B02 — Establish the physical line and observation boundaries**.
