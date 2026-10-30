# Reviewer 2 — BTS main-branch manuscript, round 3

**Manuscript:** *Optical matching and beam loss in the Korea Light Source Booster-to-Storage transfer line*
(C. S. Park). Previously titled *Beta reduction and physical clearance in a parametric booster-to-storage-ring
transfer line*.
**Version reviewed:** `docs/paper_bts/paper.tex`, `paper.pdf` (15 pages) and `supplement.tex` on `main` at
`603c3ab`. SHA-256 prefixes:

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `9595cca2dd36819a` |
| `paper.pdf` | `7595e38e50115fb9` |
| `supplement.tex` | `abc593c2599e25c8` |
| `paper.bib` | `0a2210e5b160b3ab` |

**Read first:**
- the three main-branch author responses:
  - [Reviewer 1, round 1](author_response_main_20261013.md);
  - [Reviewer 1, round 2](author_response_main_round2_20261013.md);
  - [Reviewer 2](author_response_reviewer2_20261015.md);
- my [round-2 report](reviewer2_bts_20261015_main_report.md) and the Reviewer 1 reports they answer;
- the generated tables and macros the article inputs (`generated/round3_*.tex`,
  `generated/original_setting_comparison.tex`).

**Date:** 2026-10-30. Internal pre-submission assessment, not a journal decision.
**Reviewer expertise:** transfer-line optics and matching, injection into low-emittance storage rings, aperture and
error modelling.

## Recommendation

**Major revision; the present version is not acceptable, but the route to acceptance is now short.**

The revision answers my round-2 objections in substance:
- the realistic restriction (the injection-septum blade) is in the model;
- static steering is included;
- the design observable is a validated loss probability, not mean clearance.

The phase-advance argument of Section 3.2 is a genuine and transferable result. I would support publication of a
paper built on it.

Two problems remain, and both concern inputs rather than numerics:
1. **The booster shot jitter is unrealistically large, and it drives every loss number in the paper.** It is not
   varied in the sensitivity study (M1).
2. **The new baseline-versus-optimized framing is circular** and now leads the abstract (M2).

Neither needs new machinery. Both can be settled with the existing analytic loss model and short text changes.

## Status of the earlier requests

### Reviewer 1, rounds 1 and 2

The responses to Reviewer 1 established:
- transport validation;
- centred maps and quadrature;
- the limiting-station mechanism;
- paired machine-cluster inference.

I accepted these in round 2 and do not reopen them.

### My round-2 tasks

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2B-01 element-wise apertures | Resolved | Every element carries an aperture, and the blade is one-sided at the stated distance. The unsourced gap and channel dimensions are labelled and swept. |
| R2B-02 analytic boundary-fixed clearances | Resolved | Section 3.1 is now correct and concise. |
| R2B-03 trajectory correction | Resolved with caveats | Horizontal steering by dipole trims, with the lattice unchanged, is acceptable. The readings, however, assume monitors that the lattice does not contain, and the vertical exit error is not reported (M3). |
| R2B-04 loss-relevant objective | Resolved | Tracking agrees with the Gaussian prediction within 1 %. The optimizer evidence is weak, but the conclusion does not depend on it (M4). |
| R2B-05 exit target and dispersion | Largely resolved | The source of the target is stated and the divergence budget is given. The dispersion-free result is analytic only (minor 4). |
| R2B-06 error-level sensitivity | Formally resolved | Rolls and energy jitter are varied as I asked. The decisive input, the betatron jitter, is not varied (M1). I should have requested it in round 2. |
| R2B-07 editorial and declarations | Partly reopened | The round-2 abstract was good. The later rewrite has reintroduced a weak headline (M2). The availability statement has been removed rather than finalised (minor 9). |

### Changes not covered by the Reviewer 2 response

The [Reviewer 2 response](author_response_reviewer2_20261015.md) says the title is kept. Since then, the
manuscript has also changed in ways the response does not record:
- **Framing:** the baseline-versus-optimized comparison (Section 4.1, Table 5, Figs. 2–3, the abstract and the
  first Discussion paragraph);
- **Title and nomenclature:** a new title, and the "matched reference" terminology;
- **Removed sections:** the generative-assistance statement, the availability statement and the appendix.

A referee at the journal will compare the response with the manuscript, so the response must be brought up to date.

## Major comments

### M1. The booster jitter is several beam sizes, sets every loss number, and is not varied

The jitter at m1 is 0.5 mm rms in position and 0.2 mrad rms in angle (Section 2.4). From Table 1 and Section 2.2:

| Quantity at m1 | Beam (rms, with dispersion) | Jitter (rms) | Jitter / beam |
| :--- | ---: | ---: | ---: |
| Position | 0.379 mm | 0.5 mm | 1.3 |
| Angle | 91 µrad | 200 µrad | 2.2 |

In normalised phase space, the mean centroid action of the jitter is about 54 times the beam emittance, so a typical
shot centroid sits about 5σ from the design orbit. At the exit the paper's own numbers give:
- jitter position spread: 0.643 mm (matched reference) and 0.506 mm (loss-based);
- beam size: σ_x = 0.159 mm;
- so the jitter is 4.0σ and 3.2σ;
- the blade distance d_b = 1.478 mm is only 2.3 and 2.9 jitter standard deviations.

The 1–2 % blade losses, the 3.3-fold gain and the conclusion that "booster shot jitter governs the remaining
interception" all follow from this input.

Booster extraction stability is usually specified as a fraction of the beam size, typically 10–20 % of σ. That is
the level at which top-up injection with a transparent injection kicker makes sense, and it is presumably the level
the NKM scheme assumes. A centroid moving several σ shot to shot would also overwhelm the kicker's 0.44 mrad
angular acceptance quoted in Section 4.4. The paper itself finds an exit-angle jitter of 0.33–0.39 mrad, almost
the whole acceptance.

The text calls the values "model inputs" and says they are "the same as in the NKM injection study". Consistency
with the companion paper is necessary, but it is not a justification.

**Requested.**
1. Source the jitter level: booster extraction-kicker and septum ripple, booster orbit stability, or a published
   specification from a comparable booster. Otherwise state plainly that 0.5 mm / 0.2 mrad is a stress level.
2. Add the betatron jitter to the sensitivity study. This is cheap, because the shot-averaged loss is analytic
   (Eq. 7 with the summed covariance):
   - scale position and angle jitter together, for example 0.1, 0.2, 0.5 and 1 times the present level;
   - report the loss of the three settings;
   - report the loss-based gain;
   - report where static residuals, rather than jitter, start to dominate.
3. Report the gain as a function of jitter level. The phase-advance mechanism (Eq. 6) is independent of the
   jitter level, but the loss gain is not. At a realistic level the blade loss may be negligible for every setting,
   and the useful output of the paper becomes the exit position/angle jitter partition rather than a loss reduction.
   The paper should say which regime the KLS line is in.

### M2. The baseline-versus-optimized comparison is circular and should not lead the abstract

The abstract now opens with the finding that the baseline setting "does not satisfy the prescribed exit lattice
functions and has insufficient nominal clearance at the injection-septum blade". Table 5 shows the baseline exit:
- β_x = 45.0 m and β_y = 242.6 m against targets of 2.34 m and 4.26 m;
- a normalised residual of 4.8 × 10³.

This is not a nearly matched design setting that optimization improves. It is a set of strengths that does not
belong to this exit target. The paper does not say where the strengths come from. They are the `BTSConfig`
defaults, and the TDR line has a different magnet count, so they are not the TDR setting either.

The blade clearance comparison is circular as well:
- the blade distance d_b is defined from the matched exit beam as 3σ_x + 1 mm (Section 2.3);
- any setting whose exit β_x is 19 times larger must therefore have negative clearance.

So "matching restores positive clearance" restates how d_b was chosen.

Three consequences:
- **Headline.** The first half of the abstract and the first Discussion paragraph present an expected property of
  any matched solution as a result.
- **Two optimized settings.** The "optimized" setting of Figs. 2–3 and Table 5 is the vertical-beta setting, which
  the paper later shows gives no resolved loss change. The setting the paper recommends (loss-based) appears only
  in Table 7 and Fig. 4. A reader of the abstract will take the wrong setting as the result.
- **Two references.** The abstract's "reference" (the baseline) and the error study's "matched reference" are
  different settings. Section 4.1 has to warn the reader of this twice, and so does the Fig. 4 caption.

**Requested.**
- State the provenance of the baseline strengths: which design, for which exit target.
- If they were designed for a different exit, say so, and present the baseline only as a starting point. One
  sentence and Table 5 suffice; Figs. 2–3 can show the matched reference against the low-beta and loss-based
  settings, all with the same exit.
- If they are a real candidate setting for this target, explain why the exit is so far off.
- Rewrite the abstract and the first Discussion paragraph around the results that carry the paper:
  - boundary-fixed nominal clearance;
  - the phase-advance partition of jitter;
  - the validated loss observable;
  - the jitter-level dependence from M1.
