# Reviewer 2 — BTS main-branch manuscript

**Manuscript:** *Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line*
(C. S. Park). Prospective journal: Journal of the Korean Physical Society (JKPS), Research Article.
**Version reviewed:** `docs/paper_bts/paper.tex`, `paper.pdf` (12 pages) and `supplement.tex` on `main` at
`82598dc`. SHA-256 prefixes:

| Asset | SHA-256 prefix |
| :--- | :--- |
| `paper.tex` | `e1a449809091c950` |
| `paper.pdf` | `fe35db8574e70120` |
| `supplement.tex` | `bdfef790ff7f9c43` |
| `paper.bib` | `f2bfe5beb59526c8` |

**Read first, as requested:**
- the Reviewer 1 main-branch reports (round 1 and round 2), with their task registers;
- the two point-by-point author responses;
- the historical BTS-branch reports 01–03 and their responses;
- the reviews index;
- the supporting notes `beam_and_boundaries.md`, `article_scope.md` and `round2_task_status.md`.

The historical reports 01–03 assess a different manuscript (*Constrained optical matching, error sensitivity, and
transmission robustness …*). Their acceptance recommendations do not transfer to this version, and I do not rely on
them.

**Date:** 2026-10-15. Internal pre-submission assessment, not a journal decision.
**Reviewer expertise:** transfer-line optics and matching, injection into low-emittance storage rings, aperture and
error modelling.

## Recommendation

