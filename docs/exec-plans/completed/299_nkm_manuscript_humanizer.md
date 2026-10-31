# Milestone 299: humanize and compile the NKM manuscript

Completed: 2026-10-31, after the four BTS round-six revisions. Used the explicitly
requested humanizer skill at /home/cspark/.agents/skills/humanizer/SKILL.md in file
mode: edited final prose only, with a second pass for meaning, grammar and repeated
AI-style phrasing. Simplified the abstract and introduction, split dense results
paragraphs, removed repetitive framing and clarified the Discussion/Conclusions
and availability text. Author attribution, funding, qualifications and numerical
claims are preserved. No new literature or scientific result was introduced.

Preservation checks compare the revised source against the saved original:
890 LaTeX commands in the same sequence, all 250 inline mathematical expressions,
591 numeric literals and 45 citation commands unchanged; all eight tabular blocks
and ten figure blocks byte-identical. The bibliography, generated numerical
macros, supplementary TeX and two-column wrapper are unchanged. These mechanical
checks supplement the prose/meaning review; they are not a new physics validation.

Built and installed the primary one-column article (34 pages), the side two-column
preview (17 pages) and supplement (7 pages), using the existing submission-package
script in fresh results/nkm_humanized_manuscript_20261031 directories. Both layouts
pass its log gate: no LaTeX errors, unresolved citations/references, overfull boxes
or unsettled labels; BibTeX checks pass. Existing REVTeX/nameref notices and
underfull-box diagnostics remain and are recorded in layout_checks.json. Title/
abstract pages of both layouts were visually checked. Nine submission-package
tests pass. Updated the manuscript README's file counts and distinguished its
historical scientific-review snapshot from this prose update.

Reproduce from the repository root in the project environment, using new paths:

```bash
python scripts/build_submission_package.py --layout one-column --output-dir results/new_nkm_prose_one
python scripts/build_submission_package.py --layout two-column --output-dir results/new_nkm_prose_two
python -m pytest tests/test_submission_package.py -q
```

The reviewed originals, before/after preservation checks and build manifests are
retained in results/nkm_humanized_manuscript_20261031. No simulation or scientific
revision task is executed by the prose edit. Protected inputs and all earlier
review records remain unchanged; BTS R5-BTS-09 decisions stay deferred.
