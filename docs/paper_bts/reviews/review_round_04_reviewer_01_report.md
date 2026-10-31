# Reviewer 1 — fourth assessment of the main-branch BTS article

Date: 2026-10-31. Reviewed scientific checkpoint: `6a968f86fbbaff286d3c00a31adf11167552e6cc`.
Title: *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*.
Author: Chong Shik Park. Journal context: prospective JKPS submission; the author has not yet selected between
JKPS and NIM A. This is an internal pre-submission assessment, not a journal editorial decision.

## Recommendation and answer on acceptability

**Minor revision. The scientific study is acceptable in principle for publication as a conditional accelerator-design article, subject to the corrections below. I do not recommend unconditional acceptance or submission of the present files.**

The round-four work answers my previous substantive objections. The nominal matched-end theorem is now separated
from error realizations; round-aperture probabilities are repaired; the mean-clearance explanation is uncensored;
and the phase-advance result is supported by additional constrained searches without a global-optimality claim.
The new jitter and blade-distance sweeps make the regime of the result much clearer. The contribution is the
quantitative design trade for this specified line and beam, not a new optimization algorithm or a commissioned
KLS transmission prediction. This is sufficient scientific scope for the present assessment.

The remaining corrections mainly concern population definitions, overbroad accuracy wording, two contradictory
conclusion sentences, and submission/provenance details. They can largely be made from existing evidence. I do
not request another major campaign, a larger error population, ring tracking or hardware commissioning.
A source for actual KLS booster jitter would improve practical relevance, but it is not a prerequisite for an
honestly labelled stress study. The recommendation is conditional; it is not a guarantee of journal acceptance.

## Material considered

I read all seven author-response documents available in the BTS review directory:

- Main-branch [first response](review_round_01_author_response_to_reviewer_01.md),
  [second response](review_round_02_author_response_to_reviewer_01.md),
  [response to Reviewer 2](review_round_02_author_response_to_reviewer_02.md), and
  [joint round-four response](review_round_03_author_response_to_reviewers_01_02.md).
- Restored historical BTS-branch [response 01](historical_branch_review_round_01_author_response_to_reviewer_01.md),
  [response 02](historical_branch_review_round_02_author_response_to_reviewer_02.md), and [response 03](historical_branch_review_round_03_author_response_to_reviewer_03.md).

The three restored documents describe another manuscript version. Their acceptance statements, aperture claims,
beam parameters and proposed engineering conclusions are historical, not validation of the current article.
For the current scientific decisions, the four main-branch responses and their actual evidence take precedence.

I reviewed the article TeX and extracted PDF text (19 pages), the nine-page supplement, the two round-three
reports, consolidated R4-BTS register, new protocol/reproduction guide, relevant model/driver/exporter code,
generated tables and selected saved summaries. I inspected rendered pages containing the new test and phase
figures. I checked the raw numerical identities supporting the observations below; I did not repeat the full
simulation, optimizer searches, bootstrap inference, TeX builds or referee-increment extraction.

Read-only checks performed for this review:

- `audit_bts_evidence.py`: **63 claim pointers and 45 artifact identities verified**.
- `package_bts_revision.py --verify`: **75 selected final-asset hashes verified**.
- Two existing circular/elliptical-probability tests: **2 passed, 14 deselected**, including the isotropic limiting
  case and the offset/correlated Gaussian case. This is a focused check, not a repeat of the recorded 768-test suite.
- Arithmetic on `final_test_b/final_test.json`: counts, conditional predictions and jitter-integrated values
  distinguished explicitly below. No new simulation or bootstrap samples were generated for these comparisons.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `45edf6a9b7a544ef8498090335fed9e702cbb0c92dfdd4eec40fb3c6405936a0` |
| `paper.pdf` | `4e5a4cf8d6af21976e8d849f63f7c4bf31d7288d9206a6a979f8f4030c37da63` |
| `supplement.tex` | `4d4a29c9f80effcca8b51e288bc152781396c640c98e5d9886695ee3fefcceff` |
| `supplement.pdf` | `2fea85ad8f1bc3dae9168a7d0ac5167fb83d632b075b8630911ef3f07dfba5ee` |
| `paper.bib` | `0a2210e5b160b3ab804a45f6f284aa2d07e7faf2af9897116545436486129830` |

## Disposition of my previous requests

| Previous item | Assessment after the joint response |
| :--- | :--- |
| R3-BTS-01: boundary theorem | Scientifically addressed in Sections 3.1–3.2. Keep the same nominal-model qualification in the abstract and interpretation (C2). |
| R3-BTS-02: circular probability bounds | Addressed. The exact Gaussian event replaces the chord recipe; the limiting-case test now passes. The 66-number recheck is recorded as unchanged. The mathematical event is exact for the Gaussian model; finite angular quadrature and linearized transport remain numerical approximations. |
| R3-BTS-03: discrete aperture checks | Addressed by narrowing the claim to the declared check locations; no continuous interception claim or modified production lattice is needed. |
| R3-BTS-04: mean clearance/statistical language | Substantially addressed by uncensored means, the mean-versus-variance argument and paired intervals. Two conclusion statements still need reconciliation (C3). |
| R3-BTS-05: sampled search | Addressed by constrained phase scans, explicit termination records and sampled/local scope. Figure 4 retains an older legend label (C4). No global proof is required. |
| R3-BTS-06: pairing/precision | Design-specific reading noise and shared shot/particle draws are now disclosed. Clarify nominal transfer equivalence versus perturbed-line response (C2), and restrict the accuracy claim to the rows that meet it (C1). |
| R3-BTS-07: self-contained submission | Scientific definitions and supplement naming are improved; target venue, availability wording and author approval remain open (C5). The jitter is now explicitly a stress input, so a missing measured specification is a limitation rather than an invented completion. |
| R3-BTS-08: reconciliation | Substantial execution is documented and local identity checks pass. Final reconciliation must follow the small corrections requested here (C6). |