- Use one name for one setting throughout.

### M3. Steering assumptions: monitors, power supplies and the vertical exit error

The steering model is acceptable in principle, but three assumptions need stating or checking.

1. **Monitors.** "No corrector or monitor element is added", yet readings are taken after each of the nine
   quadrupoles, at the septum entrance and at the line end, which amounts to eleven BPMs. The lattice contains only
   the markers m1–m4. The readings are therefore assumed instrumentation. That is fine, but the text should say so,
   together with the reading count. It should also show how the result changes with a realistic set of, say, three
   or four BPMs or screens, for example one per triplet plus the septum.
2. **Independent trims.** Using b1–b3, kext and both septa as six independent knobs assumes six independently
   powered circuits or trim coils. Main transfer-line bends are often powered in series, and b1/b3 are identical
   magnets. State the assumption; if b1–b3 share a supply, repeat the correction with four knobs.
3. **Vertical exit error.** The vertical plane is not corrected, and the text says only that the orbit "stays far
   inside the vertical restrictions". The companion NKM study, however, identifies the static vertical injection
   error left by transfer-line errors as a capture loss. Section 4.4 defers its correction to a future study. The
   vertical exit centroid (rms position and angle over realizations) is the number the injection calculation needs
   from this paper, so report it in Table 6.

Wording:
- "the exit position spread falls to 684 µm and the angle spread to 367 µrad" — the angle spread does not fall; it
  is 364 µrad uncorrected (Table 6).
- "Steered static errors add a small residual" (Section 3.2) contradicts Table 7. The error-free shot-averaged
  losses are 1.28 % and 0.27 %, while the tracked losses on steered realizations are 2.30 % and 0.69 %. The static
  residual therefore roughly doubles the loss. This matters for M1: at a realistic jitter level the residual may
  dominate.
- "The matched reference and low-beta settings are indistinguishable in every column" (Section 4.2). Table 6 gives
  1.68 % against 1.47 % with no interval. Either give the paired interval or say "not resolved".

### M4. The reachable phase-advance interval and the loss-based setting rest on sampling and a non-converged optimizer

The paper's design result is that loss decreases monotonically toward the lower edge of the reachable μ_x interval,
and that the loss-based setting sits at that edge (200.2°). The evidence is as follows:
- **The interval is sampled, not derived.** It comes from 360 random starts.
- **The optimizer did not converge.** All three SLSQP starts reach the 200-iteration limit, and only one is
  feasible.
- **The constraint is not identified.** The paper does not say which constraint fixes the edge: a strength bound,
  the 60 m peak-beta ceiling, or the exit dispersion equalities.
- **The same pattern recurs.** The dispersion-free optimum (187.7°) is also at the lower edge of its interval.

If the edge is set by an engineering bound, the "best setting" is a property of that bound. The design conclusion
would then be "relax this bound to reach lower loss", which is more useful than an iteration-limited point.

**Requested.**
- Replace the random-start pool and the free SLSQP search by a constrained scan: add μ_x as a seventh equality and
  minimise peak beta at each μ_x. For each μ_x, report:
  - feasibility;
  - the active bound at the interval edges;
  - the predicted loss;
  - the exit angle jitter.
- This gives the loss-versus-angle-jitter trade curve directly, for both exit targets. It also removes the need to
  describe a non-converged optimum, and it is a figure a designer can use.
- Keep the fresh tracked test for the chosen point.

### M5. The blade distance is a second decisive input and is not swept

The blade distance d_b = 1.478 mm is taken from the companion geometry, which chose it as 3σ_x + 1 mm. Loss at the
blade depends exponentially on d_b divided by the summed jitter and beam size. The 1 mm thin septum of the KLS
TDR, now cited, would change d_b. The protocol exports blade-variant clearances (0.17/1.17/2.17 mm), but the article
does not use them. The response states that "the blade distance sets it" without showing a result.

**Requested.**
- Plot the predicted loss against d_b for the three settings, at the present and a realistic jitter level.
- State the d_b at which the blade loss falls below a stated tolerance, for example 0.1 %.
- Note that a larger d_b moves the injected beam further from the stored beam, which costs ring acceptance. This
  trade belongs to the companion paper, but it should be stated here.

## Minor comments

1. **Title.** The studied line is "a different design version" from the TDR BTS, with three bends and nine
   quadrupoles against two and eight. The title should not suggest that the paper studies the KLS BTS line as
   designed. Something like *Optical matching and beam loss in a booster-to-storage-ring transfer line for
   nonlinear-kicker injection at the Korea Light Source* would be accurate. "Booster-to-Storage" also lacks "Ring".
