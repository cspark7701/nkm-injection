# Milestone 289 — R5-BTS-06: angle-weighted steering sensitivity

Completed: 2026-10-31. Round-5 task R5-BTS-06 (Reviewer 2 R2D-06), executed as a documented sensitivity.

**Study.** Layout `angle_weighted` in `bts_round4.LAYOUTS`, declared in `round5_protocol.json`:
- the same eleven position readings and six trims as the full layout, with the same knob limits;
- the septum-entrance and line-end readings weighted 10 instead of 3;
- run in `layouts_b` on the shared-reading realizations (seeds 91001–91005, tracked).

There is no angle monitor and no new hardware.

**Result.**
- **Matched reference:** unchanged (1.675 %, 0.367 mrad).
- **Loss-based setting:** exit-angle rms 0.413 → 0.411 mrad, loss 0.381 → 0.380 %, jitter-integrated gain 4.55
  against 4.59.

Reweighting position readings does not reduce the angle residual. A smaller residual would need an angle
measurement or more accurate readings, which the study does not model.

**Article.** One sentence in the layout paragraph, plus the angle-weighted rows in Table 5 (since R5-BTS-01). The
prose follows the humanizer rules. The isolated build is clean. Protected files are unchanged.
