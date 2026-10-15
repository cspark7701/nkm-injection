# Response to Reviewer 2 — BTS main-branch manuscript

This response addresses the [2026-10-15 report](reviewer2_bts_20261015_main_report.md) and its tasks R2B-01 to
R2B-07. The report and all earlier reviews and responses are unchanged. This is a pre-submission revision record,
not a journal decision.

**Evidence entry points:**
- [protocol](../round3_protocol.json), declared before the campaigns, with one recorded amendment;
- [reproduction guide](../round3_reproduction.md);
- claims BR3-01 to BR3-13 in the [claim ledger](../claim_evidence.csv), verified by `scripts/audit_bts_evidence.py`;
- milestones 225–231 in the [completed-task index](../../exec-plans/completed/README.md).

## Summary of the revision

The article is re-framed around the reviewer's central point; its title, *Beta reduction and physical clearance in a parametric booster-to-storage-ring transfer line*, is kept. Its findings:
- **Active restriction.** With element-wise apertures and the companion septum geometry, the injection-septum blade
  is the active restriction. Its nominal clearance is independent of the quadrupoles.
- **Jitter transfer.** With matched ends, the quadrupoles act on the exit jitter only through the horizontal phase
  advance, which exchanges blade loss for injection-angle jitter.
- **Loss observable.** A Gaussian loss probability, validated against tracking within 1 %, replaces mean clearance
  as the design observable.
- **Fresh-machine test.** A loss-based setting cuts the tracked loss 3.5-fold. Lowering the vertical peak beta gives
  no resolved change.
- **Exit dispersion.** A dispersion-free exit is feasible and lowers the predicted loss much further.
- **Supplement.** The four-station study moves to the supplement.

## Major comments

**M1 / R2B-02 — Boundary-fixed clearances** (milestone 225).
- Section 3.1 now states analytically that the end-station clearances follow from the boundary Twiss, dispersion,
  emittance and energy spread. This gives 17.455/18.865 and 18.555/19.064 mm for every matched setting. A test
  reproduces Table 2 of the old model.
- The statement is generalised: every restriction upstream of q11 or downstream of q33 has quadrupole-independent
  nominal clearance.
- The baseline ensemble result is no longer a headline.

**M2 / R2B-01 — Physical restrictions** (milestone 226).
- Every element now has an aperture (Table 2): quadrupole bores, curved bend chambers with stated sagittas (30.8 and
  19.5 mm), the extraction septum and kicker, and the injection-septum channel with the blade at +1.478 mm. The
  blade value is taken from the companion geometry; all other dimensions are labelled assumptions and swept.
- **Result.** The blade channel is active at 0.648 mm for both settings; interior clearances are at least 9.1 mm.
  Bend-gap and extraction-septum sweeps leave the minimum unchanged, and the blade distance sets it.
- The m2/m3 hypothetical restrictions, with their tables and figures, are moved to the supplement.

**M3 / R2B-03 — Trajectory correction** (milestone 227).
- **Model.** Thin correctors and monitors with 50 µm static reading errors; model-response, Tikhonov-regularised
  least squares; kicks ±1 mrad. Shot jitter is not corrected.
- **The declared layout.** It corrected position but raised the exit-angle spread (0.36 → 0.54 mrad), because its
  last corrector, 1 m from the exit, trades position for angle.
- **The amendment.** A corrector before b3 and a monitor at the septum entrance were added. The amendment is
  recorded in the protocol before any later campaign, and both layouts are reported.
- **Result.** Loss falls from 10.08 % (uncorrected) to 2.39 % (declared) and 1.60 % (amended). The residual exit
  spread equals the booster-jitter transfer.
- **Error-model consistency.** The error model is now consistent with the companion (steered statics, booster
  jitter at m1).

**M4 / R2B-04 — A loss-relevant objective** (milestone 228).
- **Loss model.** Per-shot Gaussian loss probabilities at every aperture agree with the tracked losses within 0.6 %
  (relative) in all six steering rows and within 1 % on the fresh test.
- **Mean clearance mis-ranks.** The uncorrected line has the largest mean clearance and six times the loss.
- **Phase advance.** Matched ends make the exit jitter a function of μx only. 349 matched solutions from 360 starts
  reach μx = 200.2–232.0°.
- **Loss-based setting.** Optimising the shot-averaged loss gives a feasible setting at μx = 200.2°. SLSQP ended at
  its iteration limit; this is reported as a boundary point, not a certified optimum.
- **Fresh test.** On 200 fresh steered machines it loses 0.66 % against 2.32 % for the reference: −1.66
  [−2.42, −0.99] percentage points. Low beta changes the loss by −0.17 [−0.38, +0.02], unresolved. The mean-clearance
  change of the loss-based setting is unresolved, −0.013 mm.
- **Cost.** Exit-angle jitter is 13 % higher.

**M5 / R2B-05 — Exit target** (milestone 229).
- The m4 target is identical to the companion's injected beam at the septum exit. The text and the Table 1 caption
  now say so, and state that the nonzero D/D′ is inherited rather than derived from the ring.
- **Divergence budget.** 57 µrad betatron plus 50 µrad dispersive; shot energy jitter adds 47 µrad and 81 µm.
- **Dispersion-free exit.** It is feasible: 115 of 120 starts matched, all peaks below 60 m. It widens μx to
  187.7–214.2°.
- At its best setting the predicted blade loss is 4.1×10⁻⁵, at 0.39 mrad exit-angle jitter. This is analytic, not
  tracked.
- The trade against the companion's 0.44 mrad angular window is stated as an injection-design decision.

## Minor comments

1. **Abstract.** Rewritten around the physical question and result (about 220 words).
2. **Section 3.1.** Analytic statement (R2B-02). Equation (3) is retained. The blade response is treated through the
   jitter transfer (Eq. 4) and the loss (Eq. 5).
3. **Error levels.** R2B-06 (milestone 230) repeats the steered evaluation at rolls of 0.1, 0.2 and 0.5 mrad and
   energy jitter of 0.05 and 0.1 %.
   - The roll level has no effect on the horizontal blade loss.
   - Halving the energy jitter changes the reference loss from 1.47 to 1.44 %.
   - The ranking holds at every level.
   - The gain varies between machine populations (×8.4 against ×3.5) because the loss is heavy-tailed: the top 5 of
     200 machines carry 39 %.
4. **Fig. 3 (phase space).** Moved to the supplement with the four-station study.
5. **Facility name.** "Korea Light Source (KLS)" is used in the text; "Korea-4GSR" remains only in cited titles.
6. **Declarations.**
   - The generative-assistance statement now names both tools, consistently with the companion.
   - Funding, acknowledgments and final approval remain author inputs and are not invented.
7. **Availability.** The statement still describes the local referee attachment. The deposit route or
   "available on reasonable request" wording is an author decision and remains pending.

## Questions

1. **Is m4 the companion's septum-exit beam?** Yes, all six values are identical. The nonzero D and D′ are inherited
   from the configuration, not derived from the ring. A dispersion-free alternative is evaluated (M5).
2. **Where is the booster jitter defined?** At m1 in both manuscripts; the BTS paper now states it in Section 2.4.
3. **Real bend gaps and septum channels?** Not available. They are swept as labelled assumptions, and the
   conclusions do not depend on them within the swept ranges.

## Checks

- The article (12 pages) and supplement (8 pages) build without warnings.
- Final asset hashes verify (`package_bts_revision.py --verify`), and all 49 manifest claims verify.
- Round-3 tests: 13 in `tests/test_bts_round3.py`. The full repository suite is recorded in milestone 231.
- Protected files are unchanged.
