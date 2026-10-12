# Comparison of Nominal Matching and Operating Margin Design

**Document Reference:** Task B08 Deliverable  
**Date:** 2026-10-13  
**Status:** Evaluated on Held-Out Ensemble of 1,000 Perturbations (Seed 98765).

---

## 1. Executive Summary

Task B08 addresses the core physical design question: **Does nominal optics matching sacrifice operating envelope margin, and can a transfer line design explicitly chosen for aperture margin provide superior robustness without compromising injection target matching?**

We perform a fair, head-to-head comparison between:
1. **Unoptimized Baseline**: Historical starting point ($\mathcal{M}_x = 8.67, \mathcal{M}_y = 28.61, \beta_{y,\max} = 242.61\text{ m}$).
2. **Nominal Matched Design**: Minimum-merit solution from nominal start ($\beta_{x,\max} = 31.44\text{ m}, \beta_{y,\max} = 50.75\text{ m}$).
3. **Low-$\beta$ Margin Design**: Discovered via multi-start topology exploration in Task B05, explicitly lowering vertical envelope peak to $\beta_{y,\max} = 36.12\text{ m}$ (a $28.8\%$ reduction in peak $\beta_y$).

Both designs match exit optics to floating-point precision ($\mathcal{M}_x = \mathcal{M}_y = 0.000000$) under nominal zero-noise conditions. When evaluated on a common **held-out ensemble of 1,000 randomized error realizations** (seed `98765`), the low-$\beta$ margin design achieves an identical $100.0\%$ feasibility rate while providing an extra **$16.5\text{ m}$ of envelope safety margin** below the $60\text{ m}$ limit.

---

## 2. Head-to-Head Comparison on Common Held-Out Error Ensemble

Both matched configurations and the unoptimized baseline were evaluated on 1,000 independently sampled error realizations combining static quadrupole gradient errors ($0.1\%$), transverse misalignments ($100\,\mu\text{m}$), roll tilts ($0.5\text{ mrad}$), energy jitter ($0.1\%$), centroid jitter ($100\,\mu\text{m}$ / $50\,\mu\text{rad}$), and booster mismatch ($5\%$):

| Performance Metric | Unoptimized Baseline | Nominal Matched Design | Low-$\beta$ Margin Design | Benefit of Margin Design |
| :--- | :---: | :---: | :---: | :---: |
| **Nominal Peak $\beta_x$ [m]** | $44.98$ | $31.44$ | **$29.65$** | $-1.79\text{ m}$ (lower) |
| **Nominal Peak $\beta_y$ [m]** | $242.61$ | $50.75$ | **$36.12$** | **$-14.63\text{ m}$ ($28.8\%$ reduction)** |
| **Held-Out Feasibility Rate** | $0.0\%$ | $100.0\%$ ($1000/1000$) | $100.0\%$ ($1000/1000$) | Identical $100.0\%$ feasibility |
| **Held-Out Median Mismatch $\mathcal{M}_x$** | $8.652$ | $0.002181$ | $0.002352$ | Comparable ($\approx 0.0022$) |
| **Held-Out 95th Percentile $\mathcal{M}_x$** | $9.287$ | $0.01513$ | $0.01611$ | Comparable |
| **Held-Out Median Mismatch $\mathcal{M}_y$** | $28.578$ | $0.002544$ | $0.002330$ | Slightly better ($8.4\%$ lower) |
| **Held-Out 95th Percentile $\mathcal{M}_y$** | $30.137$ | $0.01865$ | $0.02063$ | Comparable |
| **Held-Out Median Peak $\beta_x$ [m]** | $51.97$ | $31.23$ | **$29.48$** | $-1.75\text{ m}$ |
| **Held-Out Worst-Case Peak $\beta_x$ [m]** | $65.44$ | $41.42$ | **$37.41$** | $-4.01\text{ m}$ |
| **Held-Out Median Peak $\beta_y$ [m]** | $242.31$ | $50.73$ | **$36.12$** | **$-14.61\text{ m}$ ($28.8\%$ reduction)** |
| **Held-Out Worst-Case Peak $\beta_y$ [m]** | $267.10$ | $57.05$ | **$40.58$** | **$-16.47\text{ m}$ extra stay-clear** |
| **Maximum Gradient $G_{\max}$ [T/m]** | $19.86$ | $37.67$ (`q22`) | $40.02$ (`q32`) | $+2.35\text{ T/m}$ cost |
| **Maximum Pole-Tip $B_{\text{pole}}$ [T]** | $0.384$ | $0.729$ | $0.774$ | Comfortable ($< 0.78\text{ T} \ll 1.2\text{ T}$) |

---

## 3. Physical Trade-Off and Hardware Cost Analysis

### 3.1 Aperture Margin Gain:
- In the nominal matched design, the worst-case vertical beta function under random errors flares to $\beta_{y,\max} = 57.05\text{ m}$, coming within $2.95\text{ m}$ of the hard $60.0\text{ m}$ constraint.
- In the low-$\beta$ margin design, the worst-case vertical beta function never exceeds $\beta_{y,\max} = 40.58\text{ m}$, maintaining a robust **$19.42\text{ m}$ safety cushion** below the $60\text{ m}$ threshold under identical error realizations.

### 3.2 Hardware Strength Cost:
- The low-$\beta$ margin design requires slightly higher focusing gradients in `q12` ($-36.11\text{ T/m}$) and `q32` ($+40.02\text{ T/m}$).
- However, the peak pole-tip field is $B_{\text{pole}} = 0.774\text{ T}$, which remains well below the $1.2\text{ T}$ iron pole saturation limit ($35.5\%$ safety margin).

### 3.3 Target Optics Invariance:
- Both designs match the exact required injection Twiss parameters at marker `m4` ($\beta_x = 2.3365\text{ m}, \beta_y = 4.2562\text{ m}, D_x = 0.0809\text{ m}, D_x' = 0.0475\text{ rad}$).
- Under random errors, their median and 95th-percentile mismatch metrics are practically identical ($\mathcal{M} \approx 0.0022$).

---

## 4. Visual Layout Asset

Figure 3 has been generated and validated:
- **PNG Asset:** [`docs/paper_bts/figures/fig3_margin_tradeoff.png`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig3_margin_tradeoff.png) (300 DPI).
- **PDF Vector Asset:** [`docs/paper_bts/figures/fig3_margin_tradeoff.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig3_margin_tradeoff.pdf).

The figure visualizes:
1. Top panel: Transverse betatron functions $\beta_x(s)$ and $\beta_y(s)$ comparing the nominal matched design against the low-$\beta$ margin design along the 21.789 m beamline, showing the dramatic reduction in vertical beta flare from $50.7\text{ m}$ down to $36.1\text{ m}$.
2. Bottom panel: Horizontal dispersion function $D_x(s)$ for both designs, confirming identical convergence to the target exit dispersion ($D_x = 0.0809\text{ m}$).
