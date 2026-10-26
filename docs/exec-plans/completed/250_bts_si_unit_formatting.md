# Milestone 250 — Use siunitx for BTS quantities

Completed: 2026-10-26 at the author's request to use `\SI` for numbers and units.

Added `siunitx` to the main manuscript and supplement. Converted explicit physical quantities and percentages to `\SI`, lists to `\SIlist`, and hand-written unit-only labels to `\si`. Preserved numerical values, generated scientific exports and the frozen historical evidence attachment.

Built both documents in fresh isolated directories under `results/bts_si_units_final_20261026/`; the existing layout/reference gates pass. Installed the PDFs and refreshed their four source/PDF hashes in `revision_selection.json`. Asset verification and whitespace checks pass. No scientific simulations or unrelated pytest runs were needed. Protected files are unchanged. The subsequent request for shaded constraint-space plots and paragraph development is a separate task.
