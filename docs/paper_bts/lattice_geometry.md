# BTS Transfer Line Geometry and Coordinate Systems

**Document Reference:** Task B02 Deliverable  
**Date:** 2026-10-13  
**Status:** Validated against canonical model `src/nkm_injection/bts_lattice.py` and pyAT 0.7.2.

---

## 1. Overview of the Canonical BTS Transfer Line

The Booster-to-Storage Ring (BTS) transfer line transports a $4.0\text{ GeV}$ electron beam from the extraction point of the booster synchrotron to the injection straight of the 4th-generation storage ring (Korea-4GSR).

The canonical model is implemented in [`src/nkm_injection/bts_lattice.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/bts_lattice.py) via `create_bts_lattice(config: BTSConfig)`.

### Key Parameters:
- **Design Beam Energy:** $E_0 = 4.0\text{ GeV}$ ($\gamma = 7827.8$, beam rigidity $(B\rho) \approx 13.34256\text{ T}\cdot\text{m}$)
- **Total Physical Length:** $L_{\text{total}} = 21.789000\text{ m}$
- **Element Count:** 36 elements (comprising 4 markers, 4 physical aperture stations, 6 dipoles/septa, 9 quadrupoles, and 13 drift spaces).
- **Quadrupole Layout:** 9 quadrupoles ($L = 0.200\text{ m}$ each) grouped into three triplets:
  - Triplet 1: `q11`, `q12`, `q13` (focusing, defocusing, focusing)
  - Triplet 2: `q21`, `q22`, `q23`
  - Triplet 3: `q31`, `q32`, `q33`
- **Dipole Magnets:** 6 bending elements:
  - `kext`: Booster extraction fast kicker ($L = 0.310\text{ m}$, $\theta = +7.500\text{ mrad}$)
  - `sept_in`: Booster extraction pulsed magnetic septum ($L = 1.000\text{ m}$, $\theta = +88.500\text{ mrad}$, exit face angle $e_2 = +88.500\text{ mrad}$)
  - `b1`: Transfer line dipole 1 ($L = 1.400\text{ m}$, $\theta = -111.701\text{ mrad}$)
  - `b2`: Transfer line dipole 2 ($L = 1.400\text{ m}$, $\theta = +176.000\text{ mrad}$)
  - `b3`: Transfer line dipole 3 ($L = 1.400\text{ m}$, $\theta = -111.701\text{ mrad}$)
  - `sept_ex`: Storage ring injection pulsed septum ($L = 1.000\text{ m}$, $\theta = +88.500\text{ mrad}$, entrance face angle $e_1 = +88.500\text{ mrad}$)
- **Net Horizontal Deflection:**
  $$\sum_{i} \theta_i = 0.0075 + 0.0885 - 0.111701 + 0.176000 - 0.111701 + 0.0885 = +0.137098\text{ rad} \approx 7.8552^\circ$$

---

## 2. Complete Sequence and Coordinate Table

All coordinates are referenced to the transfer line trajectory ($s$-axis), where $s = 0.0000\text{ m}$ corresponds to the upstream entrance marker `m1`.

| Index | Family Name | Element Type | Length $L$ [m] | $s_{\text{start}}$ [m] | $s_{\text{end}}$ [m] | Optical & Physical Parameters |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 0 | `m1` | Marker | 0.0000 | 0.0000 | 0.0000 | Entrance observation boundary ($s=0$) |
| 1 | `ap_rect` | Aperture | 0.0000 | 0.0000 | 0.0000 | Rectangular chamber: $x \in [-19.35, +19.35]\text{ mm}$, $y \in [-19.35, +19.35]\text{ mm}$ |
| 2 | `kext` | Dipole | 0.3100 | 0.0000 | 0.3100 | $\theta = +0.007500\text{ rad}$ ($+0.430^\circ$), $e_1 = 0$, $e_2 = 0$ |
| 3 | `sept_in` | Dipole | 1.0000 | 0.3100 | 1.3100 | $\theta = +0.088500\text{ rad}$ ($+5.071^\circ$), $e_1 = 0$, $e_2 = +0.088500\text{ rad}$ |
| 4 | `dr1` | Drift | 1.8450 | 1.3100 | 3.1550 | Inter-magnet drift |
| 5 | `q11` | Quadrupole | 0.2000 | 3.1550 | 3.3550 | Baseline $K_1 = +0.448572\text{ m}^{-2}$ (Matched $K_1 = -0.367525\text{ m}^{-2}$) |
| 6 | `dr_q11_12` | Drift | 0.3500 | 3.3550 | 3.7050 | Intra-triplet drift |
| 7 | `q12` | Quadrupole | 0.2000 | 3.7050 | 3.9050 | Baseline $K_1 = -1.026778\text{ m}^{-2}$ (Matched $K_1 = -1.216433\text{ m}^{-2}$) |
| 8 | `dr_q12_13` | Drift | 0.3500 | 3.9050 | 4.2550 | Intra-triplet drift |
| 9 | `q13` | Quadrupole | 0.2000 | 4.2550 | 4.4550 | Baseline $K_1 = +0.887640\text{ m}^{-2}$ (Matched $K_1 = +1.586072\text{ m}^{-2}$) |
| 10 | `dr2` | Drift | 2.3780 | 4.4550 | 6.8330 | Inter-section drift |
| 11 | `m2` | Marker | 0.0000 | 6.8330 | 6.8330 | Intermediate observation station 1 |
| 12 | `ap_rect2` | Aperture | 0.0000 | 6.8330 | 6.8330 | Expanded chamber: $x \in [-30.00, +30.00]\text{ mm}$, $y \in [-30.00, +30.00]\text{ mm}$ |
| 13 | `b1` | Dipole | 1.4000 | 6.8330 | 8.2330 | $\theta = -0.111701\text{ rad}$ ($-6.400^\circ$), $e_1 = 0$, $e_2 = 0$ |
| 14 | `dr3` | Drift | 1.5730 | 8.2330 | 9.8060 | Inter-section drift |
| 15 | `q21` | Quadrupole | 0.2000 | 9.8060 | 10.0060 | Baseline $K_1 = -1.066465\text{ m}^{-2}$ (Matched $K_1 = -1.068373\text{ m}^{-2}$) |
| 16 | `dr_q21_22` | Drift | 0.3500 | 10.0060 | 10.3560 | Intra-triplet drift |
| 17 | `q22` | Quadrupole | 0.2000 | 10.3560 | 10.5560 | Baseline $K_1 = +1.488384\text{ m}^{-2}$ (Matched $K_1 = +2.823108\text{ m}^{-2}$) |
| 18 | `dr_q22_23` | Drift | 0.3500 | 10.5560 | 10.9060 | Intra-triplet drift |
| 19 | `q23` | Quadrupole | 0.2000 | 10.9060 | 11.1060 | Baseline $K_1 = -0.669894\text{ m}^{-2}$ (Matched $K_1 = -2.490968\text{ m}^{-2}$) |
| 20 | `dr4` | Drift | 0.6550 | 11.1060 | 11.7610 | Drift before middle bend |
| 21 | `m3` | Marker | 0.0000 | 11.7610 | 11.7610 | Intermediate observation station 2 |
| 22 | `ap_rect2` | Aperture | 0.0000 | 11.7610 | 11.7610 | Expanded chamber: $x \in [-30.00, +30.00]\text{ mm}$, $y \in [-30.00, +30.00]\text{ mm}$ |
| 23 | `b2` | Dipole | 1.4000 | 11.7610 | 13.1610 | $\theta = +0.176000\text{ rad}$ ($+10.084^\circ$), $e_1 = 0$, $e_2 = 0$ |
| 24 | `dr4` | Drift | 0.6550 | 13.1610 | 13.8160 | Drift after middle bend |
| 25 | `q31` | Quadrupole | 0.2000 | 13.8160 | 14.0160 | Baseline $K_1 = +0.589886\text{ m}^{-2}$ (Matched $K_1 = +2.042678\text{ m}^{-2}$) |
| 26 | `dr_q31_32` | Drift | 0.3500 | 14.0160 | 14.3660 | Intra-triplet drift |
| 27 | `q32` | Quadrupole | 0.2000 | 14.3660 | 14.5660 | Baseline $K_1 = -1.168702\text{ m}^{-2}$ (Matched $K_1 = -1.434271\text{ m}^{-2}$) |
| 28 | `dr_q32_33` | Drift | 0.3500 | 14.5660 | 14.9160 | Intra-triplet drift |
| 29 | `q33` | Quadrupole | 0.2000 | 14.9160 | 15.1160 | Baseline $K_1 = +0.941655\text{ m}^{-2}$ (Matched $K_1 = +0.351115\text{ m}^{-2}$) |
| 30 | `dr3` | Drift | 1.5730 | 15.1160 | 16.6890 | Inter-section drift |
| 31 | `b3` | Dipole | 1.4000 | 16.6890 | 18.0890 | $\theta = -0.111701\text{ rad}$ ($-6.400^\circ$), $e_1 = 0$, $e_2 = 0$ |
| 32 | `dr5` | Drift | 2.7000 | 18.0890 | 20.7890 | Final drift to injection septum |
| 33 | `sept_ex` | Dipole | 1.0000 | 20.7890 | 21.7890 | $\theta = +0.088500\text{ rad}$ ($+5.071^\circ$), $e_1 = +0.088500\text{ rad}$, $e_2 = 0$ |
| 34 | `ap_rect` | Aperture | 0.0000 | 21.7890 | 21.7890 | Rectangular chamber: $x \in [-19.35, +19.35]\text{ mm}$, $y \in [-19.35, +19.35]\text{ mm}$ |
| 35 | `m4` | Marker | 0.0000 | 21.7890 | 21.7890 | Exit observation boundary ($s=21.789\text{ m}$) |

---

## 3. Physical Chamber Apertures and Station Placement

Two distinct vacuum chamber aperture sizes are declared across the line:
1. **Station 1 (End/Entrance Flanges):** `ap_rect` with half-gap limits $[-19.35, +19.35]\text{ mm}$ horizontally and vertically.
   - Located at $s = 0.0000\text{ m}$ (immediately after marker `m1`) and $s = 21.7890\text{ m}$ (immediately before marker `m4`).
2. **Station 2 (Internal Dispersive Arc Stations):** `ap_rect2` with expanded half-gap limits $[-30.00, +30.00]\text{ mm}$.
   - Located at $s = 6.8330\text{ m}$ (upstream of dipole `b1`) and $s = 11.7610\text{ m}$ (upstream of dipole `b2`).

> [!NOTE]
> Physical beam loss evaluation occurs at these discrete aperture locations during element-by-element particle tracking. In linear optics optimization, the mathematical constraint $\beta_{x,y} \le 60.0\text{ m}$ is imposed along the continuous envelope to guarantee adequate physical clearance inside the vacuum pipe.

---

## 4. Reconciliation of Historical MAD-X Sequence (`bts.madx`) vs Canonical Model

In historical project files, a legacy MAD-X input file [`bts.madx`](file:///home/cspark/Work/projects/nkm-injection/bts.madx) is present alongside the canonical Python/pyAT implementation. A careful comparative analysis confirms that **`bts.madx` is a non-equivalent, preliminary exploration sequence**:

| Property | Canonical Model (`src/nkm_injection/bts_lattice.py`) | Legacy Input (`bts.madx`) | Status / Reconciliation |
| :--- | :--- | :--- | :--- |
| **Total Length** | $21.789000\text{ m}$ | $38.122790\text{ m}$ | **Non-equivalent** ($+16.33\text{ m}$ longer in MAD-X) |
| **Quadrupole Count** | 9 quadrupoles (`q11`–`q33`, 3 triplets) | 10 quadrupoles (`Q11`–`Q34`, 4 in triplet 3) | **Non-equivalent** (MAD-X includes a 10th quad `Q34`) |
| **Bending Elements** | 6 dipoles (`kext`, `sept_in`, `b1`, `b2`, `b3`, `sept_ex`) | 8 bending magnets (`KEXT`, `BM1`, `SEPEXT` $\times 2$, `BTSBM` $\times 2$, `SEPSR`, `SEPSR2`) | **Non-equivalent** (Different bend layout and drift allocations) |
| **Apertures Defined** | 2 distinct stations ($\pm 19.35\text{ mm}$, $\pm 30.00\text{ mm}$) | Global marker `aperture=50` mm | **Non-equivalent** |
| **Tracking PassMethod** | Symplectic element integrators (`DriftPass`, `BndMPoleSymplectic4Pass`, `StrMPoleSymplectic4Pass`) | Thin/thick MAD-X element passes | Pass-method differences documented |

### Conclusion on Model Equivalence
The 21.789 m pyAT lattice represents the frozen, authoritative BTS model used in all recent journal optimization, tolerance, and tracking studies. The legacy file `bts.madx` represents an earlier concept that included extended drift sections and an extra quadrupole `Q34`. For all manuscript claims, the 21.789 m model is the sole physical line under study.

---

## 5. Visual Layout Asset

Figure 1 has been generated and validated:
- **PNG Asset:** [`docs/paper_bts/figures/fig1_bts_layout.png`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig1_bts_layout.png)
- **PDF Vector Asset:** [`docs/paper_bts/figures/fig1_bts_layout.pdf`](file:///home/cspark/Work/projects/nkm-injection/docs/paper_bts/figures/fig1_bts_layout.pdf)

The figure visualizes:
1. Magnet geometry diagram showing dipole blocks (blue), focusing quadrupoles (orange), defocusing quadrupoles (purple), and aperture stations (dashed lines).
2. Transverse betatron functions $\beta_x(s)$ and $\beta_y(s)$ comparing baseline and matched solutions against the $\beta_{\max} \le 60\text{ m}$ envelope constraint and target markers.
3. Horizontal dispersion function $D_x(s)$ along the line.
