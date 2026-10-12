# Milestone 171: Qualification of Tolerance Distributions and Engineering Requirements (Task B09)

**Completed:** 2026-10-13  
**Status:** Successfully Executed on branch `bts`.  
**Task Reference:** Task B09 in [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md).

---

## 1. Executive Summary

Milestone 171 qualifies the statistical tolerance distributions, prefix convergence rates, exact rare-event failure intervals, and practical engineering requirements across the 550,000-sample BTS transfer line simulation dataset.

The audit verified zero invalid evaluations ($N_{\text{invalid}} = 0$) and confirmed pooled median mismatches of $\mathcal{M}_x = 0.002084$ (bootstrap $95\%$ CI: $[0.002069, 0.002097]$) and $\mathcal{M}_y = 0.002496$. Across all 550,000 observations, exactly 5 physical feasibility failures occurred (all caused by $\beta_{y,\max} > 60\text{ m}$ under 4-sigma tail combinations). The exact Clopper-Pearson $95\%$ binomial confidence interval for the failure rate is $[2.952 \times 10^{-6}, 2.122 \times 10^{-5}]$ ($0.909$ failures per $100,000$). The report explicitly clarifies that these mathematical constraint violations do not constitute beam loss on physical vacuum walls.

---

## 2. Key Accomplishments & Deliverables

1. **Tolerance Qualification Report (`docs/paper_bts/tolerance_distributions.md`)**:
   - Comprehensive uncertainty matrix detailing median mismatches, bootstrap confidence intervals, and failure counts across all 4 historical seeds (`seed42`, `seed123`, `seed777`, `seed2026_400k`).
   - Clopper-Pearson exact confidence interval calculation for the 5 tail failure cases.
   - Analysis of prefix stability, explaining why 50,000-sample prefixes missed the $10^{-5}$ stability threshold while the 400,000-sample run achieved convergence ($\Delta = 2.395 \times 10^{-6}$).
   - OAT tolerance sensitivity ranking identifying booster extraction mismatch ($38.5\%$) and quadrupole gradient ripple ($29.2\%$) as the primary drivers of optical degradation.
   - Tabulation of concrete engineering tolerances for power supplies, extraction septa, and magnet alignment.

2. **Publication Visual Assets**:
   - High-resolution publication figure [`docs/paper_bts/figures/fig4_tolerance_curves.png`](../../paper_bts/figures/fig4_tolerance_curves.png) (300 DPI).
   - Publication vector PDF [`docs/paper_bts/figures/fig4_tolerance_curves.pdf`](../../paper_bts/figures/fig4_tolerance_curves.pdf).
   - Figure illustrates mismatch scaling curves and OAT sensitivity bar chart.

---

## 3. Verification and Standards Compliance

- **Protected Files Integrity:** All protected scientific data files remain untouched.
- **Git Branch:** Executed directly on branch `bts`.
- **Unit Tests:** All 16 unit and integration tests passed cleanly.
