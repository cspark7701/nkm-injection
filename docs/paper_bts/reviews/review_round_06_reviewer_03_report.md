# Referee Report — Reviewer 3, Sixth Round (NIM A Submission)

**Manuscript Title:** *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Nuclear Instruments and Methods in Physics Research Section A (NIM A)*  
**Version Reviewed:** Current NIM A Elsevier layout at commit `fd16b2a` / latest `main` (`docs/paper_bts/paper.tex`, `paper.pdf` [19-page article], `supplement.tex`, `supplement.pdf` [10 pages], and `paper.bib`).  
**Reviewer Role:** Reviewer 3 (Senior Accelerator Physicist, specialist in transfer-line beam transport, optical matching, injection septa, beam loss mechanisms, trajectory steering, and statistical error modeling).  
**Date:** November 1, 2026.  

---

## 1. Executive Recommendation

**Recommendation: Accept for Publication.**  
*The manuscript is scientifically rigorous, mature, and ready for publication in Nuclear Instruments and Methods in Physics Research A (NIM A). No further simulations, tracking reruns, or mandatory revisions are requested.*

Over six successive rounds of review, the author has conducted an exemplary, intellectually honest, and deep dialogue with the referees. What began as a conventional optics-matching exercise has been systematically reshaped into a sophisticated, well-bounded investigation of transfer-line beam delivery, horizontal phase-advance jitter partitioning, and physical beam loss at the injection septum blade.

The paper makes several clear, permanent contributions to accelerator physics and transfer-line engineering:
1. **The Blade Clearance Boundary:** It demonstrates that matching fixed boundary Twiss parameters analytically determines the nominal beam size at the limiting injection-septum blade, so lowering intermediate peak beta functions provides negligible clearance buffer where beam loss actually occurs.
2. **Phase-Advance Jitter Partitioning:** In an uncoupled, dispersion-matched transfer line, the horizontal phase advance $\mu_x$ acts as the decisive physical knob partitioning incoming booster jitter between spatial excursion and angular deflection at the septum blade.
3. **The Dispersion-Slope Boundary:** Within local gradient searches, the inherited non-zero dispersion slope target ($D'_x = 0.0475$) sets a physical lower bound on the accessible horizontal phase advance ($\mu_x \ge 0.69 \times 2\pi$), directly constraining the achievable loss reduction.
4. **Decoupling of Jitter and Static Regimes:** A sharp distinction is established between the stress-level jitter regime (where phase advance governs blade scraping) and the realistic low-jitter regime (where blade losses are negligible and beam delivery is dominated by static dipole steering residuals and uncorrected vertical orbit).

The numerical and statistical evidence is presented with complete transparency: comparisons use controlled shared-reading errors on independent machines, the linearized Gaussian surrogate is rigorously benchmarked against 1.2 million tracked particles, and discrepancies (such as the localized excess in Shot 2 of Machine 116) are honestly identified rather than smoothed away.

---

## 2. In-Depth Audit of Author Responses Across Rounds 1–6

As Reviewer 3 joining in Round 6, I have audited all historical and main-branch author response documents (Rounds 1–5, the restored branch responses, and the round-7 implementation response), tracking how every major referee objection was addressed:

### Rounds 1 & 2: Shift from Abstract Betas to Physical Apertures and Blade Restrictions
- **Initial Flaw Identified:** Early drafts emphasized peak beta reduction ($\beta_{y,\max} = 50.75\text{ m} \to 36.12\text{ m}$) as a proxy for clearance across four arbitrary stations, ignoring the true aperture geometry and the septum blade.
- **Reviewer Critique:** Reviewer 2 showed that because boundary optics are clamped to match the booster and storage ring, nominal beam envelopes at the exit septum blade are analytically invariant to quadrupole rematching. Furthermore, quadrupole bore restrictions and the thin septum blade (1.5 mm clearance) were missing.
- **Author's Action:** The author rebuilt the model around element-wise physical apertures, explicitly modeled the 1 mm septum blade at $x_{\mathrm{blade}} \approx -18.0\text{ mm}$, moved the four-station study to the supplement, and implemented trajectory steering using horizontal field trims of the three existing dipoles.

### Round 3: Phase Advance Discovery and Booster Jitter Dominance
- **Key Physics Uncovered:** Tracking revealed that beam loss at the septum blade was heavily driven by incoming booster jitter ($0.5\text{ mm}$ position, $0.2\text{ mrad}$ angle). By analyzing the transfer matrix, the author showed that the spatial beam jitter $\sigma_x(s_{\mathrm{sept}})$ scales directly with the horizontal phase advance $\mu_x$.
- **Reviewer Critique:** Reviewer 1 and Reviewer 2 noted that the reachable lower edge of $\mu_x$ was restricted by local search limits, and that baseline-vs-optimized comparisons were circular since the baseline was unmatched.
- **Author's Action:** The author demoted the baseline to an illustrative starting point, executed a comprehensive phase-advance scan across the feasible matching space, proved that the non-zero dispersion slope $D'_x$ acts as the active constraint preventing lower $\mu_x$, and formulated a fast linearized Gaussian loss surrogate validated by tracking.

### Round 4: Shared-Reading Noise and Residual Error Decomposition
- **Reviewer Critique:** Reviewer 2 discovered that comparisons between optical settings had drawn independent random monitor noise per setting, confounding the low-beta contrast. Both reviewers also demanded that static steering residuals and uncorrected vertical errors be separated from dynamic jitter.
- **Author's Action:** The author executed an independent 200-machine, 3-shot, 2000-particle validation campaign using frozen, shared reading error draws across all settings (Table 5). This definitively showed that the true low-beta gain over matched reference is $-0.13$ percentage points ($95\%\text{ CI: } [-0.24, -0.04]$), while the loss-based phase-edge setting achieves a factor-of-4.48 reduction in jitter-integrated loss. Furthermore, the author demonstrated that at realistic low jitter, blade losses vanish and beam delivery is dominated by the $0.18\text{ mrad}$ dipole trim residual and $1.1\text{ mm}$ uncorrected vertical orbit.

### Rounds 5 & 6: Probability Bounds, Loss Localization, and NIM A Conversion
- **Reviewer Critique:** Reviewer 2 noted that Section 3.3's probability bracket was stated as a strict bound on sampled particle counts, and requested localization of the discrepancy between predicted (880.5) and observed (942) lost particles.
- **Author's Action:** The author clarified that the probability bracket applies strictly within the linearized Gaussian event model; identified that 16 loss-bearing shots occurred (correcting Reviewer 2's count of 20); showed that Machine 116, Shot 2 accounts for $\approx 70\%$ of the excess (454 observed vs 410.9 expected); converted the manuscript cleanly to the Elsevier `elsarticle` format for NIM A; and trimmed the text to 19 pages.

