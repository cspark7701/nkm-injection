# BTS optics manuscript

Round-three one-column article for prospective JKPS submission, *Optical matching and beam loss in a booster-to-storage-ring transfer line*: [paper.tex](paper.tex), [paper.pdf](paper.pdf),
[supplement.tex](supplement.tex) and [supplement.pdf](supplement.pdf). It responds to the
[Reviewer 2 report](reviews/reviewer2_bts_20261015_main_report.md); see the
[response](reviews/author_response_reviewer2_20261015.md), the [round-3 protocol](round3_protocol.json) and the
[round-3 reproduction guide](round3_reproduction.md).

**Findings.**
- With element-wise apertures, the injection-septum blade limits the line, with a nominal clearance independent of
  the quadrupoles.
- With matched ends, booster jitter reaches the exit through the horizontal phase advance alone.
- Steering, a Gaussian loss observable validated by tracking, a loss-based setting tested on fresh machines and a
  dispersion-free exit complete the study.

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

Funding and acknowledgments were supplied by the author on 2026-10-19 (NRF Grant No. RS-2022-00143178); competing interests are confirmed as none. The data-availability statement is final (2026-10-20): code in the public repository, selected raw data and reproduction material in a referee attachment, available on reasonable request, with no public deposit. The referee attachment is prepared and verified (milestone 247); handing it to the journal at submission is the author's step. Final scientific approval remains pending, and R2-BTS-08 closes with it. Local execution does not imply journal acceptance or submission.

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
