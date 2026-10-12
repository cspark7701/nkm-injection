# Author inputs A1–A6 for the round-2 revision

Answers to the author inputs requested in
[consolidated_revision_plan_round2.md](reviews/consolidated_revision_plan_round2.md). The inputs are the KLS chamber,
lattice version, kicker status, booster and septum, coupling target and journal. Compiled by the author; sources
checked 2026-10-12.

**Status labels used below:**

| Label | Meaning |
| :--- | :--- |
| **V** | Verified in the primary source (PDF text checked) |
| **A** | Author statement (internal knowledge, no public source) |
| **S** | Secondary source, not re-checked against a primary document |
| **U** | Unsourced; do not use as a fact without a reference |
| **—** | Not available; parametrise |

## Summary

| Input | Answer | Status | Effect on the plan |
| :--- | :--- | :---: | :--- |
| A1 Chamber | Arc: octagonal 24 × 18 mm (±12 × ±9 mm). Centre bend: 24 × 9.74 mm. IVUs: 5 mm minimum gap. Injection-straight chamber not public. | V / — | D6 can use a real arc and ID profile; the vertical limits are much tighter than the round-1 scan (±5 mm everywhere). |
| A2 Lattice | `K4GSR_HBIv4-1` is the lattice used by Kim et al. (IPAC'25); it is not the latest KLS version. | A | D1: describe it as "the KLS design lattice of Kim et al. (IPAC'25)" and state that later versions exist. |
| A3 Kicker | A preliminary NKM design for this study by Dong-Eon Kim (PAL), not the KLS project design. Loop powering is not answered. | A / — | D1, D9: state the design status; treat series and independent loop powering as two cases. |
| A4 Booster, septum | Booster extraction ε_x = 7.67 nm rad, σ_δ = 0.106 %. Septum parameters are published. Extraction orbit jitter is not public. | V / — | D4: the assumed 100 nm rad is 13 times the design value; rerun with the design value (D8). Parametrise the jitter. |
| A5 Coupling | ε_y/ε_x = 0.10 | A | D9: keep 0.10, labelled as the assumed coupling target, with the scaling. |
| A6 Journal | Decided at the last step | A | D15 stays author-gated. |

## A1 — Vacuum chamber and apertures

| Region / component | Value | Status | Source |
| :--- | :--- | :---: | :--- |
| Regular arc chamber | Octagonal beam channel, 24 mm horizontal × 18 mm vertical (full); stated as "12 mm horizontal × 9 mm vertical" octagonal in the IPAC'25 paper | V | [THPC61], [WEPS103] |
| Arc chamber, impedance approximation | Ellipse, semi-axes 10 mm × 9 mm (resistive-wall model only; not the tracking aperture) | V | [THPC61] |
| Centre-bend chamber | Vertical full width reduced from 18 mm to 9.74 mm; horizontal unchanged | V | [THPC61] |
| Photon absorbers | In the antechamber, 17 mm from the beam (not a beam-channel aperture) | V | [THPC61] |
| In-vacuum undulators | 3 m long, minimum gap 5 mm; impedance model with 19 IVUs closed at 5 mm | V | [WEPS103] |
| First-phase IVUs (IVU20/22/24) | Magnetic gap range 5–18 mm | S | [JKPS], not re-checked (paywalled) |
| ID10 / ID24 operating gaps | Effective minimum 6 mm for some beamlines | S | Beamline TDR pages [TDR10], [KBSI] |
| Injection straight | 11.6 m, 6 quadrupoles, 4 bump kickers (two 3.1 mrad, two 2.4 mrad) | V | [TUPR52] |
| Bump-kicker aperture | Vertical gap 30 mm, horizontal 64 mm (magnet clearance, not the ceramic chamber) | V | [TUPR52] |
| Injected-beam offset (bump scheme) | 12 mm from the stored-beam centre; 5 mm from the bumped orbit at kicker 3 | V | [TUPR52] |
| NKM chamber in the injection straight | Not public | — | — |

**Notes for the tracking model (D6):**
- **The KLS baseline injection is a four-kicker bump with a 1 mm thin septum.** The NKM study is an alternative
  scheme, so the injection-straight chamber of the NKM case must be assumed. The 64 × 30 mm clearance belongs to the
  bump kickers.
- **Vertical limits are the critical ones.** The NKM study found that the large injected oscillation couples into the
  vertical plane. The relevant limits are ±4.87 mm at the centre bends and ±2.5 mm in closed IVUs.
