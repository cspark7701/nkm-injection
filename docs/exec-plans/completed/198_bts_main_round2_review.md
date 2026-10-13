# Milestone 198 — Second review of the revised BTS main-branch article

Completed 2026-10-13. Reviewed the full current TeX and eight-page PDF, bibliography, generated evidence, claim ledger, supporting notes, transport/comparison code and saved raw machine/shot results. Preserved every earlier report and task register.

Created a new [Reviewer 1 report](../../paper_bts/reviews/reviewer1_bts_20261013_main_round2_report.md) recommending major revision and [eight ordered revision tasks](../../paper_bts/reviews/reviewer1_bts_20261013_main_round2_revision_tasks.md). Main findings concern the limiting entrance and tied clearance minima, design-strategy contribution, approximation accuracy in clearance units, spatial sampling of beta extrema, inference event definitions and pending submission declarations. Added the assessment to the BTS review index without changing earlier entries.

## Verification performed for this review

- Selected manuscript/asset hashes verified with `python scripts/package_bts_revision.py --verify`; exact TeX/PDF/bibliography digests included in the report.
- Reconstructed the mean paired clearance change (0.0146103 mm) and 95% machine-bootstrap interval [-0.0179072, +0.0483232] mm from 200 saved machine means with 10000 replicates and seed71004.
- Read 600 saved shot records:406 identical paired minima,93 identical machine averages, zero observed losses. Machine-average difference range is [-0.92289, +1.40103] mm. Active-station frequencies require additional reconstruction and are requested, not presumed.
- Extracted PDF text and inspected all eight rendered pages in a montage. Checked official JKPS guidance and the SLS2.0 primary transfer-line report; the attempted IPAC24 beam-source PDF retrieval failed and that limitation is disclosed.
- Fresh tracking/optimization and the full test suite were not rerun: the active interpreter lacks the installed project package and pyAT. Earlier recorded checks remain evidence from their original execution.
- New local Markdown links resolve; documentation diff passes whitespace checks. All existing tracked files except the two additive indexes remain byte-identical, including current manuscripts, prior reports and protected scientific inputs.

This task writes an assessment, not scientific revisions or a submission. All R2-BTS tasks are open; funding remains deferred by the author. No branch rebase, push, remote GitHub operation or journal submission was performed.
