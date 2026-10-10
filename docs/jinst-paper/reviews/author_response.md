# Author response to Reviewers 1 and 2

Date: 2026-10-11. Manuscript: *Finite-length and vertical effects in nonlinear-kicker injection into the Korea Light
Source* (revised; previously *Nonlinear-kicker injection into a 4 GeV storage ring*).

I thank both reviewers for their careful reports. The revision follows the
[consolidated plan](consolidated_revision_plan.md) (tasks C1–C12). Where the two reviewers differ, the plan records
which requirement was adopted and why.

**The principal change: a new kicker model.** All revised results use the exact 3-D field of the RADIA filament
geometry, tracked in 640 slices. This model does two things the original thin kick map did not:
- it reproduces the beam's self-deflection inside the magnet;
- it applies the physical vertical kick. Building the model exposed a sign error in the tabulated vertical kick.

**Consequences for the paper:**
- The title and the abstract now state the two physical results that follow from this.
- The operating point, the window, the survival study, the error ensembles and the tolerance curves were all redone
  with the 3-D model.
- Every number in the manuscript is generated from the campaign artifacts by `scripts/build_revision_figures.py`.

**Facility name.** The 4 GeV ring is now named the Korea Light Source (KLS). The lattice file keeps its original
name, `K4GSR_HBIv4-1`.

**Notation in this response:**
- Section (§) and figure numbers refer to the revised manuscript.
- Milestone numbers refer to `docs/exec-plans/completed/`.
- Raw outputs are in `results/journal_campaign_02/` and in the frozen evidence bundle (C11).

---

## Reviewer 1

### M1. One controlled kicker model for the principal conclusions (R1-02)

**Concern.** The thin map and the thick model gave opposite conclusions, the headline used the weaker model, and the
conventions were not audited.

**Action.** I wrote an independent Biot–Savart model of the four filament loops of the RADIA geometry
(`src/nkm_injection/wire_field.py`, 7 tests). Its straight-line integrals reproduce both components of
`kickmap_file.txt` to 7×10⁻¹² rad (4×10⁻¹⁰ relative) on 3657 nodes.

The audit found that the map stores (∫B_y, +∫B_x)/Bρ, which is not curl-free. The physical vertical kick is
−∫B_x/Bρ. The tracker integrates the field in AT canonical coordinates: the drift uses p/(1+δ) and the kick carries no
1/(1+δ) factor.

**Results:**
- Slice and span refinement change the exit angle by less than 7×10⁻¹¹ rad.
- The momentum dependence of the exit angle is 0.12 µrad per 10⁻³ in δ.
- On identical bunches: legacy thin map 91.1 %, sign-corrected thin map 89.7 %, 3-D model 81.8 %.

**Where.** §2.2; table 1; figure 2.

**Evidence.** `docs/jinst-paper/kicker_model_validation.md`; milestone 121.

**Remaining limitation.** The model has no iron, chamber or eddy-current fields and no pulse time dependence (§8). A
1 mm conductor-loss radius is assumed; no particle came within it.

### M2. Demonstrate the mechanism; make the novelty explicit (R1-01, R1-03)

**Action.** Four single-centroid models were compared, each at its own matched angle: thin; the kick profile sampled
on the straight path; the profile sampled on the self-consistent deflected path; and the exact 3-D field.

**Results.**

| Model | Matched angle |
| :--- | ---: |
| Thin | 4.870 mrad |
| Straight path | 4.762 mrad |
| Deflected path | 4.6476 mrad |
| 3-D | 4.6475 mrad |

The deflected-path model reproduces the 3-D field to 10⁻⁷ rad and its angle-error response to 0.01 mm. The
mechanism is therefore the beam's own deflection inside the magnet (sagitta 0.32 mm). It holds the trajectory on the
outer side of the kick extremum.

For a +0.3 mrad error the amplitude change is:
- thin model: +1.22 mm;
- 3-D model: −0.12 mm.

A length scan shows that no matched solution exists for L ≥ 0.75 m.

**Novelty.** The novelty statement and a verified comparison with the closest NLK/MIK systems are in §1 and
`docs/jinst-paper/novelty_and_comparison.md`. The contributions are:
- self-deflection as the finite-length mechanism, with a length trade-off;
- the vertical defocusing hidden by the map's sign;
- transparency as an exact symmetry, with tolerances;
- capture tolerance curves.

