# Contribution, scope and comparison with existing systems (revision task C9)

Date: 2026-10-10. Addresses R1-01, R2-10, R2-15 and R2-20.

## Scope

**Lattice.** A simulation study of one wire-based NKM design for the **Korea Light Source (KLS)**, the 4 GeV
fourth-generation storage ring formerly referred to as K4GSR/4GSR. The ring is modelled with the design lattice file
`K4GSR_HBIv4-1` (high-beta injection straight, revision v4-1): circumference 799.30 m, ε_x = 61.6 pm, on-momentum DA
at the kicker −12/+13 mm. The facility name was confirmed by the author on 2026-10-10. The paper presents the design
lattice, not an operating machine.

**Assumptions.** All error amplitudes and the booster beam parameters are design assumptions, not machine
specifications. The study is an ideal-lattice design study with bounded sensitivities to ring errors and chamber
apertures (task C4).

## Contribution beyond existing near-extremum injection ideas

Liu et al. (IPAC'16) identified kick nonlinearity across the injected bunch and the bunch size as the efficiency
limit. Placing the beam near the kick extremum is an established design idea. The revision's distinct, demonstrated
results are listed below.

**1. Finite-length self-deflection.**
- **Effect.** In a strongly nonlinear kicker the beam's own deflection inside the magnet changes the injection
  physics. The sagitta |K|L/8 is 0.32 mm here.
- **Evidence.** Thin kick maps misplace the matched angle by 0.22 mrad. They overestimate the sensitivity to one sign
  of angle error.
- **Test.** The exact 3-D field and the "bent-path" model agree to 10⁻⁷ rad. Straight-path averaging does not
  reproduce them (`kicker_model_validation.md` §5).
- **Generalisation.** A magnet-length scan at fixed integrated kick gives a design trade-off and a limit beyond which
  no matched solution exists.

**2. Vertical defocusing of the off-axis injected beam.**
- **Effect.** Near the kick extremum the field is vertically defocusing, which costs about 5 points of capture in this
  design.
- **Error found.** A sign error in the stored kick map (a non-curl-free vertical component) had hidden this.
- **Generalisation.** Any kick-map-based NLK study should verify ∂Δx′/∂y = ∂Δy′/∂x.

**3. Transparency is a symmetry statement.** For the aligned kicker, transparency is exact (an odd kick on a centred
beam). The physically meaningful quantity is the alignment and residual-field tolerance:
- centroid amplitude 0.016/0.10/1.5 σ_x for 0.1/0.2/0.5 mm offset;
- the on-axis dipole residual must stay below about 4×10⁻⁵ of the peak kick for A < 0.1 σ_x (task C8).

**4. Capture robustness as tolerance curves** against the booster jitter, the kicker–orbit offset and the injected
emittance, rather than one assumed budget (task C6). The capture loss is traced to the transmission of booster
extraction jitter through the transfer line.

## Comparison with existing systems

Values are as reported in the cited sources. Definitions differ between sources: injection efficiency measured over
the full injection process, against capture over 500 turns in simulation. The table is therefore qualitative, not a
ranking.

| System | Kicker type | Reported stored-beam disturbance | Reported injection efficiency | Source |
| :--- | :--- | :--- | :--- | :--- |
| KEK-PF (2.5 GeV) | pulsed sextupole | reduced relative to bump injection | — | Takaki 2010 |
| BESSY II (1.7 GeV) | NLK, field maximum 10–12 mm off axis | NLK expected to reduce the bump distortion by ≈ 30× | up to 97 % with optimised sextupoles | Atkinson 2011; Gora 2023 |
| MAX IV (3 GeV) | MIK | meets the < 10 % σ transparency specification | — | Alexandre 2021; Kallestrup 2019 |
| SOLEIL (2.75 GeV) | MIK (copy) | < 2 % of rms size measured | — | Ollier 2023 |
| SIRIUS (3 GeV) | NLK; booster emittance 3.5 nm | — | design 99 % at −9 mm DA; ≈ 85 ± 8 % with design sextupoles, improved by online optimisation | Liu 2016; Velloso 2023 |
| This work: KLS design lattice (4 GeV, simulation) | four-loop wire NKM, 0.525 m | exactly zero when aligned; 0.10 σ_x at 0.2 mm offset | capture over 500 turns at the selected point (3-D model; see paper) | — |

The ring energies of KEK-PF, MAX IV, SOLEIL and SIRIUS are general facility parameters, not taken from the cited
papers. They are context only and are not cited as results.

**Common finding.** Every operating NLK/MIK reaches its efficiency only after DA-oriented sextupole optimisation
(BESSY II, SIRIUS). This is consistent with this study's ideal-lattice capture being an upper bound, and with its
conclusion that the dynamic aperture and the injected-orbit stability, not the kick strength, set the limit.

## Journal framing (R2-20)

The venue is undecided; the revision is venue-neutral.
- **Instrumentation/methods journal:** emphasise contributions 3 and 4 and the validated field model.
- **Beam-physics journal:** emphasise contributions 1 and 2.

The manuscript keeps both, with the mechanism and the vertical effect presented as the physics results and the
tolerance curves as the design guidance.

## Round-3 positioning against Sun et al. (2020) (task E2)

**What Sun et al. establish.**
- An eight-conductor NLK of the same four-quadrant topology as the present NKM.
- Segmented drift–kick–drift tracking through a Biot–Savart field, with Runge–Kutta integration as the reference.
- A finite three-dimensional conductor model with return loops, which showed that fringe fields did not
  significantly change ALS injection efficiency.
- MOGA optimisation of conductor positions and injection conditions, with field tolerances near the axis.

None of these tools is claimed as new here.

**What differs.**

| Quantity | ALS (Sun et al.) | This study |
| :--- | :--- | :--- |
| Kicker length | 0.28 m | 0.525 m |
| Incoming angle | 0.08 mrad at the septum; nearly parallel injection | 4.85 mrad from a septum 2.26 m upstream, cancelled by the kicker |
| Kick | ≈ 1 mrad (estimated from their published B_y ≈ 0.02–0.025 T over 0.28 m at 1.9 GeV) | 4.89 mrad peak |
| Sagitta \|K\|L/8 | ≈ 0.04 mm | 0.32 mm, about 3 % of the 9.4 mm kick-lobe FWHM |

The two questions also differ:
- Sun et al. compare **field models** (infinite against finite conductors) along the tracked path.
- The present study compares **trajectory approximations** (a single thin map against sliced maps and the 3-D
  field) at fixed field.

These are different approximations. The ALS finding and the present result are therefore consistent: a much smaller
sagitta places the ALS design where a single thin map would also be adequate. The present contribution is the
quantified thin-map error versus η (E3), the matched-angle shift and the sign-dependent error response at this η.