- **The IVU magnetic gap is an upper bound on the vacuum aperture.** Any liner reduces it. Use 5 mm full gap (closed
  IVUs) as the worst case and an open-gap case as the reference.
- **IVU locations are not in the lattice file.** Their straights must be identified before the aperture is applied.

Aperture model for D6 (half-apertures, mm):

```python
KLS_APERTURES_MM = {
    "arc_octagon":    {"half_x": 12.0, "half_y": 9.0,  "shape": "octagon", "status": "V"},
    "centre_bend":    {"half_x": 12.0, "half_y": 4.87, "shape": "octagon", "status": "V"},
    "ivu_closed":     {"half_x": None, "half_y": 2.5,  "shape": "flat gap, magnetic (upper bound)", "status": "V"},
    "nkm_straight":   {"half_x": None, "half_y": None, "shape": "pending (not public)", "status": "-"},
}
```

The octagon's corner geometry is not given in the sources. A rectangle with the same half-widths is an upper bound on
the aperture; the inscribed ellipse is a lower bound.

## A2 — Lattice version

The author states that `K4GSR_HBIv4-1` is the lattice used in Kim et al., IPAC'25 ([MOPS089]), and that it is not the
latest KLS version. **Status: A.**

Consequence for D1:
- name the lattice as "the KLS design lattice of Kim et al. (IPAC'25)";
- state that later versions exist and that their sextupole and octupole settings may enlarge the injection DA;
- the title can keep "Korea Light Source" if the text says "design lattice".

## A3 — Kicker design status and powering

- **Design status (A).** The 0.525 m four-loop NKM is a preliminary design for this study by Dong-Eon Kim (Pohang
  Accelerator Laboratory). It is not the KLS project injection kicker; the KLS baseline uses a four-kicker bump
  ([TUPR52]).
- **Loop powering (—).** Not answered. D9 treats two cases:
  - all four loops in series, where current imbalance is negligible;
  - independent loops, where the current balance becomes a tolerance.

## A4 — Booster extraction beam and septa

| Quantity | Value | Status | Source |
| :--- | :--- | :---: | :--- |
| Extraction energy | 4 GeV | V | [TUPC12] |
| Natural emittance at 4 GeV | 7.67 nm rad | V | [TUPC12], table 1 |
| Natural energy spread | 0.106 % | V | [TUPC12], table 1 |
| Circumference, repetition rate | 772.893 m, 2 Hz | V | [TUPC12] |
| Emittance range 7–11 nm rad (lattice and ramp versions) | — | U | No source found |
| Energy-jitter envelope ±0.4 % | — | U | No source found |
| Extraction flat-top 30 ms; extraction in a zero-dispersion section | — | U | No source found |
| Extraction orbit jitter | Not public | — | Parametrise |

**Storage-ring injection septa** ([TUPR52], table 3; all V):

| Septum | Type | Bend | Blade | Full gap × width | Length | Current | Pulse |
| :--- | :--- | ---: | ---: | :--- | ---: | ---: | :--- |
| BTSEP-1, 2, 3 | Out-of-vacuum thick eddy-current septum, 0.5 mm µ-metal shield | 87.27 mrad each | 2.5 mm | 15 × 30 mm | 1.7 m | 8.22 kA | 100 µs half-sine |
| BTSEP-4 | In-vacuum thin eddy-current septum | 10 mrad | 1 mm | 13 × 14 mm | 0.4 m | 3.42 kA | < 20 µs half-sine |

**Stability and leakage** ([TUPR52]; V):
- Thick-septum leakage field: 0.3 ± 0.1 G in the shielded region.
- Thin-septum leakage at the bumped-orbit position: about 0.1 % of the main field (about 3.3 G) for a 20 µs pulse.
- Bump-kicker pulse-current reproducibility: ±0.2 %. This applies to the storage-ring bump kickers, not to the booster
  extraction or the septa.

The paper's text also calls the thick septum "direct current driven" while its table gives a 100 µs half-sine. The
table values are used here.

**Not given in the sources:** the septum current stability and the booster extraction-kicker stability. The septum
angle-jitter term in D4 therefore stays parametric.