Reviewer 2's central jitter objection also receives a useful answer: at 0.1–0.2 times the stated betatron jitter,
the Gaussian model predicts negligible blade loss for all three matched settings. The large loss-reduction
factor is therefore not promoted as a measured operational gain. The baseline is retained as an unmatched
starting point rather than evidence for superiority over a competing optical design. These changes improve
both relevance and fairness.

## Remaining corrections

### C1 — Separate conditional particle predictions from the jitter-averaged design quantity

**Required; Section 4.4, Table 7, the accuracy summary and conclusions.**

The new evidence contains three different quantities:

1. The observed loss on 600 sampled shots, with 2,000 particles each.
2. The Gaussian prediction conditional on those same shots, averaged over the realized centroids and beta factors.
3. The jitter-integrated quantity on each steered line, evaluated using the nominal beam covariance and an
   analytic Gaussian centroid distribution, without sampling those 600 jitter values or their beta-factor mixture.

Only (1) and (2) directly test particle-count consistency for the sampled shots. Quantity (3) is useful for the
unconditional design comparison, but it has a different sampling/approximation definition. The following values
come directly from the selected second-test summary. All probability columns are **percent**:

| Setting | Observed count / 1,200,000 | Observed loss | Conditional Gaussian prediction | Jitter-integrated quantity |
| :--- | ---: | ---: | ---: | ---: |
| Matched reference | 11,673 | 0.97275 | 0.97544 | 1.32260 |
| Low beta | 10,305 | 0.85875 | 0.85826 | 1.20265 |
| Loss-based (R3) | 1,022 | 0.08517 | 0.08079 | 0.28450 |
| Phase edge | 1,564 | 0.13033 | 0.12400 | 0.29160 |
| Dispersion-free | 1 | 0.00008333 | 0.00002253 | 0.00615461 |

The new loss-based and phase-edge rows differ from their conditional Gaussian mean predictions by about
**5.14% and 4.86% relative to the observed fraction**, respectively; the scan-grid row differs by about 1.98%.
Consequently, the general statement that mean tracked losses agree "within 1% relative" does not cover the new
second-test rows. Restrict it to the earlier rows actually checked, or report conditional prediction/count
uncertainty for the new test rather than imposing a fixed relative tolerance on sparse counts. These differences
alone do not establish model failure; finite conditional particle sampling must be considered.

For the dispersion-free row, the conditional expected count is **0.2704**, whereas multiplying the
jitter-integrated mean by 1.2 million gives **73.86**. The difference is explained by the different conditioning
and potentially rare shot centroids, not by non-Gaussian tails in a simulation that itself draws Gaussian inputs.
One observed loss is not validation of the integrated rare-tail probability at a specified relative accuracy.
Replace the unqualified phrase "consistent with its jitter-integrated prediction" by the appropriate conditional
comparison and state that the finite shot sample does not precisely determine the unconditional tail. Show both
predictions in the text/table or point directly to the numerical evidence. No extra particles or shots are needed
merely to make a rare-tail ratio look better.

Also qualify "exactly averaged" as exact Gaussian averaging within the chosen linearized-transport,
nominal-beam-covariance model, using the stated marginal-event surrogate. The driver computes `clearance_and_loss`
at the combined covariance; that is not a universal exact nonlinear line-union probability or an average over
the test's beta-factor mixture. Likewise, non-Gaussian booster tails **could** matter if present; their dominance
has not been established by these Gaussian calculations.

### C2 — Preserve the scope of phase-only transport and avoid unsupported attribution

**Required; abstract, Section 4.3 and Table 7 caption.**

The relation Mx = B4 R(mu_x) B1^-1 fixes the nominal horizontal end-to-end betatron transfer once the boundary
functions and mu_x are specified. It does not imply that different quadrupole vectors have identical interior
optics, vertical phase advance, coupling/error sensitivities, steering response or measurement-noise realization.
The phase-edge and older loss-based settings have different strength vectors. Call them nominal-horizontal-
transfer-equivalent to the reported precision, rather than generically "optically identical".

They share the sampled entrance jitter and particle variates. The jitter tail can amplify differences in their
perturbed transport and steering, but is not by itself an independent paired random input distinguishing them.
Different reading errors are a plausible contributor to their different counts; a unique attribution requires a
control that also holds those errors fixed. The proportionate correction is to state that perturbed-response and
reading-noise differences are not decomposed here. I do not require a new steering campaign unless the author
retains an exclusive causal attribution. Keep "loss depends on mu_x alone" explicitly restricted to the nominal
Gaussian blade-loss model in the abstract as well as in the methods.

