# Round-three (Reviewer 2) numerical and article reproduction

Environment as for round 2 (Python 3.11.9, pyAT 0.7.2.dev26, NumPy 2.4.6, SciPy 1.17.1), with this package
installed. Every stage writes a new directory and refuses an existing one. Its `configuration.json` records:
- the protocol;
- the environment;
- SHA-256 of the round-3 sources.

The protocol (`round3_protocol.json`) was declared before the campaigns. Its `steering_amendment` entry records the
one post-hoc change (the corrector/monitor layout) and was written before the test and sensitivity campaigns ran.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C=results/bts_journal_campaign_r3_20261015
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
| steering | R2B-03 | `steering/steering.json`, `raw_machines.json` (three variants) |
| robust | R2B-04 | `robust/robust.json` (frozen settings) |
| test | R2B-04 | `test/test.json`, `raw_machines.json` |
| exit | R2B-05 | `exit/exit.json` |
| sensitivity | R2B-06 | `sensitivity/sensitivity.json` |

**Retained runs.**
- `steering_declared_only/`: the first steering run with the declared layout, retained as the evidence for the
  amendment.
- In the rerun, BPM-error draws are seeded per design. The declared variant therefore uses different BPM draws from
  the first run: reference loss 2.39 % in both runs (identical draws), low beta 2.44 % in the rerun against 2.12 % in the first run. This
  spread is a BPM-draw effect within the declared layout and does not affect the amended results.

**Selected results** (installed by the exporter in `generated/round3_*`; claims BR3-01 to BR3-13 in
`claim_evidence.csv` and `evidence_manifest.json`, verified by `audit_bts_evidence.py`):
- **Active restriction:** the injection-septum channel at the blade, 0.648 mm, for every quadrupole setting.
- **Steering:** loss 10.08 % → 2.39 % (declared) → 1.60 % (amended).
- **Reachable μx:** 200.2–232.0°; the loss-based setting sits at 200.2°.
- **Fresh test** (tracked loss): reference 2.32 %, low beta 2.15 %, loss-based 0.66 %. Loss-based minus reference:
  −1.66 [−2.42, −0.99] percentage points.
- **Dispersion-free exit:** feasible; μx 187.7–214.2°; best predicted loss 4.1×10⁻⁵.
- **Sensitivity:** the roll level has no effect, the energy jitter little, and the ranking is unchanged.

Bitwise identity across library versions or thread settings is not claimed. Compare against the installed summaries
at the stated precision. No public deposit or journal submission is implied.
