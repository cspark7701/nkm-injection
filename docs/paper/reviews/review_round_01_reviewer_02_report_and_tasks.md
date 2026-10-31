# Referee report — Reviewer 2

**Manuscript:** "Capture window and robustness of nonlinear-kicker injection into a 4 GeV storage ring with a small
dynamic aperture" (C. S. Park). Prepared in JINST format. **The target journal is not yet decided**, so this report
judges the science independently of venue and adds venue-specific guidance (see "Choice of journal").
**Version reviewed:** `docs/paper/paper.tex` / `paper.pdf` at commit `acd891c` (10 pages, 7 figures, 10 references).
**Date:** 2026-10-10.
**Reviewer expertise:** storage-ring beam dynamics, off-axis and multipole-kicker injection, transfer-line design,
pulsed-magnet modelling.

## Recommendation

**Major revision** at any regular peer-reviewed accelerator or instrumentation journal. I do not recommend acceptance
in the present form, and I do not recommend rejection. How heavily each comment weighs depends on the venue; the section
"Choice of journal" explains this.

The study is careful in the parts it controls. It uses native nonlinear tracking, couples the transfer line to the
ring, compares the kicker against paired calibrated controls on identical particles, gives honest intervals, and is
unusually transparent about its own corrections. The question is relevant to fourth-generation rings. However, the
central quantitative results rest on a kicker model that the manuscript itself shows to be inadequate (section 5.2),
on an ideal ring, and on an assumed error budget whose dominant term is not justified. In its current form the paper
is a well-executed design note for one unnamed lattice, not yet a general research result. The revisions below are
needed for the conclusions to be reliable and useful to other laboratories.

## Summary of the manuscript

The author models a four-wire NKM with a RADIA kick map, tracks a booster bunch through a matched BTS line to a septum
2.26 m upstream of the kicker, applies a thin kick, and tracks for 500 turns in a 4 GeV lattice whose on-momentum DA at
the kicker is −12 to +13 mm. The main results are:

- **Operating point:** 91.1 % capture at x_inj = −20 mm, S = 0.85, against 94.6 % for an equally strong uniform kick.
- **Window:** an angular window of about ±0.5 mrad.
- **Stored-beam transparency:** 5×10⁻⁶ σ for an aligned kicker, rising to 0.10 σ at a 0.2 mm offset.
- **Combined errors:** mean capture of 37.8 % (thin kick) or 47.4 % (thick magnet), limited by booster extraction jitter.
- **Linear one-turn maps** are shown to overestimate capture.

## Assessment against general journal criteria

| Criterion | Assessment |
| :--- | :--- |
| Originality | Moderate. The mechanism (kick nonlinearity across the bunch) is known [Liu 2016]; the new elements are the coupled BTS–ring robustness analysis and the alignment–transparency relation for a cubic field. |
| Technical soundness | Good numerics. Physics model incomplete at the points that matter most (kicker model, ring errors, pulse). |
| Reproducibility | Excellent: hashed artifacts, public code, generated numbers. |
| Presentation | Clear but dense. Several figures and passages need work (see minor comments). |
| Conclusions supported? | Partly. The ranking of error sources is supported. The absolute capture values and the ±0.5 mrad window are not yet. |

## Major comments

**M1. The kicker model is internally inconsistent, and the headline numbers use the weaker model.**
Section 4 states that the thick magnet lowers nominal capture "because the trajectory inside the magnet samples a
steeper part of the kick profile". Section 5.2 then shows that the same model *raises* capture under errors by 9.5
points, and calls the mechanism "plausible". The operating-window map (figure 4), the paired-control comparison
(figure 5) and the conclusions are all computed with the thin kick, which the paper itself says "misrepresents the
sensitivity". The injected beam crosses about 2.6 mm of a strongly nonlinear profile inside a 0.525 m magnet, so a
thin kick evaluated along straight lines is not a controlled approximation here. The thick model is itself
simplified: B_y(x) is taken uniform over the length, with no fringe field and no y dependence. The required revisions
are:

- (a) Track through the 3-D RADIA field (sliced, or as a 3-D field map) or use an angle-dependent kick map, and
  validate this against the straight-line integrals.
