# BTS optics manuscript

Current state (2026-10-31): the round-4 revision is executed. It answers both round-3 reports, from Reviewer 1
(focused major revision) and Reviewer 2 (major revision), through the
[consolidated tasks](reviews/round4_consolidated_revision_tasks.md) R4-BTS-01 to 14 (milestones 265–278). See the
[joint response](reviews/author_response_round4_20261031.md), the [round-4 protocol](round4_protocol.json) and the
[round-4 reproduction guide](round4_reproduction.md). No reviewer has reassessed it yet, and the author's scientific
approval is pending.

Round-four one-column article (19 pages, with a 9-page supplement), *Optical matching and beam loss in a
booster-to-storage-ring transfer line for nonlinear-kicker injection at the Korea Light Source*:
[paper.tex](paper.tex), [paper.pdf](paper.pdf), [supplement.tex](supplement.tex) and
[supplement.pdf](supplement.pdf).

**Findings.**
- **Nominal blade clearance.** Once the line is matched, the injection-septum blade is the active restriction, and
  its nominal clearance is the same for every matched setting.
- **Loss and phase advance.** The blade loss of a matched setting depends on the horizontal phase advance alone. It
  is smallest at the lower edge of the matched range (200.17°), which no strength bound or peak-beta limit sets.
- **Best-found setting.** It reduces the tracked loss 3- to more than 10-fold on independent error realizations, at
  13 % more exit-angle jitter.
- **Jitter regime.** These loss numbers hold at the assumed booster jitter, a stress level of 1.3 / 2.2 beam sizes.
  At 0.1–0.2 of it, every setting loses at most 3 × 10⁻¹¹.
- **Supporting results.**
  - The steered static residual adds only 2–5 %.
  - The round-aperture loss is exact.
  - Reduced monitors change nothing; series-powered bends raise the angle spread.
  - The dispersion-free exit is tracked.
- **Baseline.** The unmatched starting point (Figures 2–3) is not a competing design.

**Open author decisions:** the target journal (JKPS or NIM A), the data-availability wording, a source for the
booster jitter, and final approval (see the [submission checklist](submission_checklist.md)).

The earlier round-two article (four-station model, hypothetical restrictions) is preserved in the supplement and the
records below.

## Round-two records
The round-two article explained fixed-entrance saturation and compares reference, spatially refined low-beta and nominal direct-clearance settings under explicit hypothetical restrictions. Higher mean clearance remains distinct from smaller loss probability, real chamber transmission and ring capture.

- [Review history and current response](reviews/README.md)
- [Frozen original identity](round2_identity.json) and [new protocol](round2_protocol.json)
- [Station mechanism](round2_station_mechanism.md), [clearance accuracy](round2_clearance_accuracy.md) and [interior extrema](round2_spatial_extrema.md)
- [Frozen strategies/new machines](round2_strategy_comparison.md) and [inference/event definitions](round2_inference.md)
- [Beam and boundaries](beam_and_boundaries.md), [literature verification](literature_comparison.md), [claim ledger](claim_evidence.csv) and [evidence manifest](evidence_manifest.json)
- [Exact reproduction commands](round2_reproduction.md), [execution status](round2_task_status.md), [author declarations](author_declarations_round2.md) and [submission checklist](submission_checklist.md)

Original R1 campaign and all prior reports are preserved, including the restored older BTS-branch reviews. New comparisons use200 independently drawn machines with three shots each and2000 particles per shot,totalling10.8 million particle transports across nine combinations. All restrictions, bounds and errors remain labelled assumptions. Invalid preliminary shared-aperture runs are retained and excluded.

Funding and acknowledgments were supplied by the author on 2026-10-19 (NRF Grant No. RS-2022-00143178); competing interests are confirmed as none. The data-availability statement is final (2026-10-20): code in the public repository, selected raw data and reproduction material in a referee attachment, available on reasonable request, with no public deposit. The referee attachment is prepared and verified (milestone 247); handing it to the journal at submission is the author's step. Final scientific approval remains pending, and R2-BTS-08 closes with it. Local execution does not imply journal acceptance or submission. On 2026-10-30, at the author's request, the article's generative-assistance and data-availability statements and Appendix A (evidence and reproducibility) were removed; the referee attachment and the repository are unchanged.

To prepare a fresh portable attachment after asset verification:

```bash
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --round2-package-dir results/new_round2_attachment
```

Never reuse an existing output directory. Use the scientific environment listed in the reproduction guide. The attachment is local, not a public deposit.

The [entrance/exit phase-space figure](figures/phase_space.pdf) compares the
shared initial beam with reference and refined low-beta exits in both planes.
It uses 20,000 nominal particles, seed 83001, and native AT covariance ellipses;
[reproduction details](round2_reproduction.md#nominal-phase-space-distributions)
identify the new diagnostic independently of the error campaign.
