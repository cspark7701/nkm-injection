# Tolerance Distributions, Uncertainty Quantification, and Engineering Requirements

**Document Reference:** Task B09 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated with 550,000 Historical Observations, Exact Binomial CIs, and OAT Sensitivity.

---

## 1. Executive Summary

Task B09 qualifies the statistical tolerance distributions and hardware engineering requirements for the Korea-4GSR Booster-to-Storage Ring (BTS) transfer line.

Key findings:
1. **Audited 550,000-Sample Statistics**:
   - The pooled historical campaign comprises 550,000 total observations across 4 independent seeds (`seed42`, `seed123`, `seed777` at 50,000 samples, and `seed2026_400k` at 400,000 samples).
   - Zero invalid evaluations were recorded ($N_{\text{invalid}} = 0$).
   - Pooled median horizontal mismatch is $\mathcal{M}_x = 0.002084$, with a 20,000-replicate bootstrap $95\%$ confidence interval of $[0.002069, 0.002097]$ at seed 1729.
   - Pooled median vertical mismatch is $\mathcal{M}_y = 0.002496$.
2. **Exact Binomial Confidence Interval for Rare Tail Failures**:
   - Across 550,000 evaluations, exactly 5 physical feasibility failures were recorded (all caused by $\beta_{y,\max} > 60.0\text{ m}$ flaring under extreme 4-sigma tail combinations).
   - The observed empirical failure rate is $p = 5 / 550,000 = 9.091 \times 10^{-6}$ ($0.909$ failures per $100,000$ bunches).
   - The Clopper-Pearson exact $95\%$ binomial confidence interval is **$[2.952 \times 10^{-6}, 2.122 \times 10^{-5}]$**.
   - These 5 cases reflect mathematical constraint violations in the linear optics evaluator, **not beam loss on vacuum chamber walls**.
3. **Prefix Stability and Convergence**:
   - The three 50,000-sample seeds missed the strict absolute median stability criterion ($\Delta < 1.0 \times 10^{-5}$).
   - The 400,000-sample run achieved convergence with a prefix difference of $\Delta = 2.395 \times 10^{-6}$ between 200,000 and 400,000 samples, establishing sample size requirements for future precision studies.
4. **Engineering Specification Recommendations**:
   - OAT variance ranking shows that booster extraction mismatch ($38.5\%$) and quadrupole gradient ripple ($29.2\%$) dominate exit optical degradation, followed by roll tilt ($16.4\%$).
   - Transverse quadrupole alignment errors ($100\,\mu\text{m}$) contribute primarily to centroid steering distortion rather than envelope swelling ($4.8\%$).

---

## 2. Statistical Uncertainty Matrix (550,000 Observations)

| Campaign Seed | Sample Size $N$ | Invalid Evals | Feasibility Failures | Median Mismatch $\mathcal{M}_x$ | Bootstrap 95% CI (Seed 1729) | Median Mismatch $\mathcal{M}_y$ | Failure Rate per $10^5$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`seed42`** | $50,000$ | $0$ | $0$ | $0.002103$ | $[0.002064, 0.002144]$ | $0.002497$ | $< 6.00$ ($95\%$ upper bound) |
| **`seed123`** | $50,000$ | $0$ | $1$ | $0.002079$ | $[0.002041, 0.002123]$ | $0.002513$ | $2.00$ |
| **`seed777`** | $50,000$ | $0$ | $0$ | $0.002103$ | $[0.002060, 0.002139]$ | $0.002507$ | $< 6.00$ ($95\%$ upper bound) |
| **`seed2026_400k`** | $400,000$ | $0$ | $4$ | $0.002084$ | $[0.002069, 0.002097]$ | $0.002496$ | $1.00$ |
| **Pooled Total** | **$550,000$** | **$0$** | **$5$** | **$0.002084$** | **$[0.002074, 0.002099]$** | **$0.002496$** | **$0.909$ ($95\%$ CI: $[0.295, 2.122]$)** |

---

## 3. Engineering Tolerance Specifications and Practical Guidelines

Based on the sensitivity scans, the following hardware tolerances are established for the BTS transfer line:

| Component / Subsystem | Parameter | Design Tolerance | Hardware Implementation Rule |
| :--- | :--- | :---: | :--- |
| **Quadrupole Power Supplies** | Relative current ripple $\Delta I / I$ | $\le 0.10\%$ ($1.0 \times 10^{-3}$) | Independent DC-DC converters with 16-bit DAC regulation. |
| **Booster Extraction Septum** | Trajectory angle ripple $\Delta x'$ | $\le 50\,\mu\text{rad}$ | Low-ripple pulsed power supply with PFN pulse forming. |
| **Magnet Girder Alignment** | Transverse offset $\Delta x, \Delta y$ | $\le 100\,\mu\text{m}$ | Precision laser tracker survey with kinematic mounts. |
| **Magnet Roll Leveling** | Skew tilt $\Delta \theta_{\text{roll}}$ | $\le 0.50\text{ mrad}$ | Digital precision bubble inclinometer alignment. |
| **RF Booster Energy** | Momentum stability $\Delta p / p$ | $\le 0.10\%$ ($1.0 \times 10^{-3}$) | Booster LLRF feedback loop controlling extraction phase. |

---

## 4. Visual Layout Asset

Figure 4 has been generated and validated:
- **PNG Asset:** [`docs/paper_bts/figures/fig4_tolerance_curves.png`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig4_tolerance_curves.png) (300 DPI).
- **PDF Vector Asset:** [`docs/paper_bts/figures/fig4_tolerance_curves.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig4_tolerance_curves.pdf).

The figure illustrates:
1. Optical mismatch metric scaling as a function of error amplitude multiplier ($0.0\times$ to $3.0\times$), demonstrating quadratic sensitivity and ample margin below the $0.05$ tight matching threshold.
2. Horizontal bar chart showing the One-At-A-Time (OAT) variance ranking across active error categories.
