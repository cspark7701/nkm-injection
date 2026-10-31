# BTS manuscript referee reviews

## Review document filenames

Filenames now state the round, reviewer and document role, with two-digit numbers:

- `review_round_04_reviewer_01_report.md`: Reviewer 1's round-4 report.
- `review_round_04_reviewer_01_tasks.md`: the corresponding reviewer task list.
- `review_round_03_author_response_to_reviewers_01_02.md`: response to the round-3 reviews.
- `revision_round_03_plan_for_review_round_03.md`: the round-4 revision plan answering round-3 reviews.

The two numbers in a consolidated-plan filename now match its review-round suffix. The original implementation
cycle and task IDs (R4-BTS, R5-BTS or R6-BTS) remain in the document body; the filename does not renumber those
completed activities. The [plan transition map](revision_plan_filename_rename_map.json) records all three renames.
Dates, task IDs, decisions and author statements remain in the documents. A
`report_and_tasks` suffix means the original report contains its own task register; it was not split or discarded.
The [rename map](document_rename_map.json) records every old/new path and before/after digest. Old snapshot paths
and hashes identify the original Git/attachment contents; they are not rewritten to pretend those bytes are new.

BTS records prefixed `historical_branch_` belong to the restored `bts` branch and remain distinct from the main-branch
review sequence. Historical report numbers are retained without assigning a referee identity absent from the
report itself. Reviewer 2's main-sequence report/task filenames now use consecutive numbers starting at 01,
one lower than their previous names. Their original titles, round references, dates, decisions and task IDs
remain historical records. Author-response filenames retain their existing numbering; consolidated-plan
filenames use the matching-number convention above.
Thus the first Reviewer 2 assessment, whose body calls it round 2, is now
`review_round_01_reviewer_02_report_and_tasks.md`; it includes its own task register.
The pre-normalization report/task pair numbered 05 retains review round 6 in its original text.
New Reviewer 2 assessments continue from filename round 06.
The [Reviewer 2 transition map](reviewer_02_sequence_rename_map.json) records all nine renames and content hashes.
The earlier `document_rename_map.json` is a frozen historical map; use this transition and its hashes to resolve
paths reused by later reports. Frozen protocols also retain their original path strings and hashes; the maps
provide their current document locations. In particular, the October-31 joint response answers **review round 3** in its
original sequence, while recording **revision round 4**.


