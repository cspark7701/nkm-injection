# Round 2 pulse and timing requirements

Native nominal-centroid tracking supplies positions after turns 1–3 at the NKM centre. Coordinates and conditional residual allowances are saved in `results/journal_campaign_03/d10_pulse.json`. The manuscript builder verifies its hash and generates the pulse macros.

Injection occurs at the peak of a half-sine of total duration tau. A return delayed by T samples cos(pi*T/tau) within the pulse support and zero outside. The allowance is an assumed one tenth of the historical 0.74 mrad conditional 500-turn window. Native positions give a maximum peak-phase duration of 5.84 µs for that allowance; no return field requires at most 5.332 µs. A 5.3 µs example has zero field on all returns. An 8 µs pulse retains 0.500 of its peak on the first return and violates the allowance.

Deterministic timing loss is 1−cos(pi*dt/tau), ranging from 7.71e-8 to 4.93e-6 for dt=1–5 ns and tau=5–8 µs. D4's 2 ns Gaussian rms is a sampling distribution, not a hard bound. Capture tracking uses a spatial single-pass field; these estimates do not simulate residual-field capture.

For a 5.3 µs pulse with its first bunch at peak, 100, 200 and 500 ns trains give approximately 0.18%, 0.70% and 4.4% field variation. At nonzero kicker-to-orbit offset, the stored centroid response scales with the sampled field. Symmetric-axis centroid cancellation does not imply unchanged full-beam moments.

A hypothetical thin-shell estimate tau_eddy≈mu0*sigma*a*t/2 gives 9.4 ns for sigma=1e6 S/m, a=15 mm, t=1 µm, and 0.47 ms for sigma=5e7 S/m, a=15 mm, t=1 mm. These illustrative parameters do not specify the NKM chamber, whose material and geometry are unavailable. Chamber-specific eddy-current multipoles and post-pulse residuals remain necessary before operational claims.

Reproduction: `.venv/bin/python scripts/analyze_round2_pulse.py --study-config results/journal_campaign_03/operating_point_design_beam.json --output results/journal_campaign_03/<new>.json`.
