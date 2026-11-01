# Reviewer 1 — NKM manuscript, round 6

Date: 2026-11-01. Target: Physical Review Accelerators and Beams (PRAB).

Manuscript: *Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design lattice*, Chong Shik Park.

Reviewed checkpoint: `2c813feb0a09d7c7ba2505c722acf9431659028c`. Assessment perspective: accelerator beam dynamics, nonlinear injection magnets, tracking validation and statistical interpretation. This is an internal pre-submission assessment, not an editorial decision or a claim of commissioned performance.

## Recommendation

**Accept on scientific grounds within the stated model scope. I do not require another scientific revision or simulation campaign.** The fifth-round corrections resolve my outstanding objections. The additional two-plane jitter scan requested by Reviewer 2 supplies a useful negative result and is reported without converting it into an unsupported hardware tolerance. Two optional presentation improvements are listed in the [companion checklist](review_round_06_reviewer_01_tasks.md); neither conditions this recommendation.

The article makes a defensible specialist contribution: it quantifies the error of a single thin kick map in an angle-cancelling geometry and investigates how static vertical injection errors, booster jitter and operating-point choice affect capture. Its value does not depend on demonstrating a superior injection system. The low robustness under the assumed budget is scientifically informative when its population, correction model and limitations remain explicit, as they now do.

## Materials and version identity

I read the current article and supplement sources, the rendered article text, and all five joint author responses:

- [Round 1](review_round_01_author_response_to_reviewers_01_02.md): field/sign conventions, finite-length mechanism, controls and initial sensitivities.
- [Round 2](review_round_02_author_response_to_reviewers_01_02.md): design beam, physical chamber, corrected-ring scenarios, independent integration, inference and evidence.
- [Round 3](review_round_03_author_response_to_reviewers_01_02.md): contribution against established tracking methods, diagnostic scaling, corrected optics and point selection.
- [Round 4](review_round_04_author_response_to_reviewers_01_02.md): paired ablation, steering interventions, point comparisons, losses and current-point pulse/transparency.
- [Round 5](review_round_05_author_response_to_reviewers_01_02.md): recovery-budget labels, chamber correction, companion-model audit, five-level two-plane scan and final evidence reconciliation.

I also examined the fifth-round reports, consolidated register, protocol, precise companion audit, selected raw records, statistical analyzer, generated macros, provenance and verification receipts. The two-column page containing Table VII/Figure 10 and the point-comparison table was inspected visually. The installed layouts have 36/18 pages and the supplement seven; the extracted abstract has 250 whitespace-delimited words.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `f9e8dc4603b56d5913e453299c98b26a0cad61f012a5820f4fac1d493cb6e5e7` |
| `paper.pdf` | `91d0043489195330788de06c367efd68ba54d26d40553e6ba82a505c8b0bcb3f` |
| `paper_twocolumn.pdf` | `caeed92a1611a36cf77bb51d1dcc9a0de67d5bedff1dc221cb992e4d56b44b85` |
| `supplement.tex` | `936f36cd37432d9828e11fee64b1400103dc142e98d0e6be821fe279fc708ab3` |
| `supplement.pdf` | `e6147e7dca6f78b255f48c19abb209ed3746d370baefc966eae64c416731cdbd` |
| `revision_manifest_round5.json` | `9a6392fb71cc46d7eb62a390742fc17a67a2bc6142ec9f74ac2cc92bdfa53bd2` |

Older responses describe older configurations. In particular, the earlier booster-angle attribution, rms labels and chamber-location wording must be read with the explicit fourth-/fifth-round corrections. Preserving those historical documents is appropriate; they do not override the current evidence.

## Disposition of previous concerns

| Concern | Round-6 assessment |
| :--- | :--- |
| Controlled field/tracking model | Resolved for the stated filament geometry and paraxial equations. RADIA-integral agreement, adaptive integration and slice/span checks support numerical consistency; they do not validate an as-built pulsed magnet. |
| Novelty and generality | Resolved within the adopted scope. Established segmented tracking is credited. The empirical sagitta fit is restricted to the tested diagnostic launches and related wire families. The 161 microradian production-trajectory error is compared with an explicit 0.044 mrad analysis allowance. |
| Chamber, corrected rings and survival | Resolved as conditional scenarios: physical apertures, ten corrected rings, lack of skew correction, 500-turn capture and selected 4000-turn checks are distinguished. No commissioned efficiency is claimed. |
| Attribution and operating point | Resolved by paired alone/omitted interventions, ideal two-plane removal and recalibrated point comparisons. Associations are exploratory. Retaining the selected point does not establish equivalence, optimality or an error-inclusive optimum. |
| R1E-01 — recovery budget | Closed. Abstract and conclusions distinguish the 150-draw horizontal-only 16.1/44.1% means from the paired 50-draw full-budget 33.9/57.2% two-plane sensitivity. The 76.6% recovery explicitly excludes booster jitter and has the paired 40.13% horizontal-only baseline. |
| R1E-02 — chamber interception | Closed. Section V acknowledges later interceptions at the NKM chamber. The ring-5501 evidence contains 133 NKM and 154 dipole interceptions at the magnet halves. Widening 3.8 to an infeasible 15 mm gives only 29.8→33.2% and 33.2→37.6%; the location of interception is separated from its driving dynamics. |
| R1E-03 — reconciliation | Closed locally. Final sources/PDF identities, manifests, claim locations, response, packages and frozen attachment are identified. The scientific snapshot and later completion receipts are distinguished honestly. Actual delivery remains separate. |
| Reviewer 2's additional fifth-round requests | Substantively answered: both steering headlines, beam-size jitter units, paired scan, nonidentical companion error correlations, statistical definitions, historical strength labels, dates and scoped tuning/correction claims. This assessment does not speak for Reviewer 2. |

