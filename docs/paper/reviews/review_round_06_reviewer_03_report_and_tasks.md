# Referee Report — Reviewer 3, Sixth Round

**Manuscript Title:** *Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design lattice*  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Physical Review Accelerators and Beams (PRAB)*  
**Version Reviewed:** PRAB REVTeX draft at commits `2c813fe` / `a6949f0` (`docs/paper/paper.tex`, `paper.pdf` [36-page preprint], `paper_twocolumn.pdf` [18-page layout], `supplement.pdf` [7 pages], and `revision_manifest_round5.json`).  
**Reviewer Role:** Reviewer 3 (Senior Accelerator Physicist, specialist in storage-ring injection systems, pulsed multipole magnets, non-linear tracking, and accelerator error/tolerance modeling).  
**Date:** November 1, 2026.  

---

## 1. Executive Recommendation

**Recommendation: Accept for Publication.**  
*The manuscript is scientifically sound, meticulously executed, and ready for publication in Physical Review Accelerators and Beams. No additional simulations, tracking campaigns, or mandatory revisions are requested.*

Over five successive rounds of peer review, the author has systematically addressed every major and minor critique raised by Reviewers 1 and 2. What began as a conventional tracking study relying on a standard thin kick map has evolved into an exceptionally thorough, methodologically transparent, and physically grounded investigation. The paper provides an invaluable contribution to the accelerator community by clearly explaining:
1. Why thin kick maps fundamentally misrepresent long, strongly self-deflecting nonlinear kickers;
2. How uncorrected vertical centroid offsets from transfer-line errors couple catastrophically with the steep transverse kick gradient;
3. Why the nonlinear kicker (NKM) suffers severe sensitivity to booster jitter even under ideal vertical trajectory correction; and
4. How realistic chamber geometry, non-linear lattice dynamic aperture, and stored-beam perturbation jointly constrain injection system feasibility.

The negative results reported—specifically that the NKM achieves only 16.1% mean capture under baseline horizontal-only steering (against 44.1% for a uniform kick), and that no nonzero tested jitter level passes a 1-point noninferiority margin—are stated with total clarity and rigorous statistical conditioning. This level of scientific integrity is exemplary.

Below, I provide a detailed audit of the author responses across all five rounds, a comprehensive evaluation of the core physics, and an actionable checklist of optional, camera-ready presentation refinements.

---

## 2. Comprehensive Audit of Author Responses Across Rounds 1–5

As Reviewer 3 joining in Round 6, I have thoroughly read all five author response letters, the associated review reports, the completed revision registers (C1–C12, D1–D15, E1–E11, F1–F9, G1–G7), and the underlying evidence manifests. The evolution of the paper reflects exemplary responsiveness to peer review:

### Round 1: Model Overhaul and Physical Field Consistency
- **Initial Flaw Identified:** The original manuscript relied on a 2D thin kick map from RADIA (`kickmap_file.txt`) and reported conflicting results between thin-map and thick-model tracking, without auditing field conventions.
- **Author's Decisive Action:** The author implemented an exact Biot–Savart field solver for the four filament loops (`wire_field.py`), validated straight-line field integrals against RADIA to $7 \times 10^{-12}\text{ rad}$, and discovered a critical curl-free sign defect in the tabulated kick map: the tabulated vertical kick was $+\int B_x / B\rho$, whereas the physical Lorentz deflection is $-\int B_x / B\rho$.
- **Outcome:** The author transitioned the entire tracking suite to a 640-slice 3D vector integrator in Accelerator Toolbox, retracted artificially optimistic claims, and renamed the manuscript to reflect finite-length and vertical effects.

### Round 2: Design Beam, Real Chamber, and Ring Error Ensembles
- **Reviewer Critiques:** Over-reliance on an idealized 100 nm historical beam without an actual vacuum chamber; lack of realistic ring misalignments; unverified numerical integration.
- **Author's Decisive Action:**
  1. Switched all primary evaluations to the official KLS design beam ($\varepsilon_x = 7.67\text{ nm}\cdot\text{rad}$, 10% coupling, $\varepsilon_y = 0.767\text{ nm}\cdot\text{rad}$, $\sigma_\delta = 0.0008$).
  2. Integrated the official vacuum chamber profile across the ring, specifically introducing a flat $16 \times 3.8\text{ mm}$ inner chamber inside the NKM.
  3. Generated an ensemble of ten realistic corrected rings (seeds 5501–5510) featuring closed-orbit correction, Gauss–Newton beta-beat/dispersion correction, and tune matching.
  4. Performed independent integration verification against an adaptive DOP853 Runge–Kutta solver, confirming slice and span errors stay $< 10^{-11}\text{ rad}$.

