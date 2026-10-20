# Response to the fourth-round reviews

These were pre-submission assessments, not journal editorial decisions. This response addresses:
- Reviewer 1's R1D-01 to R1D-08 ([report](reviewer1_round4_20261016_report.md),
  [tasks](reviewer1_round4_20261016_revision_tasks.md));
- Reviewer 2's R2d-1 to R2d-7 and three questions ([report](reviewer2_report_round4.md)).

It follows the consolidated plan [F1–F9](consolidated_revision_plan_round4.md). Earlier reports, plans and responses
remain unchanged. The study is simulation-only and conditional on the supplied KLS design lattice, the declared
chamber and error budget, and ten corrected rings. The author's scientific approval of the revised claims is pending.

**Evidence entry points:**
- the [manuscript PDF](../paper.pdf) and [Supplemental Material](../supplement.pdf);
- the [round-4 protocol](../round4_protocol.json), declared before any round-4 run and amended only before the runs
  it adds;
- the [round-4 manifest](../revision_manifest_round4.json) and [claim table](../claim_evidence.csv), rows F0–F9;
- the round-4 notes:
  - [ablation](../round4_ablation.md);
  - [points](../round4_points.md);
  - [two-plane steering](../round4_vertical_steering.md);
  - [associations](../round4_associations.md);
  - [loss locations](../round4_loss_locations.md);
  - [dispersion and accuracy scope](../round4_dispersion_scope.md);
  - [pulse and transparency](../round4_pulse_transparency.md);
- the [reproduction instructions](../round2_reproduction.md), round-4 section;
- milestones 236–246 in the [completed-task index](../../exec-plans/completed/README.md).

## Main changes and what they changed in the conclusions

| Item | Change | Effect |
| :--- | :--- | :--- |
| Attribution | Paired error-class ablation without booster jitter: 15 new ensembles, every other draw unchanged. | BTS magnet errors cause the loss (NKM −39.2, dipole −14.5 points); every other class is ≤ 1.6 points. The "chiefly booster angle jitter" claim is withdrawn. |
| Mechanism | The steering in the model is horizontal only. The BTS errors leave a 0.90 mm / 77 µrad rms vertical centroid. A declared two-plane steering sensitivity tests it. | Without jitter the NKM rises 40.1 → 76.6 % (gap −28.3 → −6.1). With the vertical error removed, booster position and angle jitter become comparably NKM-specific (gaps −14.7 and −13.2). |
| Operating point | Paired test of the earlier and extremum-centred points, under a declared rule. | Current point retained (no resolved NKM gain). The dipole loses 17–23 points at the alternatives, so the gap is point-dependent. |
| Pulse | Recomputed at the current point with one allowance convention (0.044 mrad). | Limits 5.76 / 5.33 µs; the 5.3 µs example still holds. |
| Transparency | Recomputed at S = 0.95. | 0.2 mm offset gives 0.11–0.12 σ, slightly above 0.1 σ; wire limits 0.26–1.82 µm. |
| Associations | Signed and physical predictors for both models and their difference. | Post-kick amplitude organises capture; the signed NKM offset is NKM-specific. |
| Losses | Per-particle loss records for zero-capture cases and ring 5501. | First-turn, mostly vertical, none in the magnet; ring 5501 is not limited by the NKM chamber. |
| Scope | Septum dispersion stated; thin-map error on the production trajectory; chromaticity claim reduced. | 161 µrad thin-map error at the current point (3.7 × allowance); fit stated as empirical. |

## Reviewer 1

**R1D-01 — Paired ablation** (F1, F2; milestones 236, 241).
- The seven classes are declared in `round4_protocol.json`. A disabled class keeps its random draws (σ = 0), so
  particles, ring identities and every other error are unchanged (tested).
- Alone and omitted effects with paired intervals are reported for the NKM, the dipole and their gap, together with
  the non-additivity: +3.5 points for the NKM, +0.2 for the dipole.
- The abstract, attribution, discussion and conclusions are rewritten from these effects. No causal claim rests on a
  correlation.

