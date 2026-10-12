# Milestone 164: Physical Line and Observation Boundaries (Task B02)

**Completed:** 2026-10-13  
**Status:** Successfully Executed on branch `bts`.  
**Task Reference:** Task B02 in [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md).

---

## 1. Executive Summary

Milestone 164 establishes the physical transfer line layout, magnet sequence, aperture stations, coordinate systems, and observation boundaries for the standalone JKPS Booster-to-Storage Ring (BTS) transfer line article.

All historical discrepancies between the preliminary 10-quadrupole MAD-X sequence (`bts.madx`, $38.123\text{ m}$) and the canonical 9-quadrupole Accelerator Toolbox (AT) model (`src/nkm_injection/bts_lattice.py`, $21.789\text{ m}$) have been reconciled and documented. The exact provenance of the boundary optical functions (entrance booster optics at $s = 0$ and target exit optics at $s = 21.789\text{ m}$) has been verified, explicitly distinguishing the BTS exit boundary from the storage-ring NKM magnet center.

---

## 2. Key Deliverables Produced

1. **Lattice Geometry Specification (`docs/paper_bts/lattice_geometry.md`)**:
   - Comprehensive 36-element geometry table listing element indices, families, lengths, start/end $s$-positions, bending angles, edge angles, aperture limits, and baseline/matched quadrupole strengths.
   - Exact definitions of the two physical vacuum chamber aperture stations: `ap_rect` ($\pm 19.35\text{ mm}$ at $s = 0$ and $s = 21.789\text{ m}$) and `ap_rect2` ($\pm 30.00\text{ mm}$ at $s = 6.833\text{ m}$ and $s = 11.761\text{ m}$).
   - Formal technical reconciliation proving that `bts.madx` ($38.123\text{ m}$, 10 quads) represents a non-equivalent legacy concept, whereas the 21.789 m pyAT model is the authoritative line.

2. **Author Inputs and Boundary Provenance (`docs/paper_bts/author_inputs.md`)**:
   - Detailed provenance of entrance Twiss ($\beta_x = 7.560\text{ m}, \beta_y = 12.269\text{ m}, \alpha_x = 1.5231, \alpha_y = -1.6547, D_x = 0.2762\text{ m}, D_x' = -0.0657\text{ rad}$) and target exit Twiss ($\beta_x = 2.336495\text{ m}, \beta_y = 4.256241\text{ m}, \alpha_x = -0.016335, \alpha_y = 0.017772, D_x = 0.080868\text{ m}, D_x' = 0.047472\text{ rad}$).
   - Explicit distinction between BTS exit optics at marker `m4` and the circulating beam optics at the NKM center ($\beta_x \approx 16.20\text{ m}, \beta_y \approx 5.35\text{ m}$). Prohibits substituting NKM-center optics without accounting for intervening injection geometry.
   - Matrix of verified hardware specifications versus working modeling assumptions.

3. **Publication Layout Figures**:
   - High-resolution publication figure [`docs/paper_bts/figures/fig1_bts_layout.png`](../../paper_bts/figures/fig1_bts_layout.png) (300 DPI, 343 KB).
   - Publication vector PDF [`docs/paper_bts/figures/fig1_bts_layout.pdf`](../../paper_bts/figures/fig1_bts_layout.pdf).
   - Figure illustrates magnet layout (dipoles, quadrupoles, apertures), baseline vs matched transverse $\beta$-functions, envelope constraint $\beta_{\max} \le 60\text{ m}$, and horizontal dispersion $D_x(s)$.

---

## 3. Verification and Standards Compliance

- **Protected Files Integrity:** All protected scientific files (`By.txt`, `kickmap_file.txt`, `K4GSR_HBIv4-1.mat`, `nkm_field.xlsx`, `nkm_field_expanded.xlsx`, `NKM_radia.ipynb`, `NKM_radia_y=0.ipynb`, `nlk.py`, `storage_ring.ipynb`) remain completely untouched.
- **Git Branch:** Executed directly on branch `bts`.
- **Unit & Integration Tests:** Existing test suites continue to pass cleanly.