---

## 3. Detailed Technical Review of Core Physics

### 3.1. Phase-Advance Jitter Partitioning
In an uncoupled beamline matched between declared Twiss boundaries $(\beta_0, \alpha_0)$ and $(\beta_1, \alpha_1)$, the linear transfer matrix elements between line entrance ($s=0$) and the injection septum ($s=L$) are:
$$
R_{11} = \sqrt{\frac{\beta_1}{\beta_0}} \left(\cos\mu_x + \alpha_0 \sin\mu_x\right), \qquad R_{12} = \sqrt{\beta_1 \beta_0} \sin\mu_x.
$$
The horizontal position of a particle at the septum exit is:
$$
x_1 = R_{11} x_{\mathrm{jit}} + R_{12} x'_{\mathrm{jit}} + \eta_{x,1} \delta.
$$
Because the beam envelope $\sqrt{\beta_1 \varepsilon_x}$ is fixed by the storage-ring injection target, the only degree of freedom available to accelerator operators to minimize the spatial excursion at the blade is the horizontal phase advance $\mu_x$. Lowering $\mu_x$ drives $R_{12} \to 0$ and reduces spatial variance $\langle x_1^2 \rangle$, shifting the jitter into the angular coordinate $x'_1$. 

The author's loss-based setting operates at the lower accessible boundary ($\mu_x \approx 0.69 \times 2\pi$), shrinking spatial jitter at the septum blade at the expense of an increase in angular jitter. This trade-off is quantified with extreme precision.

