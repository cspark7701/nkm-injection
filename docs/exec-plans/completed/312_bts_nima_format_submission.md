# Milestone 312 — Convert the BTS manuscript to NIM A format

Completed: 2026-11-01. The user selected NIM A as the target and requested format conversion for submission.

Converted the primary article to Elsevier `elsarticle` one-column preprint format with native author/affiliation/correspondence fields, six keywords and numbered `elsarticle-num` references. Applied the Humanizer skill to shorten the abstract to 215 whitespace-delimited words in extracted PDF text, preserving the conditional-model and stress-jitter qualifications. Added four editable highlights (each below 85 characters). The supplement retains a separate article layout with consistent numbered references. Funding, competing interests and pending approval remain unchanged. Main text from the Introduction through the declarations is byte-identical to the previous version.

Added [build and submission instructions](../../paper_bts/nima_submission.md) and `scripts/build_bts_nima_submission.py`. The builder creates a fresh flat source directory, compiles both documents, retains logs/identities, supplies `.bbl` files and the bibliography style, and creates an editable source ZIP. It rejects existing output directories and ambiguous flattened filenames. The selected build is `results/bts_nima_submission_20261101_v4/`; earlier attempts remain diagnostic records. Resolved the class title-page footer overflow using a plain page style and removed correspondence-macro PDF metadata warnings.

Updated current target/status documents and selected hashes, preserving the earlier 90-asset selection as `round7_final_assets_sha256`. The new 92-asset selection includes the submission guide and highlights. Older review reports, author responses, generated results, scientific evidence and referee attachments remain intact. NIM A selection closes only the journal-choice decision. No external upload, submission or final author approval is inferred.

Validation:

- Article 19 pages and supplement 10 pages; both builds have no layout, reference or missing-character warnings.
- The 46-file flat ZIP was extracted into a new directory; both PDFs rebuilt without warnings and their extracted text exactly matches the selected PDFs. Build and extraction records are retained alongside the ZIP.
- Existing output directory rejection was exercised without overwriting.
- All 80 evidence claim checks and 92 selected asset hashes pass.
- Seven relevant BTS test modules pass: 46 tests in 11.36 seconds.
- Title/abstract, primary comparison table and reference pages inspected visually. Local Markdown links and Git whitespace checked; protected files unchanged. No tracking, optimization or full-suite rerun.

The official Elsevier LaTeX guidance was accessible and supports the article class and flat submission structure. The live NIM A guide returned HTTP 403; the submission guide records that limitation rather than claiming verification of all current portal requirements.
