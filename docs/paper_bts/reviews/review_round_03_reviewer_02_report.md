# Reviewer 2 — BTS main-branch manuscript, round 4

**Manuscript:** *Optical matching and beam loss in a booster-to-storage-ring transfer line for nonlinear-kicker
injection at the Korea Light Source* (C. S. Park).
**Version reviewed:** `docs/paper_bts/paper.tex`, `paper.pdf` (19 pages), `supplement.tex` and `supplement.pdf`
(9 pages) on `main` at `6a968f8`. SHA-256 prefixes:

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `45edf6a9b7a544ef` |
| `paper.pdf` | `4e5a4cf8d6af2197` |
| `supplement.tex` | `4d4a29c9f80effcc` |
| `supplement.pdf` | `2fea85ad8f1bc3da` |
| `paper.bib` | `0a2210e5b160b3ab` |

**Read first:** all main-branch author responses:
- [Reviewer 1, round 1](review_round_01_author_response_to_reviewer_01.md);
- [Reviewer 1, round 2](review_round_02_author_response_to_reviewer_01.md);
- [Reviewer 2, round 2](review_round_02_author_response_to_reviewer_02.md);
- the [joint round-4 response](review_round_03_author_response_to_reviewers_01_02.md).

Also read: my reports of [2026-10-15](review_round_01_reviewer_02_report_and_tasks.md) and
[2026-10-30](review_round_02_reviewer_02_report.md), the
[Reviewer 1 round-3 report](review_round_03_reviewer_01_report.md), the
[consolidated register](revision_round_03_plan_for_review_round_03.md), the round-4 protocol and reproduction guide, and
the round-4 stage outputs.

**Date:** 2026-10-31. Internal pre-submission assessment, not a journal decision.
**Reviewer expertise:** transfer-line optics and matching, injection into low-emittance storage rings, aperture and
error modelling.

## Recommendation

**Major revision of limited scope. The present version is not acceptable, but I expect to recommend acceptance once
items R2D-01 to R2D-03 are done.**

The round-4 revision is thorough and honest. It answers my round-3 objections:
- the jitter is stated in beam-size units and swept;
- the baseline is demoted to a starting point;
- the phase-advance edges are searched explicitly;
- the blade distance is swept.

The revision also corrected two statements of its own on the basis of new evidence, which reflects well on the work.

One problem remains, and the revision itself created it. The new abstract and Discussion conclude that, at realistic
booster jitter, "the design output of the line is the position–angle partition delivered to the injection kicker".
The paper's own round-4 data contradict this. At realistic jitter the beam delivered to the kicker is dominated by
the static steering residual and the uncorrected vertical trajectory, not by how the jitter is partitioned (M1).
The fix uses data already computed. It changes the paper's final message, so I want to see the revised text.

## Status of my round-3 requests

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2C-01 jitter level | Resolved | Beam-size units, a stress-level label and the sweep (Table 9) are what I asked for. The jitter-integrated loss is a good observable. The source of the jitter level remains open, as an author input. |
| R2C-02 baseline framing | Resolved, with a remnant | The abstract and first Discussion paragraph are fixed, and the provenance is stated. Section 4.1 still ends with "optimization of the baseline BTS line improves nominal delivery" (minor 2). |
| R2C-03 constrained scan | Resolved | The edge searches, the μ_x-only dependence of the loss (Fig. 5) and the converged edge are convincing. The physical reason for the lower edge is missing (M3). |
| R2C-04 blade distance | Resolved | Fig. 6 is clear. |
| R2C-05 steering | Largely resolved | The assumptions are stated, the layouts are tested and the vertical centroid is reported. The per-setting reading errors are now shown to matter (M2). |
| R2C-06 dispersion-free | Resolved | Tracked, with an appropriate caveat. |
| R2C-07 length | Not resolved | 15 → 19 pages. Three generations of results now coexist (M4). |
| R2C-08 to R2C-10 | Resolved | Remaining declaration items are author decisions (minor 9). |

Reviewer 1's R3-BTS tasks appear to be resolved: the theorem scope, exact round-aperture bounds, discrete check
points, the mean-clearance argument and the sampled-search wording. I leave their assessment to Reviewer 1.

## Major comments

### M1. At realistic jitter the static residuals, not the jitter partition, dominate the delivered beam

The round-4 jitter stage (`jitter_b/jitter.json`) reports the rms exit centroid of the steered realizations. Next to
it are the exit jitter of the error-free line and the uncorrected vertical centroid:

| Jitter scale | Steered x_rms [mm] | Steered x′_rms [mrad] | Jitter alone σ_x,j / σ_x′,j [mm / mrad] | y_rms / y′_rms [mm / mrad] |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.096 | 0.176 | 0.081 / 0.047 (momentum only) | 1.07 / 0.096 |
| 0.1 | 0.113 | 0.179 | 0.103 / 0.057 | 1.07 / 0.096 |
| 0.2 | 0.156 | 0.187 | 0.151 / 0.080 | 1.07 / 0.096 |
| 1 | 0.639 | 0.366 | 0.643 / 0.327 | 1.07 / 0.096 |

