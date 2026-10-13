# BTS optics manuscript

Round-two one-column article for prospective JKPS submission: [paper.tex](paper.tex), [paper.pdf](paper.pdf), [supplement.tex](supplement.tex) and [supplement.pdf](supplement.pdf). The article explains fixed-entrance saturation and compares reference, spatially refined low-beta and nominal direct-clearance settings under explicit hypothetical restrictions. Higher mean clearance remains distinct from smaller loss probability, real chamber transmission and ring capture.

- [Review history and current response](reviews/README.md)
- [Frozen original identity](round2_identity.json) and [new protocol](round2_protocol.json)
- [Station mechanism](round2_station_mechanism.md), [clearance accuracy](round2_clearance_accuracy.md) and [interior extrema](round2_spatial_extrema.md)
- [Frozen strategies/new machines](round2_strategy_comparison.md) and [inference/event definitions](round2_inference.md)
- [Beam and boundaries](beam_and_boundaries.md), [literature verification](literature_comparison.md), [claim ledger](claim_evidence.csv) and [evidence manifest](evidence_manifest.json)
- [Exact reproduction commands](round2_reproduction.md), [execution status](round2_task_status.md), [author declarations](author_declarations_round2.md) and [submission checklist](submission_checklist.md)

Original R1 campaign and all prior reports are preserved, including the restored older BTS-branch reviews. New comparisons use200 independently drawn machines with three shots each and2000 particles per shot,totalling10.8 million particle transports across nine combinations. All restrictions, bounds and errors remain labelled assumptions. Invalid preliminary shared-aperture runs are retained and excluded.

Funding and acknowledgments are author-deferred; competing interests are confirmed as none. Final scientific approval and actual referee delivery remain pending. R2-BTS-08 can only be fully closed after these author actions; local execution does not imply journal acceptance or submission.

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
