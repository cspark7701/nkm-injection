# Milestone 226 — R2B-01: Element-wise aperture model of the BTS line

Completed: 2026-10-15. Reviewer 2 BTS task R2B-01 (M2).

**Model** (`src/nkm_injection/bts_round3.py`, declared in `docs/paper_bts/round3_protocol.json` before any campaign):
- Every element carries its own aperture; magnets are sliced (quadrupoles 4, bends and septa 8). The four legacy
  marker apertures are removed.
- **Sourced:** only the exit-septum blade, at +1.478 mm, from the companion NKM geometry.
- **Assumed:** drifts and quadrupoles round 19.35 mm; kicker 15 × 10 mm; extraction septum 7.5 × 5 mm; curved bend
  chambers 30 × 10 mm; injection-septum outer wall −8.5 mm, half-gap 5 mm.
- Bend sagittas over the chord: 30.8 mm (b2), 19.5 mm (b1/b3).
- Round apertures use the projected halfwidth at the other plane's centroid. A Gaussian loss probability is reported
  at each aperture.

**Result** (stage `apertures`, `results/bts_journal_campaign_r3_20261015/apertures/`):
- The active restriction is the injection-septum channel at the blade: 0.648 mm at the septum entrance and 0.683 mm
  at its exit, identical for the reference and low-beta settings (downstream of q33).
- The extraction septum follows (4.44 mm vertical); the closest interior restriction is the b2 vertical gap,
  9.12 and 9.32 mm.
- Sweeping the bend gap or the extraction-septum width leaves the minimum unchanged; the blade distance sets it
  (0.17, 0.648, 1.17 and 2.17 mm for 1, 1.478, 2 and 3 mm).
- Nominally, the quadrupoles cannot change the limiting clearance.

**Manuscript.**
- New Section 2.3, Table 2 (aperture model), Results 4.1 and Fig. 3 (clearance profile).
- Section 3.1 is generalised: any restriction outside the quadrupole section has quadrupole-independent nominal
  clearance.
- The four-station method and results (old Sections 3.3 and 4.1–4.4, Tables 2–4, Figs. 2, 3, 5 and 6) moved to a new
  supplement section, unchanged in substance.

**Tooling.**
- `scripts/run_bts_round3.py` (all round-3 stages).
- `scripts/export_bts_round3_assets.py` (installs `generated/round3_*` and `figures/round3_*`).

**Tests.** `tests/test_bts_round3.py` (7 pass): sliced transport equals the original line to 1e-10; every magnet
slice has an aperture; the blade is active and independent of K; the Gaussian tail formula is checked analytically
and against 20 000 tracked particles. Article and supplement build without warnings.
