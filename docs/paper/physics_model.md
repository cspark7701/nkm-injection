# Canonical physics model for the journal campaign (Task 002)

Frozen 2026-10-09 as injection-study schema version 1
(`src/nkm_injection/injection_study.py`, example `config/injection_study_v1.json`).
Supersedes the linear-map injection model used in `run_multiturn_injection.py` for all
article claims. Units: m, rad, eV, T, T m; reported mm/mrad conversions are explicit.

## 1. Sources and what they contain

| Input | Content (verified in `NKM_radia*.ipynb`, read-only) |
| :--- | :--- |
| `By.txt` | Transverse profile B_y(x) at y = 0 and z = 0 (magnet centre), 201 points over x in [−50, 50] mm; RADIA vertical field `bz`. **Not** a longitudinal profile. |
| `kickmap_file.txt` | 201×201 grid, x, y in [−50, 50] mm. Section 1 = ∫B_x dl/(Bρ), section 2 = ∫B_y dl/(Bρ), each in **mrad** (RADIA `FldInt` in T·mm divided by E/c in T·m), at 4 GeV, length 0.525 m. No charge sign applied. The header "Units: meters, Tm" is incorrect. |
| `K4GSR_HBIv4-1.mat` | 4 GeV ring. The study lattice inserts `NKM` (0.525 m drift) after `SectionStart` and `NKMUPRING` (2.0 m drift) before `SectionEnd` (`build_storage_ring_nkm_lattice`). 3,483 elements, C = 799.297 m. |

On the midplane the kick map equals By.txt·L/(Bρ) to ~1e−10 relative, so the two files are
not independent validations of each other.

## 2. Ring (derived from the lattice, not assumed)

6D with RF and radiation pass methods from the source lattice. At the NKM centre: β_x = 16.27 m,
α_x = −0.145, β_y = 5.60 m, α_y = −0.510, D_x = 0.33 mm. Tunes 68.179/23.260, chromaticities
+6.02/+3.39, equilibrium ε_x = 61.6 pm·rad, σ_δ = 1.264e−3, σ_z = 3.63 mm, energy loss 1.10 MeV/turn,
synchrotron period ≈ 290 turns, horizontal damping time 10.5 ms (≈ 3,950 turns). The 6D closed
orbit (δ_co = 9.6e−6, ct_co = 0.36 mm) is added to all generated particles. The lattice has
no physical aperture elements; vertical stored emittance is taken as 10 % of ε_x (assumption).

## 3. Injection geometry and frames

AT ring coordinates (x, p_x, y, p_y, δ, ct), canonical momenta normalised by p₀.

1. Injected bunch created at the septum exit (entrance of `NKMUPRING`) with the BTS-exit
   distribution plus centroid (x_inj, x′_inj); nominal x_inj = −20 mm.
2. Septum blade inner (stored-side) edge at −16 mm, thickness 2 mm: injected particles with
   x ≥ −18 mm at creation are lost (`septum_creation`); circulating particles with x < −16 mm
   at the `NKMUPRING` entrance are lost on every turn (AT aperture).
3. Drift 2.0 m + `SectionEnd` + `SectionStart` + half NKM (0.2625 m) to the NKM centre.
4. One thin kick at the NKM centre on the first passage only (single-turn pulse); observation
   point and ring start = NKM centre (ring re-ordered, otherwise identical).
5. Native element-by-element tracking (`backend="element"`) is the reference model;
   the linear one-turn map (`backend="map"`, segment maps around the 6D closed orbit with the
   same septum check) is a cross-check only.

## 4. Kick models and sign convention

Δp_x = P·S·K_x(x − Δx_NKM, y) + k_off, Δp_y = P·S·K_y(...), with K the stored map value in rad,
S = field scale, P = polarity. **P = +1** (the electron kick equals the stored value) is the
operating polarity: it gives Δp_x < 0 at x < 0, which cancels the positive incoming angle of
a beam travelling from the septum towards the axis. It corresponds to the coil current opposite
to the RADIA notebook sign (I = −3000 A) under the identification x_AT = x_RADIA; the RADIA→AT
handedness is otherwise undocumented, and the polarity is a coil-current choice.

