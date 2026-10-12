# Response to the second-round reviews

These were pre-submission assessments, not journal editorial decisions. This response addresses Reviewer 1's R1B-01–R1B-10 and Reviewer 2's R2b-1–R2b-15 under the adopted D1–D14 plan. The first-round response and both original review reports remain unchanged. The study is simulation-only and conditional on the supplied KLS design lattice, declared chamber, finite corrected-ring population and assumed error budget.

Evidence entry points: [manuscript PDF](../paper.pdf), [round-2 manifest](../revision_manifest_round2.json), [claim table](../claim_evidence.csv), [reproduction instructions](../round2_reproduction.md), and [completed-stage index](../../exec-plans/completed/README.md).

## Main changes

- The design booster beam replaces the 100 nm sensitivity beam in the headline, chamber, window and final robustness studies. The retained larger-emittance diagnostics are labelled by their beam and aperture assumptions.
- The chamber follows the author-verified arc and centre-bend dimensions, with explicit assumptions for the unknown NKM chamber and IVU assignments. Ten saved corrected rings supply the finite ring-error population.
- Independent trajectory integration, finite-turn survival, paired jitter intervals, held-out tuning and two-plane wire/current tolerances replace unsupported general claims.
- The manuscript now distinguishes ideal centroid symmetry, finite-beam moments and full-system transparency. Septum leakage, coating and pulse calculations are conditional estimates.
- A new manifest, claim table and frozen evidence bundle provide the numerical provenance and a verified figure/macro rebuild.

## Final numerical results

| Observable | Result |
| :--- | :--- |
| Nominal design-beam survival, 500 / 4000 turns | 97.0% / 96.1% |
| Joint-error NKM mean, 150 draws | 14.8% [11.2, 18.8] |
| Quarter-minus-zero jitter, 50 paired draws | +2.2 [-1.5, +6.1] percentage points |
| Held-out tuning gain, zero jitter | +11.6 [+7.8, +15.5] percentage points |
| Held-out tuning gain, quarter jitter | +5.5 [+1.1, +10.0] percentage points |
| Tuned means, zero / quarter jitter | 45.7% / 41.8% |

Bracketed ranges are 95% joint-realization bootstrap intervals. The jitter
interval does not establish the declared one-percentage-point loss margin;
neither the untuned nor tuned ensembles establish an 80% mean-capture target.
These results are conditional on the ten corrected rings and assumed budget.

## Reviewer 1

### R1B-01 — Survival duration and scope

The duration macro comes from the artifact's turn count. The 100 nm sensitivity result retains its 4000-turn interval, 1000 particles, seeds 1001/1002 and 3.5-point late loss, explicitly separated from the design-beam result. Final native tracking uses the declared chamber; its 500-turn masks exactly reproduce D6. Fresh seeds 2001/2002 test both angular edges and corrected ring 5501 to 4000 turns. The operating window is a conditional 500-turn contour, not a converged acceptance boundary. See the operating-window and survival sections, [round2_validation](../revision_manifest_round2.json) and [round2_window](../revision_manifest_round2.json) manifest artifacts, and [validation methods](../round2_validation.md).

### R1B-02 — Independent trajectory validation

An adaptive DOP853 solution of the stated paraxial equations checks nominal and final-edge trajectories, three nonzero vertical-coordinate cases and two momentum offsets. All eight pass the slice/span gates. The manuscript table reports x, px, y and py errors, with solver tolerances and deterministic units. The exact filament field is distinguished from the paraxial tracking approximation. Evidence: [round2_trajectory_final](../revision_manifest_round2.json), its scan-input hash record, and `scripts/validate_round2_trajectory.py`.

### R1B-03 — Ideal steering and stochastic estimand

The text writes the actual transformation: subtract only the zero-input perturbed BTS reference's x and px at the septum exit. Vertical displacement, optics distortion and all shot terms remain. Each draw contains one static machine and one shot. Bootstrap uncertainty is over joint draws conditional on the ten corrected rings, not a nested machine/shot population. RF phase and pulse-relative timing are separate, and pulser timing does not also displace the bunch by c times its timing error. Evidence: [implementation audit](../round2_implementation_audit.md), [error budget](../round2_error_budget.md), and [final robustness methods](../round2_robustness.md).

### R1B-04 — Paired jitter and loss margin

All jitter levels reuse sample, particle and ring identities, verified by the analysis. Paired differences from zero jitter have 95% realization-bootstrap intervals (10,000 resamples, seed 1729); the declared loss margin is one percentage point. The final inference is based on these intervals, not on overlapping independent error bars. Mean, median, tenth percentile and fraction at or above 80% are reported separately. Partial Spearman tests use Holm adjustment over sampled-error hypotheses while controlling ring identity. Evidence: [round2_robustness](../revision_manifest_round2.json) and the jitter table.

