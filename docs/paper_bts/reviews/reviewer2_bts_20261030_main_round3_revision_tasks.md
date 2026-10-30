# Reviewer 2 round-3 revision tasks — BTS main-branch manuscript

Tasks from the [Reviewer 2 round-3 report](reviewer2_bts_20261030_main_round3_report.md) (2026-10-30) on the
manuscript at `603c3ab`. All tasks are open at review.

Priority: **A** = required for acceptance, **B** = strongly recommended, **C** = editorial. "Sim" = new
calculation. "Analytic" means the existing Gaussian loss model is enough; no particle tracking is needed.

| ID | Priority | Task | Sim | Acceptance criterion | Est. effort |
| :--- | :---: | :--- | :---: | :--- | :--- |
| R2C-01 | A | **Booster jitter level (M1).** Source the 0.5 mm / 0.2 mrad jitter at m1, or label it a stress level. Sweep position and angle jitter together (×0.1, 0.2, 0.5, 1) for the matched reference, low-beta and loss-based settings. Report the loss, the loss-based gain and the level at which static residuals dominate. | analytic | Jitter stated in beam-size units; sensitivity table with betatron-jitter rows; abstract and conclusions state the regime the results apply to | 1 d |
| R2C-02 | A | **Baseline framing (M2).** State the provenance of the baseline `BTSConfig` strengths and the exit target they were designed for. Present the baseline as a starting point only, not a result. Rewrite the abstract and the first Discussion paragraph around boundary-fixed clearance, the phase-advance jitter partition, the loss observable and the jitter dependence. Use one name per setting; the recommended (loss-based) setting must appear in the headline figures or tables. | no | Abstract no longer leads with matching the unmatched baseline; no circular blade-clearance claim; consistent setting names | 0.5–1 d |
| R2C-03 | A | **Constrained phase-advance scan (M4).** Add μ_x as an equality and minimise peak beta over a μ_x grid, for the configured and dispersion-free exits. Report feasibility, the active bound at each interval edge, the predicted loss and the exit angle jitter. Replace the iteration-limited SLSQP point by the scan optimum; keep the fresh tracked test for the chosen point. | yes (matching) | Loss versus angle-jitter trade curve; active constraint named at 200.2° and 187.7°; converged chosen point | 1–2 d |
| R2C-04 | A | **Blade-distance sweep (M5).** Predicted loss against d_b for the three settings at the present and a realistic jitter level. State the d_b for a stated loss tolerance (e.g. 0.1 %) and note the ring-acceptance cost of a larger d_b. Relate it to the TDR 1 mm thin septum. | analytic | Figure or table of loss versus d_b; tolerance statement | 0.5 d |
| R2C-05 | B | **Steering assumptions (M3).** State the assumed instrumentation (eleven horizontal readings) and the independent powering of the six trims. Repeat the correction with a reduced monitor set (one per triplet plus the septum) and, if b1–b3 share a supply, with four knobs. Report the vertical exit centroid rms (position and angle). Correct "angle spread falls", "small residual" and "indistinguishable in every column". | yes (small) | Assumptions stated; reduced-instrumentation row; vertical exit centroid in Table 6; wording consistent with Tables 6–7 | 1 d |
| R2C-06 | B | **Dispersion-free point (minor 4).** Track the best dispersion-free setting on the fresh realizations, or quote its gain only as an order of magnitude with a non-Gaussian-tail caveat. Explain why the configured exit inherits 80.9 mm / 47.5 mrad. | yes (tracking) | Tracked loss or qualified analytic statement; dispersion origin stated | 0.5–1 d |
| R2C-07 | C | **Length and structure (minors 2, 3, 7).** Move Section 3.4 and Tables 3–4 to the supplement, keeping a one-sentence summary. Move the last Section 2.2 sentence (historical ensembles) with them. Fix or drop Eq. (5) for the one-sided restriction. Collapse the roll rows of Table 8. | no | Main text shortened; no symmetric-station equation applied to a one-sided edge | 0.5 d |
| R2C-08 | C | **Title and wording (minors 1, 5, 6, 10–12).** Title naming the studied design version; "Booster-to-Storage-Ring". "Within 1 % relative". Gaussian-validation caveat. Introduction redundancy. "Septum entrance" versus m1. The clustering method of the intervals. | no | Text | 0.5 d |
| R2C-09 | C | **Supplement and declarations (minors 8, 9).** Align the supplement nomenclature ("error realizations", "baseline", "matched reference"). Deduplicate Funding and Acknowledgments. Remove "final approval is pending" before submission. Restore a data-availability statement, with the wording the author chooses. | no | Consistent nomenclature; declarations ready for submission | 0.5 d |
| R2C-10 | C | **Response update.** Extend the Reviewer 2 response to record the changes made after it: the new title, the baseline framing, the matched-reference nomenclature and the removed sections. Answer questions 1–5 of the report. | no | Response matches the manuscript | 0.5 d |

## Suggested order

1. **Analytic sweeps, R2C-01 and R2C-04.** They may change the emphasis of the paper and are cheap.
2. **Phase-advance scan, R2C-03.** It replaces the iteration-limited optimizer result.
3. **Framing, R2C-02.** Rewrite the headline once the jitter-dependent results are known.
4. **Model checks, R2C-05 and R2C-06.**
5. **Editorial, R2C-07 to R2C-10.**

## Coordination with the companion NKM manuscript

- **R2C-01.** The booster jitter is shared with the NKM injection study, which uses the same 0.5 mm / 0.2 mrad at
  m1. Any change of level or justification should be made in both papers.
- **R2C-04 and R2C-06.** These touch the injected-beam geometry (blade distance) and the injected dispersion, which
  the NKM paper also uses.
- **R2C-05.** Its vertical exit centroid is the input to the static vertical injection error discussed in the NKM
  paper.

Per the author's instruction, the BTS lattice is not changed by any of these tasks. R2C-05 varies only which
existing element boundaries carry readings and which existing dipoles are trimmed.
