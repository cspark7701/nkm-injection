# Round 2 beam and error budget

The design extraction beam is 7.67 nm rad horizontally, with assumed 10% vertical emittance and design rms energy spread 0.106%. These values come from TUPC12 table 1, as verified in author input A4; the 100 nm rad campaign is a historical sensitivity case. Booster Twiss and bunch length remain the selected study assumptions. No measured extraction jitter or septum current stability is supplied.

All errors are untruncated Gaussian rms values. A realization draws static machine and shot quantities once. Sampling of the three new shot terms uses an independent seeded stream, leaving all historical draws unchanged. Units below are public-interface units.

| Term | RMS | Source or reason | Class |
| :--- | :--- | :--- | :--- |
| BTS quadrupole gradient | 0.1% | Assumed strength-error sensitivity, not a measured specification | Static |
| BTS dipole field | 0.05% | Assumed rigidity/trajectory sensitivity | Static |
| Quadrupole x/y offset | 100 µm each | Assumed alignment sensitivity | Static |
| Quadrupole roll | 0.5 mrad | Assumed coupling sensitivity | Static |
| Booster x / x′ | 0.5 mm / 0.2 mrad reference | Not public; parametrized over 0–1 of this scale | Shot |
| Booster beta mismatch | 5% | Assumed extraction-optics sensitivity | Static |
| Emittance variation | 10% relative | Assumed variation about the sourced design value | Shot |
| Mean energy variation | 0.1% | Assumed mean-energy sensitivity; distinct from within-bunch spread | Shot |
| Energy-spread variation | 1e-4 absolute | Assumed spread sensitivity about 0.00106 | Shot |
| NKM amplitude | 0.5% | Assumed pulser sensitivity; bump-kicker ±0.2% reproducibility is not an NKM specification | Shot |
| NKM x placement | 0.2 mm | Assumed magnet-to-orbit sensitivity | Static |
| Ring orbit at NKM | 0.2 mm | Assumed residual displacement in capture model | Static |
| Septum position | 0.1 mm | Assumed geometry sensitivity | Static |
| Thin-septum bend strength | 0.1% relative | Parametric assumption; no measured septum stability available | Shot |
| RF phase | 0.001 rad | Parametric longitudinal injection-phase sensitivity | Shot |
| Independent arrival time | 2 ns | Assumed timing sensitivity at peak of a 5.3 µs half-sine | Shot |

The thin-septum nominal bend is 10 mrad (TUPR52, author A4). Its strength error is an extra canonical momentum `(1+delta)*0.01*relative_error` at the septum exit, distinct from booster angle jitter. The source lattice RF is 499593472.8240743 Hz; RF-phase error translates ct by `c*phase/(2*pi*f)`. Independent arrival time translates ct by `c*dt` and multiplies the NKM field by `cos(pi*dt/tau)` at peak phase, with zero field outside the half-sine support. This separates arrival-time and RF-phase sources instead of assigning either an additive transverse dipole kick. Legacy equivalent `nkm_timing_std_mrad` is zero in the final budget, avoiding double counting. This is a single-pass timing sensitivity; D10 limits later-pass residuals.

Source-dependent septum leakage and chamber values are recorded in `dependent_answers.md`. The unspecified NKM pulser and extraction jitter are not given invented literature ranges. The published KLS bump-kicker reproducibility is a comparison, not justification for the septum assumption.

Longitudinal quadrupole placement, power-supply quantization and ring-beta scalar fields remain unmodelled in capture studies and must not be counted as applied errors. D5's distributed ring-error scenario is a separate selected scenario, with its own residual orbit and tune diagnostics. Final beam and error configurations are `results/journal_campaign_03/operating_point_design_beam.json` and `error_budget.json`.
