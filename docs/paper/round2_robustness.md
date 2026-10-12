# Final joint-error and reduced-tuning study (D8)

The final campaign is conditional on the design booster beam, selected matched
BTS, declared reference chamber, and ten corrected rings of D5. It is not a
commissioned-machine prediction. Inputs and outputs remain under
`results/journal_campaign_03/`; the final evidence manifest freezes their hashes.

`run_round2_campaign.py` requires the D5 correction gate, the complete ideal-ring
chamber reference, and all four chamber profiles for each of the ten corrected
rings before launching any ensemble. It runs three independent ensemble seeds
(42, 123, 777), each with 50 joint machine/shot draws, 200 particles per draw and
500 native nonlinear turns with RF and radiation. Both the 640-slice 3-D NKM and
the calibrated uniform dipole receive identical particles and error draws.

Each realization samples one of the ten saved corrected rings with replacement,
using a separate deterministic RNG stream keyed by ensemble seed and sample ID.
The zero-error diagnostic uses the ideal ring and is excluded from ensemble
statistics. A draw contains one static machine and one shot; it is not a nested
distribution of many shots on a fixed machine. The 150-draw bootstrap therefore
estimates the joint distribution conditional on this finite corrected-ring
population. It does not establish uncertainty over all possible ring errors.

Ideal static steering tracks the zero-input reference through the perturbed BTS
and subtracts only its horizontal position and canonical momentum from the bunch
at the septum exit. Vertical displacement, optics distortion and all shot terms
remain. The return septum aperture moves with the same sampled blade position
used at beam creation. The pulse-relative timing term scales the field of both
the NKM and the paired calibrated control; RF phase independently shifts the
longitudinal coordinate. These terms follow the sourced or explicitly assumed
[final error budget](round2_error_budget.md).

The jitter scan uses seed 42 and pairs sample IDs, particle seeds and corrected
ring IDs across scales 0, 0.25, 0.5, 0.75 and 1 of the reference 0.5 mm / 0.2 mrad
booster centroid jitter. Position-only and angle-only cases retain one reference
component and set the other to zero. All other sampled quantities remain fixed.
The full-jitter result reuses the seed-42 combined ensemble. The analysis verifies
these pairings before calculating differences from zero jitter.

Reported quantities are mean, median, tenth percentile and fraction of draws
with capture at least 80%. They are not interchangeable. Mean intervals and
paired differences use 10,000 realization bootstrap resamples, seed 1729.
The predeclared equivalence margin is one percentage point. Partial Spearman
associations control the other sampled scalar errors, vector-error RMS values,
and corrected-ring identity. Holm adjustment covers the sampled-error tests;
ring-identity indicator variables are controls, not additional physics tests.
These associations are conditional on the chosen model, not causal rankings.

## Reduced capture-based tuning

The tuning study uses the 50 seed-42 static machines. Training uses 100 fresh
particles per machine, with all shot errors and emittance/spread fluctuations
set to zero. One bounded coordinate sweep evaluates the nominal point and the
two directions of each of three knobs (seven evaluations total):

| Knob | Bounds | Step |
| :--- | :--- | :--- |
| Septum-exit horizontal position | −22 to −18.2 mm | 0.5 mm |
| Septum-exit canonical angle | 3.5 to 6.5 mrad | 0.3 mrad |
| NKM field scale | 0.7 to 1.2 | 0.05 |

Strict improvements are accepted; ties preserve the current setting. The search
records its seed, bounds, feasibility and fixed-budget termination. It does not
optimize the storage-ring sextupoles, reconfigure apertures or retune the dipole
control. The training capture count has a one-percentage-point resolution.

The selected knobs are evaluated on the same held-out 200-particle samples and
joint error draws as the untuned zero- and quarter-jitter ensembles. No held-out
capture is used to select knobs. Paired gains and their realization bootstrap
intervals quantify what this reduced search recovers.

This is ideal capture-based tuning, not a demonstrated BPM feedback system.
There is no BPM resolution, calibration, latency, actuator reproducibility or
charge-monitor noise model. Those omissions preclude an operational tuning
claim. The finite training bunch supplies sampling variation, not an instrument
resolution specification.

Each realization is written atomically. Resume requires an identical input
signature, including scientific source files, corrected lattices, configuration,
particle count, seeds and bootstrap settings. Existing complete results are
retained byte-for-byte. Generated results are never added to git.
