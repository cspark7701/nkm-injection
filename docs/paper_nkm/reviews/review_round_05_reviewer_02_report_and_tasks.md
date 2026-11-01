# Referee report — Reviewer 2, fifth round

**Manuscript:** "Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design
lattice" (C. S. Park), PRAB REVTeX version.
**Version reviewed:** `docs/paper_nkm/paper.tex`, `paper.pdf` (34-page one-column preprint), `paper_twocolumn.pdf`
(17 pages) and `supplement.pdf` (7 pages), at commit `ccc5c86`. The manuscript was last changed by the round-4
rewrite (`207e4fc`) and the prose pass of milestone 299 (`79dce19`).

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `62d03c80d7a404ef` |
| `paper.pdf` | `11786804edf067f3` |
| `paper_twocolumn.pdf` | `24ba0a61f99b12ba` |
| `supplement.tex` | `35f689b7b4188a74` |
| `supplement.pdf` | `48a9409d4093d8eb` |
| `revision_manifest_round4.json` | `6580a19cc36b89e7` |

**Also read:**
- all four rounds of author responses, in particular
  [the round-4 response](review_round_04_author_response_to_reviewers_01_02.md) to my R2d-1 to R2d-7 and three
  questions;
- the round-4 notes on ablation, two-plane steering, operating points, associations, loss locations, dispersion
  scope, and pulse and transparency;
- the companion BTS manuscript's current treatment of the same booster jitter and BTS error budget.

**Date:** 2026-11-01. Internal pre-submission assessment, not a journal decision.
**Reviewer expertise:** storage-ring beam dynamics, off-axis and multipole-kicker injection, transfer-line design,
pulsed-magnet modelling.

## Recommendation

**Minor revision. The paper is scientifically acceptable in principle. I expect to recommend acceptance after the
headline is reframed and one targeted jitter scan is run (R2e-1 and R2e-2), together with the consistency
corrections below.**

The fourth revision answers my round-4 objection in the way I hoped:
- **The paired ablation identifies the cause.** The ~28-point NKM-specific gap without jitter comes from the BTS
  magnet errors (−39.2 points alone for the NKM, −14.5 for the dipole). They act through a 0.90 mm / 77 µrad rms
  static vertical injection error that the model's horizontal-only steering cannot remove.
- **The mechanism is physical.** A vertically displaced centroid receives a vertical kick proportional to the local
  horizontal kick slope, which is steep at the selected point. It is supported by the first-turn vertical loss
  records and by the two-plane steering sensitivity, which restores the NKM to 76.6 % without jitter.
- **The "chiefly booster angle jitter" claim is withdrawn,** and the abstract no longer makes it.
- **The operating-point comparison shows the gap is point-dependent.** The dipole loses 17–23 points at the
  alternatives, so the selected point, chosen without injection errors, favours the uniform kick. This is now stated.

What remains is a question of what the headline represents, and of the jitter regime in which it holds.

## Status of my round-4 tasks

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2d-1 paired ablation and rewrite | **Resolved** | Seven declared classes, draws held fixed, alone and omitted effects with paired intervals, and non-additivity reported. The causal text follows the ablation. |
| R2d-2 operating points | **Resolved** | Paired earlier and extremum-centred points with recalibrated controls; point retained under a declared rule; the "does not test" sentence removed and the selection limitation stated. |
| R2d-3 pulse at the selected point | **Resolved** | One allowance convention (0.044 mrad); native returns; limits 5.76 / 5.33 µs; `round2_pulse` re-pointed, with identity checks. |
| R2d-4 signed associations | **Resolved** | Signed and physical predictors, both models and their difference, Holm-adjusted and labelled exploratory. |
| R2d-5 losses and chromaticity | **Resolved** | First-turn vertical losses located; numerical domain separated from the physical boundary; chromaticity claim reduced; ring 5501 consistent with uncorrected coupling. |
| R2d-6 dispersion | **Resolved** | Septum D = 80.9 mm and D′ = 47.5 mrad in Table II, with their angular contributions. |
| R2d-7 editorial | **Largely resolved** | Two point-label inconsistencies remain (minor 2). The tuning range is accepted as is by the author's decision. |
| Questions 1–3 | Answered | Kick slope +0.32 against −0.09 mrad/mm; septum dispersion inherited from the BTS target; zero-capture clustering traced to the vertical error. |

