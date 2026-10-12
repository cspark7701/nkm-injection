# Milestone 165: Justification of Beam, Magnet and Aperture Constraints (Task B03)

**Completed:** 2026-10-13  
**Status:** Successfully Executed on branch `bts`.  
**Task Reference:** Task B03 in [`docs/paper_bts/002_manuscript_tasks.md`](../../paper_bts/002_manuscript_tasks.md).

---

## 1. Executive Summary

Milestone 165 establishes the physical justifications and quantitative margins for all beam emittances, vacuum chamber apertures, envelope constraints, quadrupole magnet gradients, and error tolerances governing the Korea-4GSR Booster-to-Storage Ring (BTS) transfer line study.

The analysis formally separates the historical inherited constraint beam ($\epsilon_x = 100\text{ nm}\cdot\text{rad}$) from the author-sourced design booster beam ($\epsilon_x = 7.67\text{ nm}\cdot\text{rad}$). It proves that the optical constraint $\beta_{x,y} \le 60.0\text{ m}$ is an envelope safety boundary providing $\ge 18.5\,\sigma$ physical aperture clearance ($> 13.0\text{ mm}$ margin) inside the narrowest $19.35\text{ mm}$ vacuum chamber, and demonstrates that all 9 matched quadrupole settings operate far below the $1.2\text{ T}$ iron pole saturation threshold.

---

## 2. Key Accomplishments & Deliverables

1. **Beam Parameters, Hardware Limits, and Constraint Justifications (`docs/paper_bts/beam_and_constraints.md`)**:
   - **Beam Matrix**: Comparative audit of historical inherited beam ($100\text{ nm}\cdot\text{rad}$), baseline tracking beam ($10.89\text{ nm}\cdot\text{rad}$), and author design booster beam ($7.67\text{ nm}\cdot\text{rad}$), with explicit rules prohibiting misrepresenting the conservative constraint beam as the machine design beam.
   - **Envelope Clearance Justification**: Quantitative proof that $\beta \le 60\text{ m}$ guarantees $> 7.6\,\sigma$ clearance even under the historical $100\text{ nm}\cdot\text{rad}$ envelope and $> 20.4\,\sigma$ clearance ($> 13.6\text{ mm}$) for the $7.67\text{ nm}\cdot\text{rad}$ design beam.
   - **Quadrupole Field Conversions**: Explicit conversion $G = K_1 (B\rho)$ and $B_{\text{pole}} = |G| r_0$ at $E_0 = 4.0\text{ GeV}$ ($(B\rho) = 13.3426\text{ T}\cdot\text{m}$) across all 9 quadrupoles. Proven that maximum pole-tip field in the matched line is $B_{\text{pole}} = 0.7289\text{ T}$ (at `q22`), retaining $39.3\%$ safety margin below the $1.2\text{ T}$ iron saturation limit.
   - **Error Budget Definition**: Machine-readable specification of static quadrupole gradient ($0.1\%$), dipole field ($0.05\%$), alignment ($100\,\mu\text{m}$), roll tilt ($0.5\text{ mrad}$), and shot jitter ($100\,\mu\text{m}$ centroid, $50\,\mu\text{rad}$ angle, $0.1\%$ energy).
   - **Permitted Claim Boundaries**: Prohibits mischaracterizing the 5 optical feasibility failures across 550,000 samples as lost bunches on chamber walls.

---

## 3. Verification and Standards Compliance

- **Protected Files Integrity:** All protected scientific data files remain untouched.
- **Git Branch:** Executed directly on branch `bts`.
- **Unit & Integration Tests:** Ran `pytest tests/test_bts_lattice.py tests/test_baseline.py -v`; all 14 tests passed cleanly.
