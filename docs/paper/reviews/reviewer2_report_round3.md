# Referee report — Reviewer 2, third round

**Manuscript:** "Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design
lattice" (C. S. Park), PRAB REVTeX version.
**Version reviewed:** `docs/paper/paper.tex` and `paper.pdf` at commit `139c7c7`: 28-page one-column preprint
(14 pages two-column), 11 figures and 7 tables. SHA-256 prefixes: paper.tex `94a9728f1c9c576a`, paper.pdf
`5be00c58322e06c1`.
**Also read:**
- the round-2 response (`author_response_round2.md`);
- the author inputs (`../dependent_answers.md`);
- the third-round Reviewer 1 report and register (`reviewer1_round3_20261012_*`);
- the campaign-03 artifacts.
**Date:** 2026-10-13.
**Reviewer expertise:** storage-ring beam dynamics, off-axis and multipole-kicker injection, transfer-line design,
pulsed-magnet modelling.

## Recommendation

**Major revision, focused on the robustness study. I do not recommend acceptance of the present version.**

The second revision is thorough and honest:
- the design booster beam replaces the 100 nm rad assumption;
- the chamber is declared from KLS sources;
- ten corrected-error rings, held-out tuning, paired jitter statistics and two-plane wire/current tolerances are added;
- the transparency, pulse and septum statements are now correctly scoped.

Every one of my round-2 tasks received a substantive answer (table below), and I do not reopen them.

The revision, however, produced a new headline that changes the paper's message: a joint-error mean capture of
14.8 %, a median of 1.0 % and a tenth percentile of 0 %. The ring-only mean is 61.7 %. From the campaign-03
artifacts, I find that this collapse is not an intrinsic property of the nonlinear kicker. It comes from three
modelling choices made during the revision:

1. **The operating point was not re-selected for the design beam.**
2. **The "corrected" rings stop correcting at a 100 µm rms criterion and receive no optics correction.**
3. **The assumed NKM chamber is incompatible with the magnet's own conductor geometry.**

The uniform-dipole control collapses in the same way (mean 22.5 %, median 7.8 %), which supports this reading. As
the robustness section stands, it characterises an unoptimised injection into an under-corrected ring, and the abstract
and conclusions inherit that. These points can be fixed with existing tools, and the paper's physics core (sections
3–4, the trajectory validation, the transparency analysis) is sound.

**Evidence access.** Reviewer 1 (round 3) could not find the campaign-03 evidence. In this checkout, all 205 artifacts
of `revision_manifest_round2.json` are present and match their SHA-256 hashes. `round2_evidence_bundle.tar.gz` matches
the D13 record (`0e07de5f…3f3d`). R1C-01 can therefore be closed by documenting the access route; no regeneration is
needed.

## Status of my round-2 tasks

| Round-2 task | Status | Comment |
| :--- | :--- | :--- |
| R2b-1 chamber | **Addressed, with a new defect** | Arc and centre-bend apertures follow KLS sources; loss map and aperture scan are given. The NKM-straight aperture is not physically possible (M3). |
| R2b-2 corrected ring seeds | **Addressed in form, not in substance** | Ten seeds with misalignments and SVD correction exist, but correction stops after 1–2 iterations at 66–85 µm rms, with no optics or coupling correction (M2). |
| R2b-3 manufacturing tolerances | **Addressed** | Two-plane wire and loop sensitivities; limits of 0.29–2.04 µm per wire. See M5 for what this now implies. |
| R2b-4 pulse | **Addressed** | Peak phase, return fractions, 5.33 µs no-return limit and timing formulas are consistent. |
| R2b-5 beam-based tuning | **Addressed as a reduced study** | One coordinate step per knob. The result itself shows the optimum lies outside the explored range (M1). |
| R2b-6 budget sources | **Addressed** | Design emittance and energy spread are cited; every other term is labelled with its reason. |
| R2b-7 lattice identity | **Addressed** | Title and text say "design lattice"; the NKM is a preliminary study design. |
| R2b-8 generality | **Addressed for the declared scope** | Reviewer 1's C4 (normalised error) is the remaining refinement. |
| R2b-9 survival / backend | **Addressed** | |
| R2b-10 inference | **Addressed** | See m6 on ring clustering. |
| R2b-11 comparison table | **Addressed** | The "This study" aperture entry inherits M3. |
| R2b-12 septum leakage, coupling, quadrature | **Addressed as estimates** | See M6. |
| R2b-13, 14 presentation and parameters | **Addressed** | |
| R2b-15 format and access | **Addressed** | REVTeX 4.2 builds; the bundle verifies (see above). |

