# Round-5 NKM reproduction

The model, scales and paired estimands were frozen in [round5_protocol.json](round5_protocol.json) before tracking. The [companion audit](round5_companion_comparison.md) records the nominal strength agreement and the different dipole-error correlation. G7 approval/access/delivery stays separate.

## Environment

This execution uses `/home/cspark/Work/simulation_codes-working/miniforge3/envs/pyat-dev/bin/python`, with `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MPLBACKEND=Agg` for tracking. The final frozen attachment records exact package versions and the committed source snapshot. No package installation or network access is needed in the prepared scientific environment.

## Declared tracking and saved-output analysis

Run from the repository root:

```bash
NKM_PYTHON=/home/cspark/Work/simulation_codes-working/miniforge3/envs/pyat-dev/bin/python
"$NKM_PYTHON" scripts/run_round5_campaign.py --prepare-only
"$NKM_PYTHON" scripts/run_round5_campaign.py --workers 8
```

The driver uses `results/journal_campaign_06/`, with `g2_xy_0p1`, `g2_xy_0p25` and `g2_xy_0p5`. Zero/full endpoints are identified historical two-plane runs. An existing new-scale output is rejected unless `--resume` is supplied; resumption then uses the underlying tracker's exact input/source checkpoint check. Do not alter the historical protocol or delete outputs to force a resume.

For a separate reproduction without overwriting the selected campaign, supply
`--output-dir results/nkm_round5_tracking_new` to the driver, and later
`--campaign-dir results/nkm_round5_tracking_new` to the analyzer. The model and
scales remain fixed by the declared protocol. This option is for a fresh
reproduction, not a way to bypass a mismatched checkpoint.

After all scales complete:

```bash
"$NKM_PYTHON" scripts/analyze_round5_jitter.py \
  --output results/journal_campaign_06/g2_jitter_analysis.json
"$NKM_PYTHON" scripts/make_round5_manifest.py \
  --output docs/paper/revision_manifest_round5.json
```

Both output files must be new. For repeated post-processing, choose a fresh result filename instead of replacing the selected record. The analyzer audits complete job fields, latent non-jitter errors, scaled jitter, particle/ring identities and particle/loss reconciliation before computing paired intervals. The common dipole-field error, adopted point, native ring tracking and all non-jitter inputs remain unchanged.

The one-point noninferiority comparison is NKM(scale) minus NKM(zero), under ideal two-plane steering. Its lower central-95% endpoint must exceed −1 percentage point. The NKM-minus-dipole gap and its paired change are separate estimands. Pointwise intervals do not define a continuous threshold or a hardware tolerance.

## Figures, macros and PDFs

Once the round-5 selection exists:

```bash
"$NKM_PYTHON" scripts/build_revision_figures.py \
  --manifest docs/paper/revision_manifest_round5.json \
  --output-dir results/nkm_round5_rebuild_new
"$NKM_PYTHON" scripts/build_submission_package.py \
  --layout one-column --output-dir results/nkm_round5_source_one_new
"$NKM_PYTHON" scripts/build_submission_package.py \
  --layout two-column --output-dir results/nkm_round5_source_two_new
```

Use fresh output directories. Figure/macro regeneration above does not install changes; it can be compared with the selected `generated/journal_macros.tex`. The submission builder stages the installed manuscript sources/macros/figures, includes the round-5 support documents when present, and builds the supplement in both layouts' packages. Installing regenerated assets or PDFs is a deliberate maintenance step, not necessary to verify an existing selection.

## Frozen evidence and portable reanalysis

The final attachment is built only from committed sources:

```bash
"$NKM_PYTHON" scripts/build_evidence_bundle.py \
  --manifest docs/paper/revision_manifest_round5.json \
  --output-dir results/nkm_round5_evidence_new --builder revision --verify
```

Verify the attachment's hash inventory and use its `REBUILD.md` to regenerate the macros with the archived builder on bundled evidence alone. To reanalyze the saved raw ensembles, supply the extracted evidence root explicitly:

```bash
"$NKM_PYTHON" /path/to/extracted/code/scripts/analyze_round5_jitter.py \
  --repo-root /path/to/extracted/evidence --output /tmp/new_round5_analysis.json
```

The output must not exist. Absolute original job paths are identity strings in the pairing audit; this reanalysis reads selected files through the explicit evidence root and does not execute tracking or need the original checkout. Earlier attachments remain historical and do not contain the new scan. No archive is uploaded by these commands.

## Selected execution

All 150 new realizations are complete. The five-level paired analysis verifies configuration/draw/particle/ring identities and reconciles loss counts. The new manifest selects 272 artifact keys. No nonzero tested level passes the declared one-point loss test; the [result note](round5_jitter.md) gives exact costs and model gaps. The installed article layouts and supplement are 36/18/7 pages; the extracted abstract contains 250 words. [Scientific source/PDF identities](round5_final_identity.json) identify these installed assets.

The launch implementation identity preserves commit `65bf56d` and original script hashes. Subsequent portable CLI/reporting checks (`fd4b96b`) do not change the tracking physics or launched commands. Thirty relevant tests and the earlier 774-test full suite pass. Frozen-source attachment verification follows from a clean committed checkpoint; its digest and isolated reanalysis result will be recorded after that check. Earlier archives remain historical.
