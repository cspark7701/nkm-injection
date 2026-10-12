# Transport and Optics Evaluator Validation Report

**Document Reference:** Task B04 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated with Element-by-Element Tracking and Matrix Theory.

---

## 1. Executive Summary

Task B04 validates the linear optics evaluator and element-by-element particle tracking engine for the 21.789 m Booster-to-Storage Ring (BTS) transfer line.

We cross-verify:
1. **Transfer Matrix Symplecticity**: Transfer matrices $M_{44}$ and $M_{66}$ satisfy symplectic conservation laws to floating-point numerical precision ($\|M_{44}^T J M_{44} - J\|_\infty = 2.44 \times 10^{-15}$ and $\|M_{66}^T J M_{66} - J\|_\infty = 2.07 \times 10^{-12}$).
2. **Covariance Matrix & Envelope Agreement**: Linear transfer matrix propagation $\Sigma_{\text{out}} = M \Sigma_{\text{in}} M^T$ is compared against $10,000$-particle and $100,000$-particle element-by-element tracking. Tracked beam sizes agree with linear matrix theory within statistical sampling bounds ($< 0.5\%$).
3. **Dispersion Conventions & Propagations**: Linear dispersion propagation ($\vec{D}_{\text{out}} = M \vec{D}_{\text{in}} + \vec{\eta}_{\text{line}}$) is audited and validated against off-momentum trajectory tracking.
4. **Physical Vacuum Aperture Loss Accounting**: Discrete aperture stations (`ap_rect` at $\pm 19.35\text{ mm}$ and `ap_rect2` at $\pm 30.00\text{ mm}$) are tracked with divergent and halo beams, verifying 100% loss localization at the declared physical coordinates.

---

## 2. Transfer Matrix Consistency and Symplecticity

For Hamiltonian transport in the absence of radiation damping, the $2n \times 2n$ transfer matrix $M$ must satisfy the symplectic condition:
$$M^T J M = J, \quad J = \bigoplus_{i=1}^n \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$$

### 2.1 Symplecticity Quantifications across BTS Line
- **Transverse 4D Symplecticity Error:**
  $$\|M_{44}^T J_4 M_{44} - J_4\|_\infty = 2.442 \times 10^{-15}$$
- **Full 6D Symplecticity Error:**
  $$\|M_{66}^T J_6 M_{66} - J_6\|_\infty = 2.074 \times 10^{-12}$$

Both values are orders of magnitude below the standard threshold ($10^{-10}$), confirming that pyAT symplectic integrators (`DriftPass`, `StrMPoleSymplectic4Pass`, `BndMPoleSymplectic4Pass`) preserve canonical phase-space geometry without artificial dissipative damping.

---

## 3. Comparison of Linear Optics with Particle Tracking

To verify transport consistency, we inject an ensemble of $N = 10,000$ particles drawn from the multivariate Gaussian covariance matrix $\Sigma_{\text{in}}$ corresponding to the Korea-4GSR booster extraction design beam ($\epsilon_x = 7.67\text{ nm}\cdot\text{rad}, \epsilon_y = 0.767\text{ nm}\cdot\text{rad}$):

$$\Sigma_{x,\text{in}} = \begin{pmatrix} \beta_{x,0}\epsilon_x & -\alpha_{x,0}\epsilon_x \\ -\alpha_{x,0}\epsilon_x & \gamma_{x,0}\epsilon_x \end{pmatrix}, \quad \Sigma_{y,\text{in}} = \begin{pmatrix} \beta_{y,0}\epsilon_y & -\alpha_{y,0}\epsilon_y \\ -\alpha_{y,0}\epsilon_y & \gamma_{y,0}\epsilon_y \end{pmatrix}$$

### 3.1 Transverse Envelope Comparison at BTS Exit ($s = 21.789\text{ m}$)

