# Article scope, principal question and journal fit (Task 001)

Prepared 2026-10-09. Sources accessed 2026-10-09. Status: decided for the current campaign;
the author must confirm title, authorship and journal before submission (Task 012).

## Principal question

**For a 4 GeV fourth-generation storage-ring lattice whose on-momentum horizontal dynamic
aperture (DA) at the injection point is only ~12–16 mm, can a wire-based nonlinear kicker
magnet (NKM), modeled with its RADIA field map and placed 2 m downstream of the injection
septum, capture the beam delivered by the matched BTS line while keeping the stored-beam
disturbance below a small fraction of its rms size — and how wide and how robust is that
operating window under realistic magnet, beam and alignment errors?**

The question is answered with nonlinear element-by-element ring tracking. Linear one-turn-map
tracking is retained only as a cross-check, because it misses the DA (milestone 103).

## Bounded candidate claims (to be accepted or narrowed by evidence)

| ID | Candidate claim | Evidence required (task) |
| :--- | :--- | :--- |
| C1 | The on-momentum DA at the NKM is ~12–16 mm; a linearized ring model overestimates capture | Native vs linear tracking, DA/momentum scan (003) |
| C2 | With the septum at −20 mm and a 2 m drift, an incoming angle near +5.75 mrad places the beam near the kick-map peak (−8.5 mm), where the kick cancels the angle and leaves an amplitude inside the DA | Operating-region map with paired controls (004) |
| C3 | The NKM disturbs the stored beam by a small fraction of its rms size, whereas a uniform dipole kick of equal strength at the injection point would not be transparent | Stored-beam tracking with calibrated controls (004) |
| C4 | Capture remains high for a quantified fraction of combined-error realizations; the dominant error sources are identified | Capture robustness ensembles (006); optics tolerance replication (005) |
| C5 | The matched BTS optics are required: baseline optics give lower capture | Coupled BTS→NKM handoff, baseline vs optimized (004) |

Excluded unless separately validated: operational readiness, experimental validation, beam
lifetime, "zero perturbation", and Pareto-optimal BTS design as a main claim (decided in Task 007).

## Novelty relative to closest work (verified records)

- Single pulsed multipole / nonlinear kickers have been demonstrated: KEK-PF pulsed sextupole
  (Takaki et al., PRST-AB 13, 020705, 2010), BESSY II NLK prototype (IPAC'11 THPO024), and the
  SOLEIL/MAX IV multipole injection kicker (Ollier et al., PRAB 26, 020101, 2023).
- Liu et al. (IPAC'16 THPMR011, Sirius) identify the kick nonlinearity at the injected beam and
  the injected beam size as the main efficiency limits.
- **This article's contribution:** a quantified capture/transparency operating window for a
  specific wire-based NKM in a 4GSR lattice with a small DA, using the RADIA map, nonlinear
  ring tracking, a coupled BTS handoff and combined-error capture ensembles, with paired and
  calibrated controls. Software infrastructure (hash checks, manifests, test suite) is supporting
  method, not novelty.

## Journal and category

Provisional venue: **JINST, regular research paper**. JINST scope includes accelerator
instrumentation and simulation; regular papers versus technical reports are distinguished by
scientific contribution. If the evidence supports only C1–C3 qualitatively, a JINST technical
report is the fallback.

JINST requirements recorded (author instructions, accessed 2026-10-09):
`jinstpub.sty` template (JINST.cls obsolete); abstract fits on the first page and has no
formulae or references; 2–4 keywords from the official JINST list; numbered references in
order of citation (JHEP.bst), with the `.bbl` supplied; data/software/code availability
statement at the end; AI-assisted preparation declared in methods or acknowledgments.

## Author metadata (to be confirmed by the author)

Chong Shik Park — Department of Accelerator Science and Center for Accelerator Research,
Korea University, Sejong 30019, Republic of Korea; corresponding e-mail kuphy@korea.ac.kr.
Funding: not recorded in the repository — **author input required**.

## Sources

- JINST author instructions: https://jinst.sissa.it/jinst/help/helpLoader.jsp?pgType=author
- JINST scope: https://jinst.sissa.it/jinst/help/JINST/JINST_about.jsp
- Takaki et al. 2010: https://doi.org/10.1103/PhysRevSTAB.13.020705
- Ollier et al. 2023: https://doi.org/10.1103/PhysRevAccelBeams.26.020101
- BESSY II NLK, IPAC'11 THPO024: https://accelconf.web.cern.ch/ipac2011/papers/thpo024.pdf
- Liu et al., IPAC'16 THPMR011: https://doi.org/10.18429/JACoW-IPAC2016-THPMR011
