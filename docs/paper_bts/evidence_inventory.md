# Scientific Evidence Inventory and Provenance Audit (Task B01)

Prepared: 2026-10-13. Target Venue: **Journal of the Korean Physical Society (JKPS)**.
Author: Chong Shik Park, Department of Accelerator Science and Center for Accelerator Research, Korea University, Sejong, 30019 Republic of Korea.

---

## 1. Executive Summary

This inventory audits all historical and archived numerical evidence supporting the standalone BTS optics matching and tolerance manuscript. Every numerical result reported in the manuscript draft is traced to its exact source file, cryptographic SHA-256 hash, generating git commit, software environment, random seed, and sample count.

All five physical feasibility failures identified across 550,000 Monte Carlo evaluations are individually audited and cataloged below. Across the entire 550,000-sample ensemble, zero invalid evaluations were generated ($n_{\text{invalid}} = 0$).

---

## 2. Generating Software Environment & Git Provenance

The archived optimization and tolerance data were generated on a high-performance Linux workstation under the following environment:

| Property | Value |
| :--- | :--- |
| **Source Run Directory** | `backups_20261009/production_statistical_01` & `results/journal_campaign_01` |
| **Generating Git Commit** | `8b62bcd4037031551a1787aabae0bd5dae708046` |
| **Python Version** | Python 3.11.9 |
| **NumPy Version** | 2.4.6 |
| **SciPy Version** | 1.17.1 |
| **Accelerator Toolbox** | pyAT 0.7.2.dev26+g4701d48c.d20260831 |
| **Provenance Record** | `results/journal_campaign_01/environment.txt` |

---

## 3. Selected Deterministic Optimization Artifacts

The baseline matching solution was produced by bounded numerical least-squares optimization with multi-start initialization:

| Artifact Description | File Path | File Size | SHA-256 Checksum |
| :--- | :--- | :---: | :--- |
| **BTS Optimization Summary** | `backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json` | 5,482 B | `fe10758922697a3d0ff6496f068706099c2089348811cd31f859cdcead1cf3cb` |
| **Optimization Config** | `backups_20261009/production_statistical_01/optimization/config.json` | 2,752 B | `382e23dd1d4ed167e6cf321e40f5041e42c5909a0b5dbf1da9101ce4883f8ae2` |
| **Candidate Table (3 Starts)** | `backups_20261009/production_statistical_01/optimization/candidate_table.json` | 4,891 B | `398be628e1b017375bbbdf4c58d225e694ede6109bfda28733cdbe8419cee9d7` |

### Multi-Start Feasibility Audit:
Three independent random restarts were performed within the enforced family bounds ($[-2.5, 2.5]\text{ m}^{-2}$ for $q_{11}, q_{33}$; $[-3.0, 3.0]\text{ m}^{-2}$ for others):
- **Candidate 0 (Start ID 0, Seed 191664964)**:
  - Optimizer status: `True` (`Optimization terminated successfully`).
  - Physically feasible: **`True`** (Selected candidate).
  - Residual merit: $1.2906 \times 10^{-13}$; Mismatch $M_x = 0.0$, $M_y = 0.0$.
  - Envelopes: $\beta_{x,\text{max}} = 31.4368\text{ m}$, $\beta_{y,\text{max}} = 50.7459\text{ m}$ (both $\le 60.0\text{ m}$).
  - Quadrupole strengths ($\text{m}^{-2}$):
    - $q_{11} = -0.367525, q_{12} = -1.216433, q_{13} = 1.586072$
    - $q_{21} = -1.068373, q_{22} = 2.823108, q_{23} = -2.490968$
    - $q_{31} = 2.042678, q_{32} = -1.434271, q_{33} = 0.351115$
- **Candidate 1 (Start ID 1, Seed 1662057958)**:
  - Optimizer status: `True` (`Optimization terminated successfully`).
  - Physically feasible: **`False`** (Infeasible).
  - Residual merit: $1.2146 \times 10^{-12}$; Mismatch $M_x = 2.22 \times 10^{-16}$, $M_y = 0.0$.
  - Violation: $\beta_{y,\text{max}} = 62.5564\text{ m} > 60.0\text{ m}$ ceiling ($n_{\text{violations}} = 1$).
- **Candidate 2 (Start ID 2, Seed 1405681632)**:
  - Optimizer status: `False` (`Max function evaluations exceeded`).
  - Physically feasible: **`False`** (Infeasible).
  - Residual merit: $1284.86$; Mismatch $M_x = 0.9930, M_y = 3.63 \times 10^{-5}$.
  - Violations: $\beta_{x,\text{max}} = 69.9212\text{ m} > 60.0\text{ m}$ and $\beta_{y,\text{max}} = 65.0433\text{ m} > 60.0\text{ m}$ ($n_{\text{violations}} = 2$).

---

## 4. Monte Carlo Tolerance Run Summaries Audit

Four independent large-scale Monte Carlo tolerance runs were executed using the matched Candidate 0 configuration under a 5-category error budget:

