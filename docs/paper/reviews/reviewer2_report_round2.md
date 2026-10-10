# Referee report — Reviewer 2, second round

**Manuscript:** "Finite-length and vertical effects in nonlinear-kicker injection into the Korea Light Source"
(C. S. Park), revised version.
**Version reviewed:** `docs/paper/paper.tex` and `paper.pdf` at commit `03b8fe9`. The PDF has 12 pages in the generic
`article` class and contains 8 figures, 2 tables and 22 cited references. SHA-256 prefixes: paper.tex
`3fa584e90a15e27b`, paper.pdf `e5cc5b651961cb0d`.
**Also read:** the author response (`reviews/author_response.md`) and the journal-fit note (milestone 134), which
names Phys. Rev. Accel. Beams first and JINST or NIM A as alternatives.
**Date:** 2026-10-11.
**Reviewer expertise:** storage-ring beam dynamics, off-axis and multipole-kicker injection, transfer-line design,
pulsed-magnet modelling.

## Recommendation

**Major revision. I do not recommend acceptance in the present form.**

The revision is substantial and much improved:
- The kicker is now an exact filament field tracked in slices, validated against the RADIA map to 4×10⁻¹⁰.
- The finite-length mechanism is demonstrated rather than conjectured.
- The window is defined by a threshold at 0.1 mrad resolution.
- Survival is checked to one damping time.
- The stored-beam response is computed deterministically and confirmed by tracking.
- The error analysis now separates jitter from static errors.

Most of my first-round A tasks are resolved (table below).

Three of the paper's main conclusions still rest on idealisations whose size I could check, and they are not small:
- **Capture depends on the chamber.** The headline capture (93 %) is computed without a vacuum chamber. The
  manuscript's own aperture scan gives 47.9 % at a ±10 mm half-width and 76.0 % at ±11 mm, which are typical
  fourth-generation chamber dimensions.
- **Transparency is fragile.** It is presented as an exact symmetry. I evaluated the author's filament model with one
  inner wire displaced by 1 µm. The on-axis vertical dipole kick is 7.3×10⁻⁵ of the peak kick, which already exceeds
  the 4×10⁻⁵ residual limit stated in section 8. Transparency therefore rests on sub-micrometre conductor placement or
  on a correction scheme, and the paper discusses neither.
- **The pulse range contradicts the residual requirement.** The 5–8 µs half-sine pulse quoted in section 8 does not
  meet the paper's own requirement r ≲ 0.19 on the turn after injection. At 8 µs, r = 0.50; the limit is a base
  length of about 6.1 µs.

These points do not invalidate the physics of sections 3–4. However, they change what a designer can take from the
paper, and they must be resolved before acceptance at any of the candidate journals.

## Summary of the revised manuscript

A 0.525 m four-loop wire NKM (3 kA, peak kick 4.89 mrad at x = −8.6 mm, S = 0.85) is modelled by the Biot–Savart field
of its filaments. The kicker sits in a KLS design lattice (file K4GSR_HBIv4-1; 61.6 pm; DA −12/+13 mm at the kicker).
A coupled bunch is tracked from the booster through a matched BTS, and the ring is tracked natively in 6-D. The claims
are:

- **(i) Self-deflection.** The beam's self-deflection inside the magnet (sagitta |K|L/8 = 0.32 mm) shifts the matched
  angle by 0.22 mrad and makes capture tolerant to positive angle errors.
- **(ii) Vertical defocusing.** The curl-free vertical kick costs up to about 5 points of capture, and about 2 at the
  selected point. It had been hidden by a sign error in the tabulated map.
- **(iii) Capture and window.** At x_inj = −19.5 mm and x′ = 4.853 mrad, capture is 93.0 % against 97.0 % for a
  calibrated dipole. The angular window is 0.74 mrad and the position window 1.44 mm at 80 % capture.
- **(iv) Transparency.** For an aligned kicker it holds exactly by symmetry; at a 0.2 mm offset the response is 0.10 σ.
- **(v) Combined errors.** Mean capture is 40.5 % without and 44.4 % with ideal static orbit correction. Booster
  jitter below a quarter of the assumed value costs nothing, and 80 % is not reachable under the assumed budget.