**Where.** §1, §3, figure 3.

**Evidence.** `c2_mechanism/finite_length_mechanism.json`; milestones 122 and 123.

### M3. Angular window not measured at the quoted resolution (R1-04)

**Action:**
- A declared 80 % capture threshold.
- A matched-point grid (27 points, 200 particles each) with a selection rule declared before the scan.
- A 0.10 mrad angle scan and a 0.20 mm position scan, each with 1000 particles per value.
- Validation of the selected point on fresh bunches, with paired controls.

**Results.** The selected point is x_inj = −19.5 mm, S = 0.85, x′ = 4.853 mrad.

| Quantity | Value |
| :--- | :--- |
| Validation on fresh bunches (4 × 500) | 93.0 % [91.7, 94.0] |
| Angle window at 80 % | −0.54 ± 0.04 to +0.20 ± 0.03 mrad (width 0.74 mrad, asymmetric) |
| Best capture in the angle scan | 95.1 % at −0.10 mrad |
| Position window | −0.60 to +0.83 mm |

Zero exit angle is therefore close to, but not exactly at, the capture optimum. The grid estimate at the selected
point (92.5 %) is reported separately from the fresh-bunch validation.

**Where.** §4, figure 5.

**Evidence.** `c3_operating_window/`; milestone 125.

### M4. Justify the dominant errors and report actionable tolerances (R1-05, R1-09)

**Action:**
- Table 2 lists every applied error, labelled as an assumption. No component specification exists for the design
  lattice.
- Combined-error ensemble: 3 seeds × 50 realizations with the 3-D NKM and the 3-D-calibrated dipole on identical
  realizations.
- Two treatments of the static transfer-line errors: no orbit correction, and ideal steering at the septum exit that
  removes each perturbed line's static trajectory (the shot-to-shot jitter is kept).
- Paired jitter scaling at 0, 0.25, 0.5, 0.75 and 1 of the assumed jitter, plus position-only and angle-only runs, in
  both treatments. The latent draws are shared across levels.
- Driver ranking by partial rank correlation.

**Results.**

| Quantity | No correction | Ideal static correction |
| :--- | ---: | ---: |
| Mean capture, 3-D NKM (150 realizations) | 40.5 % [35.6, 45.5] | 44.4 % [39.7, 49.3] |
| Mean capture, dipole | 61.4 % | 65.6 % |
| Paired difference (NKM − dipole) | −20.9 [−24.1, −17.7] | −21.2 [−23.9, −18.5] |
| Capture without errors (NKM / dipole) | 92.5 % / 94.5 % | 92.5 % / 94.5 % |
| Booster angle jitter, partial ρ (NKM / dipole) | −0.45 / −0.68 | −0.52 / −0.75 |
| Booster position jitter, partial ρ (NKM / dipole) | not significant | −0.24 / −0.24 |
| Mean capture at jitter 0 / 0.25 / 0.5 / 0.75 / 1 (seed 42) | 58.6 / 58.0 / 55.0 / 51.6 / 46.4 % | 69.7 / 70.0 / 63.6 / 55.8 / 47.3 % |
| Position jitter only / angle jitter only | 55.3 % / 48.1 % | 64.7 % / 52.3 % |
| Median and fraction ≥ 80 % without jitter | 68.2 %, 34 % | 80.0 %, 50 % |

**Conclusions for the tolerances:**
- Booster jitter below a quarter of the assumed amplitude (0.125 mm, 0.05 mrad) costs nothing measurable. The angle
  jitter costs more than the position jitter.
- Without correction, removing the jitter raises the mean only to 58.6 %: the static transfer-line errors displace
  the exit centroid by 0.7 mm rms, more than the position window. Static orbit correction is therefore required.
- Even with correction and without jitter, the mean stays below 80 %. No single static error dominates (all partial
  correlations p > 0.13); the worst realizations combine small kicker, orbit and septum offsets with a kicker-scale
  error. No jitter reduction alone reaches a mean of 80 %.
- A mean of 80 % under this budget therefore needs orbit correction, booster jitter at most a quarter of the assumed
  value, and tighter static tolerances or a wider window, for example from sextupole optimisation for the injection
  DA. The manuscript states this instead of a single jitter requirement.

**Where.** §7, table 2, figure 8.

