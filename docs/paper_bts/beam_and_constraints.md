# Beam Parameters, Hardware Limits, and Constraint Justifications

**Document Reference:** Task B03 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated and Formally Documented.

---

## 1. Booster Beam Parameters: Historical vs Design Specifications

A critical requirement of Task B03 is to formally distinguish between the **historical inherited constraint beam** used in optimization definitions and the **author-sourced design booster beam** for the Korea-4GSR facility.

### 1.1 Comparative Beam Parameter Matrix

| Parameter | Symbol [Unit] | Historical Inherited Beam (`constraints.py`) | Baseline Tracking Beam (`bts.ipynb` Cell 48) | Author Design Booster Beam (Korea-4GSR) | Physical Meaning / Provenance |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Beam Energy** | $E_0$ [GeV] | $4.00$ | $4.00$ | $4.00$ | Full-energy booster extraction |
| **Lorentz Factor** | $\gamma$ | $7827.8$ | $7827.8$ | $7827.8$ | Ultra-relativistic electron beam |
| **Magnetic Rigidity** | $(B\rho)$ [$\text{T}\cdot\text{m}$] | $13.3426$ | $13.3426$ | $13.3426$ | $p_0 / q = E_0 / c$ |
| **Horizontal Emittance** | $\epsilon_x$ [$\text{nm}\cdot\text{rad}$] | **$100.0$** | **$10.89$** | **$7.67$** | Geometric emittance |
| **Vertical Emittance** | $\epsilon_y$ [$\text{nm}\cdot\text{rad}$] | **$10.0$** | **$1.089$** | **$0.767$** | 10% transverse coupling ratio |
| **Relative Momentum Spread** | $\sigma_\delta$ [$10^{-3}$] | $1.10$ | $1.00$ | $1.00$ | RMS fractional momentum spread |
| **Bunch Length** | $\sigma_z$ [mm] | $13.4$ | $13.4$ | $13.4$ | RMS longitudinal bunch length |
| **Transverse Centroid Jitter** | $\sigma_{x,\text{jit}}, \sigma_{y,\text{jit}}$ [$\mu\text{m}$] | $500$ | — | $100$ | Shot-to-shot extraction centroid jitter |
| **Angular Jitter** | $\sigma_{x',\text{jit}}, \sigma_{y',\text{jit}}$ [$\mu\text{rad}$] | $200$ | — | $50$ | Shot-to-shot trajectory angle jitter |

> [!IMPORTANT]
> **Strict Nomenclature Requirement**: The historical $\epsilon_x = 100\text{ nm}\cdot\text{rad}$ beam was adopted in early optimization routines as an ultra-conservative stress-test envelope to ensure ample stay-clear margin. **It must NEVER be described in the manuscript as the nominal design booster beam.** The Korea-4GSR booster design produces an extracted horizontal emittance of $\epsilon_x = 7.67\text{ nm}\cdot\text{rad}$.

---

## 2. Vacuum Chamber Apertures and Justification of the $\beta \le 60\text{ m}$ Envelope Limit

The physical vacuum chamber along the BTS line consists of:
1. Standard / straight pipe sections: inner half-aperture $A_{x,1} = A_{y,1} = 19.35\text{ mm}$ (aperture station `ap_rect` at $s = 0.0\text{ m}$ and $s = 21.789\text{ m}$).
2. Expanded arc sections: inner half-aperture $A_{x,2} = A_{y,2} = 30.00\text{ mm}$ (aperture station `ap_rect2` at $s = 6.833\text{ m}$ and $s = 11.761\text{ m}$).

### 2.1 Transverse Beam Envelope Formulation

The transverse RMS beam sizes including dispersion and momentum spread are:
$$\sigma_x(s) = \sqrt{\beta_x(s) \epsilon_x + \left[D_x(s) \sigma_\delta\right]^2}$$
$$\sigma_y(s) = \sqrt{\beta_y(s) \epsilon_y}$$

To guarantee transmission without halo scraping, accelerator design requires at least $n_\sigma \ge 6$ standard deviations of clearance between the beam core and the vacuum chamber wall:
$$\text{Clearance}_u(s) = A_u(s) - 6\sigma_u(s) - |\Delta u_{\text{orbit}}(s)| \ge \delta_{\text{margin}}$$

### 2.2 Beam Envelope and Clearance at $\beta = 60\text{ m}$

