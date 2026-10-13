# Peer Review Report 02: In-Depth Scientific & Journal Editorial Assessment

**Manuscript Title:** Constrained Optical Matching, Error Sensitivity, and Transmission Robustness of a Booster-to-Storage-Ring Transfer Line  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Date of Review:** October 13, 2026  
**Review Round:** Round 2 (Independent Deep Scientific Assessment)  
**Reviewer Recommendation:** **Accept with Minor Editorial & Clarification Adjustments**

---

## 1. Executive Summary & Review Overview

Following the initial round of revisions where essential physical context regarding continuous vacuum chamber dimensions, Courant–Snyder citations, uncorrected trajectory steering assumptions, and chromaticity effects were added, this second review assesses the manuscript's overall scientific depth, numerical precision, figure clarity, journal alignment, and potential publication vulnerabilities.

### Evaluation Scorecard:
- **Scientific Originality & Contribution:** **Very Strong** (demonstrates that mathematical optimizer convergence does not imply physical feasibility; discovers a low-$\beta$ margin design with 16.47 m envelope stay-clear gain; clarifies Jacobian conditioning with a dimensionless formulation; establishes an extreme-scale $N = 550,000$ tail failure bound).
- **Technical Rigor & Methodology:** **Excellent** (symplectic tracking errors $< 10^{-14}$, 6D multi-particle phase-space transport matching matrix propagation within 0.4%, exact Clopper–Pearson binomial intervals for tail failures).
- **Presentation, Structure & Clarity:** **Strong** (12-page comprehensive structure, high-resolution vector figures, clear equations).
- **Completeness & Reproducibility:** **Exceptional** (machine-readable cryptographic SHA-256 provenance records, automated test suites passing 100%).

**Final Recommendation:** **Accept with Minor Editorial & Clarification Adjustments**. Below are the specific points that will elevate the paper to highest publication standards.

---

## 2. In-Depth Scientific Analysis & Discussion Points

### Point 1: Physical Mechanism of the 3-Mode Null Space (Section 4.2)
- **Observation:** The manuscript demonstrates that the dimensionless Jacobian $\tilde{J} \in \mathbb{R}^{6 \times 9}$ has rank 6, resulting in a 3-dimensional null space ($\sigma_7 = \sigma_8 = \sigma_9 = 0$). The text astutely notes that this null space allows internal envelope optimization without perturbing exit boundary matching.
- **Reviewer Insight:** Which specific quadrupole families form the dominant basis of this null space? In a three-triplet system ($\mathrm{q11}$--$\mathrm{q13}$, $\mathrm{q21}$--$\mathrm{q23}$, $\mathrm{q31}$--$\mathrm{q33}$), triplet 2 in the dispersive region and symmetric counter-trimming between triplet 1 and triplet 3 typically provide the internal betatron phase advance shifts.
- **Recommendation:** Add a concise sentence in Section 4.2 detailing the physical composition of the null-space modes (e.g., opposing trims between triplets 1 and 3, or internal triplet-2 waist adjustments) to provide actionable accelerator commissioning guidance.

### Point 2: Quadrupole Power Dissipation & Hardware Cost Comparison (Table 2)
- **Observation:** In Section 4.1 and Table 2, the low-$\beta$ margin design is shown to reduce $\beta_{y,\max}$ from 50.75 m to 36.12 m. The text mentions that it operates with "lower overall quadrupole excitation, reducing power dissipation."
- **Reviewer Insight:** Quantifying the excitation reduction adds concrete engineering weight to the claim. For example, comparing the sum of squared gradients $\sum K_i^2$ ($19.78\ \text{m}^{-4}$ for nominal vs. $16.14\ \text{m}^{-4}$ for margin design) demonstrates an approximate 18.4% reduction in magnetic excitation and resistive power dissipation ($\propto I^2$).
- **Recommendation:** Quote the numerical reduction in integrated gradient squared ($\sum K_i^2$) in Section 4.1 to substantiate the power dissipation claim quantitatively.

