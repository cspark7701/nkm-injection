# Response to Reviewers 1 and 2 — BTS round 3 (round-4 revision)

This joint response addresses:
- the [Reviewer 1 round-3 report](reviewer1_bts_20261030_main_round3_report.md) and its tasks R3-BTS-01 to 08;
- the [Reviewer 2 round-3 report](reviewer2_bts_20261030_main_round3_report.md) and its tasks R2C-01 to 10.

Both were executed through the [consolidated register](round4_consolidated_revision_tasks.md), R4-BTS-01 to 14
(milestones 265–278). The reports, task registers and all earlier responses are unchanged. This is a pre-submission
revision record, not a journal decision; the scientific interpretation awaits the author's approval.

**Evidence.**
- **Protocol:** [round-4 protocol](../round4_protocol.json), declared before the campaigns. Its amendments are
  recorded in the protocol before the outputs they affect.
- **Reproduction:** [round-4 reproduction guide](../round4_reproduction.md).
- **Claims:** BR4-01 to BR4-14 in the [claim ledger](../claim_evidence.csv). All 63 claims verify with
  `scripts/audit_bts_evidence.py`.
- **Lattice:** the BTS lattice is not changed.

## Summary of what changed in the conclusions

1. **The loss reduction is a property of large booster jitter (R2 M1).** The assumed jitter is 1.3 / 2.2 beam sizes
   at m1. At that level the loss-based gain is 4.7, measured with the exact jitter average. At 0.1–0.2 of the level
   every setting loses at most 3 × 10⁻¹¹. The abstract and conclusions now state this regime.
2. **The static residual is small; earlier statements are corrected.** Averaged exactly over the jitter, the static
   residual adds only 2–5 % to the loss. The spread between populations (0.97–2.30 % for the matched reference)
   comes from sampling the jitter tail with 600 shots.
3. **The loss of a matched setting depends on μ_x alone (R2 M4, R1 M5).** The lower edge of the configured matched
   range, 200.17°, is set by no strength bound and no peak-beta limit. The round-3 loss-based setting is optically
   identical to the converged edge solution.
4. **The baseline no longer leads the paper (R2 M2).** It is an unmatched starting point of recorded provenance, and
   its blade overlap is a consequence of how d_b is defined.

## Reviewer 1 (R3-BTS)

| Task | Response | Milestone |
| :--- | :--- | :--- |
| R3-BTS-01 boundary theorems | Sections 3.1–3.2 are restricted to the nominal, error-free, uncoupled, exactly matched line. Σ_out(K,e) is stated, and restrictions upstream of q11 are K-independent even with errors. J is defined as the non-dispersive centroid jitter. Static errors are "reduced", with the residual, optics errors and vertical trajectory named. The statement about the static-residual effect is corrected by measurement (milestone 267). | 266, 267 |
| R3-BTS-02 round-aperture bounds | `ellipse_loss_probability` gives the exact 2-D Gaussian loss outside round and elliptical apertures, so the max/union bracket is now valid. A test checks the centred 5σ counterexample, exp(−12.5) = 3.73 × 10⁻⁶ against 4Φ(−5). A full rerun reproduces all 66 selected round-3 numbers bitwise, so the correction is methodological. "Within 1 %" is now "relative, for aggregate means". | 265 |
| R3-BTS-03 discrete checks | The narrowed claim was chosen. Losses are counted at element entrances and the line end, with the blade checked at both septum ends; no continuous interception is claimed. Every recorded first loss is at the blade. | 269 |
| R3-BTS-04 mean clearance | The explanation now uses uncensored moments (mean exit x −68.5 µm uncorrected, +8.8 µm corrected) and the analytic E[c]/E[P] argument. "Indistinguishable" is replaced by the paired intervals; the bootstrap and its tail limitation are stated. | 270 |
| R3-BTS-05 sampled-search language | "Pins", "reach only" and "reachable" are removed. The ranges are "found by sampled and local searches". The loss-based setting is the "best-found feasible setting at the lower edge". The exit-target leverage is conditional on the alternatives tested. A constrained scan with edge searches was added at Reviewer 2's request. | 274 |
| R3-BTS-06 pairing and precision | Reading errors are disclosed as drawn per setting, while magnet errors, shots and particles are shared. The effect is shown directly: the round-3 loss-based and edge settings are optically identical, with jitter-integrated losses of 0.28 % and 0.29 %, yet lose 0.085 % and 0.13 % when tracked. The objective's scope (error-free, nominal beta) is stated. The dispersion-free result is now tracked. | 274–276 |
| R3-BTS-07 self-contained submission | The TDR difference stays prominent. The baseline provenance is stated, and the supplement's title, date, introduction and nomenclature are aligned. Data availability, the target journal and final approval remain author decisions; nothing is invented. | 273, 277 |
| R3-BTS-08 reconciliation | 14 new claims; the audit and `--verify` pass; full tests pass; clean builds; new installed PDFs and hashes. This response is new, and earlier responses are unchanged. | 278 |

