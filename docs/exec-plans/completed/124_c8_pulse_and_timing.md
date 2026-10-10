# Milestone 124 — C8: Pulsed-magnet and timing requirements

Completed: 2026-10-10. Consolidated task C8 (R1-08, R2-7). Record:
[`pulse_and_timing.md`](../../paper/pulse_and_timing.md).

**Scope.** Results apply to an ideal single-pass spatial field. Unmodelled pulse effects become requirements, computed
by the `pulse` step of `scripts/build_revision_figures.py` from the operating point, the C7 transparency analysis and
the C3 angular window (0.74 mrad at 80 % capture):
- after-turn residual field r ≲ 0.19 on the next turn and r ≲ 0.02 two turns later, so the pulse must end within
  about 5.3 µs;
- on-axis dipole residual < 4×10⁻⁵ of the peak kick;
- gradient residual < 7×10⁻⁵ of the peak gradient;
- ns timing jitter on a half-sine pulse is negligible.

**Error model.** Timing error is now a field-scale error (campaign 02).
