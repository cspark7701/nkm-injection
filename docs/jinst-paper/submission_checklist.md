# Submission checklist — revised manuscript (KLS, exact 3-D NKM)

Prepared 2026-10-11 for the consolidated reviewer revision (C1–C12). This is a reviewable package; **submission is a
separate author action** (nothing was uploaded, pushed or sent). The journal is not yet chosen; the manuscript uses the
JINST class and is written venue-neutrally.

## Package (rebuild locally; results are not committed)

```bash
python scripts/make_revision_manifest.py --require-all --output docs/jinst-paper/revision_manifest.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg python scripts/build_revision_figures.py \
    --manifest docs/jinst-paper/revision_manifest.json --output-dir results/<new> --install-dir docs/jinst-paper/generated
python scripts/build_submission_package.py --output-dir results/<new> [--install-pdf]
python scripts/build_evidence_bundle.py --manifest docs/jinst-paper/revision_manifest.json --builder revision \
    --output-dir results/<new> --verify
```

`build_submission_package.py` writes the source archive (paper.tex, paper.bib, compiled paper.bbl, jinstpub.sty, macros
and the eight referenced figures), `paper.pdf`, the supplement (revision manifest, claim table, review, bibliography
audit, cover letter, provenance) and `package_manifest.json` with SHA-256 digests, git commit, software versions and
commands. It fails on LaTeX errors, undefined references or citations, BibTeX warnings and overfull boxes. Reference
build: `results/journal_campaign_02/submission_package_rev1` — 13 pages, clean; the committed
`docs/jinst-paper/paper.pdf` is that build. The evidence bundle for referees is described in milestone 131.

## Headline findings → evidence

| Finding (paper) | Artifact (revision_manifest key) | Claim row | Milestone |
| :--- | :--- | :--- | :--- |
| DA −12…+13 mm at the kicker | backend_validation | C1 | — |
| exact filament field = RADIA map; 640 slices converged | kicker_validation | C2 | 121 |
| self-deflection shifts matched angle by 0.2 mrad | mechanism | C3 | 122 |
| vertical defocusing costs about five points | vertical_diagnostic | C4 | 122 |
| operating point; 93.0 % NKM, 97.0 % dipole, 97.8 % linearised, 0 % off | c3_grid, c3_validate | C5 | 125 |
| angle window 0.74 mrad, position window 1.44 mm | c3_angle, c3_position | C6 | 125 |
| 2000-particle capture 92.4 %; 89.5 % after 4000 turns | c4_particles, c4_longturn | C7 | 126 |
| aperture and ring-error sensitivities | c4_aperture, c4_ring_errors, c4_aper_* | C8 | 126 |
| transparency by symmetry; 0.10 σ at 0.2 mm; tracked check | c7_analytic, c7_tracked | C9, C10 | 129 |
| pulsed-magnet residual requirements | builder (operating point) | C11 | 124 |
| combined errors 40.5 % / 44.4 % (no / ideal static correction); dipole 61.4 / 65.6 % | c5_raw_*, c5c_raw_* | C12–C14 | 127, 128 |
| jitter tolerance curves; no 80 % from jitter reduction alone | c6_raw_*, c6c_raw_* | C15, C16 | 128 |

Configurations: `results/journal_campaign_02/operating_point_3d.json`, frozen `error_budget.json`, selected BTS
optimisation in `backups_20261009/production_statistical_01` (read-only). Seeds are recorded in every raw artifact.
Rows A1–B18 of `claim_evidence.csv` document the campaign-01 manuscript and are superseded (row C0).

## Gate

- [x] All reported simulations ran; `make_revision_manifest.py --require-all` records 46 artifacts with digests, and the
      builder verifies every digest it reads.
- [x] MOGA excluded from claims (`moga_decision.md`).
- [x] Statistical intervals stated (Wilson, cluster bootstrap, paired differences, partial rank correlation).
- [x] Limitations stated (ideal lattice with bounded ring-error and aperture sensitivities, no iron/chamber/eddy fields,
      assumed error budget, 500-turn survival checked to one damping time, no sextupole optimisation).
- [x] References verified (`bibliography_audit.md`); no undefined citations.
- [x] Full test suite passed; protected files unchanged.
- [x] Isolated build clean; archive contains only referenced files.

## Author confirmation required before submission

- [ ] Choose the journal; adapt the class, keywords and cover letter to it.
- [ ] Final title, sole authorship, affiliation and corresponding e-mail.
- [ ] Funding statement (none recorded in the repository).
- [ ] Bibliography style required by the chosen journal (`unsrt` used now).
- [ ] Persistent archive (e.g. Zenodo DOI) for code and data at acceptance; update the availability statement.
- [ ] Review and sign the cover letter (`cover_letter.md`); decide on suggested referees.
- [ ] Review the response to the reviewers (`reviews/author_response.md`).
- [ ] Accept the claims, especially the vertical-sign correction of the kick map and the robustness conclusion
      (80 % mean capture is not reached under the assumed budget).