- (b) Repeat the operating-window scan and the paired controls with the validated model.
- (c) Replace the "plausible reason" with a demonstrated mechanism, for example a figure of exit angle and amplitude
  against entry x and x′ for the thin and thick models.

**M2. The ring is ideal, so the capture values are upper bounds of unknown size.**
The lattice has no magnet errors, misalignments, coupling, insertion devices or physical apertures. For a 4GSR-type
lattice, error-seeded and orbit-corrected DA is commonly 20–40 % smaller than the bare-lattice DA. The selected point
sits 3 mm inside the bare DA edge, so it is exactly where this reduction matters. The ±12 × ±6 mm aperture check
(section 3) was made only at a provisional point. The author should:

- evaluate capture at the operating point on at least 10 error-seeded, orbit- and optics-corrected ring models with
  the real chamber profile;
- report the distribution of capture over ring seeds;
- state clearly that the error ensembles of section 5.2 do not include ring errors.

**M3. The tracking duration is short relative to the longitudinal and damping time scales.**
500 turns is about 1.7 synchrotron periods and 0.13 horizontal damping times. Turn convergence (0.44 → 0.43 at 2000
turns) was shown only at the provisional point, with no ring errors. Injected particles with large amplitude and
large δ can be lost late, through synchrotron-betatron coupling and resonance crossing. The author should:

- show loss-turn histograms at the operating point;
- extend at least one reference case to one damping time (≈ 4000 turns) or to equilibrium;
- justify "capture = survival over 500 turns" quantitatively.

**M4. The dominant error term is assumed, not justified, and the result is given at one amplitude only.**
The main conclusion — that capture is jitter-limited — depends on a booster extraction jitter of 0.5 mm / 0.2 mrad,
which the BTS turns into 0.63 mm / 0.32 mrad at the septum. These values need a source: booster design, kicker
flat-top stability, or measured data from comparable boosters. They look large for a modern full-energy booster. More
importantly, a single error amplitude gives no design guidance. The most useful result this paper could offer is a
**tolerance curve**: capture (mean and 10th percentile) against septum orbit jitter, and against NKM-to-orbit offset,
from which the jitter required for e.g. 80 % mean capture can be read. The same applies to the injected emittance.
100 nm rad horizontal should be justified, and the sensitivity to it shown, because Liu et al. identify beam size as
the second key factor.

**M5. The pulsed-magnet aspects that decide transparency in practice are absent.**
The NKM is modelled as an ideal single-turn magnetostatic kick. At any venue, the following must at least be discussed
with order-of-magnitude estimates; for an instrumentation journal they should be modelled:

- the pulse length and shape relative to the 2.67 µs revolution period;
- residual field on the following turns;
- the different field seen by stored bunches along the train;
- eddy currents and field distortion from the coated ceramic chamber;
- timing jitter.

The transparency figure of 5×10⁻⁶ σ applies only to the aligned, static, ideal case. In practice the residual
oscillation of the stored beam will be set by these effects and by kicker-to-orbit alignment. The paper shows the
alignment effect but none of the others.

**M6. The near-axis transparency rests on interpolation below the grid resolution.**
The stored beam (σ_x = 32 µm) samples the kick map between the nodes at 0 and ±0.5 mm, where the kick is cubic and
about 10⁻⁹ rad. A bicubic spline through 0.5 mm nodes cannot resolve this reliably; the paper itself notes that
bilinear interpolation gives a different answer. The near-axis kick should be taken from a fit to the multipole
expansion, from the analytic four-wire model, or from RADIA evaluated on a fine grid near the axis, with the
truncation error stated. Two further omissions:

- **Vertical transparency:** the kick map has a vertical component, and β_y = 5.6 m at the kicker.
- **Tracked residual oscillation:** the tracked multi-turn residual oscillation and emittance growth of the stored
  beam (not the first-turn linear estimate) should be reported.

