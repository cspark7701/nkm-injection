# Journal research-article revision tasks

Prepared: 2026-10-09. All tasks below are **planned**, not executed.

The present manuscript describes a technical framework and mixes historical
results with current models. This sequence builds a validated physical argument
and a regular journal article. Formatting and more Monte Carlo samples alone do
not establish novelty or model validity.

Read the [simulation strategy](../../023_ADDITIONAL_SIMULATION_AND_JOURNAL_STRATEGY.md)
first. It gives exact supported commands and separately identifies proposed CLIs
that need implementation. The provisional venue is JINST; Task 001 establishes
the final scientific scope and journal fit.

| Order | Task | Dependencies |
| :--- | :--- | :--- |
| 001 | [Define the scientific question, novelty and journal fit](001_research_question_and_journal_fit.md) | None |
| 002 | [Freeze the canonical physical model and audit existing claims](002_canonical_physics_and_claim_audit.md) | 001 |
| 003 | [Implement independent tracking and numerical validation drivers](003_tracking_validation_driver.md) | 002 |
| 004 | [Establish fair controls and a coupled injection operating region](004_calibrated_controls_and_coupled_injection.md) | 002, 003 |
| 005 | [Replicate fixed-optics tolerances and report defensible uncertainty](005_tolerance_replication_and_uncertainty.md) | 002; repeat after 003-004 if the physical model changes |
| 006 | [Implement and run combined-error capture robustness](006_combined_error_capture_study.md) | 003, 004; audited error coverage from 002 |
| 007 | [Decide and validate the role of Pareto optimization](007_design_comparison_and_moga_evidence.md) | 001, 002, 004; 006 for robustness-ranked finalists |
| 008 | [Rewrite the manuscript around a scientific argument](008_restructure_research_article.md) | 001, 002; scientific results from 003-007 before finalizing claims |
| 009 | [Connect the article to selected evidence and journal-quality figures](009_publication_data_and_figures.md) | 002-007 for included claims; 008 outline |
| 010 | [Verify references and prepare scholarly metadata](010_literature_and_submission_metadata.md) | 001, 008; 009 for data/software citations |
| 011 | [Review the article as a referee before freezing it](011_independent_scientific_review.md) | 008, 009, 010; all included simulation tasks complete |
| 012 | [Assemble a complete regular-article submission package](012_submission_package_and_final_gate.md) | 011; author final scientific review |

Tasks 002-004 are scientific gates before costly new ensembles. Task 005 can run
on the existing frozen model for characterization, but must be repeated if the
model or selected optics change. Tasks 006-007 supply additional evidence only
when required by the final article's scope. Tasks 008-010 can begin with an outline
and evidence inventory, but final numerical claims wait for validated results.

The manuscript source and existing PDF are not revised by creation of this plan.
The completed-plan archive records only preparation of these documents. Each
subsequent implemented task receives its own execution summary and evidence.
