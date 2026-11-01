# Journal recommendations for the NKM manuscript

Recorded: 2026-11-01. Based on the author's [journal clarification](/home/cspark/Documents/journal_recommendations/journal_recommendations.md), dated 2026-10-30, and the current NKM manuscript after round-5 revisions. Publisher scope and author pages were checked for this recommendation.

**Recommend submitting to Physical Review Accelerators and Beams (PRAB) first.** NIM A is the strongest alternative for the present manuscript. The ranking below prioritizes the scientific contribution, audience and amount of reframing required, rather than impact factor or an estimated acceptance probability.

The article is *Finite-length and vertical effects in nonlinear-kicker injection into a Korea Light Source design lattice*: [source](paper.tex), [one-column article](paper.pdf), [two-column preview](paper_twocolumn.pdf) and [supplement](supplement.pdf). The reviewed scientific version is identified in [round5_final_identity.json](round5_final_identity.json); the article is 36/18 pages in its two layouts, with seven supplemental pages. Both [Reviewer 1](reviews/review_round_06_reviewer_01_report.md) and [Reviewer 2](reviews/review_round_06_reviewer_02_report_and_tasks.md) recommend scientific acceptance with optional editorial suggestions. These are internal assessments, not decisions by a journal.

## Ranked top five

| Rank | Journal | Fit for the current NKM paper | Preparation needed |
| :--- | :--- | :--- | :--- |
| **1** | **Physical Review Accelerators and Beams (PRAB)** | **Best fit.** The finite-length accuracy result, vertical-kick mechanism, paired capture attribution and magnet tolerances directly address its accelerator audience. | Retain the current Research Article framing and REVTeX sources; finish author/submission decisions. |
| **2** | **Nuclear Instruments and Methods in Physics Research Section A (NIM A)** | **Strongest alternative.** The validated magnet model and its consequences for injection-system design fit accelerator and instrument development. | Emphasize modelling validation and design implications; adapt to Elsevier formatting if selected. |
| **3** | **Nuclear Science and Techniques (NST)** | **Credible specialist alternative.** Accelerators and synchrotron-related technology are explicitly in scope. | Lead with the physical mechanism and its usefulness for injection design, supported by the KLS application. |
| **4** | **Journal of Instrumentation (JINST)** | **Good accelerator-modelling alternative.** Its scope explicitly includes accelerator concepts, theory, modelling and simulations. | Present a regular research paper about validated modelling and design limits; retain the distinction between simulation and hardware performance. |
| **5** | **Physical Review Research (PRResearch)** | **Plausible broader-physics option, with more reframing.** Methodological and applied physics are in scope, but the current presentation serves accelerator specialists most directly. | Make the approximation error and interaction of static errors with shot jitter accessible to a general physics readership. Keep the demonstrated validity range. |

These are manuscript-specific judgments inferred from the scope pages and the evidence in this paper. NST and JINST are close alternatives; their ordering is less decisive than PRAB's lead and NIM A's position as the principal alternative.

## Why PRAB remains first

PRAB explicitly covers magnet calculations, single-particle dynamics, accelerator design and beam control. Its Research Article category has no fixed length limit, although length should be justified by content. The present detailed article can therefore retain the validation and attribution evidence supporting its conclusions. The journal is currently diamond open access, without author publication charges. [PRAB scope and criteria](https://journals.aps.org/prab/about), [author information](https://journals.aps.org/prab/authors).

The closest comparison already discussed in the manuscript, Sun et al., “Optimizations of nonlinear kicker injection for synchrotron light sources,” appeared in PRAB. This establishes a relevant specialist readership, without making the new manuscript's acceptance automatic. Its contribution must remain the quantified approximation error and conditional injection physics, with established segmented tracking credited. [Published article](https://journals.aps.org/prab/abstract/10.1103/PhysRevAccelBeams.23.010702).

The paper's negative robustness result is compatible with that contribution. A methods-and-mechanism article need not demonstrate a better operational kicker. It should preserve the distinction between horizontal-only production steering and ideal two-plane removal, and between the 150-draw headline and 50-draw sensitivities.

## Why these alternatives

**NIM A:** Elsevier's scope includes accelerator development, beam transport, theoretical work and simulation tools. It also warns against unvalidated or insufficiently original studies using standard simulation codes. This paper's independent integration checks, field-convention audit and paired mechanism tests are central to the case for submission. NIM A is an appropriate alternative, not a guaranteed or undemanding destination. The ScienceDirect pages returned access errors during this check; the publisher's accessible shop description supplies the scope and simulation-study qualification. [Elsevier description](https://shop.elsevier.com/journals/nuclear-instruments-and-methods-in-physics-research-section-a-accelerators-spectrometers-detectors-and-associated-equipment/0168-9002).

**NST:** Its scope includes accelerator technology and applications, synchrotron radiation and beamline technology. The argument would be the injection-physics insight and validated design assessment, rather than a new general-purpose tracking algorithm. [NST aims and scope](https://link.springer.com/journal/41365/aims-and-scope).

**JINST:** Accelerator concepts, modelling and simulations are explicitly included. Experimental hardware is therefore not an absolute prerequisite for a regular research article in scope. I recommend that category for the present contribution; its separate Technical Reports category should not be assumed to be the easier route for a simulation-only study. [JINST scope and editorial policy](https://jinst.sissa.it/jinst/help/JINST/JINST_about.jsp).

**PRResearch:** It welcomes significant applied, theoretical and methodological physics and asks authors to write for a general readership. That makes it possible, but less directly matched to this specialist presentation than PRAB. Reframing should explain the physics beyond KLS without promoting the empirical sagitta fit into a universal law. [Scope and criteria](https://journals.aps.org/prresearch/about), [readership guidance](https://journals.aps.org/prresearch/authors).

## Relationship to the author's clarification

The clarification already recommends PRAB first, puts PRResearch or New Journal of Physics among broader-physics possibilities, and identifies NIM A as an alternative. I retain its first choice but move the specialist alternatives ahead of PRResearch for the current version. This reflects the bounded diagnostic families, assumed error budget and application to one design lattice, rather than a judgment based on journal metrics.

New Journal of Physics remains a possible choice if broader visibility is the main objective. Its guidance stresses substantial advances and accessibility to non-specialists; the current accelerator-focused article makes the specialist venues a more direct match. It falls just outside this practical top five. [NJP scope and requirements](https://publishingsupport.iopscience.iop.org/journals/new-journal-of-physics/about-new-journal-physics/).

I would not prioritize a computational-methods journal merely because the repository contains substantial software: the paper credits established numerical methods and its principal new results concern beam dynamics. Nor does the current scope support a PRL-style broad-physics claim. No stronger generality claim is needed to justify PRAB.

The clarification explicitly marks its impact factors/quartiles as provisional and partly drawn from different reporting years or aggregators. They are not independently verified here or used as the ranking criterion; use Clarivate JCR if a formal metric-based decision is required. No acceptance percentages or turnaround guarantees are assigned.

## Recommended action

Keep **PRAB as the first submission target**, as already selected by the author. Use **NIM A as the principal alternative** if a different venue becomes necessary. Consider NST or JINST for a specialist design/modelling presentation, and PRResearch if the author prefers broader exposure and accepts the additional framing work.

This recommendation does not change the manuscript, select a new target on the author's behalf or perform submission. The existing [G7 author/access/delivery gate](reviews/revision_round_05_plan_for_review_round_05.md#g7--submission-stage-author-gate) remains separate. Local review recommendations do not establish external evidence access or guarantee an editor's decision.