**M7. The definition and resolution of the window need work.**
The "angular window of about ±0.5 mrad" rests on three angle settings (−0.5, 0, +0.5 mrad), and the capture is
asymmetric (15–85 % against 13–64 %). The (x_inj, S) grid steps are coarse: 0.5–1 mm in x_inj and 0.05 in S. The
operating point is chosen as the maximum Wilson lower bound over 120 points, which has selection bias; the replicate
run mitigates this but does not remove it. Please:

- (a) Present the standard injection diagram: the ring acceptance after the NKM, mapped back to septum phase space
  (x, x′), with the injected-beam ellipse and the septum blade. This is the clearest way to show the window and its
  asymmetry.
- (b) Define the window quantitatively, e.g. the full width at 80 % of maximum capture, with a fine angle scan.
- (c) State whether the angle-matched condition (zero exit angle) is actually capture-optimal. Section 5.2 suggests
  it is not.

**M8. The positioning against prior work is too thin for a regular paper.**
Ten references, of which four are statistical or software citations, do not establish the state of the art. Please
add:

- a comparison table of operating NLK/MIK systems (BESSY II, MAX IV, SOLEIL, Sirius and others): field, kick, aperture
  and reported injection efficiency;
- the four-wire NLK design references;
- kick-map formalism references (Elleaume);
- recent fourth-generation injection studies (on-axis swap-out against off-axis NLK).

The facility and lattice should be named, or the reason for anonymity stated, and the ring parameters compared with
other 4 GeV rings. The claim that linear one-turn maps overestimate capture is expected for a DA-limited problem; it
should be framed as a validation step, not as a conclusion.

## Minor comments

**m1. Parameter tables are missing.** Add tables for the ring, booster beam, BTS, NKM (wire positions, current, pulse,
field at the extremum) and the full error budget (σ, distribution, truncation, applied where). These are currently
spread across the text.

**m2. Kicker geometry.** Add a figure of the NKM cross-section and of B_y(x, y). The kick map is described only by its
grid.

**m3. Chromatic scaling.** The thin kick is not scaled by 1/(1+δ). With σ_δ = 1.1×10⁻³ the effect is small, but it
should be included or stated.

**m4. Validation point (section 3).** The validation uses a "provisional point" (x′ = 5.75 mrad, S = 1) that differs from
the operating point. Repeat the backend comparison, turn and particle convergence, and the aperture check at the
operating point, or explain why the provisional point is representative.

**m5. Transfer-line tolerances (section 5.1).** This analysis is statistically thorough, but a median mismatch of
2×10⁻³ has no effect on capture. The 550,000 samples and the prefix-stability target are disproportionate to its
physical relevance. Condense it to one paragraph, and move the β-limit failure statistics to a supplement. Fix the
grammar of "Only 5 of the 550 000 realizations exceeds".

**m6. Control statistics.** The dipole control has 50 realizations (seed 42); the NKM has 150. Run the dipole control on
all three seeds, or state the asymmetry in the figure 7 legend and the text.

**m7. Figure 2.** The legend reads "required kick −x in" (missing prime/subscript). The DA band and the curves overlap;
consider a lighter band.

**m8. Figure 5 (right).** Mixed number formats ("5e-6", "2971"). Use LaTeX-style labels and state the reference
(first-turn linear estimate).

**m9. Figure 7 (left).** Five ECDFs, three of them in the same colour, are hard to read in print. Consider two panels:
thin-kick diagnostics, and thin vs thick vs dipole.

**m10. Abstract.** It contains about 15 numbers. Keep the four that carry the conclusions and remove the
thick/thin parenthesis once M1 is resolved.

**m11. Notation.** Define M_x on first use (section 2.3 uses it, section 5.1 defines it). Define "capture" before
section 2.3. Use one notation (σ or "rms sizes") throughout.

**m12. Format.** The manuscript uses the JINST class with the `unsrt` bibliography style. Once the journal is chosen,
convert to that journal's template and reference style. JINST requires JHEP.bst. Other candidate journals have their own
templates and bibliography styles, and some require a word or page limit, a graphical abstract or highlights. Check
the current author instructions.

**m13. Data availability.** The availability statement points to a manuscript directory path. Provide a DOI (Zenodo) at
submission rather than at acceptance; many referees will want to inspect the code.

