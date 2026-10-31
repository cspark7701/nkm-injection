# BTS implementation round 7: filename-round-5 follow-up

This execution answers the renamed [Reviewer 2 checklist](reviews/review_round_05_reviewer_02_tasks.md)
(R2F-BTS-01 to 06) and [Reviewer 1 follow-ups](reviews/review_round_05_reviewer_01_tasks.md)
(R1E-BTS-01 and 02). Original review-body round numbers are historical; no
previous response is replaced. See the [new joint response](reviews/review_round_05_author_response_to_reviewers_01_02.md).

No tracking or optimization campaign was rerun. The low-beta correction uses
the review's wording alternative; the new computation is saved-output
post-processing. The review's count of 20 loss-bearing shots is corrected to 16.
One shot carries about 70% of the excess, whose cause remains unresolved.

## Reproduce from the repository root

Use the project environment containing pyAT, NumPy, matplotlib and pytest, plus
the installed LaTeX tools. Choose fresh output directories for every command
that writes results:

```bash
python scripts/audit_bts_round7_shot_losses.py --output-dir results/new_bts_shot_audit
python scripts/export_bts_round4_assets.py --part blade
python scripts/export_bts_round4_assets.py --part phase
python scripts/audit_bts_evidence.py
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/new_bts_article \
  --supplement-build-dir results/new_bts_supplement
python -m pytest tests/test_bts_round2.py tests/test_bts_round3.py \
  tests/test_bts_round4.py tests/test_bts_evidence_audit.py tests/test_bts_journal.py \
  tests/test_bts_lattice.py tests/test_bts_figure_reference.py -q
python scripts/package_bts_round7_increment.py \
  --output-dir results/new_bts_increment --verify-dir results/new_bts_extracted
```

The shot audit writes `shot_loss_diagnostic.json` and `round7.tex`; compare them
with the installed `generated/round7_shot_losses.json` and `generated/round7.tex`.
It does not automatically overwrite selected manuscript files. The figure
export commands write existing generated paths; they preserve numerical data
and use the corrected setting labels.

## Selected execution and identities

- Reviewed source/PDF snapshot and input hashes:
  `results/bts_round7_revision_20261031/reviewed_snapshot` and `before_identity.json`.
- Shot diagnostic: `results/bts_round7_revision_20261031/shot_diagnostic`.
- Final article and supplement builds:
  `results/bts_round7_revision_20261031/final_article` and `final_supplement`.
  Installed lengths are 19 and 10 pages. Primary comparison: Table 5; layouts:
  Table 4; residuals: Table 7; earlier steering table: supplement Section 5.
- Referee increment:
  `results/bts_round7_revision_20261031/referee_increment_v2/bts_referee_round7_increment.tar.gz`.
- Fresh extraction and isolated check logs:
  `results/bts_round7_revision_20261031/extracted_verification_v2/verification.json`.
- Current selected hashes: `revision_selection.json`; the preceding 86-asset
  selection is retained as `round6_final_assets_sha256`.

The new increment overlays the original round-3 base attachment in
`results/bts_referee_attachment_20261020/bts_referee_attachment.tar.gz`. Its
`ROUND7_SHA256.json` records the base digest and every increment file; the
archive digest is in `referee_increment_v2/increment_sha256.txt`. Verification
checks that inventory, the evidence ledger, selected manuscript hashes and both
post-processing audits from the extracted root. No imports from the live
checkout are used for those isolated checks.

The evidence audit verifies 80 claims; 46 relevant tests pass. Exact count and
input identities do not certify nonlinear model accuracy, an unconditional
Gaussian tail or commissioned transmission. The declared stress level, fixed
beam covariance, discrete apertures and correction assumptions remain explicit.
Protected scientific inputs and earlier reports/responses are unchanged.
R5-BTS-09 decisions remain deferred; no external submission was performed.

The first `referee_increment` / `extracted_verification` attempt is retained. Its audit launch failed because a relative extraction path was resolved again after changing the working directory. The packager now resolves both output arguments before use; the selected successful attempt uses the `_v2` directories. No scientific input was changed by that fix.