This index preserves the main-branch review history and separate restored BTS-branch records. The original
main-branch assessment concerned the eight-page manuscript at `bee78914caa16945ef63dba8bf5205c434d0415c`;
its conclusions are historical. [Reviewer 1's latest assessment is round 6](review_round_06_reviewer_01_report.md):
accept the scientific content within its stated scope, with no mandatory scientific revision.
Its [closure checklist](review_round_06_reviewer_01_tasks.md) verifies that both earlier R1E-BTS follow-ups are closed.
[Reviewer 2's latest assessment](review_round_06_reviewer_02_report.md) independently recommends acceptance;
its [editorial suggestions](review_round_06_reviewer_02_tasks.md) remain optional.
The [latest joint author response](review_round_05_author_response_to_reviewers_01_02.md) records implementation round 7.
R5-BTS-09 remains deferred to submission readiness. These are internal referee recommendations, not journal decisions.
Earlier assessments are retained below as history.

| Review | Recommendation | Revision register |
| :--- | :--- | :--- |
| [Reviewer 1, BTS main-branch draft](review_round_01_reviewer_01_report.md), 2026-10-13 | Major revision; no acceptance in present form | [Ten ordered tasks R1-BTS-01–10](review_round_01_reviewer_01_tasks.md) |

The report records exact TeX/PDF/bibliography hashes, checks the nine selected scientific-source digests and five infeasible observations, and identifies discrepancies in the supporting claim ledger, Jacobian normalization, OAT labels, restart interpretation and historical provenance.

## Execution of this review

[Point-by-point main-branch response](review_round_01_author_response_to_reviewer_01.md) records R1-BTS-01–09 and the prepared R1-BTS-10 article/evidence. See [selected asset identity](../revision_selection.json) and [submission checklist](../submission_checklist.md). Funding and remaining author declarations/approval/delivery are pending. The original report and open-at-review task register are preserved verbatim; their date-specific status is historical. No journal acceptance is claimed.

## Historical reviews restored from bts

The following three rounds were recovered verbatim from local `bts` commit `466fca5376c76ab1ceb587c801a696b6613a66f4`. They assess the manuscript developed on that branch, rather than the subsequently revised main-branch article. Their recommendations, numerical claims and completion labels record the historical review state; they do not establish journal acceptance or validate those claims for the current manuscript. Consult the main-branch review and response above for the current revision status.

| Historical round | Report | Revision tasks | Author response |
| :--- | :--- | :--- | :--- |
| 1 | [Report 01](historical_branch_review_round_01_report.md) | [Round 1 tasks](historical_branch_revision_round_01_tasks.md) | [Response 01](historical_branch_review_round_01_author_response_to_reviewer_01.md) |
| 2 | [Report 02](historical_branch_review_round_02_report.md) | [Round 2 tasks](historical_branch_revision_round_02_tasks.md) | [Response 02](historical_branch_review_round_02_author_response_to_reviewer_02.md) |
| 3 | [Report 03](historical_branch_review_round_03_report.md) | [Round 3 tasks](historical_branch_revision_round_03_tasks.md) | [Response 03](historical_branch_review_round_03_author_response_to_reviewer_03.md) |

The original branch milestones are `6878ba7` (first review), `05a645f` (first-round execution), `814c0c4` (second round), and `aff4ef7` (third round). References inside these historical documents to manuscript sections, provenance, tests and generated submission packages refer to their original branch versions. Restoring these records does not regenerate or import those assets.

## Second assessment of the revised main-branch article

[Reviewer 1 main-branch round-2 report](review_round_02_reviewer_01_report.md), 2026-10-13, evaluates the revised eight-page *Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line* at `742b940`. Recommendation: **major revision; no acceptance in present form**. The [eight ordered R2-BTS tasks](review_round_02_reviewer_01_tasks.md) are open at review. This assessment credits the completed R1 revisions while requiring limiting-station analysis, clearance-scale validation, interior-extrema checks and a stronger physical design comparison. It is separate from the restored historical BTS-branch rounds.

## Execution of main-branch round2

[Point-by-point round2 response](review_round_02_author_response_to_reviewer_01.md) records R2-BTS-01–07 scientific/manuscript execution and R2-BTS-08 submission preparation. The [new reproduction guide](../round2_reproduction.md) distinguishes original and new independently seeded campaigns and retained invalid runs. Author confirmed no competing interests; funding and acknowledgments remain deferred. Final scientific approval and actual reviewer delivery remain pending. The open-at-review task register and every earlier report are preserved unchanged; their historical recommendations do not constitute current journal acceptance.

## Reviewer 2 assessment of the revised main-branch article

[Reviewer 2 main-branch report](review_round_01_reviewer_02_report_and_tasks.md), 2026-10-15, evaluates the twelve-page
*Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line* at `82598dc`, after
reading both Reviewer 1 rounds, the responses and the historical reports. Recommendation: **major revision; no
acceptance in present form**. It accepts the numerical validation and inference. Its objections concern the physical
model of the line:
- the nominal end-station clearances are analytically independent of the quadrupoles;
- the positive results rest on hypothetical m2/m3 restrictions, while quadrupole bores, dipole gaps, septum channels
  and the exit septum blade (about 1.5 mm from the beam in the companion geometry) are absent;
- trajectory correction is missing;
- mean clearance is not a loss-relevant objective.

Seven tasks, R2B-01 to R2B-07, are included in the report.

## Execution of the Reviewer 2 report

[Point-by-point response to Reviewer 2](review_round_02_author_response_to_reviewer_02.md) records R2B-01 to R2B-07 (milestones
225–231). The article keeps its title, *Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line*, and is re-framed around:
- element-wise apertures with the companion septum blade;
- trajectory correction, with a recorded layout amendment;
- jitter transfer through the horizontal phase advance;
- a tracking-validated Gaussian loss observable;
- a loss-based setting tested on fresh machines;
- a dispersion-free exit;
- an error-level sensitivity study.

The four-station study moved to the supplement. Funding and acknowledgments are installed (2026-10-19); the
availability wording is final and the referee attachment prepared (2026-10-20). Final approval remains an author action. The Reviewer 2 report is preserved unchanged.

At the author's instruction the BTS lattice is not changed: the round-3 study was rerun (milestone 234) without
added corrector or monitor elements. Steering now uses horizontal trims of the existing dipoles, and the
added-corrector campaign is superseded.

## Reviewer 2 round-3 assessment

[Reviewer 2 round-3 report](review_round_02_reviewer_02_report.md), 2026-10-30, evaluates the 15-page
*Optical matching and beam loss in the Korea Light Source Booster-to-Storage transfer line* at `603c3ab`, after
reading the three main-branch author responses. Recommendation: **major revision; not acceptable in present form,
with a short route to acceptance**.

The report accepts the Reviewer 2 round-2 resolutions: element-wise apertures, steering, the loss observable and
the phase-advance mechanism. Its remaining objections:
- **Booster jitter.** The 0.5 mm / 0.2 mrad jitter is about five beam sizes in normalised phase space, drives every
  loss number, and is not varied.
- **Baseline framing.** The baseline-versus-optimized headline is circular: the baseline exit is far from the
  target, and the blade distance is defined from the matched beam.
- **Phase advance.** The reachable μ_x edge and the loss-based setting rest on sampling and an iteration-limited
  optimizer.
- **Blade distance.** It is not swept.

There are ten tasks, R2C-01 to R2C-10, in the
[round-3 task register](review_round_02_reviewer_02_tasks.md). Earlier reports and responses are
unchanged.

## Reviewer 1 — round-3 assessment of the current main-branch article

[Reviewer 1 report, 2026-10-30](review_round_03_reviewer_01_report.md) evaluates the current 15-page
*Optical matching and beam loss in the Korea Light Source Booster-to-Storage transfer line* and eight-page
supplement at `603c3ab`, based on all three main-branch author responses. Recommendation: **focused major revision;
no acceptance in present form**. The loss-based held-out comparison is credited, while the nominal-versus-error
boundary theorem, round-aperture probability bounds, mean-clearance interpretation and sampled-search scope
require correction or qualification. The [eight R3-BTS tasks](review_round_03_reviewer_01_tasks.md)
are all pending. Existing reports/responses and the restored historical round 3 are unchanged; the new report is
a pre-submission assessment, not a journal decision. No scientific revision was executed by this review.

## Round-4 consolidated revision tasks

The [round-4 consolidated register](revision_round_03_plan_for_review_round_03.md), 2026-10-30, merges Reviewer 1's
R3-BTS-01 to 08 and Reviewer 2's R2C-01 to 10 into fourteen tasks, R4-BTS-01 to R4-BTS-14 (nine A, three B, two
C). It maps each task to its source items and records how differences between the reviewers are resolved:
- the phase-advance scan is done, together with sampled-search wording;
- the baseline comparison is kept but removed from the headline;
- the dispersion-free tracking is optional.

All tasks are open. Both source registers are unchanged.

## Execution of the round-4 revision

The [joint response](review_round_03_author_response_to_reviewers_01_02.md), 2026-10-31, records the execution of R4-BTS-01 to 14
(milestones 265–278) against both round-3 reports.

**What changed in the conclusions.**
- **Booster jitter.** The loss reduction is a property of the large assumed booster jitter.
- **Static residual.** It is small: earlier statements attributing the spread between populations to it were
  corrected.
- **Phase advance.** The loss depends on μ_x alone.
- **Baseline.** It is a starting point, not a result.

The joint response also answers Reviewer 2's questions. All reports, task registers and earlier responses are
unchanged. No reassessment or journal decision is implied.

## Reviewer 2 round-4 assessment

[Reviewer 2 round-4 report](review_round_03_reviewer_02_report.md), 2026-10-31, evaluates the 19-page round-4
article at `6a968f8` after reading all main-branch author responses. Recommendation: **major revision of limited
scope; not acceptable in present form; acceptance expected after R2D-01 to R2D-03**.

The report accepts the round-3 resolutions. Its remaining objections:
- **Static residuals (M1).** At the realistic jitter the paper identifies, the delivered beam is dominated by
  the static steering residual (about 0.18 mrad) and the uncorrected vertical trajectory (about 1.1 mm), not by the
  jitter partition the new abstract names.
- **Reading errors (M2).** They are drawn per setting and should be shared by all settings.
- **Headline estimate (M3).** It should be the jitter-integrated loss.
- **Lower edge and length (M4).** The lower μ_x edge needs a physical explanation, and the article should be
  consolidated.

Twelve tasks with checkboxes, R2D-01 to R2D-12, are in the
[round-4 task register](review_round_03_reviewer_02_tasks.md). Earlier reports and responses are
unchanged.

## Reviewer 1 round-4 assessment

[Reviewer 1 round-4 report](review_round_04_reviewer_01_report.md), 2026-10-31, assesses the 19-page article
and nine-page supplement at `6a968f8`, considering all seven historical/current author responses. Recommendation:
**minor revision; scientifically acceptable in principle after bounded corrections, not unconditional acceptance**.
The prior major remedies are credited. Remaining items concern conditional versus jitter-integrated predictions,
the accuracy claim for the new sparse-loss rows, nominal horizontal transfer equivalence and low-jitter residuals,
contradictory conclusions, provenance/legend details and author-dependent submission gates.
The [seven checkbox tasks](review_round_04_reviewer_01_tasks.md), R1D-BTS-01–07, are all pending.
No new major campaign or executed revision is implied. Earlier reports, registers and author responses remain
unchanged; the separate Reviewer 2 assessment retains its own recommendation.

## Consolidated follow-up to both round-4 reviews

Use the [round-5 consolidated checkbox register](revision_round_04_plan_for_review_round_04.md) as the single queue for
revising the round-4 manuscript. It maps all 19 original top-level requests to ten pending tasks, R5-BTS-01–10,
retains both reviewers' recommendations, and records the decisions on shared reading errors, headline estimators
and editorial targets. The original Reviewer 1 and Reviewer 2 registers and the executed round-4 plan remain
unchanged. No revision task has been executed by the consolidation.

## Execution of the round-5 revision

The [joint response](review_round_04_author_response_to_reviewers_01_02.md), 2026-10-31, records the execution of
R5-BTS-01 to 10 (milestones 283–292) against both round-4 reports. The [round-5 plan](revision_round_04_plan_for_review_round_04.md)
shows each task with its milestone and commit; R5-BTS-09 stays open for author decisions. All reports, task
registers and earlier responses are unchanged. No reassessment or journal decision is implied.

## Reviewer 2 round-5 assessment

[Reviewer 2 round-5 report](review_round_04_reviewer_02_report.md), 2026-10-31, assesses the 19-page article
and 10-page supplement at `50d4699`, considering all eight preserved author responses. Recommendation:
**minor revision; scientifically acceptable in principle after bounded corrections**. The round-4 major
requests on residual delivery errors, shared monitor noise and the headline estimator are resolved.

The [four open-at-review R2E-BTS checkbox tasks](review_round_04_reviewer_02_tasks.md) cover the validation-percentage
denominator, qualifications to phase-edge/steering claims, population cross-references and response/evidence
reconciliation. No new broad campaign is required. At the author's instruction, R5-BTS-09 decisions are
deferred to the submission-ready stage and excluded from this checklist. No revision is executed by this
review; all previous reports, task lists and responses remain unchanged. This is a pre-submission scientific
recommendation, not a journal acceptance.

## Consolidated round-6 execution register

The [current consolidated register](revision_round_05_plan_for_review_round_05.md) combines the
[round-5 implementation plan](revision_round_04_plan_for_review_round_04.md) and
[Reviewer 2 round-5 checklist](review_round_04_reviewer_02_tasks.md). It carries nine completed tasks as
history, maps the four follow-up corrections to R6-BTS-01–04, and accounts for all fourteen source items.
R5-BTS-09 remains deferred to submission readiness, outside the active checklist. Both input lists and
all previous reports/responses remain unchanged. Consolidation executes none of the four new tasks.

## Execution of revision round 6

All four R6-BTS tasks are executed (milestones 295 to 298). The
[new response to Reviewer 2 round 5](review_round_05_author_response_to_reviewer_02.md) records the denominator
correction, scoped phase-edge/steering conclusions and repaired population references. Current PDFs have
20 article pages and 10 supplement pages; 76 claims, selected asset hashes and 46 relevant tests pass.
The [round-6 reproduction guide](../round6_reproduction.md) distinguishes post-processing from a simulation rerun.
Original reviewer checklists remain open-at-review records; the consolidated register records completion.
R5-BTS-09 remains deferred. No reassessment, author approval or journal acceptance is implied.

## Reviewer 1 round-5 assessment

[Reviewer 1's round-5 report](review_round_05_reviewer_01_report.md), 2026-10-31, assesses the current
20-page article and 10-page supplement at `79dce19`, after the round-6 implementation, using all nine
author responses. Recommendation: **accept the scientific content within its stated conditional-model scope;
no mandatory scientific revision**. This updates Reviewer 1's round-4 recommendation; it does not revise
Reviewer 2's independent round-5 report or constitute a journal decision.

The [two-item follow-up checklist](review_round_05_reviewer_01_tasks.md) distinguishes optional shortening
from a technical package update before evidence delivery. The existing incremental recipe lacks the new
round-6 audit script referenced by the current reproduction guide; local numerical checks remain valid.
R5-BTS-09 author decisions stay deferred and outside the checklist. All prior reports, task lists and responses
are preserved, and no revision task is executed by this assessment.

## Reviewer 2 review round 6

[Reviewer 2 round-6 report](review_round_05_reviewer_02_report.md), 2026-10-31, assesses the revision-round-6
article at `79dce19` (20 pages, 10-page supplement) after reading all main-branch author responses, including the
round-5 response to Reviewer 2. Recommendation: **minor revision; acceptable after small corrections, without
another review round**.

The round-5 checklist (R2E-BTS-01 to 04) is resolved. Three points remain, and none changes the conclusions:
- **Low beta.** The effect is still partly quoted from a per-setting-reading population.
- **Loss bracket.** Section 3.3's per-shot bracket is violated by the tracked loss-based count; the excess comes
  from one near-blade shot.
- **Headline interval.** Its scope should be stated.

There are six checkbox tasks, R2F-BTS-01 to 06, in the [round-6 checklist](review_round_05_reviewer_02_tasks.md).
The R5-BTS-09 submission decisions stay deferred. Earlier reports and responses are unchanged.

## Execution of filename-round-5 tasks (implementation round 7)

All six R2F-BTS items and both R1E-BTS follow-ups are addressed in milestones 303 to 308.
The [new joint response](review_round_05_author_response_to_reviewers_01_02.md) records the controlled-low-beta
wording alternative, 16 loss-bearing shots (correcting the review's 20), model interval scope, revised labels
and bounded shortening. Current PDFs have 19 article pages and 10 supplement pages. The older steering table
is in supplement Section 5; the primary comparison is now Table 5, layouts Table 4 and residuals Table 7.
The [round-seven guide](../round7_reproduction.md) records 80 verified claims, current hashes, 46 passing tests
and a new increment verified after extraction, including both post-processing audits. The cause of the excess
remains unresolved; no new tracking is claimed. R5-BTS-09 stays deferred. Reports and earlier responses remain
historical records; the source checklists now record execution rather than a new reviewer verdict.

## Reviewer 2 review round 6

[Reviewer 2 round-6 report](review_round_06_reviewer_02_report.md), 2026-10-31, assesses the article at `fd16b2a`
(19 pages, 10-page supplement) after reading all main-branch author responses, including the joint response to the
round-5 reports. Recommendation: **accept**.

All six round-5 Reviewer 2 tasks (R2F-BTS-01 to 06) are resolved. The report acknowledges the corrected shot count:
16 loss-bearing shots, not 20.

The [optional editorial checklist](review_round_06_reviewer_02_tasks.md), R2G-BTS-01 to 05, covers:
- Section 4.2's opening;
- the abstract length (about 300 words);
- an optional nonlinear check;
- final shortening.

None is a condition of acceptance. The R5-BTS-09 submission decisions stay deferred. Earlier reports and responses
are unchanged.

## Reviewer 1 review round 6

The [round-6 report](review_round_06_reviewer_01_report.md), dated 2026-10-31, assesses the scientific files selected at `fd16b2a` after considering all ten author responses. Recommendation: **accept the scientific content within its stated conditional-model scope**. No mandatory scientific revision remains. The [closure checklist](review_round_06_reviewer_01_tasks.md) closes both previous follow-ups and records the selected evidence checks: 80 claims, 90 hashes, 46 tests and matching post-processing records. The unresolved near-blade excess remains explicitly qualified. R5-BTS-09 stays deferred; earlier records are preserved.
