# Referee report — Reviewer 1

Date: 2026-10-10. Recommendation: **major revision; do not accept in the present form.**

Manuscript: *Capture window and robustness of nonlinear-kicker injection into a
4 GeV storage ring with a small dynamic aperture*, Chong Shik Park.
Target: JINST regular research article.

This is a pre-submission assessment written in the role of an accelerator-physics
referee, not an actual journal decision or a claim of appointment by JINST.

## 1. Version and review scope

Reviewed [paper.tex](../paper.tex), the compiled [paper.pdf](../paper.pdf) (10 pages,
seven figures), [paper.bib](../paper.bib), generated numerical macros, model and
validation notes, the campaign manifest, selected raw observations and maintained
study implementations. The PDF text was checked and pages containing the operating
window and robustness figures were visually inspected. The existing
[Reviewer 2 report](reviewer2_report.md) was read as supplementary context; this
report is a separate assessment of the present evidence.

Review snapshot:

- Repository HEAD: `f34965a40781541ff1e6f9d129096ee2b30b20eb`.
- SHA-256, `paper.tex`: `776ca2d226b0af216f92b1f4f66ce0fab207d41bde6e6a22436c1cfc2b6ffd31`.
- SHA-256, `paper.pdf`: `45fbc89bccdc8399b1b479b049914c42c47031f155d5e309a63cb2e79e2cef12`.

All 35 files selected by [campaign_manifest.json](../campaign_manifest.json) were
available locally and matched their recorded hashes. Direct averaging of saved
realizations reproduced the principal capture means: 37.8467% for the thin NKM
and 47.3900% for the finite-length approximation, each from 150 realizations.
The associated saved intervals are approximately [33.05, 42.69]% and
[42.44, 52.39]%. I did not rerun the campaign, independently reconstruct the
magnet, validate every citation, or certify public access to the ignored results.
Hash agreement verifies identity of local evidence, not the physical model.

Manuscript references below use sections and source-line locations for this
snapshot. Proposed revisions are listed in the
[revision task register](reviewer1_revision_tasks.md); none is marked executed.

## 2. Decision and scientific merit

**I would not accept this version. I would invite a major revision rather than
reject the topic or redirect it automatically to a technical report.** The present
manuscript already has a research question, comparative results and a discussion
of limitations. It has progressed beyond an inventory of software capabilities.
Its strongest possible contribution is the interaction between a small nonlinear
acceptance, finite-length NKM transport and the transmission of booster jitter
through the BTS—not merely the use of RADIA, pyAT or a larger Monte Carlo sample.