### Round 3: Positioning, Empirical Sagitta Scaling, and Operating Point
- **Reviewer Critiques:** Overlapping claims with Sun *et al.* (ALS 8-conductor kicker); unvalidated general scaling; operating point chosen without corrected-ring physics.
- **Author's Decisive Action:**
  1. Properly credited Sun *et al.* (PRAB 2020) for segmented drift-kick-drift tracking and clarified that the novelty lies in quantifying thin-map breakdown in an angle-canceling geometry with large sagitta ($0.32\text{ mm}$, vs ALS's $\sim 0.04\text{ mm}$).
  2. Formulated the empirical sagitta-to-width scaling law ($\Delta\theta_x / |K| \propto \eta^{1.46}$) over 30 configurations across two wire families with 3.4% log-rms scatter.
  3. Re-selected the operating point on the corrected rings ($x_{\mathrm{inj}} = -19.48\text{ mm}, S=0.95$), defining explicit 500-turn and 4000-turn survival boundaries.

### Round 4: Paired Ablation, Causal Attribution, and Steering Decoupling
- **Reviewer Critiques:** Reviewer 2 demonstrated that the ~28-point gap between NKM and uniform kick persisted at zero jitter, disproving the author's previous assertion that booster angle jitter was the primary cause of capture loss.
- **Author's Decisive Action:**
  1. Executed a rigorous 7-class paired ablation study over 15 ensembles with frozen noise streams.
  2. Identified the true physical root cause: transfer-line magnet errors left an uncorrected $0.90\text{ mm}$ vertical centroid offset and $77\ \mu\text{rad}$ angle offset at the septum exit under the baseline horizontal-only steering.
  3. Formulated an ideal two-plane steering benchmark, proving that removing this vertical offset dramatically elevates zero-jitter NKM capture from 40.1% to 76.6%.
  4. Mapped individual particle loss locations, demonstrating that 99.4% of losses occur on turn 1 in the vertical plane around the ring, with zero losses inside the magnet bore itself.

### Round 5: Dual Headlines, Paired Jitter Scan, and Companion Audit
- **Reviewer Critiques:** Headlines required clear labeling under both steering scenarios; the jitter tolerance boundary required a formal paired scan; cross-paper discrepancies with the BTS transfer-line companion paper needed resolution.
- **Author's Decisive Action:**
  1. Rewrote the abstract and conclusions to feature both figures: 16.1% vs 44.1% under baseline horizontal-only steering, and 33.9% vs 57.2% under full-jitter two-plane steering (76.6% zero-jitter baseline).
  2. Pre-declared and executed a 5-level paired two-plane jitter scan ($0, 0.1, 0.25, 0.5, 1.0$), establishing that even at 0.1 jitter, the NKM suffers a statistically resolved loss of $-2.35$ percentage points ($95\%\text{ CI: } [-4.32, -0.66]$), failing the declared 1-point noninferiority margin.
  3. Audited the companion BTS paper, discovering and documenting that the BTS study assumed independent dipole field errors per bend, whereas the NKM study used a common series-powered dipole error, alongside differing population estimators (population standard deviation vs rms analytic centroid).

---

## 3. Detailed Technical Review of Current Manuscript

### 3.1. Physical Field Modeling and Trajectory Slicing
The 0.525 m four-conductor NKM model is mathematically sound. In this geometry, incoming particles at $x_{\mathrm{inj}} = -19.48\text{ mm}$ arrive with a $-4.85\text{ mrad}$ angle and are kicked by $+4.85\text{ mrad}$ to emerge parallel to the stored beam. The trajectory sagitta inside the magnet is:
$$
\Delta x_{\mathrm{sag}} \approx \frac{1}{8} L_{\mathrm{mag}} \Delta\theta_x \approx \frac{1}{8} (0.525\text{ m}) (4.85\text{ mrad}) \approx 0.318\text{ mm}.
$$
Because the horizontal kick profile $B_y(x)$ possesses a steep curvature (kick-lobe half-width $w \approx 9.3\text{ mm}$), evaluating the entire kick at the center chord ($s = L/2$) introduces a systematic angle error of $161\ \mu\text{rad}$ ($3.7\times$ the author's declared $0.044\text{ mrad}$ allowance). The 640-slice drift–kick–drift segmentation resolves this sagitta completely, reducing integration error to $< 10^{-7}\text{ rad}$. The curl-free verification, adaptive DOP853 solver cross-checks (Table S1), and the empirical $\eta^{1.46}$ scaling across both wire geometries place the tracking methodology on unimpeachable footing.

### 3.2. Mechanism of Vertical Deficit: The Off-Axis Kick Gradient
The central accelerator physics insight of this paper is the mechanism governing the NKM-specific loss. From Maxwell's equations ($\nabla \times \mathbf{B} = 0$), the transverse kick derivatives satisfy:
$$
\frac{\partial K_y}{\partial y} = -\frac{\partial K_x}{\partial x}.
$$
Near the injection operating point ($x \approx -19.5\text{ mm}$), the magnet operates on the steep inward slope of the kick lobe, where $\partial K_x / \partial x \approx -0.32\text{ mrad/mm}$, which dictates:
$$
\frac{\partial K_y}{\partial y} \approx +0.32\text{ mrad/mm}.
$$
Consequently, an incoming vertical centroid displacement $\Delta y$ receives a strong net vertical kick $\Delta y' \approx (+0.32\text{ mrad/mm}) \Delta y$. In contrast, an ideal uniform dipole kicker has $\partial K_x / \partial x \equiv 0$, imparting zero vertical kick regardless of vertical position. 

In the baseline BTS transfer line, no vertical steering correction was included. Uncorrected quadrupole misalignments ($100\ \mu\text{m}$) and rolls ($0.5\text{ mrad}$) produce an exit vertical centroid distribution with $\sigma_y = 0.90\text{ mm}$ and $\sigma_{y'} = 77\ \mu\text{rad}$. For an NKM, a $0.90\text{ mm}$ offset generates an unexpected vertical deflection of $\approx 0.29\text{ mrad}$. When injected into a low-emittance storage ring where the vertical angular acceptance is merely $\approx 0.44\text{ mrad}$, this deflection induces severe vertical betatron oscillations, driving 99.4% of particles into the vacuum chamber on turn 1. This fully explains why the NKM captures only 16.1% under baseline conditions while the uniform kick achieves 44.1%.

### 3.3. Two-Plane Jitter Stress Scan and Noninferiority Inference
Section V.B and Table VII present a textbook application of noninferiority testing in computational accelerator physics. By fixing all machine errors, particle seeds, and ring draws, the author evaluated five scaled levels of booster jitter ($0, 0.1, 0.25, 0.5, 1.0\times$) under ideal two-plane steering.

The paired bootstrap results (10,000 resamples, seed 1729) demonstrate:
- At Scale 0.0 (Zero Jitter): NKM = 76.57%, Uniform = 82.64% (Gap = $-6.07$ points).
- At Scale 0.1: NKM = 74.22%, Uniform = 82.86% (NKM change = $-2.35$ points, $95\%\text{ CI: } [-4.32, -0.66]$).
- At Scale 0.25: NKM = 65.25%, Uniform = 80.99% (NKM change = $-11.32$ points, $95\%\text{ CI: } [-16.55, -6.58]$).
- At Scale 1.0: NKM = 33.91%, Uniform = 57.22% (NKM change = $-42.66$ points, $95\%\text{ CI: } [-51.39, -33.84]$).

Under the pre-declared rule (lower bound of 95% CI must be $>-1.0$ percentage point), even 10% of the nominal jitter fails noninferiority. Crucially, the author resists the temptation to over-claim: the text explicitly emphasizes that this does not prove a continuous failure threshold, nor does it establish a hardware tolerance below 0.1. It stands as a robust, verified negative result: **ideal static two-plane correction recovers zero-jitter capture, but does not shield the NKM from dynamic shot-to-shot jitter**.

### 3.4. Vacuum Chamber Boundaries and Ring Acceptance
The author properly accounted for real-world physical aperture limits:
- Chamber profile includes the $16 \times 3.8\text{ mm}$ flat chamber inside the NKM and narrow in-vacuum undulator (IVU) gaps.
- Multi-turn tracking on corrected ring 5501 revealed that opening the internal magnet chamber from $3.8\text{ mm}$ to $15\text{ mm}$ only increases capture from 29.8% to 33.2%. This elegantly proves that particle loss is not simply a matter of localized chamber clipping inside the magnet bore; rather, it is driven by global phase-space excursion and uncorrected coupling resonances in the storage ring.

### 3.5. Stored Beam Transparency and Pulse Constraints
In Section VI, the author demonstrates that single-wire positioning errors of $10\ \mu\text{m}$ produce on-axis dipole kicks displacing the stored beam by several rms beam sizes ($\sigma_x$), exceeding the standard $0.1\sigma_x$ transparency threshold. Consequently, active feedforward compensation (such as auxiliary trim coils) is mandatory. The temporal analysis of the half-sine current pulse confirms that to avoid perturbing circulating bunches on subsequent turns ($T_0 = 2.67\ \mu\text{s}$), the pulse duration must satisfy $\tau \le 5.33\ \mu\text{s}$. The eddy current shielding times for ceramic chambers with thin titanium coatings ($\approx 46\text{ ns}$) are shown to be fully compatible with this pulse length.

---

## 4. Minor Editorial & Camera-Ready Polish Items

The manuscript is ready for publication as is. However, to maximize presentation clarity and reader convenience, I have cataloged four minor, optional copyediting suggestions:

1. **Table VII Loss-Test Column Label (Harmonization with Reviewer 1):**  
   In Table VII, the decision column currently labels Scale 0.1 as `fail`. As Reviewer 1 pointed out, the paired difference is $-2.35$ with 95% CI $[-4.32, -0.66]$. Because the interval crosses the $-1.0$ point boundary, the formal statistical outcome is *failure to establish noninferiority* (inconclusive / not established), rather than proving that true loss exceeds 1 point with 97.5% confidence. Changing `fail` to `not established` (or adding a brief footnote clarifying the noninferiority convention) would improve statistical precision.

2. **Table I Standalone Row Label (Harmonization with Reviewer 1):**  
   In Table I (bottom subtable), the row `This study` quotes `16.1% mean under the assumed joint errors`. A reader examining Table I in isolation might not realize that this 16.1% corresponds specifically to the 150-realization ensemble with *horizontal-only* steering. Adding `(horizontal-only steering)` locally in Table I prevents any misinterpretation.

3. **Explicit Mechanism at Small Jitter in Abstract/Text (Harmonization with Reviewer 2):**  
   At 0.1 jitter, the NKM loses 2.35 points while the uniform kick loses nothing (+0.22 points). Briefly mentioning in the text that this initial sensitivity is directly governed by the local kick gradient $\partial K_x / \partial x \approx -0.32\text{ mrad/mm}$ acting on centroid jitter within the narrow $0.44\text{ mrad}$ angular acceptance window provides clear physical intuition.

4. **Dipole Error Correlation Context (Harmonization with Reviewer 2):**  
   In Section V.A, the author notes that the NKM study assumes a common relative dipole field error across all BTS bends, whereas the companion BTS study uses independent draws. Briefly noting that a common error represents series-powered dipole strings in a real transfer line provides helpful engineering context.

---

## 5. Reviewer 3 Revision Tasks Checklist

All tasks in this register are **strictly optional editorial refinements**. None condition the acceptance of the manuscript.

- [ ] **Task R3-1 — Table VII Decision Labeling (Optional)**
  - [ ] Update the `Loss test` column in Table VII (or footnote) to clarify that `fail` at scale 0.1 denotes failure to demonstrate noninferiority at the 1-point margin, rather than a proven catastrophic loss.
- [ ] **Task R3-2 — Table I Local Population Label (Optional)**
  - [ ] Add `(150 draws, horizontal-only steering)` to the `This study` capture cell in Table I.
- [ ] **Task R3-3 — Physical Intuition at Small Jitter (Optional)**
  - [ ] Add a brief sentence in Section V.B connecting the 2.3-point NKM loss at 0.1 jitter to the local transverse gradient $\partial K_x/\partial x = -0.32\text{ mrad/mm}$ and the $0.44\text{ mrad}$ angular acceptance window.
- [ ] **Task R3-4 — Series Dipole Rationale (Optional)**
  - [ ] Briefly state in Section V.A that common dipole field errors correspond physically to series-powered bending dipoles.
- [ ] **Task R3-5 — Final Pre-Submission Gate G7 Verification**
  - [ ] Confirm author approval, data availability declarations, and repository/archive readiness prior to formal journal upload.

---

## 6. Concluding Remarks

The author and the research team have performed a monumental service to accelerator physics through this paper. By rigorously dismantling the assumptions behind thin-kick-map models and confronting the harsh realities of vertical orbit errors, beam jitter, and 3D fringe fields, this work will prevent costly design oversights in future diffraction-limited storage rings.

I enthusiastically recommend **Acceptance for Publication in Physical Review Accelerators and Beams**.
