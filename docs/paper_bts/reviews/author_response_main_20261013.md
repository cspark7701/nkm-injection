# Response to Reviewer 1 — main-branch BTS revision

This response addresses the [2026-10-13 review](reviewer1_bts_20261013_main_report.md) and its ten tasks. The original reviews remain unchanged. See [revision identity](../revision_identity.md). Scientific completion is distinct from journal acceptance; author declarations will be confirmed separately.

## R1-BTS-01 — Freeze BTS reviewer revision identity

Select the main-branch draft, preserve baseline asset hashes and reopen the B01 audit while distinguishing the later BTS article.

Validation: Verified baseline hashes, branch identity and unchanged protected inputs, NKM files and prior reviews. See [milestone 187](../../exec-plans/completed/187_r1_bts_01.md).

## R1-BTS-02 — Correct BTS claims and artifact provenance

Audit twelve BC claims with exact JSON pointers, repair restart, Jacobian, OAT, failure and boundary interpretations, and record artifact-specific metadata.

Validation: All nine selected artifact digests and twelve claim pointers verified; unresolved hardware and target provenance explicitly retained as assumptions. See [milestone 188](../../exec-plans/completed/188_r1_bts_02.md).

## R1-BTS-03 — Establish the BTS physical question and primary literature

Replace unsupported regional and global comparisons with checked primary passages and define a paired physical-clearance design question.

Validation: Verified SLS, Sirius, ESRF and MAX IV records; unverified PLS-II and RAON references and quantitative comparisons withdrawn. See [milestone 189](../../exec-plans/completed/189_r1_bts_03.md).

## R1-BTS-04 — Specify BTS boundaries beam and model constraints

Freeze the source-labelled model, full design-beam covariance and assumed hardware limits; record actual aperture positions and legacy MAD-X non-equivalence.

Validation: Validated 36-element order, 21.789 m length, K-to-gradient/pole-field conversion and geometry figure; physical target and continuous chamber remain parametric. See [milestone 190](../../exec-plans/completed/190_r1_bts_04.md).

## R1-BTS-05 — Validate independent BTS transport and active errors

Implement hard-edge affine transport, coupled covariance and fixed-geometry active errors; validate against AT particle maps and Gaussian transport.

Validation: 13 tests pass; 40-step maps meet declared tolerances, isolated errors and first losses checked, and the missed default-step tolerance remains reported. See [milestone 191](../../exec-plans/completed/191_r1_bts_05.md).

## R1-BTS-06 — Reproduce BTS matching and all search outcomes

Replay all three historical starts and independently verify raw and rounded settings with optical, family-bound and model-clearance checks.

Validation: Historical candidate values reproduced; 40-step and independent-map settings remain feasible, with explicit engineering tolerances and termination records. See [milestone 192](../../exec-plans/completed/192_r1_bts_06.md).

## R1-BTS-07 — Normalize BTS response and withdraw operational knob claims

Define dimensionless row and actuator scaling, verify finite-difference convergence and local finite response, and withdraw unsupported practical correction claims.

Validation: Six local finite checks pass within bounds; rank and null-space conventions are recorded without claiming operational decoupling. See [milestone 193](../../exec-plans/completed/193_r1_bts_07.md).

## R1-BTS-08 — Evaluate frozen BTS designs on held-out machines

Complete constrained low-beta design and paired physical-clearance/particle comparisons on 200 held-out machines with independent shots.

Validation: Track 1.2 million particles per design, retain first-loss records and nonzero zero-loss bounds, and report paired machine-cluster uncertainty without claiming beta equals clearance. See [milestone 194](../../exec-plans/completed/194_r1_bts_08.md).

## R1-BTS-09 — Reconstruct BTS statistics and qualify tolerance claims

Audit all 550000 historical observations and pooling fields, reconstruct quantile/failure intervals and preserve missed prefixes while separating new physical transport.

Validation: 15 relevant tests pass; all five failure records, exact asymmetric intervals and order-statistic quantiles match; hardware tolerance and optional-stopping claims remain withdrawn. See [milestone 195](../../exec-plans/completed/195_r1_bts_09.md).

## Report comments and manuscript locations

| Referee point | Resolution and evidence | Revised manuscript |
| :--- | :--- | :--- |
| M1 contribution | [Completed paired design comparison](../heldout_comparison.md): no resolved clearance benefit despite lower beta | Introduction, Results4.2, Discussion |
| M2 boundary/hardware | [Source-labelled beam and boundaries](../beam_and_boundaries.md); ring target, chamber and hardware assumptions remain explicitly parametric | Model2.1–2.2, Table1, Figure1 |
| M3 active transport | [Independent map/covariance/particle validation](../transport_validation.md), with integration miss retained | Methods3.1–3.2 |
| M4 evidence corrections | [Seventeen-claim ledger](../claim_evidence.csv), [discrepancy resolutions](../discrepancy_resolution.md) and exact-key/digest checker | Model, Results4.1/4.3, appendix |
| M5 literature | [Verified primary comparisons](../literature_comparison.md); unverified PLS-II/RAON entries withdrawn; MAX IV title corrected; undated ESRF report cited by actual title | Introduction and bibliography |
| M6 correction/margin | [Normalized local response](../correction_knobs.md), practical knob claims withdrawn; frozen-design alternative replaces operational correction claims | Results4.1–4.2 |
| M7 statistics | [All-observation statistical reconstruction](../tolerance_distributions.md), actual thresholds, asymmetric intervals and missed prefixes retained | Results4.3 |
| M8 reproducibility | Isolated eight-page PDF, selected raw-output attachment, exact source snapshots and portable commands; author declarations/delivery pending | Declarations and appendix |
| §4 presentation |202-word abstract, three figures, concise one-column source, numbered references and checked JKPS guidance | [Submission checklist](../submission_checklist.md) |

R1-BTS-10 author-confirmed funding, competing interests/acknowledgments, final approval and actual referee delivery remain pending. The author explicitly deferred funding. They are not fabricated or described as complete. Scientific work and publication preparation do not imply journal acceptance.

The full comparison and all-observation statistical audit were reproduced from the extracted attachment with identical selected values. [Final checks](../validation_checks.md) record the suite, links, hashes and layout evidence.

## R1-BTS-10 — Prepare the revised BTS article and referee evidence package

Prepare the eight-page article, seventeen-claim ledger, point-by-point response and portable raw-evidence package; author-confirmed declarations and actual submission delivery remain pending.

Validation: 713 repository tests and 15 isolated checks pass; extracted comparison/statistics reproduce exactly, fresh PDF has no warnings, layout/links/hashes verified and protected inputs unchanged. See [milestone 196](../../exec-plans/completed/196_r1_bts_10.md).