## Major comments

### M1. The headline describes the configuration without vertical correction

The abstract and conclusions lead with "16.1 % … against 44.1 % for an equally strong uniform kick". The paper then
shows that this deficit is caused mainly by the uncorrected static vertical injection error, and the companion BTS
manuscript confirms that the modelled line has no vertical corrector. The two-plane sensitivity on the same full
budget gives:

| Steering | Full budget, NKM | Full budget, dipole | Gap | Without booster jitter, NKM |
| :--- | ---: | ---: | ---: | ---: |
| Horizontal only (headline) | 16.1 % | 44.1 % | −28.0 points | 40.1 % |
| Two-plane | 33.9 % | 57.2 % | −23.3 points | 76.6 % |

The abstract quotes the 76.6 %, but not the 33.9 / 57.2 % pair that applies under full jitter. A reader therefore
cannot see that, once the vertical error is corrected, a full-budget deficit remains and is now carried by booster
jitter.

The horizontal-only population is a legitimate model result. But a transfer line without vertical correction is not
an operational design. The headline should not leave the reader thinking that 16 % is the NKM's capture in a
correctable configuration.

**Requested.**
- Give the full-budget results under both steering assumptions in the abstract and the conclusions, and say which
  population the headline number refers to.
- Attribute the horizontal-only deficit to the absent vertical correction in the modelled line, not to the NKM alone.

### M2. State the booster-jitter regime and evaluate the NKM where it would be operated

The booster centroid jitter (0.5 mm / 0.2 mrad) is shared with the companion BTS manuscript. That manuscript now
states that this is 1.3 and 2.2 beam sizes at extraction, treats it as a stress level, and finds that 0.1–0.2 of it
changes its conclusions qualitatively.

Here, Table III lists the value as an unsourced sensitivity assumption without beam-size units. The only
reduced-jitter evidence (Table IV) uses horizontal-only steering, where the vertical error dominates: the gap is
already −28 points at zero jitter. "Even a quarter of the assumed jitter fails" is therefore mostly a statement about
the uncorrected vertical error.

Under two-plane steering only zero and full jitter are available. The Discussion's requirement to "stabilize the
booster extraction" is consequently unquantified.

**Requested.**
- State the jitter in beam-size units, and as a stress level unless a source is supplied.
- Run a paired jitter scan under the declared two-plane steering: the same 50 seed-42 realizations, particles and
  rings; scales of at least 0, 0.1, 0.25, 0.5 and 1; both models; paired 95 % realization-bootstrap intervals.
- Report the jitter level at which the declared one-point noninferiority test passes, or that it does not pass within
  the scan.

This reuses the existing machinery, so no new campaign design or ring ensemble is needed.

### M3. Reconcile the shared quantities with the companion manuscript

Both manuscripts use the same BTS line, error budget (gradient 0.1 %, offsets 100 µm, rolls 0.5 mrad, dipole field
0.05 %) and booster jitter. They quote different values of the same static vertical centroid at the septum exit:
- **NKM:** 0.90 mm and 77 µrad rms, from 50 seed-42 realizations (`round4_ablation.md`);
- **BTS:** about 1.07 mm and 0.096 mrad for the matched reference, from 200 independent realizations.

With 50 draws, the relative standard error of an rms is about 10 %, so the difference is plausibly sampling. It
should be stated rather than left for the reader.

**Requested.**
- Quote each population, cross-reference the companion value, and confirm that the BTS strengths and error-draw
  definitions are identical.
- Align the jitter wording with the companion.

## Minor comments

1. **Abstract.** "161 µrad, 3.7 times a tenth of the angular window" is hard to parse. Write "3.7 times the 0.044 mrad
   allowance". The abstract is also long for PRAB's guidance of about 250 words.
2. **Selected-point labels.**
   - Table I's "this study" row gives the peak kick at the earlier point (4.89 mrad, S = 0.85) but the disturbance at
     S = 0.95. Use the selected point, or label the mixed row.
   - Add the selected-point peak kick beside the S = 0.85 value in Table II.
