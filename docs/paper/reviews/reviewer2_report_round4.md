# Referee report — Reviewer 2, fourth round

**Manuscript:** "Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design
lattice" (C. S. Park), PRAB REVTeX version.
**Version reviewed:** `docs/paper/paper.tex`, `paper.pdf` and `supplement.pdf` at commit `4b30e09`: 30-page one-column
preprint (15 pages two-column) and a 6-page Supplemental Material. SHA-256 prefixes: paper.tex `9be5b6edd5b4de92`,
paper.pdf `c0887f7f4d8c371e`, supplement.tex `13a3119f8128f9c2`.
**Also read:**
- the round-3 response (`author_response_round3.md`);
- the round-3 method notes (`../round3_*.md`);
- the campaign-04 artifacts (`results/journal_campaign_04/`), including the per-realization records.
**Date:** 2026-10-15.
**Reviewer expertise:** storage-ring beam dynamics, off-axis and multipole-kicker injection, transfer-line design,
pulsed-magnet modelling.

## Recommendation

**Major revision of limited scope. I cannot recommend acceptance of the present version, but I expect to after one
targeted ablation study and a set of consistency corrections.**

The third revision answers every task I set in round 3 (status table below):
- the NKM chamber is now feasible;
- the rings are corrected to commissioning standard;
- the operating point is re-selected for the design beam on those rings;
- the robustness study is rerun once with ring-cluster statistics.

The finite-length core (sections 1–3) is strengthened by the normalised η^1.46 scaling, which now has a declared
operational meaning. I consider that part publishable. The transparency section now states the compensation
requirement plainly, which is the honest result.

My remaining concern is the paper's new headline interpretation. The abstract states that "the losses that distinguish
the NKM come from injection errors, chiefly the booster angle jitter, acting on a 0.44 mrad angular window"; the
synthesis paragraph and the discussion repeat it. **The authors' own paired data do not support "chiefly the booster
angle jitter".** Over the paired jitter scan (seed 42, 50 realizations, identical particles and rings):

| | No booster jitter | Full booster jitter | Cost of jitter |
| :--- | ---: | ---: | ---: |
| 3-D NKM | 40.1 % | 19.5 % | −20.6 points |
| Dipole control | 68.5 % | 48.2 % | −20.3 points |
| NKM − dipole | −28.4 points | −28.7 points | — |

Booster jitter costs the two kickers the same number of points. The NKM-specific deficit, about 28 points, is
already fully present **without any booster jitter**. Table V shows the same thing from the other side: the gap is
only 4 points on the corrected rings without injection errors (78.0 against 82.2 %). The NKM-specific loss therefore
comes from the *other* injection-side errors of the budget, which the paper does not identify. In relative terms
the NKM is more jitter-sensitive (it loses half its capture, the dipole 30 %), and that may be stated. But the causal
sentence in the abstract, the synthesis and the conclusions has to be rewritten on evidence.

Two smaller but verifiable problems compound this:
1. The driver analysis enters signed errors as magnitudes, which hides one-sided effects on an asymmetric window.
2. The pulse section still uses the round-2 operating point.

Both are detailed below.

## Status of my round-3 tasks

