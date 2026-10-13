# Milestone 214 — E4: Feasible NKM vacuum chamber

Completed: 2026-10-13. Round-3 task E4 (R2c-1).

**Model.**
- **Chamber.** A flat in-magnet chamber of 16 × 3.8 mm half-aperture. Its half-height is the inner-wire y (5.3 mm)
  minus a 1.5 mm wall-plus-conductor allowance, the value used for the ALS NLK (Sun et al. 2020).
- **Where it acts.** It is checked per slice by the 3-D kicker on the injection pass, applied to the ring's magnet
  halves `NKM_H1` and `NKM_H2` on every later turn, and checked at the magnet centre for the thin controls.
- **Validation.** `ChamberProfile.validate_against_wires` rejects any chamber that reaches a conductor; the round-2
  30 × 15 mm rectangle is rejected.
- **Defaults.** `None` keeps the round-2 model.

**Results.**
- **Normalised vertical aperture.** The NKM chamber gives 1.61 mm m^-1/2, against 1.81 (arc), 2.64 (centre bend) and
  1.31 (closed IVU, stress case). With open IVUs it is the tightest vertical restriction.
- **Capture.** On the ideal ring with the design beam, capture is 97.0 % [95.7, 97.9] (dipole 97.3 %) for every
  half-height from 3.0 to 4.3 mm and without the chamber. No particle is lost in the magnet, because the injected
  vertical size is about 60 µm.
- **Interpretation.** On the ideal ring the chamber is not limiting. E7 tests the corrected rings.

**Code.**
- `src/nkm_injection/wire_field.py`: optional chamber for `FilamentNKMKicker` and `CalibratedControl`.
- `src/nkm_injection/chamber.py`: in-magnet fields, the wire-clearance check, `kicker_kwargs`, and `NKM_H*`
  apertures.
- `run_round2_chamber.py`, `run_round2_window.py`, `run_capture_robustness.py`: the chamber is passed to the kickers
  (backward compatible).
- New: `run_round3_nkm_chamber.py`, `analyze_round3_chamber.py`, `make_round3_manifest.py`.
- `build_revision_figures.py`: step `round3_chamber` (macros `NkmChamberNorm*`, `ArcNormY`, `CentreNormY`,
  `ClosedIvuNormY`, `ScanCap*`, `ScanMagLoss*`).
- Tests: `tests/test_nkm_magnet_chamber.py` (7).

**Manuscript.**
- The chamber paragraph of section 5 gives the definition, justification, normalised aperture and scan result.
- Table 1 (32 × 7.6 mm) and the parameter table are updated.
- The section-8 eddy estimate is recomputed for the 3.8 mm half-gap, with the ALS coating reference.

**Evidence.**
- `results/journal_campaign_04/e4_nkm_chamber_scan/`, `e4_aperture_normalisation.json` and
  `docs/paper/round3_chamber_config.json`.
- `docs/paper/revision_manifest_round3.json`: the round-2 selection plus round-3 artifacts present so far.

**Process note.** The first scan applied the chamber only on the injection pass; it was stopped and rerun with the
ring apertures. A summary key error in an earlier run lost its in-memory rows, so the driver now writes each profile
before summarising.

**Checks.**
- Chamber, wire-field, robustness and window tests pass.
- The one-column gated build is clean.
- Method note: `docs/paper/round3_chamber.md`.
