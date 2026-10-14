# Response to the third-round reviews

These were pre-submission assessments, not journal editorial decisions. This response addresses:
- Reviewer 1's R1C-01 to R1C-08 ([report](reviewer1_round3_20261012_report.md));
- Reviewer 2's R2c-1 to R2c-9 ([report](reviewer2_report_round3.md)).

It follows the consolidated plan [E1–E11](consolidated_revision_plan_round3.md). Earlier reports, plans and responses
remain unchanged. The study is simulation-only and conditional on the supplied KLS design lattice, the declared
chamber and error budget, and ten corrected rings.

**Evidence entry points:**
- [manuscript PDF](../paper.pdf) and [Supplemental Material](../supplement.pdf);
- [round-3 manifest](../revision_manifest_round3.json) and [claim table](../claim_evidence.csv), rows E0–E11;
- [reproduction instructions](../round2_reproduction.md), round-3 section;
- milestones 211–222 in the [completed-task index](../../exec-plans/completed/README.md).

## Main changes and what they changed in the conclusions

| Item | Change | Effect |
| :--- | :--- | :--- |
| Positioning | Segmented and finite-conductor NLK tracking credited to Sun et al. (2020). The contribution is restated as a quantified thin-map error. | No claim of method novelty. |
| Scaling | Normalised thin-map error ∝ η^1.46 over both wire families (3.4 % scatter). The sliced map stays below 2×10⁻⁵ of the kick. | At the selected point the thin-map error is 155 % of a declared allowance of one tenth of the window. |
| NKM chamber | A flat 16 × 3.8 mm chamber inside the magnet, below the wires, applied every turn. | Tightest vertical restriction with open IVUs. Not limiting on the ideal ring. |
| Corrected rings | BPM references, converged orbit, β-beat/dispersion and tune correction. | β-beat ≤ 2 %. Ring 5501 recovers (−7.5 → −10.5 mm). |
| Operating point | Re-selected for the design beam on the corrected rings: x_inj −19.48 mm, S 0.95. | Corrected-ring mean 78.0 % (68.9 % at the old point). Windows 0.44 mrad / 2.40 mm. |
| Robustness | One rerun with all of the above; ring-cluster intervals; matched-knob tuning. | NKM 16.1 % against dipole 44.1 % under joint errors. Booster angle jitter dominates. |
| Synthesis | Hierarchy table and ring-level correlates. | Ring errors cost both kickers alike. The NKM-specific loss is injection angle error on a narrow window. |
| Transparency | Δε/ε units; a simultaneous wire/current Monte Carlo; the septum-leakage allowance. | Compensation required; septum leakage of order 0.07 G. |
| Presentation | Supplemental Material (tables, larger-emittance case, statistics, procedures). | Both layouts build clean. |

## Reviewer 1

**R1C-01 — Evidence access** (E1, milestone 211).
- The round-2 attachment (`round2_evidence_bundle.tar.gz`, SHA-256 `0e07de5f…3f3d`) was re-verified: all 213
  inventory entries.
- An isolated rebuild from the archived source on the bundled evidence alone reproduces the manuscript macros byte
  for byte.
- The access route and commands are in `round2_reproduction.md`. The round-3 evidence has its own bundle (R1C-08).

**R1C-02 — Contribution against the overlapping literature** (E2, milestone 212).
- Sun et al. (PRAB 23, 010702, 2020) is read and cited. They established, for an eight-conductor ALS NLK:
  - segmented drift–kick–drift tracking with a Runge–Kutta reference;
  - a finite 3-D conductor model with return loops, finding small fringe-field effects on efficiency.
- The manuscript claims neither tool. Its contribution is the quantified approximation error of a single thin map in
  an angle-cancelling geometry, where the sagitta (0.32 mm) is a few percent of the kick-lobe width. The ALS sagitta,
  about 0.04 mm, is an order of magnitude smaller, which is consistent with their finding; no inadequacy of their model
  is implied.
- The comparison table gains an ALS row.

**R1C-03 — What the sagitta ratio predicts** (E3, milestones 213 and 218).
- K, w, the reference path (chord through the extremum) and the launch recipe are defined in the main text.
- Normalised by |K|, the thin-map horizontal error follows 1.95 η^1.46 over 30 configurations, with 3.4 % log-rms
  scatter. The two families give exponents 1.47 and 1.45.
- The vertical error organises less tightly (η^0.81, 7 %).
- A declared allowance of one tenth of the angular window gives η* = 0.025 at the selected point. The nominal magnet
  (η = 0.034) exceeds it.

**R1C-04 — Robustness hierarchy and physical synthesis** (E8, milestone 221). Table V lists the capture of the
selected point as conditions accumulate, with populations stated:

| Condition | NKM | Dipole |
| :--- | ---: | ---: |
| Ideal ring, 500 / 4000 turns | 98.4 / 97.8 % | 100 % |
| Corrected rings, no injection errors | 78.0 % | 82.2 % |
| Joint errors, no booster jitter | 40.1 % | 68.5 % |
| Joint errors, full budget | 16.1 % | 44.1 % |

Rows are not subtracted as paired effects. The physical lesson:
- **Corrected ring errors** cost both kickers alike. They follow the residual chromaticity and β-beat (ρ = −0.68 and
  −0.58 for the NKM; −0.65 and −0.54 for the dipole; ten rings), not the on-axis DA margin (ρ = −0.23 over 400 pairs).
