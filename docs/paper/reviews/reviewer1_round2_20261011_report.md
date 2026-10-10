# Reviewer 1 — second-round manuscript assessment

Date: 2026-10-11  
Manuscript: *Finite-length and vertical effects in nonlinear-kicker injection into the Korea Light Source*  
Author: Chong Shik Park  
Reviewed repository revision: `03b8fe998dea4059dcc952049ed663bfc6eaceb1`  
Recommendation: **Major revision, focused in scope. Do not accept the present version.**

This is a pre-submission referee-style assessment of the current manuscript, not an appointment by a journal or an editorial decision. It assesses the revised article in `docs/paper/`, rather than repeating the assessment of the earlier thin-kicker study. The [first-round report](reviewer1_report.md), [original task register](reviewer1_revision_tasks.md), [author response](author_response.md), and all other existing reviews are preserved. The new actionable register is [Second-round revision tasks](reviewer1_round2_20261011_revision_tasks.md).

## 1. Recommendation and overall assessment

The revision is substantially stronger. It now has a credible accelerator-physics question: how finite-length self-deflection and the physical vertical field change injection matching and error sensitivity in a nonlinear kicker. The hierarchy from a thin map to a self-deflecting trajectory and a three-dimensional field, together with native nonlinear ring tracking, gives the paper a scientific argument beyond a software or simulation report. The discussion also acknowledges the unfavorable capture comparison with a uniform kicker rather than presenting the NKM as universally superior.

I would not accept this version yet. The remaining issues concern the reliability and interpretation of its central claims: validation of the off-midplane trajectory approximation, the distinction between 500-turn capture and longer survival, inference of a quarter-jitter tolerance, the meaning of ideal static correction, and the status of pulse requirements. There is also a concrete numerical reporting error in the survival paragraph. These issues warrant a focused major revision because some require limited validation or reanalysis, not merely copy editing.

This is not a recommendation to repeat the whole production campaign. Most revisions can use the existing raw evidence. A small independent trajectory check and, if retained as quantitative claims, selected long-turn boundary or pulse checks are more useful than indiscriminately increasing Monte Carlo counts. A simulation-only article can be publishable if its assumptions, validation and contribution are explicit; hardware measurements are not a blanket acceptance condition for this paper's declared scope.

