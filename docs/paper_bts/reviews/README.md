# BTS manuscript referee reviews

This index preserves the main-branch review history and separate restored BTS-branch records. The original
main-branch assessment concerned the eight-page manuscript at `bee78914caa16945ef63dba8bf5205c434d0415c`;
its conclusions are historical. The current Reviewer 1 round-3 assessment is linked below.

| Review | Recommendation | Revision register |
| :--- | :--- | :--- |
| [Reviewer 1, BTS main-branch draft](reviewer1_bts_20261013_main_report.md), 2026-10-13 | Major revision; no acceptance in present form | [Ten ordered tasks R1-BTS-01–10](reviewer1_bts_20261013_main_revision_tasks.md) |

The report records exact TeX/PDF/bibliography hashes, checks the nine selected scientific-source digests and five infeasible observations, and identifies discrepancies in the supporting claim ledger, Jacobian normalization, OAT labels, restart interpretation and historical provenance.

## Execution of this review

[Point-by-point main-branch response](author_response_main_20261013.md) records R1-BTS-01–09 and the prepared R1-BTS-10 article/evidence. See [selected asset identity](../revision_selection.json) and [submission checklist](../submission_checklist.md). Funding and remaining author declarations/approval/delivery are pending. The original report and open-at-review task register are preserved verbatim; their date-specific status is historical. No journal acceptance is claimed.

## Historical reviews restored from bts

The following three rounds were recovered verbatim from local `bts` commit `466fca5376c76ab1ceb587c801a696b6613a66f4`. They assess the manuscript developed on that branch, rather than the subsequently revised main-branch article. Their recommendations, numerical claims and completion labels record the historical review state; they do not establish journal acceptance or validate those claims for the current manuscript. Consult the main-branch review and response above for the current revision status.

| Historical round | Report | Revision tasks | Author response |
| :--- | :--- | :--- | :--- |
| 1 | [Report 01](reviewer_report_01.md) | [Round 1 tasks](revision_tasks.md) | [Response 01](author_response_to_reviewer_01.md) |
| 2 | [Report 02](reviewer_report_02.md) | [Round 2 tasks](revision_tasks_round2.md) | [Response 02](author_response_to_reviewer_02.md) |
| 3 | [Report 03](reviewer_report_03.md) | [Round 3 tasks](revision_tasks_round3.md) | [Response 03](author_response_to_reviewer_03.md) |

The original branch milestones are `6878ba7` (first review), `05a645f` (first-round execution), `814c0c4` (second round), and `aff4ef7` (third round). References inside these historical documents to manuscript sections, provenance, tests and generated submission packages refer to their original branch versions. Restoring these records does not regenerate or import those assets.

## Second assessment of the revised main-branch article

[Reviewer 1 main-branch round-2 report](reviewer1_bts_20261013_main_round2_report.md), 2026-10-13, evaluates the revised eight-page *Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line* at `742b940`. Recommendation: **major revision; no acceptance in present form**. The [eight ordered R2-BTS tasks](reviewer1_bts_20261013_main_round2_revision_tasks.md) are open at review. This assessment credits the completed R1 revisions while requiring limiting-station analysis, clearance-scale validation, interior-extrema checks and a stronger physical design comparison. It is separate from the restored historical BTS-branch rounds.

## Execution of main-branch round2

[Point-by-point round2 response](author_response_main_round2_20261013.md) records R2-BTS-01–07 scientific/manuscript execution and R2-BTS-08 submission preparation. The [new reproduction guide](../round2_reproduction.md) distinguishes original and new independently seeded campaigns and retained invalid runs. Author confirmed no competing interests; funding and acknowledgments remain deferred. Final scientific approval and actual reviewer delivery remain pending. The open-at-review task register and every earlier report are preserved unchanged; their historical recommendations do not constitute current journal acceptance.

## Reviewer 2 assessment of the revised main-branch article

[Reviewer 2 main-branch report](reviewer2_bts_20261015_main_report.md), 2026-10-15, evaluates the twelve-page
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

[Point-by-point response to Reviewer 2](author_response_reviewer2_20261015.md) records R2B-01 to R2B-07 (milestones
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

[Reviewer 2 round-3 report](reviewer2_bts_20261030_main_round3_report.md), 2026-10-30, evaluates the 15-page
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
[round-3 task register](reviewer2_bts_20261030_main_round3_revision_tasks.md). Earlier reports and responses are
unchanged.

## Reviewer 1 — round-3 assessment of the current main-branch article

[Reviewer 1 report, 2026-10-30](reviewer1_bts_20261030_main_round3_report.md) evaluates the current 15-page
*Optical matching and beam loss in the Korea Light Source Booster-to-Storage transfer line* and eight-page
supplement at `603c3ab`, based on all three main-branch author responses. Recommendation: **focused major revision;
no acceptance in present form**. The loss-based held-out comparison is credited, while the nominal-versus-error
boundary theorem, round-aperture probability bounds, mean-clearance interpretation and sampled-search scope
require correction or qualification. The [eight R3-BTS tasks](reviewer1_bts_20261030_main_round3_revision_tasks.md)
are all pending. Existing reports/responses and the restored historical round 3 are unchanged; the new report is
a pre-submission assessment, not a journal decision. No scientific revision was executed by this review.
