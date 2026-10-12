# Milestone 158 — Journal recommendation after round-two revision

Date: 2026-10-12

## Request and assessment

Read the updated `docs/paper/paper.tex` and the current 19-page `paper.pdf`, the generated numerical macros and author inputs in `dependent_answers.md`. The manuscript reviewed is at commit `acff07fc0a819c1c80dda5bcc971acdd973f2d90`, following completed D1–D14 revisions. This milestone recommends a venue; it does not select the journal on the author's behalf or execute D15 formatting/submission.

**First choice: Physical Review Accelerators and Beams (PRAB), as a regular research article.** The strongest contribution is a validated beam-dynamics comparison: finite-length self-deflection, flank-dependent vertical response, thin versus sliced vector maps, sagitta-to-kick-width scaling and an independent adaptive trajectory check. The KLS design lattice is the application and validation setting. The declared chamber, corrected-ring scenarios and transparency tolerances add practical significance.

The [official PRAB scope and acceptance criteria](https://journals.aps.org/prab/about) include single-particle dynamics, magnet calculations and accelerator design studies, and require a significant substantive contribution. PRAB also has directly related work: [Sun et al., 23, 010702 (2020)](https://journals.aps.org/prab/abstract/10.1103/PhysRevAccelBeams.23.010702), on nonlinear-kicker injection optimization, and [Ollier et al., 26, 020101 (2023)](https://journals.aps.org/prab/abstract/10.1103/PhysRevAccelBeams.26.020101), on multipole-kicker transparency and commissioning. This is evidence of audience fit, not an acceptance prediction.

**Second choice: Nuclear Instruments and Methods in Physics Research Section A (NIM A).** It is a reasonable alternative if framed primarily as a practical injection-system modelling and tolerance study. Related published work includes [Alexandre et al., 986, 164739 (2021)](https://doi.org/10.1016/j.nima.2020.164739), already cited in the manuscript, and [A novel kind of nonlinear kicker for the Hefei Advanced Light Facility](https://www.sciencedirect.com/science/article/abs/pii/S0168900220313838). Publisher search results confirmed the latter's title and venue; its full text was not accessed. Do not imply hardware qualification of the preliminary filament design.

**Third choice: Journal of Instrumentation (JINST).** Its [official scope](https://jinst.sissa.it/jinst/help/helpLoader.jsp?pgType=about) explicitly includes accelerator theory, modelling and simulation. A stronger instrumentation emphasis would highlight wire/current sensitivities, septum leakage, pulse consistency and construction implications. The present article is primarily a beam-physics study, which makes PRAB the more direct fit. This ranking is editorial judgment, not a ranking of journal quality or an estimate of acceptance probability.

## Manuscript-specific preparation

- Clearly compare the new contribution with Sun et al. (2020), which is absent from the current bibliography. Its abstract describes nonlinear-kicker design and injection optimization for ALS/ALS-U; assess its methods before asserting the distinction. The present candidate distinction is the controlled finite-length/vector-map accuracy analysis and its validated limitations, not the general idea of nonlinear-kicker injection.
- Keep nominal 97.0% capture at 500 turns and 96.1% at 4000 turns separate from the 14.8% joint-error mean conditional on ten corrected rings. The low latter value is an important sensitivity result, not evidence for a commissioned injection design. Frame the paper around the mechanism and robustness limitations.
- The 0.29–2.04 micrometre single-wire tolerances are model-conditioned local sensitivities, not a certified simultaneous manufacturing budget. Preserve the current qualifications about chamber, pulse and full-system transparency.
- Streamline long sensitivity tables and procedural detail into supplementary material if they obscure the finite-length argument. The 19-page general article should not be treated as exceeding a fixed journal limit; PRAB explicitly permits detailed longer articles.
- Prepare a cover letter stating the specific new result and provide the frozen numerical attachment. A simulation-only submission can be within scope; neither this recommendation nor journal scope establishes scientific acceptance.

## Verification and changes

Checked working-tree status before and after. No manuscript, PDF, code, prior review or protected scientific input was changed. No simulation or numerical test suite was run for this advisory task. Created this archive and updated the completed-task index. Official journal scope pages and primary publication pages/search results were checked; the NIM A scope page could not be retrieved directly, so its fit is supported by related publisher-listed papers rather than an unverified quotation of its current policy.
