# Milestone 216 — E5: Corrected ring population with optics correction

Completed: 2026-10-13. Round-3 task E5 (R2c-2; author inputs B1 and B5 at their defaults).

**Work.** The same ten error draws as round 2 (seeds 5501–5510, same staged ramp) receive a commissioning-style chain:
- BPM readings referenced to the adjacent quadrupole centre (10 µm residual);
- converged SVD orbit correction with the 120 HVC correctors;
- β-beat and dispersion correction with the 344 individual quadrupoles;
- Q11/Q12 tune correction and a final orbit correction.

There is no coupling correction: the lattice has no skew correctors.

**Results.**
- rms β-beat falls from 4.3–10.5 % to ≤ 2.0 %, and β_x at the NKM is 15.8–16.3 m.
- The NKM closed orbit is ≤ 56 µm.
- The orbit relative to the references converges to 69–83 µm (x) and 49–63 µm (y), with unsaturated correctors. This
  is the floor of the 120-corrector file, not a stopping rule.
- The first unstable horizontal launch is −11.0 to −9.5 mm (round 2: −10.0 to −7.5 mm).
- Ring 5501 recovers from −7.5 to −10.5 mm: its round-2 collapse was caused by uncorrected optics.

**Code.**
- `src/nkm_injection/ring_error_scenario.py`: `bpm_reference_offsets`, `correct_orbit_converged`,
  `optics_observables`, `correct_optics`.
- New: `scripts/run_round3_corrected_ring.py`.
- `build_revision_figures.py`: step `corrected_ring_round3`, which replaces Figure 10 (round-2 versus round-3 DA edge,
  β-beat before and after, orbit residuals) and emits the `RThree*` macros. The round-2 figure path is skipped when
  round-3 data exist; its ideal-ring macros are kept.
- Tests: `tests/test_round3_correction.py` (3, on a FODO ring).

**Manuscript.**
- The section-5 corrected-ring paragraph and the Figure 10 caption describe the chain and the results.
- The per-ring capture sentence that follows is still the round-2 value; it is updated with the E6 validation and the
  E7 rerun.

**Evidence.**
- `results/journal_campaign_04/e5_corrected_ring/` (summary, per-seed JSON and lattices).
- Manifest keys `round3_ring_*` in `revision_manifest_round3.json`.

**Checks.** The correction tests pass and the one-column gated build is clean.