All values are for the matched reference; the loss-based setting is similar.

At the realistic levels the paper itself identifies (×0.1–0.2, i.e. 13–44 % of the beam size):
- **Horizontal angle.** The exit-angle error is about 0.18 mrad. That is the static steering residual: it barely
  changes between scale 0 and 0.2, and it is two to three times the angle jitter. Any choice of μ_x moves only the
  jitter part, 0.06–0.08 mrad.
- **Vertical.** The exit offset is about 1.1 mm and 0.1 mrad, uncorrected. It is independent of the jitter and of
  μ_x, and an order of magnitude larger than the realistic horizontal position jitter.
- **Blade loss.** As the paper states, it is negligible for every setting.

So at realistic jitter, neither the blade loss nor the position–angle partition is the operative quantity. The
quantities that act on injection are:
- the horizontal angle residual left by steering, which reads positions only and has 50 µm reading errors;
- the uncorrected vertical trajectory.

Both are set by the error model and the correction scheme, not by the quadrupole setting. The abstract's closing
statement and the Discussion paragraph ending "…bounds what either choice can achieve" are therefore not supported
at the jitter levels the paper calls realistic. The comparison of 0.33–0.39 mrad with the 0.44 mrad NKM acceptance
in the Discussion holds only at the stress level, and should say so.

This does not invalidate the paper; it sharpens it. The honest conclusion is regime-dependent:
- **Large booster jitter** (the stress level): the jitter partition and the blade loss matter. The phase advance is
  the design knob, and the loss-based setting gains 3–10-fold.
- **Realistic booster jitter:**
  - the blade loss is negligible;
  - the delivered beam error is set by the static steering residual (about 0.18 mrad horizontally) and the
    uncorrected vertical trajectory (about 1.1 mm);
  - the optics choice is then free with respect to loss, and the transfer-line priority is correction and
    instrumentation, especially vertical.

**Requested.**
- Add the static-residual columns (jitter scale 0) to Table 9, or to a short companion table, with the exit
  centroid by plane.
- Rewrite the closing sentences of the abstract and the corresponding Discussion paragraph in the two-regime form
  above.
- Qualify the 0.44 mrad comparison as stress-level only.
- State in Section 4.2 that the steering reads positions only, so the exit angle is only indirectly constrained.
  Consider reporting the angle residual for a layout that weights the two exit-adjacent readings for angle; the
  septum entrance and the line end are 1 m apart.

### M2. Reading errors belong to the monitors, not to the setting

The round-4 test shows that two optically identical settings, the round-3 loss-based setting and the converged edge,
lose 0.085 % and 0.13 % when tracked. The paper attributes this, correctly, to reading errors drawn separately for
each setting, together with shot sampling.

Physically, a reading error is a property of the instrument on a given machine: a monitor offset or a calibration
residual. Two quadrupole settings tried on the same installed line see the same monitor offsets. Drawing them per
setting adds a noise source that does not exist in the comparison the paper wants to make. In this test it moved
the tracked loss by 50 % between identical optics.

Reviewer 1 called a common-noise rerun optional unless it was material. It is now material: it changes the
paired-difference intervals that the abstract quotes.

**Requested.**
- Draw the reading errors per realization and monitor, shared by all settings.
- Rerun the second fresh test and the steering-layout stage. Both are cheap (about 2 minutes each).
- Report the paired differences from this rerun. The optically identical pair should then give identical results;
  that is a useful regression test.

### M3. The headline statistic should be the jitter-integrated loss, with tracking as validation

Different populations and estimators give different gains of the loss-based setting over the matched reference:

| Population and estimator | Gain |
| :--- | ---: |
| Round-3 test, tracked | 3.3 |
| Sensitivity population, sampled prediction | 5.6 |
| Jitter population, jitter-integrated | 4.7 |
| Round-4 test, tracked (edge) | 7.5 |
| Round-4 test, tracked (round-3 setting) | 11 |

The abstract and Discussion compress these into "a factor of 3 to more than 10". The paper has shown that most of
this spread comes from sampling the jitter tail with 600 shots, and that the jitter-integrated loss removes it. The
estimand should follow:
- **Primary result.** The jitter-integrated loss averaged over steered realizations, with a realization-cluster
  interval. It is available for every population, including the tracked tests, where Table 7 already lists it
  ("Integr.").
- **Tracked losses.** These validate the per-shot model (agreement within 1 % relative per row) and illustrate the
  tail. They are not the estimate.

With this, the abstract can give one number with its interval, for example 4.6–4.7 across the populations where
the integrated loss exists. "3 to more than 10" can go.

### M4. Explain the lower phase-advance edge physically, and consolidate the results

