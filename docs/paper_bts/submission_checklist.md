# Submission Readiness Checklist & Verification Manifest (Task B12)

**Document Date:** October 13, 2026  
**Target Venue:** Journal of the Korean Physical Society (JKPS)  
**Article Title:** Constrained Optical Matching, Error Sensitivity, and Transmission Robustness of a Booster-to-Storage-Ring Transfer Line  
**Author:** Chong Shik Park (Department of Accelerator Science and Center for Accelerator Research, Korea University)  
**Branch:** `bts`

---

## 1. Executive Summary & Verification Matrix

The BTS standalone manuscript has completed full scientific qualification across Tasks B01 through B12. This document certifies compliance with journal guidelines, evidence integrity, and submission readiness.

| Verification Item | Specification / Requirement | Actual Status | Decision |
| :--- | :--- | :--- | :--- |
| **Scientific Scope** | Independent BTS optics matching & error robustness | Verified distinct from companion NKM paper | **PASS** |
| **Model Geometry** | 21.789 m canonical pyAT lattice, 36 elements | Audited in `lattice_geometry.md` | **PASS** |
| **Aperture Baseline** | 19.35 mm ends, 30 mm interior discrete stations | Audited in `beam_and_constraints.md` | **PASS** |
| **Nominal Match** | $\mathcal{M}_{x,y} = 0$, $\beta_{x,y} < 60\text{ m}$ | Recomputed ($\beta_x = 31.44\text{ m}, \beta_y = 50.75\text{ m}$) | **PASS** |
| **Multistart Topology** | Identify feasibility rate across random starts | 4 of 15 starts violate envelope ceilings | **PASS** |
| **Low-$\beta$ Margin** | Reduce envelope below 40 m | $\beta_{x,\max} = 29.65\text{ m}, \beta_{y,\max} = 36.12\text{ m}$ | **PASS** |
| **Stay-Clear Buffer** | Quantify envelope buffer gain | $16.47\text{ m}$ vertical stay-clear gain | **PASS** |
| **SVD Condition No.** | Dimensionless Jacobian sensitivity | $\kappa = 57.78$ (reconciles legacy 1421.6) | **PASS** |
| **Tuning Knobs** | Orthogonal modes and null space | 6 active correction knobs, 3-mode null space | **PASS** |
| **Tolerance Volume** | High-statistics tail resolution | $N = 550,000$ across 4 independent seeds | **PASS** |
| **Tail Failure Rate** | Clopper--Pearson exact 95% confidence interval | $\hat{p} = 9.09 \times 10^{-6}$, $[2.95 \times 10^{-6}, 2.12 \times 10^{-5}]$ | **PASS** |
| **Failure Mechanism** | Audit 100% of physical failure modes | 5/5 failures caused strictly by $\beta_y > 60\text{ m}$ | **PASS** |
| **Held-Out Tracking** | 5 seeds $\times$ 10,000 particles through apertures | $100.00\% \pm 0.00\%$ physical transmission | **PASS** |
| **Jitter Breakdown** | Determine physical transmission survival limit | 100% transmission up to $5\times$ design jitter | **PASS** |
| **Static vs Dynamic** | Decouple retuning from shot jitter | Decoupled; documented in manuscript | **PASS** |
| **PDF Compilation** | Zero errors, warnings, or missing citations | Clean 11-page PDF (`paper.pdf`, 608 KB) | **PASS** |
| **Test Suite** | Full pytest regression pass | 709/709 passed in 132s | **PASS** |
| **Protected Files** | Scientific source files intact | Verified unmodified (`git status` clean) | **PASS** |

---

## 2. Reviewer Report & Technical Reconciliation

### 2.1 Scope and Novelty Review
- **Finding:** Pure numerical optimizer benchmarking is insufficient for publication novelty.
- **Resolution:** The manuscript centers on physical insights: (1) multi-start feasibility topology showing that optimizer convergence does not imply envelope feasibility; (2) discovery of the low-$\beta$ margin design saving 16.47 m in vertical envelope headroom; (3) dimensionless SVD exposing 6 orthogonal knobs and 3 null-space degrees of freedom; (4) extreme-scale ($N = 550,000$) tail qualification proving that vertical envelope blowup is the sole failure mode; (5) rigorous separation of static machine retuning from random beam shot jitter.

### 2.2 Model and Hardware Assumptions
- **Finding:** Previous internal notes conflated the 100 nm rad conservative tolerance test beam with the 7.67 nm rad Korea-4GSR design booster beam.
- **Resolution:** Section 2 explicitly defines both parameter sets. Design-beam tracking confirms $> 18.5\sigma$ aperture clearance to 19.35 mm chamber walls. Quadrupole gradients ($|G| \le 40\text{ T/m}$) and pole-tip fields ($B_{\text{pole}} \le 0.73\text{ T}$) operate well below the 1.2 T iron saturation limit.

### 2.3 Unit and Dimension Consistency
- **Finding:** Legacy reports listed an apparent Jacobian condition number of 1421.6 due to mixing meters, radians, and dimensionless ratios.
- **Resolution:** Section 4.2 formulates the dimensionless Jacobian $\tilde{J}$, proving the actual physical condition number is a well-behaved $\kappa = 57.78$.

---

## 3. Referee & Reviewer Evidence Manifest

All manuscript assets are cataloged with cryptographic SHA-256 digests in [`draft_provenance.json`](draft_provenance.json):

1. **LaTeX Document Source:** `docs/paper_bts/paper.tex` (`f3d1df6f0f287f1452b7d863a6b787caacc78a9bade2679fe986ac87017737d5`)
2. **BibTeX Bibliography:** `docs/paper_bts/paper.bib` (`fc4aea2ebfe1d534bb946047ae79f8f410ca797c352931f2b890d9208b67c8b1`)
3. **Compiled Article PDF:** `docs/paper_bts/paper.pdf` (`ac7e3b346212f9dbe251806f93662490de614a522c4829e6907c2051514a4c2b`)
4. **Figure 1 (Layout & Optics):** `docs/paper_bts/figures/fig1_bts_layout.pdf` (`f1a26a852f8c3e318009ef3e67fefc4df6dcba39bab126cf656e2ddf0b857b35`)
5. **Figure 2 (SVD Knobs):** `docs/paper_bts/figures/fig2_svd_knobs.pdf` (`2ea45d3fe81244fe8825d7e8762a9eaca26925b769d5251c67fc68c150c3a63a`)
6. **Figure 3 (Margin Design):** `docs/paper_bts/figures/fig3_margin_tradeoff.pdf` (`ee9a0e5afe857bbab8798b3ba243f33028d9b30b4c757dca4125226a55fbdc65`)
7. **Figure 4 (Tolerances):** `docs/paper_bts/figures/fig4_tolerance_curves.pdf` (`cd095ebf086ee1ca52eeb2c42518458d05107a5cd8fc32d3618090b6f9d4eaa6`)
8. **Figure 5 (Transmission):** `docs/paper_bts/figures/fig5_heldout_transmission.pdf` (`48e9f3aa394247a00dc31040826368192204b19b30176990959b6804275a0d2a`)

---

## 4. Submission Next Steps & Author Instructions

- **Submission Policy Reminder:** In accordance with project policy (`AGENTS.md`), no automated `git push` or online journal submission will be performed. Submission remains an explicit action for the author.
- The compiled manuscript `docs/paper_bts/paper.pdf` and its source bundle are complete, fully self-contained, and ready for formal submission to the *Journal of the Korean Physical Society*.
