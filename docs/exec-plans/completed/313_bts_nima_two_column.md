# Milestone 313 — Add the two-column NIM A BTS manuscript

Completed: 2026-11-01.

Added [paper_twocolumn.tex](../../paper_bts/paper_twocolumn.tex) and its [15-page PDF](../../paper_bts/paper_twocolumn.pdf). The wrapper selects Elsevier's `final,5p,twocolumn` layout and inputs the existing manuscript. Both formats share scientific text, numerical macros, citations and figures. Wide tables/figures remain readable across both columns; two paired equations stack in the narrow format. Ragged-bottom column setting avoids artificial vertical stretching. No scientific prose or numerical values were changed.

Extended `scripts/build_bts_nima_submission.py` with optional `--two-column`. The default article-and-supplement build remains available. The expanded flat source ZIP includes the wrapper and all three bibliographies; it rebuilds the 19-page preprint, 10-page supplement and 15-page two-column article. Updated manuscript indexes, submission instructions and selected hashes, preserving the earlier one-column NIM A selection as `nima_preprint_final_assets_sha256`.

Selected output: `results/bts_nima_twocolumn_20261101_v2/`, with build identities and fresh extracted-verification records. The initial unsuccessful layout build remains diagnostic output.

Validation: all three PDFs build and rebuild from the extracted flat source archive without layout/reference warnings; extracted PDF text agrees with the corresponding selected builds. One-column PDF text matches the previous conversion exactly. Inspected the two-column title/abstract, clearance equation, schematic, table and main result figures. All 80 evidence claims and 94 selected asset hashes pass. Checked local links, Git whitespace and changed-file scope. Protected source data and prior reviews/responses remain unchanged. No scientific simulation or regression suite was rerun for this layout-only change, and no submission occurred.
