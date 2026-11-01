# Milestone 332 — NKM PRAB one- and two-column versions

Completed: 2026-11-01. Requested entry points: docs/paper/paper.tex and docs/paper/paper_twocolumn.tex.

Inspected the existing sources and found the requested conversion already implemented in REVTeX 4.2: paper.tex selects aps,prab,preprint by default; paper_twocolumn.tex defines PRABTwoColumn and includes the same manuscript, selecting aps,prab,reprint. Both are compilable entry points sharing scientific text, bibliography, figures and numerical macros. No duplicate article or gratuitous scientific-source edit was introduced.

Fresh isolated package builds in results/nkm_prab_formats_20261101_one and results/nkm_prab_formats_20261101_two produce clean 36-page one-column and 18-page two-column articles and seven-page supplements. No LaTeX errors, unresolved references/citations, disallowed bibliography warnings, overfull boxes or float failures. Nine package-helper tests pass. Rendered body pages show the requested layouts, and fresh/installed PDF extracted layout text is byte-identical in both articles and supplements. All staged scientific input hashes match the installed sources.

Retained the already-correct installed PDFs rather than changing creation-time metadata and invalidating their recorded identities. Every source/PDF identity in round5_final_identity.json remains valid. Fresh source packages and their manifests are available under the new result directories; the verification record is results/nkm_prab_formats_20261101_verification.json. Updated the PRAB guide with a linked entry-point table and the verification commands/outcome. Protected sources, manuscript prose, old reviews, frozen evidence and simulation outputs are unchanged. No new simulation, remote interaction or submission occurred.