3. **Date line.** "Dated: October 20, 2026" predates the October 31 prose revision.
4. **Recovery statements.** In the conclusions, state that the two-plane sensitivity is an upper bound on what
   correction can recover, since a fitted correction with monitor errors recovers less. The companion BTS study
   finds about 0.18 mrad of horizontal residual for such a correction.
5. **Tuning gain.** Attach "under horizontal-only steering and without booster jitter" to the +11.9-point tuning gain
   in the conclusions.
6. **Status documents.** `docs/paper_nkm/README.md` and the review index should describe the executed round 4 and this
   round consistently, with page counts that match the installed files. Dated reports and responses stay unchanged.
7. **Data availability.** Confirm at submission that the GitHub repository named in the statement is publicly
   accessible.

## Questions to the author

1. Under two-plane steering, what is the NKM-minus-dipole gap at a quarter of the assumed jitter?
2. Do the NKM and BTS studies use identical BTS strengths and error-draw definitions?
3. Is any vertical correction foreseen for the BTS version studied? If so, the two-plane sensitivity can be described
   as representative rather than ideal.

## Revision tasks (for the author)

Priority: **A** = required for acceptance, **B** = recommended, **C** = editorial. Earlier tasks R2d-1 to R2d-7 are
closed. All boxes are open at review.

- [ ] **R2e-1 (A) — Headline under both steering assumptions (M1).**
  - [ ] In the abstract and conclusions, give the full-budget NKM and dipole capture under horizontal-only steering
        (16.1 / 44.1 %) and under two-plane steering (33.9 / 57.2 %), and name the headline population.
  - [ ] Attribute the horizontal-only deficit to the absent vertical correction.
  - *Done when:* no headline sentence reads as the NKM's capture with a correctable vertical error left in place.
- [ ] **R2e-2 (A) — Jitter regime and a two-plane jitter scan (M2).**
  - [ ] State the jitter in beam-size units, and as a stress level unless sourced.
  - [ ] Declare and run the paired two-plane jitter scan: scales of at least 0, 0.1, 0.25, 0.5 and 1, on the same
        realizations, particles and rings, for both models.
  - [ ] Report the noninferiority outcome per scale, and quantify the "stabilize the booster extraction" statement.
  - *Done when:* the NKM-specific loss is given as a function of jitter with vertical correction present.
- [ ] **R2e-3 (A) — Companion consistency (M3).**
  - [ ] Quote the vertical-centroid populations, cross-reference the BTS value, and confirm the shared strengths and
        error definitions.
  - [ ] Align the jitter wording with the companion.
- [ ] **R2e-4 (C) — Abstract wording and length (minor 1).**
- [ ] **R2e-5 (C) — Selected-point labels in Tables I and II, and the date line (minors 2 and 3).**
- [ ] **R2e-6 (B) — Recovery statements (minors 4 and 5).**
  - [ ] State that the two-plane sensitivity is an upper bound.
  - [ ] Attach the conditions to the tuning gain.
- [ ] **R2e-7 (C) — Status documents (minor 6).**
- [ ] **R2e-8 (A) — Reconciliation and response.**
  - [ ] Update the claim table, manifest, figure provenance and generated macros for the new result.
  - [ ] Rebuild both PRAB layouts and the supplement under the clean-log gate, and run the relevant tests.
  - [ ] Write a point-by-point response, preserving earlier reports and responses.
- [ ] **R2e-9 (submission) — Evidence access (minor 7).** Confirm that the named repository is publicly accessible, and
  record final author approval separately.

**Suggested order:**
1. Declare and run the R2e-2 scan.
2. R2e-1 and R2e-3, which use its result.
3. R2e-4 to R2e-7.
4. R2e-8.

R2e-9 is handled at submission.

## Choice of journal

PRAB remains the right venue for a finite-length accuracy study with a full capture and attribution analysis.

## Confidential comments to the editor

The round-4 ablation was the decisive test, and it overturned the paper's earlier causal claim on evidence. That is
to the author's credit.

My remaining request is mainly about framing. The headline should not present the configuration without vertical
correction as the NKM's performance. The jitter scan is small, reuses existing realizations, and would tell
designers how stable the booster must be. After these, I expect to recommend acceptance.
