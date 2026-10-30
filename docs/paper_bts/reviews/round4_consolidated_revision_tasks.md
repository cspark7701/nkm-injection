# Round-4 consolidated revision tasks — BTS main-branch manuscript

Date: 2026-10-30. Manuscript reviewed: `603c3ab`, *Optical matching and beam loss in the Korea Light Source
Booster-to-Storage transfer line*, 15 pages, with an eight-page supplement.

**Sources.** This register merges two round-3 task registers into one list for the round-4 revision:
- [Reviewer 1 round-3 tasks](reviewer1_bts_20261030_main_round3_revision_tasks.md), R3-BTS-01 to R3-BTS-08, from
  the [Reviewer 1 report](reviewer1_bts_20261030_main_round3_report.md): focused major revision;
- [Reviewer 2 round-3 tasks](reviewer2_bts_20261030_main_round3_revision_tasks.md), R2C-01 to R2C-10, from the
  [Reviewer 2 report](reviewer2_bts_20261030_main_round3_report.md): major revision.

Both source registers stay unchanged and authoritative for their reviewers' wording. Every source task appears
below, in some cases split between two consolidated tasks. All tasks are **open**.

**Constraints.**
- The BTS lattice is not changed. Any refinement uses an auxiliary evaluation copy.
- New numerical outputs go in new `results/` directories.
- Earlier reports, responses, campaigns and attachments are preserved.

**Priority:**
- **A:** required by at least one reviewer for acceptance;
- **B:** strongly recommended, or conditional;
- **C:** editorial.

**Computation:**
- **analytic:** the existing Gaussian loss model, with no tracking;
- **tracking:** new particle tracking;
- **matching:** new optics matching runs.

## Task register

### A — required