Evaluating at the maximum allowed optical constraint $\beta_{x,y} = 60.0\text{ m}$ with peak BTS dispersion $D_x = 0.66\text{ m}$ and $A_{\min} = 19.35\text{ mm}$:

| Beam Model | Transverse Emittances ($\epsilon_x / \epsilon_y$) | RMS Size $\sigma_x$ at $\beta=60\text{ m}$ | RMS Size $\sigma_y$ at $\beta=60\text{ m}$ | Stay-Clear $A_{\min} / \sigma_x$ | $6\sigma_x$ Clearance [mm] | $6\sigma_y$ Clearance [mm] |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Historical Conservative** | $100\text{ nm} / 10\text{ nm}$ | $2.555\text{ mm}$ | $0.775\text{ mm}$ | **$7.6\,\sigma$** | $+4.02\text{ mm}$ | $+14.70\text{ mm}$ |
| **Tracking Baseline** | $10.89\text{ nm} / 1.09\text{ nm}$ | $1.044\text{ mm}$ | $0.256\text{ mm}$ | **$18.5\,\sigma$** | $+13.09\text{ mm}$ | $+17.82\text{ mm}$ |
| **Design Korea-4GSR** | $7.67\text{ nm} / 0.77\text{ nm}$ | $0.946\text{ mm}$ | $0.215\text{ mm}$ | **$20.4\,\sigma$** | $+13.67\text{ mm}$ | $+18.06\text{ mm}$ |

### 2.3 Physical Justification of the $\beta_{\max} \le 60\text{ m}$ Constraint
The limit $\beta \le 60\text{ m}$ is **not** a physical aperture plate. Rather, it is an optical envelope constraint chosen such that:
1. Even under the historical high-emittance case ($100\text{ nm}\cdot\text{rad}$), the full beam envelope remains strictly within $7.6\,\sigma$ of the narrowest $19.35\text{ mm}$ aperture, providing $> 4\text{ mm}$ physical clearance for orbit distortion and alignment tolerances.
2. For the actual $7.67\text{ nm}\cdot\text{rad}$ design beam, the clearance exceeds $20\,\sigma$ ($> 13.6\text{ mm}$ margin), completely eliminating linear aperture scraping during transport.
3. In the unoptimized baseline, $\beta_y$ flares to $242.61\text{ m}$, which under static errors causes large beam swelling and aperture clipping. Constraining $\beta \le 60\text{ m}$ keeps beam sizes sub-millimeter.

---

## 3. Quadrupole Gradients, Pole-Tip Fields, and Hardware Bounds

All 9 quadrupoles have core length $L_{\text{quad}} = 0.200\text{ m}$ and mechanical bore radius $r_0 = 19.35\text{ mm}$ ($0.01935\text{ m}$).

### 3.1 Field-to-Gradient Conversion
The magnetic field gradient $G$ and pole-tip magnetic field $B_{\text{pole}}$ are related to the normalized quadrupole strength $K_1$ by:
$$G = K_1 (B\rho) = K_1 \cdot 13.34256\text{ T}\cdot\text{m}$$
$$B_{\text{pole}} = |G| \cdot r_0 = |K_1| \cdot (B\rho) \cdot r_0$$

For standard water-cooled iron-dominated electromagnets, magnetic saturation of standard silicon steel poles begins above $B_{\text{pole}} \approx 1.2\text{ T} - 1.4\text{ T}$. Therefore, $B_{\text{pole}} \le 1.2\text{ T}$ represents a safe linear operating regime.

### 3.2 Quadrupole Hardware Limits and Matched Solution Operating Points

| Quadrupole Name | Family / Role | Allowable Bounds $|K_1|$ [$\text{m}^{-2}$] | Max Gradient $|G|$ [T/m] | Max Pole-Tip $B_{\text{pole}}$ [T] | Matched Setting $K_1$ [$\text{m}^{-2}$] | Matched Gradient $|G|$ [T/m] | Matched $B_{\text{pole}}$ [T] | Margin to 1.2 T Saturation |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `q11` | Triplet 1 (Entrance) | $[-2.5, +2.5]$ | $33.36$ | $0.645$ | $-0.367525$ | $4.904$ | $0.0949$ | **92.1%** |
| `q12` | Triplet 1 (Entrance) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $-1.216433$ | $16.230$ | $0.3141$ | **73.8%** |
| `q13` | Triplet 1 (Entrance) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $+1.586072$ | $21.162$ | $0.4095$ | **65.9%** |
| `q21` | Triplet 2 (Middle Arc) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $-1.068373$ | $14.255$ | $0.2758$ | **77.0%** |
| `q22` | Triplet 2 (Middle Arc) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $+2.823108$ | $37.667$ | $0.7289$ | **39.3%** |
| `q23` | Triplet 2 (Middle Arc) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $-2.490968$ | $33.236$ | $0.6431$ | **46.4%** |
| `q31` | Triplet 3 (Exit Matching) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $+2.042678$ | $27.255$ | $0.5274$ | **56.1%** |
| `q32` | Triplet 3 (Exit Matching) | $[-3.0, +3.0]$ | $40.03$ | $0.775$ | $-1.434271$ | $19.137$ | $0.3703$ | **69.1%** |
| `q33` | Triplet 3 (Exit Matching) | $[-2.5, +2.5]$ | $33.36$ | $0.645$ | $+0.351115$ | $4.685$ | $0.0907$ | **92.4%** |

