# Independent scientific review of the manuscript (Task 011)

Date: 2026-10-09. Reviewed: `paper.tex` (Task 008), generated assets (Task 009), references (Task 010).
Reviewer stance: referee for JINST, looking for unsupported claims, model gaps and numerical inconsistencies.

## 1. Numerical cross-checks (independent recomputation from raw files)

Recomputed outside the figure builder (`results/journal_campaign_01/review/independent_checks.txt`, not committed):

| Quantity | Manuscript | Recomputed from raw | Status |
| :--- | :--- | :--- | :--- |
| NKM / linearised / dipole / off capture (4 × 500) | 91.1 / 96.2 / 94.6 / 0.0 % | 0.9105 / 0.9625 / 0.9460 / 0.0 | agrees |
| Baseline-BTS capture | 26.9 % | 0.2690 | agrees |
| Pooled combined-error capture (150) | 37.8 %, median 34.5 % | 0.3785, 0.3450 | agrees |
| On-momentum DA | −12 to +13 mm | −12.0 / +13.0 mm | agrees |
| Tolerance seed 123 failures, median M_x | (pooled) | 1 failure, 2.079e-3 | consistent with pooled 2.095e-3 |

Every quantity in the text is a macro from `generated/journal_macros.tex` (test `test_installed_macros_cover_manuscript`).

## 2. Model gap found and quantified: thin versus thick NKM

Referee question: the 0.525 m NKM is modelled as a thin kick at its centre, but the injected trajectory crosses
≈ 2.6 mm inside the magnet in a region where the kick gradient is large. Check: `scripts/run_thick_nkm_check.py`
integrates the identical S6 replicate bunches (4 seeds × 500 particles, native ring tracking, 500 turns) through the
`By.txt` profile in 160 drift–kick–drift slices (`ThickNKMKicker`; zero-field identity, sign and no-extrapolation tested).

| Model | Mean capture | Per seed |
| :--- | ---: | :--- |
| thin kick map (reproduction of S6) | 91.05 % | 90.6, 91.4, 92.0, 90.2 |
| thick, same injection angle | 87.4 % | 86.8, 87.4, 88.8, 86.6 |
| thick, angle re-matched (4.64 mrad) | 87.0 % | 87.0, 87.8, 86.8, 86.4 |

All losses are ring losses (no septum-creation or outside-map losses). Conclusion: thin-kick capture values are optimistic
by ≈ 4 percentage points; the conclusions (window position, dipole comparison, robustness ranking) are unchanged.
Action taken: the abstract quotes the thick-magnet value, §4 reports the check, §6 lists it as a limitation.
Not checked: thick-magnet effect on the combined-error ensemble (expected to shift it by a similar amount).

## 3. Claim review

| Item | Finding | Action |
| :--- | :--- | :--- |
| "transparent" | supported for the aligned kicker; qualified by the alignment dependence (0.10 σ at 0.2 mm) | kept with qualifier |
| paired dipole difference | earlier wording implied the NKM–dipole gap was negligible; it is 16.5 points under errors | corrected (§5.2) |
| static correction vs jitter | static correction gives +1.1 ± 2.8 points (n.s.), removing jitter +11.2 ± 4.1 | stated; jitter named as the limiting error |
| linear-map overestimate | supported by paired backend comparison | kept; linear map used only as cross-check |
| tolerance prefix target | unmet (1.1–2.1e-5 > 1e-5) | disclosed in §5.1 |
| MOGA | not part of the evidence | omitted (moga_decision.md) |
| units | mrad (not "mm rad") for angles | corrected in §4 |

## 4. Software and reproducibility

- `NKM_PYTHON=<pyat-dev python> ./scripts/check_github_actions.sh --quiet`: all selected local checks passed, including the
  full regression suite and the pre/post protected-file immutability checks (exit 0).
- Figure builder verifies SHA-256 of all 18 manifest artifacts; rebuild reproduces `journal_macros.tex`.
- Isolated LaTeX build (pdflatex → bibtex → pdflatex × 2): 10 pages, no errors, undefined references or overfull boxes.
- No remote GitHub Actions were queried; nothing was pushed.

## 5. Remaining referee-level limitations (stated in the paper)

Ring without magnet errors and chamber apertures; magnetostatic map without measurement; assumed error budget;
500-turn survival instead of lifetime; no sextupole or septum-optics optimisation; single seed for the diagnostic
ensembles.

## Verdict

Suitable to proceed to the submission package (Task 012) after author review of the thick-magnet result and the
funding statement.