### R1B-05 — Pulse phase and return fields

Injection is at the peak of a finite-support half-sine. The one-tenth-window allowance is labelled an assumption and updated from the final angular width. Native return positions supply the kick estimates. A 5.3 µs example has no nominal return field; an 8 µs pulse retains about half the peak at the first return. Deterministic timing offsets, Gaussian rms timing, train variation and hypothetical shell diffusion are distinguished. No time-dependent capture or chamber-specific feasibility is claimed. See [pulse note](../pulse_and_timing.md) and [round2_pulse](../revision_manifest_round2.json).

### R1B-06 — Mechanism and control claims

The contribution is a quantified finite-length comparison and conditional tolerance study, not a novel sliced-map method. Vector maps retain the signed vertical field; the incorrect vertical sign was an input-convention error. Focusing is flank dependent. The sagitta ratio uses kick-lobe FWHM and is tested over 30 centroid configurations with two related wire families, without claiming a universal capture criterion. Controls share particles and are not independently optimized injection systems. See the introduction, finite-length comparison, scaling figure and discussion, with [scaling methods](../round2_generality.md).

### R1B-07 — Centroid and full-beam transparency

Aligned symmetric centroid cancellation is separated from finite-beam moment changes. Deterministic quadrature orders 20/40/60 agree at the reported precision. Tracked amplitudes use ends of turns 1–50, while emittance ratios use the end of turn 1000, for two 300-particle seeds. Wire displacement and loop-current tables cover both planes, with series powering conditional on symmetric geometry. Evidence: [round2_transparency](../revision_manifest_round2.json), [round2_stored_tracked](../revision_manifest_round2.json), and [transparency methods](../round2_transparency.md).

### R1B-08 — Figures, uncertainty and presentation

Captions identify particles or joint realizations, seeds/counts, observation windows, deterministic quantities and interval types. Figure 7 adds paired-bunch NKM-minus-dipole differences and a bootstrap interval, with the four-bunch precision limit stated. Provisional backend validation is replaced by the final-point native/affine comparison. The text removes campaign history and selection-unbiasedness claims and labels retained sensitivity studies physically. See the [revised manuscript](../paper.pdf).

### R1B-09 — Referee evidence

The new campaign-03 manifest records hashes for all selected artifacts and supporting configurations, corrected rings and raw results. The frozen local attachment includes committed source, scientific inputs, environment information, a complete hash inventory and rebuild instructions. Rebuilding from that snapshot reproduces the installed macros exactly. The availability statement does not invent a public DOI or claim that ignored results are in git. See the [reproduction instructions](../round2_reproduction.md); bundle details and verification are recorded in the [D13 completion archive](../../exec-plans/completed/156_round2_evidence_verification.md).

### R1B-10 — Final reconciliation

The final manuscript, macros and figures were rebuilt together, the full test suite and protected-file inventory checked, and the round-1 response retained unchanged. Final counts, build outcome and evidence hashes are recorded in the [D14 completion archive](../../exec-plans/completed/157_round2_final_reconciliation.md). See the [verification guide](../round2_final_checks.md). Journal conversion is outside D14 and remains author-gated.

## Reviewer 2

