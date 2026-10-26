# Milestone 251 — Strengthen the BTS introduction and scientific presentation

Completed: 2026-10-26 at the author's request to improve the introduction, terminology, spelling, captions, and companion citation.

## Changes

- Rewrote the introduction around transfer-line requirements, previous studies, the distinction between interior beta reduction and loss at fixed-boundary restrictions, the study goal and comparison method, and a labeled section roadmap. Removed the conversational framing and the previous final sentence about algorithmic novelty. Retained the existing literature basis without adding claims of demonstrated ring capture.
- Used American English throughout the main text and supplement; retained `siunitx` quantity formatting and added explicit units to the quadrupole strength bounds.
- Applied the requested entrance/exit lattice terminology and caption deletions. Removed the undocumented-derivation sentence, the hardware-specification phrase, and manuscript-revision references from the scientific narrative. Model assumptions and the configured exit target remain identified.
- Defined b1, b2, and b3 as the three main dipole bending magnets, in beam order. Removed the dipole-name parenthesis from the trajectory-correction description.
- Replaced the obsolete ten-quadrupole MAD-X comparison with the current BTS model's independent analytical validation. The current BTS model retains its actual nine quadrupoles.
- Added `ParkNKM2026`, an unpublished companion-manuscript entry with its current title, author and “Manuscript in preparation” status. Cited it for the injection geometry and related results; no arXiv URL or identifier was invented.

## Validation

Built the main paper from final sources in `results/bts_editorial_final_20261026/paper` (12 pages) and the supplement in `results/bts_editorial_20261026/supplement` (8 pages). Both passed the isolated builder's layout/reference gate. Visually checked the introduction, roadmap, lattice description, Figure 1 and boundary table. Checked all citation keys and section references, the requested wording removals, American spellings, whitespace and changed paths.

Installed both PDFs and refreshed the five current source/bibliography/PDF digests in `revision_selection.json`; asset verification passes. Numerical exports, simulation inputs, existing reviews and the historical referee attachment remain unchanged. This editorial task did not require simulation or unrelated pytest reruns. No push or external submission was performed.