**Evidence.** `c5_errors_seed*`, `c5c_errors_seed*`, `c5_pooled/`, `c6_jitter_*`, `c6c_jitter_*`; milestones 127
and 128.

**Remaining limitation.** The budget is a design hypothesis, and the correction is ideal. The tolerances are stated
relative to both.

### M5. Survival and physical acceptance at the final point (R1-06)

**Action:**
- 2000-particle bunch.
- 4000-turn survival, about one damping time.
- Loss accounting by location.
- Septum phase-space acceptance diagram.
- Parameterised chamber-aperture scan.
- Uncorrected ring gradient and sextupole errors (10 seeds per level).

**Results:**
- 2000 particles: 92.4 % [91.2, 93.5]. Losses: 17 at the septum on later turns, 135 elsewhere, 0 at creation, 0 in
  the magnet. All categories reconcile with N.
- Survival: 93.0 % at 500 turns, 89.6 % at 2000 and 89.5 % at 4000. The 500-turn capture is about 3.5 points
  optimistic, as the text states.
- Apertures: a ±5 mm half-height costs about 7 points, with or without the NKM vertical kick. The cause is the ring's
  x–y coupling, not the kicker.
- Ring errors (uncorrected):

| Quadrupole σ | Mean capture | Range | DA edge |
| :--- | ---: | ---: | ---: |
| 5×10⁻⁴ | 85.6 % | 77.6–89.6 % | −13 to −11 mm |
| 10⁻³ | 69.9 % | 58–80 % | −12 to −9.5 mm |

**Where.** §5, figure 6.

**Evidence.** `c4_survival/`, `c4_aperture_diag_*`; milestone 126.

**Remaining limitation.** These are bounded sensitivities. The DA of the corrected KLS lattice is required for an
operational estimate (§9).

### M6. Uncertainty floor on the aligned transparency (R1-07)

**Action.** The near-axis kick is odd and cubic. Its coefficient is c₃ = 2.4×10⁴ rad m⁻³, and the bicubic
interpolation error is 9×10⁻¹¹. Beam averages use deterministic Gauss–Hermite quadrature instead of sampling.

**Results:**
- For the aligned kicker the centroid kick vanishes exactly by symmetry. The earlier 5×10⁻⁶ σ was the Monte Carlo
  standard error of the mean.
- With a kicker-to-orbit offset:

| Offset | Amplitude / σ | Δε/ε from the kick spread | Total ε ratio after filamentation |
| :--- | ---: | ---: |
| 0.1 mm | 0.016 | 9.4×10⁻⁵ | 1.000 |
| 0.2 mm | 0.10 | 1.2×10⁻³ | 1.007 |
| 0.5 mm | 1.54 | 4.2×10⁻² | 2.22 |

- Vertical offset of 0.2 mm: 0.17 σ_y (ε_y = 0.1 ε_x assumed).
- The total ratio is 1 + A²/2 + Δε/ε once the centroid oscillation has filamented.
- Multi-turn tracking of the stored beam through the 3-D magnet (300 particles, 6-D with RF and radiation, paired with
  an unperturbed reference): 0.10 σ at 0.2 mm and 1.47 σ at 0.5 mm, with emittance ratios 1.01 and 2.23 after
  1000 turns, in agreement with the single-pass estimates (1.007 and 2.22).
- The control kicks are labelled as hypothetical linear estimates, not surviving oscillations.

**Where.** §6 (transparency), figure 7.

**Evidence.** `c7_transparency/`; milestone 129.

### M7. Pulse physics must match the transparency scope (R1-08)

**Action.** A new pulsed-magnet section derives the requirements from the revolution period (2.666 µs) and the
injected-beam centroid on the following turns.

**Results:**
- The residual kick ratio must be r ≲ 0.19 on turn 1 and r ≲ 0.02 on turn 2.
- The dipole residual at the stored beam must be < 4×10⁻⁵ of the peak kick, and the gradient residual
  < 7×10⁻⁵ of the peak gradient.
- Timing jitter is modelled as a field-scale error, not an additive kick.

**Where.** §8.

**Evidence.** `docs/jinst-paper/pulse_and_timing.md`; milestone 124.

**Remaining limitation.** No pulse or eddy-current simulation was done. The abstract and conclusions claim only
ideal single-pass spatial-field transparency, together with these requirements.

### M8. Balanced statistics and accessible provenance (R1-09, R1-10)