For a physics-oriented submission, the argument should remain centered on the finite-length mechanism and its limits. That framing is compatible with the accelerator and beam physics coverage of [Physical Review Accelerators and Beams](https://journals.aps.org/prab/about). A [JINST](https://jinst.sissa.it/jinst/help/JINST/JINST_about.jsp) submission would benefit from clearer engineering requirements and the limits of the filament/pulse model. The actual editorial decision would also depend on the chosen journal and its reviewers.

## 2. Review basis and evidence checks

I read the current `paper.tex` and extracted text from the current 12-page `paper.pdf`, including the rendered control/transparency and robustness figures. Supporting material examined includes `kicker_model_validation.md`, `pulse_and_timing.md`, the revision manifest and generated macros, selected raw survival/robustness/transparency artifacts, and the implementations in `wire_field.py`, `build_revision_figures.py`, and `track_stored_beam_3d.py`.

All **46 artifacts** listed in `revision_manifest.json` exist locally and match their recorded SHA-256 hashes. This establishes consistency with the manifest; it is not an independent reproduction of the simulations or proof of physical accuracy. No simulations, manuscript rebuild, or numerical test suite were run during this review. The paired jitter calculation below is a new analysis of already saved results, not a new tracking study.

The current nominal comparison uses four fresh 500-particle bunches; combined-error comparisons use 150 paired realizations across three seeds with 200 particles and 500 turns per realization. The jitter-level curves use 50 paired realizations at seed 42. The distinction matters when interpreting their intervals and extrapolating engineering recommendations.

## 3. Status of the first-round concerns

| Earlier concern | Second-round assessment |
| :--- | :--- |
| R1-M1: principal magnetic model | Substantially addressed. Exact filament-field agreement with RADIA, a physical vertical sign, end fields and self-deflection are now included. Off-midplane trajectory validation remains to be strengthened; see M1. |
| R1-M2: scientific contribution and mechanism | Substantially addressed. The self-deflection mechanism and length dependence make a credible contribution. General claims about all kick maps and vertical defocusing need narrowing; see M6. |
| R1-M3: operating window and selection | Largely addressed. A declared selection rule, fresh validation bunches, resolved scans and crossing uncertainties replace a single coarse optimum. The quoted window remains a 500-turn, ideal-lattice result. |
| R1-M4: robustness and actionable tolerances | Partly addressed. Paired ensembles and jitter curves are a major improvement. The quarter-jitter specification and static-correction interpretation are stronger than the evidence; see M3–M4. |
| R1-M5: final-point survival, aperture and lattice sensitivity | Partly addressed. Final-point 4000-turn survival and aperture/error studies are present. Duration reporting is wrong, and the scope of the shorter window and sensitivity tests needs reconciliation; see M2. |
| R1-M6: sampled transparency floor | Substantially addressed. Symmetry, deterministic quadrature and paired stored-beam tracking replace a tiny noisy sampled centroid. Centroid cancellation must not be described as the disappearance of every disturbance; see M7. |
| R1-M7: pulse and later turns | Partly addressed. The ideal single-pass limitation is explicit. Later-turn coordinates remain a linear diagnostic and timing estimates need their pulse-phase assumptions; see M5. |
| R1-M8: balanced statistics and reproducibility | Largely addressed for local evidence. Equal paired comparisons and hashes are present. A referee-accessible bundle and precise statistical definitions remain submission requirements. |

“Substantially addressed” recognizes progress; it does not certify the complete absence of residual model uncertainty. The previous blanket blockers should not be reintroduced without reference to the revised evidence.

## 4. Major comments

### M1. Distinguish an exact field from a validated trajectory integrator

The exact closed-filament Biot–Savart field and the RADIA integrated-field comparison are convincing checks of the magnetic calculation within the declared geometry. They do not, by themselves, validate all features of the particle transport approximation. The tracking equations use paraxial slopes and a discretized drift–kick map. In `FilamentNKMKicker.apply`, the horizontal momentum is updated before the vertical increment uses it in the longitudinal-field term. This ordering is not proof of an erroneous result, but its effect is not covered by a convergence check of the nominal midplane horizontal exit momentum alone.

The saved convergence table reports `x_m` and `px_rad` for the earlier midplane reference point. The manuscript's vertical-loss contribution and offset transparency are precisely where off-midplane motion matters. Add a small independent comparison against integration of the same stated Lorentz/paraxial equations, with controlled tolerances, for representative final-point trajectories: nonzero vertical position/angle, angular-window edges and representative momentum offsets. Report exit differences in both planes, slice/span convergence and a tolerance tied to the reported window and transparency scale. State which aspects are exact and which are paraxial or numerical. An independent trajectory reference is sufficient; a second full production Monte Carlo campaign is not required if the discrepancies are demonstrably negligible.

### M2. Correct the survival duration and reconcile the capture definition

Section 5 currently uses `\SurvLong` both for the number of turns and the final survival percentage. That macro expands to **89.5**, so the sentence reads as tracking for 89.5 turns while calling this about one damping time. The existing duration macro `\SurvTurns` is **4000**. This must be corrected in the source and checked in the rebuilt PDF.

The saved evidence gives 93.0% survival at 500 turns, 89.6% at 2000 and 89.5% at 4000 for the long-turn study's 1000 particles. The 3.5 percentage-point late loss is scientifically relevant. Also distinguish the 93.0% obtained in that study from the separately validated four-bunch nominal estimate; identical rounded values are not the same ensemble.

The 0.74 mrad angular window, 80% threshold and combined-error means were defined at 500 turns. One nominal 4000-turn test does not establish those boundaries or ensembles at one damping time. Either keep all these results explicitly conditional on 500-turn survival and limit the conclusions accordingly, or check representative boundary/degraded cases at the longer duration. Provide uncertainty on the long-turn nominal survival from existing counts. Replace “bounded sensitivities” by “selected sensitivity studies” unless a genuine bound on a corrected machine is demonstrated: ten uncorrected error seeds and artificial uniform apertures are informative scenarios, not mathematical or operational bounds.

### M3. Recast the quarter-jitter result as a conditional statistical finding

The corrected curve gives 70.0% mean capture at quarter jitter and 69.7% with zero jitter. I recomputed their paired difference using the 50 matching nonnegative sample IDs, `fieldmap_3d` capture fractions, 10,000 bootstrap resamples and bootstrap seed 1729. Quarter minus zero is **+0.30 percentage points**, with a percentile 95% interval of **−1.50 to +2.15 points**. The raw inputs are `c6c_jitter_0.25/capture_robustness_raw.json` and `c6c_jitter_0/capture_robustness_raw.json` under `results/journal_campaign_02/`.

This supports “no difference resolved at the present precision.” It does not establish that jitter “costs nothing,” which the conclusion states without a qualifier. For an equivalence or acceptable-loss claim, specify a physically motivated margin and assess the paired interval against that margin. Do not infer equivalence from overlapping mean intervals or from an insignificant difference.

Nor does this curve establish that a future 80% mean necessarily requires jitter at most 0.125 mm and 0.05 mrad. The zero-jitter mean remains below 80%, and no successful joint tolerance allocation is shown. Present quarter jitter as a candidate operating target under the assumed budget, or demonstrate an allocation that meets a declared success criterion. Distinguish mean capture, median capture and the fraction of realizations exceeding 80%; they answer different questions. A mean near 70% with a median near 80% is not an 80% operating guarantee.

### M4. Describe what ideal steering actually removes

Section 7.2 says that, after ideal steering, “only the shot-to-shot errors remain.” That conflicts with both the implementation's limited correction of the static transfer-line reference trajectory and the later discussion of remaining static errors. Static optics changes, kicker/septum offsets and ring-orbit errors are not all erased by correcting the reference centroid at the septum exit.

Give the correction as an explicit transformation or concise algorithm: which reference trajectory is calculated, which position/angle components are subtracted, where this is applied, and which random quantities remain. Classify the table's terms as static or shot dependent, including energy, consistently with the sampling implementation. One joint draw per realization estimates performance across a distribution of machine/shot configurations; it does not separately estimate repeated-shot reliability on each fixed machine. State that distinction rather than requiring a nested campaign merely to retain a conditional joint-ensemble result.

Likewise, a small transfer-line Twiss mismatch is evidence of optical stability, not sufficient proof that optics errors are “minor for capture.” Rephrase that inference, or support it with an appropriate paired removal of optics errors. Partial rank correlations identify associations within the sampled model; they are not an independent causal tolerance allocation.

### M5. Label pulse diagnostics correctly and state the pulse phase

The later-turn positions and residual-field ratios in section 8 are generated from a linear betatron rotation in `pulse_macros`, as the supporting note acknowledges. The manuscript presents the positions as actual subsequent passages without this qualification. Given the large amplitudes and the article's reliance on native nonlinear tracking elsewhere, either label these as illustrative linear estimates or derive the positions from the selected model's tracked trajectory. One tenth of the angular-window width is a chosen engineering allowance, not a validated survival threshold for an additional kick at a different phase.

For a half-sine of total duration tau and injection at its peak, the relative kick reduction from a timing displacement dt is `1 − cos(pi dt/tau)`. The stated duration/jitter ranges, 5–8 microseconds and 1–5 ns, span approximately **7.7e−8 to 4.9e−6**, rather than the narrower stated range. Away from the peak the leading response is generally linear in timing displacement. Specify duration, phase and whether jitter is an rms quantity or a deterministic displacement before comparing this with the field-scale error budget.

Pulse width and repeat-pass suppression must also be consistent. An 8 microsecond half-sine sampled at its peak has about **0.50** of its peak field at the first return 2.666 microseconds later, exceeding the manuscript's illustrative first-return limit of about 0.19. This is a conditional example, not proof that every pulse scheme fails. Show at least one compatible pulse/phase example, or clearly retain these as preliminary requirements with feasibility outside scope. An operational efficiency claim would require time-dependent return tracking; the current ideal single-pass paper can instead keep its narrower scope.

### M6. Separate model limitations from implementation errors and qualify mechanism claims

The abstract says “Two effects that kick-map models miss.” A physical two-dimensional vector kick map can contain the vertical kick. The wrong vertical sign found in the older tabulation/implementation is not an intrinsic limitation of all kick maps. The real finite-length limitation is the neglected trajectory evolution in the longitudinally distributed field. Identify these separately in the abstract, discussion and conclusion.

Similarly, a nonzero horizontal gradient implies a nonzero vertical linear response under the stated Maxwell relation; whether that response focuses or defocuses depends on its sign and the sampled flank. “Defocuses ... wherever ... non-zero” is too general. Restrict the statement to the tested operating region. “Four results generalise beyond this design” should distinguish the general symmetry/field arguments from numerical thresholds conditional on the KLS lattice, error budget and selected point.

Finally, the controls are thin kicks calibrated to the finite-length NKM's nominal angular response. They do not reproduce every finite-length position/angle correlation. Their paired capture differences are useful model comparisons, but “separate the cost of nonlinearity” is stronger than this calibration alone establishes. Explain the residual transport difference or add a finite-length matched control if a pure decomposition is essential. The aperture comparison excluding the NKM vertical kick narrows the origin of losses to ring transport; call the detailed coupling mechanism an interpretation unless a ring diagnostic isolates it.

### M7. Make the transparency observable precise throughout

For the centered symmetric distribution, the centroid kick cancels by symmetry. That is different from saying the entire stored beam is undisturbed: a nonlinear kick can change particle actions and beam moments even when the mean vanishes. Use “zero centroid excitation by symmetry” where that is the result; quantify or bound the aligned moment change if claiming full transparency. Describe the near-axis cubic term as the leading term, not a purely cubic field over a finite region.

The stored-beam tracking implementation reports centroid amplitude as the maximum paired centroid difference during the **first 50 turns**, while the emittance ratio is evaluated at turn **1000**. State both observation windows, particle counts and seeds; avoid presenting the amplitude as a measurement at turn 1000. The Figure 7 caption says its right panel shows filamented emittance growth, whereas the dashed curve is labeled and generated as the kick-spread contribution. Distinguish immediate centered emittance growth, filamented coherent contribution and tracked final emittance. The tracked agreement is encouraging, but two 300-particle seeds do not justify excessive numerical precision or a universal 0.2 mm hardware tolerance.

## 5. Additional presentation and submission points

- Fresh-seed validation reduces selection overfitting; it does not prove that selection “is not biased by grid noise.” Describe the actual selection rule and independent evaluation.
- Add the statistical unit and interval method to each relevant caption: pooled particle Wilson interval, realization bootstrap interval, paired difference, or seed spread. Explain what uncertainty is conditional on fixed physics and what is not represented.
- Figure 7's four-bunch markers are closely overlapping and the NKM/dipole gap occupies a small part of its 0–100% axis. A small inset or paired-difference panel would improve readability without dropping the zero-kicker control.
- Identify the KLS lattice version/source and distinguish the ideal design lattice from a commissioned corrected machine. Make the assumed injected distribution and vertical emittance ratio easy to find.
- Local hash verification is good evidence hygiene. Before submission, provide the editor/referees with the frozen bundle, source/configuration versions and regeneration instructions through a stable archive or actual review attachment. A statement that it can be supplied later is weaker than a working submission artifact. A public DOI can follow journal policy; it is not necessary to fabricate one now.
- Update the claim-to-evidence table and a new round-two response after revisions. Preserve the previous response as historical evidence rather than silently editing its claims of closure.

## 6. Conditions for a favorable next decision

A revised version would be a credible candidate for acceptance if it validates the relevant off-midplane transport approximation, fixes and scopes the survival claims, reports the paired jitter uncertainty without an unsupported tolerance guarantee, describes correction and pulse assumptions accurately, and reconciles the model and transparency wording across the abstract, figures and conclusion. No measured hardware demonstration, new global optimizer or arbitrarily larger campaign is required solely to make this declared simulation study publishable.

The attached task register distinguishes evidence checks from editorial corrections. Completing it should yield a tighter physics article with defensible engineering implications rather than another expansion of the technical report.
