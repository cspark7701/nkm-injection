# Referee report — Reviewer 2, sixth round

**Manuscript:** "Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design
lattice" (C. S. Park), PRAB REVTeX version.
**Version reviewed:** `docs/paper_nkm/paper.tex`, `paper.pdf` (36-page one-column preprint), `paper_twocolumn.pdf`
(18 pages) and `supplement.pdf` (7 pages), at commit `2c813fe`, dated November 1, 2026.

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `f9e8dc4603b56d59` |
| `paper.pdf` | `91d0043489195330` |
| `paper_twocolumn.pdf` | `caeed92a1611a36c` |
| `supplement.tex` | `936f36cd37432d98` |
| `supplement.pdf` | `e6147e7dca6f78b2` |
| `revision_manifest_round5.json` | `9a6392fb71cc46d7` |

**Also read:**
- all five rounds of author responses, in particular the
  [round-5 response](review_round_05_author_response_to_reviewers_01_02.md) to my R2e-1 to R2e-9 and to
  Reviewer 1's evidence assessment;
- the [G1–G7 register](revision_round_05_plan_for_review_round_05.md);
- the round-5 jitter and companion-comparison notes;
- the supplement's Table S4.

**Date:** 2026-11-01. Internal pre-submission assessment, not a journal decision.
**Reviewer expertise:** storage-ring beam dynamics, off-axis and multipole-kicker injection, transfer-line design,
pulsed-magnet modelling.

## Recommendation

**Accept. The paper is scientifically acceptable in its present form. The suggestions below are editorial and
optional, and I do not need to see the paper again.**

The fifth revision did what I asked:
- **Headline under both steering assumptions (R2e-1).** The abstract and conclusions now give the 150-realization
  horizontal-only result (16.1 against 44.1 %) and the paired 50-realization two-plane sensitivity (33.9 against
  57.2 % under full jitter, 76.6 % for the NKM without jitter), with their populations named. The horizontal-only
  deficit is attributed to the absent vertical correction in the modelled line.
- **Jitter regime and scan (R2e-2).** The jitter is a stated stress level of 1.3 and 2.2 extraction beam sizes. The
  paired two-plane scan was declared before tracking and reuses the paired endpoints after configuration checks. It
  answers the design question directly: no nonzero tested scale passes the one-point acceptable-loss test, including
  one tenth of the stress level (−2.3 [−4.3, −0.7] points). The paper correctly says this sets no continuous
  threshold or hardware specification.
- **Companion consistency (R2e-3).** It was resolved honestly. The audit found that the two studies share the
  nominal BTS strengths and element sequence but differ in dipole-error correlation (common here, independent per
  bend in the companion), in steering and in population summaries. The paper states this, and I agree with
  withdrawing the sampling-only explanation I had suggested.
- **Editorial items (R2e-4 to R2e-8).** Done: the 250-word abstract, the point labels and date, the recovery and
  tuning scope, the status documents, and the reconciliation with a frozen-source verification.

The scientific content is now complete for its stated scope:
- **Thin-map error.** A single thin kick map misdescribes this strongly self-deflecting magnet; a sliced vector map
  does not.
- **Capture under errors.** Capture is evaluated with paired controls and declared populations.
- **Attribution.** Ablation traces the NKM-specific loss to an identified physical mechanism: the vertical kick on a
  displaced centroid where the kick slope is steep.
- **Operational demand.** Even with ideal vertical correction, the NKM loses capture at a tenth of the assumed
  booster jitter, while the uniform kick does not. That is a clear and useful negative result.

## Status of my round-5 tasks

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2e-1 headline under both steering assumptions | **Resolved** | Populations, budgets and steering named in the abstract and conclusions. |
| R2e-2 jitter regime and two-plane scan | **Resolved** | Declared protocol; scales 0, 0.1, 0.25, 0.5 and 1; paired intervals; noninferiority per scale; no continuous-threshold claim. |
| R2e-3 companion consistency | **Resolved** | Definitions and model differences stated; the sampling-only explanation removed. |
| R2e-4 abstract | **Resolved** | "3.7 times the 0.044 mrad allowance"; 250 words. |
| R2e-5 point labels and date | **Resolved** | — |
| R2e-6 recovery and tuning scope | **Resolved** | Two-plane steering called an optimistic ideal benchmark. I accept the author's refusal of a universal upper-bound claim. |
| R2e-7 status documents | **Resolved** | — |
| R2e-8 reconciliation | **Resolved** | 272-key manifest; clean-log builds; 775 tests; frozen-source archive verified. |
| R2e-9 submission access | Deferred | Submission-stage author gate (G7). |
| Questions 1–3 | Answered | Quarter-jitter gap −15.7 [−21.3, −10.6] points; error definitions differ; no vertical correction foreseen in the supplied input. |

