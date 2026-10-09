# Submission checklist — JINST regular paper (Task 012)

Prepared 2026-10-09. This is a reviewable package; **submission is a separate author action** (nothing was uploaded,
pushed or sent).

## Package (rebuild locally; results are not committed)

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg python scripts/build_journal_figures.py \
    --manifest docs/jinst-paper/campaign_manifest.json --output-dir results/<new> --install-dir docs/jinst-paper/generated
python scripts/build_submission_package.py --output-dir results/<new> [--install-pdf]
```

Output: `nkm_jinst_submission_source.tar.gz` (paper.tex, paper.bib, compiled paper.bbl, jinstpub.sty, macros and the seven
referenced figures only), `paper.pdf`, `supplement/` (manifest, provenance, claim table, review, bibliography audit,
cover letter) and `package_manifest.json` (SHA-256 of every source and output, git commit, Python/pyAT/NumPy/SciPy/
Matplotlib/TeX versions, commands). The builder fails on LaTeX errors, undefined references or citations, BibTeX
warnings and overfull boxes. Reference build: `results/journal_campaign_01/submission_package_v1` — 10 pages, clean.
The committed `docs/jinst-paper/paper.pdf` is that build.

## Headline findings → evidence → review

| Finding (paper) | Artifact (campaign_manifest key) | Claim row | Review |
| :--- | :--- | :--- | :--- |
| DA −12…+13 mm (§2.1) | backend_validation | B1 | recomputed, agrees |
| linear one-turn map overestimates capture (§3) | backend_validation | B2 | supported |
| operating point and 89.5 % grid capture (§4) | operating_region_grid | B4 | supported |
| 91.1 / 94.6 / 96.2 / 0 % paired controls; baseline BTS 26.9 % (§4) | operating_region_replicate | B5 | recomputed, agrees |
| thick-magnet capture 87.0 % (abstract, §4, §6) | thick_nkm_check | B14 | added in review |
| stored-beam 5e-6 σ aligned, 0.10 σ at 0.2 mm (§4) | computed by builder from operating point | B6 | bicubic; bilinear is upper bound |
| angular window ≈ ±0.5 mrad (§4) | operating_region_grid | B7 | supported |
| BTS tolerance median M_x and failure bound; prefix target unmet (§5.1) | tolerance_replicates | B8 | disclosed |
| combined-error capture 37.8 % [33.1, 42.7] (§5.2) | capture_analysis | B9 | recomputed, agrees |
| static correction 43.9 %, no jitter 54.5 %, dipole 59.3 % (§5.2) | capture_raw_* | B10 | wording corrected |
| septum orbit jitter and Spearman driver (§5.2) | capture_raw_*, capture_analysis | B11 | supported |
| stored beam under errors (§5.2) | capture_analysis | B12 | supported |

Configurations: `results/journal_campaign_01/operating_point_study_config.json`, frozen `error_budget.json`, selected BTS
optimisation in `backups_20261009/production_statistical_01` (read-only). Seeds are recorded in every raw artifact.

## Gate

- [x] All reported simulations ran (campaign_manifest digests verified by the builder); no planned study is described as done.
- [x] MOGA excluded from claims (`moga_decision.md`).
- [x] Statistical intervals stated (Wilson, Clopper–Pearson, cluster bootstrap, order statistics).
- [x] Model limitations stated in §6 (no ring errors/apertures, thin kick −4 points, magnetostatic map, assumed budget, 500-turn survival).
- [x] References verified (`bibliography_audit.md`); no undefined citations.
- [x] Local checker and full test suite passed; protected files unchanged.
- [x] Isolated build clean; archive contains only referenced files.

## Author confirmation required before submission

- [ ] Final title, sole authorship, affiliation and corresponding e-mail.
- [ ] Journal (JINST) and category (regular paper) — confirm against current JINST author instructions.
- [ ] Keywords from the official JINST keyword list.
- [ ] Funding statement (none recorded in the repository).
- [ ] Bibliography style: JHEP.bst required by JINST is not installed locally; `unsrt` used. Rebuild with JHEP.bst.
- [ ] Persistent archive (e.g. Zenodo DOI) for code and data at acceptance; update the availability statement.
- [ ] Review and sign the cover letter (`cover_letter.md`); decide on suggested referees.
- [ ] Accept the claims, especially the thick-magnet correction and the jitter-limited robustness conclusion.
