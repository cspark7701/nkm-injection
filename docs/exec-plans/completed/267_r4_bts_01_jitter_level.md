# Milestone 267 — R4-BTS-01: booster jitter level and sweep

Completed: 2026-10-30. Round-4 task R4-BTS-01 (Reviewer 2 R2C-01; Reviewer 1 R3-BTS-01, definition of J).

**Infrastructure.** All round-4 stages reuse it.
- **Protocol:** `docs/paper_bts/round4_protocol.json`, declared before the runs.
- **Module:** `src/nkm_injection/bts_round4.py`, with steering layouts and phase-constrained residuals.
- **Runner:** `scripts/run_bts_round4.py`, with the stages jitter, blade, phase_scan, layouts and final_test.
- **Exporter:** `scripts/export_bts_round4_assets.py`.
- **Tests:** `tests/test_bts_round4.py`, six tests. The full layout reproduces round-3 steering exactly.

**Observable added.** Each steered realization now also gets a jitter-integrated loss: the exact Gaussian average
of Eq. (7) over the entrance jitter on its steered line, with no shot sampling.
- The first jitter/blade runs (`jitter/`, `blade/`) are retained.
- They showed that the mean over 600 sampled shots cannot resolve small losses, so the protocol was amended and
  the stages rerun as `jitter_b/` and `blade_b/`.

**Results.** `results/bts_round4_campaign_20261030/jitter_b`: 200 fresh steered realizations, seeds 94001–94005,
analytic.
- **Jitter in beam-size units.** At m1 the beam is 0.379 mm / 91 µrad, so the assumed jitter is 1.3 / 2.2 beam
  sizes, and the mean centroid action is 54 times the emittance. At the exit it is 4.0σ (matched reference) and
  3.2σ (loss-based).
- **Full level.** The losses are 1.31 % and 0.28 %, against 1.28 % and 0.27 % on the error-free line. The static
  residual adds only 2 % and 5 %, and the gain is 4.7.
- **Half level.** The losses fall by more than two orders of magnitude, and the gain is 31.
- **Realistic levels.** At ×0.1–0.2 (13–44 % of the beam size), every setting loses at most 3 × 10⁻¹¹, and the
  loss-based setting is no better.

**Correction to R4-BTS-04.** R4-BTS-04 said the static residual raised the loss 1.8–2.6-fold; that is withdrawn.
The tracked population means vary by setting:
- matched reference: 1.24–2.30 % (error-free 1.28 %);
- loss-based: 0.69 % tracked, against 0.27 % error-free.

These differences reflect the jitter tail sampled by 600 shots, not the static residual. Sections 3.2 and 4.2 now
say so.

**Article changes.**
- **Section 2.4:** the jitter in beam-size units, with the 0.5 mm / 0.2 mrad called a stress level. No KLS
  specification is available; the source remains an author input.
- **Section 4.5:** the jitter-integrated observable and new Table 9 (jitter-level sweep). The loss reduction is
  stated as a property of large booster jitter.
- **Discussion:** the jitter regime of the results.

The abstract is rewritten in R4-BTS-07. The isolated build is clean; the installed PDF is rebuilt in R4-BTS-09.
22 round-3/round-4 tests pass. Protected files are unchanged.