| ID | Task | From | Computation | Completion criterion |
| :--- | :--- | :--- | :---: | :--- |
| R4-BTS-01 | **Booster jitter input.** Source the 0.5 mm / 0.2 mrad jitter at m1, or label it a stress level. State it in beam-size units (1.3σ / 2.2σ at m1; about 4σ at the exit). Define J as the non-dispersive centroid jitter before the separate momentum term. Sweep position and angle jitter together (×0.1, 0.2, 0.5, 1) for the matched reference, low-beta and loss-based settings. Report the loss, the loss-based gain and the level at which static residuals dominate. | R2C-01; R3-BTS-01 (definition of J) | analytic | Sensitivity table with betatron-jitter rows; the abstract and conclusions state the jitter regime of the results |
| R4-BTS-02 | **Blade-distance sweep.** Predicted loss against d_b for the three settings, at the present and a realistic jitter level. Give the d_b for a stated tolerance (e.g. 0.1 %). Note the ring-acceptance cost of a larger d_b and the TDR 1 mm thin septum. | R2C-04 | analytic | Figure or table of loss versus d_b; tolerance statement |
| R4-BTS-03 | **Loss model and bounds.** For the round/elliptical apertures, use the correct probability, or call the chord-at-the-other-centroid construction an approximation. Claim rigorous max/union bounds only for exact rectangular and one-sided edges. Add a deterministic limiting-case test: a centered isotropic Gaussian at a 5σ circle gives exp(−12.5) = 3.73 × 10⁻⁶, against the current 4Φ(−5) = 1.15 × 10⁻⁶. Show whether the blade-dominated predictions and the chosen settings change, and regenerate only affected outputs. Separate the max-of-marginals design surrogate from the line union loss. State that "within 1 %" means relative agreement of aggregate means in the tracked rows. Add a caveat that Gaussian-formula versus Gaussian-tracking agreement is numerical consistency, not evidence about real booster tails. | R3-BTS-02; R3-BTS-06 (aggregate versus per-shot); R2C-08 (within 1 % relative; Gaussian caveat) | analytic; tracking only if outputs change | Counterexample handled; bounds stated only where valid; affected numbers regenerated or shown unchanged |
| R4-BTS-04 | **Scope of the boundary theorems.** Restrict the fixed-end clearance theorem (Section 3.1) and the phase-only jitter transfer (Section 3.2) to the nominal, error-free, uncoupled, exactly matched line. Under errors, the endpoint covariance also depends on K, through gradient errors, rolls, chromatic transport and the beta factors. Name the full covariance calculation used for the test losses. Do not claim that static errors are removed: replace "steered static errors add a small residual" by the recorded effect. The error-free losses are 1.28 % / 0.27 % and the tracked steered losses 2.30 % / 0.69 %, so the residual roughly doubles the loss. | R3-BTS-01; R2C-05 (small residual) | none | Sections 3.1, 3.2, 4.2 and the conclusions are consistent with the error model and Tables 6–7 |
| R4-BTS-05 | **Phase-advance design.** (a) **Wording:** call the μ_x ranges the ranges found by the 349/360 and 115/120 searches, not proven reachability, and call the loss-based setting a best-found feasible point. Keep the record that all three SLSQP starts hit the iteration limit. Make the leverage of the exit target conditional on the alternatives tested. (b) **Scan:** add μ_x as an equality, minimise peak beta on a μ_x grid for both exit targets, and report feasibility, the active bound at each interval edge, the predicted loss and the exit-angle jitter. Run a fresh tracked test of the point chosen from the scan. | R3-BTS-05 (a); R2C-03 (b) | matching + tracking | Figure 4, Section 4.3 and the conclusions use sampled-search language. A loss versus angle-jitter trade curve is shown, with the active constraint named at the edges. |
| R4-BTS-06 | **Mean clearance and statistics language.**<br>• **Mean clearance.** Explain the mean-clearance counterexample without implying survivor censoring: all 600 shots are in the denominator. Use the recorded mean exit x (−68.50 µm uncorrected, +8.77 µm corrected) and the analytic argument that E[c] does not depend on the jitter variance, whereas E[P] does.<br>• **Low-beta comparison.** Replace "indistinguishable in every column" by the paired intervals: 1.68 % against 1.47 % in Table 6; the low-beta change is unresolved, not equal.<br>• **Intervals.** Describe the clustered interval method once, and say that the bootstrap does not certify tail convergence. | R3-BTS-04; R2C-05 (indistinguishable); R2C-08 (clustering method) | none | Section 4.2 and the conclusions agree with the recorded intervals and uncensored moments |
| R4-BTS-07 | **Framing, baseline and title.**<br>• **Baseline provenance.** State where the `BTSConfig` baseline strengths come from and which exit target they were designed for. Keep Table 5 as a nominal starting-point comparison; Reviewer 1 accepts it as an envelope/matching change. Remove it from the headline, because its blade-clearance comparison is circular (d_b = 3σ_x + 1 mm of the matched beam).<br>• **Abstract and Discussion.** Rewrite the abstract and the first Discussion paragraph around the results that carry the paper: boundary-fixed nominal clearance, the phase-advance partition of jitter, the validated loss observable, the jitter dependence and the angular-jitter cost.<br>• **Setting names.** Use one name per setting (baseline, matched reference, low beta, loss-based), and show the loss-based setting in the headline figures or tables.<br>• **Title and TDR.** The title should name the studied design version and say "Booster-to-Storage-Ring". Keep the difference from the TDR line prominent. | R2C-02; R2C-08 (title); R3-BTS-07 (strength labels, TDR prominence) | none | The abstract no longer leads with matching the unmatched baseline; names are consistent; the title is accurate |
| R4-BTS-08 | **Submission readiness.**<br>• **Data availability.** Restore a statement whose wording the author chooses and which matches actual access. JKPS and NIM A both require one.<br>• **Declarations.** Deduplicate Funding and Acknowledgments. Remove "final approval is pending" only after author approval.<br>• **Companion study.** Identify the companion NKM study as a manuscript in preparation and keep its acceptance width conditional.<br>• **Supplement.** Update its title and date, align its nomenclature ("error realizations", "baseline", "matched reference"), and label historical strength tables as historical.<br>• **Target journal.** Confirm it: Reviewer 1 assessed JKPS, while the earlier recommendation was NIM A. | R3-BTS-07; R2C-09 | none (author input) | Declarations and supplement are consistent; no invented deposit, DOI or approval |
| R4-BTS-09 | **Reconciliation and response.**<br>• **Response.** Write one new point-by-point response covering both round-3 reports, mapping each R3-BTS and R2C item to R4-BTS tasks. Record the changes made after the Reviewer 2 response: the title, the baseline framing, the nomenclature and the removed sections. Answer Reviewer 2's questions 1–5.<br>• **Evidence and builds.** Update the claim ledger and run the audit. Add model tests for any changed method, rebuild the article and supplement cleanly, update hashes and freeze a new attachment. | R3-BTS-08; R2C-10 | checks only | Responses and manuscript agree; audit and `--verify` pass; earlier responses unchanged |

### B — strongly recommended or conditional

