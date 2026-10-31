# Author Response to Reviewer 2

**Manuscript Title:** Constrained Optical Matching, Error Sensitivity, and Transmission Robustness of a Booster-to-Storage-Ring Transfer Line  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Date:** October 13, 2026  

---

We sincerely thank the Reviewer for their thorough re-evaluation and constructive recommendations in Round 2. We are gratified that the Reviewer found the revisions from Round 1 rigorous and recommended our manuscript for publication in the *Journal of the Korean Physical Society* subject to minor editorial and clarification adjustments.

Below is our point-by-point response detailing the specific revisions incorporated into the final manuscript.

---

### Response to Specific Recommendations

#### Point 1 (Substantiate Power Dissipation Claim with Numerical Metric)
> *In Section 4.1, the text asserts that the low-$\beta$ margin design operates with "lower overall quadrupole excitation, reducing power dissipation." To make this scientifically concrete for accelerator engineers, please quote the integrated sum of squared normalized gradients $\sum K_i^2$ (or $\int K^2 ds$) comparing nominal matched vs. margin designs.*

**Author Response:**  
We agree that quoting the quantitative integrated gradient squared provides essential engineering substantiation. In Section 4.1 (page 5), we have added the explicit values:
> *"Furthermore, it operates with lower overall quadrupole excitation: the integrated sum of squared normalized gradients $\sum K_i^2$ drops from $19.78~\mathrm{m}^{-4}$ in the nominal design to $16.14~\mathrm{m}^{-4}$ in the margin design, yielding an 18.4\% reduction in magnetic excitation and associated resistive power dissipation."*

---

#### Point 2 (Physical Mechanics of the 3-Mode SVD Null Space)
> *In Section 4.2, the 3-D null space ($\sigma_{7-9} \equiv 0$) is noted as allowing internal envelope optimization without perturbing exit matching. Briefly clarify the physical composition of these modes across the 3 triplet families.*

**Author Response:**  
In Section 4.2 (page 6), we have elaborated on the physical mechanism:
> *"Physically, these null modes correspond to balanced counter-trims between entrance triplet 1 ($\mathrm{q11}$--$\mathrm{q13}$) and exit triplet 3 ($\mathrm{q31}$--$\mathrm{q33}$), coupled with internal phase-advance redistribution in triplet 2 ($\mathrm{q21}$--$\mathrm{q23}$). This allows operators to suppress internal envelope peaks without disrupting the phase-space match at the ring boundary."*

---

#### Point 3 (Loss Plane at 6× Jitter Breakdown Threshold)
> *In Section 6.2, the initial physical loss is observed at $6\times$ jitter ($T = 99.82\%$). Specify which transverse plane (horizontal vs. vertical) dominates this loss at $s = 21.789$~m.*

**Author Response:**  
In Section 6.2 (page 8), we have clarified that initial scraping is predominantly in the horizontal plane:
> *"Tracking particle loss coordinates reveals that this initial scraping occurs predominantly in the horizontal plane at the final exit aperture station ($s = 21.789$~m), driven by the combined effects of uncorrected horizontal dispersion excursions ($D_x = 0.081$~m), dipole steering kicks, and betatron envelope magnification."*

---

#### Point 4 (Prioritizing Diagnostic Screens over Magnet Machining Tolerances)
> *In Section 7 (item 3), reinforce the engineering recommendation regarding booster extraction instrumentation by contrasting it against quadrupole manufacturing capabilities.*

**Author Response:**  
In Section 7 (item 3, page 9), we have updated the discussion:
> *"Because incoming booster Twiss errors are the leading contributor to BTS mismatch, high-resolution profile monitors (e.g., three-screen or multi-wire stations) must be installed at the extraction interface to measure and correct booster extraction optics prior to transfer-line tuning. Standard magnet manufacturing tolerances ($\Delta K/K \le 10^{-3}$) are routinely achieved through precision pole machining; hence, capital investment in entrance diagnostic screens delivers far higher operational return than over-tightening magnet machining specifications."*

---

#### Point 5 (Figure 5 Caption Polish)
> *Clarify in the Figure 5 caption that the black dashed boundary in the left plot denotes the physical $19.35 \times 19.35$~mm aperture limit.*

**Author Response:**  
In the caption of Figure 5 (page 8), the description has been updated:
> *"Figure 5: Physical beam transmission and jitter stress analysis. (Left) Transverse phase-space tracking distribution at the BTS exit ($s = 21.789$~m) showing the injected bunch well inside the $19.35 \times 19.35$~mm aperture limit indicated by the dashed black bounding box. (Right) Transmission survival curve under magnified error jitter..."*

---

### Verification and Deliverables Summary
- All LaTeX sources recompiled with zero errors or warnings (`paper.pdf`, 12 pages).
- All cryptographic hashes recorded and verified in `draft_provenance.json`.
- Tarball submission bundle regenerated (`results/bts_submission/bts_jkps_submission.tar.gz`) and tested in an isolated build directory.
- Test suites passed (`pytest tests/test_bts_paper_assets.py` and `python scripts/reproduce_bts_paper.py --verify`).
