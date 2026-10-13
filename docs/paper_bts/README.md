# BTS optics manuscript

Revised one-column article for a prospective JKPS Research Article. It reports a conditional negative result: lowering vertical peak beta does not resolve an increase in minimum five-sigma clearance at the selected model aperture stations.

- [LaTeX manuscript](paper.tex) and [eight-page PDF](paper.pdf)
- [Reviewer report, tasks and response](reviews/README.md)
- [Version identity](revision_identity.md) and [frozen asset hashes](revision_selection.json)
- [Source-labelled boundaries/beam](beam_and_boundaries.md) and [configuration](journal_config.json)
- [Independent transport validation](transport_validation.md)
- [Matching reproduction](nominal_matching_reproduction.md)
- [Local normalized response and claim withdrawals](correction_knobs.md)
- [Held-out physical comparison](heldout_comparison.md)
- [Historical statistical reconstruction](tolerance_distributions.md)
- [Evidence manifest](evidence_manifest.json), [claim ledger](claim_evidence.csv) and [discrepancy resolutions](discrepancy_resolution.md)
- [Primary literature comparison](literature_comparison.md)
- [Submission checklist](submission_checklist.md) and [validation record](validation_checks.md)

R1-BTS-01–09 numerical/editorial revisions are executed. R1-BTS-10 article, evidence attachment and build are prepared; funding (author will update later), competing interests, acknowledgments, final author approval and actual referee delivery remain pending. Earlier B-task plans describe the original scope; the point-by-point reviewer response supersedes their draft-status statements for this selected revision. No operational correction, continuous-chamber certification, storage-ring capture or journal acceptance is claimed.

## Reproduce

Use the recorded scientific environment and install the project package. Each output path must be new:

```bash
python scripts/audit_bts_evidence.py
python scripts/audit_bts_statistics.py --output-dir results/new_bts/statistics
python scripts/run_bts_journal_revision.py --stage validation --output-dir results/new_bts/validation
python scripts/run_bts_journal_revision.py --stage matching --output-dir results/new_bts/matching
python scripts/run_bts_journal_revision.py --stage response --output-dir results/new_bts/response
python scripts/run_bts_journal_revision.py --stage comparison --output-dir results/new_bts/comparison
python scripts/package_bts_revision.py --verify
python scripts/package_bts_revision.py --build-dir results/new_bts/pdf
python scripts/package_bts_revision.py --package-dir results/new_bts/referee_attachment
```

The selected original campaign is `results/bts_journal_campaign_r1_20261013/`. Ignored raw results are supplied separately in the prepared attachment; portable commands resolve data relative to its extracted root. Historical observations are rebuilt statistically, not regenerated from an unverified historical generating revision. Hashes identify files, not physical validity. No original scientific sources or NKM manuscript files were changed.
