# Milestone 232 — Floating-point tolerance in the BTS spatial-subdivision test

Completed: 2026-10-15. Reported failure on another machine:
`tests/test_bts_round2.py::test_spatial_subdivision_preserves_total_map_with_bend_edges` at
`assert np.all(np.array(profile['peak_beta_m'])>=spatial_profile(lat,1)['peak_beta_m'])`.

**Cause.** For the test lattice both peak betas lie exactly on element boundaries (s = 15.116 m and 21.789 m), which
the 8-subdivision mesh also samples. The two values are mathematically equal but reached through different matrix
products, so they differ by rounding: +3.3e-13 and +5.4e-13 m here, slightly negative on the other machine's
BLAS/NumPy build. The exact `>=` was therefore platform-dependent.

**Fix.** The finer-mesh peak must not fall below the boundary peak by more than a relative 1e-12. The test's intent
is unchanged: a refined mesh cannot miss a sampled maximum. No source code or result changed.

**Checks.** `tests/test_bts_round2.py` and `tests/test_bts_round3.py`: 18 pass.
