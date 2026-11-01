# Milestone 335 — Rename the NKM manuscript directory

Completed: 2026-11-01. Author requested docs/paper → docs/paper_nkm, link and packaging checks, and documentation updates without changing paper text.

Moved all 141 tracked manuscript files to docs/paper_nkm, parallel to docs/paper_bts. No old-directory symlink or second manuscript tree remains. All TeX, BibTeX and PDF bytes, as well as frozen scientific JSON/CSV records, are unchanged. Updated NKM path references across current and historical Markdown/HTML documentation, build/cleanup scripts, publication staging and tests. Historical document edits are limited to authorized path/link updates. The migration map records old/new file hashes and external reference-update hashes against the original Git checkpoint; old review findings and SHA values are not relabelled as new experiments.

Added a shared path resolver for historical/current NKM prefixes. It prefers an existing path and preserves strict content-hash checks. Updated manifest/figure readers and evidence packaging to resolve the moved files, while old manifests, protocols, identity records, provenance and frozen attachments keep their bytes. Saved-output analysis retains historical protocol identifiers. Historical tracking source/checkpoint guards remain strict; exact reruns require the recorded source version rather than bypassing changed hashes. Current source packages include the migration note/map.

Validation:

- Full suite: 779 passed in 180.65 seconds, including four new historical/current-path and hash-rejection cases.
- Link checker: 601 Markdown/HTML documents scanned, 363 local links into the NKM folder checked, zero stale or broken NKM links. Unrelated historical links to removed code or absent ignored outputs are outside this rename check.
- All 272 selected scientific artifact hashes match through the resolver. All moved manuscript and frozen-record identities and protected root input hashes match the pre-task snapshot.
- Full numerical figure/macro rebuild reproduces installed macros byte for byte. Fresh paired jitter analysis is byte-identical to the selected record, both from the renamed checkout and from evidence extracted from the unchanged old archive.
- Both PRAB source packages build under the clean-log gate: one-column 36 pages, two-column 18 pages, supplement seven pages. Staged scientific/support hashes and extracted PDF text match the relocated originals. Fresh packages are under results/nkm_directory_migration_final_one and results/nkm_directory_migration_final_two.
- Verified the evidence-bundle build/archive/rebuild workflow from a clean temporary Git snapshot, without committing the user's project tree. The temporary fixture commit is 490438e56fb47775c69f8cbff0340a9b661e3208; it is only a packaging test, not a release/referee checkpoint. The resulting test bundle has 272 selected keys, 280 verified inventory entries and byte-identical rebuilt macros. Existing release/referee attachments retain their original identities.

Check outputs are ignored under results/nkm_directory_migration*. The current migration note/map and link-check command are in docs/paper_nkm/path_migration.md and scripts/check_manuscript_links.py. No simulation, remote GitHub/API action, push, external submission or scientific prose revision occurred. Historical manuscript availability wording retains its old directory spelling under the author's instruction; the migration note identifies the current location.
