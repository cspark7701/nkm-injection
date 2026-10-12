# Milestone 161 — Plan a standalone BTS optics paper

Completed 2026-10-13: created `docs/paper_bts/README.md`, `001_manuscript_outline.md` and `002_manuscript_tasks.md` at the author's request. Proposed target is Journal of the Korean Physical Society (Research Article), with current official scope and author guidance linked in the outline.

## Scientific basis and decisions

Read the selected deterministic optimization summary/config/candidate table, historical physics/error coverage, MOGA decision, author inputs, current scripts and pooled tolerance analysis. Verified the two selected optimization hashes and all four tolerance-summary hashes recorded by the pooled analysis. The four runs select the same optimization/config and error-budget hashes.

Selected peak beta is 31.4368/50.7459 m, with one feasible start of three and nominal mismatch zero at floating-point precision. The pooled historical optics ensemble contains 550,000 samples with zero invalid evaluations and five feasibility failures. Median horizontal mismatch is 0.00208629 [0.00207403, 0.00209890] at 95% confidence. Preserve the failed 50k prefix checks and passing 400k prefix check; do not interpret optical feasibility as beam transmission or storage-ring capture.

The outline proposes a distinct BTS design/correction question, section and figure/table plans, a provisional abstract and source/assumption reconciliation. Twelve pending tasks cover novelty, physical boundaries, hardware/beam inputs, validation, nominal matching, normalized correction knobs, active error coverage, fair design comparisons, uncertainty, held-out transport, writing and final review/evidence packaging. MOGA is optional and requires corrected dimensions, budgets and physical finalist validation.

## Verification and scope

This milestone creates documentation only. No new simulations, manuscript build or scientific revision tasks were executed. Existing NKM manuscript/review files and protected inputs were hash-snapshotted before editing and verified unchanged afterward. Markdown local links and whitespace were checked; no new executable code or tests were introduced. Actual campaign outputs remain ignored in their original directories. Updated the root README and completed-plan index to link the new outline.