| Task | Status | Comment |
| :--- | :--- | :--- |
| R2c-1 Feasible NKM chamber | **Resolved** | Flat 16 × 3.8 mm below the wires, applied every turn, per-slice wire-clearance check. The normalised-aperture comparison is the right way to present it. |
| R2c-2 Ring population | **Resolved**, one gap | BPM references, converged orbit, β-beat/dispersion and tune correction; β-beat ≤ 2 %; ring 5501's collapse explained. Chromaticity is not corrected, which matters now (R2d-5). |
| R2c-3 Operating point | **Met as specified; specification insufficient** | The rule I asked for was applied correctly. The objective excluded injection errors, the selected x_inj is the outermost candidate of the grid, and the choice trades angular width (0.76 → 0.44 mrad) for corrected-ring capture. See R2d-2. |
| R2c-4 Rerun | **Resolved**, criterion partly unmet | My acceptance criterion was "tuning optimum not at a sweep boundary". 28 % of the machines end on the outer x_inj bound. |
| R2c-5 Synthesis | **Done; attribution incorrect** | The hierarchy table and the rejection of the DA-margin hypothesis are good work. The NKM-specific mechanism is misattributed (R2d-1). |
| R2c-6 Simultaneous wire errors | **Resolved** | A median of 2.6σ/4.8σ at 10 µm, with 3 % of draws inside 0.1σ, is a clear and important result. |
| R2c-7 Septum leakage | **Resolved** | The 0.066 G requirement is correctly derived and scoped. |
| R2c-8 Ring dependence | **Resolved** | Ring-cluster and leave-one-ring-out ranges given. |
| R2c-9 Minor | **Resolved** | — |

I also accept that two of my round-3 expectations were not borne out, and I thank the author for reporting this
directly: the gain did not come from the septum position, and the DA margin does not organise capture.

## Major comments

### M1. The NKM-specific loss is not explained by booster angle jitter (abstract, section 7.2, discussion, conclusions)

The arithmetic is in the recommendation above. In detail:

1. **Paired jitter scan.** The NKM − dipole difference is essentially constant over the scan: −28.4 points at zero
   jitter and −28.7 at full jitter on the same 50 realizations. On the 150-realization full budget it is −28.0
   [−32.5, −23.5].
2. **Where the gap opens.** Between the "corrected rings, no injection errors" row (−4.2 points) and the "joint
   errors, no booster jitter" row (−28.4 points) of Table V. The rows are not paired, as the caption correctly says.
   The order of magnitude, a 24-point NKM-specific loss from non-jitter injection errors, is nevertheless
   unambiguous.
3. **Why the driver analysis points to booster angle.** The Holm-significant association with booster angle
   (ρ = −0.38) is a statement about the NKM's capture, not about the NKM − dipole difference. The dipole would show a
   similar association.

**Candidate mechanisms.** The non-jitter terms that act on the NKM but not on a uniform kick are:
- the NKM-to-orbit offset (0.2 mm rms each for the magnet and the residual orbit);
- the common NKM amplitude (0.5 %);
- the septum position (0.1 mm) and strength (0.1 %);
- the beam's emittance and energy fluctuations through the *nonlinear* kick.

A physical expectation helps. At the selected point the centroid passes the magnet at −7.44 mm, about 1.2 mm on the
inner flank of the kick extremum (−8.6 mm). On that flank the kick slope is large, so a 0.2 mm offset between kicker
and beam converts directly into an exit-angle error of the same order as the 0.44 mrad window. A uniform kick is
immune to it.

**An exploratory check I made on the campaign-04 records.** Zero-jitter ensemble, 50 realizations, unadjusted, not
controlled for ring identity:
- *Signed* NKM displacement `nkm_dx_m`: ρ = +0.32 (p = 0.02) with NKM capture, against +0.12 (p = 0.40) with
  dipole capture.
- The *magnitude* gives +0.12 for the NKM, i.e. nothing.

This is suggestive, not conclusive. It does show that the conclusion depends on how the errors are entered (M3).

**Requested.** A paired one-factor ablation at zero booster jitter on the seed-42 machines:
- each error class switched on alone, and each switched off from the full zero-jitter budget;
- NKM and dipole on identical particles;
- the NKM − dipole difference reported per class.

This needs about 12 × 50 realizations at the existing 200 particles and 500 turns. Then rewrite the abstract, the
synthesis paragraph ("Third, …"), the discussion paragraph and the conclusions on that evidence. If the offset term
dominates, the paper's design message becomes "kicker-to-orbit alignment on the steep flank", which is a more useful
result than "angular stability of the booster beam". It also connects directly to the transparency section, where the
same offset sets the stored-beam disturbance.

