# Kicker-model validation and finite-length mechanism (revision tasks C1, C2)

Date: 2026-10-10. Addresses R1-02, R1-03, R2-1 and R2-14 (consolidated plan C1–C2).

Raw results are kept outside git in `results/journal_campaign_02/`:
- `c1_kicker_validation/kicker_model_validation.json`
- `c1_vertical_diagnostic/kicker_model_validation.json`
- `c2_mechanism/finite_length_mechanism.json`

Drivers:
- `scripts/validate_kicker_models.py`
- `scripts/analyze_finite_length_mechanism.py`

Field model: `src/nkm_injection/wire_field.py` (tests in `tests/test_wire_field.py`).

## 1. Exact 3-D field of the RADIA geometry

The RADIA model in `NKM_radia.ipynb` was read only; no protected notebook was executed.
- **Geometry:** four closed rectangular filament loops, one per quadrant. The inner wire is at (±5.3, ±5.3) mm and
  the outer wire at (±10.25, ±10.25) mm. The wires are 525 mm long, with straight end connectors at s = ±262.5 mm.
- **Current:** 3000 A. The RADIA frame (x, s, y) is left-handed relative to the beam frame (x, y, s), which is why
  RADIA's −3000 A appears as +3000 A here.
- **Field evaluation:** the field of straight filaments in vacuum is evaluated in closed form (Biot–Savart). It
  includes the fringe and end-connector fields, but no iron, chamber or time dependence.

**Agreement with `kickmap_file.txt`.** This was checked on 3,657 nodes with |x|, |y| ≤ 30 mm that lie at least
1.5 mm from a wire:
- the map's horizontal kick equals ∫B_y ds/Bρ to within 6.9×10⁻¹² rad (4.0×10⁻¹⁰ relative);
- the map's vertical kick equals **+∫B_x ds/Bρ** to within 6.4×10⁻¹² rad.

The independent field model therefore reproduces the RADIA integrals to numerical precision, and confirms how the map
was written.

**Vertical sign error found and corrected.** The stored pair (∫B_y, +∫B_x) is not curl-free: ∂Δx′/∂y = −∂Δy′/∂x.
The physical kick pair is (∫B_y, −∫B_x)/Bρ.
- **Effect:** the thin model of journal campaign 01 applied the vertical kick with the wrong sign. On the midplane
  this is zero, but off-plane particles near the injected centroid were focused vertically instead of defocused.
- **Fix:** `KickModelEvaluator` now uses `vertical_sign = −1`; the legacy behaviour is available as +1 for
  comparison. The linearised control gains the curl-free partner −k₁y.

## 2. Sliced finite-length tracker

`FilamentNKMKicker` integrates the exact field over s ∈ [−0.45, 0.45] m in AT canonical coordinates:
- **Kick:** dp_x/ds = P S (B_y − y′B_s)/Bρ and dp_y/ds = P S (−B_x + x′B_s)/Bρ. The kick acts on the canonical
  momentum and carries no 1/(1+δ) factor.
- **Drift:** uses the slope p/(1+δ). This resolves R2-14 as qualified by Reviewer 1.
- **Losses:** a particle within 1 mm of a conductor, or outside |x|, |y| ≤ 50 mm, is lost. Fields are never
  extrapolated.

**Convergence** of the exit angle of the nominal centroid at the operating point (x_inj = −20 mm, S = 0.85,
x′ = 4.869 mrad), relative to 1280 slices and a ±0.8 m span:

| Slices | ±0.45 m span | ±0.8 m span |
| ---: | ---: | ---: |
| 80 | 7.8×10⁻⁶ rad | 3.1×10⁻⁵ rad |
| 160 | −1.6×10⁻⁷ | 5.4×10⁻⁶ |
| 320 | −9.4×10⁻¹⁰ | −3.3×10⁻⁹ |
| **640 (adopted)** | **−6.7×10⁻¹¹** | −7.5×10⁻¹⁰ |

**Momentum dependence:** the exit angle changes by 0.37 µrad per 10⁻³ in δ, which is negligible against the angular
window.

## 3. Centroid response at the operating point

Values are the exit p_x and p_y in mrad after the magnet, referred to the NKM centre.

| Case | Thin map (physical sign) | Thick, uniform 1-D profile | Exact 3-D |
| :--- | ---: | ---: | ---: |
| nominal | 0.000 | +0.093 | +0.088 |
| septum Δx = +0.5 mm | −0.016 | +0.019 | +0.013 |
| septum Δx = −0.5 mm | +0.092 | +0.227 | +0.223 |
| septum Δx′ = +0.3 mrad | +0.310 | +0.317 | +0.310 |
| septum Δx′ = −0.3 mrad | −0.155 | −0.015 | −0.020 |
| y = +1 mm: p_y | +0.134 (legacy: −0.134) | 0 (no vertical model) | **+0.248** |