**m14. Spearman ranking.** The candidate predictors are correlated: booster jitter drives the septum error. Present
partial correlations or a simple regression, or restrict the claim to "strongest marginal association".

## Questions to the author

1. What is the NKM pulse length, and does the stored beam see the field on the turn after injection?
2. Is the matched centroid at the NKM (−9 mm) inside the physical chamber, and what is the stay-clear?
3. Does the 9 % loss at the operating point come from the horizontal tails, the energy tails or the septum? A
   loss-cause breakdown would help.
4. Was the sextupole configuration optimised for DA at the injection point, or is it the bare design?

## Revision tasks (for the author)

Priority: **A** = required for acceptance, **B** = strongly recommended, **C** = editorial. "Sim" = new simulation
required.

| ID | Priority | Task | Sim | Acceptance criterion | Est. effort |
| :--- | :---: | :--- | :---: | :--- | :--- |
| R2-1 | A | Validate the NKM model: track through the 3-D RADIA field (or an angle-dependent kick map); compare with thin and current thick models; show the mechanism figure (exit x′/amplitude vs entry x, x′). | yes | Model choice justified with a quantitative comparison; "plausible reason" replaced by a demonstrated effect | 3–5 d |
| R2-2 | A | Repeat the operating-window scan (figure 4), paired controls (figure 5) and the combined-error ensemble with the validated model; make it the headline model. | yes | Abstract, figures 4–7 and conclusions use one validated model | 1–2 d compute |
| R2-3 | A | Ring with errors: ≥ 10 error seeds, corrected orbit/optics, real chamber apertures; capture at the operating point per seed. | yes | Distribution of capture over ring seeds reported; DA reduction quantified | 3–5 d |
| R2-4 | A | Tracking duration: loss-turn histograms; one reference case to ≥ 1 damping time (~4000 turns). | yes | Loss saturation shown, or the capture definition revised | 1 d |
| R2-5 | A | Tolerance curves: capture (mean, p10) vs septum orbit jitter (0–0.6 mm / 0–0.3 mrad), vs NKM–orbit offset, vs injected emittance; required tolerances stated. | yes | Figure with tolerance curves; jitter requirement for 80 % capture quoted | 1–2 d compute |
| R2-6 | A | Justify the booster jitter, emittance and energy spread with sources; full error-budget table. | no | Table with a source for each σ | 0.5 d |
| R2-7 | A | Pulsed-magnet section: pulse length vs revolution period, after-turn residual field, train uniformity, chamber eddy currents, timing jitter; estimates or simulation. | partly | Section with quantified estimates for each effect | 2–3 d |
| R2-8 | A | Near-axis transparency from a multipole fit, the analytic 4-wire model or a fine RADIA grid; vertical transparency; tracked multi-turn stored-beam residual oscillation. | yes | Near-axis kick with stated truncation error; vertical result; tracked residual amplitude | 1–2 d |
| R2-9 | A | Septum phase-space acceptance diagram with beam ellipse and blade; fine angle scan; quantitative window definition; test whether zero exit angle is optimal. | yes | New figure; window defined (e.g. 80 % width) with resolution ≤ 0.1 mrad | 1–2 d |
| R2-10 | A | Literature: comparison table of NLK/MIK systems; four-wire NLK, kick-map and 4GSR injection references (each verified). | no | ≥ 20 verified references; comparison table | 1–2 d |
| R2-11 | B | Parameter tables (ring, booster beam, BTS, NKM, errors); NKM geometry and B_y(x, y) figure. | no | Tables 1–3 and new figure | 1 d |
| R2-12 | B | Re-run model validation (backend, turns, particles, chamber aperture) at the operating point. | yes | Section 3 at the operating point | 0.5 d compute |
| R2-13 | B | Dipole control on all three seeds; partial correlations or regression for error drivers. | yes | Balanced controls; driver claim qualified | 0.5 d |
| R2-14 | B | Include the 1/(1+δ) chromatic scaling of the kick; state the effect. | small | Code change and test; effect quantified | 0.5 d |
| R2-15 | B | Name the facility/lattice, or state why it is anonymous; compare with other 4 GeV rings. | no | Text | 0.5 d |
| R2-16 | C | Condense section 5.1; move failure statistics and prefix stability to a supplement; fix grammar. | no | ≤ 1 paragraph in the main text | 0.5 d |
| R2-17 | C | Figure fixes: fig 2 legend, fig 5 number format, fig 7 split into two panels; one σ notation throughout. | no | Figures pass inspection | 0.5 d |
| R2-18 | C | Abstract reduced to the key numbers; define M_x and "capture" on first use. | no | Text | 0.5 d |
| R2-19 | C | Choose the journal (see "Choice of journal"); convert to its template and reference style (JINST: JHEP.bst); Zenodo DOI at submission. | no | Clean build in the target template; DOI in the availability statement | 0.5–1 d |
| R2-20 | B | Reframe the introduction, abstract and conclusions to the emphasis of the chosen journal (beam physics vs instrument/method vs facility design). | no | Framing matches the journal scope statement | 0.5–1 d |