## Major comments

**M1. The operating point was selected for the 100 nm rad beam and not re-selected for the design beam.**
Section 4 states that the point (x_inj = −19.5 mm, S = 0.85, x′ = 4.853 mrad) "was selected … using a 100/10 nm rad
sensitivity beam" and that the design-beam studies "retain these knobs without reselection". The septum geometry
explains why this matters:
- The blade's outer edge is at −18.0 mm (stored-beam edge −16 mm, blade 2 mm), so x_inj = −19.5 mm leaves 1.5 mm of
  clearance.
- With the 100 nm beam, σ_x at the septum is 0.49 mm (β_x = 2.34 m, D_x = 0.081 m, σ_δ = 1.06×10⁻³), so 1.5 mm is a
  3σ clearance and a sensible choice.
- With the 7.67 nm rad design beam, σ_x = 0.16 mm, and the same point keeps 9.4σ of clearance.
- A 3σ clearance would allow x_inj ≈ −18.5 mm, about 1 mm closer to the stored beam, with a correspondingly smaller
  injected betatron amplitude.
- The KLS baseline thin septum has a 1 mm blade (Hahn et al. 2024), not the assumed 2 mm, which would allow about
  another millimetre.

The authors' own held-out tuning confirms the direction. The single coordinate sweep tried one 0.5 mm step toward the
blade, and **33 of the 50 machines accepted x_inj = −19.0 mm** (`d8_tuning/tuning_*.json`). That was the only step
tried in that direction, so the optimum lies beyond the explored range. The sweep also changes x_inj at fixed angle,
which mismatches the trajectory. The physically sensible knob is x_inj with the angle re-matched.

Because the corrected-ring DA margin is below 1 mm (M2), a 1–2 mm reduction of the injected amplitude is decisive,
not cosmetic. Required:
- **(a)** Re-select the operating point with the design beam, under an explicit septum clearance rule (e.g. nσ of the
  design beam), for the assumed 2 mm blade and for the KLS 1 mm blade.
- **(b)** Use a robustness-aware objective: mean or tenth-percentile capture over the corrected-ring population, not
  ideal-ring capture.
- **(c)** Parametrise the injection knob as (x_inj, re-matched x′) plus S.

**M2. The "corrected" ring population is defined by a stopping rule, and it sets the robustness headline.**
From `d5_selected_scenario/seed55*.json`:
- **Orbit correction.** The SVD correction runs for 1–2 iterations and stops once the BPM rms falls below the
  100 µm criterion. Final residuals are 66–85 µm horizontal and 47–56 µm vertical. The text reports that a 20 µm
  target "was not attained", but the record shows that it was not attempted to convergence.
- **No optics or coupling correction.** Only the Q11/Q12 tunes are trimmed, so β_x at the NKM ranges from 15.1 to
  17.7 m (16.27 m design, up to +9 %) and α_x from −0.08 to −0.26.
- **Orbit at the NKM.** The closed orbit at the NKM reaches −103 µm, half of the 0.2 mm transparency scale of section 6.
- **Dynamic aperture.** The first unstable horizontal point is −9.0 to −10.0 mm for nine rings and −7.0 mm for
  ring 5501. Ring 5501 captures 2.7 %, the others 57–87 %. Without ring 5501 the ring-only mean is 68.3 %, not 61.7 %.