2. **Length and housekeeping.** At 15 pages and 8 tables the article is long for its result. Section 3.4 and
   Tables 3–4 should go to the supplement, with a one-sentence summary and the maximum discrepancies kept in the
   text. Section 3.4 contains the four-station campaign accuracy audit, the subdivision convergence and the old
   affine-map shift. The final sentence of Section 2.2 (historical optics-only ensembles) belongs there too.
3. **Equation (5).** It applies to "a single symmetric active station", but the active restriction is one-sided.
   Either give the one-sided form (the first term only, with the sign fixed) or drop the equation; Eqs. (6)–(7)
   carry the argument.
4. **Dispersion-free exit.** The 65-fold gain is analytic and extrapolated to loss fractions of 4 × 10⁻⁵, where the
   Gaussian tail is least trustworthy. Track at least the best dispersion-free point on the fresh realizations, as
   for the configured target. Alternatively, state the gain only to the order of magnitude, and say that
   non-Gaussian booster tails would dominate at that level. Since the ring dispersion at injection is about 0.3 mm,
   the dispersion-free exit is arguably the natural target. The text should say why the line inherits 80.9 mm /
   47.5 mrad from the companion configuration.
5. **"Within 1 %".** Section 4.3 and the Discussion say "within 1 % of its prediction", but losses are themselves
   in percent. Write "within 1 % relative".
6. **Gaussian validation.** Agreement between Gaussian tracking and a Gaussian formula is a check of numerical
   consistency, not of the loss physics. Say so in one sentence, and note that real booster tails would raise the
   blade loss at large d_b/σ.
7. **Table 8.** All three roll levels give identical rows. Collapse the table to the energy-jitter rows and state the
   roll result in the text. Add the betatron-jitter rows of M1.
8. **Supplement nomenclature.** The supplement still uses "machines" and "Original", while the article now uses
   "error realizations" and "baseline"/"matched reference". Align them.
9. **Declarations.**
   - Funding and Acknowledgments repeat the same sentence. Thank people or facilities in the Acknowledgments, or
     leave them out.
   - "Final approval is pending" must not remain in a submitted manuscript.
   - The data-availability statement has been removed. NIM A and most journals require one at submission. Restore
     a one-line statement ("available from the author on reasonable request", or a deposit), as the author decides.
10. **Introduction.** The sentence "This is a closely related transfer-line application; the link … is therefore
    directly relevant" is redundant after the preceding sentence. The last Introduction paragraphs also repeat the
    outline. Shorten both.
11. **Section 4.1.** "0.648 mm at the entrance and 0.683 mm at the exit": say "septum entrance" and "line end (m4)".
    "Entrance" elsewhere means m1.
12. **Statistics.** Give the clustering method for the "pointwise 95 % interval clustered by error realization" once
    in Section 3 (for example, paired cluster bootstrap with the number of resamples).

## Questions to the author

1. Where do the baseline `BTSConfig` quadrupole strengths come from, and for which exit target were they designed?
2. Is there any specification or measurement of booster extraction stability (kicker and septum ripple, orbit
   jitter) for the KLS booster?
3. Which constraint is active at μ_x = 200.2° and at 187.7°?
4. Are b1–b3 on a common power supply in the design version studied?
5. Which beam-position monitors or screens does the design version provide?

## Revision tasks

The ordered task register is [reviewer2_bts_20261030_main_round3_revision_tasks.md](reviewer2_bts_20261030_main_round3_revision_tasks.md).

## Assessment

The phase-advance view of matched-end jitter transfer and the validated loss observable are publishable and useful
beyond this line. What prevents acceptance is that the quantitative conclusions are evaluated at a jitter level that
is not justified and is probably several times too large, together with a headline that presents matching an
unmatched setting as a result. Once tasks R2C-01 to R2C-04 are done, I expect to recommend acceptance subject to
editorial changes.

## Confidential comments to the editor

The author has responded thoroughly to three demanding rounds. The model is now physically meaningful, and the
central mechanism is correct and well validated.

My remaining concern is the input jitter. With 0.5 mm / 0.2 mrad at the booster, the shot centroid moves about five
beam sizes in normalised phase space. That level, not the optics, generates the percent-level losses the paper
optimises. I checked this from Table 1, Section 2.2 and Table 7 of the manuscript.

The analytic loss model makes the requested sweep inexpensive. The outcome may change the emphasis of the paper
but should not prevent publication.
