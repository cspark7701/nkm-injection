# Milestone 249 — Clarify the BTS abstract boundary conditions

Completed: 2026-10-26 at the author's request to apply the discussed abstract wording and commit.

Replaced the absolute statement that quadrupoles cannot change endpoint beam sizes with two sentences: the transfer line transports the extracted booster beam while satisfying storage-ring injection requirements; for fixed beam parameters and prescribed entrance/exit optics, quadrupole rematching preserves nominal endpoint sizes. This distinguishes the physical motivation from the study's fixed matching constraints without asserting an undocumented derivation of the exit targets from ring optics.

Rebuilt and installed the 12-page main PDF using `python scripts/package_bts_revision.py --build-dir results/bts_abstract_opening_20261026`. The isolated build passed the existing layout/reference gate; visually checked the first page. Refreshed only the current `paper.tex` and `paper.pdf` asset digests in `revision_selection.json`; `python scripts/package_bts_revision.py --verify` passes. Checked whitespace and changed paths. Protected inputs, numerical results, supplement and historical referee attachment remain unchanged. No simulation or unrelated pytest suite was rerun for this wording change; no push performed.
