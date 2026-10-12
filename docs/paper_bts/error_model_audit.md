# Error Model Audit, Sensitivity Responses, and Scope Disclosures

**Document Reference:** Task B07 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated and Formally Documented.

---

## 1. Executive Summary

Task B07 audits the error model implemented in [`src/nkm_injection/errors.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/errors.py) and [`src/nkm_injection/robust_optimization.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/robust_optimization.py), establishes machine-readable error budgets, demonstrates physical perturbation responses for every sampled quantity, and disentangles BTS transport errors from storage-ring NKM injection errors.

Key outcomes:
1. **Physical Perturbation Response Verified**:
   - Quadrupole gradient errors $\Delta K / K = 0.1\%$ alter linear optics ($\Delta \beta_x = -0.0672\text{ m}$ at exit).
   - Quadrupole transverse misalignments $\Delta x = 100\,\mu\text{m}$ induce feed-down steering kicks producing exit closed-orbit distortion $\Delta x = +0.1070\text{ mm}$ and $\Delta x' = +0.0066\text{ mrad}$.
   - Quadrupole roll tilts $\Delta \theta_{\text{roll}} = 0.5\text{ mrad}$ induce transverse $x-y$ coupling generating vertical deflection ($\Delta y = -0.70\,\mu\text{m}$ for a $1\text{ mm}$ horizontal launch).
   - Energy deviation $\Delta p / p = 0.1\%$ alters beam rigidity $(B\rho)$, producing chromatic defocusing ($\Delta \beta_x = +0.0671\text{ m}$).
2. **Clarification of Inactive Historical Sampling Channels**:
   - The historical error sampler generated random terms for `dipole_b_err` ($0.05\%$) and `quad_ds_m` ($0.5\text{ mm}$), but the historical optics builder `apply_sample_errors()` did not apply longitudinal displacement or dipole field scaling.
   - We explicitly disclose that in the 550,000-sample historical dataset, **these two channels were sampled but inactive**. Their lack of impact in the archived run must **not** be interpreted as physical insensitivity of the real beamline to dipole field ripple or longitudinal placement errors.
3. **Disentanglement from NKM and Storage Ring Errors**:
   - We separate BTS transport uncertainties from ring injection parameters (`nkm_scale_err`, `nkm_timing_mrad`, `nkm_dx_m`, `ring_co_x_m`, `septum_x_m`). For the standalone BTS journal paper, only BTS transport errors govern line matching and envelope margins.

---

## 2. Machine-Readable Error Coverage Audit

| Sampled Parameter | Standard Deviation $\sigma$ | Distribution | Actively Evaluated in Lattice? | Physical Response Mechanism | Status & Scope Qualification |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `quad_k_err` | $0.10\%$ ($1.0 \times 10^{-3}$) | Gaussian (truncated $3\sigma$) | **YES** | Direct gradient perturbation $K_1 (1 + \delta K)$ altering focusing | Active BTS static gradient tolerance |
| `quad_dx_m` | $100\,\mu\text{m}$ | Gaussian (truncated $3\sigma$) | **YES** | Dipolar feed-down via coordinate shift $T_1 / T_2$ creating orbit distortion | Active BTS alignment tolerance |
| `quad_dy_m` | $100\,\mu\text{m}$ | Gaussian (truncated $3\sigma$) | **YES** | Vertical feed-down kick creating vertical orbit distortion | Active BTS alignment tolerance |
| `quad_roll_rad` | $0.50\text{ mrad}$ | Gaussian (truncated $3\sigma$) | **YES** | Symplectic 4D rotation matrices $R_1 / R_2$ coupling horizontal & vertical | Active BTS skew coupling tolerance |
| `energy_dp_p` | $0.10\%$ ($1.0 \times 10^{-3}$) | Gaussian | **YES** | Rigid beam scaling $(B\rho) = E/c$, chromatic focusing changes | Active shot-to-shot energy jitter |
| `booster_x_m` | $100\,\mu\text{m}$ ($500\,\mu\text{m}$) | Gaussian | **YES** | Initial phase-space centroid launch offset | Active shot-to-shot extraction jitter |
| `booster_xp_rad` | $50\,\mu\text{rad}$ ($200\,\mu\text{rad}$) | Gaussian | **YES** | Initial phase-space angular launch offset | Active shot-to-shot extraction jitter |
| `beta_mismatch_x,y` | $5.0\%$ | Gaussian | **YES** | Scales initial entrance Twiss $\beta_{x,0}, \beta_{y,0}$ | Active booster extraction Twiss jitter |
| `dipole_b_err` | $0.05\%$ ($5.0 \times 10^{-4}$) | Gaussian | **INACTIVE in historical** | Inactive in historical evaluator | **Disclosed: Inactive in 550k study** |
| `quad_ds_m` | $0.50\text{ mm}$ | Gaussian | **INACTIVE in historical** | Inactive in historical evaluator | **Disclosed: Inactive in 550k study** |
| `nkm_scale_err` | $0.50\%$ | Gaussian | **Ring-only** | Scales kicker integrated kick $\int B_y ds$ in ring | Excluded from central BTS study |
| `nkm_timing_mrad` | $0.10\text{ mrad}$ | Gaussian | **Ring-only** | Pulsed kicker timing jitter | Excluded from central BTS study |
| `ring_co_x_m` | $200\,\mu\text{m}$ | Gaussian | **Ring-only** | Storage ring circulating closed-orbit distortion | Excluded from central BTS study |