| ID | Task | From | Computation | Completion criterion |
| :--- | :--- | :--- | :---: | :--- |
| R4-BTS-10 | **Steering and pairing assumptions.**<br>• **Instrumentation.** State the assumed eleven horizontal readings and the independent powering of the six trims. Repeat the correction with a reduced monitor set (one per triplet plus the septum), and with four knobs if b1–b3 share a supply.<br>• **Vertical exit.** Report the vertical exit centroid rms (position and angle) in Table 6.<br>• **Pairing.** Disclose that the BPM reading errors are seeded per design (`[bpm_seed, machine, design_index]`), while static errors, shots and particles are shared. State that the loss objective excludes static residuals and the beta-factor mixture used in testing.<br>• **Wording.** Correct "the angle spread falls" (364 → 367 µrad). | R2C-05; R3-BTS-06 | tracking (small) | Assumptions stated; reduced-instrumentation row; vertical centroid reported; pairing reproducible |
| R4-BTS-11 | **Discrete aperture checking.** State that apertures are checked at element entrances and the line end, with interior envelopes on an observation copy. Present the loss as loss on the declared checked boundaries. Only if a continuous-channel interpretation is retained, test representative tail shots at intermediate locations on an auxiliary copy. | R3-BTS-03 | none, or targeted tracking | The claim matches the observation locations; the source lattice is unchanged |
| R4-BTS-12 | **Dispersion-free exit.** Track the best dispersion-free setting on the fresh realizations, or quote its gain only as an order of magnitude with a non-Gaussian-tail caveat. Explain why the configured exit inherits 80.9 mm / 47.5 mrad. Reviewer 1 accepts the analytic status if it is labelled. | R2C-06; R3-BTS-06 (analytic status) | tracking (optional) | Tracked loss, or a qualified analytic statement; origin of the dispersion stated |

### C — editorial

| ID | Task | From | Computation | Completion criterion |
| :--- | :--- | :--- | :---: | :--- |
| R4-BTS-13 | **Length and structure.**<br>• Move Section 3.4 and Tables 3–4 to the supplement, keeping a one-sentence summary. Move the last Section 2.2 sentence (historical ensembles) with them.<br>• Give Eq. (5) in its one-sided form, or drop it.<br>• Collapse the identical roll rows of Table 8, and add the R4-BTS-01 rows. | R2C-07 | none | Shorter main text; no symmetric-station equation applied to a one-sided edge |
| R4-BTS-14 | **Wording.**<br>• Remove the redundant Luo2026 sentence and the repeated outline in the Introduction.<br>• Write "septum entrance" / "line end (m4)" in Section 4.1, since "entrance" elsewhere means m1. | R2C-08 | none | Text |

## Where the reviewers differ, and how this register resolves it

| Topic | Reviewer 1 | Reviewer 2 | Consolidated decision |
| :--- | :--- | :--- | :--- |
| Phase-advance search | Wording is sufficient; no further optimization required | Constrained μ_x scan required (A) | Do both (R4-BTS-05). The scan satisfies Reviewer 2 and also gives Reviewer 1 an honest description of the search. |
| Baseline comparison | Acceptable as an envelope/matching change, correctly not a loss claim | Circular and should not lead the abstract | Keep Table 5 with provenance; remove it from the headline (R4-BTS-07) |
| Dispersion-free exit | Analytic status acceptable if labelled | Track it, or quote only the order of magnitude (B) | B; the author chooses tracking or a qualified statement (R4-BTS-12) |
| Jitter level | Not raised | Main objection | A (R4-BTS-01); Reviewer 1's definition of J is folded in |
| Round-aperture bounds | Main objection | Not raised | A (R4-BTS-03) |

## Computation summary

| Kind | Tasks |
| :--- | :--- |
| Analytic only | R4-BTS-01, R4-BTS-02, R4-BTS-03 (unless outputs change) |
| New matching | R4-BTS-05 (μ_x scan, both exit targets) |
| New tracking | R4-BTS-05 (fresh test of the chosen point); R4-BTS-10 (reduced-monitor and four-knob steering); R4-BTS-12 (optional); R4-BTS-03 and R4-BTS-11 (conditional) |
| None | R4-BTS-04, 06, 07, 08, 09, 13, 14 |

## Suggested order

1. **R4-BTS-03 and R4-BTS-04.** Settle whether the loss method or the error interpretation changes any selected
   number.
2. **R4-BTS-01 and R4-BTS-02.** These analytic sweeps may shift the emphasis of the paper.
3. **R4-BTS-05.** The μ_x scan and fresh test. If the scan changes the chosen setting, rerun the test before
   R4-BTS-10.
4. **R4-BTS-10 to R4-BTS-12.** The model checks.
5. **R4-BTS-06 and R4-BTS-07.** The text and framing, once the numbers are final.
6. **R4-BTS-13 and R4-BTS-14**, then **R4-BTS-08** (with author input), then **R4-BTS-09** last.

## Coordination with the companion NKM manuscript

- **R4-BTS-01.** The booster jitter (0.5 mm / 0.2 mrad at m1) is shared with the NKM paper. Any change of level or
  justification should be made in both papers.
- **R4-BTS-02 and R4-BTS-12.** These concern the injected-beam geometry and the dispersion that the NKM paper uses.
- **R4-BTS-10.** Its vertical exit centroid is the input to the static vertical injection error in the NKM paper.

Completing these tasks is a basis for reassessment by both reviewers. It is not acceptance, and it does not
authorize submission, upload or a remote push.