## Status of the first-round tasks

| Round-1 task | Status | Comment |
| :--- | :--- | :--- |
| R2-1 validated kicker model and mechanism | **Resolved** | Exact field, slice convergence, mechanism figure. Well done. |
| R2-2 one model for headline, figures, conclusions | **Resolved** | All results use the 3-D model, except figure 4 (see M8). |
| R2-3 ring errors, corrected, real chamber | **Partly** | Only uncorrected gradient/sextupole errors, without misalignments or correction. The chamber is a parameter scan, not the headline (M1, M2). |
| R2-4 tracking duration | **Resolved** | 4000 turns; the late loss is 3.5 points. The headline is still the 500-turn value (M8). |
| R2-5 tolerance curves | **Resolved, with caveats** | Jitter, offset and emittance curves are given. Their interpretation depends on M5. |
| R2-6 sources for jitter, emittance and energy spread | **Not resolved** | Every entry in table 2 is still "assumed". No booster design value is cited (M5). |
| R2-7 pulsed-magnet section | **Partly** | Order-of-magnitude estimates are given, but the quoted pulse range contradicts them, and eddy currents are not quantified (M4). |
| R2-8 near-axis transparency, vertical, tracked | **Resolved for the ideal geometry** | Manufacturing tolerances are missing (M3). |
| R2-9 acceptance diagram, fine scan, window definition | **Resolved** | |
| R2-10 literature and comparison table | **Partly** | 22 references, but the requested NLK/MIK comparison table is not in the manuscript (m4). |
| R2-11 parameter tables, geometry figure | **Resolved** | Some ring/RF entries are missing (m7). |
| R2-12 validation at the operating point | **Partly** | Figure 4 is still at a provisional thin-map point (M8). |
| R2-13 balanced controls; partial correlations | **Resolved** | |
| R2-14 chromatic scaling | **Resolved** | Canonical momentum is treated correctly. |
| R2-15 name the facility | **Resolved, with a question** | The lattice version relative to the KLS baseline is unclear (M7). |
| R2-16 condense section 5.1 | **Resolved** | |
| R2-17 figure fixes | **Resolved** | |
| R2-18 abstract and definitions | **Partly** | The abstract mixes two operating points (m6). |
| R2-19 journal and template | **Partly** | Generic article class. The PRAB recommendation is not yet applied (m5). |
| R2-20 framing for the chosen journal | **Not yet** | See M6. |

## Major comments

**M1. Capture without a vacuum chamber is not a usable headline.**
Section 2.1 states that in the main results "losses arise at the septum blade and from dynamical instability". There
is no physical aperture. Section 5 then shows how much the chamber matters:

| Rectangular chamber half-width × half-height, every element | Capture |
| :--- | ---: |
| ±15 × ±5 mm | 86.3 % |
| ±12 × ±5 mm | 83.8 % |
| ±11 × ±5 mm | 76.0 % |
| ±10 × ±5 mm | 47.9 % |

Arc chambers in fourth-generation rings typically have inner radii of about 10–12 mm. Insertion devices, especially
in-vacuum undulators, restrict the vertical aperture much further. The manuscript shows that the injected oscillation
couples into the vertical plane, so this restriction matters directly. Capture at the KLS chamber could therefore lie
anywhere between about 50 % and 85 %, and the 93 % headline does not tell the reader where. Required:
- **(a)** Use the KLS chamber profile, including the injection straight, the arcs, the small-gap insertion devices and
  the septum region, as the default aperture model for every capture number.
- **(b)** Give a loss map (s, plane) at the operating point.
- **(c)** If the chamber is not yet defined, state the minimum half-width and half-height for which the conclusions
  hold. Report the headline as a function of that dimension, not without a chamber.