**Lower edge.** The lower edge of the configured matched range (200.17°) is the paper's central design boundary,
yet the text says only that it is "set by the matching conditions themselves". The dispersion-free target extends
the range down to about 187°. That strongly suggests the exit dispersion conditions (D = 80.9 mm,
D′ = 47.5 mrad), together with the fixed bend angles, constrain the horizontal phase between the bends. A short
argument would turn an empirical edge into an understood one: the dispersion-closure condition expressed in terms of
μ_x, or a scan of the edge against D′ at m4. The paper already argues that the configured exit dispersion is
inherited and not derived from the ring. If that dispersion is what sets the loss-limiting edge, it is the paper's
most important design statement and deserves to be explicit.

**Consolidation.** The article now carries three generations of results:
- the round-3 test (Table 6);
- the round-4 test (Table 7), which supersedes it;
- the round-3 sensitivity table with its sampled predictions (Table 8), which Section 4.5 itself shows to be
  unreliable for small losses.

Fig. 4 (right) duplicates Fig. 5 and still uses the round-3 labels "reachable" and "Refined low beta". These
contradict the sampled-search wording and the setting names elsewhere.

I recommend:
- one test table (Table 7, recomputed under M2), with Table 6 moved to the supplement;
- Fig. 4 reduced to its left panel, with Fig. 5 carrying the solutions;
- Table 8 replaced by its jitter-integrated equivalent, or merged into Table 9;
- the duplicate wording of Sections 4.2–4.3 removed.

A JKPS or NIM A referee will expect about 12 pages for this content.

## Minor comments

1. **Abstract.** After M1 and M3 the abstract should contain:
   - one gain with its interval;
   - the two-regime conclusion;
   - the static residuals at realistic jitter.

   "Best-found setting" is fine.
2. **Section 4.1, last paragraph.** "Thus optimization of the baseline BTS line improves nominal delivery" repeats
   the framing the Discussion now rejects. Delete it, or say "matching is required for nominal delivery".
3. **Minus signs.** Intervals use hyphens: "-0.84 [-1.39, -0.40]". Use siunitx or a math minus throughout, in the
   text, Table 7 and the macros.
4. **Table 9.** The number format is mixed ("1.3", "2.8 × 10⁻¹"). Use one format per column; percent with two
   decimals above 0.01 % is fine.
5. **Table 7, dispersion-free row.** "8.3 × 10⁻⁵ %" is one particle. Write "1 particle (8 × 10⁻⁷)", or give the
   one-sided 95 % upper bound.
6. **Section 4.4.** "394 µrad against 327 µrad" uses the round-3 dispersion-free point, while Table 7 and the
   preceding paragraph use the scan point (393 µrad). Use one.
7. **Section 2.4.** "Booster extraction stability is commonly specified as a fraction of the beam size" needs a
   citation, for example a booster or extraction-kicker stability specification from a comparable facility.
8. **References.** [13] is a conference abstract and [5] is in preparation. Both are acceptable for an internal
   draft, but journals will ask for the companion manuscript to be available to referees. [13] should be updated if
   a full IPAC'26 paper appears.
9. **Declarations.**
   - The data-availability statement is still absent, and both candidate journals require one.
   - "Final approval is pending" must not appear in a submitted version.
   - The target journal should be decided before reformatting, since NIM A and JKPS differ in format.
10. **Supplement.** Its introduction is now clear. Section 3 still describes the "earlier four-station campaign"
    accuracy audit at length; one table would suffice.

## Questions to the author

1. What is the horizontal exit-angle residual if the steering weights the septum entrance and line end readings to
   control angle explicitly?
2. Does the lower μ_x edge move with the D′ target at m4, and is the configured D′ the binding condition?
3. Are vertical trims of existing elements plausible in the studied design version, for example a vertical trim
   winding on the septa or quadrupole movers? If not, the 1.1 mm uncorrected vertical offset is a design limitation
   of this line, and the paper should state it as a finding.

## Revision tasks

The checkbox register is
[review_round_03_reviewer_02_tasks.md](review_round_03_reviewer_02_tasks.md).

## Assessment

This is now a careful, well-validated parametric study, and its central mechanism is correct and useful:
- matched ends fix the nominal clearance;
- the loss depends on the phase advance alone;
- the loss is set by the jitter at the one-sided blade.

What remains is to draw the right conclusion from the paper's own regime analysis (M1), to use the estimator the
paper has shown to be the right one (M3), to remove an artificial noise source from the comparisons (M2), and to
consolidate (M4). Only M2 needs new computation, a few minutes of reruns. After these I expect to recommend
acceptance.

## Confidential comments to the editor

Over four rounds the author has responded to every point, including several where the evidence went against the
earlier text. The new regime analysis is the most valuable addition. Taken to its conclusion, it shows that the
optics-based loss reduction matters only for large booster jitter. At realistic jitter, correction and
instrumentation, especially vertical, are the transfer-line priorities.

I verified this from the round-4 stage outputs: the static exit residual barely changes between jitter scales 0 and
0.2. The revision required is interpretive, plus one inexpensive rerun.
