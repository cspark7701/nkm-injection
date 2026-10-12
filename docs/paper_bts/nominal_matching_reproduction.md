# Nominal Matching Reproduction, Multi-Start Topology, and Baseline Comparison

**Document Reference:** Task B05 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated and Formally Documented across 5 Outer Seeds.

---

## 1. Executive Summary

Task B05 reproduces the archived deterministic optimization solution for the Korea-4GSR Booster-to-Storage Ring (BTS) transfer line, audits multi-start solver behavior, and evaluates unoptimized baseline vs matched optical profiles.

Key findings:
1. **Exact Reproduction of Archived Solution**: Running from the nominal initial strengths under seed 42 reproduces the archived matched solution to full floating-point precision:
   - Final merit: $1.290601 \times 10^{-13}$
   - Exit optical mismatches: $\mathcal{M}_x = 0.000000$, $\mathcal{M}_y = 0.000000$
   - Exit dispersion residuals: $\Delta D_x = 4.38 \times 10^{-11}\text{ m}$, $\Delta D_x' = -1.77 \times 10^{-11}\text{ rad}$
   - Peak betatron functions: $\beta_{x,\max} = 31.4368\text{ m}$, $\beta_{y,\max} = 50.7459\text{ m}$ (satisfying $\le 60.0\text{ m}$).
2. **Multi-Start Topology & Feasibility Separation**: Running 5 independent outer seeds (`[42, 123, 777, 2026, 9999]`) with 3 multi-starts each demonstrates the multimodal landscape of 9-quadrupole transfer line matching. While all restarts achieve mathematical optimizer convergence ($\text{merit} < 10^{-12}$), multiple local minima violate the physical $\beta \le 60\text{ m}$ constraint (e.g., Start 1 under seed 123 reaches $\beta_{y,\max} = 61.89\text{ m}$).
3. **Discovery of Alternative Low-Beta Topology**: Randomized multi-start exploration discovers an alternative viable topology (Start 2 under seed 123) that matches exit optics to $\text{merit} = 8.50 \times 10^{-14}$ while lowering peak beta functions even further to $\beta_{x,\max} = 29.65\text{ m}$ and $\beta_{y,\max} = 36.12\text{ m}$.

---

## 2. Formulation of the Matching Problem