**Action:**
- Every comparison is paired by (seed, sample_id).
- The dipole control was run on all three seeds.
- Intervals are Wilson intervals for particles and cluster-bootstrap intervals for realizations.
- A frozen evidence bundle was built: selected raw outputs, configurations, SHA-256 hashes, environment, code
  snapshot and a rebuild script. Its `--verify` mode rebuilds the macros in a clean directory.
- `figure_provenance.csv` lists the hash of every artifact consumed by each figure.

**Evidence.** `scripts/build_evidence_bundle.py`, `scripts/make_revision_manifest.py`; milestone 131.

**Remaining limitation.** No public DOI yet. It will be created at submission or acceptance, as the author decides
(R2-19).

### Presentation items (R1-11)

| Item | Change |
| :--- | :--- |
| DA "about 12 mm" | Both limits given: −12 to +13 mm (§1, §2.1). |
| Signed peak kick | Table 1 gives the magnitude 4.89 mrad at x = −8.6 mm, with the polarity defined in §2.2. |
| 2.0 m drift vs 2.2625 m | Table 1 states the septum-to-NKM-centre distance as 2.26 m; geometry in figure 2. |
| Mismatch metric | M_x = ½Tr(Σ₀⁻¹Σ) − 1 is defined where it is used (§7.1). The transfer-line tolerance study is condensed to one sentence there. |
| Capture threshold before window | 80 % is declared in §4 before the scan. |
| Figures 5 and 7 (old) | Control amplitudes are separated from transparency; scientific notation is used; the ECDF figure is replaced by figures 7 and 8. |
| "Only 5 … exceeds" | Rewritten as "5 exceed the 60 m β limit", and the limit is defined. |
| Abstract | Reduced to the question, the model, the two effects, the headline capture and the tolerance. |
| "should not be used" | Replaced by the demonstrated validity condition (sagitta ≪ extremum width). |
| JINST formatting | Line numbers added. The AI-assistance disclosure was updated to describe the actual use. |

---

## Reviewer 2

### M1. Inconsistent kicker model (R2-1, R2-2, R2-14)

See R1 M1 and M2. One validated model, the exact 3-D field, is used for the abstract, every figure and the
conclusions.

**Chromatic scaling.** The kick is applied to canonical momentum, so it carries no 1/(1+δ) factor. The drift slope is
p/(1+δ). The residual momentum dependence is 0.12 µrad per 10⁻³ (§2.2). This follows Reviewer 1's distinction; the
consolidated plan records the reasoning.

### M2. Ideal ring (R2-3)

The study is stated as an ideal-lattice design study, and the ring errors and apertures are bounded sensitivities
(R1 M5).

I did not implement ten corrected-orbit error seeds with real chamber apertures. No chamber or misalignment
specification exists for the KLS design lattice, and Reviewer 1 accepts a bounded sensitivity. Gradient and sextupole
errors need no orbit correction; their DA reduction and capture are reported per seed.

### M3. Tracking duration (R2-4)

See R1 M5. Survival over 4000 turns (about one damping time) saturates by turn 2000 at 89.5 %. The survival curve versus turn is in figure 6 (right).

### M4. Dominant error assumed; one amplitude only (R2-5, R2-6)

See R1 M4. Tolerance curves are given against booster jitter scale (mean, 10th percentile, bootstrap band), against
NKM–orbit offset (87.0–93.6 % within ±0.6 mm) and against injected emittance (98.9 % at 25 nm rad, 81.1 % at
200 nm rad). The jitter curves are given with and without ideal static orbit correction. Jitter below a quarter of
the assumed amplitude costs nothing; no jitter reduction alone reaches a mean of 80 %, which in addition needs orbit
correction and tighter static tolerances or a wider window (§7.2).

Every σ in table 2 is labelled "assumed": no measured booster data exist for this design. The bibliography audit
records which published values informed the choices.

### M5. Pulsed-magnet aspects (R2-7)

See R1 M7.

### M6. Near-axis transparency rests on interpolation (R2-8)

See R1 M6. The exact field and a multipole fit replace interpolation, and both the vertical response and multi-turn
tracking are included.

### M7. Window definition and resolution (R2-9)

See R1 M3:
- an 80 % threshold;
- resolution 0.10 mrad, with crossings interpolated to ±0.04 mrad;
- a septum phase-space acceptance diagram (figure 6, left), with the blade and the 1σ and 2σ beam ellipses;
- a test of zero exit angle, which is not optimal: the best capture is at −0.10 mrad.

