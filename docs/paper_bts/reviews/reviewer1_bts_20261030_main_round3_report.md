# Reviewer 1 — third assessment of the main-branch BTS article

Date: 2026-10-30. Reviewed checkpoint: `603c3abedda3dede9e032d68dbe48896f347e5ca`.
Title: *Optical matching and beam loss in the Korea Light Source Booster-to-Storage transfer line*.
Author: Chong Shik Park. Prospective journal: Journal of the Korean Physical Society (JKPS).
This is an internal pre-submission referee-style assessment, not an appointed journal referee's decision.
It is Reviewer 1's main-branch round 3, distinct from the restored BTS-branch `reviewer_report_03.md`.

## Recommendation

**Focused major revision; I do not recommend acceptance in the present form.**

The paper now has a credible, potentially publishable physical result: matching improves the nominal baseline,
while a separate loss-based choice within the matched solution set reduces blade losses on independent error
realizations. It has progressed beyond the earlier optics/statistics report. My remaining objections concern the
validity and scope of several analytical statements and their interpretation, rather than a demand for higher
transmission or a larger simulation campaign. In particular, the stated general loss bounds are not valid for the
implemented circular-aperture approximation, and the matched-boundary argument is extended incorrectly to error
realizations. Those issues require a substantive response even though the blade-dominated tracked comparison
itself remains supported. A limited revision may suffice; acceptance is not guaranteed by completing a task list.

## Review basis and verification limits

I read the current article TeX and supplement, extracted the 15-page article PDF, inspected rendered result/table
pages and selected figures, read the prior Reviewer 1 reports and Reviewer 2's report, and considered all three
main-branch author responses in full:

1. [Response to Reviewer 1](author_response_main_20261013.md), R1-BTS-01–10.
2. [Response to Reviewer 1, round 2](author_response_main_round2_20261013.md), R2-BTS-01–08.
3. [Response to Reviewer 2](author_response_reviewer2_20261015.md), R2B-01–07, including the unchanged-lattice rerun.

Their completion records describe their respective versions; they are not journal decisions. Restored BTS-branch
responses concern another historical manuscript and their acceptance language is not evidence of acceptance here.
The current supplement has eight pages. I inspected the protocol, generated summaries, source implementation,
selected raw steering/test realizations, nominal baseline comparison records, claim ledger and asset identities.
`audit_bts_evidence.py` verified all **49 claim pointers and 39 artifact identities**;
`package_bts_revision.py --verify` passed. I independently summed the archived loss counts and checked their
normalizations. I did not rerun tracking, optimization, bootstrap inference, the test suite, a TeX build or the
referee-attachment rebuild. These identity/arithmetic checks do not validate every modeling assumption.

| Reviewed asset | SHA-256 |
| :--- | :--- |
| `paper.tex` | `9595cca2dd36819a83081d688efcd24c194f6e5f70f0bd2c25bc146859862cb3` |
| `paper.pdf` | `7595e38e50115fb9df6e203fd621fa7b7266c517be17de3512cc175113c027f6` |
| `supplement.tex` | `abc593c2599e25c8fbd15a4132b4d26bee48554b0580e96625078aa64ff647fd` |
| `supplement.pdf` | `190ae3b0c17b34710e88ed3693e4656798ffc20afcc245c443d0407b99821887` |
| `paper.bib` | `0a2210e5b160b3ab804a45f6f284aa2d07e7faf2af9897116545436486129830` |

The source-model identities inspected match the recorded generating bytes:
`bts_round3.py` SHA-256 `cbc707f52e2e6333c80d38560e95b80d8184b90b3c46ed350da15dcec77fe275`;
`run_bts_round3.py` SHA-256 `3fc5bf5780cda6d1eb72afc27eafeafc02703b7f9468ce62145df679e5f3b697`.

## What the three responses have resolved