The optimization adjusts the 9 independent quadrupole strengths $\vec{K} = [K_{11}, K_{12}, K_{13}, K_{21}, K_{22}, K_{23}, K_{31}, K_{32}, K_{33}]^T$ to match the 6 exit optical parameters $\vec{y}(\vec{K}) = [\beta_x, \beta_y, \alpha_x, \alpha_y, D_x, D_x']^T$ to target values $\vec{y}_{\text{target}}$.

### 2.1 Dimensionless Residual Formulation
To avoid ill-conditioning from mixed units (meters vs radians), the objective vector $\vec{R}(\vec{K}) \in \mathbb{R}^6$ is normalized by declared optical tolerances:
$$R_1 = \frac{\beta_{x,\text{exit}} - \beta_{x,\text{target}}}{\sigma_{\beta_x}}, \quad \sigma_{\beta_x} = 0.05\text{ m}$$
$$R_2 = \frac{\beta_{y,\text{exit}} - \beta_{y,\text{target}}}{\sigma_{\beta_y}}, \quad \sigma_{\beta_y} = 0.05\text{ m}$$
$$R_3 = \frac{\alpha_{x,\text{exit}} - \alpha_{x,\text{target}}}{\sigma_{\alpha_x}}, \quad \sigma_{\alpha_x} = 0.01$$
$$R_4 = \frac{\alpha_{y,\text{exit}} - \alpha_{y,\text{target}}}{\sigma_{\alpha_y}}, \quad \sigma_{\alpha_y} = 0.01$$
$$R_5 = \frac{D_{x,\text{exit}} - D_{x,\text{target}}}{\sigma_{D_x}}, \quad \sigma_{D_x} = 0.002\text{ m}$$
$$R_6 = \frac{D_{x,\text{exit}}' - D_{x,\text{target}}'}{\sigma_{D_x'}}, \quad \sigma_{D_x'} = 0.001\text{ rad}$$

The scalar merit function minimized is:
$$\Phi(\vec{K}) = \frac{1}{2} \|\vec{R}(\vec{K})\|_2^2 = \frac{1}{2} \sum_{i=1}^6 R_i^2$$

### 2.2 Physical and Hardware Constraints
- Quadrupole boundaries: $|K_{11}| \le 2.5\text{ m}^{-2}$, $|K_{33}| \le 2.5\text{ m}^{-2}$, and $|K_i| \le 3.0\text{ m}^{-2}$ for $i \in \{12, 13, 21, 22, 23, 31, 32\}$.
- Peak envelope limits: $\beta_{x,\max} \le 60.0\text{ m}$, $\beta_{y,\max} \le 60.0\text{ m}$, and $D_{x,\max} \le 1.5\text{ m}$.

---

## 3. Comparison: Unoptimized Baseline vs Matched Solutions

| Parameter | Unoptimized Baseline | Nominal Matched (Seed 42 Start 0) | Low-Beta Matched (Seed 123 Start 2) | Target Value | Unit |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Exit $\beta_x$** | $44.9808$ | **$2.3365$** | **$2.3365$** | $2.336495$ | m |
| **Exit $\beta_y$** | $242.6069$ | **$4.2562$** | **$4.2562$** | $4.256241$ | m |
| **Exit $\alpha_x$** | $+0.6248$ | **$-0.0163$** | **$-0.0163$** | $-0.016335$ | — |
| **Exit $\alpha_y$** | $-10.2146$ | **$+0.0178$** | **$+0.0178$** | $+0.017772$ | — |
| **Exit $D_x$** | $+0.0809$ | **$+0.0809$** | **$+0.0809$** | $+0.080868$ | m |
| **Exit $D_x'$** | $+0.0475$ | **$+0.0475$** | **$+0.0475$** | $+0.047472$ | rad |
| **Horizontal Mismatch $\mathcal{M}_x$** | $8.6746$ | **$0.000000$** | **$0.000000$** | $0.0000$ | — |
| **Vertical Mismatch $\mathcal{M}_y$** | $28.6147$ | **$0.000000$** | **$0.000000$** | $0.0000$ | — |
| **Peak $\beta_x$** | $44.98$ | **$31.44$** | **$29.65$** | $\le 60.0$ | m |
| **Peak $\beta_y$** | $242.61$ | **$50.75$** | **$36.12$** | $\le 60.0$ | m |
| **Peak $D_x$** | $0.66$ | **$0.58$** | **$0.52$** | $\le 1.5$ | m |
| **Objective Merit $\Phi$** | $2.450 \times 10^7$ | **$1.291 \times 10^{-13}$** | **$8.503 \times 10^{-14}$** | $0.00$ | — |

---

## 4. Quadrupole Settings for the Two Matched Topologies

| Quadrupole | Family Role | Nominal Matched Solution $K_1$ [$\text{m}^{-2}$] | Low-Beta Solution $K_1$ [$\text{m}^{-2}$] | Nominal Gradient $G$ [T/m] | Low-Beta Gradient $G$ [T/m] |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `q11` | Triplet 1 | $-0.367525$ | $+0.973845$ | $-4.904$ | $+12.994$ |
| `q12` | Triplet 1 | $-1.216433$ | $-2.706382$ | $-16.230$ | $-36.109$ |
| `q13` | Triplet 1 | $+1.586072$ | $+1.687002$ | $+21.162$ | $+22.509$ |
| `q21` | Triplet 2 | $-1.068373$ | $+1.149694$ | $-14.255$ | $+15.340$ |
| `q22` | Triplet 2 | $+2.823108$ | $-2.945555$ | $+37.667$ | $-39.301$ |
| `q23` | Triplet 2 | $-2.490968$ | $+1.996604$ | $-33.236$ | $+26.640$ |
| `q31` | Triplet 3 | $+2.042678$ | $-1.643728$ | $+27.255$ | $-21.932$ |
| `q32` | Triplet 3 | $-1.434271$ | $+2.999585$ | $-19.137$ | $+40.022$ |
| `q33` | Triplet 3 | $+0.351115$ | $-1.289728$ | $+4.685$ | $-17.208$ |

---

## 5. Multi-Start Reproducibility and Feasibility Matrix

To quantify solver stability across independent seeds, we evaluated 5 distinct RNG sequences generating 3 restarts each:

| Outer Seed | Total Starts | Feasible Solutions | Infeasible Solutions | Best Merit $\Phi$ | Selected Peak Beta $(\beta_{x,\max}, \beta_{y,\max})$ | Wall Time [s] |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **42** | $3$ | **$1$** | $2$ | $1.291 \times 10^{-13}$ | $(31.44\text{ m}, 50.75\text{ m})$ | $9.44$ |
| **123** | $3$ | **$2$** | $1$ | $8.503 \times 10^{-14}$ | $(29.65\text{ m}, 36.12\text{ m})$ | $7.43$ |
| **777** | $3$ | **$2$** | $1$ | $1.129 \times 10^{-13}$ | $(36.09\text{ m}, 49.67\text{ m})$ | $9.14$ |
| **2026** | $3$ | **$3$** | $0$ | $1.140 \times 10^{-13}$ | $(35.63\text{ m}, 43.10\text{ m})$ | $9.36$ |
| **9999** | $3$ | **$3$** | $0$ | $1.226 \times 10^{-13}$ | $(35.39\text{ m}, 48.20\text{ m})$ | $7.73$ |

### Physical Insight:
- Every run that begins from the nominal configuration (Start 0) converges deterministically to the identical nominal candidate ($\text{merit} = 1.291 \times 10^{-13}, \beta = 31.44 / 50.75\text{ m}$).
- Across randomized initializations, $11$ out of $15$ starts ($73.3\%$) yield physically feasible solutions, whereas $4$ starts find local minima with excessive vertical beta swelling ($\beta_{y,\max} > 60\text{ m}$).
- This confirms that **feasibility-first candidate selection** is indispensable for accelerator transfer lines: an optimizer claiming "success" on objective value alone will routinely deliver physically unusable lattices with severe envelope clipping.
