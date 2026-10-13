# Milestone 184 — Review the BTS manuscript on main

Completed 2026-10-13 at the author's request. Wrote a new referee-style report and ten ordered revision tasks under `docs/paper/reviews/`, with the BTS identity explicit in their names. The reviewed manuscript is the eight-page `docs/paper_bts/` draft at main commit `bee78914caa16945ef63dba8bf5205c434d0415c`.

## Decision and scope

Recommendation: major revision, with no acceptance in its present form. The report recognizes traceable historical results and careful optical-feasibility versus transmission distinctions. It calls for a completed physical contribution, justified boundary/hardware/beam specifications, active-error and independent transport validation, finite correction/margin evidence, correct claim/provenance documents and accessible referee data.

Local BTS branch `466fca5` holds a later manuscript and reviews; those are not judged by this main-version report. The workspace remained on main, and no branch was merged or rebased for this review. Milestone 184 follows numbering already used through 183 on the local BTS branch, avoiding duplicate sequence numbers across the branches.

## Evidence examined

Read the TeX, PDF, exported tables, bibliography, draft provenance, B01 scope/literature/inventory/claim documents, and B01–B12 plan. Verified all nine recorded scientific-source hashes and all three installed manuscript asset hashes. Inspected the three candidate outcomes, pooled and per-seed summaries/OAT values, and all five actual failing records in the 50k/400k runs with failures. Read the current optimizer, raw-Jacobian, applied-error and OAT/failure definitions. Verified the historical 60.01 m beta and 2.05 sum-mismatch criteria against raw evaluation metadata.

Confirmed supporting-document errors: mixed-unit Jacobian labelled normalized, swapped OAT labels/values, nominal start called random, failed optimization called converged, nonexistent pooled CI key, two bends instead of three main bends, inaccurate artifact sizes and generating-commit conflation. Checked current official JKPS scope/guidance and a publisher record showing a MAX IV title mismatch in the literature survey. Unverified references are labelled unresolved rather than declared nonexistent.

## Validation and preservation

Protected scientific inputs, BTS manuscript/plan/evidence files and previous review reports were snapshotted and checked unchanged. The review README was extended with an index entry while preserving its earlier content. Checked new local links, ordered revision IDs, manuscript/source version identity, unchanged scientific inputs and whitespace. This is a documentation/review task; no physics simulations, manuscript recompilation or numerical test suite were run. No external messages, GitHub API access, fetch or push were performed.