**M2. Ring errors are still only an uncorrected bound.**
Random 0.05 % and 0.10 % gradient errors without misalignments or correction already reduce mean capture to 85.6 % and
69.9 %. A real machine has larger magnet errors but is corrected, so the net effect is unknown in either direction.
The cited KLS lattice paper (Kim et al., IPAC'25) reports commissioning simulations with optics correction. Error
seeds of that kind are exactly what is needed. Required:
- at least 10 corrected seeds with misalignments and multipole errors, at the operating point and with the chamber of
  M1;
- capture and DA per seed, including the corrected-seed spread of the negative DA edge, which sets the margin of the
  window.

This is the step from a magnet study to a design study of the KLS, as the title implies.

**M3. Transparency "by exact symmetry" needs a manufacturing tolerance analysis.**
The symmetry argument holds only for an ideal four-fold geometry with identical loop currents. Using the author's own
filament model (`FilamentGeometry`, integrated on axis), I obtain:

| Perturbation | On-axis ∫B_y / peak | On-axis ∫B_x / peak |
| :--- | ---: | ---: |
| One inner wire displaced 1 µm in x | −6×10⁻⁹ | 7.3×10⁻⁵ |
| One inner wire displaced 10 µm in x | −7×10⁻⁷ | 7.3×10⁻⁴ |
| One inner wire displaced 50 µm in x | −1.7×10⁻⁵ | 3.6×10⁻³ |
| One loop's current +0.1 % | 1.9×10⁻⁴ | −1.9×10⁻⁴ |

Section 8 requires an on-axis dipole residual below 4×10⁻⁵ of the peak kick for 0.1 σ_x. The vertical plane is
stricter: with ε_y = 0.1 ε_x and β_y = 5.6 m, the 1 µm case already gives A_y ≈ 0.3 σ_y. If these numbers are right,
transparency is set by:
- conductor placement at the sub-micrometre level;
- current balance between loops at the 10⁻⁴ level, unless the loops are in series;
- or a correction scheme.

It is not set by the kicker-to-orbit offset that the abstract emphasises. The paper must:
- **(a)** Give the sensitivity of the on-axis dipole and quadrupole residuals, in both planes, to the position of each
  wire and to the current imbalance between loops.
- **(b)** Say whether the loops are powered in series.
- **(c)** Derive the mechanical tolerances or the correction (trim, beam-based compensation) needed for 0.1 σ in both
  planes.
- **(d)** Compare with the transparency actually achieved by the MIKs at MAX IV and SOLEIL, which was limited by
  manufacturing and coating effects.

Until this is done, "transparency is set by the kicker-to-orbit offset" should not appear in the abstract or the
conclusions.

**M4. The pulsed-magnet section is internally inconsistent and incomplete.**
For a half-sine pulse injected at its peak, the field fraction on the next turn is |cos(πT_rev/T)| when T/2 < T_rev ≤ T.
It is zero when the base length T is at most 2T_rev = 5.3 µs.

| Base length T | r on the next turn |
| :--- | ---: |
| 5 µs | 0 |
| 6 µs | 0.17 |
| 7 µs | 0.37 |
| 8 µs | 0.50 |

The requirement r ≲ 0.19 therefore needs T ≲ 6.1 µs, but the text quotes 5–8 µs. Required:
- **(a)** State the maximum pulse length implied by the requirement, and the timing of injection on the pulse.
- **(b)** Quantify the bunch-to-bunch variation of the field seen by the stored train during one revolution. It
  matters as soon as the kicker is offset (M3).
- **(c)** Estimate the eddy-current and coating fields for the planned chamber: material, thickness, and the
  resulting dipole and quadrupole terms. MAX IV measured such terms (Kallestrup 2019), so "outside this study" is not
  sufficient for a paper whose main claim is transparency.

**M5. The robustness conclusion depends on an unsourced budget and on an unrealistic correction model.**
Both ends of the correction model are unrealistic:
- **No correction.** Static transfer-line errors reach the septum unchecked.
- **Ideal correction.** The static trajectory is removed exactly.

In operation neither happens. Injection is tuned with beam: the septum position and angle and the kicker amplitude are
scanned to maximise efficiency. Static NKM, orbit and septum offsets are therefore largely compensated, which the
manuscript's own figure 8 (right) suggests is possible. The paper concludes that "the remaining loss comes from the
combined static errors", but that loss may simply disappear after such tuning. Required:
- **(a)** Re-evaluate the static-error ensemble after per-realization re-optimisation of the injection knobs
  (x_inj, x′_inj, S), with realistic BPM resolution, or at least after a two-knob septum scan.
- **(b)** Replace "assumed" in table 2 with sources: the KLS booster design emittance, the extraction kicker and septum
  stability, and measured values from comparable full-energy boosters. The emittance curve of section 7.2 shows a 10–15 point
  sensitivity between 100 and 200 nm rad, so 100 nm rad needs a source.
- **(c)** List the pulsed septum strength and the RF phase / arrival-time jitter as separate error terms. Angle jitter
  is the dominant driver, and part of it physically comes from the septum, not the booster.

Without (a) and (b), the central robustness numbers (40.5 % and 44.4 %) describe an arbitrary budget, not the KLS.

**M6. Novelty and generality must be framed accurately, especially for PRAB.**
Two contributions need reframing:
- **Self-deflection.** The "deflected-path" model of section 3 is a kick-map profile distributed along the magnet and
  sampled along the actual trajectory, i.e. a sliced kick map. This is standard practice for undulators and for
  long nonlinear elements. The general content is the validity criterion "sagitta ≪ width of the kick extremum". To
  establish it, the author should:
  - express it as a dimensionless parameter, e.g. η = |K|L / (8 w), with w the half-width of the extremum where
    capture stays above threshold;
  - show the matched-angle shift and the asymmetric sensitivity as functions of η, for several L and K, and for at
    least one other NLK/MIK geometry, for example the BESSY II type;
  - compare with a sliced kick map, not only the single thin map.
- **Vertical sign error.** Contribution (ii) is described as "previously hidden by a sign error in the tabulated
  vertical kick". That is a correction of the project's own input data, not a physical result. The physics is that the
  curl-free vertical partner, −∂Δx′/∂x, defocuses the injected bunch off the extremum, which follows from Maxwell's
  equations. Present it as a consistency check for kick maps, ∂Δx′/∂y = ∂Δy′/∂x, plus the capture consequence. Move
  the history to a footnote or methods remark.

For PRAB, the abstract and conclusions should lead with the criterion and its scaling, not with KLS-specific numbers.

**M7. Lattice identity and version.**
The title names the KLS, and Kim et al. 2025 describe a KLS baseline with sextupoles and octupoles optimised for "a
large dynamic aperture". The manuscript uses the file K4GSR_HBIv4-1, whose DA is −12/+13 mm with "the bare design"
sextupoles, and its discussion says that sextupole optimisation "is expected to enlarge the window". Please:
- state the version and date of the lattice file and its relation to the current KLS baseline;
- say whether the 0.525 m four-loop NKM is a KLS project design or the author's study design;
- if the baseline differs, repeat at least the DA, the operating point and the window on it, or retitle the paper, for
  example "…into a 4 GeV hybrid-MBA ring (KLS design)".

**M8. Headline definitions and the validation section.**
- Capture is defined as survival over 500 turns, but 3.5 % of particles are lost between turns 500 and 4000. Either
  define the headline at the converged survival (89.5 %), or state in the abstract and the conclusions that 500-turn
  values overestimate it by about 3.5 points.
- Figure 4 (backend validation) still refers to "a provisional point (campaign 01, thin kick map)". Repeat the
  backend comparison and the turn convergence at the operating point with the 3-D model, or move it to an appendix as
  a historical validation.

## Minor comments

- **m1. Internal project history in the text.** "Earlier work" (section 6, the 5×10⁻⁶ σ value), "the earlier
  operating point" (section 3, never defined in this paper), "campaign 01" (figure 4) and "previously hidden by a sign
  error" refer to unpublished drafts. A journal reader cannot follow them. Define every point used and remove draft
  history.
- **m2. Report the paired statistics behind "costs nothing measurable".** From the artifacts, corrected jitter at 0.25
  versus 0 gives a paired difference of +0.3 points (95 % bootstrap −1.5 to +2.1). Half the jitter versus none gives
  −6.1 (−9.9 to −2.4). Quote these instead of overlapping unpaired bands, and state that the scan uses one seed
  (50 realizations).
- **m3. Partial correlations.** Thirteen inputs are tested. State whether p-values are corrected for multiplicity, or
  give Holm-adjusted values. The conclusion (angle jitter dominates) is robust, but p = 0.006 for position jitter should
  be reported with the correction.
- **m4. Comparison table.** Put the table of NLK/MIK systems (KEK-PF, BESSY II, MAX IV, SOLEIL, SIRIUS, and others
  under construction) in the paper. It should list magnet type, length, peak kick, aperture, DA, achieved efficiency
  and transparency. The response cites `novelty_and_comparison.md`, which reviewers and readers cannot see.
- **m5. Format.** The keywords are the JINST keyword list. For PRAB, use REVTeX 4.2 with PhySH subject headings and the
  APS reference style. Remove the line numbers in the final version according to journal practice.
- **m6. Abstract.**
  - It contains about 12 numbers.
  - "Costing up to five percentage points" refers to an operating point not used elsewhere, whereas the effect at the
    selected point is about 2 points.
  - "Up to five" reads as the effect at the operating point. Quote the selected-point value or state the condition.
- **m7. Table 1.** Add:
  - RF frequency and voltage, momentum compaction, synchrotron tune and damping times;
  - the bunch length of the injected beam;
  - the NKM pulse;
  - the chamber dimensions (see M1).
  The DA in table form would help.
- **m8. Vertical emittance.** ε_y = 0.1 ε_x is assumed for the stored beam. State its source (the KLS coupling target)
  and how the vertical transparency scales with it, since the vertical case is the tighter one (M3).
- **m9. Septum.** The septum leakage field on the stored beam is not mentioned. In a transparent-injection paper it
  belongs in the budget of the stored-beam disturbance, if only as an estimate.
- **m10. Gauss–Hermite quadrature.** Give the order and the convergence check, one sentence each.
- **m11. Data availability.** A frozen bundle "provided to referees" should be accessible through an anonymous or
  persistent link at submission, not created on acceptance.
- **m12. Figure 7 (left).** Four bunches per control are shown as markers. Add the paired NKM − dipole difference with
  its interval directly on the panel, since this is the quantity discussed in the text.
- **m13. Wording.** "Transparency is set by the kicker-to-orbit offset" (abstract) and "the engineering quantities are
  the kicker-to-orbit alignment, the on-axis residual field and the pulse length" (section 9) should agree. After M3
  the second, more complete statement should be the one used.

## Questions to the author

1. Are the four NKM loops powered in series from one pulser? What is the expected wire-positioning accuracy of the
   assembly?
2. What is the KLS vacuum-chamber profile at the injection straight and in the arcs? What are the smallest
   insertion-device gaps?
3. Does the KLS booster design specify the extraction emittance and the orbit stability at extraction? Which booster
   design is assumed?
4. Is K4GSR_HBIv4-1 the lattice of Kim et al. (IPAC'25), or an earlier version?
5. How would the injection be tuned in commissioning (knobs, diagnostics)? Could a beam-based scan recover the static
   errors of table 2?

## Revision tasks (for the author)

Priority: **A** = required for acceptance, **B** = strongly recommended, **C** = editorial. "Sim" = new simulation
required.

| ID | Priority | Task | Sim | Acceptance criterion | Est. effort |
| :--- | :---: | :--- | :---: | :--- | :--- |
| R2b-1 | A | Realistic chamber (KLS profile incl. IDs and septum region) as the default aperture for all capture numbers; loss map; or the minimum aperture for which conclusions hold. | yes | Headline capture quoted with a defined chamber; loss map figure | 2–3 d |
| R2b-2 | A | Corrected ring-error seeds (≥ 10; misalignments, multipoles, orbit/optics correction, ideally the KLS commissioning seeds) at the operating point with the chamber of R2b-1. | yes | Capture and DA distributions over seeds; margin of the window stated | 3–5 d |
| R2b-3 | A | Manufacturing and powering tolerances of transparency: sensitivity of on-axis dipole/quadrupole residuals (both planes) to each wire position and to loop-current imbalance; required tolerances or correction scheme; vertical plane included. | small | Table of sensitivities; tolerances for 0.1 σ in x and y; abstract and conclusions revised accordingly | 1–2 d |
| R2b-4 | A | Pulsed-magnet consistency: maximum pulse length from r ≲ 0.19, injection timing on the pulse, bunch-train variation, eddy-current/coating estimate for the planned chamber. | partly | Section 8 internally consistent; each effect quantified | 1–2 d |
| R2b-5 | A | Beam-based re-optimisation of injection knobs per static-error realization (septum position/angle, NKM amplitude), with BPM resolution; compare with ideal correction. | yes | Capture under static errors after tuning; robustness conclusion revised | 2–3 d |
| R2b-6 | A | Sources for the error budget: KLS booster emittance and extraction stability, septum strength stability, RF phase jitter as separate terms. | no (rerun if values change) | Table 2 with a source per entry or an explicit statement of where none exists | 1 d |
| R2b-7 | A | State the lattice version and the NKM design status; repeat DA, operating point and window on the current KLS baseline if different, or retitle. | maybe | Text, and figures if the lattice differs | 0.5–3 d |
| R2b-8 | A (PRAB) / B (JINST, NIM A) | Generalise the finite-length result: a dimensionless parameter (sagitta / extremum width), scaling over L and K, one other NLK/MIK geometry, comparison with a sliced kick map; reframe the vertical-sign item as a kick-map consistency check. | yes | Scaling figure; contributions restated; draft history removed | 3–4 d |
| R2b-9 | B | Headline at converged survival, or the 500-turn bias stated; repeat backend validation (figure 4) at the operating point with the 3-D model or move it to an appendix. | small | Abstract and conclusions consistent with section 5; figure 4 updated | 0.5–1 d |
| R2b-10 | B | Paired statistics for the jitter levels; multiplicity-adjusted partial correlations; seed count stated. | no | Paired differences with intervals in the text | 0.5 d |
| R2b-11 | B | NLK/MIK comparison table in the manuscript. | no | Table with verified values and references | 1 d |
| R2b-12 | B | Septum leakage-field estimate on the stored beam; vertical-emittance source and scaling; Gauss–Hermite order. | no | Text | 0.5 d |
| R2b-13 | C | Remove internal history ("earlier work", "earlier operating point", "campaign 01"); abstract with fewer numbers and the selected-point vertical cost; wording consistency (m13). | no | Text | 0.5 d |
| R2b-14 | C | Table 1 additions (RF, momentum compaction, damping times, bunch length, pulse, chamber). | no | Table | 0.5 d |
| R2b-15 | C | Convert to the chosen journal (PRAB: REVTeX 4.2, PhySH, APS style); accessible evidence link at submission. | no | Clean build in the journal template; link in the availability statement | 0.5–1 d |

**Suggested order:**
1. R2b-7, because the lattice decides everything else.
2. R2b-6, which fixes the budget before rerunning.
3. R2b-1, then R2b-2, which set the realistic baseline.
4. R2b-5, for robustness with realistic tuning.
5. R2b-3 and R2b-4, for transparency and pulse (largely independent and cheap).
6. R2b-8, for generality.
7. Then the B and C items.

R2b-1, R2b-2 and R2b-5 change the absolute capture numbers, so rerun the C5/C6 ensembles only after them.

## Choice of journal

I agree with the author's ranking (milestone 134). The required work differs by venue:
- **PRAB:** R2b-8 is decisive. Without the generalisation, the paper is a facility design study, which PRAB accepts
  only if it is complete (R2b-1, R2b-2, R2b-5).
- **JINST or NIM A:** R2b-3 and R2b-4 (mechanical and pulsed-magnet tolerances) carry the most weight. The tolerance
  orientation of the paper fits these journals well.

In either case the A items above are needed.

## Confidential comments to the editor

The author has responded to the first round thoroughly and with unusual transparency; the numerical work is
reproducible and the statistical treatment is sound. My remaining concerns are about realism rather than correctness:
- the absent chamber;
- the uncorrected ring errors;
- an untreated manufacturing tolerance that I estimate to be at the micrometre level and that undermines the
  transparency claim as stated;
- an assumed error budget whose static part would in practice be tuned out.

I checked the two quantitative points (M3 and M4) with the author's own model and stated formulae. These require
another revision, but not a rejection. I would be glad to see the next version.