| Request | Change and evidence | Remaining scope restriction |
| :--- | :--- | :--- |
| R2b-1 — chamber | Default design-beam chamber, aperture grid and longitudinal/plane loss map; D6 and [round2_chamber_ideal](../revision_manifest_round2.json), [round2_chamber_corrected](../revision_manifest_round2.json), [round2_chamber_da](../revision_manifest_round2.json). | Octagon corners, NKM ceramic dimensions, actual IVU map and incoming-line chamber remain unspecified. The smallest tested ideal-ring width is not a universal engineering minimum. |
| R2b-2 — corrected seeds | Ten seeds with girder/magnet offsets, rolls and multipoles; 120-HVC SVD correction, bounded tune correction, saved lattices, capture/acceptance distributions. [Evidence](../round2_corrected_ring.md). | A selected scenario with a 100 µm BPM-rms criterion, not commissioned as-built seeds. A stricter 20 µm criterion was not achieved. |
| R2b-3 — manufacturing/powering | Both-plane dipole and normal/skew quadrupole derivatives, one-wire and independent-loop 0.1-sigma limits; D9 sensitivity tables. [Evidence](../round2_transparency.md). | Local one-error limits, not a simultaneous manufacturing allocation; loop powering is unknown, so series and independent cases are distinct. |
| R2b-4 — pulse | Final-window allowance, native return positions, peak phase, compatible example, timing/train variation and thin-shell diffusion estimates; D10 updated with D11 window. [Evidence](../pulse_and_timing.md). | Actual chamber material/coating and pulse-field evolution are unknown; no operational pulsed capture is claimed. |
| R2b-5 — tuning | Seven-evaluation bounded capture-based coordinate sweep on 50 static machines; 100 independent training particles, held-out 200-particle zero/quarter-jitter validation and paired gains. [Evidence](../round2_robustness.md). | This fulfills the adopted reduced tuning study. No BPM/charge-monitor noise or actuator-resolution model is supplied; operational beam-based feedback remains unvalidated. |
| R2b-6 — budget sources | Design booster emittance/spread, separate septum-strength/RF/pulse-timing terms, source or explicit sensitivity reason for every table entry; D4 and D8. [Evidence](../round2_error_budget.md). | Extraction jitter and septum stability have no supplied measurements; no invented specification or literature range is used. |
| R2b-7 — identity | Author identifies K4GSR_HBIv4-1 with Kim et al. IPAC'25; title and text say design lattice. NKM is a preliminary study design by Dong-Eon Kim, not the baseline injection system. [Evidence](../dependent_answers.md). | Later KLS versions exist but were not supplied or simulated. |
| R2b-8 — generality | Sagitta/width scaling in length and strength, a 1.25-scaled transverse wire family, thin versus sliced vector-map comparison, and narrowed claims; D7. [Evidence](../round2_generality.md). | Related geometries and deterministic centroids, not validation across arbitrary NLK designs or capture populations. |
| R2b-9 — survival/backend | Final-point affine/native comparison, exact 500-turn prefix check, 4000-turn nominal/edge/degraded checks; D11. [Evidence](../round2_validation.md). | The main estimand remains conditional 500-turn capture, with later losses quantified. |
| R2b-10 — inference | Paired jitter intervals, 150 pooled joint draws, 50 per jitter level, Holm-adjusted partial associations; D8. [Evidence](../round2_robustness.md). | Conditional associations are not causal driver rankings or uncertainty over an unlimited ring population. |
| R2b-11 — comparison | Source-checked geometry and performance table for PF, BESSY II, MAX IV, SOLEIL, SIRIUS and this study; [source audit](../round2_comparison_audit.md). | Missing comparable quantities are dashes; design and measured results and different publication stages are distinguished. |
| R2b-12 — leakage/coupling/quadrature | Thin/thick septum order-of-magnitude kick estimates, assumed 0.10 vertical ratio and inverse-square-root response scaling, quadrature order checks; D9/D12. [Evidence](../round2_transparency.md). | Baseline bumped-orbit leakage is not the field at the unbumped NKM orbit; a local map is still needed for system transparency. |
| R2b-13 — presentation | Shorter abstract; physical labels replace draft history; centroid/moment and model-validity language reconciled in introduction/discussion/conclusion; D12. [Evidence](../paper.pdf). | Larger-emittance studies remain explicitly labelled sensitivity results. |
| R2b-14 — parameters | RF frequency/voltage, momentum compaction, damping times, synchrotron tune, stored/injected bunch lengths, pulse example and chamber limits in the parameter table; [round2_lattice_parameters](../revision_manifest_round2.json). | Injected Twiss/bunch length, coupling and NKM clearance are study assumptions. |
| R2b-15 — format/access | Verified referee attachment and explicit access route; D13. [Evidence](../round2_reproduction.md). | A6 defers the venue decision. Generic article format is retained; D15 journal conversion is not part of the authorized D1–D14 completion. |

## Minor comments and author inputs

The model sections and captions now state units, statistical units, particle/seed counts and observation windows. The selected-point rule is distinguished from unbiased validation, transfer-line mismatch from capture, and ideal kicker transparency from septum/chamber contributions. The parameter table, the final error budget and the comparison table address the requested parameter and source additions. Author inputs A1–A5 are used with their supplied verified/assumed/unknown status; A6 remains deferred. No protected scientific source was regenerated or edited.

## Final verification

- Full repository suite: **702 passed** in 128.10 s.
- Gated manuscript build: **19 pages**, without LaTeX errors, undefined references/citations, BibTeX warnings or overfull boxes. The installed and final-package PDFs have identical rendered text.
- All **205 selected artifact hashes**, **10 protected input hashes**, and **nine historical review/response/plan files** match their recorded states.
- The frozen attachment contains **213 inventoried files**; every inventory entry verifies, and the archived-source rebuild reproduces the manuscript macros exactly. Its committed source is `9028978e8f4627efc18a21d6a58f625e7e4b4c2d`.

The [D13 verification record](../../exec-plans/completed/156_round2_evidence_verification.md) identifies the local attachment and its archive hash. The [D14 completion record](../../exec-plans/completed/157_round2_final_reconciliation.md) records the final tests and build. These are reproducibility and consistency checks, not journal acceptance or validation of commissioned-machine performance.
