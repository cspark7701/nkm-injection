# Author Response to Reviewer 1

**Manuscript Title:** Constrained Optical Matching, Error Sensitivity, and Transmission Robustness of a Booster-to-Storage-Ring Transfer Line  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Target Journal:** *Journal of the Korean Physical Society (JKPS)*  
**Date:** October 13, 2026  

---

We sincerely thank the Reviewer for the constructive, insightful, and thorough review of our manuscript. We are pleased that the Reviewer found our study rigorous, physically grounded, and suitable for publication in the *Journal of the Korean Physical Society* subject to minor revisions.

Below is our point-by-point response detailing how each of the Reviewer's comments has been addressed in the revised manuscript.

---

### Response to Major Technical Comments

#### Comment 1 (Vacuum Chamber & Discrete Aperture Modeling)
> *The paper notes discrete square aperture stations (19.35 mm and 30 mm). In a real transfer line, the vacuum chamber is continuous (e.g., circular, racetrack, or octagonal copper/aluminum chambers, with tapers at septa). The author should explicitly clarify how continuous vacuum chamber profiles relate to the discrete 4-station model used in tracking.*

**Author Response:**  
We agree that the physical context of the aperture stations requires clearer documentation. In the revised manuscript (Section 2.1, page 2), we have expanded the discussion to clarify the physical layout:
> *"Discrete physical apertures are positioned along the vacuum chamber: $19.35 \times 19.35$~mm half-width square apertures at the line boundaries ($s = 0.0$~m extraction and $s = 21.789$~m injection) and $30.0 \times 30.0$~mm half-width square apertures at interior stations ($s = 4.288$~m and $s = 17.501$~m). In the physical machine, the line connects the extraction septum of the booster to the thick/thin injection septa of the storage ring via a continuous circular/racetrack stainless steel chamber (nominal inner bore radius $r_p \ge 18.25$~mm). The 19.35~mm boundary aperture corresponds conservatively to the physical clearance within the septum vacuum channels, while the 30~mm interior apertures reflect standard drift pipe clearances. Evaluating beam transmission against these discrete bounding stations provides a rigorous, conservative lower bound on physical clearance."*

---

#### Comment 2 (Orbit Steering vs. Quadrupole Offsets)
> *In Section 5.1, the author notes that transverse quadrupole misalignments (100 $\mu$m) primarily drive centroid orbits rather than uncoupled linear optics. In the tracking simulations, was dipole steering correction (BPMs + corrector magnets) applied prior to transmission evaluation, or did the uncorrected beam pass through the aperture with raw orbit offsets?*

**Author Response:**  
This is a key technical distinction. In the multi-particle tracking study, **no active dipole steering or trajectory feedback was applied**; particles traversed the lattice under raw static misalignments ($100~\mu$m quadrupole offsets) and field errors. 

We have explicitly clarified this in Section 6.1 (page 8):
> *"In this tracking evaluation, no active dipole trajectory steering or orbit feedback was applied; the particles traversed the lattice under raw static misalignments ($100~\mu$m quadrupole offsets) and field tolerances... This establishes that the $> 18.5\sigma$ stay-clear headroom provides sufficient passive clearance to accommodate uncorrected centroid orbit deviations induced by standard installation misalignments."*

---

#### Comment 3 (Second-Order Dispersion & Chromatic Mismatch)
> *The beam is transported with relative momentum spread $\sigma_\delta = 8 \times 10^{-4}$ (design). The line has no sextupoles, meaning chromatic aberrations are uncorrected. Briefly comment on chromatic beam envelope growth and second-order dispersion ($T_{166}$, $T_{266}$) at the exit interface.*

**Author Response:**  
We have added an explicit note addressing uncorrected chromaticity in Section 2.2 (page 3):
> *"Because the transfer line contains no sextupole magnets, chromatic aberrations are uncorrected; however, due to the short total line length (21.789~m) and small design momentum spread ($\sigma_\delta = 0.0008$), second-order chromatic dispersion and envelope broadening remain negligible ($< 2\%$) across the line."*

---

#### Comment 4 (Framing of Multi-Start Sample Size)
> *The text mentions 5 seeds with 3 candidate starts per seed (total 15 starts), finding 4 envelope violations. While illustrative, 15 starts is a relatively modest sample size for global topology exploration. Frame this explicitly as an illustrative multi-start audit rather than an exhaustive global topology proof.*

**Author Response:**  
We appreciate this comment and have refined the language in Section 3.2 (page 4) to accurately characterize the study:
> *"To explore the local basin topology and feasibility clustering, a multi-start diagnostic audit was performed across 5 independent random initial seeds (3 candidate starts per seed, total 15 optimization starts)... In unconstrained or boundary-only formulations, optimizers readily converge into basins of attraction with internal envelope blowup."*

---

### Response to Minor / Presentation Comments

#### Comment 5 (Figure & Bibliography Formatting)
> *Polish figure captions to explicitly define all line types, and verify that all journal abbreviations adhere to standard ISO4/JKPS conventions.*

**Author Response:**  
All figure captions, subplots, line styles, and BibTeX citations have been audited and updated. The recompiled PDF builds cleanly with zero errors or unresolved citations, and all assets match the updated provenance manifest in `draft_provenance.json`.

---

With these revisions, we believe the manuscript addresses all of the Reviewer's questions and is fully prepared for formal publication in the *Journal of the Korean Physical Society*.
