# Selected evidence inventory — corrected reviewer audit

[evidence_manifest.json](evidence_manifest.json) supplies exact byte sizes, digests and JSON pointers for all seventeen BC claims. Run `python scripts/audit_bts_evidence.py`; missing keys, altered values or digests fail the audit. The original review is preserved.

- `backups_20261009/production_statistical_01/optimization/bts_optimization_summary.json`: 3200 bytes, SHA-256 `fe10758922697a3d0ff6496f068706099c2089348811cd31f859cdcead1cf3cb`; generating commit `None` (null means not established).
- `backups_20261009/production_statistical_01/optimization/config.json`: 4286 bytes, SHA-256 `382e23dd1d4ed167e6cf321e40f5041e42c5909a0b5dbf1da9101ce4883f8ae2`; generating commit `f2ac6e27f60dd19d0dfbc74419df585b6f0a8748` (null means not established).
- `results/journal_campaign_01/tolerances_seed42/publication_tolerances_summary.json`: 74827952 bytes, SHA-256 `620626291ee47d9a8d50b5372d54aaeabf640d1a64e0f846be246ea433e9da1b`; generating commit `None` (null means not established).
- `results/journal_campaign_01/tolerances_seed123/publication_tolerances_summary.json`: 74827566 bytes, SHA-256 `d1f381f714e9d2c808b28b6d3ada90eca4781895a0955aa3bedffccd4006c974`; generating commit `None` (null means not established).
- `results/journal_campaign_01/tolerances_seed777/publication_tolerances_summary.json`: 74827778 bytes, SHA-256 `353c1986e6330686d235ce3e29e622706fe04e0e5e88445f308fe8e0e1707644`; generating commit `None` (null means not established).
- `results/journal_campaign_01/tolerances_seed2026_400k/publication_tolerances_summary.json`: 598918614 bytes, SHA-256 `fa3c0b8254836171ff6cab17d4e6bf3c85ec24c5023096c74cb4a2ee9209b296`; generating commit `None` (null means not established).
- `results/journal_campaign_01/followup_analysis/tolerance_replicates_with_400k.json`: 23740 bytes, SHA-256 `5d11a050b8aa7ab813fff286b849fb7d93d02e4d04733e5f904c69e60860b589`; generating commit `None` (null means not established).
- `backups_20261009/production_statistical_01/optimization/candidate_table.json`: 4330 bytes, SHA-256 `398be628e1b017375bbbdf4c58d225e694ede6109bfda28733cdbe8419cee9d7`; generating commit `None` (null means not established).
- `results/journal_campaign_01/error_budget.json`: 565 bytes, SHA-256 `6a1ce41f2f72e97a6b550f138469491a00d8c2883dd31ed453c98b97cb876146`; generating commit `None` (null means not established).

The optimization config records `f2ac6e27f60dd19d0dfbc74419df585b6f0a8748`. A later environment checkpoint is not evidence of a global generating commit. The historical tolerance summaries contain their own source/configuration records; do not infer their generating revision from the draft authoring commit. Physical target, chamber and hardware provenance remain unresolved and are assumptions.

## Newly selected outputs

The five installed numerical summaries are compact publication exports of separate raw directories; they are not substituted for the supplied observations. The historical statistical re-audit adds its exact code/environment identity.

- `docs/paper_bts/generated/heldout.json`: 26636 bytes, SHA-256 `32b2260a7911194f7e71f0de4f87c24242c7d973d2d73d03fe7e443654f62a6f`.
- `docs/paper_bts/generated/heldout.json`: 26636 bytes, SHA-256 `32b2260a7911194f7e71f0de4f87c24242c7d973d2d73d03fe7e443654f62a6f`.
- `docs/paper_bts/generated/normalized_response.json`: 10791 bytes, SHA-256 `8ae746396351d6d1ab3bc5926ca689f500839b6aab8318a2264c176d91a4ec12`.
- `docs/paper_bts/generated/transport_validation.json`: 3236 bytes, SHA-256 `6aa07d5da8b5f91a62ed5ab410fbd7b41c83d30384eeee240c48b08f22ca8a02`.
- `docs/paper_bts/generated/historical_statistics.json`: 16540 bytes, SHA-256 `7c2029d170348e55aaf60f2fbf5c0b5772cff6ac265cbe8f09296bcf9ae79140`.
