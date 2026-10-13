# Round2 numerical and article reproduction

Use the recorded Python3.11.9,pyAT0.7.2.dev26+g4701d48c.d20260831,NumPy2.4.6,SciPy1.17.1 environment with this package installed. Paths below are relative to the repository or extracted referee root; each output directory must be new. The selected original R1 and new R2 raw records are supplied in the local attachment.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python scripts/audit_bts_evidence.py
python scripts/run_bts_round2.py --stage stations --output-dir results/new_r2/stations
python scripts/run_bts_round2.py --stage accuracy --output-dir results/new_r2/accuracy
python scripts/run_bts_round2.py --stage spatial --output-dir results/new_r2/spatial
python scripts/run_bts_round2.py --stage designs --spatial-file results/new_r2/spatial/spatial.json --output-dir results/new_r2/designs
python scripts/run_bts_round2.py --stage comparison --design-file results/new_r2/designs/designs.json --output-dir results/new_r2/comparison
python scripts/audit_bts_round2_inference.py --output-dir results/new_r2/inference
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/new_r2/article --supplement-build-dir results/new_r2/supplement
python -m pytest tests/test_bts_round2.py tests/test_bts_journal.py tests/test_bts_lattice.py tests/test_bts_evidence_audit.py -q
```

Thread limits above avoid oversubscription; assess numerical agreement at declared tolerances rather than assuming bitwise identity across runtime threading configurations.

The inference command defaults to reconstruction of the selected archived campaign, whose exact arrays are supplied. To audit a fresh campaign, pass `--campaign-dir results/new_r2`. The comparison defaults to the selected frozen designs if no `--design-file` is supplied; use the explicit argument above to route fresh optimization into fresh evaluation. Spatial/design stages preserve original matching inputs and require the supplied R1 records. Different numerical library versions require validating tolerances rather than assuming bitwise identity.

`python scripts/export_bts_round2_assets.py` explicitly regenerates selected numerical tables and figures from installed summary exports and the selected spatial records. It does not overwrite source physics inputs. Exact stage source snapshots distinguish the original stage bytes from later CLI additions. `round2_identity.json` identifies the pre-review article and full original campaign; invalid shared-aperture outputs are retained separately and excluded from evidence claims.

No public deposition or submission is implied by local reproduction. Funding and acknowledgments remain author inputs; competing interests are author-confirmed as none. Final scientific approval and referee delivery remain pending.
