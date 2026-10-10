# Consolidated revision plan — round 2 (Reviewers 1 and 2)

Date: 2026-10-11. Manuscript: `docs/paper/paper.tex` at commit `03b8fe9`, as reviewed.

Inputs:
- [Reviewer 1, round 2](reviewer1_round2_20261011_report.md) and its [register](reviewer1_round2_20261011_revision_tasks.md):
  10 tasks, R1B-01 to R1B-10. Recommendation: focused major revision.
- [Reviewer 2, round 2](reviewer2_report_round2.md): 15 tasks, R2b-1 to R2b-15. Recommendation: major revision.

The round-1 plan ([consolidated_revision_plan.md](consolidated_revision_plan.md), tasks C1–C12) and the round-1
[author response](author_response.md) stay unchanged as historical records.

## How the two reviews relate

The reviewers agree on five points:
- the survival duration and the 500-turn estimand;
- the paired jitter statistics instead of "costs nothing";
- the pulse-length inconsistency (both computed r = 0.50 at 8 µs);
- the over-general novelty wording (the vertical sign was an input error, not a limitation of kick maps);
- a referee-accessible evidence package.

They differ in what is required for realism. Reviewer 1 explicitly does **not** require a corrected as-built ring, a
larger campaign or a time-dependent pulse model, provided the claims are restricted. Reviewer 2 requires a chamber,
corrected ring seeds and beam-based tuning, because the headline numbers are otherwise not usable by a designer.

Reviewer 1 adds checks that Reviewer 2 did not raise:
- independent validation of the off-midplane trajectory integrator;
- an exact description of the "ideal steering";
- the centroid-versus-full-beam transparency wording;
- the observation windows of the tracked stored beam.

Reviewer 2 adds checks that Reviewer 1 did not raise:
- the micrometre-level wire tolerance of transparency;
- the lattice version;
- the generality scaling for PRAB.

## Adopted resolution where the reviewers differ

| Topic | Reviewer 2 | Reviewer 1 | Adopted |
| :--- | :--- | :--- | :--- |
| Vacuum chamber | KLS chamber as default aperture; loss map; or the minimum aperture for which the conclusions hold | Uniform apertures are scenarios, not bounds | Use the KLS chamber if the author can supply it (A1). Otherwise report the headline as a function of half-width and half-height, with a loss map at a declared reference aperture. "Bounded" becomes "scenario" in either case. |
| Ring errors | ≥ 10 corrected seeds with misalignments and multipoles | Not required if the claims are restricted | Limited corrected-error study: 10 seeds, girder and magnet misalignments, SVD orbit correction with the 120 HVC correctors and the BPM markers, tune correction. Feasible with the lattice alone. Presented as a selected scenario, not an as-built prediction. |
| Static errors and tuning | Re-optimise the injection knobs per realization | Describe ideal steering exactly; no nested Monte Carlo | Both. The ideal-steering algorithm is documented (D3). A reduced beam-based tuning study (D8: seed 42, 50 realizations, zero and quarter jitter, 100-particle scans) quantifies what tuning recovers. |
| Error budget | Source every entry; separate septum strength and RF phase jitter | A "hypothetical" label is acceptable | Cite sources where they exist. Otherwise keep "assumed", with the reason and the comparable published range. Add the septum-strength and RF-phase terms. Rerun the ensembles only once, with the final budget, chamber and tuning (D8). |
| Generality | Dimensionless criterion η = \|K\|L/(8w), scaling over L and K, a second geometry, comparison with a sliced kick map | Narrow the claims; no new magnet design | Do the scaling with single-centroid computations (cheap). For the second geometry, use a scaled wire family rather than a new design. Compare with a sliced map. Narrow the wording as Reviewer 1 asks. |
| Pulse | State the maximum pulse length; bunch-train variation; eddy-current estimate | Label the linear estimates; state the phase; time-dependent tracking only for operational claims | Analytic consistency, the maximum length (≤ 6.1 µs at peak injection, ≤ 5.3 µs for no return field), later-turn positions from native tracking, and an order-of-magnitude eddy-current estimate. No full time-dependent model. |
| Headline duration | Converged survival, or state the bias | Keep 500 turns as the conditional estimand, or check boundaries | Keep the 500-turn estimand. Fix the macro bug, and report the 4000-turn survival with an interval and the 3.5-point late loss. Check the window edges and one degraded case at 4000 turns (D11). |
| Journal format | PRAB: REVTeX 4.2, PhySH | Not raised | Author decision (A6). The text is framed for PRAB as in milestone 134; conversion is done last, only if confirmed. |

