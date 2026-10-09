# Milestone 111 — Journal Task 008: manuscript rewritten around the scientific argument

Completed: 2026-10-09. Task: [008](../../jinst-paper/tasks/008_restructure_research_article.md).

Replaced the framework-inventory manuscript `docs/jinst-paper/paper.tex` with a research article:
"Capture window and robustness of nonlinear-kicker injection into a 4 GeV storage ring with a small dynamic
aperture". Structure: introduction and open question; system and model (ring/DA, NKM field map and polarity,
injection geometry and coupled BTS handoff, controls and observables); model validation; operating window with
paired calibrated controls and transparency; robustness (BTS optics tolerances, combined-error capture with
diagnostic ensembles); discussion and limitations; conclusions; data/software availability; AI-assistance
declaration. Every quantitative result is a macro from `generated/journal_macros.tex` (Task 009). Removed:
MOGA, the framework/test/hash inventory, "zero perturbation", "proves", "rigorous 6D symplectic", the linear-map
capture table and the 430× ratio. Limitations (no ring errors or chamber apertures, thin kick, magnetostatic
map without measurement, assumed error budget, 500-turn survival) and the unmet tolerance-prefix target are
stated. Clean isolated compilation: 10 pages, no errors, warnings, undefined references or overfull boxes.
