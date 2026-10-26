# Primary-source literature comparison

Checked 2026-10-13. This replaces the unsupported B01 survey; it does not infer universal sample budgets or the provenance of this model's target from other facilities.

| Study and primary record | Passage checked | Supported comparison and limit |
| :--- | :--- | :--- |
| [Kallestrup and Schlott, SLS 2.0 BRTL, IPAC25 TUPM056](https://proceedings.jacow.org/ipac2025/pdf/TUPM056.pdf) | p.1 Quadrupole scans; p.3 Trajectory control and Transmission | Demonstrates measured beam characterization and separate trajectory control; the present work is a parametric simulation comparison, not commissioned feedback. |
| [ESRF–EBS Design Report](https://www.esrf.fr/files/live/sites/www/files/com%20photos/About%20Us/EBS-TECHREPORT-reduced.pdf) | printed pp.285–286, Fig.9.19 | Rematches TL2 including off-axis QF fields and mechanical constraints within supply limits; those facility-specific boundaries are not imported here. |
| [Resende et al., Sirius Injection Optimization, IPAC22 THPOPT038](https://proceedings.jacow.org/ipac2022/papers/thpopt038.pdf) | p.1 Table2; p.2 Emittance exchange; p.3 Pending issues | Separates injector stages and addresses extraction-beam size and repeatability; this paper does not compare simulated BTS clearance with measured ring-injection efficiency. |
| [Leemann, Pulsed sextupole injection for Sweden's new light source MAX IV](https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.15.050705) | publisher title and abstract | Corrects the title at volume15, 050705; context is pulsed-multipole ring injection, not evidence for a nine-quadrupole BTS target. |

The previously supplied PLS-II and two RAON title/page combinations have not been verified against primary passages and are omitted from the revised bibliography and all comparative claims. This is a withdrawal of unsupported comparisons, not an assertion that those studies do not exist. The originally cited Sirius/ESRF conference identifiers are replaced with the primary records above. No claim of full six-dimensional mismatch or 33% feasible volume remains.

The contribution tested here is a conditional design choice: reducing vertical peak beta while maintaining the same exit target, then estimating paired clearance changes under frozen held-out errors. The analytical meaning and validity range of that comparison, including dispersion/centroid effects, distinguishes it from an optimizer demonstration. Shared upstream BTS assets with the NKM study are disclosed; capture and kicker transparency are excluded.

## Round2 source verification and contribution

The new comparison explicitly contrasts refined beta optimization with nominal direct-clearance optimization, keeping old and newly frozen tests distinct. The active-station analysis supplies the physical mechanism; no algorithm novelty or actual facility tolerance is claimed.

Primary beam numbers were reverified against Lee et al., Table1:4 GeV,7.67 nm rad natural emittance and0.106% natural spread. The [original paper mirrored by INSPIRE](https://inspirehep.net/files/74b1a2721975b480d634b9772e634e0b) was checked; [JACoW TUPC12 metadata](https://proceedings.jacow.org/ipac2024/doi_per_institute/tupc12/index.html) establishes Nashville,19–24May2024 and pp.1025–1028. These numbers do not establish the model's entrance Twiss or vertical emittance.

[ESRF's own EBS overview](https://www.esrf.fr/about/upgrade) identifies the linked technical report as2018. This establishes the bibliography year without inferring it from the2016 Orange Book mentioned in the PDF introduction. The selected report passages and limits remain as above.

The exact-binomial reference is Clopper and Pearson,Biometrika26(4),404–413(1934),DOI10.1093/biomet/26.4.404. DOI-linked original-paper retrieval was unavailable through the browsing tool; the metadata is recorded with that limitation, while the intervals are independently reconstructed numerically. Wilson remains only the attribution for Wilson intervals in the historical supplement.

## Expanded review checked 2026-10-26

The introduction now compares interface matching and geometry, beam characterization/trajectory control, and requirements imposed by nonlinear injection. No cross-facility efficiency values are used as KLS predictions.

| Added primary record | Material checked | Comparison used and evidence limit |
| :--- | :--- | :--- |
| [Guo et al., HEPS high-energy transport lines, IPAC17 TUPAB063](https://proceedings.jacow.org/ipac2017/papers/tupab063.pdf) | Full primary paper; layout constraints and injection matching; authors, title and pp. 1466–1468 | Relates ring interfaces, equipment geometry and injection scheme. Does not establish KLS targets or hardware. The DOI endpoint could not be verified and is omitted from the new entry. |
| [Guo et al., The transfer line design for the HEPS project](https://rdtm.ihep.ac.cn/article/cstr/32043.14.s41605-020-00209-6) | Journal abstract, author list and citation metadata; Radiation Detection Technology and Methods 4(4), 440–447 (2020), DOI 10.1007/s41605-020-00209-6 | Supports the limited statement that line layouts/optics evolve with connected accelerator designs. Full text was not exposed by the journal page; no detailed performance claims are taken from it. |
| [Martin et al., Diamond-II injector, IPAC22 THPOPT049](https://accelconf.web.cern.ch/ipac2022/papers/thpopt049.pdf) | Full primary paper, especially “Transfer Lines,” p. 2710; pp. 2708–2711, DOI 10.18429/JACoW-IPAC2022-THPOPT049 | Documents low-loss bunch transport, diagnostics, flexible matching and BTS geometry changes. Booster-capture results are not relabeled as BTS transmission. |
| [Luo et al., TPS nonlinear-kicker transfer line, IPAC26 TUP2685](https://indico.jacow.org/event/95/contributions/14036/) | Author-supplied conference abstract and author list | Closely related proposal addresses existing-ring geometry, trajectory correction and beam characterization. Full manuscript download failed; cite explicitly as a conference abstract, with no unverified DOI, page range, numerical performance or publication-status claim. |

Rechecked the SLS 2.0 and Sirius primary papers for the expanded commissioning/control discussion. The ESRF comparison retains the previously checked report passages above; re-download hit the browser size limit. MAX IV remains injection-method context rather than evidence for this BTS lattice. The new comparisons motivate the particular KLS design question without an unverified priority claim.