### M2. The operating-point conclusion is untested where the paper states it as a direction

Section 7.2 states: "a selection that includes them would favour a wider angular window, such as that of the earlier
point (0.76 mrad), which this study does not test." Three observations from the artifacts make this a required test
rather than an outlook:

1. **Selection grid.** The selected x_inj (−19.48 mm) is the outermost candidate of the E6 grid (clearance limit
   +1.0 mm). The selection's p10 margin over the next candidates is 1.7–4 points, which is below the counting
   resolution of 100 particles per ring.
2. **Tuning.** Under the error budget, the tuned machines move away from the selected point:
   - x_inj moves outward in 32 of 50 machines (14 on the bound);
   - S drops to ≤ 0.925 in 31 of 50;
   - the angle trim stays near zero (28 of 50 at 0, balanced ±).
   Both moves bring the centroid toward the kick extremum, i.e. toward the geometry of the earlier point
   (S = 0.85, centroid −8.52 mm).
3. **No paired evidence.** The earlier point was never run under the E7 joint-error conditions on the corrected rings.
   The round-2 joint result (14.8 %) used orbit-only rings and the old chamber, so it is not comparable.

**Requested.** Run the earlier point, and one point with the centroid at the kick extremum at the selected x_inj, on
the E7 zero-jitter and full-budget seed-42 ensembles. Use paired particles and machines (2 points × 2 ensembles ×
50 realizations).

Report the paired differences against the selected point. If a wider-window point is more robust, either re-select
with an objective that includes the error budget (on an x_inj grid extended beyond +1.0 mm), or state plainly that the
selected point is optimal only without injection errors. The present text leaves the reader unable to tell whether the
round-3 re-selection improved or worsened the robust capture.

### M3. Association analysis enters signed errors as magnitudes

`analyze_round2_robustness.py` builds every scalar feature as `abs(s[key])`, including:
- the booster offsets;
- the NKM displacement;
- the NKM amplitude;
- the septum position;
- the energy error.

The angular window is strongly asymmetric: −0.32/+0.12 mrad about the matched angle. The kick slope also has a sign on
the flank. A one-sided effect therefore has no monotone relation to the magnitude, and a partial Spearman on |x|
cannot detect it. This is why the NKM offset is invisible in the ranking (M1).

**Requested.**
- Use signed features for signed errors, or a physically constructed predictor such as the predicted exit-angle
  error of the centroid from the linearised kick slope at the centroid.
- Report the dipole association table alongside the NKM table, so the reader sees which drivers are NKM-specific.

### M4. The pulse section uses the round-2 operating point (consistency error)

Section 8 takes its inputs from `results/journal_campaign_03/d12_final_pulse.json` (manifest key `round2_pulse`). In
consequence:
- **The allowance.** The residual allowance is 0.076 mrad, i.e. one tenth of the *earlier* 0.76 mrad window. Section 3
  uses one tenth of the *selected* window, 0.044 mrad, and both are described as "one tenth of the angular-window
  width".
- **The other quantities.** The turn-1–3 positions (−2.9/6.2/… mm), the full-field kicks, the first/second-return
  fractions and the pulse-length limits (5.85 and 5.33 µs) all belong to the earlier point.

The 5.3 µs example sits within 0.03 µs of the "no return" limit, so the conclusion can change at the selected point.

**Requested.** Recompute the pulse quantities at the selected point, and move `round2_pulse` into the round-3
overrides, so the manifest check catches this class of omission.

### M5. What kills half of the realizations?

**The observation.**
- 51 % of the 150 full-budget realizations capture nothing (the median of 0 in the text).
- In the per-realization records, more than 98 % of all NKM losses are classified `ring_elsewhere`. The remainder
  are septum creation (325 particles) and `outside_field_map` (99).
- The in-magnet chamber and the septum are therefore not where the beam dies.

