# Milestone 213 — E3: Normalised finite-length approximation error

Completed: 2026-10-13. Round-3 task E3 (R1C-03). Existing campaign-03 data only; no new tracking.

**Result** (from `d7_generality/generality_scaling.json`; 30 configurations, two wire families).
- **Horizontal fit.** |Δp_x|/|K| = 1.95 η^1.46 for the thin map against the exact field, with 3.4 % log-rms scatter
  and 11 % largest deviation. The per-family exponents are 1.47 and 1.45, so η organises the normalised horizontal
  error across both families.
- **Vertical.** The error scales as η^0.81 with 7 % scatter; it organises less tightly because it depends on the
  vertical launch.
- **Sliced map.** It stays below 2×10⁻⁵ |K| in both planes.
- **Accuracy allowance.** The declared allowance is one tenth of the angular window, 0.076 mrad. The thin map reaches
  it at η* ≈ 0.036, and the nominal η = 0.034 uses 91 % of it. Per pass, the nominal thin-map error is
  |Δp_x| = 0.069 mrad and |Δp_y| = 0.129 mrad at y = 1 mm.

**Changes.**
- **`scripts/build_revision_figures.py`.** `fig_generality` now plots |Δp|/|K| for both planes on log axes, adds the
  power-law fit, the allowance and the nominal marker, and emits the `Gen*` macros. The allowance is derived from the
  `round2_window` artifact through `round2_reporting.window_bounds`.
- **`paper.tex`.** The section-3 paragraph defines K, w, the reference path and the launch recipe; explains the
  |K|L/8 sagitta; and quotes the fit, the scatter, the sliced-map bound and η*. The Figure 9 caption is updated.
- **Installed figures and macros.** `docs/paper/generated` gains the `Gen*` macros (additions only) and the new
  `fig9_generality.pdf`; provenance now records `round2_window` for Figure 9. The other figures were restored to
  their committed bytes, because the local Matplotlib differs from the one that produced them; their data did not
  change.
- **`round2_generality.md`.** A round-3 section.

**Checks.**
- The one-column gated build is clean (28 pages).
- The two-column preview reports a REVTeX "float is stuck" warning, which the gate rejects. Bisection shows the
  warning is caused by text reflow congesting the full-width float queue; it disappears when the wire and
  loop derivative tables leave the main text. That move is part of E10 (supplement), so the two-column preview is
  expected to be clean after E10. All floats are rendered in the meantime.
- The builder, package and bundle tests pass (13).