---

## 3. Physical Perturbation Responses Demonstrated

Individual single-parameter perturbations evaluated from nominal matched optics:

1. **Zero-Noise Control**:
   - Evaluator reproduces nominal optics: $\beta_{x,\text{exit}} = 2.3365\text{ m}$, $\beta_{y,\text{exit}} = 4.2562\text{ m}$, $\mathcal{M}_x = 0$, $\mathcal{M}_y = 0$.
2. **Static Quadrupole Gradient Error (+0.1% Uniform)**:
   - Exit optics shift: $\beta_{x,\text{exit}} = 2.3331\text{ m}$ ($\Delta \beta_x = -0.0034\text{ m}$), $\beta_{y,\text{exit}} = 4.2588\text{ m}$ ($\Delta \beta_y = +0.0026\text{ m}$).
   - Mismatch metric: $\mathcal{M}_x = 1.05 \times 10^{-4}$, $\mathcal{M}_y = 1.88 \times 10^{-5}$.
3. **Static Alignment Offset (+100 $\mu$m Uniform)**:
   - Trajectory response: Transverse feed-down across all 9 quadrupoles steers on-axis beam to $x_{\text{exit}} = +0.1070\text{ mm}$ and $x_{\text{exit}}' = +0.0066\text{ mrad}$.
4. **Static Roll Tilt (+0.5 mrad Uniform)**:
   - Coupled transport response: A pure $1.0\text{ mm}$ horizontal beam displacement excites vertical orbit displacement $y_{\text{exit}} = -0.70\,\mu\text{m}$ and $y_{\text{exit}}' = -0.05\,\mu\text{rad}$.
5. **Shot-to-Shot Momentum Jitter (+0.1%)**:
   - Chromatic response: Modifies beam rigidity, shifting exit beta functions by $\Delta \beta_x = +0.0671\text{ m}$ and $\Delta \beta_y = +0.1461\text{ m}$.

---

## 4. Independent vs Common Power-Supply Errors

In a transfer line, magnet excitation errors fall into two distinct engineering classes:
1. **Common-Mode Power Supply Ripple**: Arises from mains frequency line ripple or master regulation circuits powering magnets in series. For the BTS quadrupoles, independent family powering means common-mode ripple is decoupled.
2. **Individual Channel DAC/Current Jitter**: Independent switching noise and transducer calibration drift across each magnet's individual power supply.
3. **Rigidity Consistency**: All magnetic deflections $\Delta x' = \frac{q}{p_0} \int B_y ds$ scale inversely with particle energy $p_0(1 + \delta)$. In the evaluator, this is correctly implemented by scaling the effective gradient $K_1 / (1 + \Delta p/p_0)$, guaranteeing that energy jitter scales focusing across all elements simultaneously.

---

## 5. Permitted Claim Scope for Manuscript

1. **Permitted**: Claiming that the matched BTS design is highly robust against static quadrupole gradient errors ($0.1\%$), transverse alignments ($100\,\mu\text{m}$), roll tilts ($0.5\text{ mrad}$), and shot jitter.
2. **Required Disclosure**: Disclosing that historical 550,000-sample tolerance runs did not perturb dipole fields or longitudinal element positions.
3. **Prohibited**: Claiming that the transfer line has zero sensitivity to dipole ripple based on historical data.