The decision not to call ideal two-plane translation a universal upper bound is justified. No optimization argument establishes that every possible correction must capture less. Likewise, the companion's horizontal residual does not determine a vertical hardware penalty. An optimistic ideal static-removal benchmark is an accurate description.

## Assessment of the new two-plane jitter result

The complete scan retains 50 paired seed-42 realizations, 200 particles per realization, 500 native turns and the same corrected-ring identities. Position and angle jitter scale together. Full stress corresponds to 0.5 mm / 0.2 mrad at extraction, about 1.3 / 2.2 nominal rms beam sizes including dispersion. These are assumptions, not supplied machine specifications.

| Scale | NKM mean [%] | Uniform-kick mean [%] | NKM change from zero [points; 95% CI] | NKM − uniform [points; 95% CI] |
| :--- | ---: | ---: | :--- | :--- |
| 0 | 76.57 | 82.64 | reference | −6.07 [−8.89, −3.64] |
| 0.1 | 74.22 | 82.86 | −2.35 [−4.32, −0.66] | −8.64 [−12.53, −5.39] |
| 0.25 | 65.25 | 80.99 | −11.32 [−16.55, −6.58] | −15.74 [−21.25, −10.59] |
| 0.5 | 51.54 | 74.30 | −25.03 [−33.12, −17.18] | −22.76 [−29.93, −15.96] |
| 1 | 33.91 | 57.22 | −42.66 [−51.39, −33.84] | −23.31 [−31.74, −14.99] |

No nonzero tested scale establishes the declared acceptable loss of less than one point. At 0.1 the interval crosses the −1-point margin: noninferiority is not established, but a loss exceeding that margin is not established either. At quarter jitter the entire interval lies below the margin. The paper's general statement that no nonzero sampled level passes is correct; the result does not prove that all smaller jitter levels fail. The zero row is a reference, and these pointwise intervals do not locate a continuous threshold.

The quarter-jitter model gap directly answers Reviewer 2's question. It is distinct from the NKM's own jitter cost. The remaining zero-jitter gap is also retained, so the steering intervention is not described as complete recovery to uniform-kick performance. The joint distribution remains conditional on the ten rings and one sampled machine/shot draw per realization; it is not a commissioning-population estimate.

The companion-model reconciliation is stronger than a sampling explanation. Nominal strengths and geometry agree, but a common bend-field draw here differs from independent per-bend draws there. The NKM's 0.90 mm / 77 microradian figures are population standard deviations, whereas the companion quotes rms centroids from another population and numerical treatment. The current wording makes these distinctions. Numerical agreement between the papers need not be forced.

## Remaining limitations and presentation

The design lattice, assumed chamber/IVU assignments, unsurveyed incoming transport, ideal steering, limited ring population, deterministic damping without quantum excitation, finite capture window and approximate pulse treatment all limit transfer to hardware. Manufacturing errors require compensation, and the joint capture campaign does not include individual-wire errors. Compensation hardware, full time-dependent fields, coupling correction and error-inclusive optimization would support a future engineering study. They are not new acceptance conditions for this bounded methods-and-mechanism article.

The manuscript is dense, but its main chain is now identifiable: model accuracy, operating region, physical acceptance, transparency, joint-error behavior and paired attribution. The new table and figure are readable. I suggest only two optional refinements: use “not established” instead of the bare “fail” in the loss-test column, and repeat the steering/population label in the standalone comparison-table row containing 16.1%. Neither corrects an unsupported scientific conclusion. See the companion checkbox list for exact scope.

## Fresh checks and their limits

Performed for this review, with outputs under `results/nkm_reviewer1_round6_20261101/`:

- All **272 selected artifact-key hashes** and the current scientific source/PDF identity record match. Artifact keys are not counts of independent experiments.
- Direct reconstruction from raw captured/incident particle counts independently reproduces the five-level NKM costs, paired model gaps, bootstrap intervals and one-point decisions (10,000 resamples, seed 1729).
- A fresh paired analyzer run reproduces the selected analysis JSON byte for byte and checks scientific job fields, latent-error invariance, particle/ring pairing and loss accounting.
- A fresh full figure/macro rebuild reproduces the installed macros byte for byte; no assets were installed.
- The frozen archive digest matches `098def595a17cf2ad33955cde2c466b8cc39d9e6f90db45fa1c11235c7463ab3`, and all **280 inventory entries** verify by reading archive members.
- **30 relevant tests pass** across round-5 inference, round-4 protocol, source packaging and journal figures.

The 775-test full-suite run, clean TeX builds and archived-code execution are recorded in the preceding revision's receipts; they were not repeated as part of this review. I did not run new tracking, optimization, a remote-access check or an exhaustive new literature audit. Reproducibility checks do not establish the realism of assumed hardware inputs.

## Final decision and submission gate

I recommend **acceptance of the scientific article in its present scope**, with the two optional copyedits left to the author. No higher capture target, extra ring seeds, lower-jitter scan or global search is required by this review. The [existing G7 gate](revision_round_05_plan_for_review_round_05.md#g7--submission-stage-author-gate) remains deferred: final author approval, declarations, actual access to the named repository/ignored attachment and delivery must be confirmed at submission. This scientific recommendation neither performs nor guarantees journal acceptance.
