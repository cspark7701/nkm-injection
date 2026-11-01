# NKM manuscript directory migration

The NKM manuscript is now in `docs/paper_nkm/`, parallel to `docs/paper_bts/`. The directory itself has moved; no compatibility symlink or second manuscript copy is kept. Edit `paper.tex` for the one-column PRAB article and compile `paper_twocolumn.tex` for the shared-source two-column version.

## Current paths and manuscript text

Current documentation links, build/analysis defaults, publication staging and source-package locations use the new directory. Markdown references across the repository, including historical reports and completion notes, have been updated as authorized. Those path edits do not change the scientific findings, review recommendations or author responses. The accompanying `path_migration.json` records the pre-move commit and old/new hashes so historical document bytes remain identifiable through Git.

All manuscript TeX, bibliography and PDF files are moved byte for byte. Their contents, including the availability statement's old directory spelling, are intentionally unchanged under the author's instruction to preserve paper text. Source packages use relative `generated/` paths and remain compilable. The old directory spelling in manuscript text is a historical location; the current repository location is the directory containing this note.

## Frozen scientific and provenance records

Existing JSON manifests, declared protocols, identity records, rename maps and generated provenance CSVs retain their original bytes and hashes. Their recorded historical paths are evidence identifiers, not silently rewritten statements about an old archive's contents. A shared `manuscript_path` resolver accepts the historical and current directory prefixes when a reader opens an evidence file. An existing path takes precedence; only this exact directory rename is supported, and every content-hash check still applies. The resolver also supports evidence extracted from older attachments that contain the historical directory layout.

The round-5 selected manifest therefore remains valid without rehashing scientific inputs. Its artifacts can be read from the renamed checkout, and old frozen attachments remain unchanged. The saved-output analyzer preserves its historical protocol identifier so the selected numerical analysis remains byte-reproducible. New source packages identify their current directory and include this migration note and map.

Historical tracking checkpoints also record source-code hashes. Paths in commands can be resolved after the move, but modified source versions must still fail strict checkpoint guards. Use the identified archived source for an exact historical tracking rerun; do not disable those guards or overwrite old outputs to force a resume. This migration does not run new simulations or redefine their scientific protocols.

## Checks

The migration is checked by the full test suite, targeted legacy/current-path and hash-rejection tests, NKM-related Markdown/HTML link checks, the full numerical macro rebuild, saved-output reanalysis and both PRAB source-package builds. The execution archive records actual outcomes and result directories. Unrelated historical links to removed modules or absent ignored outputs are distinguished from links affected by this rename.
