# Milestone 284 — R5-BTS-08: provenance pointer, citations and stability statement

Completed: 2026-10-31. Round-5 task R5-BTS-08 (Reviewer 1 R1D-BTS-04; Reviewer 2 R2D-09). The status documents and
layout counts are updated after the final build in R5-BTS-10.

**Provenance.**
- `export_bts_round4_assets.py` wrote the `test_source` of `generated/round4_phase.json` as
  `final_test/final_test.json`. That directory holds only the configuration of a stopped run. The pointer now names
  the selected `final_test_b/final_test.json`.
- All round-4 provenance paths are now repository-relative; they were absolute.
- The round-4 assets were re-exported. Their numbers are unchanged; the JSON files differ only in their source
  paths.
- The blade figure's legend now reads "Loss-based (R3)", the setting name used in the round-4 tables since
  milestone 274.
- The round-5 assets record repository-relative sources (`generated/round5.json`).

**Citations.**
- **Booster stability (Section 2.4).** The uncited general statement ("commonly specified as a fraction of the beam
  size") is removed. The text now says only that no KLS specification is available, so the values are a stress
  level.
- **TPS reference [13].** It was checked on 2026-10-31. The JaCoW reference record
  (https://refs.jacow.org/reference/show/208939) lists IPAC'26 paper TUP2685 as "presented … unpublished", with no
  DOI or pages. The entry now uses that wording, and the abstract link is kept; no publication details were invented.
- **Companion NKM manuscript [5].** It stays "in preparation"; how referees get access to it is an author action
  (R5-BTS-09).

The isolated build is clean. Protected files are unchanged.
