# Consolidated revision plan (Reviewers 1 and 2)

Date: 2026-10-10. Inputs:
- [Reviewer 1 report](reviewer1_report.md) and [register](reviewer1_revision_tasks.md): 12 tasks.
- [Reviewer 2 report](reviewer2_report.md): 20 tasks.

Both recommend major revision. The target journal is undecided, so the manuscript stays in the JINST class and every
change is kept venue-neutral (R2-19 and R2-20 are author decisions).

Where the reviewers differ, the more defensible requirement is adopted and the choice recorded:

| Topic | Reviewer 2 | Reviewer 1 | Adopted |
| :--- | :--- | :--- | :--- |
| Chromatic scaling of the kick | add 1/(1+δ) | distinguish canonical momentum p_x/p₀ from slope first | AT uses canonical p_x/p₀; the kick Δp_x/p₀ = (q/p₀)∫B ds carries no 1/(1+δ). Fix only the drift (slope = p_x/(1+δ)) and quantify. |
| Ring errors | ≥ 10 corrected error seeds; DA −20…40 % | no fixed number; an ideal-lattice study with a bounded sensitivity is acceptable | Ideal-lattice design study, stated as such, plus a bounded sensitivity: ring gradient and sextupole error seeds (no orbit correction needed) and a chamber-aperture scan. |
| References | ≥ 20 | no fixed count; clear contribution and like-for-like comparison | Verified closest-system comparison table, with no target count. |
| DOI | at submission | accessible evidence; DOI desirable, not mandatory | Frozen local evidence bundle with rebuild instructions; DOI left as an author action. |
| New RADIA fields | 3-D RADIA tracking | do not run protected notebooks; analytical field with bounds acceptable | Exact Biot–Savart field of the documented RADIA filament geometry, validated against `kickmap_file.txt`. Protected files are read only. |

## Consolidated tasks in execution order

Each task records its execution under the next milestone number and is committed (results stay uncommitted).

| C | Covers | Work | Acceptance |
| :--- | :--- | :--- | :--- |
| C1 | R1-02, R2-1a, R2-14, part R1-07 | 3-D Biot–Savart field of the four filament loops; validation against the RADIA kick map (both components, x and y); sliced 3-D tracker in AT canonical coordinates (exact drift with p/(1+δ)); slice and δ convergence; `kicker_model_validation.md`. | Kick-map agreement quantified; slice convergence below a declared tolerance; δ effect bounded. |
| C2 | R1-03, R2-1c | Mechanism: centroid trajectories and accumulated kicks for thin, uniform-profile thick and 3-D models; signed-angle response; choice of the principal model. | Thin/finite-length reversal explained with controlled comparisons; principal model chosen with reasons. |
| C3 | R1-04, R2-2, R2-9 | Operating window with the principal model: matched-point grid; adaptive angle scan (≤ 0.1 mrad) with a declared 80 % threshold; septum phase-space acceptance diagram (blade, beam ellipse); angle-optimality test; fresh-bunch validation with paired controls. | Threshold crossings resolved with uncertainty; selection separated from validation. |
| C4 | R1-06, R2-3, R2-4, R2-12, m4 | Survival and acceptance at the final point: particle convergence (500/2000), 4000-turn survival, loss accounting by location, chamber-aperture and ring-error sensitivity, backend check at the operating point. | Changes below the declared tolerance, or conclusions restricted; loss categories reconcile with N. |
| C5 | R1-09, R2-13, R1-08 (timing) | Combined-error ensemble with the principal model; dipole control on all seeds; timing error as a field-scale error; finite-particle check; partial correlations. | Every comparison paired with matched IDs, N and intervals. |
| C6 | R1-05, R2-4, R2-5, R2-6 | Error-budget table with sources or a "hypothetical" label; tolerance curves: capture (mean, p10) against booster jitter scale, NKM–orbit offset, and injected emittance. | Required stability for a declared capture threshold, with uncertainty. |
| C7 | R1-07, R2-8 | Transparency from the exact field: near-axis multipole coefficients, deterministic Gauss–Hermite beam average, horizontal and vertical, offsets; tracked multi-turn stored beam; controls labelled as hypothetical linear estimates. | Uncertainty floor on the aligned centroid; centroid, rms kick and emittance reported separately. |
| C8 | R1-08, R2-7 | Pulse and timing: revolution period, parameterized residual-field and train estimates; claims restricted to an ideal single-pass spatial field where not modelled. | No practical transparency claim without a supporting estimate. |
| C9 | R1-01, R2-10, R2-15, R2-20 | Novelty and scope statement; verified comparison table of NLK/MIK systems; lattice identification (author to confirm). | One demonstrated contribution; every reference verified. |
| C10 | R1-11, R2-11, R2-16–18, minor comments | Manuscript revision: parameter and error tables, geometry figure, shorter abstract, condensed §5.1, figure fixes, notation and wording corrections. | Text, macros, figures and PDF agree; clean build. |
| C11 | R1-10, R2-19 (evidence) | Frozen evidence bundle (selected raw data, configs, hashes, environment, rebuild script); complete figure dependency closure; current claim matrix. | Rebuild from the bundle in a clean directory reproduces the macros. |
| C12 | R1-12 | Point-by-point response to both reviewers; final acceptance checklist; full test suite and gated build. | Every major comment closed by evidence or by an explicit claim restriction. |

The study design details of the Reviewer 1 register apply. Protected inputs remain unchanged, and nothing is pushed,
submitted or published.