The 1-D thick model and the 3-D model agree horizontally to within 5 µrad. Their difference from the thin map is
therefore a finite-length effect, not a field-representation effect. Vertically only the 3-D model is complete. Its
off-axis vertical kick is about twice that of the straight-line thin map, because the trajectory inside the magnet
samples the field off the straight line.

## 4. Capture on identical bunches

Operating point as above; coupled matched-BTS bunches; native tracking; 500 turns; 4 × 500 particles (seeds 42, 123,
777, 2025).

| Model | Mean capture | Paired difference vs thin (physical) |
| :--- | ---: | ---: |
| thin map, legacy vertical sign (campaign 01; paper value 91.1 %) | 91.05 % | +1.35 ± 0.69 points |
| thin map, physical vertical sign | 89.70 % | — |
| 3-D, thin-matched angle 4.869 mrad | 84.80 % | −4.9 ± 1.5 |
| 3-D, 3-D-matched angle 4.647 mrad | 81.75 % | −8.0 ± 1.9 |

**Vertical diagnostic** (seeds 42 and 123, 3-D-matched angle):

| Model | Capture |
| :--- | ---: |
| 3-D | 82.5 % |
| 3-D with the vertical kick suppressed | 87.8 % |
| 1-D thick | 87.4 % |

The roughly 5-point loss of the 3-D model beyond the 1-D thick model is caused by the NKM's vertical kick on the
off-axis injected beam. At x ≈ −9 mm the field defocuses vertically by about 0.25 mrad per mm. The legacy sign error
hid this, because it reversed the defocusing into focusing.

**Re-matching makes capture worse:** re-matching to zero exit angle lowers 3-D capture by about 3 points. Zero
centroid angle after the magnet is therefore not the capture optimum. Task C3 scans the angle directly.

## 5. Mechanism of the thin/finite-length difference (C2)

Four single-centroid models were compared, each at its own matched angle:
- **Thin:** the kick at the magnet centre.
- **Straight:** the kick density K(x)/L sampled on the undeflected straight line.
- **Bent:** the same density sampled on the self-consistent deflected path.
- **3-D:** the exact field.

| Model | Matched angle | Amplitude at Δx′ = −0.3 / 0 / +0.3 / +0.45 mrad |
| :--- | ---: | :--- |
| thin | 4.870 mrad | 9.74 / 9.08 / 10.28 / 12.38 mm |
| straight (path averaging only) | 4.762 | 9.92 / 9.30 / 10.31 / 12.14 |
| bent (self-deflection) | 4.6476 | 10.16 / 9.56 / 9.45 / 9.94 |
| 3-D | 4.6475 | 10.16 / 9.57 / 9.45 / 9.94 |

The bent model reproduces the exact 3-D field: the matched angles agree to 10⁻⁷ rad and the amplitudes to 0.01 mm.
Averaging over the slanted straight path does not.

**Mechanism.** The finite-length effect is the beam's own deflection inside the magnet. The kick of about 5 mrad
displaces the trajectory outward by roughly the sagitta |K|L/8 = 0.32 mm, so the field is sampled away from the
straight line. A positive septum angle error moves the centroid inward, past the kick extremum at x = −8.5 mm. The
outward self-deflection then carries the trajectory back across the extremum, where the kick is stronger and
compensates the error. The thin model cannot represent this feedback: it overestimates the sensitivity to positive
angle errors and underestimates the nominal amplitude.

**Magnet-length scan** (bent model at a fixed integrated kick profile, own matched angle):

| L | Matched x′ | Amplitude at −0.3 / 0 / +0.3 mrad | Sagitta |
| ---: | ---: | :--- | ---: |
| 0.20 m | 4.830 mrad | 9.76 / 9.17 / 9.88 mm | 0.12 mm |
| 0.35 m | 4.771 | 9.88 / 9.30 / 9.62 | 0.21 |
| 0.525 m | 4.648 | 10.16 / 9.57 / 9.45 | 0.32 |
| ≥ 0.75 m | no matched solution | — | ≥ 0.46 |

**Design implication.** At a fixed integrated kick, a longer magnet raises the nominal amplitude but lowers the
sensitivity to positive angle errors. Beyond about 0.75 m, self-deflection pushes the trajectory past the kick
extremum, and no angle-matched solution remains for this geometry. Kick-map (thin) models of NKMs should be used only
when the sagitta |K|L/8 is small compared with the width of the kick extremum; here 0.32 mm against an extremum full
width of a few millimetres.

## 6. Model selection

**The exact 3-D filament model, with 640 slices, is the principal model for all revised results.** Reasons:
- it is independent of interpolation;
- it reproduces RADIA to 10⁻¹⁰ relative;
- it is converged;
- it includes the finite-length self-deflection and the physical vertical kick, each of which changes capture by
  several points.

The thin map is retained only as a comparison.

**Remaining omissions:** iron, chamber and eddy-current fields; pulse time dependence (task C8); conductor size. A
1 mm loss radius is assumed for the conductors, and no particle in these runs came within it.
