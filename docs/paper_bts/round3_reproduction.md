# Round-three (Reviewer 2) numerical and article reproduction

Environment as for round 2 (Python 3.11.9, pyAT 0.7.2.dev26, NumPy 2.4.6, SciPy 1.17.1), with this package
installed. Every stage writes a new directory and refuses an existing one. Its `configuration.json` records:
- the protocol;
- the environment;
- SHA-256 of the round-3 sources.

The protocol (`round3_protocol.json`) was declared before the campaigns and revised once (revision 2, 2026-10-15) at
the author's instruction that the BTS lattice must not be changed. All stages were then rerun in
`results/bts_journal_campaign_r3b_20261015`:
- on the unchanged 36-element line, with apertures as attributes of existing elements and no slicing;
- with steering by horizontal field trims of the six existing dipoles, read at existing element boundaries;
- with no vertical correction.

The earlier campaign with added corrector elements (`results/bts_journal_campaign_r3_20261015`) is superseded; its
layouts are recorded under `superseded_steering` in the protocol and are not used in the article.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C=results/bts_journal_campaign_r3b_20261015
python scripts/run_bts_round3.py --stage apertures   --output-dir $C/apertures
python scripts/run_bts_round3.py --stage phase       --output-dir $C/phase --workers 8
python scripts/run_bts_round3.py --stage steering    --output-dir $C/steering --workers 8
python scripts/run_bts_round3.py --stage robust      --output-dir $C/robust --phase-file $C/phase/phase.json
python scripts/run_bts_round3.py --stage test        --output-dir $C/test --robust-file $C/robust/robust.json --workers 8
python scripts/run_bts_round3.py --stage exit        --output-dir $C/exit --phase-file $C/phase/phase.json
python scripts/run_bts_round3.py --stage sensitivity --output-dir $C/sensitivity --robust-file $C/robust/robust.json --workers 8
python scripts/export_bts_round3_assets.py
python scripts/audit_bts_evidence.py
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/<new>/paper --supplement-build-dir results/<new>/supplement
python -m pytest tests/test_bts_round3.py -q
```

| Stage | Task | Selected output |
| :--- | :--- | :--- |
| apertures | R2B-01 | `apertures/apertures.json` |
| phase | R2B-04/05 | `phase/phase.json` (349 configured and 115 dispersion-free solutions) |
| steering | R2B-03 | `steering/steering.json`, `raw_machines.json` (uncorrected and dipole-trim steering) |
| robust | R2B-04 | `robust/robust.json` (frozen settings) |
| test | R2B-04 | `test/test.json`, `raw_machines.json` |
| exit | R2B-05 | `exit/exit.json` |
| sensitivity | R2B-06 | `sensitivity/sensitivity.json` |

**Retained runs.** `results/bts_journal_campaign_r3_20261015/` (added correctors, including
`steering_declared_only/`) is kept on disk as a superseded record. The apertures stage of the new campaign was rerun
once after fixing the interior-minimum exclusion of the end marker m4; the other stage outputs are first runs.

**Selected results** (installed by the exporter in `generated/round3_*`; claims BR3-01 to BR3-13 in
`claim_evidence.csv` and `evidence_manifest.json`, verified by `audit_bts_evidence.py`):
- **Active restriction:** the injection-septum channel at the blade, 0.648 mm, for every quadrupole setting.
- **Steering** (dipole trims): loss 10.08 % → 1.68 % for the reference (1.47 % for low beta). The Gaussian
  prediction agrees with tracking within 0.4 %.
- **Reachable μx:** 200.2–232.0°; the loss-based setting sits at 200.2°.
- **Fresh test** (tracked loss): reference 2.30 %, low beta 2.27 %, loss-based 0.69 %. Loss-based minus reference:
  −1.61 [−2.33, −0.96] percentage points.
- **Dispersion-free exit:** feasible; μx 187.7–214.2°; best predicted loss 4.1×10⁻⁵.
- **Sensitivity:** the roll level has no effect, the energy jitter little, and the ranking is unchanged.

Bitwise identity across library versions or thread settings is not claimed. Compare against the installed summaries
at the stated precision. No public deposit or journal submission is implied.