| Earlier concern | Assessment of the current manuscript |
| :--- | :--- |
| R1-BTS-02/03: unsupported claims and literature | Substantially addressed. Historical statistics, local-response interpretations and primary-source comparisons are separated. The study distinguishes its 9-quadrupole/3-main-bend version from the TDR configuration. |
| R1-BTS-04/05: physical boundaries, units and active errors | Substantially addressed by source-labelled beam inputs, full covariance, fixed-geometry errors and independent checks; the remaining theorem/shape issues below are narrower. |
| R1-BTS-06/07: optimization outcomes and local response | Addressed. Failure/budget outcomes and bound-limited settings are retained; practical correction is modeled separately from an SVD knob claim. |
| R1-BTS-08/09 and R2-BTS-02/06: paired inference and saturation | Addressed in execution. The entrance-limited historical result and its many ties are explained; optical failures remain distinct from particle loss. Some current interpretation still needs qualification (M4). |
| R2-BTS-03/04: observable accuracy and interior beta extrema | Addressed for the declared finite cases and sampled meshes. These are not global loss-tail or continuous-chamber certificates. |
| R2-BTS-05 and R2B-04: a physically relevant alternative objective | Addressed: a frozen loss-based setting is tested on fresh realizations. The generic probability-bound statement requires correction (M2). |
| R2B-01/02: missing blade and trivial nominal end-clearance result | Largely addressed. The blade and element-wise restrictions are modeled, and the nominal fixed-end theorem is explicit. Its extension to errors is incorrect (M1). |
| R2B-03: trajectory correction | Addressed as a declared model with existing-dipole trims and noisy boundary readings, without changing the lattice; it is not a demonstrated hardware correction system. |
| R2B-05/06: exit dispersion and error sensitivity | Addressed. The dispersion-free result remains analytic and the ring trade is explicitly outside the BTS calculation. |
| R1-BTS-10, R2-BTS-08, R2B-07: preparation and presentation | Funding/acknowledgments and competing interests are now supplied, but approval remains pending. The current version removes its earlier availability statement; see M7. |

The newer nominal comparison is not confused with the matched-only error ensembles. Table 5 and the figure
validation record give baseline/low-beta exit beta_y 242.6069/4.2562 m and minimum clearance −1.5170/+0.6484 mm.
This demonstrates an envelope/matching change, not a measured loss reduction for the baseline: no baseline error
ensemble is reported, and the article appropriately says so. Negative five-sigma clearance does not mean total loss.

The independent matched-only test has 200 realizations, three shots per realization and 2,000 particles per shot:
reference/low-beta/loss-based losses are **27,603 / 27,217 / 8,285 out of 1,200,000**, or
**2.30025 / 2.26808 / 0.69042%**. All recorded first losses in these rows are `sept_ex`.
The archived loss-based-minus-reference estimate is **−1.60983 percentage points**, with the recorded paired
interval **[−2.33318, −0.96231]**; the low-beta interval includes zero. I verified the counts and inspected the
stored intervals, but did not reconstruct those intervals anew. This is good evidence for the conditional design
comparison, independent of the qualifications requested below.

## Remaining substantive comments

### M1 — Restrict the boundary theorem to the nominal matched line

**Locations:** Section 3.1, Section 3.2 and the discussion's trajectory-only explanation.

For fixed entrance covariance and an exactly matched, error-free uncoupled line, the nominal endpoint envelope
is fixed. This useful result is correct. The statement that under errors the **only** K-dependent part of the
end clearances is the centroid response is not correct. Gradient errors, rolls, momentum-dependent transport and
the sampled entrance beta factors also change the endpoint covariance. In general,
Sigma_out(K,e) = M(K,e) Sigma_in(e) M(K,e)^T; matching M(K,0) does not make Sigma_out independent of K when e is nonzero.
The code correctly transports this perturbed covariance, so the overstatement is in the interpretation.

Likewise Mx = B4 R(mu) B1^-1 characterizes the error-free, uncoupled, exactly matched transfer matrix. It is not a
complete description of the rolled, mismatched realizations. Define clearly whether J contains only the
non-dispersive centroid jitter before the separate momentum term is added. Qualify the phase-only statement and
identify the full covariance calculation used for actual test losses. Do not assert that all static errors are
removed; the fitted horizontal steering leaves residuals, does not undo optics errors and does not correct y.
No wholesale rerun is required if the existing implementation/results are retained and the claim is narrowed.

