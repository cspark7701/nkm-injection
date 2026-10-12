# Interpretable Correction Knobs and Normalized SVD Analysis

**Document Reference:** Task B06 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated with Finite Step Inversion and Nonlinear Re-evaluation.

---

## 1. Executive Summary

Task B06 derives orthogonal, dimensionally consistent optics correction knobs for the Korea-4GSR Booster-to-Storage Ring (BTS) transfer line.

Key findings:
1. **Reconciliation of Condition Numbers**:
   - The historical unscaled Jacobian computed directly from mixed units ($\text{m}, \text{rad}, \text{m}^{-2}$) exhibited an apparent ill-conditioned condition number $\kappa \approx 1421.6$.
   - When scaled properly by declared target optical tolerances ($\sigma_{\beta} = 0.05\text{ m}, \sigma_{\alpha} = 0.01, \sigma_{D} = 0.002\text{ m}, \sigma_{D'} = 0.001\text{ rad}$) and meaningful hardware adjustments ($\Delta K = 0.1\text{ m}^{-2}$), the **dimensionless normalized Jacobian condition number is $\kappa = 57.78$**.
   - This proves that the transfer line is well-conditioned for operational optical tuning and that the historical value was a dimensional artifact rather than a hardware sensitivity limitation.
2. **Singular Value Spectrum**:
   - The 6 singular values span $\sigma \in [181.25, 71.56, 21.44, 9.76, 4.77, 3.14]$. All 6 optical constraints are controllable without numerical rank deficiency.
3. **Null-Space Freedoms**:
   - Because 9 quadrupoles control 6 optical parameters, a 3-dimensional null space $\text{Null}(J) \subset \mathbb{R}^3$ exists. These orthogonal modes permit internal quadrupole current redistribution to optimize beta envelope clearance or relieve magnet saturation without disturbing exit matching.
4. **Finite-Step Prediction Validation**:
   - Testing linear pseudoinverse correction for a finite $+0.05\text{ m}$ target shift in $\beta_{x,\text{exit}}$ and $\beta_{y,\text{exit}}$ yields actual nonlinear shifts of $+0.05012\text{ m}$ ($0.25\%$ error) and $+0.04819\text{ m}$ ($3.6\%$ error) requiring only $|\Delta K| \le 0.0156\text{ m}^{-2}$ ($G \le 0.21\text{ T/m}$).

---

## 2. Dimensionless Sensitivity Formulation

Let $\vec{K} \in \mathbb{R}^9$ denote the 9 quadrupole strengths and $\vec{y}(\vec{K}) \in \mathbb{R}^6$ denote the exit observables $[\beta_x, \beta_y, \alpha_x, \alpha_y, D_x, D_x']^T$.

The unscaled Jacobian is:
$$J_{ij} = \frac{\partial y_i}{\partial K_j}, \quad i \in \{1,\dots,6\}, \quad j \in \{1,\dots,9\}$$

To formulate a physically meaningful condition number, we define row normalization matrix $S_{\text{row}} = \operatorname{diag}(\sigma_{\beta_x}, \sigma_{\beta_y}, \sigma_{\alpha_x}, \sigma_{\alpha_y}, \sigma_{D_x}, \sigma_{D_x'})$ and column scaling $S_{\text{col}} = \Delta K \cdot I_{9 \times 9}$:
$$\tilde{J} = S_{\text{row}}^{-1} J S_{\text{col}}$$

Central finite difference derivatives were evaluated across step sizes $h \in [10^{-3}, 10^{-4}, 10^{-5}]\text{ m}^{-2}$. The resulting singular spectrum is completely stable across step sizes:
$$\vec{\sigma}(\tilde{J}) = [181.25, 71.56, 21.44, 9.76, 4.77, 3.14]$$
$$\kappa(\tilde{J}) = \frac{\sigma_{\max}}{\sigma_{\min}} = \frac{181.25}{3.14} = 57.78$$

---

## 3. Orthogonal Quadrupole Correction Knobs (Right Singular Vectors $V^T$)

The SVD decomposition $\tilde{J} = U \Sigma V^T$ yields 6 orthogonal control modes (rows of $V^T$) and 3 null-space vectors:

| Mode / Knob | Singular Value $\sigma_i$ | Primary Optical Response | Dominant Quadrupoles | Normalised Strength Weights $[q11, \dots, q33]$ |
| :---: | :---: | :--- | :--- | :--- |
| **Knob 1** | $181.25$ | Common vertical focusing ($\beta_y, \alpha_y$) | Triplet 2 (`q21`, `q22`, `q23`) | `[-0.229, -0.239, -0.198, -0.458, -0.428, -0.542, -0.261, -0.237, -0.201]` |
| **Knob 2** | $71.56$ | Horizontal dispersion & $\beta_x$ balance | Triplet 3 (`q31`, `q32`, `q33`) vs Triplet 1 | `[-0.400, -0.386, -0.303, -0.077, +0.082, -0.113, +0.550, +0.380, +0.356]` |
| **Knob 3** | $21.44$ | Exit horizontal alpha $\alpha_x$ tuning | `q11`, `q23`, `q31` | `[-0.430, -0.379, -0.279, +0.219, +0.055, +0.525, -0.506, -0.097, -0.045]` |
| **Knob 4** | $9.76$ | Horizontal/vertical phase advance split | `q13`, `q22`, `q23` | `[+0.326, +0.094, -0.419, -0.369, -0.441, +0.540, +0.232, +0.097, -0.156]` |
| **Knob 5** | $4.77$ | Fine vertical dispersion slope $D_x'$ | `q22`, `q31`, `q33` | `[-0.001, +0.038, +0.362, -0.124, -0.450, +0.098, -0.349, +0.333, +0.639]` |
| **Knob 6** | $3.14$ | Fine horizontal dispersion offset $D_x$ | `q13`, `q33` | `[-0.361, -0.160, +0.668, -0.288, -0.064, +0.281, +0.244, +0.059, -0.410]` |

### Null Space Freedoms (Internal Redistribution Without Exit Detuning):
- **Null Mode 1**: `[+0.287, -0.519, +0.158, +0.534, -0.465, -0.040, +0.245, -0.245, -0.014]`
- **Null Mode 2**: `[+0.358, -0.350, +0.000, +0.013, +0.136, -0.149, -0.277, +0.701, -0.374]`
- **Null Mode 3**: `[+0.394, -0.471, +0.118, -0.465, +0.414, +0.121, -0.040, -0.339, +0.299]`

These null vectors demonstrate that the transfer line contains 3 true optical degrees of freedom that can be adjusted in real operation to depress internal peak envelopes without altering the injection Twiss functions delivered to the storage ring.

---

## 4. Visual Layout Asset

Figure 2 has been generated and validated:
- **PNG Asset:** [`docs/paper_bts/figures/fig2_svd_knobs.png`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig2_svd_knobs.png)
- **PDF Vector Asset:** [`docs/paper_bts/figures/fig2_svd_knobs.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig2_svd_knobs.pdf)

The figure displays:
1. Log-scale singular value spectrum showing smooth, well-conditioned decay with condition number $\kappa = 57.8$.
2. 2D heatmap of the 6 orthogonal correction knobs ($V^T$), clearly showing the family-grouped participation across the 3 triplets.