The thick By.txt tracker (`run_tracking_convergence.py`) applies the electron Lorentz sign to the
notebook polarity, hence the opposite sign (+2.19 mrad at −16 mm). It applies By(x) uniformly
over L and is used only for numerical slice convergence, not for injection claims.

Calibrated controls, all referenced to x_ref = nominal injected centroid at the NKM centre:
`dipole` (uniform kick equal to the map kick at x_ref), `linear` (first-order Taylor expansion
of the map at x_ref), `off`. Canonical-momentum kicks are independent of δ.
Coordinates outside the map domain are lost with cause `outside_field_map` (no extrapolation).

## 5. Beams

* Injected: BTS target Twiss at the septum exit (β = 2.3365/4.2562 m, α = −0.0163/0.0178,
  D = 0.0809 m, D′ = 0.0475), ε = 100/10 nm·rad, σ_δ = 1.1e−3, σ_z = 13.4 mm (booster
  assumptions carried by the optimisation configuration). Coupled studies replace the
  Gaussian by particles tracked through the selected (or baseline) BTS.
* Stored: equilibrium Gaussian at the NKM centre (Section 2).

## 6. Observables

* Capture: fraction of injected particles alive after N turns of native tracking (losses:
  septum, map domain, AT loss incl. numerical divergence > 1 m). Binomial Wilson intervals.
* Stored-beam disturbance (one NKM pass, linear optics at the NKM centre, 10⁵-particle sample):
  centroid amplitude A = β_x|⟨Δp_x⟩| and A/σ_x; filamented emittance growth from the exact
  kick spread. Validated against native tracking in Task 003.
* Dynamic aperture: native tracking of single particles over x, x′ and δ grids.

## 7. Error model coverage (tolerance study vs capture study)

From `results/journal_campaign_01/task002/error_coverage.json` (+3σ one at a time, selected optics):

| ErrorBudgetConfig field | σ | Tolerance study (optics) | Capture study (Task 006) |
| :--- | :--- | :--- | :--- |
| quad_k_rel_std | 1e−3 | mismatch, β_max | applied (BTS tracking) |
| dipole_b_rel_std | 5e−4 | **no effect** (sampled, not applied) | applied (BTS dipole field) |
| booster_x/xp_jitter | 0.5 mm / 0.2 mrad | **no effect** | applied (beam centroid) |
| quad_dx/dy_std_m | 100 µm | β_max only (feed-down) | applied (orbit through BTS) |
| quad_roll_std_rad | 0.5 mrad | mismatch, β_max | applied |
| quad_ds_std_m | 0.5 mm | **no effect** | not modelled |
| energy_dp_p_std | 1e−3 | mismatch, β_max | applied (rigidity + injected δ) |
| beta_mismatch_rel_std | 5 % | mismatch, β_max | applied (booster Twiss) |
| nkm_scale_std | 0.5 % | stored kick only | applied (field scale) |
| nkm_dx_std_m | 200 µm | stored kick only | applied (map offset) |
| nkm_timing_std_mrad | 1e−4 | **no effect** | applied as additive kick error (rad ×1e−3) |
| ring_co_x_std_m | 200 µm | stored kick only | applied (orbit offset at NKM) |
| septum_x_std_m | 100 µm | **no effect** | applied (septum edge and x_inj) |
| ps_quantization_std, emittance_rel_std, espread_std, ring_beta_rel_std | — | never sampled | emittance and energy spread sampled; others not modelled |

The 11-category OAT ranking therefore reports zero for six categories by construction.
All tolerance values are assumptions carried from the existing budget; none has measured or
design-specification justification in the repository.

## 8. Normalisation of optimisation objectives

The deterministic optimiser normalises β residuals by 0.05 m, α by 0.01, D_x by 2 mm and D′ by
1e−3; the dimensionless sum is reported as merit. MOGA objective f₃ adds D_x (m) and D′ (rad)
in quadrature, which is dimensionally inconsistent; MOGA is therefore excluded from main-text
claims (Task 007).