## Author inputs needed

These are needed before the dependent tasks; defaults apply if an input is unavailable.

| ID | Input | Needed by | Default if unavailable |
| :--- | :--- | :--- | :--- |
| A1 | KLS vacuum-chamber profile: injection straight, arcs, smallest insertion-device gaps, septum region | D6 | Aperture scan with a declared reference chamber; claims stated as conditional on it |
| A2 | Lattice version and date of `K4GSR_HBIv4-1` and its relation to the KLS baseline of Kim et al. (IPAC'25) | D1 | State "a KLS design lattice (version as supplied)"; consider retitling to "…a 4 GeV hybrid-MBA ring (KLS design)" |
| A3 | Status of the 0.525 m four-loop NKM (KLS project design or study design); are the loops powered in series? | D1, D9 | Study design; treat series and independent powering as two cases |
| A4 | KLS booster extraction emittance, energy spread and orbit stability; septum type and stability | D4 | Literature ranges for comparable full-energy boosters, labelled assumed |
| A5 | KLS coupling target (ε_y/ε_x) | D9 | Keep 0.1 and give the scaling |
| A6 | Target journal (PRAB recommended) | D15 | Keep the generic article class |

## Consolidated tasks in execution order

Each task is archived under the next milestone number (from 139) and committed; results stay uncommitted under
`results/journal_campaign_03/`, a new campaign directory. Compute estimates use 8 workers, scaled from the round-1
logs: one combined-error seed with dipole control took about 40 min, one jitter level about 19 min.

| D | Covers | Work | Acceptance | Sim / cost |
| :--- | :--- | :--- | :--- | :--- |
| D1 | R2b-7; R1 §5 (lattice version); A2, A3 | Lattice identity and design status: record the file version and baseline relation, and the NKM design and powering status. Decide on the title. | Text states version and status; the title matches the scope | No |
| D2 | R1B-01 (part), R1B-04, R2 m2, m3 | Existing-data fixes and analyses: `\SurvTurns` macro fix; 4000-turn survival with Wilson interval, particle count and seeds; paired jitter differences for all levels (bootstrap, fixed seed); a declared loss margin for any equivalence statement; Holm-adjusted partial correlations; mean, median, p10 and fraction ≥ 80 % kept distinct. | New builder macros; the quarter-jitter result stated as precision-limited, with 0.125 mm / 0.05 mrad as a conditional candidate target | No |
| D3 | R1B-02, R1B-03 (implementation part) | Implementation audits: (a) independent trajectory reference (adaptive ODE integration of the stated equations in the same filament field) at the nominal point, the window edges, y and y′ ≠ 0 and δ = ±2×10⁻³, with x, p_x, y, p_y discrepancies against the 640-slice map and slice/span convergence in both planes; (b) the ideal-steering transformation written out and checked against the code, with static and shot-dependent variables classified. | Discrepancies well below the window (0.74 mrad) and transparency (0.1 σ) scales, or the integrator fixed and only affected evidence regenerated | Small (minutes) |
| D4 | R2b-6, R2 M5(b, c); A4 | Error budget: a source or reason per entry; septum strength jitter and RF phase / arrival-time jitter added as separate terms in the error model, with tests. | Table 2 with sources; code and tests for the new terms | No (code only) |
| D5 | R2b-2; R1B-01 (scenario wording) | Corrected ring-error scenario: 10 seeds with girder and magnet misalignments and multipole errors; SVD orbit correction (HVC correctors, BPM markers); tune correction; DA per seed. | Corrected orbit and tune residuals reported; DA distribution; seeds saved for D6–D8 | Yes, ~3–5 h |
| D6 | R2b-1; R1B-01; A1 | Chamber: aperture model (A1 profile or reference chamber) applied to the ideal and corrected rings; loss map (s, plane) at the operating point; capture versus half-width and half-height; minimum aperture for the conclusions. | Headline quoted with a defined chamber; loss-map figure | Yes, ~2 h |
| D7 | R2b-8, R1B-06 | Generality and claims: η = \|K\|L/(8w) scaling over L and K; a scaled wire family as the second geometry; sliced kick map against the 3-D field; narrowed wording (vector maps can carry the vertical kick; flank-dependent focusing sign; controls described as paired model comparisons; the coupling mechanism as an interpretation unless diagnosed). | Scaling figure; contributions restated consistently in abstract, introduction, discussion and conclusions | Yes, single-centroid, < 1 h |
| D8 | R2b-5, R1B-03, R1B-04; final robustness | Final robustness campaign with the D4 budget, D6 chamber and, where applicable, the D5 corrected ring: (a) combined errors, three seeds, NKM and dipole, ideal steering; (b) jitter scan (0–1 and x/x′ only); (c) reduced beam-based tuning, re-optimising (x_inj, x′_inj, S) per realization (seed 42, 50 realizations, zero and quarter jitter, 100-particle scans). | Robustness section rewritten on these ensembles; tuning gain quantified; the 80 % statement re-derived | Yes, ~12–16 h total; overnight queue |
| D9 | R2b-3, R1B-07; A3, A5 | Transparency: on-axis dipole and quadrupole sensitivity to each wire position and to loop-current imbalance, in both planes; tolerances for 0.1 σ_x and 0.1 σ_y (series or independent powering); aligned-beam moment change (not only the centroid); "leading cubic term"; tracked observation windows (first 50 turns for amplitude, turn 1000 for emittance; 2 seeds × 300 particles); Figure 7 curves and caption reconciled. | Sensitivity table and tolerances; abstract and conclusion use the same observable | Small |
| D10 | R2b-4, R1B-05 | Pulse: later-turn centroid positions from native tracking; the one-tenth-window allowance labelled as an assumption; maximum half-sine length and injection phase; timing sensitivity 1 − cos(π dt/τ), with rms or deterministic stated; bunch-train field variation with an offset kicker; order-of-magnitude eddy-current estimate. | Section 8 and `pulse_and_timing.md` consistent; one compatible pulse example | Small |
| D11 | R2b-9, R1B-01 | Validation at the operating point: backend comparison (native versus linear map) and turn convergence with the 3-D model, replacing the provisional figure; 4000-turn checks at the two window edges and one degraded realization. | Figure 4 at the operating point; window conclusions qualified or confirmed | Yes, ~2–3 h |
| D12 | R2b-10–14, R1B-08; R2 m1, m4–m10, m12, m13; R1 §5 | Manuscript revision: remove draft history; comparison table of NLK/MIK systems; Table 1 additions (RF, α_c, damping times, bunch length, pulse, chamber); septum leakage estimate; Gauss–Hermite order; statistical unit and interval in every caption; Figure 7 paired-difference inset; selection-bias wording; shorter abstract. | Text, macros, figures and PDF agree; gated clean build | No |
| D13 | R1B-09, R2b-15 (evidence) | Evidence: new revision manifest for campaign 03; claim table refreshed (D rows); new frozen bundle verified by rebuild; access route stated in the availability statement (attachment or archive, no invented DOI). | Bundle verifies and regenerates the macros | No |
| D14 | R1B-10 | Round-2 author response as a **new** file, linking every R1B and R2b task to evidence or to an explicit claim restriction; full test suite; gated build; protected-file check. | Response complete; tests pass; earlier responses unchanged | No |
| D15 | R2b-15 (format); A6 | Journal conversion, only after the author confirms the venue (PRAB: REVTeX 4.2, PhySH, APS style). | Clean build in the journal template | No |

## Order and dependencies

```text
A1–A6 requested from author (non-blocking until D4/D6)
D1 ─┐
D2 ─┼─ existing data; can run first and in parallel
D3 ─┘   (D3 gates every new simulation: an integrator problem would invalidate reruns)
D4 ─→ D5 ─→ D6 ─→ D8 (overnight)        realism chain; rerun ensembles once
D7, D9, D10 ─ independent, cheap; run while D5–D8 compute
D11 ─ after D6 (uses the chamber)
D12 ─→ D13 ─→ D14 ─→ D15 (author-gated)
```

Rationale:
- **D3 comes first** among the computational tasks. If the off-midplane integrator were wrong, every rerun would be
  wasted.
- **D4 → D6 precede D8.** The robustness ensembles are the most expensive item and should run once, with the final
  budget, chamber and ring. Reviewer 2 explicitly warns against rerunning them earlier.
- **D7, D9 and D10 are cheap and independent.** They fill the compute wait.

## Not undertaken

Neither reviewer requires these items for the declared simulation scope:
- measured hardware data;
- a full time-dependent pulsed-magnet model;
- a global optimiser;
- a commissioned as-built machine;
- arbitrary increases of the particle or seed counts.

If the manuscript later claims operational efficiency or pulsed capture, these become necessary (Reviewer 1, "Work
not required").

Protected inputs remain read-only. Nothing is pushed, submitted or published.
