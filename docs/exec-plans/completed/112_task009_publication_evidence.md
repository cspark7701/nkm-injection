# Milestone 112 — Journal Task 009: selected evidence, figures and provenance

Completed: 2026-10-09. Task: [009](../../jinst-paper/tasks/009_publication_data_and_figures.md).

Added `docs/jinst-paper/campaign_manifest.json` (17 explicitly selected campaign artifacts with SHA-256 digests; no
timestamp discovery) and `scripts/build_journal_figures.py`, which verifies the digests, regenerates seven figures
(kick/geometry, DA, model validation, operating window, paired controls and transparency, capture robustness, BTS optics
and tolerance), computes the bicubic stored-beam response, and writes `generated/journal_macros.tex` (all numbers quoted in
the text), `generated/figure_provenance.csv` and `generated/consumed_artifacts.json` (repository-relative paths and digests).
Figures use a validated categorical palette (dataviz validator: all checks pass; aqua relieved by markers/labels), a single-hue
sequential ramp, one axis per panel, and were inspected for collisions. `claim_evidence.csv` gained B1–B13 mapping every new
article claim to its artifact and macro. Tests: `tests/test_journal_figures.py` (formatting, digest enforcement, every
manuscript macro defined). Rebuilding from the manifest reproduces the macros exactly. Old historical figures in
`docs/jinst-paper/figures/` are no longer referenced by the manuscript.
