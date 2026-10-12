# Constrained optical matching and error sensitivity of a booster-to-storage-ring transfer line

Draft outline, 2026-10-13. Author: Chong Shik Park, Department of Accelerator Science and Center for Accelerator Research, Korea University, Sejong, 30019 Republic of Korea.

## 1. Article question and venue

**Working title:** “Constrained optical matching and error sensitivity of a booster-to-storage-ring transfer line” (11 words).

**Question:** Can the nine-quadrupole, 4 GeV BTS model meet a declared exit-optics target within magnet and envelope constraints, and which errors and correction combinations determine its usable operating margin?

**Proposed contribution:** a validated transfer-line matching case study with interpretable quadrupole correction knobs and statistically qualified tolerance limits. Least-squares, SLSQP and NSGA-II are established methods; their use alone is not algorithmic novelty. The physical contribution must come from the constrained design comparison and explanation of the dominant sensitivities. These additional analyses are tasks, not existing findings.

JKPS is a reasonable first target for a focused accelerator-optics study: its current scope covers pure and applied physics. That is a scope assessment, not an acceptance prediction or a claim that a lower-impact journal accepts weaker evidence. See the [official scope](https://link.springer.com/journal/40042/aims-and-scope) and [author guidance](https://link.springer.com/journal/40042/submission-guidelines), checked 2026-10-13. No alternative venue is ranked here without a separate scope review.

Use a Research Article with approximately 3,800 words including abstract and captions, at most six main figures, captions below 200 words, and a 150–250-word abstract. These follow the current JKPS recommendations; the journal states that word/page limits are not strict. The title is below its 20-word guidance. LaTeX is accepted for mathematical manuscripts and the Springer Nature template is recommended. Do not reuse PRAB REVTeX as the assumed JKPS submission format or add PACS codes. Recheck the guidance before submission.

## 2. Relationship to the NKM paper

The BTS paper concerns transport to a specified exit boundary: matching, envelope control, error propagation and possible rematching. The NKM paper concerns the nonlinear magnet and subsequent ring injection. Cite the companion work appropriately for its publication status and disclose shared lattice, code and selected BTS solution. Develop new text and BTS-specific figures; do not reuse its capture/transparency conclusions as the new contribution.

Optical mismatch is not transmission, and BTS transmission is not storage-ring capture. A beta ceiling is an optics constraint; its satisfaction alone does not certify chamber clearance or loss-free beam transport. The NKM field is not required for the central BTS claims. Historical stored-kick observables should be excluded from BTS tolerance tables.

## 3. Existing evidence and limits

The following files were read locally on 2026-10-13. Historical data are usable starting points, subject to the provenance and physics audits in B01–B04.

| Evidence | Observed result | Use and qualification |
| :--- | :--- | :--- |
| `backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json`, adjacent `config.json` and `candidate_table.json` | Selected mismatch Mx = My = 0 at floating-point precision; peak beta x/y = 31.4368/50.7459 m; one feasible candidate of three starts | Nominal solution for the archived target. Not proof of global optimality or a measured hardware setting. |
| `results/journal_campaign_01/followup_analysis/tolerance_replicates_with_400k.json` and its four selected raw summaries | 550,000 requested samples, zero invalid evaluations; pooled median Mx = 0.00208629, 95% order-statistic interval [0.00207403, 0.00209890]; median My = 0.00249860 | Fixed-optics error model, not capture. Raw summary hashes match those recorded in the analysis. All four select the same optimization/config and error-budget hashes. |
| Same pooled analysis | Five physical feasibility failures / 550,000; estimated probability 9.09e-6, exact 95% interval [2.95e-6, 2.12e-5] | Probability under the implemented budget and feasibility definition; not a machine loss probability. Audit all failure causes before attributing them. |
| Same analysis, per-run prefixes | Three 50,000-sample runs miss the declared absolute median-stability target 1e-5; the 400,000-sample run meets it with a 2.395e-6 change from 200,000 to 400,000 | Report both outcomes. One passing prefix does not prove convergence of rare failures or extreme tails. |
| [Tolerance uncertainty notes](../paper/tolerance_uncertainty.md) and [physics-model coverage](../paper/physics_model.md) | Booster beta mismatch dominates historical OAT merit ranking, followed by quadrupole gradient and energy errors | Budget-dependent ranking. Some sampled errors have no effect in the optics evaluator; zero response is not a demonstrated tolerance. |
| [MOGA decision](../paper/moga_decision.md) | Archived dispersion objective combines D [m] and D' [dimensionless]; small-budget fronts vary; legacy finalist tracking uses an ideal kicker for ten turns | Historical MOGA performance is excluded from the core paper. Correct and rerun only if a distinct BTS trade-off is needed. |

Selected optimization SHA-256: `fe10758922697a3d0ff6496f068706099c2089348811cd31f859cdcead1cf3cb`.
Adjacent config SHA-256: `382e23dd1d4ed167e6cf321e40f5041e42c5909a0b5dbf1da9101ce4883f8ae2`.
The original record is `results/journal_campaign_01/source_optimization_hashes.txt`. Raw outputs are ignored by git and require a separately supplied evidence attachment.

Do not merge earlier values (30.23/44.52 m in README or the older partially matched optimization report) into this selected design. Archived global fallback bounds are ±3 m^-2, with q11/q33 limited to ±2.5 m^-2 and other families to ±3 m^-2; they are model assumptions pending hardware confirmation. The older report's ±5 m^-2 is not this configuration.

The archived entrance beta x/y is 7.56/12.269 m, alpha x/y is 1.5231/-1.6547, D = 0.2762 m and D' = -0.0657. Exit targets are beta x/y = 2.336495/4.256241 m, alpha x/y = -0.016335/0.017772, D = 0.080868 m and D' = 0.047472. Establish their physical observation boundary before calling them ring injection optics: these differ from the ring Twiss at the NKM centre.

The historical constraints use 100/10 nm rad emittances and 0.0011 relative energy spread. The NKM author's later input identifies a 7.67 nm rad design booster horizontal emittance. Preserve the historical study as a sensitivity case and obtain a justified main beam specification; do not relabel the historical ensembles as design-beam transport results. The current nine-quadrupole AT line and preliminary ten-quadrupole MAD-X file are different sequences; reconcile them before any code comparison.

## 4. Provisional abstract

Optical matching in a booster-to-storage-ring transfer line must control beam envelopes while delivering the required phase-space distribution at the injection boundary. We study a 4 GeV, nine-quadrupole transfer-line model using normalized optical residuals and constrained numerical optimization. For the archived target, the selected solution matches both transverse planes to floating-point precision and has peak horizontal and vertical beta functions of 31.44 m and 50.75 m, below the imposed 60 m limit. Four fixed-optics error ensembles containing 550,000 realizations give a median horizontal mismatch of 0.002086, with a 95% interval of 0.002074–0.002099, and five violations of the implemented feasibility criteria. These estimates are conditional on the assumed error budget and optics evaluator. The proposed final analysis will relate normalized quadrupole sensitivities to practical correction combinations and compare nominal matching with a design selected for envelope margin. Independent transport checks will distinguish optical feasibility from physical beam transmission. The study is intended to identify which input-beam and magnet errors require control, and to quantify the limitations of a matched transfer line without treating optical agreement as evidence of storage-ring capture.

This is a planning abstract; rewrite it after B08–B10. Its future-tense analyses must not appear as completed results in a submitted abstract.

## 5. Section-by-section outline

| Section | Approximate words | Scientific content and required evidence |
| :--- | ---: | :--- |
| Abstract | 180 | Problem, validated model, main design comparison, qualified tolerance result and practical implication. |
| 1. Introduction | 430 | Matching in low-emittance light sources; why envelope and correction margins matter; related BTS studies; specific unresolved design question. Distinguish a physical design study from optimizer benchmarking. |
| 2. Transfer-line model and boundary conditions | 580 | Versioned layout, lengths, bends and nine quadrupoles; beam and optics at both boundaries; dispersion convention; apertures, magnet limits and assumed error inputs. Resolve the AT/MAD-X sequence difference and nominal/assumed specifications. |
| 3. Matching and sensitivity methods | 620 | Dimensionless residuals, least-squares initialization and SLSQP feasibility; family bounds, tolerances, start selection and termination. Normalize Jacobian rows/columns before SVD and validate proposed correction knobs. Explain beam transport and uncertainty estimators. |
| 4. Matched design and operating margin | 650 | Compare baseline, archived matched and newly selected margin/robust design using identical beam, geometry and constraints. Show optics, dispersion, magnet strengths and physical envelope clearance. Give both optimizer status and independent feasibility. |
| 5. Error sensitivity and correction | 660 | Trace each implemented error to its observable; correlated versus independent assumptions; OAT and combined errors; finite correction ranges; held-out rematching or correction test. Distinguish static machine errors from beam-shot jitter. |
| 6. Discussion | 300 | Dominant sensitivities and engineering implications; uncertainty in input specifications; modeling limitations; what transfers to other lattices and what does not. Avoid a universal optimality claim. |
| 7. Conclusions | 160 | Answer the design question with supported numbers and a practical correction/tolerance recommendation. State that ring capture was outside scope. |
| Main captions | 220 | Explain compared cases, units, sample counts and uncertainty bars; keep total main text near 3,800 words. |

Add acknowledgments, funding, author contributions, competing interests and data/code availability using author-confirmed information. Disclose generative assistance as applicable under the journal's guidance. Supplement detailed bounds, candidate tables, error-coverage audit, all seeds, convergence checks and a hash inventory.

## 6. Figure and table plan

| Item | Planned content | Evidence/task |
| :--- | :--- | :--- |
| Figure 1 | BTS layout with both observation boundaries, aperture stations and nine quadrupoles | B02 |
| Figure 2 | Baseline and selected designs: beta, dispersion and physical beam-envelope/clearance profiles | B04–B05, B08 |
| Figure 3 | Dimensionless Jacobian singular spectrum and validated correction-knob responses | B06 |
| Figure 4 | Matching versus envelope/robustness trade-off, including equal-condition deterministic controls | B08; optional MOGA only after its gate |
| Figure 5 | Error-amplitude scans and sensitivity ranking restricted to active BTS observables | B07, B09 |
| Figure 6 | Independent-seed mismatch distributions, tail intervals and held-out correction results | B09–B10 |
| Table 1 | Boundary Twiss, beam parameters, lattice and hardware constraints with source/assumption labels | B02–B03 |
| Table 2 | Baseline, matched and margin-design strengths, objectives, feasibility and transport | B05, B08, B10 |
| Table 3 | Error budget and uncertainty-qualified performance summaries | B07, B09 |

If correction or trade-off analyses do not yield a meaningful new result, reconsider the article's scope before drafting a results-heavy paper. Large sample counts alone do not establish novelty.

## 7. Sources to build into the literature review

Start from the source-backed KLS and booster references in [author inputs](../paper/dependent_answers.md), the existing [bibliography audit](../paper/bibliography_audit.md), AT publications and established matching/multi-objective methods. B01 must retrieve and assess relevant transfer-line design and correction papers, including JKPS accelerator studies, before claiming novelty. This outline does not certify a completed literature review.
