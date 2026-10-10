# Pulsed-magnet and timing considerations (revision task C8)

Date: 2026-10-10. Addresses R1-08 and R2-7. All numbers are written by `scripts/build_revision_figures.py` (step
`pulse`) into the manuscript macros. Their sources are:
- the selected operating point `results/journal_campaign_02/operating_point_3d.json` (x_inj = −19.5 mm, S = 0.85);
- the exact-field transparency analysis (task C7);
- the measured angular window (task C3).

## Scope adopted in the manuscript

All capture and transparency results apply to an **ideal single-pass spatial field**: a field scale S at the injection
passage and none on any other passage. Pulse shape, after-turn residual field, train uniformity, coating or chamber
eddy currents and conductor size are not modelled. They enter only through the requirements below, which turn each
unmodelled effect into a quantitative specification. The manuscript makes no practical transparency claim beyond these
requirements.

## Requirements and estimates

| Effect | Estimate | Requirement |
| :--- | :--- | :--- |
| Revolution period | T₀ = 799.30 m / c = 2.666 µs | — |
| Residual field on the turn after injection (fraction r of peak) | injected centroid at −2.6 mm, where the full kick is 0.39 mrad | r·0.39 mrad < 0.074 mrad (1/10 of the 0.74 mrad window) ⇒ **r ≲ 0.19** |
| Residual field two turns after injection | centroid at +6.3 mm, full kick 3.82 mrad | **r ≲ 0.02**; the pulse must be essentially over within two turns (≈ 5.3 µs) |
| Three turns after | centroid at +8.0 mm, full kick 4.81 mrad | as above |
| Stored beam, aligned kicker | odd field ⇒ zero centroid kick for any pulse amplitude | none (symmetry) |
| Stored beam, offset kicker, any time along the pulse | response scales with the instantaneous field ≤ peak response | bounded by the offset results of C7 (0.10 σ_x at 0.2 mm) |
| On-axis dipole residual (eddy currents, conductor or chamber asymmetry) | A = β b₀ | b₀ < 0.1 σ_x/β_x ⇒ **< 4×10⁻⁵ of the peak kick** |
| On-axis gradient residual | Δν = β k₁/(4π) | Δν < 10⁻⁴ ⇒ **< 7×10⁻⁵ of the peak gradient** |
| Timing jitter Δt on a half-sine pulse of length τ at its peak | ΔS/S = ½(πΔt/τ)² = 1.7×10⁻⁷ – 4×10⁻⁶ for τ = 5–8 µs and Δt = 1–5 ns | negligible next to the 0.5 % amplitude jitter |
| Coating-induced quadrupole fields during the pulse | observed at the MAX IV MIK (Kallestrup 2019) | outside this study; must be assessed with the chamber design |

The centroid positions on later turns use the linear one-turn rotation at the NKM centre: fractional tune 0.179;
β_x = 16.27 m, α_x = −0.145; starting from the 3-D exit state of the nominal centroid. They are centroid estimates,
not tracked distributions.

## Change to the error model

The previous error model represented NKM timing jitter as an additive dipole kick, which breaks the zero-field
symmetry on axis (Reviewer 1, M7). In campaign 02 (`--timing-model scale`) it is represented as the field-scale change
that gives the same kick change for the nominal injected centroid: ΔS/S = Δθ/|x′_inj|. This leaves the stored-beam
field zero on axis. The assumed rms timing equivalent is 0.1 µrad, small next to the 0.5 % amplitude jitter.
