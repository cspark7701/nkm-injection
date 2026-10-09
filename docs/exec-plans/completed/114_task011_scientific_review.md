# Milestone 114 — Journal Task 011: independent scientific review

Completed: 2026-10-09. Task: [011](../../jinst-paper/tasks/011_independent_scientific_review.md).

Referee-style review recorded in [`scientific_review.md`](../../jinst-paper/scientific_review.md). Headline numbers were
recomputed from raw campaign files and agree. A model gap was found and quantified: a thick drift–kick–drift NKM
(`ThickNKMKicker`, `scripts/run_thick_nkm_check.py`, identical S6 bunches) captures 87.0 % (re-matched angle) versus
91.1 % for the thin kick, so thin-kick capture is optimistic by ≈ 4 points; the abstract, §4 and limitations now say so
(manifest entry `thick_nkm_check`, macros `Thick*`, claim B14). Wording fixes: paired-dipole gap, static-correction
versus jitter, mrad units. Local workflow checker (full regression, protected-file immutability) passed; manuscript
compiles cleanly (10 pages).