**What the paper does not say.**
- Whether those dynamical losses are horizontal or vertical, where they occur, and at which turns.
- Section 5 promises: "Whether coupling on the corrected rings uses that margin is part of the robustness study
  below." The robustness study never returns to it.
- With no skew correction, 100 µrad rolls and skew-quadrupole components, vertical losses at the 3.8 mm chamber
  (βy = 5.6 m) or at the closed IVUs are plausible.
- Ring 5501, which captures 31 % with a first unstable launch at −10.5 mm, i.e. a large margin, is the obvious place
  to look.

**Requested.**
- Report the loss plane and location (per-plane loss histograms like Fig. 8, centre) for the zero-capture
  realizations and for ring 5501.
- Report the residual coupling or vertical emittance of the ten corrected rings.
- Close the section 5 promise explicitly.
- Define `outside_field_map` as a loss category: is it a numerical bound or a physical aperture?

## Minor comments

1. **Chromaticity attribution (section 7.2, R2d-5).**
   - The corrected-ring chromaticities span only 5.86–6.89, with 3.4 design.
   - The ρ = −0.68 association comes from ten rings and 16 unadjusted tests (8 correlates × 2 models), with
     p = 0.03.
   - The β-beat association has p = 0.08 (NKM) and 0.11 (dipole).
   - Ring 5502 has the highest chromaticity and 87 % capture.

   Either correct the chromaticity to its design values with the sextupole families, a standard commissioning step
   absent from the chain, and show whether the ring spread survives, or reduce the claim to "ring-to-ring spread is
   common to both kickers".
2. **BTS dispersion at the septum (Table II, section 2C).** The injected beam carries D = 80.9 mm and D′ = 47.5 mrad
   at the septum exit (`injected_beam` in the study configuration), against Dx = 0.3 mm in the ring at the NKM. This
   appears nowhere in the paper. For a 0.44 mrad window it matters:
   - The 0.1 % rms mean-energy jitter becomes a 48 µrad shot-to-shot angle error.
   - The 1.06×10⁻³ energy spread adds about 50 µrad of correlated angular spread, comparable to the betatron
     divergence (57 µrad).

   State D and D′ in Table II, quantify their share of the angular budget, and say whether a dispersion-matched BTS
   (D′ → 0 at the septum) is feasible. It is a design lever directly aimed at the paper's narrow window.
3. **Dipole jitter sensitivities.** Add the dipole's position-only and angle-only paired differences to Table IV, so
   the "angle-only costs 16.8 points" statement has a control.
4. **Bimodal distribution.**
   - With 51 % zero-capture realizations, the mean (16.1 %) is a mixture statistic.
   - Report the zero-capture fraction and the mean of the non-zero realizations next to the mean, for both models.
   - The ECDF in Fig. 10 shows it, but the text should say it.
5. **Transparency at the selected S.**
   - Section 6, Table I ("0.10 of σx at 0.2 mm") and the wire Monte Carlo are evaluated at S = 0.85 and rescaled by
     1.12 in the text.
   - At S = 0.95 the 0.2 mm response is about 0.11σ, nominally above the 0.1σ criterion the sentence invokes.
   - Regenerate at S = 0.95, or state the rescaled values in Table I and the abstract.
6. **Fig. 9 (left) caption.** "at the selected point" for the 100/10 nm rad sensitivity case should name the point
   (it is not the round-3 point).
7. **Margin fit.** Say that the logistic fit is degenerate: its width ends on the 5 mm fit bound. "Does not organise
   capture" is then supported by ρ alone, which is fine.
8. **Tuning range.** Stated now. Extend it as part of M2, or keep the boundary fraction in the abstract-level
   statement of the tuning gain.
9. **Dates.** The paper is dated October 12 and the supplement October 13; both predate the round-3 results. Update
   both.

## Questions to the author

