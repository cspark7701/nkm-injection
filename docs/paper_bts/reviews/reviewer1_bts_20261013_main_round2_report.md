# Reviewer 1 — BTS main-branch manuscript, second assessment

Date: 2026-10-13. Internal pre-submission assessment, written from the perspective of an accelerator-physics referee. This is not a journal decision or a representation of an appointed journal referee.

**Recommendation: major revision; I would not recommend acceptance in its present form.** The revised study is more credible and substantially better bounded than the earlier draft. A publishable parametric research article is possible, but its scientific contribution and observable-level validation need strengthening. Further large particle counts alone would not address the principal concerns.

## Manuscript reviewed and review scope

Title: *Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line*. Author: Chong Shik Park. Prospective journal: Journal of the Korean Physical Society (JKPS).

Reviewed local `main` at `742b940`, including the complete TeX, eight-page PDF text and rendered page montage, bibliography, generated summaries, claim ledger, model/validation/comparison notes, relevant transport and comparison code, and saved machine/shot results. The original main-branch review and point-by-point response were consulted. The restored BTS-branch reports concern another manuscript version and do not supply acceptance evidence for this article.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `c1966ad65ac1d8fb78cb71bd8839e45c318e60470a437031a3fc655665eb69f3` |
| `paper.pdf` | `161565288d9bf03eba55815980d1f60703e69720691b5d0b2dff725b3a418566` |
| `paper.bib` | `ebfa36249d60cf878f605485b8e3a0ac9370dca1d813443b5a8ac5c908597162` |

`python scripts/package_bts_revision.py --verify` passed. Using NumPy on the saved 200 paired machine means, I independently reconstructed the 10,000-replicate percentile bootstrap with seed 71004: mean change **0.0146103 mm**, interval **[-0.0179072, +0.0483232] mm**. The saved 600-shot records contain zero observed particle losses for both designs. This review did not rerun transport, optimization, the full simulation campaign or the test suite: the active interpreter lacks pyAT and the installed project package. Prior recorded tests and reproduction checks are distinguished from checks performed for this review. Hash verification establishes asset identity, not physical validity.

## Evaluation and improvements already achieved

The article now asks a specific physical question and reports an honest conditional negative result. It separates optical matching, aperture-station transmission and downstream ring capture. It withdraws unsupported chamber, hardware, correction-knob and power-dissipation interpretations. The complete beam covariance includes dispersion and roll-induced coupling. A common-random-draw paired design and machine-level bootstrap avoid treating millions of particles as millions of independent machines. The failed original integration tolerance and historical stopping limitations are retained rather than concealed.

The layout is readable and the article is concise. Existing evidence supports the numerical statement that these two settings have no resolved **mean minimum-station-clearance** benefit at the reported precision. It does not yet demonstrate a broadly useful design criterion, a comparison with clearance-based design, or accuracy of that small difference under the complete error distribution.

## Major comments

### M1. Distinguish a useful physical result from saturation of the chosen metric

Sections 2.2, 3.2 and 4.2 minimize clearance over four stations including an entrance unaffected by downstream quadrupoles. At zero error, both settings therefore encounter the same entrance ceiling, 17.4546 mm. This follows structurally from the metric; it is not evidence that lower beta cannot benefit downstream restrictions.

The manuscript recognizes this limitation, but does not quantify when the entrance dominates or which other station/plane replaces it. Saved results show **406/600 shots** with exactly equal paired minima and **93/200 machines** with exactly equal machine averages. Machine-average differences range from **-0.92289 to +1.40103 mm**. Equal values suggest metric saturation, but the saved scalar results alone do not prove the active station in every case. The near-zero mean can also hide substantial changes in opposite directions.

Provide station/plane-resolved nominal and held-out clearances, active-limit frequencies and paired distributions. Explain the zero-difference mass and compensating gains/losses. Establish the entrance bound analytically and then demonstrate a regime in which another restriction is active, through a clearly labelled parametric aperture/beam sweep or confirmed geometry. A study of hypothetical restrictions is acceptable if it remains explicitly parametric. Do not remove the entrance from the headline metric merely to manufacture a gain.

### M2. Establish the contribution beyond one low-beta alternative

The conclusion recommends optimizing the actual limiting observable, but only a reference setting and a single-start vertical-beta minimization are evaluated. No clearance-based optimization is demonstrated. The alternative also reaches q32 = -3 m^-2, an active assumed bound. The present evidence supports an example, not an optimal design rule or a general comparison of strategies.

Add a modest, fair comparison against a nominal or training-based clearance objective under the same exit constraints, K bounds and beam assumptions. If the entrance ceiling makes optimization degenerate, show that degeneracy and compare downstream profiles as secondary diagnostics. Report finite search budgets and all outcomes; no global-optimum assertion is needed. Explore at least one non-entrance-limited parametric case. Freeze all new settings before a new independent validation ensemble. The previously inspected held-out set must remain a historical test set, not become a silently reused untouched test.

A verified engineering target would strengthen the article, but experimental commissioning is not intrinsically required for a bounded parametric paper. Without hardware provenance, the transferable physical analysis must carry the contribution. State what this analysis adds to established transfer-line envelope, dispersion and trajectory-control practice.

### M3. Validate the clearance observable at the claimed scale

Section 3.1 reports excellent nominal integration convergence, but perturbed validation is materially weaker: the exported maximum map discrepancies are approximately **1.3869e-4** for offset and **5.3553e-4** for dipole errors, accepted against **1e-3**, compared with **2e-6** nominally. These are maximum entries across a map with mixed coordinate units, not clearance errors. They cannot be converted directly into micrometres or compared directly with 0.0146 mm.