| Observable | Analytical Matrix Propagation ($\Sigma_{\text{out}} = M \Sigma_{\text{in}} M^T$) | Element Tracking ($N=10,000$ Particles) | Element Tracking ($N=100,000$ Particles) | Relative Difference | Statistical Confidence |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Horizontal $\beta_x$ [m]** | $44.9808$ | $44.912$ | $45.144$ | $0.36\%$ | Consistent within $1/\sqrt{N}$ |
| **Vertical $\beta_y$ [m]** | $242.6069$ | $241.984$ | $243.468$ | $0.35\%$ | Consistent within $1/\sqrt{N}$ |
| **RMS Size $\sigma_x$ [mm]** | $0.5874$ | $0.5870$ | $0.5885$ | $0.18\%$ | Passed ($< 1\%$) |
| **RMS Size $\sigma_y$ [mm]** | $0.4314$ | $0.4308$ | $0.4321$ | $0.17\%$ | Passed ($< 1\%$) |
| **On-Energy Transmission** | $100.0\%$ | $100.0\%$ ($10,000/10,000$) | $100.0\%$ ($100,000/100,000$) | $0.00\%$ | **Zero unperturbed loss** |

---

## 4. Dispersion Vector Convention and Cross-Verification

The longitudinal coordinate and momentum deviation are defined by $\delta \equiv \Delta p / p_0$. The dispersion vector $\vec{D} = [D_x, D_x', D_y, D_y']^T$ transforms linearly according to:
$$\vec{D}(s) = M(s) \vec{D}_0 + \vec{\eta}_{\text{line}}(s)$$

Where $\vec{\eta}_{\text{line}}(s)$ is the chromatic deflection accumulated across the bending magnets.

### Dispersion Conventions in pyAT:
In pyAT, `twiss_in` dictionaries take `dispersion = [Dx, Dpx, Dy, Dpy]`.
- Entrance dispersion: $D_{x,0} = 0.2762\text{ m}$, $D_{x,0}' = -0.0657\text{ rad}$.
- Exit dispersion: $D_{x,\text{exit}} = 0.080868\text{ m}$, $D_{x,\text{exit}}' = 0.047472\text{ rad}$.

When tracking an off-momentum test trajectory with $\delta = 1.0 \times 10^{-5}$ through the full lattice, the tracked phase-space displacement $\Delta x / \delta$ and $\Delta x' / \delta$ matches the linear optical dispersion vector to high numerical accuracy.

---

## 5. Physical Aperture Stations and First-Loss Accounting

To verify that physical aperture stations properly intercept halo particles at their physical positions rather than relying on abstract mathematical boundaries:

### 5.1 Aperture Stations Tested:
1. **Station 1 (`ap_rect`)**: Located at $s = 0.0000\text{ m}$ (immediately after marker `m1`), limits $x, y \in [-19.35, +19.35]\text{ mm}$.
2. **Station 2 (`ap_rect2`)**: Located at $s = 6.8330\text{ m}$ (upstream of dipole `b1`), limits $x, y \in [-30.00, +30.00]\text{ mm}$.
3. **Station 3 (`ap_rect2`)**: Located at $s = 11.7610\text{ m}$ (upstream of dipole `b2`), limits $x, y \in [-30.00, +30.00]\text{ mm}$.
4. **Station 4 (`ap_rect`)**: Located at $s = 21.7890\text{ m}$ (immediately before exit marker `m4`), limits $x, y \in [-19.35, +19.35]\text{ mm}$.

### 5.2 Divergent Beam Scraping Test:
When tracking $N = 10,000$ particles launched with wide transverse coordinates and large divergence ($\sigma_{p_x} = \sigma_{p_y} = 8\text{ mrad}$):
- **First Loss at Station 2 ($s = 6.833\text{ m}$)**: $8,258$ particles ($84.2\%$ of losses) are intercepted at the entrance to the first bending arc where the beam envelope first expands beyond $\pm 30\text{ mm}$.
- **First Loss at Station 3 ($s = 11.761\text{ m}$)**: $1,001$ particles ($10.2\%$ of losses) are intercepted at the middle dipole station.
- **First Loss at Station 4 ($s = 21.789\text{ m}$)**: $553$ particles ($5.6\%$ of losses) are intercepted at the narrow exit aperture.

All particle terminations produce clean `NaN` coordinates with zero unhandled memory faults or out-of-bounds indexing.

---

## 6. Regression Testing Suite

Automated regression tests have been added to [`tests/test_bts_lattice.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_bts_lattice.py):
- `test_matrix_and_particle_tracking_envelope_consistency`: Validates that tracked transverse beam covariance matches linear transfer matrix propagation within $3\%$ statistical tolerance.
- `test_physical_aperture_station_loss_accounting`: Validates that particles launched outside declared aperture limits are strictly stopped at the corresponding physical station.

All 11 tests in `tests/test_bts_lattice.py` pass cleanly in $< 1.0\text{ s}$.
