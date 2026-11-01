# Milestone 328 — NKM round-5 completed-status source packages

Completed: 2026-11-01.

Refreshed both PRAB source packages from clean completed-status checkpoint `af76d39`, after G6 verification. Both package manifests report an unmodified source tree, the round-5 selected manifest, and matching installed scientific inputs. All support-document hashes match the current response, final audit, reproduction guide and identity/verification receipt. The one-column article/supplement are 36/7 pages and the two-column article/supplement are 18/7 pages; both builds pass the clean-log gate.

| Layout | Source archive | SHA-256 |
| :--- | :--- | :--- |
| one-column | `results/nkm_round5_completed_source_one/nkm_article_submission_source.tar.gz` | `2274938524e0a6441973b8cd7e82ecb7114cc333c2a6d91240ab664cad25ef7b` |
| two-column | `results/nkm_round5_completed_source_two/nkm_article_submission_source.tar.gz` | `628a45502e42767962a8bc6b09e77eb4dd8d59a6edb01ac5efa8b42bd781bbba` |

The manuscript source archive contains submission TeX/BibTeX/figures; accompanying support files are in each package directory’s supplement/ with a hashed package_manifest.json. These packages include the completed verification receipts. The separate scientific evidence attachment remains the identified clean `3c981c2` checkpoint; its scientific assets match and its pre-verification support-document timing is explicitly recorded. Recompiled package PDFs can differ in creation-time metadata from the installed PDFs; their source identities and page counts agree. No installed scientific asset was changed by this packaging step.

Final checks: 775 full-suite tests and 30 targeted tests pass; all protected input hashes match the pre-task snapshot; old reviews/responses and frozen bundles are preserved. G1–G6 remain complete and G7 remains deferred. No remote interaction or submission occurred.
