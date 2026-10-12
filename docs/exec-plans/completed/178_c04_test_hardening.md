# Milestone 178 — Continuous Integration & Regression Test Hardening (C04)

Completed: 2026-10-13. User request: After complete the task, create a new task list and execute them.

## 1. Summary of Work Completed

Task C04 of `docs/paper_bts/003_post_submission_tasks.md` was executed to implement automated test hardening for the BTS publication pipeline:

1. **Test Suite Development (`tests/test_bts_paper_assets.py`)**:
   - `test_provenance_file_exists`: Validates provenance file structure, status tag, and publication asset registry.
   - `test_paper_pdf_integrity`: Validates existence and non-trivial file size (>100 KB) of `paper.pdf`.
   - `test_all_five_figures_exist`: Checks existence and integrity of Figures 1 through 5.
   - `test_sha256_matches_provenance`: Verifies that live files on disk match the frozen cryptographic SHA-256 digests in `draft_provenance.json`.
   - `test_archived_latex_macros_present`: Asserts presence and exact values of published mathematical variables in `generated/archived_results.tex` ($\beta_{x,\max} = 31.4368\text{ m}, \beta_{y,\max} = 50.7459\text{ m}$, median mismatch $0.00208629$).

2. **Automated Verification**:
   - Ran `pytest tests/test_bts_paper_assets.py`, achieving 100% pass (5/5 tests passed in 0.02s).
   - Marked Task C04 completed in `docs/paper_bts/003_post_submission_tasks.md`.

---

## 2. Deliverables Produced

- [`tests/test_bts_paper_assets.py`](../../tests/test_bts_paper_assets.py)
- [`docs/paper_bts/003_post_submission_tasks.md`](../../paper_bts/003_post_submission_tasks.md)

---

## 3. Verification and Acceptance Checks

- All tests pass in pytest suite.
- Protected scientific source files remain unmodified (`git status`).
- Tasks C01–C04 are completed.