### 3.2. Active Constraint of the Inherited Dispersion Slope
A key insight of the paper is why the optimizer cannot push $\mu_x$ arbitrarily lower. The BTS line inherits a storage-ring injection target with non-zero dispersion slope: $D'_{x,\mathrm{target}} = +0.0475$. In a three-dipole geometry with nine quadrupoles, simultaneously satisfying:
$$
D_x(L) = 0.0809\text{ m}, \qquad D'_x(L) = 0.0475
$$
alongside the four transverse Twiss parameters forces the intermediate dispersion trajectory to peak, locking the quadrupole strengths into a regime where $\mu_x$ cannot drop below $\approx 0.69 \times 2\pi$ without violating quadrupole gradient limits ($|K| \le 3.0\text{ m}^{-2}$). When the author tested a hypothetical dispersion-free target ($D_x = 0, D'_x = 0$), the accessible phase advance dropped further to $0.63 \times 2\pi$, reducing blade loss by an additional order of magnitude. This is an elegant demonstration of how ring lattice choices constrain transfer-line robustness.

### 3.3. Independent Shared-Reading Benchmark (Table 5)
Table 5 represents the gold standard of simulation reporting. By evaluating 200 independently generated transfer lines under raw static errors ($100\ \mu\text{m}$ misalignments, $0.5\text{ mrad}$ rolls, $10^{-3}$ gradient errors) corrected with existing dipole trims, and holding monitor reading errors ($100\ \mu\text{m}$ BPM noise) fixed across designs, the author achieves clean, unconfounded contrasts:
- **Nominal Matched Reference:** 11,673 particles lost ($0.97\%$ mean loss rate).
- **Low-Beta Design:** 10,104 particles lost ($0.84\%$ mean loss rate). Paired contrast: $-0.13$ percentage points ($95\%\text{ CI: } [-0.24, -0.04]$).
- **Loss-Based Phase-Edge Setting:** 942 particles lost ($0.08\%$ mean loss rate). Paired contrast: $-0.89$ percentage points ($95\%\text{ CI: } [-1.20, -0.58]$).

This establishes that peak beta reduction produces only a minor clearance benefit, whereas optimizing the phase advance provides a massive 4.48-fold reduction in beam loss.

### 3.4. Tracking Discrepancy Localization & Surrogate Limits
The tracking-to-surrogate comparison (942 tracked vs 880.5 expected) is handled with exemplary integrity. Rather than smoothing over the 61.5-particle excess, the author localized it to 16 loss-bearing shots. In particular, Machine 116, Shot 2 contributed 454 observed losses against 410.9 expected. In that specific realization, the static orbit and shot jitter placed the beam centroid exceptionally close to the physical septum blade ($< 1\sigma_x$), where non-Gaussian tail truncation and finite chromatic kicks produce higher scraping than the linear Gaussian integral. The author properly leaves this mechanism open as a topic for future nonlinear-moment studies, perfectly suited for an applied methods paper.

### 3.5. Separation of Operating Regimes
The discussion in Section 5 and Section 6 provides vital clarity for facility commissioning:
- **Stress-Jitter Regime ($1\times$ budget: $0.5\text{ mm} / 0.2\text{ mrad}$):** Booster jitter dominates; $\mu_x$ phase advance is the primary operational tuning knob to prevent blade scraping.
- **Realistic Jitter Regime ($0.1\times$--$0.2\times$ budget):** Blade losses drop to zero across all matched settings; beam delivery is dominated entirely by static dipole steering residuals ($\approx 0.18\text{ mrad}$) and the uncorrected vertical centroid ($\approx 1.1\text{ mm}$). Because the modeled line has no vertical steerers, vertical trajectory correction must be prioritized during actual machine installation.

---

## 4. Minor Editorial & Camera-Ready Polish Items

The manuscript is acceptable as it stands. To aid the author during final proof preparation for NIM A, I provide five optional, non-blocking suggestions:

1. **Section 4.2 Opening Harmonization (Harmonizing with Reviewer 2):**  
   The opening paragraph of Section 4.2 still refers to the earlier per-setting reading comparison (1.47% for low-beta) before introducing the confounding caveat. Citing Table 4 directly for the matched-reference numbers and placing the 1.47% figure immediately adjacent to its caveat will streamline reader comprehension.
2. **Abstract Conciseness:**  
   The current abstract is approximately 300 words. NIM A guidelines typically favor abstracts between 150 and 250 words. Moving secondary descriptive clauses (such as the 3-bend/9-quadrupole element count or repetitive interval scope definitions) to the Introduction would bring the abstract into ideal journal range.
3. **Machine 116 Shot 2 Physical Context:**  
   In Section 3.3, a brief one-sentence note stating that the 43-particle excess in Shot 2 of Machine 116 arises from a centroid grazing the physical blade within $\sim 1\sigma_x$ would give readers immediate physical intuition for the surrogate underestimation.
4. **Cross-Paper Rationale for Dipole Field Errors:**  
   Briefly state in Section 2.1 that the independent dipole field errors assumed in this study contrast with the series-powered common dipole error in the companion NKM paper (`ParkNKM2026`), directly closing the cross-paper question.
5. **Final Submission Readiness (Gate G7):**  
   Confirm author declarations, repository URLs, and submission bundle integrity prior to Elsevier portal upload.

---

## 5. Conclusion

This paper provides an authoritative, mathematically rigorous, and physically transparent blueprint for transfer-line matching and injection blade clearance in next-generation light sources. 

I enthusiastically recommend **Acceptance for Publication in NIM A**.
