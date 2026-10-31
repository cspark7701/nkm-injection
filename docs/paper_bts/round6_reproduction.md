# BTS revision round 6: reproduction and verification

Revision round 6 answers Reviewer 2's review round 5 through
[R6-BTS-01 to 04](reviews/revision_round_06_plan_for_review_round_05.md).
This is a reporting and prose revision using the frozen round-4/round-5 campaigns.
No tracking or optimizer campaign was rerun.

The manuscript defines the 6.5% discrepancy relative to the observed count,
qualifies the phase-edge and steering conclusions, and distinguishes the earlier
sensitivities from the shared-reading primary population. The headline integrated
gain and raw simulation outputs are unchanged. See the
[point-by-point response](reviews/review_round_05_author_response_to_reviewer_02.md).

Use the existing project environment with NumPy, pyAT, matplotlib, pytest and
LaTeX available. The selected original runs retain their own environment/source
records. Run from the repository root, choosing new output paths for every build
and audit invocation:

```bash
python scripts/export_bts_round5_assets.py
python scripts/audit_bts_round6_revision.py --output-dir results/new_bts_round6_checks
python scripts/audit_bts_evidence.py
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/new_bts_round6_article \
  --supplement-build-dir results/new_bts_round6_supplement
python -m pytest tests/test_bts_round2.py tests/test_bts_round3.py \
  tests/test_bts_round4.py tests/test_bts_evidence_audit.py tests/test_bts_journal.py \
  tests/test_bts_lattice.py tests/test_bts_figure_reference.py -q
```

The post-processing script compares stored raw counts with summaries and
reconstructs the declared paired bootstrap with seed 97005. It writes a new
`round6_checks.json`; compare it with the selected
[checks record](generated/round6_checks.json). Source-file hashes distinguish the
exact post-processing inputs. This does not independently regenerate the magnetic
field, lattice or tracking studies.

## Selected execution

- Reviewed identity and snapshot: `results/bts_round6_revision_20261031/reviewed_identity.json`
  and `reviewed_snapshot/`. The old current hash set remains in
  `revision_selection.json` as `round5_final_assets_sha256`; earlier-round sets are unchanged.
- Post-processing: `results/bts_round6_revision_20261031/checks/round6_checks.json`,
  also installed at `generated/round6_checks.json`.
- Article: `results/bts_round6_revision_20261031/final_article_v2/paper.pdf`, 20 pages.
- Supplement: `results/bts_round6_revision_20261031/final_supplement/supplement.pdf`, 10 pages.
- Earlier task-specific builds remain in the same parent directory. They are not
  selected as the final article.
- Tests: 46 relevant BTS tests passed; no full-suite or new production result is claimed.

The compiled primary comparison remains Table 6 and residuals Table 8. The
prediction shortfall is 6.533617385% relative to observation. The primary gain is
4.48037334 with paired interval [4.32593473, 4.62891107]. Two zero-slope starts pass
the declared match test, and those searches remain iteration-limited.

The final asset check establishes selected-file identity, not physical validity
outside the stated model. Rare-loss and linearized-Gaussian limitations remain.
Protected scientific inputs and earlier review records are unchanged.
R5-BTS-09 author decisions remain deferred; no submission or external delivery
was performed.