The physical synthesis is therefore simple. In these rings the injected betatron amplitude at the NKM (about
9.5 mm; 9.57 mm at the −20 mm diagnostic launch) sits at or beyond the first unstable point. Capture is decided by a
sub-millimetre margin between the injected amplitude and a DA reduced by uncorrected optics. The NKM nonlinearity
plays a secondary role: the dipole control also drops to 22.5 % mean and 7.8 % median.

In current fourth-generation commissioning simulations, an orbit corrected to tens of micrometres or better followed
by optics (LOCO-type) and coupling correction is the standard chain. The cited KLS lattice paper (Kim et al., IPAC'25)
reports commissioning simulations with optics correction. Required:
- **(a)** Iterate the orbit correction to convergence, include all available correctors (state whether the KLS design
  has more than the 120 HVC elements in this file, e.g. sextupole trim windings), and add β-beat and coupling
  correction. Report the achieved residuals, and compare them with the KLS commissioning simulations, or use their
  seeds.
- **(b)** Diagnose ring 5501 (DA −7.0/+7.5 mm): is it a resonance, a correction failure or a genuine outlier?
- **(c)** If a full chain is not undertaken, rename the population "partially corrected (orbit only, 100 µm criterion)"
  in the abstract, the figures and the conclusions. Add the sentence that the robustness results are dominated by the
  DA margin of that population.

**M3. The assumed NKM chamber is physically incompatible with the NKM conductors.**
Table 2 and section 5 assume an NKM-straight half-aperture of 30 × 15 mm, and the comparison table lists "60 × 30
assumed". The inner wires sit at (±5.3, ±5.3) mm and the outer wires at (±10.25, ±10.25) mm. A 30 × 15 mm chamber
would contain all eight conductors. In wire-type NLK/MIK designs the conductors lie outside a flat chamber, as at
BESSY II (42 × 10 mm) and SOLEIL (46.8 × 7.8 mm), the systems compared in table 1.

Here the inner wires limit the full vertical aperture to less than about 10.6 mm minus conductor radius and wall,
i.e. a half-height of at most about 4.3 mm with the model's 1 mm conductor exclusion, and less with a ceramic wall.
Normalised by √β_y:

| Location | Half-height | β_y | Normalised aperture (mm/√m) |
| :--- | ---: | ---: | ---: |
| Arc (worst) | 9 mm | 24.9 m | 1.80 |
| Centre bend | 4.87 mm | 3.41 m | 2.64 |
| NKM, half-height ≤ 4.3 mm | ≤ 4.3 mm | 5.6 m | ≤ 1.82 (~1.3 with a 1 mm wall) |
| NKM, assumed | 15 mm | 5.6 m | 6.3 |

With a feasible chamber, the NKM is therefore among the tightest vertical restrictions in the ring. It sits exactly
where the injected beam's large horizontal oscillation transfers into the vertical plane (section 5). The current model
only removes particles within 1 mm of a wire, which is not a chamber. Required:
- **(a)** Define a feasible NKM chamber consistent with the wire positions: flat, conductors outside, with a stated wall
  thickness. Apply it to the capture, window and robustness studies.
- **(b)** Correct table 1 accordingly.
- **(c)** Use the same chamber in the eddy-current and coating estimates of section 8, which currently use a
  hypothetical a = 15 mm shell.

**M4. Rerun the robustness study once, after M1–M3, and rewrite its interpretation.**
The final joint-error ensembles (section 7.2), the jitter table and the tuning study all depend on M1–M3. Rerun them
once with the re-selected point, the improved ring population and the feasible NKM chamber. Then replace the list of
qualifications in the discussion by the physical synthesis (DA margin versus injected amplitude; NKM versus dipole).
This coincides with Reviewer 1's R1C-04 (robustness hierarchy), which should be executed on the new results rather
than the current ones.

If the robust capture remains low after M1–M3, that is a legitimate and publishable conclusion for this lattice.
The paper should then state its cause and the DA margin needed. A useful result would be the required DA, or the
injected amplitude, for a stated capture target, obtained by scanning the DA margin.

**M5. Transparency: the tolerance result now says the ideal-symmetry concept needs compensation.**
The new tables are a real improvement. The one-error-at-a-time 0.1σ limits are 0.29–2.04 µm per wire, and 1.1×10⁻⁴
for independent loop currents. These are one to two orders of magnitude below achievable conductor placement. SOLEIL's
MIK needed active compensation (Ollier et al. 2023, cited in the paper). The discussion should draw the consequence:
- for a magnet built to realistic tolerances (e.g. 10–50 µm placement), the expected residual dipole in both planes
  is far above 0.1σ;
- transparency then rests on a compensation scheme (trim coil, beam-based shimming, a pulsed dipole corrector) whose
  requirements follow from the tables.

A short Monte Carlo of simultaneous wire errors at two or three placement tolerances, giving the distribution of A_x
and A_y, would turn the tables into a design statement. This is strongly recommended (B), not required, if the
qualification is stated in the abstract and conclusions.

**M6. Septum leakage dominates the system-level disturbance estimate and needs a distance-resolved number.**
Section 6 estimates an "order-five-σ_x" response from the published bumped-orbit leakage (3.3 G at about 5 mm from the
blade). In the NKM scheme the stored beam sits about 16 mm from the blade, where the leakage is much smaller. The cited
source (Hahn et al. 2024, fig. 8) gives the leakage profile. Please evaluate the leakage at the NKM-scheme stored-orbit
distance, or state the shielding factor needed. Otherwise the paper's own estimate implies that the septum, not the
NKM, decides transparency by an order of magnitude.

## Minor comments

- **m1. Abstract and conclusions.** State the population definition next to the robustness numbers: "orbit-only
  correction to 100 µm rms, ten seeds". Also state the operating-point provenance (selected with the 100 nm beam), or
  update both after M1–M2.
- **m2. Open-IVU gap.** The reference "open" IVU half-gap is 9 mm. The cited impedance study (Seok et al. 2024) models
  open IVUs at a 16 mm full gap, i.e. 8 mm half-gap. Use the sourced value, or state the reason for 9 mm.
- **m3. Conductor-loss rule.** "Particles within 1 mm of a conductor are counted as lost" should be replaced by the
  chamber of M3, or kept only as a secondary check.
- **m4. Comparison table.**
  - The aperture of "This study" should be the feasible chamber (M3).
  - The efficiency column should add the robust capture next to the nominal 97 %, as for SIRIUS (simulated versus
    measured).
- **m5. Tuning description.** Report the distribution of the selected knobs, as in M1, and give the fraction of
  machines whose optimum lies at a sweep boundary. That fraction is the diagnostic of an insufficient search range.
- **m6. Ring clustering.** Joint draws sample the ten rings with replacement, so the realization bootstrap interval of
  the mean (11.2–18.8 %) treats ring identity as fixed. Add a ring-cluster bootstrap, or the leave-one-ring-out
  range (ring 5501 alone moves the ring-only mean by 6.6 points), so that readers can see the population dependence.
- **m7. NKM–dipole robust comparison.** Quote the paired NKM − dipole robust difference (14.8 versus 22.5 % mean) and
  interpret it. It is the cleanest measure of what the NKM nonlinearity costs under errors, as distinct from what the
  ring costs.
- **m8. Table formatting.** The wire-sensitivity table prints "−0.000" and "+0.000". Use a consistent number of
  significant digits or scientific notation.

## Questions to the author

1. Does the KLS correction system include correctors beyond the 120 HVC elements of `K4GSR_HBIv4-1`, for example
   sextupole trim windings? What orbit and β-beat residuals do the KLS commissioning simulations reach?
2. What vacuum chamber is envisaged inside the four-loop NKM: material, inner height and wall thickness?
3. Is the 2 mm septum blade of the NKM scheme a deliberate choice? Could the NKM scheme use the KLS 1 mm in-vacuum
   thin septum?
4. With the design beam, what septum clearance in σ_x would the KLS injection group accept?

## Revision tasks (for the author)

Priority: **A** = required for acceptance, **B** = strongly recommended, **C** = editorial. "Sim" = new simulation.

| ID | Priority | Task | Sim | Acceptance criterion | Est. effort |
| :--- | :---: | :--- | :---: | :--- | :--- |
| R2c-1 | A | Feasible NKM chamber consistent with the wire geometry (flat, conductors outside, stated wall); apply it to the chamber, window and robustness studies; correct table 1 and the section 8 eddy/coating estimate. | yes | Chamber defined and justified; NKM normalised vertical aperture reported; results rerun | 1 d plus compute |
| R2c-2 | A | Ring population: orbit correction to convergence with all available correctors, plus β-beat and coupling correction; residuals compared with the KLS commissioning simulations or their seeds; ring 5501 diagnosed. Otherwise relabel the population as "partially corrected" everywhere. | yes | Residuals and DA per seed; population definition in the abstract | 2–4 d |
| R2c-3 | A | Re-select the operating point with the design beam, an explicit septum clearance rule (2 mm and 1 mm blade), matched-angle knob parametrisation and a robustness objective over the ring population. | yes | New operating point with its selection rule; design-beam window recomputed | 1–2 d plus compute |
| R2c-4 | A | Rerun the final robustness study once after R2c-1 to R2c-3 (joint ensembles, jitter table, tuning with matched knobs and an adequate range). | yes | Section 7.2 regenerated; tuning optimum not at a sweep boundary | ~1 d compute |
| R2c-5 | A | Physical synthesis of robust capture: DA margin versus injected amplitude, NKM versus dipole under errors, and the required DA margin or amplitude for a stated capture target. Execute together with R1C-04. | small | Discussion states the limiting mechanism with supporting data | 1 d |
| R2c-6 | B | Simultaneous wire-placement and current-error Monte Carlo at 2–3 tolerances; A_x and A_y distributions; compensation requirement. | small | Distribution figure or table; consequence stated in the abstract and conclusions | 1 d |
| R2c-7 | B | Septum leakage at the NKM-scheme stored-orbit distance, from the published leakage profile, or the required shielding factor. | no | Distance-resolved estimate replaces the bumped-orbit scale | 0.5 d |
| R2c-8 | B | Ring-cluster bootstrap or leave-one-ring-out range for every population mean; paired NKM − dipole robust difference. | no | Intervals reflect ring-population dependence | 0.5 d |
| R2c-9 | C | Open-IVU half-gap from the source (8 mm) or justified; abstract population wording; conductor-loss rule; table number formatting. | no | Text and table | 0.5 d |

**Suggested order:**
1. R2c-1 (chamber) and R2c-2 (ring population), which fix the model.
2. R2c-3 (operating point on that model).
3. R2c-4 (one rerun).
4. R2c-5 together with R1C-04 (synthesis).
5. B and C items in parallel.

**Coordination with Reviewer 1, round 3:**
- **R1C-01 (evidence).** Close it by documenting the access route; the bundle verifies.
- **R1C-02 (literature, Sun et al. 2020) and R1C-03 (normalised scaling error).** Independent of these tasks; they can
  proceed now.
- **R1C-04 (hierarchy).** Should use the R2c-4 results.
- **R1C-05 to R1C-08.** Editorial, after the rerun.

## Choice of journal

PRAB remains appropriate. Its referees will judge whether the finite-length comparison adds to Sun et al. (2020),
which is Reviewer 1's C1, and whether the robustness conclusion is a property of the scheme or of the modelling
choices, which is this report. A design-study paper whose robustness section reports a 1 % median capture without
identifying the cause would be returned on that point at any of the candidate journals.

## Confidential comments to the editor

The core finite-length analysis is careful, independently validated and now properly scoped, and I would like to see
it published. My concerns are confined to the robustness section introduced in this revision. I checked them directly
against the campaign-03 artifacts:
- the correction stops after 1–2 iterations at 66–85 µm;
- β_x at the NKM varies by up to 9 %;
- the tuning moved toward the septum in 33 of 50 machines;
- the NKM chamber encloses its own conductors.

All four are fixable with the existing tools. After those changes, and Reviewer 1's literature positioning, I expect
to be able to recommend acceptance.