**R1D-02 — Operating-point comparison** (F1, F3; milestones 236, 242).
- Earlier (S 0.85) and extremum-centred (S 0.95) points have feasible matched roots, septum clearance and recalibrated
  controls. They are evaluated against the current point at zero and full jitter on the E7 realizations.
- Under the rule declared before the runs, neither candidate improves the full-budget NKM mean with an interval above
  zero. The current point is retained explicitly.
- The text no longer recommends an untested robust optimum.
- **Disposition (author decision): error-inclusive point re-selection is closed for this revision.** The paper states
  that the selected point was chosen without injection errors and favours the uniform kick; it leaves error-inclusive
  selection open.

**R1D-03 — Pulse at the adopted point** (F7; milestone 244).
- The pulse is recomputed at the current point with the current chamber: native turn 1–3 coordinates, full kicks,
  allowance and finite-support pulse limits.
- One allowance convention: one tenth of the current 0.443 mrad window, i.e. 0.044 mrad, for both the pulse and the
  thin-map accuracy.
- `make_round4_manifest.py` re-points the builder keys and checks operating-point identity, injection position and
  field scale for every current-point artifact, not only hashes (tested). The S = 0.85 originals remain as labelled
  history.

**R1D-04 — Loss diagnostics** (F5; milestone 239).
- Losses are recorded by plane, element, s and turn for the first NKM zero-capture realization on each of 8 rings and
  for ring 5501. The reruns reproduce the stored category counts exactly.
- 1 491 of the 1 500 NKM losses are first-turn, 955 vertical, and none is inside the magnet. F2 then traced them to the
  static vertical injection error.
- The flat chamber is the physical boundary inside the magnet. The 1 mm conductor guard and the ±50 mm field domain
  (`outside_field_map`) are numerical and act only in the fringe span.
- The section-5 coupling sentence is closed.
- **Disposition (author decision): the coupling question is closed.** Ring 5501's slow vertical losses are reported as
  consistent with uncorrected coupling (no skew correctors), not isolated. Opening the in-magnet chamber to 15 mm
  raises capture only to 33.2 / 37.6 %.
- The chromaticity inference is reduced to "common to both kickers; mechanism not identified".

**R1D-05 — Signed predictors** (F4; milestone 237).
- Signed errors, plus a physically constructed post-kick centroid amplitude for each kicker, are used for the NKM, the
  dipole and their paired difference, with Holm adjustment within each response.
- The relative displacement is the NKM offset minus the closed orbit. Both controls are calibrated to the 3-D
  centroid response under the same rule.
- Results:
  - own-kicker amplitude ρ = −0.60 (NKM) and −0.70 (dipole);
  - signed NKM offset +0.26 (p_Holm 0.011), NKM only;
  - signed booster position +0.28 with the gap.
- These are labelled exploratory.

**R1D-06 — Accuracy scope and dispersion** (F6; milestone 238).
- The η^1.46 fit is stated as an empirical description of the stated family and diagnostic launch. Along the
  production trajectory the thin-map error is 161 µrad at the current point (3.7 × the allowance) and about 47 µrad
  near the extremum; the sliced map agrees to better than 1×10⁻⁷ rad.
- The opening claim is restricted to this geometry and regime.
- The septum D = 80.9 mm and D′ = 47.5 mrad are in Table II, with their angular contributions (50 µrad within the
  bunch, 47 µrad per 0.1 % shot).
- The companion dispersion-free BTS exit is mentioned as an alternative without importing a capture claim.

**R1D-07 — Strength, labels and conventions** (F7, F8; milestones 244, 245).
- Transparency is recomputed at S = 0.95 rather than rescaled. The emittance quantities are re-evaluated, not scaled
  linearly.
- Historical S = 0.85 items are labelled: Table I and Table II peak kick, the Fig. 1 and Fig. 7 captions.
- Zero-capture fractions and conditional means are given for both models: NKM 51 % zero-capture with conditional mean
  33.0 %; dipole 10 % and 49.0 %.
- Jitter rows cover both models.
- The acceptable-loss bound is stated as the lower endpoint of a central 95 % interval, i.e. a conservative 97.5 %
  one-sided bound.
- The margin fit is stated as degenerate; dates are updated.