### Findings:
1. **Zero Saturation**: In the matched configuration, all 9 quadrupoles operate comfortably below $B_{\text{pole}} < 0.73\text{ T}$, well beneath the $1.2\text{ T}$ iron saturation boundary.
2. **Polarity and Margin**: The strongest quadrupole is `q22` ($K_1 = +2.823108\text{ m}^{-2}$, $G = 37.67\text{ T/m}$), utilizing $94.1\%$ of its nominal $|K_1| \le 3.0\text{ m}^{-2}$ bound but retaining ample $39.3\%$ physical margin before pole saturation.

---

## 4. Transfer Line Error Budget Formulation

The comprehensive error model incorporates both static machine imperfections and shot-to-shot beam jitter:

| Error Category | Parameter | Distribution | Standard Deviation ($\sigma$) | Physical Origin / Notes |
| :--- | :--- | :---: | :---: | :--- |
| **Quadrupole Gradient** | $\Delta K_1 / K_1$ | Gaussian (truncated $3\sigma$) | $0.10\%$ ($1.0 \times 10^{-3}$) | Power supply regulation and calibration error |
| **Dipole Field** | $\Delta B_0 / B_0$ | Gaussian (truncated $3\sigma$) | $0.05\%$ ($5.0 \times 10^{-4}$) | Main bend power supply stability |
| **Quadrupole Transverse Alignment** | $\Delta x, \Delta y$ | Gaussian (truncated $3\sigma$) | $100\,\mu\text{m}$ | Survey and girder alignment tolerance |
| **Quadrupole Roll Angle** | $\Delta \theta_{\text{roll}}$ | Gaussian (truncated $3\sigma$) | $0.50\text{ mrad}$ | Mechanical roll leveling tolerance |
| **Longitudinal Position** | $\Delta s$ | Gaussian (truncated $3\sigma$) | $0.50\text{ mm}$ | Flange-to-flange positioning |
| **Booster Centroid Jitter** | $\delta x_{\text{inj}}, \delta y_{\text{inj}}$ | Gaussian | $100\,\mu\text{m}$ ($500\,\mu\text{m}$ stress) | Shot-to-shot extraction kicker ripple |
| **Booster Angular Jitter** | $\delta x_{\text{inj}}', \delta y_{\text{inj}}'$ | Gaussian | $50\,\mu\text{rad}$ ($200\,\mu\text{rad}$ stress) | Shot-to-shot trajectory angle variation |
| **Booster Energy Jitter** | $\Delta p / p_0$ | Gaussian | $0.10\%$ ($1.0 \times 10^{-3}$) | Booster RF cavity amplitude/phase jitter |
| **Booster Optical Mismatch Jitter**| $\Delta \beta / \beta$ | Gaussian | $5.0\%$ | Extracted Twiss variation |

---

## 5. Permitted Scientific Claim Scope

Based on the physical justifications established in B02 and B03:
1. **Permitted**: Claiming that the nominal matching solution satisfies all physical hardware constraints ($B_{\text{pole}} \le 1.2\text{ T}$) with substantial margin.
2. **Permitted**: Claiming that the matched beam envelope provides $\ge 18.5\,\sigma$ clearance across the entire transfer line for the design booster beam.
3. **Prohibited**: Claiming that the 5 optical feasibility failures across 550,000 samples represent lost bunches on physical aperture walls. As proven above, even a $60\text{ m}$ beta function provides $> 13\text{ mm}$ clearance; the 5 failure cases reflect mathematical constraint violations in the optimizer, not beam loss.