### M8. Positioning against prior work (R2-10, R2-15)

`novelty_and_comparison.md` and §1 compare with the KEK-PF, BESSY II, MAX IV, SOLEIL and SIRIUS pulsed-multipole
systems. I verified every reference (`bibliography_audit.md`). Four were added: Kallestrup 2019, Alexandre 2021,
Velloso 2023 and Elleaume 1992.

Following Reviewer 1, I set no target count. The facility is named (KLS), and the lattice file is identified.

### Minor comments

| ID | Response |
| :--- | :--- |
| m1 | Table 1 (ring, booster beam, BTS, septum, NKM) and table 2 (errors) added. |
| m2 | Figure 2: NKM cross-section with wires, field lines and \|B\|, plus the kick profile. |
| m3 | See M1 (canonical kick; drift corrected; effect 0.12 µrad per 10⁻³). |
| m4 | Particles, turns, apertures and loss accounting are now checked at the operating point (§5). The backend comparison stays at the provisional point and is labelled as such (figure 3). The backend conclusion (native vs linear map) does not depend on the point. |
| m5 | The transfer-line tolerance study is condensed to one sentence in §7.1; the prefix-stability and failure statistics stay in the supporting documents. |
| m6 | Dipole control on all three seeds (150 paired realizations). |
| m7 | The figure was rebuilt as figure 1 (DA in x–δ and x–x′); its legend and band overlap are gone. |
| m8 | Scientific notation throughout; reference stated. |
| m9 | The ECDF figure was replaced: controls are in figure 7 and ensembles in figure 8 (two series, distinct colours). |
| m10 | Abstract shortened to the key numbers. |
| m11 | "Capture" defined in §2.3 before first use; M_x defined where it is used (§7.1); σ notation throughout. |
| m12 | The JINST class is kept because the journal is undecided. The bibliography style will be converted with the journal choice (JHEP.bst for JINST). |
| m13 | The evidence bundle is available to referees. A DOI is an author action at submission. |
| m14 | Partial rank correlations, controlling for all other sampled errors, replace the marginal ranking. |

### Questions

1. **Pulse length.** The pulse length is not yet specified. §8 states the requirement instead: residual kick below
   0.19 (turn 1) and 0.02 (turn 2) of the peak.
2. **Is the −9 mm centroid inside the chamber?** The chamber is not specified, so the stay-clear was scanned (§5).
   Capture falls steeply below a 12 mm half-width: 83.8 % at 12 mm, 76.0 % at 11 mm, 47.9 % at 10 mm. At a 15 mm
   half-width the residual loss is vertical, and a 10 mm half-height restores it.
3. **Source of the 9 % loss.** At the selected point the loss is about 7 %, nearly all in the ring after the first
   turn: 135 of 152 losses at 2000 particles. 17 are lost at the septum on a later turn and none at creation. The
   energy-tail contribution was not separated.
4. **Sextupoles.** They are the bare design configuration, not optimised for injection DA (§2.1, §9).

---

## Acceptance checklist (C12)

| Condition (Reviewer 1 §5) | Status |
| :--- | :--- |
| Novel physical result with a controlled model and validity range | Self-deflection mechanism and vertical defocusing; validity condition sagitta ≪ extremum width; model validated to 10⁻¹⁰ |
| Threshold-defined, independently checked operating region | 80 % threshold, declared selection rule, fresh-bunch validation |
| Survival and acceptance at that region | 4000 turns, 2000 particles, acceptance diagram, apertures, ring-error bounds |
| Actionable sensitivity to parameterised errors | Jitter (with and without orbit correction), offset and emittance tolerance curves; conditions for 80 % stated |
| Defensible stored-beam response | Exact symmetry; deterministic quadrature; offset tolerances; tracked check |
| Balanced paired comparisons | All comparisons paired; dipole on all seeds |
| Frozen evidence package | Evidence bundle with `--verify` rebuild |
| Abstract, figures and conclusions on one model | All macros generated from the revision manifest; build gated by `--require-all` |
| Full test suite | 663 tests pass |

Open items for the author:
- choose the journal (R2-19, R2-20) and convert the template and bibliography style;
- create a DOI;
- confirm the AI-assistance disclosure.
