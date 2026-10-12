# Author Inputs, Provenance, and Boundary Verification

**Document Reference:** Task B02 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated and Audited against Author Codebase and Storage Ring Lattice.

---

## 1. Provenance of Boundary Twiss Parameters

A central requirement of Task B02 is to trace the precise mathematical and hardware origin of the boundary optical parameters used in the BTS matching study.

### 1.1 Entrance Boundary (BTS Start, $s = 0.0000\text{ m}$)

The initial Twiss and dispersion parameters at marker `m1` represent the extracted electron beam from the 4.0 GeV booster synchrotron:

$$\beta_{x,0} = 7.560000\text{ m}, \quad \alpha_{x,0} = +1.523100, \quad D_{x,0} = 0.276200\text{ m}, \quad D_{x,0}' = -0.065700\text{ rad}$$
$$\beta_{y,0} = 12.269000\text{ m}, \quad \alpha_{y,0} = -1.654700, \quad D_{y,0} = 0.000000\text{ m}, \quad D_{y,0}' = 0.000000\text{ rad}$$

- **Source:** Provided in original notebook `bts.ipynb` (Cell 29) and frozen as canonical single-source-of-truth constant `DEFAULT_BTS_ENTRANCE_TWISS` in [`src/nkm_injection/optics.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/optics.py).
- **Physical Verification:** These values reflect the optical state at the exit of the booster extraction septum, upstream of the BTS transfer line entry.

---

### 1.2 Target Exit Boundary (BTS Exit, $s = 21.7890\text{ m}$)

The matching target Twiss and dispersion parameters at marker `m4` are defined as:

$$\beta_{x,\text{target}} = 2.336495\text{ m}, \quad \alpha_{x,\text{target}} = -0.016335, \quad D_{x,\text{target}} = 0.080868\text{ m}, \quad D_{x,\text{target}}' = +0.047472\text{ rad}$$
$$\beta_{y,\text{target}} = 4.256241\text{ m}, \quad \alpha_{y,\text{target}} = +0.017772, \quad D_{y,\text{target}} = 0.000000\text{ m}, \quad D_{y,\text{target}}' = 0.000000\text{ rad}$$

- **Source:** Frozen in `DEFAULT_BTS_TARGET_TWISS` in [`src/nkm_injection/optics.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/optics.py) and [`src/nkm_injection/objectives.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/objectives.py).
- **Storage Ring Relation & Crucial Boundary Disclosure:**
  - In the companion storage ring study (`storage_ring.ipynb` and `K4GSR_HBIv4-1.mat`), the unperturbed periodic lattice functions in the long straight section (at marker `LH1` / insertion device straight) are:
    $$\beta_{x,\text{LH1}} \approx 15.939\text{ m}, \quad \beta_{y,\text{LH1}} \approx 4.445\text{ m}, \quad D_x \approx 0.00033\text{ m}$$
  - When the storage ring injection straight is modified to accommodate the Nonlinear Kicker Magnet (NKM) with upstream drift `NKMUPRING` ($L = 2.0\text{ m}$), magnet `NKM` ($L = 0.525\text{ m}$), and downstream drift `NKMDOWN` ($L = 0.175\text{ m}$), the circulating beam optics at the NKM center evaluate to:
    $$\beta_{x,\text{NKM}} \approx 16.202\text{ m}, \quad \beta_{y,\text{NKM}} \approx 5.347\text{ m}, \quad \alpha_{x,\text{NKM}} \approx -0.1285, \quad \alpha_{y,\text{NKM}} \approx -0.4505$$
  - **Non-Substitution Warning:** The BTS target optics $(\beta_x = 2.3365\text{ m}, \beta_y = 4.2562\text{ m})$ are **strictly defined at marker `m4`** (the exit of `sept_ex` at $s = 21.789\text{ m}$). **They are NOT the optics at the NKM magnet center.**
  - **Provenance:** The target values at `m4` correspond to the injected beam envelope required at the injection septum exit to achieve optimal beam clearance and phase-space orientation prior to the intervening drift into the storage ring vacuum chamber.
  - **Explicit Rule Compliance:** Manuscript text must never substitute NKM-center optics for the BTS exit boundary without accounting for the intervening injection geometry.

---

## 2. Verified Hardware Specifications vs Working Assumptions

To maintain strict scientific integrity, the following matrix categorizes all transfer line parameters into **Verified Hardware Specifications** versus **Working Modeling Assumptions**:

| Component / Parameter | Value | Category | Documentation / Justification |
| :--- | :--- | :--- | :--- |
| **Beam Energy** | $4.0\text{ GeV}$ | **Verified Spec** | Korea-4GSR design operating energy; magnetic rigidity $(B\rho) = 13.3426\text{ T}\cdot\text{m}$. |
| **Transfer Line Length** | $21.789\text{ m}$ | **Verified Spec** | Physical distance between booster extraction marker `m1` and injection septum exit `m4`. |
| **Dipole Bends & Angles** | `kext`: $7.5\text{ mrad}$<br>`sept_in`: $88.5\text{ mrad}$<br>`b1, b3`: $-111.701\text{ mrad}$<br>`b2`: $+176.0\text{ mrad}$<br>`sept_ex`: $88.5\text{ mrad}$ | **Verified Spec** | Fixed geometric deflection angles required to clear tunnel walls and match storage ring injection axis. |
| **Septum Edge Angles** | `sept_in` exit: $88.5\text{ mrad}$<br>`sept_ex` entrance: $88.5\text{ mrad}$ | **Verified Spec** | Parallel-face rectangular septum geometry. |
| **Quadrupole Physical Length** | $L_{\text{quad}} = 0.200\text{ m}$ | **Verified Spec** | Standard compact iron-dominated quadrupole core length. |
| **Quadrupole Drift Spacing** | $L_{\text{intra}} = 0.350\text{ m}$ | **Verified Spec** | Flange-to-flange mechanical clearance for BPMs, bellows, and vacuum pumps. |
| **Aperture Station Limits** | `ap_rect`: $\pm 19.35\text{ mm}$<br>`ap_rect2`: $\pm 30.00\text{ mm}$ | **Verified Spec** | Vacuum chamber internal dimensions across standard and dispersive sections. |
| **Quadrupole Strength Limits** | $|K_1| \le 4.5\text{ m}^{-2}$ ($G \le 60.0\text{ T/m}$) | **Working Assumption** | Maximum gradient achievable for $r_0 \approx 20\text{ mm}$ bore without iron saturation (to be justified in B03). |
| **Envelope Limit** | $\beta_{x,y} \le 60.0\text{ m}$ | **Working Assumption** | Imposed constraint in optimizer to ensure $\ge 3\sigma$ clearance for conservative beam sizes. |
| **Exit Optics Tolerances** | $\sigma_{\beta} = 0.05\text{ m}$<br>$\sigma_{\alpha} = 0.01$<br>$\sigma_{D} = 0.002\text{ m}$<br>$\sigma_{D'} = 0.001\text{ rad}$ | **Working Assumption** | Objective function weighting scales in SLSQP / least-squares optimizer. |

---

## 3. Boundary Coordinate System Conventions

1. **Longitudinal Coordinate $s$:**
   - Follows the curved design trajectory of a reference electron with $p_0 = 4.0\text{ GeV}/c$.
   - $s = 0$ is defined at marker `m1`.
   - $s = 21.7890\text{ m}$ is defined at marker `m4`.
2. **Transverse Deflections ($x, x'$):**
   - In pyAT and MAD-X conventions, a positive bending angle $\theta > 0$ denotes a deflection toward the inside of the bend.
   - Bending magnet signs: `sept_in` ($+0.0885\text{ rad}$) bends toward +x, `b1` ($-0.111701\text{ rad}$) bends toward -x, creating an achromatic double-bend chicane structure.
3. **Canonical Momentum Deviations:**
   - $x' \equiv p_x / p_0$, $y' \equiv p_y / p_0$, $\delta \equiv \Delta p / p_0$.
   - Dispersion vector: $\vec{D}(s) = \left[ D_x, D_x', D_y, D_y' \right]^T = \partial \vec{z} / \partial \delta$.

---

## 4. Unresolved Assumptions to be Addressed in B03–B04

1. **Booster Beam Emittance:** The historical study evaluated constraints using an assumed $10.89\text{ nm}\cdot\text{rad}$ (or $100/10\text{ nm}\cdot\text{rad}$) beam, whereas recent author documentation cites a $7.67\text{ nm}\cdot\text{rad}$ horizontal design beam. Task B03 must formally document both beams and isolate constraint justifications.
2. **Quadrupole Powering:** The canonical model treats all 9 quadrupoles (`q11` through `q33`) as independently powered. The feasibility of independent power supplies vs series-powered families will be verified against the singular value decomposition in Task B06.