`clearance_profile` uses independent affine maps; `independent_element_map` adds translations and dipole forcing but does not implement the full nonlinear chromatic dependence retained by AT. Offset and dipole cases already reveal derivative discrepancies even where orbit agreement is excellent. The nominal 50,000-particle RMS check and two delta probes are useful, but do not establish accuracy of the paired clearance statistic for both settings under simultaneous errors and shot momentum offsets.

Compare independent-map and AT-derived local centroids/covariances/clearances at every aperture for both designs on representative combined-error cases. Include expansion about the actual shot centroid, step/integration convergence and a check of chromatic covariance effects against particle tracking with its sampling uncertainty. Quantify discrepancy in the paired mean and active-station classification. Require numerical/model approximation error to be small relative to the reported confidence interval or widen/qualify the interpretation accordingly. Do not mistake the 2% RMS acceptance threshold for certification of a 14.6 micrometre effect.

### M4. Check spatial resolution of the beta objective

Sections 3.2 and 4.1 correctly label peak beta as element-boundary sampled. Nevertheless, the central quantitative improvement, 50.75 to 28.18 m, and constrained alternative depend on that sampling. Thick quadrupoles and bends can contain interior extrema. Temporal/integration-step convergence does not establish spatial convergence of a maximum evaluated only at element boundaries.

Evaluate interior beta/envelope profiles with analytic extrema or converged subdivisions, keeping source inputs unchanged. Report whether the optimum, equality residuals, horizontal screening and active restrictions change. If optimization is still boundary-sampled, distinguish its objective from the refined physical profile rather than calling it the full peak.

### M5. Define the inferential target and practical effect

The paired machine bootstrap is appropriate for the explicitly sampled three-shot block. The text appropriately avoids equating a zero-crossing interval with equivalence. Add the machine-level dispersion and gain/loss frequencies from M1 and identify a physically justified minimum relevant clearance change before interpreting new results. Three shots per machine are a sampling design, not a representation of indefinite operation.

The 1.4867% zero-loss upper bound applies to the probability that a randomly generated **three-shot, 2,000-particle-per-shot machine block** contains an observed loss under this model. It does not bound the probability that a machine ever loses a particle. Keep that event definition explicit. The descriptive particle-binomial bound is already caveated; moving it to supplementary material would reduce emphasis on an independence assumption that the experiment does not satisfy. More particles or an arbitrary million-sample tolerance run are not required by this comment.

## Presentation, attribution and submission comments

1. Section 4.3 is an unusually prominent historical statistics audit for a paper whose new result uses another beam configuration and observable. Move detailed pooling, median-prefix and legacy OAT results to a supplement, retaining only their scientific distinction from transmission in the main text. Preserve all original data and audit records.
2. Figure 3 should show where the clearance is limited, rather than relying on a beta comparison and one aggregate histogram. Supply a compact table of station/plane clearances and a clear interval on the primary effect. Avoid decimal precision unsupported by model accuracy. Figure 2 could overlay the two settings where it clarifies the mechanism.
3. `literature_comparison.md` describes the contribution as maximizing five-sigma clearance, whereas the article/code optimize vertical beta. Correct this supporting-document inconsistency now; only claim clearance maximization if M2 actually implements it. Update the claim ledger for revised/expanded conclusions.
4. Supplement the Wilson citation with an authoritative reference for the exact binomial interval used, and complete/verify the ESRF report date and conference metadata where primary records permit. Maintain protected capitalization in bibliography titles. The SLS 2.0 primary report supports separate beam characterization and trajectory control; it does not establish this model's hardware boundaries.
5. The current author-confirmation placeholders are submission blockers. Funding is already deferred by the author and must not be invented. Confirm competing interests, acknowledgments, contributions and scientific approval; provide reviewer-accessible evidence with a stable availability statement. Preserve the generative-assistance disclosure and human responsibility.

## Journal assessment and acceptance conditions

JKPS remains a plausible venue for a concise accelerator-physics parametric Research Article, conditional on demonstrating scientific insight beyond an insensitive minimum metric. I would not recommend acceptance based on task completion or the restored branch's favorable historical reports. The technical checks are valuable, but reproducibility does not substitute for the contribution.

Major revision is justified by M1–M4, rather than missing declarations alone. Acceptance could be reconsidered if the authors establish the limiting-station mechanism and a transferable design comparison, validate clearance at the relevant numerical scale, check spatial extrema, and align the claims with the bounded inference. A negative result is acceptable; an unresolved effect in one arbitrary configuration needs a stronger explanatory framework. Completion of the tasks is not a guarantee of acceptance by an editor or other referees.

## Primary sources checked for this assessment

- [JKPS submission guidance](https://link.springer.com/journal/40042/submission-guidelines): mathematical LaTeX submissions are allowed, relevant declarations are required, and author accountability extends to generative assistance. Concise Research Article formatting is encouraged.
- [Kallestrup and Schlott, SLS 2.0 transfer-line study, IPAC25 TUPM056](https://proceedings.jacow.org/ipac2025/pdf/TUPM056.pdf): primary context for measured characterization and trajectory control. No facility dimensions are imported into this model.

The attempted direct IPAC24 TUPC12 PDF retrieval failed during this assessment; the inherited beam-source citation was read locally but its numerical inputs were not newly verified against that primary PDF. No acceptance finding rests on pretending otherwise.

See the [ordered revision register](reviewer1_bts_20261013_main_round2_revision_tasks.md).
