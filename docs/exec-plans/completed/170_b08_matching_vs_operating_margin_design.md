# Milestone 170: Matching vs Operating Margin Design Comparison (Task B08)

**Completed:** 2026-10-13  
**Status:** Successfully Executed on branch `bts`.  
**Task Reference:** Task B08 in [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md).

---

## 1. Executive Summary

Milestone 170 provides a rigorous, fair comparison between nominal optics matching and a design explicitly selected for envelope operating margin on the Korea-4GSR BTS transfer line.

Both configurations were evaluated head-to-head on a common held-out error ensemble of 1,000 independent realizations (`seed=98765`). While both designs achieve an identical $100.0\%$ feasibility rate and virtually identical exit mismatch distributions (median $\mathcal{M} \approx 0.0022$), the low-$\beta$ margin design depresses the peak vertical beta function from $50.75\text{ m}$ down to $36.12\text{ m}$ ($28.8\%$ reduction), providing an extra $16.5\text{ m}$ of stay-clear buffer against worst-case envelope flare under random errors at a modest quadrupole gradient cost ($G_{\max} = 40.02\text{ T/m}$, pole-tip $B_{\text{pole}} = 0.774\text{ T} \ll 1.2\text{ T}$).

---

## 2. Key Accomplishments & Deliverables

1. **Operating Margin Comparison Report (`docs/paper_bts/margin_design_comparison.md`)**:
   - Comprehensive performance table contrasting the unoptimized baseline, nominal matched design, and low-$\beta$ margin design across 12 statistical observables.
   - Head-to-head evaluation on 1,000 held-out error realizations demonstrating $100.0\%$ feasibility for both matched designs and quantifying the $16.47\text{ m}$ envelope margin gain.
   - Engineering trade-off analysis confirming that the margin design's peak pole-tip field ($0.774\text{ T}$) retains $35.5\%$ safety margin below the $1.2\text{ T}$ iron pole saturation limit.

2. **Publication Visual Assets**:
   - High-resolution publication figure [`docs/paper_bts/figures/fig3_margin_tradeoff.png`](../../paper_bts/figures/fig3_margin_tradeoff.png) (300 DPI).
   - Publication vector PDF [`docs/paper_bts/figures/fig3_margin_tradeoff.pdf`](../../paper_bts/figures/fig3_margin_tradeoff.pdf).
   - Visual comparison of betatron functions $\beta_{x,y}(s)$ and horizontal dispersion $D_x(s)$ along the line.

---

## 3. Verification and Standards Compliance

- **Protected Files Integrity:** All protected scientific data files remain untouched.
- **Git Branch:** Executed directly on branch `bts`.
- **Unit Tests:** All 16 unit and integration tests passed cleanly.
