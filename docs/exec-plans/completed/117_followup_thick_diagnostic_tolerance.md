# Milestone 117 — Follow-up campaigns: thick-magnet robustness, three-seed diagnostics, 400k tolerances

Completed: 2026-10-10. Requested options 1, 2 and 4 of the post-submission-package review; plus an attribution
cross-check that option 1 required. All runs: native element tracking, coupled BTS, 200 particles × 500 turns, frozen
error budget, OMP/OpenBLAS threads = 1. Drivers in `results/journal_campaign_01/logs/run_followup_{s7,s4,cross}.sh`.

| Option | Runs | Result |
| :--- | :--- | :--- |
| 1 thick NKM under combined errors | 3 × 50 (+ zero error), re-matched x′ = 4.636 mrad | 47.4 % [42.4, 52.4] vs thin 37.8 %; paired +9.5 [+6.1, +13.2] |
| 1b attribution (added) | thin@4.636 and thick@4.869, seeds 42/123 | angle only −1.8 [−4.4, +0.9]; model +5.3 [+1.7, +9.2]; re-match +3.9 [+1.2, +6.7] |
| 2 diagnostics on 3 seeds | static corrected 123/777; no jitter 42 (n = 50), 123, 777 | corrected 40.9 % (+3.0 [+0.4, +5.7]); no jitter 50.8 % (+13.0 [+8.8, +17.3]); seed-42 rerun reproduces earlier 30 exactly |
| 4 tolerance precision | 400,000 samples, seed 2026, prefix 200k/400k | prefix change 2.4×10⁻⁶ (target 1×10⁻⁵ **met**); pooled 550k median 2.086×10⁻³ [2.074, 2.099], 5 failures, bound 2.1×10⁻⁵ |

Code: `fieldmap_thick` model and `--thick-slices` in `scripts/run_capture_robustness.py`, `--stored-model` in
`scripts/analyze_capture_robustness.py` (commit 1e4086e, test added). Figure builder: 20 new manifest artifacts, Fig 6
redrawn (thick ECDF; capture vs signed septum angle error, thin vs thick), Fig 7 shows four tolerance runs, new macros
for paired gains, cross-runs and single-particle amplitude sensitivity. Manuscript: abstract, §4, §5.1, §5.2, captions,
discussion, limitations and conclusions updated; the thin kick is now described as optimistic for the nominal beam
(−4 points) but pessimistic under errors (+9.5 points). Docs: `capture_robustness.md`, `tolerance_uncertainty.md`,
`scientific_review.md`, `claim_evidence.csv` (B15–B18), `submission_checklist.md`. Gated package build
`submission_package_v2`: 10 pages, clean; `docs/paper/paper.pdf` updated. Results remain uncommitted.
