# Milestone 237 — F4: Signed and physical associations, zero-capture and jitter rows

Completed: 2026-10-19. Round-4 task F4 (R1D-05/07; R2d-4/7). Note: `docs/paper/round4_associations.md`.

**Work.**
- `scripts/analyze_round4_associations.py` reuses the E7 data (150 full-budget realizations, paired seed-42 jitter
  ensembles); no new tracking.
- It computes, for each realization, the post-kick centroid amplitude for the NKM and the dipole control.
- Signed Spearman associations with Holm adjustment within each response (NKM, dipole, difference).
- Zero-capture and conditional summaries; two-model jitter rows; interval convention.

**Findings.**
- **Amplitude.** Capture follows the post-kick amplitude (ρ −0.60 NKM, −0.70 dipole).
- **NKM spread.** The NKM spreads the amplitude more (mean 3.7 against 2.2 ×10⁻³ m^1/2), through the signed
  booster angle and position.
- **Signed offset.** The signed NKM–orbit offset is NKM-specific (+0.26, p_Holm 0.011).
- **Zero capture.** 51 % NKM against 10 % dipole; conditional means 33 % against 49 %.
- **Jitter.**
  - Full jitter costs both models about 20 points.
  - Angle-only costs the dipole −18.0 against −16.8 for the NKM; position-only costs the NKM more (−8.9 against
    −2.6).
  - The gap of about −28 points exists at zero jitter.
- These associations are exploratory; F2 supplies the causal contrasts.

**Tests** (`tests/test_round4_protocol.py`, 6 pass): an error-free shot leaves the NKM with zero angle; Holm
adjustment checked.