**Major revision; I do not recommend acceptance of the present version.** The paper's central physical question is
degenerate in its realistic configuration and is answered only in artificial ones. As now posed it would not
interest a transfer-line designer. I see a clear route to a useful paper (Section "What a publishable version would
show"); it requires reframing, not more statistics.

The two Reviewer 1 rounds have made the numerical work careful:
- independent transport validation;
- interior beta extrema;
- centred linearisation and Gaussian quadrature;
- paired machine-cluster inference;
- honest reporting of an unresolved baseline result.

I accept all of that and do not reopen it. My concerns are with the *physics model of the line*, which neither
earlier round examined.

## Summary of the manuscript

The paper studies whether reducing the vertical peak beta inside a 21.8 m, 4 GeV BTS line increases the minimum
five-sigma projected clearance. The reference, low-beta and directly clearance-optimised settings share the same
boundary match, and clearance is evaluated at four model aperture stations. The findings:
- **Baseline.** The minimum is capped by the entrance station, so no strategy changes it.
- **Hypothetical restrictions.** At a 3 mm horizontal restriction at m2 and a 1.5 mm vertical one at m3, low beta
  hurts horizontally (−0.15 mm) and helps slightly vertically (+0.07 mm); direct clearance optimisation helps in
  both (+0.88 and +0.21 mm).
- **Losses.** Higher mean clearance does not imply fewer particle losses.

## Assessment of the earlier review rounds

| Reviewer 1 round-2 point | Status | My comment |
| :--- | :--- | :--- |
| M1 limiting-station mechanism | Resolved | The station decomposition (all 406 ties entrance-limited) is convincing. The mechanism is even simpler than presented (M1 below). |
| M2 strategy comparison beyond one alternative | Formally resolved | A direct-clearance strategy is added, but only for hypothetical restrictions (M2). |
| M3 clearance accuracy at the claimed scale | Resolved | The −0.155 µm shift and the 0.6 µm quadrature agreement are adequate. |
| M4 interior extrema | Resolved | — |
| M5 inferential target | Resolved | Block-event definition is correct. |
| Declarations | Open | Funding, acknowledgments and final author approval are still pending (minor 6). |

## Major comments

### M1. In the realistic configuration the design question is empty by construction

The four apertures are:
- ±19.35 mm at m1 and m4;
- ±30 mm at m2 and m3.

The quadrupoles, bends, kicker and both septa carry no aperture at all (`beam_and_boundaries.md`, element table).
Both end stations sit where the optics are *fixed by the boundary conditions*: the entrance Twiss and dispersion
are given, and the exit is matched to the target. Their nominal clearances therefore follow from Table 1 alone,
independent of every quadrupole setting. I reproduced all four from the boundary data with σ² = εβ + (Dσ_δ)²:

| Station | x | y |
| :--- | ---: | ---: |
| Entrance (19.35 − 5σ) | 17.455 mm | 18.865 mm |
| Exit (19.35 − 5σ) | 18.555 mm | 19.064 mm |

These are exactly the values of Table 2. The two interior stations have 30 mm half-widths. They could only become
limiting if 5σ exceeded about 12.5 mm, which no matched setting approaches. Hence:
- **The nominal minimum clearance is analytically K-independent for every matched setting.** Section 3.1 and
  Fig. 2 present this as an observed "saturation" with a sufficient condition. It is a one-line consequence of
  placing apertures only at the boundary-defined ends, and should be stated as such.
- **Under errors, the only K-dependent part** of the end-station clearances is the trajectory response at the exit.
  That is the physically interesting quantity, and the paper never isolates it.
- **The mean clearance change of the baseline** (+0.010 mm on 17.455 mm) is a measurement of noise around a
  constant. It does not deserve a headline sentence in the abstract.

This is not a numerical defect. It means the baseline result says nothing about the line's optics, and the paper's
positive results come only from M2's hypothetical stations.

### M2. The hypothetical restrictions are not transfer-line apertures; the real restrictions are missing

The restricted cases are a 3 mm horizontal half-width at a marker before b1 and a 1.5 mm vertical half-width before
b2. No transfer line has such restrictions in a drift ahead of a bend. These are, as the text says, stress cases. But
then every positive conclusion of the paper (Table 3, Fig. 5, Fig. 6, the abstract's "+0.881 and +0.212 mm") is a
property of an invented aperture placement. The direction of the effect also depends on which invented station is
chosen: low beta loses at m2 and gains at m3.

Meanwhile the restrictions that actually limit a BTS line are absent:
1. **Quadrupole bores.** A 19.35 mm bore is assumed and used for the pole-tip check, but it is never applied as an
   aperture along the nine quadrupoles. That is where peak beta and dispersion act.
2. **Dipole vacuum gaps.** b1–b3 bend through up to 176 mrad. Their vertical gap, plus the dispersion and sagitta
   inside them, is the usual vertical limitation of a BTS line, and the "vertical-beta reduction" question is
   precisely about it.
3. **Septum channels.** `sept_in` (0.31–1.31 m) and `sept_ex` (20.79–21.79 m) are 1 m long with no channel aperture.
4. **The injection-septum blade.** This is decisive, and the companion NKM manuscript fixes its geometry:
   - stored-beam edge at −16 mm, 2 mm blade, injected beam at x_inj = −19.48 mm;
   - so the beam passes about 1.48 mm from the blade's outer face, selected as 3σ_x plus 1 mm;
   - with σ_x = 0.159 mm at m4 (reproduced above), the five-sigma clearance to the blade is only about 0.68 mm,
     against the 18.555 mm the BTS model assumes at the same point.

   In the actual injection geometry, the exit septum blade is therefore the active restriction of the line by more
   than an order of magnitude, and it is one-sided.

With the septum blade in place, the paper's question becomes physical and non-trivial. The exit size is fixed by the
match, so the quadrupole settings act only through the *trajectory response* at the blade to the static errors and
the booster jitter. Low beta inside the line changes that response. This is exactly the size-versus-trajectory
competition the paper identifies at m3, but at a restriction that exists.

**Requested.**
- Replace the four-station model by element-wise apertures: quadrupole bores, dipole gaps with the sagitta and
  dispersion inside the bend, septum channels along their length, and the one-sided blade at the exit consistent
  with the companion paper.
- Make clearly labelled parametric sweeps of the dimensions that are not sourced.
- Redo the comparison on this model.
- Retain the m2/m3 cases, if at all, in the supplement as a mechanism illustration.

### M3. No trajectory correction: the "trajectory sensitivity" result is a model artefact of uncorrected steering

The error model has:
- 100 µm quadrupole offsets, 0.5 mrad rolls and 0.05 % dipole errors as static errors;
- 0.5 mm, 0.2 mrad and 0.1 % shot jitter at the entrance;
- "No optical correction or per-shot retuning".

On the held-out machines the mean |x| centroid at m2 is 1.2 mm, much larger than the 0.2–0.45 mm beam sizes. Every
BTS line has correctors and BPMs or screens, and static trajectory errors of this size are corrected in commissioning.
SLS 2.0, which the paper cites [4], is an example of that practice.

The companion NKM study applies at least ideal static steering at the septum. This paper applies none. Two
consequences follow:
1. The cross-paper error models are inconsistent.
2. The paper's mechanism claim ("trajectory sensitivity offsets the size benefit of low beta") may be dominated by an
   uncorrected static orbit that would not exist in operation.

**Requested.** Include static trajectory correction, at minimum position and angle steering at the exit as in the
companion, preferably correctors at the triplets with BPM noise. Keep the shot jitter uncorrected. Show which
conclusions survive. The quantity that matters operationally is the jitter-driven response, which steering cannot
remove.

### M4. Mean minimum clearance is the wrong objective for losses; the paper's own data say so

Table 4, vertical restriction:

| Setting | Mean clearance change | Lost particles | Affected blocks |
| :--- | ---: | ---: | ---: |
| Reference | 0 | 1 | 1 |
| Low beta | +0.07 mm | 43 | 6 |
| Direct clearance | +0.21 mm | 26 | 2 |

The setting with the *lowest* mean clearance loses the fewest particles. The paper reports this ("mean improvement is
not tail reliability") but does not draw the design consequence. The quantity a designer controls against is the
loss tail, which is set by the shot-to-shot *spread* of the centroid relative to the aperture, not by the mean.

**Cheap remedy.** Every shot's centroid and covariance at every aperture are already exported. The expected loss
fraction per shot is then a closed-form Gaussian tail, e.g. ½ erfc(c/(√2 σ)) for a one-sided edge, with the
two-sided and coupled forms as needed. Hence:
- this observable can be computed for all 600 shots per setting without tracking;
- it can be checked against the observed loss counts, which become a validation instead of an anecdote;
- it can serve as the design objective, e.g. a high quantile of the per-shot loss fraction over training machines
  (a chance constraint).

That would turn the paper's negative remark into a positive design result. A nominal-clearance optimisation that
improves the nominal objective under small errors is expected and does not carry the paper.

### M5. The exit target is the paper's most consequential unsourced input, and the companion uses it

Table 1 calls the m4 target unresolved and says "no transport from m4 to a ring matching point is established". Yet:
- The companion NKM paper uses exactly these values as its injected beam (β_x = 2.336 m, D = 80.9 mm,
  D′ = 47.5 mrad).
- It transports that beam from the septum to the kicker.

The two manuscripts must agree on what m4 is.

Physically, the target has consequences the paper does not discuss. At m4:
- the betatron divergence is σ_x′ = 57 µrad;
- the dispersive contribution D′σ_δ adds 50 µrad, for 76 µrad in total;
- the ring dispersion at the injection point is ≈ 0.3 mm, so the 80.9 mm / 47.5 mrad residual is a dispersion
  mismatch that the beam carries into the ring.

The companion paper finds that a 0.44 mrad angular acceptance window limits injection. The BTS exit dispersion and
divergence are therefore the BTS design quantities with the largest downstream leverage, larger than any interior
beta peak.

**Requested.**
- State the source and meaning of the exit target.
- Discuss whether the line can deliver D′ ≈ 0 (and D ≈ 0) at the septum, i.e. a dispersion-matched exit, within the
  quadrupole bounds, and at what cost in peak beta.
- If the article must stop at m4, report at least the exit divergence budget (betatron versus dispersive) as an
  output of the design.

## What a publishable version would show

A concise JKPS article could answer one question a BTS designer actually faces:

> With a matched, steered exit and a one-sided septum blade, which interior optics minimise the jitter-driven loss
> at the blade and the exit angular spread, and what does lowering interior beta cost or gain?

The existing infrastructure covers almost all of it:
- transport validation, covariance and centred maps;
- paired held-out machines;
- the new element-wise apertures, steering and analytic tail loss.

The exit dispersion-matching option (M5) is a natural second design axis. Negative or conditional answers are
acceptable if the restrictions are real or explicitly sourced.

If the author prefers not to reframe, I would recommend presenting the present material as a short conference paper
on the methodology, or merging its validated parts into the companion NKM article. As a standalone research
article, the current framing would not survive a JKPS referee with transfer-line experience.

## Minor comments

1. **Abstract.** It spends half its length on numerical housekeeping: interior sampling, centred transport,
   quadrature, "below one micrometre". After the reframing, state the physical question, the active restriction and
   the design result. Keep the validation in Methods.
2. **Section 3.1.** Replace the "sufficient condition for saturation" discussion with the analytic statement from M1.
   Equation (3) is useful; apply it at the exit blade.
3. **Error levels.** 0.5 mrad rms quadrupole rolls are large for a transfer line (0.1–0.2 mrad is typical); 0.1 %
   rms shot energy jitter is at the high end. State the basis, or show the sensitivity of the conclusions to both.
4. **Fig. 3 (phase space).** It shows, as the text says, that the exit clouds coincide because the match is fixed.
   That is expected and occupies one of JKPS's six recommended figures; move it to the supplement unless it carries
   the M5 divergence budget.
5. **Facility name.** The ring is now the Korea Light Source (KLS); the companion manuscript uses that name. Use it
   consistently, retaining "Korea-4GSR" only in cited titles.
6. **Declarations.** Funding, acknowledgments and final approval are still placeholders. These are submission
   blockers, not scientific objections. The generative-assistance statement should name the tools actually used for
   both papers consistently.
7. **Reproducibility statement.** "A local referee attachment" is not an availability statement a journal will
   accept. Name the deposit route or "available from the author on reasonable request", as the author decides.

## Questions to the author

1. Is the m4 target the beam at the injection-septum exit used by the companion paper? If so, why are D and D′
   nonzero at a point where the ring dispersion is ≈ 0?
2. Are the booster jitter values (0.5 mm, 0.2 mrad) defined at m1 in both manuscripts?
3. What are the real vertical gaps of b1–b3 and the septum channel apertures, even as preliminary design values?

## Revision tasks (for the author)

Priority: **A** = required for acceptance, **B** = strongly recommended, **C** = editorial. "Sim" = new simulation.

| ID | Priority | Task | Sim | Acceptance criterion | Est. effort |
| :--- | :---: | :--- | :---: | :--- | :--- |
| R2B-01 | A | Element-wise aperture model: quadrupole bores, dipole gaps (with sagitta and dispersion), septum channels and the one-sided exit blade consistent with the companion geometry. Labelled parametric sweeps of unsourced dimensions. | yes | Active restriction identified per setting on a physical model; m2/m3 cases demoted to the supplement or justified | 1–2 d plus compute |
| R2B-02 | A | State the analytic K-independence of the nominal end-station clearances (M1); remove the baseline "unresolved benefit" from the headline. | no | Section 3.1 and the abstract rewritten | 0.5 d |
| R2B-03 | A | Static trajectory correction (exit steering at minimum; correctors with BPM noise preferred), shot jitter uncorrected; rerun the comparison and report which conclusions survive. | yes | Corrected and uncorrected results side by side; error model consistent with the companion | 1–2 d plus compute |
| R2B-04 | A | Analytic per-shot loss probability from the exported moments; validate it against the observed counts; compare strategies on a tail quantile and, if feasible, optimise against it on training machines with frozen held-out testing. | small | Predicted and observed losses agree within sampling; the design comparison uses a loss-relevant objective | 1–2 d |
| R2B-05 | B | Exit target: source and meaning, reconciliation with the companion paper, exit divergence budget (betatron against dispersive), and the feasibility of a dispersion-matched exit within the bounds. | small | Table 1 sourced or explicitly tied to the companion; divergence budget reported | 1 d |
| R2B-06 | B | Justify or vary the 0.5 mrad roll and 0.1 % energy jitter. | small | Sensitivity statement | 0.5 d |
| R2B-07 | C | Abstract rewritten around the physical result; Fig. 3 moved or repurposed; KLS naming; declarations and availability statement. | no | Text | 0.5 d |

**Suggested order:**
1. R2B-02 (a text change that clarifies what remains).
2. R2B-01 and R2B-03 (the model).
3. R2B-04 (the objective).
4. R2B-05 to R2B-07.

**Coordination with the companion NKM manuscript.** R2B-01, R2B-03 and R2B-05 share inputs with the NKM paper's
Reviewer 2 round-4 task R2d-6 (BTS dispersion at the septum). They should be settled once for both manuscripts.

## Choice of journal

JKPS is a reasonable venue for a concise accelerator-design article from a Korean facility study. Its scope does not
lower the bar for physical relevance. With the reframing above, I expect the paper to be suitable. Without it, a
conference proceeding (IPAC) would be the appropriate format for the methodological material.

## Confidential comments to the editor

The author has responded to two demanding rounds from Reviewer 1 with exemplary care about numerical validity and
inference. My objection is different in kind. The model's apertures sit where the beam optics are fixed by the
boundary conditions, so the realistic case is trivial and the non-trivial cases are invented. Meanwhile the
companion manuscript places the injected beam about 1.5 mm from a septum blade that this model omits. I checked the
first point analytically against Table 2 and the second against the companion paper's stated geometry.

The fix is a better physical model, not more computation, and the existing tools are well suited to it.