- **The NKM-specific loss** comes from injection errors, chiefly booster angle jitter (the only Holm-significant
  driver, ρ = −0.38), acting on its 0.44 mrad angular window.
- **The 20 µm target** and the round-2 100 µm scenario stay documented. The round-3 orbit floor (69–83 µm with
  unsaturated correctors) is attributed to the 120-corrector file, not to a stopping rule.

**R1C-05 — Units of the moment changes** (E9, milestone 215). Section 6 now writes the aligned changes as fractional
Δε/ε (4.5×10⁻⁷, 1.6×10⁻⁷), from the kick spread alone. They are distinct from the filamented coherent growth and the
tracked turn-1000 ratio. The wire and current limits remain single-error sensitivities, and the new simultaneous-error
Monte Carlo is reported separately.

**R1C-06 — Noninferiority wording** (E8 and E10).
- The margin test is called a one-sided noninferiority test against the *declared* 1-point analysis margin in the
  manuscript, the Supplemental Material (S4), the method notes and this response. "Predeclared" is withdrawn.
- At the selected point, quarter jitter costs a resolved −5.7 [−9.4, −2.5] points and fails the test.

**R1C-07 — Streamlined article** (E10, milestone 219). The following moved to a compiled 6-page Supplemental
Material:
- the trajectory-check table;
- the wire and loop tables;
- the larger-emittance case;
- the statistical definitions and the procedures.

The main text keeps the chain from mechanism through accuracy, chamber, robustness hierarchy and transparency.

**R1C-08 — Final reconciliation and new response** (E11, milestone 222).
- Claim rows E0–E11, an updated cover letter, the round-3 manifest (all 37 round-2 builder keys re-pointed to
  campaign-04 runs, none missing), and both PRAB layouts with the supplement.
- A new frozen round-3 bundle, verified by archived-source rebuild.
- The full test suite.
- Earlier responses are unchanged.

## Reviewer 2

| Task | Change and evidence | Result and remaining scope |
| :--- | :--- | :--- |
| R2c-1 NKM chamber | Flat 16 × 3.8 mm chamber below the wires (1.5 mm wall-plus-conductor allowance, as for the ALS NLK), checked per slice and on every turn; wire-clearance validation; table 1 corrected; eddy estimate for a 3.8 mm half-gap (milestone 214). | Normalised vertical aperture 1.61 mm m^-1/2, the tightest with open IVUs. Capture is unchanged for 3.0–4.3 mm half-heights on the ideal ring; the concern is answered there. |
| R2c-2 Ring population | Same ten error draws with BPM references (10 µm residual), converged SVD orbit, β-beat/dispersion correction with individual quadrupoles, tune correction; ring 5501 diagnosed (milestone 216). | β-beat ≤ 2 %, NKM orbit ≤ 56 µm. Ring 5501's collapse was uncorrected optics. No skew correctors exist, so coupling is not corrected (stated). |
| R2c-3 Operating point | Declared rule: 3σ clearance, matched-angle knobs, p10 objective over the corrected rings, both blades; fresh validation (milestones 217–218). | x_inj −19.48 mm, S 0.95; corrected-ring mean 78.0 % against 68.9 % at the old point. The gain comes from a smaller injected amplitude via kick strength; **moving toward the septum did not help**, and the 1 mm blade gives about the same. |
| R2c-4 Rerun | One rerun of the joint ensembles, jitter scan and tuning with unchanged populations (milestone 220). | NKM 16.1 % [ring-cluster 10.9–21.5], dipole 44.1 %. Matched tuning +11.9 points; 28 % of the machines end on the *outer* x_inj bound. |
| R2c-5 Synthesis | Hierarchy table, margin test, ring-level correlates (milestone 221). | The single-parameter DA-margin hypothesis is **not** supported. The decisive requirement is the angular stability of the injected beam. |
| R2c-6 Simultaneous wire errors | 4000-draw Monte Carlo at 10/25/50 µm and series or independent loops (milestone 215). | Median A/σ of 2.6 (x) and 4.8 (y) already at 10 µm; compensation required (stated in the abstract and conclusions). No compensation design. |
| R2c-7 Septum leakage | Allowance for 0.1 σ_x at the septum (β_x 15.9 m): 197 nrad, i.e. 0.066 G over 0.4 m (milestone 215). | 50 times below the published bumped-orbit value. A distance-resolved field at the NKM-scheme orbit is not published, so this is stated as a requirement. |
| R2c-8 Ring dependence | Ring-cluster bootstrap and leave-one-ring-out ranges; paired NKM − dipole robust difference (milestone 220). | −28.0 [−32.5, −23.5] points. |
| R2c-9 Minor | Open-IVU half-gap justified against the sourced 8 mm (both ≥ 4.2 mm m^-1/2 normalised); population wording in the abstract; conductor rule replaced by the chamber; wire-table formatting (milestones 214, 219, 221). | — |

Two of Reviewer 2's round-3 expectations were not borne out, and the manuscript reports the evidence as found:
- the operating-point gain did not come from the septum position;
- capture is not organised by the DA margin.

The robustness of the NKM under the assumed budget remains low, and the paper states its cause.

## Final verification

The test count, build outcome and bundle hash are recorded in the
[E11 completion record](../../exec-plans/completed/222_e11_final_reconciliation.md).
