# BTS Manuscript Post-Submission Campaign & Package Extension Tasks

**Plan Date:** October 13, 2026  
**Status:** In Progress (Tasks C01–C06)  
**Author:** Chong Shik Park  
**Affiliation:** Department of Accelerator Science and Center for Accelerator Research, Korea University  
**Branch:** `bts`

---

## 1. Context and Objective

Following the successful execution and qualification of Tasks B01–B12 (Milestones 163–174), the standalone JKPS manuscript (`docs/paper_bts/paper.pdf`) and its complete evidence base are frozen and publication-ready.

In accordance with the user instruction (*"After complete the task, create a new task list and execute them"*), this campaign defines and executes the next phase of work for the BTS transfer-line project:

1. **Task C01 — Automated Submission Bundle & Tarball Packaging**: Construct a self-contained submission archive script and verify isolated building outside the git working tree.
2. **Task C02 — Interactive HTML Project Webpage Integration**: Build a GitHub.io-style project showcase page in `docs/` summarizing the BTS study, interactive figures, and downloadable artifacts in adherence with `AGENTS.md`.
3. **Task C03 — Automated Clean-Environment Reproduction Script**: Author a single-entry CLI script (`scripts/reproduce_bts_paper.py`) that can regenerate all tables, SVD matrices, and figure assets from clean scratch data.
4. **Task C04 — Cross-Platform Continuous Integration & Formatting Workflow**: Create dedicated validation workflows and test scripts ensuring long-term maintenance of the BTS lattice, optics engine, and manuscript assets.

---

## 2. Ordered Task Ledger

### C01 — Automated Submission Bundle & Tarball Packaging [COMPLETED]
- **Status:** Completed 2026-10-13 (Milestone 175).
- **Objective:** Create `scripts/package_bts_submission.py` to package LaTeX sources, bibliography, figure PDFs, and provenance JSON into a timestamped, checksummed `.tar.gz` bundle for the author's submission upload.
- **Deliverables:** `scripts/package_bts_submission.py`, `results/bts_submission/bts_jkps_submission.tar.gz`, `results/bts_submission/bundle_manifest.json`.
- **Acceptance:** The tarball extracts cleanly in an isolated directory and compiles to an identical PDF matching the frozen SHA-256 digest (`608,936` bytes, exit code 0).


### C02 — Interactive HTML Project Showcase Webpage
- **Objective:** Update and enhance `docs/index.html` (or create `docs/bts_showcase.html`) following GitHub.io project styling to present the BTS transfer-line results, layout, SVD knobs, and transmission curves.
- **Deliverables:** `docs/bts_showcase.html` (or updated `docs/index.html`), associated CSS/visual assets.
- **Acceptance:** Fully compliant with `AGENTS.md` GitHub.io styling guidelines with functioning internal links and figure embeddings.

### C03 — Standalone One-Command BTS Reproduction Script
- **Objective:** Create `scripts/reproduce_bts_paper.py` allowing independent verification of all figures, tables, and SVD knobs from the command line.
- **Deliverables:** `scripts/reproduce_bts_paper.py`, CLI documentation.
- **Acceptance:** Script executes cleanly with `--verify` flag, confirming exact agreement with `draft_provenance.json`.

### C04 — Continuous Integration & Regression Test Hardening
- **Objective:** Add comprehensive BTS paper asset regression tests in `tests/test_bts_paper_assets.py` to continuously assert PDF existence, figure hashes, and table values.
- **Deliverables:** `tests/test_bts_paper_assets.py`.
- **Acceptance:** Passes 100% in pytest suite.