JINST explicitly includes accelerator modelling and simulations and assesses
regular papers by scientific quality, originality and relevance. Thus a
simulation-only article can fit the journal; a physical experiment is not an
automatic prerequisite. This recommendation follows those criteria, not a
requirement to build the magnet. See the official
[JINST scope and editorial policy](https://jinst.sissa.it/jinst/help/JINST/JINST_about.jsp),
accessed 2026-10-10.

The following features merit retention:

- Native nonlinear ring tracking replaces the inadequate linear-map capture model.
- The transfer line supplies the injected distribution, and controls share particles.
- Capture and stored-beam disturbance are treated as competing observables.
- Combined-error ensembles use realizations as the bootstrap unit.
- Thin/finite-length discrepancies and unmet statistical targets are disclosed.

The acceptance blockers are model validity at the operating point, the statistical
meaning of the transparency and operating-window claims, and the connection of
assumed tolerances to useful design requirements. An honest limitations paragraph
helps, but does not by itself validate a headline result sensitive to those limits.

## 3. Major scientific comments

### M1. Establish one controlled kicker model for the principal conclusions

**Locations:** §§2.2, 3, 4, 5.2 and conclusions; source lines 57, 75, 96, 127–129.
**Tasks:** R1-02 and R1-03.

Nominal capture changes from 91.1% to 87.0% between thin and re-matched finite-length
models, whereas combined-error capture changes from 37.8% to 47.4%. The paired
interval for the latter gain, approximately [6.1, 13.2] percentage points, is large
enough to affect the central argument. A model that improves one ensemble and
worsens another is not contradictory; however, neither approximation has yet been
shown accurate enough to choose the physically reliable result.

`ThickNKMKicker` in `src/nkm_injection/injection_study.py` distributes the midplane
`By.txt` profile uniformly over 0.525 m and omits its vertical dependence and
fringe structure. The thin model instead uses both transverse components of a
2D integrated map. Their difference therefore combines trajectory evolution with
field-model differences; the same-angle cross-runs remove the angle confound but
not these other confounds. The reported 160 slices establish a discretization
choice, not fidelity to the actual finite magnet. Midplane agreement between
`By.txt * L` and the kick map is also not independent evidence for longitudinal
field uniformity.

Require: convergence of the actual operating-point capture and error sensitivity;
a physically consistent finite-length reference or a quantitative bound on its
omitted terms; and thin versus finite-length comparisons using matched dimensionality,
interpolation, geometry and polarity. A 3D field or angle-dependent transfer map
would be valuable, but is not the only acceptable route if an analytical field
and justified bounds control the approximation. Existing protected sources must
remain unchanged; any new field calculation requires separately authorized work.

The wrapper transports AT coordinates with paraxial back/forward drifts and a
transverse integrator that leaves longitudinal coordinates unchanged. State the
approximation and compare with a consistent AT-coordinate transport map. In
particular, do **not** insert a blanket `1/(1+delta)` into a canonical momentum
kick: distinguish `p_x/p_0` from the geometric slope and derive the conversion and
drift consistently. The existing Reviewer 2 chromatic-scaling request needs this
qualification. Show a small off-momentum check and estimate its effect on capture.

### M2. Demonstrate the proposed mechanism and make novelty explicit

**Locations:** introduction, §5.2 and §6. **Tasks:** R1-01 and R1-03.

Kick variation across a finite injected beam and the advantage of placing that
beam near a field maximum were already discussed in
[Liu et al., IPAC 2016](https://proceedings.jacow.org/ipac2016/papers/thpmr011.pdf).
That primary source also discusses phase-ellipse shaping to mitigate nonlinear
kick distortion. These established ideas cannot alone support novelty here.

A promising new result is the signed-angle response of the finite-length model:
+0.3 mrad changes the quoted amplitude by +1.31 mm in the thin model versus
−0.12 mm in the finite-length model. Replace the “plausible reason” with a
trajectory/accumulated-kick analysis, keeping the centroid, angle and field model
controlled. Show which part of the field contributes the difference and whether
it persists across beam size, energy and neighboring operating points. Explain
what follows for design or tolerance allocation beyond this one lattice.

Identify the lattice/facility and revision or explicitly call it a representative
model. Compare with the closest relevant systems using like-for-like beam and
acceptance definitions. A clear additional insight is needed; an arbitrary
minimum number of references is not.

### M3. The angular window has not been measured at the quoted resolution

**Locations:** §4, figure 4, abstract and conclusions. **Task:** R1-04.

The displayed angle scan has only three offsets (−0.5, 0, +0.5 mrad).
At the selected point, capture is approximately 80%, 90% and 39% respectively.
This demonstrates a strong, asymmetric dependence. It does not establish a
symmetric usable window of “about ±0.5 mrad” without specifying a required capture
fraction and locating the threshold crossings.

Define the useful window, for example by a declared capture threshold and its
uncertainty, rather than identifying scan endpoints with a tolerance. Refine the
angle grid adaptively near both crossings, independently confirm the selected
point and selected neighbors, and repeat with the accepted kicker model. The
maximum Wilson lower bound is a legitimate selection rule, but its interval is
pointwise: it is not a simultaneous confidence statement about an optimum chosen
from many noisy candidates. The four fresh bunches help validate the chosen point;
report their uncertainty and distinguish selection from validation.

Also test whether angle cancellation is capture-optimal. With nonzero Twiss alpha,
nonlinear acceptance and a finite bunch, zero outgoing centroid angle is not in
general the optimum. A nominal centroid rule should not silently restrict the
claimed global operating window.

### M4. Justify the dominant error distributions and report actionable tolerances

**Locations:** §5.2 and §6. **Task:** R1-05.

The conclusion that booster jitter limits injection is conditional on assumed
0.5 mm/0.2 mrad booster jitter, 100/10 nm rad emittances and the chosen transfer
optics. Provide a source or mark each as a hypothetical parameter. State
correlations, truncation, independence and which errors are static machine
realizations versus shot-to-shot fluctuations. Present the full applied error
budget in a table; distinguish sampled fields from effective physical terms.

Ideal subtraction of a trajectory at the septum is a useful diagnostic, not an
implemented steering algorithm. Specify what the subtraction removes, what it
leaves, and whether measured correction could achieve comparable residuals.
The no-jitter and correction studies support a conditional ranking within this
budget. They do not establish a universal ranking for all machines or establish
that all unmodelled ring errors are unimportant.

Derive capture versus booster/septum jitter and kicker-to-orbit offset, including
uncertainty and at least one low-capture quantile. State the stability needed to
meet an explicit operating requirement. Scan beam size/emittance or bound its
influence. If specifications are unavailable, a parameterized sensitivity result
is more defensible and useful than labelling this budget “realistic”.

### M5. Validate survival and physical acceptance at the final operating point

**Locations:** §§2.1, 3, 4 and §6. **Task:** R1-06.

The turn, particle-count and uniform-chamber checks were made at the provisional
5.75 mrad, S=1 point, rather than the selected 4.87 mrad, S=0.85 point or its
finite-length counterpart. Overlapping intervals from 200 and 1000 particles do
not prove convergence. A 500-turn DA on a 1 mm grid is a finite-time stability
slice, not a complete 6D acceptance measurement.

At the final point, provide cumulative survival and first-loss diagnostics for
nominal, boundary and representative error cases. Extend representative tracking
to at least approximately one horizontal damping time (about 3950 turns), and
increase further if late losses are still material. This is a suggested physical
scale, not proof that any fixed turn count guarantees lifetime. Verify particle
precision against a declared allowable change in capture.

State the actual apertures and septum geometry. A uniform aperture at every element
is a sensitivity test, not the chamber of a real machine. If the article retains
practical machine claims, include justified ring-error/correction and chamber
cases. Alternatively, present an explicitly ideal-lattice design study and bound
sensitivity to plausible restrictions. There is no defensible universal assertion
that ring errors must reduce DA by a fixed 20–40%, or a mandatory fixed number of
ring seeds. Use documented settings and ensemble precision to justify the study.

Separate losses at BTS, septum creation, septum return, chamber, field-domain
boundary and dynamic/numerical instability, preserving the original denominator.
The inspected combined-error runs have no BTS losses, but accounting must remain
valid when parameters change. Show beam ellipses, blade and trajectories in a
common frame, including a physical stay-clear estimate.

### M6. The aligned transparency number requires an uncertainty floor

**Locations:** abstract, §2.3, §4, figure 5 and §5.2. **Task:** R1-07.

The quoted `5e-6 sigma_x` is approximately 0.16 nm for sigma_x=31.7 micrometres.
It is obtained from a 100,000-particle sample and a bicubic interpolation of a
0.5 mm grid, whereas the stored beam has a roughly 0.032 mm rms size. Symmetry
makes the ideal centered mean kick cancel strongly; a tiny sample mean is not
by itself a resolved physical centroid response.

Quantify the standard error or use deterministic Gaussian integration and a
near-axis multipole expansion, with residual/error estimates and repeat samples.
Separate centroid shift, rms differential kick, immediate emittance change and
filamented emittance estimate. A symmetry-exact mean of zero can coexist with
nonzero emittance growth. Include vertical response and distinguish the linear
single-pass amplitude estimate from tracked multi-turn stored-beam motion.
Bilinear and bicubic answers provide interpolation sensitivity; bilinear values
are not guaranteed rigorous upper bounds without proof.

The dipole/linear control amplitudes of about 2500/2970 rms sizes are linear-optics
estimates for hypothetical kicks, not evidence of surviving stored beams at such
amplitudes. Label them accordingly; if they imply loss, report that instead of
presenting them as operational oscillations.

### M7. Pulse physics must match the stated transparency scope

**Locations:** system description, abstract and discussion. **Task:** R1-08.

A magnetostatic map applied once does not establish transparency of a pulsed
instrument. At 799.30 m circumference the revolution period is approximately
2.67 microseconds. State the pulse envelope, whether subsequent turns see a
residual field, bunch-train timing assumptions, and whether timing jitter is
represented as a scale error or an additive dipole kick. The current additive
kick surrogate is not a pulse model and can break ideal central-field symmetry.

If a realistic pulse/chamber model is outside scope, explicitly restrict the
claim to an ideal single-pass spatial field and discuss effects requiring separate
hardware validation. If practical transparency is retained as a conclusion,
provide supported pulse/eddy-current estimates and residual-field bounds. A full
hardware program is not required for a bounded simulation article.

### M8. Balance statistical comparisons and provide accessible provenance

**Locations:** §§4–5, figure 7, data availability. **Tasks:** R1-09 and R1-10.

The thin and finite-length ensembles have 150 realizations; the dipole robustness
control has 50, and the cross-angle attribution has 100. Their labels acknowledge
some differences. Principal effect estimates should use matched realizations,
with paired intervals and the corresponding N stated for every comparison.
Complete the control ensemble if necessary, or confine its quantitative comparison
to the paired seed-42 subset. Do not subtract the 150-realization NKM mean from
an unrelated 50-realization control mean.

State the precision of the nominal 91.1% versus 94.6% comparison and of fractions
above a threshold; 150 realizations do not tightly constrain a rare favorable tail.
A realization bootstrap is appropriate, but it does not remove finite-particle
noise in each realization or uncertainty in the assumed distributions. Check a
higher particle budget on selected realizations. Spearman correlations are
marginal associations among correlated predictors; intervention results are
stronger, but remain conditional on the simulated interventions.

Local provenance is good, but the selected raw files and optimization handoff live
under git-ignored `results/` and `backups_20261009/`. A code-repository link and
hash list alone do not make those observations available to a referee. Supply a
frozen accessible evidence bundle, configuration/software versions and rebuild
instructions at review time. A DOI is desirable, not a categorical precondition
for acceptance. Do not promise a release has been published before it exists.

`figure_provenance.csv` records principally JSON artifacts, while figures also
read protected map inputs and optimization configuration and recompute stored-beam
responses. Complete dependency closure and identify the actual generator version.
The historical claim matrix retains superseded B8/B10 values; expose a current
claim-to-evidence view so a reviewer need not infer which rows are authoritative.

## 4. Presentation and technical corrections

These changes support the scientific revisions; they are not a substitute for them.

| Location | Required correction |
| :--- | :--- |
| Introduction, source line 37 | “DA ... only about 12 mm” is ambiguous: −12 to +13 mm is about 25 mm full extent. Say approximate half-aperture or give both limits. |
| §2.2, line 57 | `KickPeakMrad=5.75` at x=−8.5 mm conflicts with the declared negative operating kick there. State the signed value −5.75 mrad, or label 5.75 mrad as its magnitude. |
| Abstract/introduction versus §2.3 | Distinguish the 2.0 m drift element from the 2.2625 m septum-exit-to-NKM-centre distance. Provide a geometry sketch. |
| §2.3 | Define the mismatch metric and its target. Replace exactly zero mismatch with an appropriate computed tolerance/precision. Define all beam covariance assumptions. |
| §4, figure 4 | Define capture threshold before claiming a window; show uncertainty and scan/selection resolution. |
| Figure 5 | Separate hypothetical control amplitudes from physical stored-beam survival; use consistent scientific notation and include uncertainty floors. |
| Figure 7 | Similar blue ECDFs are hard to distinguish in grayscale. Split diagnostics from model/control comparisons or strengthen line styles; show bin counts for the angle-conditioned mean and define bars. |
| §5.1 | “Only 5 ... exceeds” should read “exceed”. Define failure only as the stated beta limit; it is not failed injection. Condense software prefix details or move them to a supplement. |
| Abstract | Reduce the long inventory of numerical results. Retain the question, controlled model, principal finding with uncertainty and its physical implication. |
| Conclusion | Replace universal “should not be used” with the demonstrated limitation of this linear-map model for acceptance-limited design. |

Provide compact parameter and error-budget tables and a four-wire geometry figure
with wire positions, currents/polarity, length and relevant aperture. Identify
reference planes, observation point and physical losses consistently.

The official [JINST author instructions](https://jinst.sissa.it/jinst/help/helpLoader.jsp?pgType=author)
(accessed 2026-10-10) advise avoiding formulae in the title/abstract, suggest line
numbers, describe sequential references and the JHEP bibliography style, require
a data/software/code availability statement and disclosure of AI-assisted
manuscript preparation. The current draft has the latter statements; finalize
formatting and verify that the disclosure accurately reflects actual assistance.
A DOI is encouraged wherever available; do not call it an unconditional requirement.

## 5. Conditions for reconsideration

I would reconsider acceptance when the author supplies:

1. A demonstrated novel physical result with a controlled kicker model and a clear
   validity range, or a narrowed model-comparison article whose uncertainty is itself
   the result.
2. A threshold-defined, independently checked operating region, survival/acceptance
   validation at that region, and actionable sensitivity to justified or explicitly
   parameterized errors.
3. A statistically defensible stored-beam response and balanced paired comparisons.
4. An accessible frozen evidence package and a concise manuscript whose abstract,
   figures and conclusions match the same selected model and scope.

Not every suggested study must be run. For each task, a quantitative bound or
explicit narrowing of claims can be an acceptable response where specified.
Measurements, a prescribed number of references and a prescribed Monte Carlo
budget are not universal acceptance requirements. A point-by-point response should
identify the changed text, new evidence, residual uncertainty and any claim removed.
The [revision register](reviewer1_revision_tasks.md) gives the execution order and
acceptance tests for this major revision.