1. At the selected point, what is the local kick slope ∂Δx′/∂x at the centroid, and at the earlier point? Does the
   ratio of the two predict the ratio of the angular-window widths (0.44/0.76)?
2. Is the 80.9 mm / 47.5 mrad septum dispersion a design property of the matched BTS line, or a consequence of the
   BTS optimisation's objective (β-matching only)?
3. Are the zero-capture realizations clustered by ring identity, or by NKM offset sign?

## Revision tasks (for the author)

Priority: **A** = required for acceptance, **B** = strongly recommended, **C** = editorial. "Sim" = new simulation.

| ID | Priority | Task | Sim | Acceptance criterion | Est. effort |
| :--- | :---: | :--- | :---: | :--- | :--- |
| R2d-1 | A | Paired one-factor ablation at zero booster jitter (each class alone and each left out; NKM and dipole on identical particles; seed-42 machines). Rewrite the abstract, the section 7.2 synthesis, the discussion and the conclusions on that evidence. | yes | NKM − dipole difference attributed per error class; the abstract's causal sentence matches it | 1 d plus ~1 d compute |
| R2d-2 | A | Paired runs of the earlier point and an extremum-centred point on the E7 zero-jitter and full-budget seed-42 ensembles. Then either re-select with an error-inclusive objective on an extended x_inj grid, or state that the selected point is optimal only without injection errors. | yes | Paired differences reported; the sentence "which this study does not test" removed | 0.5 d plus ~0.5 d compute |
| R2d-3 | A | Recompute the pulse section at the selected point (allowance, turn positions and kicks, pulse-length limits); move `round2_pulse` into the round-3 overrides. | small | One allowance convention throughout; pulse macros sourced from campaign 04 | 0.5 d |
| R2d-4 | B | Signed or physically constructed predictors in the association analysis; dipole association table beside the NKM table. | no | Ranking reported for both models | 0.5 d |
| R2d-5 | B | Loss plane and location for the zero-capture realizations and ring 5501; corrected-ring coupling or vertical emittance; close the section 5 coupling sentence; define `outside_field_map`. Chromaticity correction to design values, or a reduced chromaticity claim. | small | Losses located; claims match ten-ring statistics | 1 d |
| R2d-6 | B | State the BTS dispersion at the septum; quantify its angular contribution; discuss dispersion matching. | small | Table II and section 2C updated | 0.5 d |
| R2d-7 | C | Dipole x-only and x′-only jitter rows; zero-capture fraction and conditional means; transparency at S = 0.95 (or rescaled values in Table I); Fig. 9 caption; margin-fit degeneracy; dates. | no | Text, tables and captions | 0.5 d |

**Suggested order:**
1. R2d-3 and R2d-7, which are mechanical.
2. R2d-1 and R2d-2 together. They share the seed-42 machines, and R2d-2's outcome may change the selected point;
   if it does, rerun only the zero-jitter and full seed-42 ensembles and the window, not the whole campaign.
3. R2d-4 to R2d-6 alongside.
4. A final reconciliation and a new frozen bundle as in round 3.

## Choice of journal

PRAB remains appropriate. The finite-length result now has a quantitative, falsifiable form (η^1.46 against a
declared allowance), and the robustness section is built on a defensible machine model. A PRAB referee will check
precisely the attribution in M1, because it is the paper's design recommendation; it must be right.

## Confidential comments to the editor

This is a much-improved manuscript. The author executed every round-3 request, including those whose outcome went
against my own expectations, and reported the results candidly. My remaining objection concerns the interpretation
of the robustness result, which the author's own paired data contradict. I checked it directly against the
campaign-04 per-realization records:
- booster jitter costs the NKM and the dipole the same 20 points;
- the 28-point NKM-specific gap exists at zero jitter.

The fix is a modest ablation study, together with mechanical corrections to the pulse section. I expect to recommend
acceptance once R2d-1 to R2d-3 are done.