**Suggested order** (choose the journal first, R2-19/R2-20): R2-1 → R2-14 → R2-12 → R2-2 (with R2-9) → R2-3 → R2-4 → R2-5 → R2-8 → R2-7 → R2-13. Then do the
documentation and literature tasks (R2-6, R2-10, R2-11, R2-15) and the editorial tasks (R2-16 to R2-19).

R2-2, R2-3 and R2-5 depend on the model chosen in R2-1. Running them first would repeat the thin/thick reversal found
in milestone 117.

## Choice of journal

The manuscript is in JINST format, but the venue is undecided. Each type of journal reviewing it would weigh the
comments above differently. The author should check every journal's current scope and author instructions; the
priorities below are this reviewer's judgement, not journal policy.

| Venue type (examples) | What referees there will weigh most | Tasks that become decisive | Fit of the current paper |
| :--- | :--- | :--- | :--- |
| Beam-physics journal (e.g. Phys. Rev. Accel. Beams) | New physical insight that generalises beyond one lattice; rigorous models | R2-1 (validated thick/3-D kicker and its mechanism), R2-3 (ring errors), R2-4, R2-5 (general tolerance scaling), R2-10 | Weakest now. Needs the thin-vs-thick mechanism developed into a general result (e.g. scaling with magnet length, kick gradient and injection angle) and comparison with other rings. |
| Instrumentation/methods journal (e.g. JINST, Nucl. Instrum. Methods A) | The device and the method: realistic magnet, pulse, chamber, tolerances usable by designers | R2-1, R2-7 (pulsed-magnet effects), R2-8 (transparency), R2-5 (tolerance curves), R2-11 (geometry and parameter tables) | Good fit once the pulsed-magnet and tolerance results exist; the reproducible workflow is a strength here. |
| Synchrotron-facility journal (e.g. J. Synchrotron Rad.) | Impact on facility operation and users: top-up transparency, injection efficiency | R2-3, R2-7, R2-8, R2-15 (name the facility) | Possible if the paper becomes a design study of a named facility, with transparency for users at the centre. |
| Conference proceedings (e.g. IPAC) | Timely, concise result; light review | none required; condense to 3–4 pages | Fits now as a short report of the operating window and the jitter limit, but publishes only part of the work and may limit later journal novelty. Check the chosen journal's prior-publication policy. |

**Reviewer's suggestion.** Choose between an instrumentation/methods journal and a beam-physics journal before
starting the revision, because the two need different additional work:

- **Instrumentation/methods path:** do R2-1, R2-5, R2-7 and R2-8 first, and keep the existing JINST format if JINST is
  chosen.
- **Beam-physics path:** do R2-1 and R2-3 first, and generalise the thin-versus-thick result.

The tasks marked A in the revision table are needed on either path. Without them, the paper would currently fit only
conference proceedings.

## Confidential comments to the editor

The work is reproducible and honest about its limits, which is to its credit. The present conclusions are sensitive to
the kicker model; section 5.2 of the manuscript demonstrates this itself. The absolute capture values could also
change substantially once ring errors are included. I would be glad to review a revised version. With R2-1 to R2-10
addressed, this could become a useful reference for NKM injection design in small-DA rings, in whichever regular journal
the author chooses.