## Reviewer 2 (R2C)

| Task | Response | Milestone |
| :--- | :--- | :--- |
| R2C-01 jitter | The jitter is stated in beam-size units (1.3 / 2.2σ at m1; 4.0σ at the exit). With no KLS specification available, it is called a stress level. A sweep (×0, 0.05, 0.1, 0.2, 0.5, 1) uses a jitter-integrated loss per steered realization (new Table 9). The loss reduction is a large-jitter property, and at realistic levels the design output is the position–angle partition. | 267 |
| R2C-02 baseline framing | The abstract and first Discussion paragraph are rewritten. The baseline is an unmatched starting point supplied with the configuration (in the repository since milestone 01; no design target recorded). Its blade overlap follows from d_b. Setting names are unified, and the loss-based setting appears in the abstract and Table 7. Figures 2–3 keep the author-requested baseline comparison, relabelled "Baseline setting". | 277 |
| R2C-03 constrained scan | μ_x is added as an equality on a 2° grid for both exits, with SLSQP edge searches. Configured exit: the lower edge, 200.17°, has no active constraint; the upper edge, 232.0°, is the 60 m limit. Dispersion-free exit: 187.2–214.5°, with q22 at its bound setting the upper edge. The loss falls monotonically with μ_x (Figure 5). Second fresh tracked test: matched reference 0.97 %, edge 0.13 % (−0.84 [−1.39, −0.40] percentage points). | 274 |
| R2C-04 blade distance | Loss against d_b from 1 to 3 mm at ×1 and ×0.1 jitter (Figure 6). Reaching 0.1 % needs 2.05 mm (matched reference) or 1.64 mm (loss-based). At ×0.1 jitter, even 1 mm gives at most 2 × 10⁻⁶. The ring-acceptance cost and the TDR 1 mm septum are noted. | 268 |
| R2C-05 steering | The assumed eleven readings and the independent powering are stated. Five readings change nothing; series-powered b1–b3 raise the exit-angle spread to 0.44 mrad. The vertical exit centroid, 1.12 mm / 0.10 mrad, goes in Table 5. "Angle spread falls", "small residual" and "indistinguishable" are corrected. | 266, 270, 276 |
| R2C-06 dispersion-free | Tracked: 1 of 1.2 million particles lost, consistent with the jitter-integrated prediction of 6.2 × 10⁻³ %, with a non-Gaussian-tail caveat. The configured 80.9 mm / 47.5 mrad is stated as inherited from the NKM configuration, with no derivation from the ring. | 275 |
| R2C-07 length and structure | Section 3.4 and its tables moved to the supplement; Eq. (5) has its one-sided form; the roll rows of Table 8 are collapsed. The article nevertheless grew to 19 pages, with the new Tables 5, 7 and 9 and Figures 5–6. | 271 |
| R2C-08 title and wording | New title. Other changes: "within 1 % relative", the Gaussian caveat, the Introduction redundancy, "septum entrance" against m1, and the bootstrap method. | 265, 270, 272, 277 |
| R2C-09 supplement and declarations | Supplement nomenclature aligned; the duplicated Acknowledgments removed. Data availability and approval remain author decisions. | 273 |
| R2C-10 response update | This document. Changes made after the earlier Reviewer 2 response, and not recorded there: the title (now revised again), the baseline-versus-optimized framing (milestone 259; now demoted), the "matched reference" and "error realization" nomenclature, and the removal on 2026-10-30, at the author's request, of the generative-assistance and data-availability statements and the appendix. | 278 |

## Answers to Reviewer 2's questions

1. **Origin of the baseline strengths.** They are the quadrupole settings supplied with the BTS configuration and
   have been in the repository since its first milestone (`record_baseline_metrics.py`, 2026-07-23). No record
   states the exit target they were designed for.
2. **KLS booster extraction stability.** No specification is available to us, so the article treats
   0.5 mm / 0.2 mrad as a stress level. This is an open author input, shared with the NKM paper.
3. **Active constraint at the lower edges.**
   - *Configured exit, 200.17°:* three converged searches end there with no strength bound and neither peak-beta
     limit active.
   - *Dispersion-free exit:* the converged search ends at 187.6° on the vertical 60 m limit, and searches stopped at
     their iteration limit reach 187.2° with no constraint active.
4. **Common power supply for b1–b3.** This is not known for the studied design version. Series powering is examined
   as a layout (Table 5).
5. **Monitors.** The lattice model contains none. Eleven readings are assumed, and a five-reading layout is examined
   (Table 5).

## Open items (author decisions)

- **Target journal:** JKPS or NIM A.
- **Data availability:** a statement that matches actual access.
- **Booster jitter:** a source for the jitter level, which should then change in both papers.
- **Final approval:** final scientific approval of the revised text and conclusions.