**R1D-08 — Final reconciliation** (F9; milestone 246).
- This response; the claim table, rows F0–F9; the round-4 manifest and figure provenance.
- All figures are regenerated in one environment (matplotlib 3.11.1).
- Both PRAB layouts and the supplement are built under the clean-log gate and installed.
- The full test suite passes, and the round-4 frozen bundle is verified.
- These are local checks, not a submission or acceptance claim.

## Reviewer 2

**R2d-1 — Paired ablation and rewrite** (F2, F8). See R1D-01. In summary:
- The 28-point gap without jitter comes from the BTS magnet errors, through the uncorrected vertical injection error.
  About 5 points remain at all-off.
- Removing the vertical error in the declared sensitivity restores the NKM to the omitted-class value (76.6 %).
- Booster jitter and the vertical error remove largely the same NKM shots. Once the vertical error is corrected,
  booster jitter is NKM-specific in both components.
- Your M1 observation (jitter costs both kickers about 20 points) holds under the production steering, and the
  abstract no longer attributes the loss to booster angle jitter.

**R2d-2 — Operating points** (F3). See R1D-02.
- The sentence "which this study does not test" is removed.
- Retaining the current point is a decision under a rule declared before the runs. The selection's limitation
  (injection errors excluded) is stated.

**R2d-3 — Pulse** (F7). See R1D-03. `round2_pulse` now resolves to the current-point artifact through the round-4
manifest.

**R2d-4 — Signed associations and dipole table** (F4). See R1D-05.

**R2d-5 — Losses and chromaticity** (F5). See R1D-04. The chromaticity claim is reduced rather than tested by
sextupole correction.

**R2d-6 — Dispersion** (F6). See R1D-06.

**R2d-7 — Editorial** (F7, F8).
- Dipole position-only and angle-only jitter rows are in the two-model jitter table.
- Zero-capture fractions and conditional means are given.
- Transparency is regenerated at S = 0.95.
- The Fig. 7 left caption names the earlier point.
- The margin fit is stated as degenerate; dates are updated.
- **Tuning range — disposition (author decision): accepted as is.** The range is not extended, and the 28 %
  boundary fraction stays next to the tuning gain in the text and the conclusions.

**Questions.**
1. *Kick slope.* The local slope ∂Δx′/∂x at the centroid is +0.32 mrad/mm at the selected point and −0.09 mrad/mm at
   the earlier point.
   - The magnitude ratio, about 3.5, does not predict the window ratio (0.44/0.76 = 0.58) quantitatively. The window
     also depends on the injected amplitude and the ring acceptance.
   - The steep slope explains the position sensitivity (a position error becomes an angle error) and the vertical
     kick on a displaced centroid.
2. *Septum dispersion.* It is a consequence of the declared BTS exit target, not a property the line requires.
   - The production BTS optimisation matched β, α, D and D′ to an inherited septum-exit target that includes
     D = 80.868 mm and D′ = 47.472 mrad (residual 4×10⁻¹¹ m).
   - The companion BTS study finds dispersion-free exits feasible on the unchanged magnets. Their ring capture has not
     been evaluated.
3. *Clustering of zero capture* (post hoc, from the F4 records, 150 realizations). Neither ring identity nor offset
   sign separates the zero-capture events clearly:
   - the zero-capture fraction varies between rings (χ² p = 0.056; ring 5505 has 1 of 9);
   - it is 60 % for a negative NKM-minus-orbit offset against 42 % for a positive one (Fisher p = 0.05), consistent
     with the signed-offset association.
   - F2 then identified the dominant cause, the static vertical injection error, which is set by the BTS draw, not by
     the ring.

## Round-4 frozen attachment

`results/journal_campaign_05/round4_evidence_bundle.tar.gz`: 20.1 MB, SHA-256
`dbe3a7a82f138c9709a14950ca45cdd678033a71de03e55b1ca3dde02c9dab67`.
- Built from commit `8215a48` with `uncommitted: false`; 250 artifacts and 258 inventoried files.
- `--verify` rebuilt the macros from the archived source on the bundled evidence alone, byte-identical.
- `sha256sum -c SHA256SUMS` passes for all 258 entries.
- It is git-ignored; no DOI or upload.
