# Peer Review Report: JKPS Research Article

**Manuscript Title:** Constrained Optical Matching, Error Sensitivity, and Transmission Robustness of a Booster-to-Storage-Ring Transfer Line  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Date of Review:** October 13, 2026  
**Reviewer Recommendation:** **Minor Revisions**

---

## 1. Overall Evaluation & Summary

The manuscript presents a rigorous, detailed, and technically competent study of optical matching, error sensitivity, and beam transmission for a 4 GeV booster-to-storage-ring (BTS) transfer line targeting a 4th-generation diffraction-limited storage ring (Korea-4GSR / KLS).

The work distinguishes itself clearly from standard numerical optimization papers by answering four concrete physical questions:
1. Demonstrating that unconstrained optimizer convergence does not imply physical optics feasibility (finding that 26.7% of mathematical local minima violate internal aperture beta limits);
2. Identifying an alternative "low-$\beta$ margin design" via null-space exploration that gains 16.47 m in vertical envelope stay-clear buffer while preserving matching accuracy;
3. Formulating a dimensionless SVD Jacobian that resolves an apparent condition number artifact ($\kappa = 57.78$ vs. legacy mixed-unit 1421.6) and identifies 6 active knobs plus a 3-mode null space;
4. Executing an unprecedented statistical sample of 550,000 Monte Carlo evaluations, rigorously bounding the tail failure rate to $9.09 \times 10^{-6}$ (exact Clopper–Pearson 95% CI: $[2.95 \times 10^{-6}, 2.12 \times 10^{-5}]$) and identifying vertical beta blowup as the sole failure mode;
5. Validating physical particle transmission ($100.00\% \pm 0.00\%$) across 50,000 particles and five seeds, demonstrating transmission survival up to $5\times$ magnified error jitter and conceptually separating static lattice retuning from dynamic shot jitter.

The paper is well written, the figures are clear and informative, and the provenance tracking of the underlying numerical simulations is exemplary.

**Recommendation:** The paper is suitable for publication in the *Journal of the Korean Physical Society* following **Minor Revisions** to address the technical points, presentation nuances, and specific clarifications detailed below.

---

## 2. Strengths of the Manuscript

1. **Physical Grounding over Algorithmic Benchmark:** The author appropriately avoids claiming algorithmic novelty for well-known solvers (SLSQP / TRF) and instead focuses on physical envelope constraints, parameter topology, and machine stay-clears.
2. **Dimensionless Formulation:** The resolution of the condition number discrepancy via the dimensionless Jacobian $\tilde{J}_{ij} = (\Delta K_j / s_i)(\partial O_i / \partial K_j)$ is an important pedagogical and practical contribution to transfer line literature.
3. **High-Statistics Tail Qualification:** The 550,000-sample Monte Carlo study provides rare statistical rigor in accelerator design, utilizing exact Clopper–Pearson binomial intervals rather than normal approximations.
4. **Distinction between Transfer Transport and Ring Capture:** The manuscript clearly and repeatedly states that BTS transmission is distinct from storage-ring capture, preserving strict scientific boundaries.

---

## 3. Critical Technical Comments & Areas for Revision

### Major Technical Points (To be clarified before final acceptance):

1. **Aperture Baseline vs. Real Continuous Chamber (Section 2.1):**
   - The paper notes discrete square aperture stations (19.35 mm and 30 mm). In a real transfer line, the vacuum chamber is continuous (e.g., circular, racetrack, or octagonal copper/aluminum chambers, with tapers at septa).
   - *Requirement:* The author should explicitly clarify how continuous vacuum chamber profiles (or future resistive-wall / impedance limitations) relate to the discrete 4-station model used in tracking. State clearly whether the 19.35 mm limit represents the injection septum blade clearance or the nominal pipe bore.