**Consequences for D4 and D8:**
- **Emittance.** The round-1 studies assumed ε_x = 100 nm rad at extraction, 13 times the design value. With
  7.67 nm rad the injected beam is about 3.6 times smaller in both size and divergence at the septum. Capture without
  errors is expected to rise (the round-1 scan gave 98.9 % already at 25 nm rad), and the usable centroid window
  to widen. Both must be recomputed. The final
  robustness campaign (D8) must use the design value, and the old value can be kept as a sensitivity case.
- **Energy spread.** 0.106 % agrees with the 0.11 % used so far.
- **Septum geometry.** The study's septum (2 mm blade, stored-beam edge at −16 mm) differs from the KLS thin septum
  (1 mm). D1 should state which septum the NKM scheme assumes.
- **Septum leakage (for the R2 m9 estimate).** A 3.3 G field over 0.4 m gives an angle of about 1×10⁻⁵ rad at 4 GeV.
  This applies at the bumped orbit, which does not exist in the NKM scheme. The stored beam would sit farther from the
  blade, where the leakage is lower.
- **Extraction orbit jitter.** Not public. Keep the jitter-scale curve. Suggested reference grid: 0.1, 0.25, 0.5 and
  1.0 mm with 0.05–0.5 mrad.

## A5 — Coupling target

ε_y/ε_x = 0.10, i.e. ε_x ≈ 62 pm rad and ε_y ≈ 6.2 pm rad. **Status: A.**

No KLS publication stating this target was found. A 10 % coupling is a common assumption for fourth-generation rings
(e.g. Touschek-lifetime studies). D9 keeps 0.10, labels it as the assumed coupling target, and gives the scaling
A_y/σ_y ∝ (ε_y)^(−1/2).

## A6 — Target journal

The author will decide at the last step (D15). Until then the manuscript stays in the generic article class, and the
framing follows milestone 134 (PRAB first; JINST and NIM A as alternatives).

## Sources

| Key | Reference |
| :--- | :--- |
| [MOPS089] | J. Kim, G. Jang, J. Kim, J. Lee, J. Seok, "The Korea-4GSR storage ring lattice design", Proc. IPAC'25, pp. 789–792, doi:10.18429/JACoW-IPAC2025-MOPS089 |
| [THPC61] | J. Seok, J. Lee, J. Kim, G. Jang, H. Choi, T. Ha, "Estimation of impedances and corresponding instabilities in Korea-4th generation storage ring", Proc. IPAC'24, THPC61, doi:10.18429/JACoW-IPAC2024-THPC61. https://proceedings.jacow.org/ipac2024/pdf/THPC61.pdf |
| [WEPS103] | J. Seok, J. Lee, J. Kim, G. Jang, H. Choi, T. Ha, "Impedance estimation and instability analysis for Korea-4GSR storage ring", Proc. IPAC'25, WEPS103, doi:10.18429/JACoW-IPAC2025-WEPS103. https://proceedings.jacow.org/ipac2025/pdf/WEPS103.pdf |
| [TUPR52] | G. Hahn, D.-E. Kim, Y.-G. Jung, B.-J. Kim, S.-H. Kim, J. Lee, "Injection magnet system for Korea-4GSR facility", Proc. IPAC'24, TUPR52, doi:10.18429/JACoW-IPAC2024-TUPR52. https://epaper.kek.jp/ipac2024/pdf/TUPR52.pdf |
| [TUPC12] | Y. Lee, E.-S. Kim, S. H. Park, S. Shin, J. Kim, "Study on beam injection and ramping efficiency for Korea-4GSR booster synchrotron", Proc. IPAC'24, TUPC12, doi:10.18429/JACoW-IPAC2024-TUPC12. https://inspirehep.net/files/74b1a2721975b480d634b9772e634e0b |
| [JKPS] | C. Ha, I. S. Kwon, K.-J. Kim, J. Kim, J.-H. Lim, "In-vacuum undulators for the first phase beamlines of Korea-4GSR", J. Korean Phys. Soc. 85, 371–380 (2024), doi:10.1007/s40042-024-01133-4 |
| [TDR10] | Korea-4GSR Beamline TDRs, "ID10 NanoProbe". https://korea-4gsrbeamlinetdrs.readthedocs.io/en/latest/BLs/ID10_NanoProbe.html |
| [KBSI] | KBSI beamline document (table of ID24 MSA / IVU16 parameters). https://4gsr.kbsi.re.kr/_files/board/20260403/6b18a5033942d8286bf5a873bcf0d648.pdf |

The mechanical items of [TUPR52] (coil and septum forces, ohmic heating) are omitted because they do not enter the
beam-dynamics model.
