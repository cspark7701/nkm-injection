# Milestone 139 — Repository orientation

Completed: 2026-10-12. Request: read README.md and AGENTS.md and examine the repository before further work.

Read the project instructions, README, package configuration, package exports, test fixture setup, active-plan index, completed-plan index and latest completed milestone. Inspected the notebook, script, configuration, source and test layout.

The installed package is `nkm_injection` version 0.2.0, under `src/nkm_injection/`, with the `nkm-production` entry point. Notebooks 01–03 provide the principal and optional study workflows; notebook 04 and the shell driver share production orchestration. Tests cover physics, tracking, optimization, configuration and publication contracts. Generated study artifacts belong under `results/`; the manuscript is under `docs/paper/`.

Milestone 138 consolidates round-2 manuscript revision tasks D1–D15 and author inputs A1–A6. Independent trajectory validation gates new simulations. README headline benchmarks describe the older September production run; subsequent milestones report revised exact 3-D field studies. AGENTS.md retains the former `src/nkm/` development path, while README lists broader protected-file categories than AGENTS.md. These documents were left unchanged.

Initial `git status --short` and `git diff --name-only` were empty. The command sandbox failed to initialize, so inspection commands used approved escalation. No simulations or tests were executed for this documentation-only orientation. No remote services were accessed. Only this archive and its index were changed; protected files are unchanged.