### Point 3: Physical Origin of the Initial Transmission Loss at 6× Jitter (Section 6.2)
- **Observation:** In Section 6.2 and Figure 5 (right), transmission drops from 100.0% to 99.82% at $6\times$ magnified error jitter, with losses localized at the exit aperture ($s = 21.789$ m).
- **Reviewer Insight:** What is the dominant loss plane (horizontal vs. vertical)? Given that the exit target has $\beta_y = 4.26$ m and $\beta_x = 2.34$ m, but the horizontal plane experiences both betatron envelope and dispersive excursion ($D_x = 0.081$ m), plus horizontal orbit deflection from bending dipole field errors, clarifying whether horizontal or vertical scraping dominates at $6\times$ will assist beam diagnostic placement (e.g., beam loss monitor positioning).
- **Recommendation:** Add a brief clarifying phrase in Section 6.2 specifying the loss distribution plane at the $6\times$ breakdown threshold.

### Point 4: Operational Tolerances vs. Component Procurement Specifications (Section 5.1 & Table 3)
- **Observation:** Table 3 presents statistical quantiles under the 5-category error budget. The OAT ranking demonstrates that incoming booster Twiss mismatch ($\Delta \beta/\beta = 5\%$) dominates output merit variation over magnet gradient errors ($10^{-3}$).
- **Reviewer Insight:** In real commissioning, booster extraction Twiss can be adjusted using booster extraction quadrupoles, whereas magnet fabrication tolerances are fixed once manufactured.
- **Recommendation:** In Section 7 (Discussion / Engineering Implications), explicitly highlight that magnet fabrication tolerances of $\Delta K/K = 10^{-3}$ are well within standard pole-machining capabilities ($\pm 20\ \mu\text{m}$), and emphasize that investment in diagnostic screens for incoming beam Twiss reconstruction yields higher operational return than over-specifying magnet tolerances.

---

## 3. Editorial & Presentation Enhancements

1. **Title & Heading Formatting:**
   - The article title is comprehensive and clear.
   - Section 3.2 heading and Section 5.2 heading should remain consistent in style (avoid unrendered math in PDF bookmarks).
2. **Table Presentation:**
   - Table 1 and Table 2 are crisp, using standard `booktabs` rules. Adding unit columns or column subheadings for Table 3 will make it completely standalone.
3. **Figure 4 & 5 Vector Scaling:**
   - Figures 4 and 5 are high quality (300 DPI vector PDF). In Figure 5 (left), ensure the legend explicitly defines the black dashed bounding box as the physical $19.35 \times 19.35$ mm aperture limit.

---

## 4. Actionable Revision Tasks (Round 2)

- [ ] **Task R2-1 (Quantify Integrated Gradient & Power Reduction):** Calculate and include the sum of squared gradients ($\sum K_i^2$) in Section 4.1, demonstrating an 18.4% reduction in magnetic excitation for the low-$\beta$ margin design.
- [ ] **Task R2-2 (Explain Physical Composition of Null-Space Modes):** Add a concise physical explanation in Section 4.2 detailing how the 3-mode null space trades internal triplet-2 focusing against boundary triplets 1 and 3.
- [ ] **Task R2-3 (Clarify Transverse Loss Plane at 6× Jitter Breakdown):** Specify in Section 6.2 that initial particle loss at $6\times$ jitter occurs predominantly in the horizontal plane due to combined betatron envelope, dispersion, and orbit deflection.
- [ ] **Task R2-4 (Commissioning Guidance & Hardware Cost Trade-Off):** Expand Section 7 item 3 to note that investing in booster extraction diagnostics provides higher operational stability than over-specifying magnet pole tolerances.
- [ ] **Task R2-5 (Recompile, Verify Provenance, and Update Package):** Recompile `paper.pdf`, update cryptographic digests in `draft_provenance.json`, verify test suite pass, and rebuild submission bundle.
- [ ] **Task R2-6 (Author Response to Reviewer 2):** Author a formal response letter addressing Review Round 2 comments.
