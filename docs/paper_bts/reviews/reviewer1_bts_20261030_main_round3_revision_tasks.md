# Reviewer 1 — main-branch BTS round-3 revision tasks

Date: 2026-10-30. Basis: [round-3 report](reviewer1_bts_20261030_main_round3_report.md).
Recommendation: focused major revision; no acceptance in present form.
All tasks are **pending**. Read-only review checks are not execution of these revisions.
This register does not replace the restored historical `revision_tasks_round3.md`.
A: required scientific/submission correction. B: supporting clarification or conditional check.

| ID | Priority | Revision | Completion criterion | Additional computation |
| :--- | :---: | :--- | :--- | :--- |
| R3-BTS-01 | A | Restrict fixed-end and phase-only theorems to the nominal, error-free, uncoupled, exactly matched model. Retain perturbed covariance and steering residuals in the error interpretation; define the nondispersive part of J. | Section 3.1/3.2 and conclusions no longer claim K-independent covariance under errors or complete static-error removal; the calculation used for test losses is explicit. | No new campaign if code/results are unchanged. |
| R3-BTS-02 | A | Repair or qualify circular/elliptical aperture loss treatment and the claimed probability bracket. Preserve exact rectangular/blade formulas and separate the design surrogate from the line union. | Centered isotropic round-aperture counterexample is handled correctly; bounds called rigorous only where valid. Establish whether current blade-dominated predictions/settings change and regenerate affected outputs if necessary. | Deterministic shape/limiting-case checks and targeted sensitivity; no automatic full campaign. |
| R3-BTS-03 | B | Make discrete entrance/end aperture checking distinct from continuous-channel interception. If retaining a continuous-loss interpretation, test representative tail shots at additional locations on an auxiliary copy. | The scope follows actual observation locations; any refinement leaves the original 36-element source/production lattice intact. | None for a narrowed claim; targeted refinement only if the stronger claim is retained. |
| R3-BTS-04 | A | Correct the mean-clearance explanation using uncensored shot means/variance and tail probability; replace unsupported all-column equivalence and avoid implying that bootstrap intervals alone certify tail precision. | All 600 shots remain in the declared denominator; finite-sample centroid bias and variance sensitivity are distinguished; conclusions match the recorded paired intervals. | Existing-data arithmetic/analytic explanation is sufficient; no extra samples just to resolve a null result. |
| R3-BTS-05 | A | Qualify phase-advance ranges, best-found loss design, optimizer termination and exit-target leverage as sampled-search findings. | Figure 4, results and conclusions agree with the source's non-global scope; 349/360, 115/120 and all three iteration limits are retained accurately. | No global proof or further optimization required. |
| R3-BTS-06 | B | Disclose design-specific BPM noise alongside shared static/shot/particle draws; distinguish the nominal objective from the beta-fluctuation/static-residual test mixture and aggregate from per-shot accuracy. | Pairing, noise seeds, populations and validation precision are reproducible. Retain angular-jitter trade and analytic-only dispersion-free status. | Wording/source documentation; common-noise sensitivity only if needed for a material conclusion. |
| R3-BTS-07 | A | Prepare a self-contained submission: current/supplement identities and strength labels, companion-study scope, author-approved availability wording consistent with JKPS requirements and real access. | Current paper/supplement and declarations are consistent; no fabricated source, hardware provenance, public deposit, DOI or approval. Earlier response-time pending declarations are clearly historical. | Editorial/source checking only; author input for final approval/access wording. |
| R3-BTS-08 | A | Reconcile claims, source/PDF, provenance and attachment after actual revisions; write a new response and retain previous reviews/responses. | Appropriate model tests for any method changes; clean article/supplement builds and visual checks; hashes/claim pointers and a fresh frozen attachment agree. Record author-dependent gates separately. | Checks appropriate to changes; no blanket full simulation rerun. |

## Execution sequence

R3-BTS-01 and R3-BTS-02 first: determine whether the correction is interpretive or changes any selected numerical
observable. R3-BTS-03–06 can then proceed with the existing data/source; only a retained stronger model claim or a
material change requires a targeted new run. R3-BTS-07 prepares the submission-facing material; R3-BTS-08 follows
all scientific/editorial decisions. Use new result directories and preserve the original inputs, source lattice,
invalid/superseded campaigns and prior attachment versions. No task is executed or closed by writing this review.

## Evidence entry points

- Current manuscript: [paper.tex](../paper.tex), [paper.pdf](../paper.pdf).
- Three prior main-branch responses: [first](author_response_main_20261013.md),
  [second](author_response_main_round2_20261013.md), [third](author_response_reviewer2_20261015.md).
- [Round-3 protocol](../round3_protocol.json), [reproduction](../round3_reproduction.md),
  [claim ledger](../claim_evidence.csv) and [selected asset identity](../revision_selection.json).

Completion is a basis for reassessment, not a promise of acceptance or authorization to submit or upload.
