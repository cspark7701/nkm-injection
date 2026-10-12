# Milestone 167: Nominal Matching Reproduction and Multi-Start Baselines (Task B05)

**Completed:** 2026-10-13  
**Status:** Successfully Executed on branch `bts`.  
**Task Reference:** Task B05 in [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md).

---

## 1. Executive Summary

Milestone 167 reproduces the nominal deterministic optics matching solution for the Korea-4GSR BTS transfer line, verifies dimensionless residual objective scaling, conducts a 5-seed multi-start optimization study, and contrasts baseline and matched optics profiles.

The nominal matched solution is reproduced to exact floating-point precision ($\text{merit} = 1.290601 \times 10^{-13}, \mathcal{M}_x = 0, \mathcal{M}_y = 0, \beta_{x,\max} = 31.44\text{ m}, \beta_{y,\max} = 50.75\text{ m}$). Multi-start evaluations across seeds `[42, 123, 777, 2026, 9999]` demonstrated the existence of multiple local minima, confirming that unconstrained numerical convergence frequently violates envelope limits ($\beta_{y,\max} > 60\text{ m}$). Furthermore, multi-start exploration discovered an alternative low-beta topology achieving $\beta_{x,\max} = 29.65\text{ m}$ and $\beta_{y,\max} = 36.12\text{ m}$.

---

## 2. Key Accomplishments & Deliverables

1. **Reproduction and Baseline Report (`docs/paper_bts/nominal_matching_reproduction.md`)**:
   - Exact mathematical reproduction of the nominal 9-quadrupole matched strengths.
   - Comparative parameter matrix contrasting the unoptimized baseline ($\mathcal{M}_x = 8.67, \mathcal{M}_y = 28.61, \beta_{y,\max} = 242.61\text{ m}$) against the nominal matched design and newly discovered low-beta design.
   - Comprehensive multi-start feasibility matrix over 5 outer seeds (15 total starts), documenting solver success vs physical feasibility.

2. **Dimensionless Residual Normalization Audit**:
   - Documented the dimensionless objective formulation scaling exit Twiss residuals by $\sigma_\beta = 0.05\text{ m}, \sigma_\alpha = 0.01, \sigma_D = 0.002\text{ m}, \sigma_{D'} = 0.001\text{ rad}$.

---

## 3. Verification and Standards Compliance

- **Protected Files Integrity:** All protected scientific data files remain untouched.
- **Git Branch:** Executed directly on branch `bts`.
- **Unit Tests:** All 16 tests in `tests/test_bts_lattice.py` and `tests/test_baseline.py` passed cleanly.
