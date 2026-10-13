# Author Response to Reviewer 3

**Manuscript Title:** Constrained Optical Matching, Error Sensitivity, and Transmission Robustness of a Booster-to-Storage-Ring Transfer Line  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Date:** October 13, 2026  

---

We sincerely thank the Reviewer for their thorough and thoughtful evaluation in Round 3, and for their formal recommendation to **Accept for Publication**. We have implemented both recommended camera-ready typographical and bibliographic adjustments.

Below is our point-by-point response detailing the changes made.

---

### Response to Camera-Ready Polish Items

#### Point 1 (Eliminate Overfull `\hbox` in Section 2.1)
> *In the paragraph defining the coordinate convention: "The coordinate system follows the standard Accelerator Toolbox paraxial convention $(x, p_x, y, p_y, \delta, ct)$, where...", an overfull `\hbox` of 30.97 pt occurs because LaTeX cannot break the inline mathematical tuple across lines cleanly. Rewording or breaking this sentence slightly will eliminate the margin overflow.*

**Author Response:**  
We have revised the sentence in Section 2.1 (page 2) to cleanly define the state vector $\mathbf{z}$:
> *"The paraxial coordinate convention follows Accelerator Toolbox, using state vector $\mathbf{z} = (x, p_x, y, p_y, \delta, ct)^{\mathsf T}$, where $x, y$ are transverse positions in meters, $p_x \approx x'$ and $p_y \approx y'$ are normalized canonical momenta in radians, $\delta = \Delta p/p_0$ is the relative momentum deviation, and $ct$ is the longitudinal path difference."*

This revision completely eliminates the overfull `\hbox` (0 overfull boxes in `paper.log`), producing clean line-breaking and margin alignment.

---

#### Point 2 (Formal Citation for PLS-II in Introduction)
> *In the Introduction, Pohang Light Source II (PLS-II) is mentioned alongside RAON, MAX IV, and Sirius, but lacks a formal citation. Adding a standard reference for PLS-II (e.g., Kim et al., 2012 or similar standard JKPS/IPAC citation) will complete the literature attribution.*

**Author Response:**  
We have added the standard JKPS reference for the PLS-II transfer line upgrade:
- D. E. Kim *et al.*, "Upgrade of the Beam Transfer Line for the PLS-II", *J. Korean Phys. Soc.* **60**, 1028--1034 (2012), DOI: `10.3938/jkps.60.1028` (`Kim2012`).

In Section 1 (page 1), the text is updated accordingly:
> *"Similar transfer line rematching challenges have been investigated across domestic and international facilities, including the Pohang Light Source II (PLS-II)~\cite{Kim2012}, the RAON heavy-ion transport lines~\cite{Chung2014,Kim2020}, MAX~IV~\cite{Leemann2012}, and Sirius."*

---

### Verification and Deliverables Summary
- All LaTeX sources compiled cleanly (`paper.pdf`, 12 pages, 614 KB) with zero errors, zero warnings, and zero overfull text boxes.
- All cryptographic digests updated and verified in `draft_provenance.json`.
- Tarball submission package regenerated (`results/bts_submission/bts_jkps_submission.tar.gz`) and tested in an isolated sandbox build.
- Full regression suites passed (`pytest tests/test_bts_paper_assets.py` and `python scripts/reproduce_bts_paper.py --verify`).
