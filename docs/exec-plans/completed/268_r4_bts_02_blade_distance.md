# Milestone 268 — R4-BTS-02: blade-distance sweep

Completed: 2026-10-31. Round-4 task R4-BTS-02 (Reviewer 2 R2C-04).

**Computation.** `results/bts_round4_campaign_20261030/blade_b`, analytic, with the same 200 steered realizations
as the jitter stage (seeds 94001–94005).
- **Distances:** d_b = 1.0, 1.25, 1.478, 1.75, 2.0, 2.5 and 3.0 mm.
- **Jitter levels:** ×1 and ×0.1.
- **Observable:** the jitter-integrated loss.
- **Tolerance distance:** found by log-linear interpolation.

**Results.**
- **Assumed jitter.** A loss below 0.1 % needs d_b ≥ 2.05 mm (matched reference), 2.01 mm (low beta) or 1.64 mm
  (loss-based). At d_b = 1 mm the losses are 6.6 % and 3.0 %.
- **Tenfold smaller jitter.** The loss is at most 2 × 10⁻⁶ even at 1 mm.

**Article changes.**
- **Section 4.5:** a blade-distance paragraph and Figure 5 (`figures/round4_blade_distance.pdf`).
- **Ring-acceptance cost:** a larger d_b moves the injected beam away from the stored beam. This belongs to the
  injection calculation of the companion study.
- **TDR comparison:** a 1 mm thin septum either adds 1 mm to d_b or lets the injected beam move 1 mm closer.

The figure was checked visually: the legend and labels are clear of the data, and values below 10⁻¹² are omitted
rather than drawn at the axis floor. The isolated build is clean; the installed PDF is rebuilt in R4-BTS-09.
Protected files are unchanged.