2. **Decoupling Orbit Steering from Quadrupole Focusing (Section 5.1 & 6.2):**
   - In Section 5.1, the author notes that transverse quadrupole misalignments (100 $\mu$m) primarily drive centroid orbits rather than uncoupled linear optics. In the tracking simulations, was dipole steering correction (BPMs + corrector magnets) applied prior to transmission evaluation, or did the uncorrected beam pass through the aperture with raw orbit offsets?
   - *Requirement:* Explicitly state the orbit correction assumption. If no correctors were simulated, highlight that the $18.5\sigma$ beam stay-clear headroom is wide enough that even raw uncorrected 100 $\mu$m quadrupole misalignment orbits do not scrape at $1\times$ error levels.

3. **Energy Spread vs. Chromatic Mismatch:**
   - The beam is transported with relative momentum spread $\sigma_\delta = 8 \times 10^{-4}$ (design) and $1.1 \times 10^{-3}$ (historical). The line has no sextupoles, meaning chromatic aberrations are uncorrected.
   - *Requirement:* Briefly comment on chromatic beam envelope growth and second-order dispersion ($T_{166}$, $T_{266}$) at the exit interface, confirming that chromatic distortion does not spoil the transverse match at the ring boundary.

4. **Multi-Start Optimization Sample Size (Section 3.2):**
   - The text mentions 5 seeds with 3 candidate starts per seed (total 15 starts), finding 4 envelope violations. While illustrative, 15 starts is a relatively modest sample size for global topology exploration.
   - *Requirement:* Frame this explicitly as an illustrative multi-start audit rather than an exhaustive global topology proof, or expand the discussion to contextualize how local minima cluster around the nominal and low-$\beta$ margin attractors.

### Minor / Presentation Points:

5. **Figure 1 Element Annotations:**
   - In Figure 1, the schematic labels element types with colors, but individual magnet names ($\mathrm{q11}$–$\mathrm{q33}$, $\mathrm{B1}$–$\mathrm{B3}$) are not annotated along the top. Adding brief callouts or labels for the three triplets would enhance readability.
6. **JKPS Journal Formatting:**
   - Ensure final author addresses, PACS/CRediT taxonomy, and references follow the official JKPS LaTeX style guide (`jkps.cls` when provided by the editorial office).
7. **Notation Consistency:**
   - Ensure the definition of $\mathcal{M}_u$ in Eq.~(3) clearly cites the original Courant–Snyder mismatch parameter form (equivalent to $(\beta_{\text{mag}} - 1)$ or trace form $\frac{1}{2}\operatorname{Tr}(T_1^{-1} T_2) - 1$).

---

## 4. Specific Actionable Revision Tasks

The author should address the following actionable tasks in the revised manuscript:

- [ ] **Task R1 (Aperture & Chamber Model):** Add a paragraph in Section 2.1 discussing the physical vacuum chamber profile, clarifying the origin of the 19.35 mm half-aperture (e.g., septum extraction/injection channel) and the approximation of discrete aperture stations.
- [ ] **Task R2 (Orbit Correction Clarification):** Clarify in Section 6.1 and 6.2 whether trajectory steering correctors are assumed or whether the wide stay-clear ($> 18.5\sigma$) allows passive transmission without active steering under baseline errors.
- [ ] **Task R3 (Higher-Order Dispersion & Chromaticity):** Add a brief remark in Section 2.2 / 4.1 regarding chromatic envelope expansion and second-order momentum dispersion ($T_{166}, T_{266}$).
- [ ] **Task R4 (Framing of Multi-Start Sample Size):** Clarify the phrasing in Section 3.2 regarding the 15-start multi-start audit to emphasize its role as a diagnostic sample of local optimizer basins.
- [ ] **Task R5 (Figure & Reference Polishing):** Polish Figure captions to explicitly define all line types, and verify that all journal abbreviations adhere to standard ISO4/JKPS conventions.
- [ ] **Task R6 (Author Response Document):** Prepare a point-by-point Author Response to Reviewer letter accompanying the revised manuscript.

---

## 5. Conclusion

This is an excellent, meticulous piece of accelerator physics research that provides genuine engineering insight into transfer-line matching and reliability. With the minor clarifications outlined above incorporated, the manuscript will be a strong addition to the *Journal of the Korean Physical Society*.
