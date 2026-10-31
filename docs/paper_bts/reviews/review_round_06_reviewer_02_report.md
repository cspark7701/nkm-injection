# Reviewer 2 — BTS manuscript, review round 6

**Manuscript:** *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker
injection at the Korea Light Source* (C. S. Park).
**Version reviewed:** the current article at `fd16b2a`: `docs/paper_bts/paper.tex`, `paper.pdf` (19 pages),
`supplement.tex` and `supplement.pdf` (10 pages). This version answers the round-5 reports of
[Reviewer 1](review_round_05_reviewer_01_report.md) and [Reviewer 2](review_round_05_reviewer_02_report.md),
through the [joint response](review_round_05_author_response_to_reviewers_01_02.md).

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `c104f180a476c63f` |
| `paper.pdf` | `31db583223793bd5` |
| `supplement.tex` | `7080d250c5dbebf8` |
| `supplement.pdf` | `04c94cf1a89ef3a3` |
| `paper.bib` | `f70c675c47c1e010` |

**Read first:**
- all main-branch author responses, rounds 1–5;
- my earlier Reviewer 2 reports (rounds 1–5 under the current file numbering);
- Reviewer 1's round-5 report, which recommends accepting the scientific content;
- the saved round-5 per-shot output I cite below.

**Date:** 2026-10-31. Internal pre-submission assessment, not a journal decision.

**Scope.** The R5-BTS-09 submission decisions remain deferred to the submission-ready stage and are not assessed
here. They cover the journal, data-availability wording, companion access, the jitter source and final approval.

## Recommendation

**Accept. The paper is scientifically acceptable in its present form. The items below are editorial and
optional; none is a condition of acceptance, and I do not need to see the paper again.**

The round-7 revision resolved all six of my round-5 tasks (R2F-BTS-01 to 06):
- the low-beta conclusion now rests on the controlled shared-reading result, −0.13 [−0.24, −0.04] percentage points,
  and the older 0.21 contrast is explicitly labelled confounded;
- the probability bracket is stated as a bound on model probabilities within the linearized Gaussian model;
- the loss-based excess is localized: one near-blade shot carries about 70 % of it, and the cause is honestly left
  unresolved;
- the headline gain is described in the abstract as a linearized Gaussian-model prediction whose interval reflects
  only the sampling of error realizations;
- the vertical residual is attributed to the absence of a vertical corrector in the modelled line;
- the figure labels are consistent, and the older steering table moved to the supplement.

The response also corrects an error of mine. I wrote that the 942 loss-based losses occur in 20 shots. The saved
record gives 16 loss-bearing shots, and I have confirmed this. The aggregate numbers I used were unaffected.

The paper now makes a clear, bounded contribution:
- **Matched ends.** They fix the nominal blade clearance, so lowering the interior peak beta does not help at the
  limiting restriction.
- **Phase advance.** In the nominal model the blade loss depends on the horizontal phase advance alone.
- **Inherited D′.** Within local searches, the lowest phase advance found is restricted by the exit dispersion
  slope.
- **Two regimes.** The phase advance is the design knob only at stress-level booster jitter. At realistic jitter,
  the steering residual and the uncorrected vertical trajectory dominate the delivered beam.

The evidence is controlled, the comparisons are paired with shared errors, and the limitations are stated where
the claims are made.

## Status of my round-5 tasks

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2F-BTS-01 low-beta evidence | Resolved | The wording alternative was adopted, and the 0.21 is labelled confounded in Section 4.2 and the Discussion. |
| R2F-BTS-02 bracket and excess | Resolved | The bracket is a model-probability statement, and the excess is localized (16 shots; one carries about 70 %). The optional nonlinear check was not done, and the cause is stated as unresolved, which I accept. |
| R2F-BTS-03 interval scope | Resolved | Stated in the abstract and Section 4.3. |
| R2F-BTS-04 wording and labels | Resolved | — |
| R2F-BTS-05 shortening | Partly resolved | The older steering table moved to the supplement; the article is 19 pages. Advisory only. |
| R2F-BTS-06 reconciliation | Resolved | 80 claims; current hashes; round-7 increment verified. |

## Editorial suggestions (optional)

1. **Section 4.2, opening paragraph.** The section still opens with the earlier per-setting-reading steering
   comparison, now in the supplement. It quotes "1.47 % for the low-beta setting" before the confounding caveat
   arrives a paragraph later. The matched-reference numbers are identical in the shared-reading Table 4, so the
   paragraph could cite Table 4 for them, and either drop the low-beta 1.47 % or move it next to its caveat.
2. **Abstract length.** The abstract is about 300 words. Springer and Elsevier journals usually ask for 150–250.
   Each qualification added in recent rounds is correct, but some can move to the Introduction or Discussion: the
   interval scope sentence, and the three-bend/nine-quadrupole description. This should be done when the journal is
   chosen.
3. **Optional diagnostic.** The nonlinear-moment check of the 454-particle shot would tell whether the linearized
   surrogate underestimates near-blade losses. It would strengthen the methodological point in the Discussion, but
   the paper is correct without it.
4. **Length.** At 19 pages and about 10,100 tokens before the references, the article remains long for JKPS's
   recommended 4,000 words. A final shortening pass for the chosen journal is advisable. The author's wish to keep
   the baseline figures and the literature review is noted.

## Assessment

Over six rounds the manuscript changed from an optics-statistics study with a degenerate question into a
well-posed, honestly qualified design study. Its central mechanism is correct, its controls are appropriate, and
its headline numbers are defined and scoped. **I recommend acceptance.** The editorial suggestions above can be
handled at the submission-formatting stage, together with the deferred author declarations.

## Confidential comments to the editor

The author has answered every substantive point over six rounds, including several where new evidence overturned
earlier statements, and corrected my own counting error.

The remaining suggestions are editorial. Both referees now regard the scientific content as acceptable within its
stated scope.
