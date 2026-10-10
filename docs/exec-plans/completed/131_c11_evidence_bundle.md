# Milestone 131 — C11: Frozen evidence bundle for the revised manuscript

Completed: 2026-10-11. Consolidated task C11 (R1-10, R2-19).

**Command.**

```bash
OMP_NUM_THREADS=1 python scripts/build_evidence_bundle.py --manifest docs/jinst-paper/revision_manifest.json \
    --builder revision --output-dir results/journal_campaign_02/evidence_bundle_rev1 --verify
```

**Builder change (commit 3b98ea0).** The new option `--builder journal|revision` selects the figure builder that
`REBUILD.md` names and `--verify` runs. The default `journal` keeps the campaign-01 behaviour.

**Contents** (`results/journal_campaign_02/evidence_bundle_rev1/`, 9.3 MB; archive 4.4 MB; not committed):
- `evidence/`: the 46 artifacts of `revision_manifest.json` at their repository-relative paths, plus `By.txt`,
  `kickmap_file.txt` and `K4GSR_HBIv4-1.mat`. The files are copied byte for byte, and each digest is checked against
  the manifest before copying.
- `code.tar.gz`: `git archive` of commit 3b98ea0, covering src, scripts, config, tests, docs/jinst-paper and the
  packaging files.
- `campaign_manifest.json` (a copy of the revision manifest), `environment.json`, `REBUILD.md` and `SHA256SUMS`
  (53 files).

**Verification.**
- `--verify` unpacks the code into a temporary directory. It runs `build_revision_figures.py` against `evidence/`
  only, with `PYTHONPATH` set to the unpacked `src`.
- The regenerated `journal_macros.tex` is byte-identical to the committed manuscript macros
  (`rebuild_macros_identical: true`).
- `sha256sum -c SHA256SUMS` passes.
- `uncommitted: true` was recorded because the C12 response draft (`docs/jinst-paper/reviews/author_response.md`)
  was still untracked. No code file differed from the commit. The bundle is rebuilt at the C12 commit (milestone 132).

**Scope.** Nothing is uploaded and no release or DOI is created. The bundle is for referees on request, and an
archived release is an author action at acceptance (`submission_checklist.md`).