The low-jitter design message also needs to retain the residual delivery errors. In the saved jitter sweep at
scale 0.1, the matched-reference exit centroid RMS is about **0.179 mrad horizontally and 1.073 mm vertically**;
the nominal transported horizontal jitter, including the retained momentum jitter, is only **0.0574 mrad**.
The small blade loss therefore does not mean that the delivered centroid distribution is controlled solely by
the nominal position–angle partition. At that level, steering/reading residuals and the uncorrected vertical
trajectory matter for downstream injection. State this with the existing results; a new correction system or ring
capture study is not required to retain the BTS-only scope.

### C3 — Remove the remaining contradictions in the conclusions

**Required; Discussion and conclusions, with a brief check of the response wording.**

- The sentence saying lower interior beta "on fresh steered error realizations, leaves the loss unchanged" is too
  strong. Table 7 gives low-beta minus matched reference **−0.114 percentage points**, with stored paired interval
  **[−0.24434, −0.00941]**; the earlier fresh test had an unresolved change, and the original steering comparison
  also resolves a small loss reduction. Say that vertical-peak reduction alone does not determine the gain, while
  the accompanying horizontal phase change can produce a small, population-dependent benefit. Do not claim
  equivalence or a general absence of benefit.
- The statement "The dispersion-free results are analytic" is outdated after the new tracked row. Distinguish the
  analytic scan/integrated predictions from the 1.2-million-particle test. Do not discard the new unfavorable
  precision limitation or describe the whole result as untracked.

These are consistency corrections, not grounds to reopen the successful baseline/matched framing or demand a
positive low-beta result in every population.

### C4 — Correct the remaining provenance and figure labels

**Required, documentary; no new physics run.**

`generated/round4_phase.json` records its `test_source` as `.../final_test/final_test.json`, which does not exist.
The exporter actually loads `final_test_b/final_test.json`, and that correct file is hash-selected in the evidence
manifest. Correct the exporter/source pointer and regenerate the affected provenance with refreshed hashes.
This is an identifiable pointer defect, not evidence that the selected data are absent or fabricated.

Figure 4's rendered legend still says "reachable" although its caption and the new scan correctly use found
ranges. Align that label with the sampled/local scope. Update the current checklist and index: they still mix
12/eight-page and in-progress language with the completed 19/nine-page revision. Preserve dated reports and
original task registers; do not retrospectively mark their review-time statements as current decisions.

### C5 — Close the author-dependent submission gates

**Required before submission, separate from scientific completion.**

The joint response openly leaves the target journal, data-access wording and final author approval undecided.
That means R4-BTS-08 is prepared/partly open, not an unconditional submission-readiness pass. Preserve the supplied
funding and competing-interest statements; do not invent approval or a public deposit. A measured jitter source
may be added if available, but a specified Gaussian stress level is acceptable for the scoped paper.

For JKPS, the [official submission guidelines](https://link.springer.com/journal/40042/submission-guidelines),
checked 2026-10-31, require original research to include a data-availability statement. The current article still
has none. The author should choose wording consistent with the actual attachment/access route and confirm the
journal before submission. This review does not restore author-removed text, upload data, send a manuscript or
claim that a DOI is mandatory. Other publisher-specific requirements must be checked once the author selects
the venue. The present scientific recommendation is not a new journal-selection decision.

### C6 — Final reconciliation and a concise presentation

**Required final check; shortening is a recommendation rather than a scientific acceptance condition.**

After C1–C5, prepare a short new response identifying the corrections, rebuild the article/supplement, refresh the
claim and asset identities, and update the selected referee increment. Recheck only the methods actually changed;
no new full simulation campaign is requested. Preserve the previous responses and selected old campaigns.
Author approval and actual submission/delivery must remain separately recorded.

The 19-page manuscript is readable but longer than necessary. If targeting JKPS, its current guidance recommends
concise Research Articles, approximately 4,000 words and up to six figures, while explicitly declining a strict
word/page limit. The PDF text before references contains about 9,300 whitespace-separated tokens including
captions, tables and mathematical text; that is not a formal journal word count. A manual word count and moving
historical/setup detail to the supplement would help. There are already six main figures. I do not impose a
19-page rejection rule or require removal of the stress-case limitations.

## Conclusion of this review

The prior major objections have received substantive answers, and the conditional physical result is now clear:
nominal matched endpoints fix the blade envelope, while phase advance chooses how large assumed centroid jitter
is delivered to position and angle. The response also makes clear when blade loss becomes negligible. I would
recommend acceptance after a satisfactory minor revision addressing C1–C6 and the author-dependent submission
gates. I do not see a need for another major scientific revision on the evidence inspected. This remains a
referee-style recommendation, not a journal acceptance or permission to submit.

A [checkbox task list](review_round_04_reviewer_01_tasks.md) separates the required corrections,
submission decisions and optional shortening. All new tasks remain pending.
