# Article Scope, Scientific Question, and Boundary Declarations (Task B01)

Prepared: 2026-10-13. Target Venue: **Journal of the Korean Physical Society (JKPS), Research Article**.
Author: Chong Shik Park, Department of Accelerator Science and Center for Accelerator Research, Korea University, Sejong, 30019 Republic of Korea.

---

## 1. Principal Scientific Question

**Can a 21.789 m, nine-quadrupole booster-to-storage-ring (BTS) transfer line for a 4 GeV fourth-generation synchrotron light source achieve rigorous optical matching to a declared off-axis injection boundary while strictly preserving beam-envelope margins ($\beta \le 60\text{ m}$), and which error mechanisms, physical constraints, and correction knob combinations dictate its operational feasibility and tolerance budget?**

This question addresses a physical accelerator-design problem rather than an algorithm-benchmarking study:
1. Optical matching in 4th-generation light sources must bridge between a full-energy booster synchrotron and an ultra-low-emittance storage ring where injection stay-clears and physical apertures are severely restricted.
2. The BTS transfer line must match six optical parameters ($\beta_x, \beta_y, \alpha_x, \alpha_y, D_x, D_x'$) using nine quadrupoles subject to individual power-supply gradient limits, polarity restrictions, and maximum beam-envelope ceilings.
3. The paper establishes the sensitivity of the matched solution to incoming beam jitter versus static magnetic errors, quantifies extreme tail optical feasibility failures across 550,000 statistical error realizations, and derives normalized, orthogonal correction knobs for beam commissioning.

---

## 2. Relationship and Disclosed Overlap with the Companion NKM Paper

The research in this repository encompasses two distinct accelerator domains that must remain clearly delineated:

| Feature / Domain | Companion NKM Paper (`docs/paper/`) | Standalone BTS Paper (`docs/paper_bts/`) |
| :--- | :--- | :--- |
| **Physical Scope** | Nonlinear kicker magnet (NKM) tracking & storage-ring injection | Booster-to-storage-ring (BTS) transfer line transport & matching |
| **Observation Boundary** | Multi-turn ring dynamics downstream of septum blade to 4,000 turns | Entrance of BTS line ($s = 0$) to exit matching boundary ($s = 21.789\text{ m}$) |
| **Core Physics** | 3-D Biot–Savart filament field, self-deflection, transparency | Linear transfer matrices, chromatic dispersion, Twiss matching, envelope control |
| **Primary Figures of Merit** | Ring capture efficiency (%), stored-beam perturbation ($\sigma_x, \sigma_y$) | Mismatch factors ($M_x, M_y$), peak beta ($\beta_{\text{max}}$), envelope clearance |
| **Error Handling** | Multi-turn beam loss, static ring orbit correction, booster jitter | Optics tolerance budget, OAT sensitivity ranking, Jacobian SVD correction knobs |

### Explicit Boundary and Scope Declarations:
- **Shared Assets Disclosed**: Both manuscripts share the underlying storage-ring lattice (`K4GSR_HBIv4-1.mat`), the BTS transfer-line sequence, and the core simulation framework (`src/nkm_injection/`). The selected BTS quadrupole matching solution reported here is identical to the upstream injection boundary used in the companion paper.
- **Independence of Claims**: 
  - Optical mismatch is **not** transmission. A low mismatch factor ($M_x \approx 0$) guarantees phase-space orientation matching, not 100% transmission through narrow apertures.
  - BTS transmission is **not** storage-ring capture. Stated BTS matching success does not imply multi-turn survival or stored-beam transparency.
  - Beta ceilings ($\beta \le 60\text{ m}$) represent transverse optics constraints; satisfaction of the ceiling does not replace physical vacuum-chamber clearance verification.
  - Historical stored-beam kick metrics (evaluated from the downstream NKM kick map during early unified runs) are explicitly **excluded** from BTS tolerance tables and claims.

---

## 3. Bounded Candidate Claims

The claims of the BTS manuscript are bounded as follows:

| Claim ID | Candidate Claim Statement | Required Evidence & Verification |
| :--- | :--- | :--- |
| **BC1** | The nine-quadrupole BTS model matches entrance Twiss to target injection optics to floating-point precision ($M_x = 0, M_y = 0$, merit $\approx 1.29 \times 10^{-13}$), maintaining peak beta functions of $\beta_{x,\text{max}} = 31.44\text{ m}$ and $\beta_{y,\text{max}} = 50.75\text{ m}$ strictly below the $60\text{ m}$ constraint. | `backups_20261009/.../bts_optimization_summary.json` (SHA-256: `fe107589...`), verified by linear optics propagation. |
| **BC2** | Multi-start gradient-based matching is non-trivial and topology-constrained: out of three independent random restarts within family bounds, only 1 candidate achieves physical feasibility; 1 start violates vertical beta ($\beta_{y,\text{max}} = 62.56\text{ m}$), and 1 start exceeds evaluation limits with $\beta_{x,\text{max}} = 69.92\text{ m}$. | `candidate_table.json` (SHA-256: `398be628...`), auditing all start seeds and constraint violation vectors. |
| **BC3** | Under a 5-category machine error budget (gradient, roll, alignment, field, beam jitter), median horizontal mismatch across 550,000 Monte Carlo samples is bounded at $\text{Med}(M_x) = 0.002086$ (95% CI: $[0.002074, 0.002099]$), with 0 invalid evaluations across all runs. | Pooled replicate analysis `tolerance_replicates_with_400k.json` (SHA-256: `5d11a050...`) across seeds 42, 123, 777, and 2026_400k. |
| **BC4** | The overall optics feasibility failure probability under the assumed budget is $(9.09 \pm 9.1) \times 10^{-6}$ (5 failures in 550,000 samples). All 5 failures are exclusively caused by $\beta_{y,\text{max}}$ exceeding $60.0\text{ m}$ by $< 1.65\text{ m}$ ($\beta_{y,\text{max}} \in [60.23, 61.64]\text{ m}$); zero failures violate mismatch limits. | Exact failure audit across raw summaries: sample 4158 (seed 123) and samples 159294, 160916, 258351, 372486 (seed 2026_400k). |
| **BC5** | SVD decomposition of the normalized, dimensionless optics-to-quadrupole Jacobian matrix ($\mathbf{J}_{\text{norm}}$) yields a stable singular value spectrum (condition number $\approx 1421.6$) and identifies orthogonal quadrupole knob groupings that decouple dispersion correction from beta matching. | Linear optics Jacobian calculation in `bts_optimization_summary.json`, verified via finite-difference checks. |
| **BC6** | One-at-a-time (OAT) sensitivity scans identify incoming booster horizontal mismatch ($\Delta \beta_x, \Delta \alpha_x$) and momentum offset ($\Delta p/p$) as the primary contributors to optical merit degradation, ranking ahead of quadrupole misalignments and roll errors. | OAT sensitivity tables in `publication_tolerances_summary.json` across 4 independent seeds. |

---

## 4. Predeclared Tolerances, Comparisons, and Success Criteria

To ensure scientific rigor, all numerical and statistical criteria are predeclared:

1. **Numerical Matching Tolerances**:
   - Transverse optical mismatch: $M_x, M_y < 1.0 \times 10^{-4}$ (acceptance threshold; nominal achieved is $< 10^{-12}$).
   - Horizontal dispersion residual: $|\Delta D_x| < 2.0\text{ mm}$, $|\Delta D_x'| < 1.0\text{ mrad}$.
   - Maximum beta functions: $\beta_{x,\text{max}} \le 60.0\text{ m}$, $\beta_{y,\text{max}} \le 60.0\text{ m}$.
   - Quadrupole gradient bounds: $q_{11}, q_{33} \in [-2.5, +2.5]\text{ m}^{-2}$; other 7 quadrupoles $\in [-3.0, +3.0]\text{ m}^{-2}$.

2. **Statistical and Sampling Criteria**:
   - Sample counts: minimum 50,000 samples per seed for tolerance studies.
   - Confidence level: 95% two-sided intervals ($\alpha = 0.05$).
   - Bootstrap resampling: $B \ge 20,000$ draws using isolated RNG generators.
   - Prefix stability criterion: $|\text{Med}(M_x)_{N} - \text{Med}(M_x)_{N/2}| < 1.0 \times 10^{-5}$.
     - *Predeclared Reporting Rule*: The 50,000-sample runs missed this strict threshold ($\Delta \approx 1.05\text{--}2.08 \times 10^{-5}$), while the 400,000-sample run achieved it ($\Delta = 2.39 \times 10^{-6}$). Both outcomes must be explicitly reported without retroactively relaxing tolerances.
   - Invalid evaluation policy: `raise` or zero tolerance ($n_{\text{invalid}} = 0$). Any invalid tracking call invalidates the run.

---

## 5. Reconciliation of Historical Inconsistencies

Earlier repository summaries and notebook iterations contained minor discrepancies that are hereby audited and resolved:
1. **Lattice Length**:
   - *Legacy notebook text*: Mentioned $L = 29.8\text{ m}$ (which mistakenly included an extended downstream drift/injection region).
   - *Authoritative model*: Exactly $21.789\text{ m}$ from the booster extraction point to the BTS exit boundary station.
2. **Quadrupole Strengths and Beta Peaks**:
   - *Early unconstrained prototype*: Reported $\beta_{x,\text{max}} = 30.23\text{ m}, \beta_{y,\text{max}} = 44.52\text{ m}$ under relaxed bounds ($\pm 5\text{ m}^{-2}$).
   - *Authoritative constrained baseline*: $\beta_{x,\text{max}} = 31.44\text{ m}, \beta_{y,\text{max}} = 50.75\text{ m}$ under hardware-enforced bounds ($[-2.5, 2.5]\text{ m}^{-2}$ for $q_{11}, q_{33}$ and $[-3.0, 3.0]\text{ m}^{-2}$ for others).
3. **Emittance Baseline vs Design Beam**:
   - *Historical tolerance input*: Used $100\text{ nm}\cdot\text{rad}$ / $10\text{ nm}\cdot\text{rad}$ as a conservative stress-test emittance.
   - *KLS baseline booster design*: Features a design emittance of $7.67\text{ nm}\cdot\text{rad}$. The historical $100\text{ nm}\cdot\text{rad}$ study is classified strictly as a conservative high-emittance sensitivity scenario.
