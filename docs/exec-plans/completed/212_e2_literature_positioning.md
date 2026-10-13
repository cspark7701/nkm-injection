# Milestone 212 — E2: Positioning against Sun et al. (2020)

Completed: 2026-10-13. Round-3 task E2 (R1C-02).

**Source.** Sun et al., "Optimizations of nonlinear kicker injection for synchrotron light sources", PRAB 23, 010702
(2020), doi:10.1103/PhysRevAccelBeams.23.010702. The metadata was checked with Crossref, and the full text (CC BY 4.0)
was read.

**What it establishes.**
- An eight-conductor, four-quadrant NLK, the same topology as the NKM here.
- Segmented drift–kick–drift tracking through a Biot–Savart field, with Runge–Kutta as the reference.
- A finite 3-D conductor model with return loops; fringe fields did not significantly affect ALS efficiency.
- MOGA optimisation; about 90 % efficiency, limited by the 274 nm rad booster beam.
- A 28 cm prototype with a 32 × 11 mm aperture; injection angle 0.08 mrad.

**Distinct contribution of this paper.** A quantified trajectory-approximation error (single thin map against sliced
and 3-D) in an angle-cancelling geometry. There, a 4.85 mrad incoming angle is removed in 0.525 m, and the sagitta is
0.32 mm, about 3 % of the 9.4 mm kick-lobe FWHM. The ALS sagitta is about 0.04 mm, estimated from the published field
profile. Sun et al. compare field models, whereas this paper compares trajectory approximations, so the findings are
consistent; the text says so explicitly.

**Changes.**
- `paper.tex`:
  - the abstract opens with the established tools and the unquantified thin-map accuracy;
  - the introduction gains a paragraph on Sun et al. and restates the contribution, without claiming any invention;
  - the discussion adds the complement/consistency sentence;
  - the comparison table gains an ALS row (0.280 m, 32 × 11 mm, about 90 % simulated). The table is set in
    footnotesize with a shorter caption to fit.
- `paper.bib`: the Sun2020 entry.
- `bibliography_audit.md`: a verification record.
- `novelty_and_comparison.md`: a round-3 positioning section.
- `cover_letter.md`: the contribution paragraph.

**Checks.**
- Gated builds pass in isolated directories: one-column 28 pages, and two-column.
- The installed PDF is regenerated in E11.