### M2 — Correct the claimed general probability bounds for round apertures

**Locations:** Section 3.3 and `bts_round3._edges` / `clearance_and_loss`.

Equation (7) is the exact marginal loss probability for a one-dimensional interval with a Gaussian marginal.
For rectangular restrictions, the maximum of the exact event probabilities is a lower bound and their sum a
union upper bound, regardless of correlations. For a circular/elliptical aperture, however, the code replaces
each halfwidth by a chord evaluated at the *other plane's centroid*. Two such marginal tails are not the exact
round-aperture event and do not provide the claimed general bracket.

A simple counterexample needs no tracking. For a centered isotropic 2-D Gaussian with rms sigma and a circular
aperture of radius 5 sigma, the exact loss is exp(−25/2) = **3.72665e−6**. The implemented projected recipe uses
halfwidths 5 sigma in both planes; its claimed union value is 4 Phi(−5) = **1.14661e−6**, smaller than the true loss.
Thus that value cannot be an upper bound. The gap is about a factor of 3.25.

Either evaluate the correct round-aperture probability/bounds, or call the chord construction an approximation
and confine rigorous bounds to exact rectangular/one-sided events. Add an appropriate deterministic limiting-case
check when changing this method. Show that the numerical comparison is still dominated by the rectangular blade;
the archived first-loss locations support that possibility but do not prove a general theorem. Distinguish the
maximum-of-marginals design surrogate from the line union loss. Agreement below 1% refers to the **aggregate
means in the stated tracked rows**, not all shots, all aperture shapes or the untracked dispersion-free tail.
No large new particle campaign is automatically required; establish whether the correction affects the chosen
settings before deciding what numerical results need regeneration.

### M3 — State what the discrete aperture test establishes

**Locations:** Section 2.3, loss validation and discussion.

Aperture attributes are checked at element entrances and at the line end; interior envelope samples are on an
observation copy. This is clearly disclosed and respects the unchanged lattice, but it is not continuous particle
interception through a physical septum/channel. In particular, the nominal interior observation check cannot
certify the tails under errors. Keep the headline result explicitly a loss on the declared checked boundaries.
If interpreting it as interception through a finite channel, provide a targeted refinement/intermediate-location
check on representative tail-producing shots using an auxiliary evaluation copy, without modifying the protected
or production source lattice. Otherwise retain the discrete-model limitation and avoid the continuous claim.
Actual chamber survey or full mechanical engineering is not a prerequisite for a scoped parametric paper.

### M4 — Repair the mean-clearance explanation and statistical language

**Locations:** Section 4.2 and conclusions.

The counterexample to mean clearance is useful, but saying the uncorrected mean is high because offsets toward
the blade "are lost" can suggest survivor censoring. The code obtains uncensored moments and averages all 600
shots. Their mean exit x is **−68.50 micrometres uncorrected** and **+8.77 micrometres corrected** in the reference
sample, while mean clearances are 0.58436/0.52430 mm. Report the finite-sample centroid bias and any covariance/
active-station changes rather than implying that lost shots leave the denominator.

A clean analytic explanation is available: at a fixed one-sided edge, constant sigma and centered centroid
jitter, E[c] = a − E[mu] − 5 sigma does not depend on the jitter variance, whereas
E[P] = Phi(−a/sqrt(sigma^2 + tau^2)) does. The same mean clearance can therefore hide different tail losses.
This is sufficient without attributing the observed mean ordering to undocumented censoring.

Replace "indistinguishable in every column" with the actual paired evidence. The independent loss difference
for low beta is unresolved; that is not equivalence or equality of all columns. A machine/realization bootstrap
accounts for within-realization dependence but does not by itself certify tail convergence. Keep the pointwise,
finite-population scope and distinguish sampled improvement from a universally unchanged ranking.