| Dataset ID | Random Seed | Samples Requested | Valid Count | Invalid Count | Physical Failures | SHA-256 Checksum |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Run S1** | 42 | 50,000 | 50,000 | 0 | 0 | `620626291ee47d9a8d50b5372d54aaeabf640d1a64e0f846be246ea433e9da1b` |
| **Run S2** | 123 | 50,000 | 50,000 | 0 | 1 | `d1f381f714e9d2c808b28b6d3ada90eca4781895a0955aa3bedffccd4006c974` |
| **Run S3** | 777 | 50,000 | 50,000 | 0 | 0 | `353c1986e6330686d235ce3e29e622706fe04e0e5e88445f308fe8e0e1707644` |
| **Run S4** | 2026_400k | 400,000 | 400,000 | 0 | 4 | `fa3c0b8254836171ff6cab17d4e6bf3c85ec24c5023096c74cb4a2ee9209b296` |
| **Total / Pooled** | — | **550,000** | **550,000** | **0** | **5** | Pooled Analysis: `5d11a050...` |

### Raw File Locations:
- `seed42`: `results/journal_campaign_01/tolerances_seed42/publication_tolerances_summary.json`
- `seed123`: `results/journal_campaign_01/tolerances_seed123/publication_tolerances_summary.json`
- `seed777`: `results/journal_campaign_01/tolerances_seed777/publication_tolerances_summary.json`
- `seed2026_400k`: `results/journal_campaign_01/tolerances_seed2026_400k/publication_tolerances_summary.json`
- `pooled_analysis`: `results/journal_campaign_01/followup_analysis/tolerance_replicates_with_400k.json`

---

## 5. Detailed Audit of the Five Physical Feasibility Failures

Out of 550,000 evaluated error realizations, exactly five cases were classified as physically infeasible (`status: 'infeasible'`). Every failure was traced and evaluated individually:

| Failure # | Seed Run | Sample ID | Failure Cause | $\beta_{x,\text{max}}$ (m) | $\beta_{y,\text{max}}$ (m) | Limit (m) | $M_x$ | $M_y$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | `seed123` | 4,158 | `beta_exceeded` | 31.783 | **60.230** | 60.000 | 0.000106 | 0.112563 |
| **2** | `seed2026_400k` | 159,294 | `beta_exceeded` | 26.615 | **61.639** | 60.000 | 0.020646 | 0.150997 |
| **3** | `seed2026_400k` | 160,916 | `beta_exceeded` | 32.095 | **61.609** | 60.000 | 0.001848 | 0.180141 |
| **4** | `seed2026_400k` | 258,351 | `beta_exceeded` | 29.612 | **60.604** | 60.000 | 0.002018 | 0.142655 |
| **5** | `seed2026_400k` | 372,486 | `beta_exceeded` | 31.835 | **60.260** | 60.000 | 0.000180 | 0.114204 |

### Scientific Conclusions from Failure Audit:
1. **Single Failure Mechanism**: 100% (5 of 5) of the failures violated only the vertical beta function ceiling ($\beta_{y,\text{max}} > 60.0\text{ m}$).
2. **Excursion Magnitude**: The peak vertical beta exceeded the $60.0\text{ m}$ threshold by only $0.23\text{ m}$ to $1.64\text{ m}$ ($0.38\%\text{--}2.73\%$ relative overshoot).
3. **Zero Horizontal Violations**: Horizontal beta stayed well within bounds in all five cases ($\beta_{x,\text{max}} \le 32.10\text{ m} \ll 60.0\text{ m}$).
4. **Zero Mismatch Violations**: In all five failure cases, horizontal mismatch remained well below the operational threshold ($M_x \le 0.0206 < 0.05$).
5. **Exact Statistics**:
   - Point estimate: $\hat{P}_{\text{fail}} = 5 / 550,000 = 9.0909 \times 10^{-6}$.
   - Exact Clopper–Pearson 95% Confidence Interval: $[2.952 \times 10^{-6}, 2.121 \times 10^{-5}]$.
   - Wilson score 95% Confidence Interval: $[3.870 \times 10^{-6}, 2.134 \times 10^{-5}]$.

---

## 6. Prefix Stability Audit

The prefix stability criterion measures whether the median horizontal mismatch changes by less than a declared threshold when sample size is doubled:

$$\Delta_{\text{prefix}} = |\text{Med}(M_x)_N - \text{Med}(M_x)_{N/2}| < 1.0 \times 10^{-5}$$

| Run ID | Evaluated Sizes $(N/2, N)$ | $\text{Med}(M_x)_{N/2}$ | $\text{Med}(M_x)_{N}$ | Absolute Change $\Delta$ | Target | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `seed42` | $(25\text{k}, 50\text{k})$ | 0.00208190 | 0.00210273 | $2.0830 \times 10^{-5}$ | $1.0 \times 10^{-5}$ | Outside tolerance |
| `seed123` | $(25\text{k}, 50\text{k})$ | 0.00206791 | 0.00207934 | $1.1436 \times 10^{-5}$ | $1.0 \times 10^{-5}$ | Outside tolerance |
| `seed777` | $(25\text{k}, 50\text{k})$ | 0.00211317 | 0.00210260 | $1.0567 \times 10^{-5}$ | $1.0 \times 10^{-5}$ | Outside tolerance |
| `seed2026_400k` | $(200\text{k}, 400\text{k})$ | 0.00208590 | 0.00208351 | $\mathbf{2.3948 \times 10^{-6}}$ | $1.0 \times 10^{-5}$ | **Within tolerance** |

### Reporting Rule:
Both the missed 50,000-sample prefixes and the passing 400,000-sample prefix are documented in the manuscript. The threshold is preserved without retrospective relaxation.
