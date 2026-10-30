# Round-four BTS numerical and article reproduction

Round 4 executes the [consolidated tasks](reviews/round4_consolidated_revision_tasks.md) R4-BTS-01 to R4-BTS-14
(milestones 265–278). The environment is the same as in rounds 2–3: Python 3.11.9, pyAT 0.7.2.dev26, NumPy 2.4.6
and SciPy 1.17.1, with this package installed. Every stage writes a new directory, refuses an existing one, and
records the protocol, the environment and the source SHA-256 in its `configuration.json`.

The protocol (`round4_protocol.json`) was declared before the campaigns. Its amendments are recorded in the
protocol, each before the outputs it affects:
- **Jitter-integrated loss:** added after the first jitter/blade runs.
- **Phase-scan budget:** reduced after the first scan was stopped.
- **Fresh test:** `edge_best` added before the test ran.

The BTS lattice is not changed.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C=results/bts_round4_campaign_20261030
python scripts/run_bts_round4.py --stage jitter     --output-dir $C/jitter_b
python scripts/run_bts_round4.py --stage blade      --output-dir $C/blade_b
python scripts/run_bts_round4.py --stage phase_scan --output-dir $C/phase_scan_b
python scripts/run_bts_round4.py --stage final_test --output-dir $C/final_test_b --scan-file $C/phase_scan_b/phase_scan.json
python scripts/run_bts_round4.py --stage layouts    --output-dir $C/layouts_b
python scripts/export_bts_round4_assets.py
python scripts/export_bts_round3_assets.py --only sensitivity
python scripts/export_bts_at_figures.py --output-dir <new>/at                  # then install the figures
python scripts/export_bts_round3_assets.py --clearance-figure-dir <new>/clearance
python scripts/audit_bts_evidence.py
python scripts/package_bts_revision.py --verify
python -m pytest tests/test_bts_round3.py tests/test_bts_round4.py -q
```

The R4-BTS-03 recheck reruns all round-3 stages with the exact round-aperture loss into
`results/bts_round4_r403_exact_20261030`. `scripts/compare_bts_round3_campaigns.py` then compares 66 selected
observables with `results/bts_journal_campaign_r3b_20261015`; all are identical.

| Stage | Task | Selected output | Approximate run time (8 workers) |
| :--- | :--- | :--- | :--- |
| jitter_b | R4-BTS-01 | `jitter_b/jitter.json` | 1 min |
| blade_b | R4-BTS-02 | `blade_b/blade.json` | 5 min |
| phase_scan_b | R4-BTS-05/12 | `phase_scan_b/phase_scan.json` | 26 min |
| final_test_b | R4-BTS-05/12 | `final_test_b/final_test.json`, `raw_machines.json` | 2 min |
| layouts_b | R4-BTS-10 | `layouts_b/layouts.json`, `raw_machines.json` | 2 min |

**Retained, not used.** These directories are kept on disk but hold no selected result:
- `jitter/` and `blade/`: the first runs, without the jitter-integrated observable;
- `phase_scan/`, `layouts/` and `final_test/`: stopped or failed runs, which hold only a configuration.

**Selected results.** They are installed in `generated/round4_*` and `figures/round4_*`; claims BR4-01 to BR4-14
are in `claim_evidence.csv`.
- **Jitter.** The assumed booster jitter is 1.3 / 2.2 beam sizes at m1, and the centroid action is 54 times the
  emittance.
  - At that level, the matched reference's jitter-integrated loss is 1.31 % (1.28 % error-free).
  - At 0.1–0.2 of it, every setting is at most 3 × 10⁻¹¹.
- **Blade distance.** A loss below 0.1 % needs d_b ≥ 2.05 mm (matched reference) or 1.64 mm (loss-based).
- **Phase advance.**
  - Configured exit: the lower edge, 200.17°, has no active bound; the upper edge, 232.0°, is set by the 60 m
    peak-beta limit.
  - Dispersion-free exit: the range is 187.2–214.5°, and q22 at its bound sets the upper edge.
  - The error-free loss depends on μ_x alone.
- **Second fresh test.** The tracked losses are 0.97 % (matched reference), 0.13 % (edge) and 0.085 % (round-3
  loss-based, optically identical to the edge). The dispersion-free setting loses 1 of 1.2 million particles.
- **Steering layouts.** The full layout reproduces round 3 (20 100 lost particles). Reduced monitors change nothing;
  series bends give 0.44 mrad of exit-angle spread. The uncorrected vertical exit centroid is 1.12 mm / 0.10 mrad.

Bitwise identity across library versions or thread settings is not claimed. Compare against the installed summaries
at the stated precision. No public deposit or journal submission is implied.
