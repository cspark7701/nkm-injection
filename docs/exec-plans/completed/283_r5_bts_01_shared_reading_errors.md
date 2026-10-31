# Milestone 283 — R5-BTS-01: shared reading errors and targeted reruns

Completed: 2026-10-31. Round-5 task R5-BTS-01 (Reviewer 2 R2D-02; Reviewer 1 R1D-BTS-02, pairing and attribution),
from `docs/paper_bts/reviews/revision_round_05_plan_for_review_round_04.md`.

**Protocol.** `docs/paper_bts/round5_protocol.json` was declared before the runs, and covers:
- **Reading errors:** keyed by realization and monitor location (element-boundary index) through
  `bts_round4.shared_reading_errors`, and shared by every setting and layout.
- **Primary estimator:** see R5-BTS-02.
- **Studies:** the duplicate-configuration check, the angle-weighted layout and the edge study.
- **Failed first runs:** `final_test/` and `layouts/` failed before any output. The imported round-4 runner was not
  registered for worker pickling; it is now registered in `sys.modules`. Both are retained, and the stages were
  rerun unchanged as `final_test_b/` and `layouts_b/`.

**Code.**
- `run_bts_round4._machine` takes a `reading_noise` mode, `per_setting` (rounds 3–4, the default) or `shared`, and
  applies per-layout end weights.
- `scripts/run_bts_round5.py` adds the stages final_test, layouts and edge_study.
- `scripts/export_bts_round5_assets.py` installs `generated/round5*` and `figures/round5_jitter_transfer.pdf`.
- **Tests,** in `tests/test_bts_round4.py`: shared errors depend only on realization and location, and two copies
  of one full configuration give identical steering and losses (run through the runner's `_machine` with tracking).

**Results.** `results/bts_round5_campaign_20261031`:
- **Second test,** seeds 96001–96005, shared readings:

  | Setting | Lost particles (of 1.2 million) |
  | :--- | ---: |
  | Matched reference | 11 673 |
  | Low beta | 10 104 |
  | Edge (loss-based) | 942 |
  | Round-3 loss-based | 942 |
  | Duplicate copy | 942 |
  | Dispersion-free | 1 |

  The duplicate check passes (`duplicate_identical: true`). The round-4 difference between the round-3 and edge
  settings (1 022 and 1 564 particles) therefore came from their separate reading-error draws.
- **Layouts,** seeds 91001–91005, shared readings, with the angle-weighted layout added:
  - the matched-reference rows reproduce round 4 exactly;
  - the loss-based setting loses 0.38 %, against 0.23 % with its own round-4 reading errors.
- **Note on the reproduction.** The matched reference reproduces round 4 because NumPy's `SeedSequence` pads zeros:
  the shared draw `[seed, realization]` equals the old design-index-0 draw `[seed, realization, 0]`.

**Article.**
- Section 2.4 states the shared reading errors, noting that Table 4 (round 3) still used per-setting draws.
- The layout paragraph and Table 5 come from `round5_layout_rows.tex`.
- The second-test paragraph and Table 7 (`round5_test_rows.tex`) show expected and observed counts. The attribution
  is now controlled, and "optically identical" is replaced by "same nominal horizontal transfer". The
  factor-of-3-to-10 sentence is removed, and the estimator follows in R5-BTS-02.

All prose edits follow the humanizer rules. The isolated build is clean, and 17 round-4 and import tests pass.
Protected files are unchanged.