### M5 — Use sampled-search language consistently

**Locations:** Section 4.3, Figure 4 shading/caption, Section 4.4 and conclusions.

The source `phase.json` explicitly says that bounded multistart is not a proof of global reachability. The article
nevertheless says the match "pins" phase to the interval and matched solutions "reach only" 32 degrees. The
349/360 and 115/120 search outcomes establish the ranges **found in those searches**, not the entire feasible set.
All three loss-minimization starts reach their iteration limits; only one is feasible. Preserve that honest record
and call the chosen design a best-found feasible setting, not a proven feasible-set boundary or global optimum.
The claimed greatest leverage of the exit target is likewise conditional on the tested alternatives. Wording is
sufficient; I do not require a global-optimality proof or an expanded optimizer campaign.

### M6 — Describe the paired experiment and surrogate precision completely

**Locations:** Sections 2.4/4.2/4.3 and the reproduction notes.

Static magnet errors, entrance jitter, beam variates and realization IDs are shared across settings. BPM reading
errors are not: the driver seeds them with `[bpm_seed, machine, design_index]`. Disclose that distinction instead of
implying that every error draw is identical. Design-specific measurement noise does not invalidate a paired
realization bootstrap, but it changes what the paired comparison controls and should not be silently altered.
A common-BPM-noise sensitivity is optional unless it is needed to resolve a material effect.

The nominal analytic loss objective also excludes static residuals and the beta-factor fluctuation mixture used
in testing. State that approximation beside the objective. Its 0.27% nominal prediction and 0.69% test outcome are
different populations, while the test's per-shot centered predictions and tracked means agree closely. Do not
use one agreement statement for both. Retain the angular-jitter cost and the absence of ring-capture validation.

## Submission and presentation comments

### M7 — Make the submitted article independently interpretable and policy-ready

The article states the TDR/studied-lattice difference and gives its actual element count; keep this prominent so
"KLS BTS" is not read as a claim about the current official design. The companion NKM reference is explicitly a
manuscript in preparation. The BTS beam, blade and error definitions must remain self-contained, and any
companion acceptance width must identify its conditional setting rather than become an operational requirement.
The TDR landing page could not be retrieved during this review; its exact magnet counts were not independently
rechecked here, and no unverified TDR-specific discrepancy is alleged.

The [current JKPS scope](https://link.springer.com/journal/40042/aims-and-scope) includes accelerators and beams,
so a well-founded parametric accelerator-design article fits the journal. The
[JKPS submission guidelines](https://link.springer.com/journal/40042/submission-guidelines#research-data-policy-and-data-availability-statements),
checked 2026-10-30, require a data-availability statement for original research and ask authors to explain access.
The October-30 article has removed that statement. The author should resolve the journal-facing requirement with
wording matching actual access, rather than treating the earlier prepared attachment as an external deposit.
This review does not restore removed text, invent a DOI, upload data or override the author's submission decision.

Update the supplement title/date to identify this article and distinguish historical sections. Label the current
nominal baseline, matched reference, old low-beta and refined/loss-based strengths unambiguously in the
submission materials; historical tables must not be mistaken for current strength lists. Reconcile the current
15/eight-page inventory and final attachment after any corrections. Funding is now supplied and must not be
reported as still deferred simply because the old responses record that earlier state. Obtain final scientific
approval before removing the current approval-pending wording.

## Required revision and final assessment

The [ordered task register](reviewer1_bts_20261030_main_round3_revision_tasks.md) separates required corrections
from supporting checks. The central result is promising: reducing blade loss at the cost of angular jitter is a
useful conditional design observation, and the low-beta negative result is reported honestly. The present
manuscript still needs the theorem, probability-bound and interpretation corrections before acceptance can be
recommended. No ring-capture study, commissioned hardware validation, arbitrary new sample count or forced
improvement in transmission is required for the BTS scope. Prepare a new point-by-point response after revisions;
retain all three earlier responses and all earlier reports unchanged.
