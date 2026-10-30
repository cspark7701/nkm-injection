# Milestone 269 — R4-BTS-11: discrete aperture checking stated

Completed: 2026-10-31. Round-4 task R4-BTS-11 (Reviewer 1 R3-BTS-03). The narrowed claim was chosen, so no new
computation was needed.

**Article changes.**
- **Section 2.3.** AT checks each aperture at the element entrance, and the line end (m4) carries the
  injection-septum limits, so the blade is checked at both ends of the septum. Losses are counted at these
  declared check points, not as continuous interception. The nominal interior samples locate the interior minimum
  clearance but do not certify the tails under errors.
- **Section 4.2.** "Almost all on the blade" becomes "every recorded first loss is at the injection-septum blade".
  The archived first-loss records of the round-3 steering and test campaigns contain only `sept_ex`.
- **Discussion.** A limitation sentence on the discrete check points.

The source lattice is unchanged. The isolated build is clean; the installed PDF is rebuilt in R4-BTS-09.
Protected files are unchanged.

**Build follow-up.** The first isolated build after this change failed the clean-build gate with "Label(s) may
have changed": a float moved on the third and last LaTeX pass. The labels settle on the next pass; there is no
oscillation. `package_bts_revision.py` now runs at most two extra pdflatex passes while the log asks for a rerun,
and the rebuilt article is clean (`results/bts_round4_build_r411b`).
