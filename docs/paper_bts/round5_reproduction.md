# Round-five BTS reproduction

Round 5 executes the [round-5 plan](reviews/revision_round_04_plan_for_review_round_04.md) (milestones 283–292).
The environment is the same as in rounds 2–4: Python 3.11.9, pyAT 0.7.2.dev26, NumPy 2.4.6 and SciPy 1.17.1, with
this package installed.

`round5_protocol.json` was declared before the runs. It records:
- the shared reading errors;
- the primary estimator and population;
- the duplicate-configuration check;
- the angle-weighted layout;
- the edge study.

The first `final_test/` and `layouts/` runs failed before producing output and hold only a configuration. The cause
was worker pickling of the imported round-4 runner. They are retained, and the stages were rerun unchanged with the
`_b` suffix. The BTS lattice is not changed.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C=results/bts_round5_campaign_20261031
python scripts/run_bts_round5.py --stage final_test --output-dir $C/final_test_b
python scripts/run_bts_round5.py --stage layouts    --output-dir $C/layouts_b
python scripts/run_bts_round5.py --stage edge_study --output-dir $C/edge_study
python scripts/export_bts_round5_assets.py
python scripts/export_bts_round4_assets.py          # corrected provenance paths, uniform Table 7 format
python scripts/audit_bts_evidence.py
python scripts/package_bts_revision.py --verify
python -m pytest tests/test_bts_round3.py tests/test_bts_round4.py -q
```

| Stage | Task | Selected output | Run time (8 workers) |
| :--- | :--- | :--- | :--- |
| final_test_b | R5-BTS-01/02 | `final_test_b/final_test.json`, `raw_machines.json` | 1 min |
| layouts_b | R5-BTS-01/06 | `layouts_b/layouts.json`, `raw_machines.json` | 2 min |
| edge_study | R5-BTS-05 | `edge_study/edge_study.json` | 8 min |

**Selected results.** They are installed in `generated/round5*` and `figures/round5_jitter_transfer.pdf`; claims
BR5-01 to BR5-10 are in `claim_evidence.csv`.
- **Shared reading errors.** A duplicate configuration gives identical results. The round-3 loss-based and edge
  settings lose identical counts (942 of 1.2 million particles).
- **Matched-reference rows.** They reproduce round 4 exactly. NumPy's `SeedSequence` pads zeros, so
  `[seed, realization]` equals the old `[seed, realization, 0]` draw.
- **Gain.** The primary gain, a ratio of mean jitter-integrated losses with a paired realization bootstrap, is 4.48
  [4.33, 4.63]. The layout population gives 4.59 [4.46, 4.72].
- **Validation:**

  | Setting | Observed | Expected (conditional) | z |
  | :--- | ---: | ---: | ---: |
  | Matched reference | 11 673 | 11 705 | −0.3 |
  | Low beta | 10 104 | 10 154 | −0.5 |
  | Loss-based | 942 | 880.5 | +2.1 |
  | Dispersion-free | 1 | 0.51 | — |

  The dispersion-free integrated loss corresponds to 76 particles.
- **Edge.** The lower μ_x edge is 200.2°, 194.9°, 189.5° and 184.1° for exit D′ of 47.5, 32, 16 and 0 mrad, with
  no bound active. With D = 0 at the configured D′ it is 203.2°, with the vertical peak-beta limit active.
- **Angle-weighted steering.** The loss-based exit-angle rms goes from 0.413 to 0.411 mrad, and the losses are
  unchanged.

Bitwise identity across library versions or thread settings is not claimed. No public deposit or journal submission
is implied.
