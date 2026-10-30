# Milestone 261 — BTS author wording revision, KLS TDR citation and split affiliations

Completed: 2026-10-30 at the author's request (task list of 2026-10-30).

## Affiliations (both papers)

Two separate affiliations: Department of Accelerator Science and Center for Accelerator Research, Korea University,
Sejong, 30019, Republic of Korea. BTS: numbered affiliations in `docs/paper_bts/paper.tex`. NKM: two `\affiliation`
entries in `docs/paper/paper.tex` and `supplement.tex`. The extra affiliation line overfilled the one-column NKM title
page by 1 pt; the abstract was shortened by one line ("assumed" removed, one clause tightened, and the closing
"not operational efficiency predictions" dropped from "These are conditional simulation results").

## KLS TDR

Added `KLSTDR2025`: Pohang Accelerator Laboratory, *Korea-4GSR Technical Design Report*, 4GSR-I-DE-TDR-001
(October 2025), from https://kls.kbsi.re.kr/eng/sub0305/view/id/63794. The Introduction cites it and states that the
TDR BTS line has two dipoles and eight quadrupoles and that baseline injection uses a four-kicker bump with a 1 mm
in-vacuum thin septum (TDR Sec. 2.1.4 E, 2.1.5); the studied line is a different nine-quadrupole, three-bend design
version. The TDR thin septum is also cited next to the NKM-study blade geometry (the blade citation).

## Wording

- "companion NKM study" → "NKM injection study" / "our study of NKM injection"; "TPS conference contribution" →
  "TPS study"; "appreciably" and "assumed" removed.
- "original" setting → "baseline" setting in text, captions, figure legends and the nominal table; the matched
  intermediate setting, formerly "matched baseline", is now "matched reference" to avoid a clash. "Original" meaning
  the earlier four-station campaign is reworded as "earlier campaign".
- "machines" → "error realizations" (defined in Sec. 2.4); "machine-cluster interval" → "interval clustered by error
  realization".
- Sec. 2.1 opens with "The baseline BTS model" and states AT/pyAT use with citations; kicker and septa named.
- Sec. 2.2: "This study"; plane index u defined; quadrupole rolls named; Eq. (2) explained; beta-versus-clearance
  units clarified; rigidity/pole-field paragraph rewritten.
- Sec. 2.3: removed the "no element added…", "never tracked" and "d_b is neither…" sentences.
- Sec. 2.4: Tikhonov objective written out with λ = 1e-3 × largest singular value of WA (as in
  `bts_round3.correct_trajectory`), cited to Tikhonov & Arsenin (1977).
- Units added to intervals and bare values (µm, µrad, mm, percentage points); 0.00035 m → 0.35 mm; "0.000 percentage
  points" → "less than 0.001 percentage points"; "exit lattice functions"; "Two observations arise from these
  results"; pool count reads "matched quadrupole settings".
- Removed the first sentence of the last Discussion paragraph, the Generative-assistance and Data-availability
  statements, and Appendix A. Status documents record the removal.

## Figures and tables

- Figure 1 (`export_bts_at_figures.py`): labels for q11–q33, b1–b3, kext, sept_in, sept_ex and m1–m4.
- Figures 2–4 and the nominal table: "Baseline setting", "Optimized − baseline", "Matched reference",
  "test realizations".
- Table 1: "Prescribed entrance and exit lattice functions". Table 2: Basis column and last caption sentence removed.

Regenerated with the documented `pyat-dev` environment (pyAT 0.7.2.dev26; earlier installs used 0.8.0, giving
~1e-14 differences in the validation JSON). Round-3 macros are unchanged.

## Validation

- BTS article built under the clean-log gate (`results/bts_paper_build_20261030a`, 15 pages) and installed;
  `revision_selection.json` hashes refreshed; `package_bts_revision.py --verify` passes; `audit_bts_evidence.py`
  verifies all claims.
- NKM one-column (33 pages), two-column (17) and supplement (7) built clean and installed
  (`results/nkm_submission_20261030e`, `…f`).
- 759 tests pass; protected files unchanged. Scientific approval of the new wording remains with the author.
