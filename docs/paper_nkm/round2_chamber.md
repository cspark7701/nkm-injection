# Declared chamber and capture scenario (D6)

The author-provided dimensions in [dependent_answers.md](dependent_answers.md)
define the regular arc half-width/height as 12/9 mm and the centre-bend vertical
half-height as 4.87 mm. The octagonal corner geometry is unavailable. Tracking
therefore compares a rectangle and its inscribed ellipse; the ellipse is the
reference scenario. The configuration is [round2_chamber_config.json](round2_chamber_config.json).

The NKM storage-ring straight has an assumed rectangular clearance of ±30 mm
horizontally and ±15 mm vertically. These are study assumptions, not a measured
ceramic chamber. The separate incoming septum-to-NKM transport retains the source
lattice and the septum creation cut; no additional surveyed incoming-line chamber
is claimed. The filament/conductor domain is checked separately. This limits the
interpretation to conditional capture after the specified incoming transport.

Nineteen ordinary straights are identified by the sequence LM11 / SectionEnd /
SectionStart / LM11. The first nineteen are a declared installation scenario,
since a surveyed IVU map is unavailable. Each has a 3 m central region, made by
splitting the existing two 2.94 m drifts without changing magnet positions or
circumference. Gap checks occur at entrance, centre and exit. The reference open
half-gap is 9 mm; the closed stress scenario uses 2.5 mm. The latter is a magnetic
gap and an upper bound on vacuum clearance if a liner is present. Metadata centre
indices refer to the original lattice before drift splitting.

The design booster emittances are 7.67/0.767 nm rad and rms relative energy spread
is 0.00106. Each ring/profile/model uses seeds 1001 and 1002, 500 Gaussian particles
per seed, transported through the selected matched BTS, then 500 native nonlinear
turns with RF and radiation. Injection is at x = −19.5 mm, angle = 4.852537856 mrad
and NKM strength scale 0.85. The ideal NKM and calibrated dipole share particles.
Losses include upstream transport, septum creation, injection transport, field
domain and native ring losses. Ring loss records contain particle ID, zero-based
turn, element-entrance longitudinal position from the NKM centre, element and plane. For an ellipse,
the plane label denotes the larger normalized transverse coordinate at loss.

The ideal reference gives 970/1000 captured particles with the NKM and 973/1000
with the paired dipole. Rectangle/ellipse and open/closed gaps give the same nominal
counts. The aperture-size grid uses rectangular bounds. At arc half-widths 10, 12 and 15 mm, capture is respectively 81.7%, 97.0%
and 99.7% for each tested arc half-height (4.87, 7.5, 9 mm). Thus 10 mm is the
smallest **tested rectangular-grid** width meeting 80% in this ideal-ring sample; 12 mm is the
smallest tested width retaining the reference 97%. Neither is an interpolated
engineering minimum or a guarantee for corrected-error machines.

The ten corrected seeds are 5501–5510 from D5. Their capture distribution and loss
histograms are generated from `d6_corrected_chamber/chamber_summary.json`, with each
ring given equal incident-particle weight. The bootstrap for the nominal NKM-minus-
dipole difference resamples paired particles (10,000 draws, seed 1729), conditional
on these two bunches and the model. No ensemble confidence interval is assigned to
the ten deliberately selected ring scenarios.

Horizontal acceptance uses 65 deterministic launches over ±16 mm at 0.5 mm spacing,
zero vertical launch and momentum offset, and 500 native turns. Reported boundaries
are the first failed grid points, not exact stable edges. The ideal first failed
points are −11 and +12.5 mm; corrected-ring negative first failures range from
−10 to −7 mm. These chamber-limited acceptance grids replace the aperture-free
D5 grid in the final figure.

Artifacts remain under `results/journal_campaign_03/`: `d6_chamber_full/`,
`d6_corrected_chamber/`, and `d6_chamber_da.json`. The manuscript macros, figure 11
and updated figure 10 consume the manifest-recorded summaries.