## Editorial suggestions (optional)

1. **The most design-relevant number is not in the abstract.** Two-plane steering at one tenth of the assumed jitter
   is the scenario closest to an operating regime. It gives 74.2 % NKM against 82.9 % uniform-kick capture (gap
   −8.6 [−12.5, −5.4] points). The NKM loses 2.3 points from its zero-jitter baseline, while the uniform kick loses
   nothing (+0.2 [−0.2, +0.7], Table S4), and neither has a zero-capture realization. The abstract currently ends the
   jitter story with the full-budget numbers and the stress-level label. One clause would let readers see that the
   NKM remains workable but measurably jitter-sensitive at small jitter, without claiming that 0.1 is a measured
   stability. A word could come from elsewhere to stay at about 250 words.
2. **The sensitivity at small jitter.** At 0.1 of the stress level, the centroid jitter at the magnet is a small
   fraction of a millimetre, yet it costs the NKM 2.3 points and the uniform kick nothing. One sentence linking this
   to the steep local kick slope (+0.32 mrad/mm, round-4 question 1) and the 0.44 mrad window would make the
   mechanism explicit. Check the arithmetic before stating it. If the slope alone does not account for the loss, say
   that the mechanism at small jitter is not isolated.
3. **Which dipole-error correlation is intended.** The two companion papers now differ in the BTS dipole-field
   error model. If the bends are series-powered, a common relative error is the physical choice. In the present
   model the ideal horizontal steering removes the static horizontal trajectory, and dipole field errors act mainly
   horizontally. Verify whether the correlation choice can affect the vertical centroid or capture. If it cannot,
   say so in one sentence; if it is not checked, say that. This would close the cross-paper question without forcing
   the two models to agree.
4. **Length.** The one-column preprint has grown to 36 pages. PRAB sets no strict limit, and the two-column version
   is 18 pages. A final trim of repeated qualifications, for example in the Discussion and Section VII B, would help
   readers. This is advisory.

## Revision tasks (optional; none is a condition of acceptance)

All boxes are open at review. The submission-stage gate G7 (repository access, evidence delivery, declarations and
final approval) is not repeated here.

- [ ] **R2f-1 — Small-jitter result in the abstract (suggestion 1).**
  - [ ] Add one clause giving the two-plane capture at one tenth of the assumed jitter (74.2 against 82.9 %; NKM
        −2.3 [−4.3, −0.7] points, uniform kick +0.2 [−0.2, +0.7]), keeping the stress-level qualification and the
        word limit.
- [ ] **R2f-2 — Mechanism at small jitter (suggestion 2).**
  - [ ] Check whether the local kick slope and the angular window account for the NKM's 2.3-point loss at 0.1
        jitter, and state the result in one sentence, or state that the small-jitter mechanism is not isolated.
- [ ] **R2f-3 — Dipole-error correlation (suggestion 3).**
  - [ ] State which BTS dipole-error correlation is physically intended.
  - [ ] Verify whether the common-versus-independent choice can affect the vertical centroid or capture under the
        ideal horizontal steering, and report the result, or that it is unchecked.
- [ ] **R2f-4 — Final trim (suggestion 4, advisory).**
  - [ ] Remove repeated qualifications where they occur more than once, keeping every assumption and limitation
        once.
- [ ] **R2f-5 — Record.**
  - [ ] If any of R2f-1 to R2f-4 is done, rebuild both layouts and the supplement under the clean-log gate, refresh
        the affected manifest and claim entries, and note the changes briefly. Preserve all earlier reports and
        responses.

## Choice of journal

PRAB is the right venue. The finite-length accuracy result and the paired attribution analysis are of direct
interest to designers of nonlinear and multipole injection kickers.

## Confidential comments to the editor

Over five revisions the author answered every substantive request, and twice let new evidence overturn the paper's
own earlier causal claims. The final jitter scan was declared before it was run and reported without softening an
unfavourable result. I recommend acceptance; the suggestions above are optional improvements of emphasis.
