# Milestone 85 — Repository refactoring opportunity review

Completed: 2026-10-07  
Scope: review and task documentation only.

## Request and outcome

Read AGENTS.md and README.md first, reviewed the current repository, and saved 12 numbered proposed task specifications in [05_refactor_tasks](../../../05_refactor_tasks/README.md), with a priority/dependency index and JSON task manifest. Compared findings with the 16 completed tasks in docs/04_refactor_tasks to identify remaining gaps rather than re-list completed abstractions.

## Findings

The backlog covers manifest-driven publication inputs, production stage routing, strict field-map domains and parsing, explicit evaluation failures, one-turn-map cache lifecycle, optimization-to-tolerance handoffs, strict configuration round trips, canonical package imports, tracking boundary contracts, statistical convergence evidence, isolated publication validation/builds, and reusable notebook workflows. Each task includes source evidence, implementation scope, dependencies and acceptance criteria.

## Verification and limits

- Initial git status and diff were clean; final changes are confined to review documents and this archive index.
- Checked task numbering, manifest consistency and local Markdown link targets.
- Attempted `python -m pytest -q`: 22 collection errors in Python 3.13.5 due to unavailable at/openpyxl and the uninstalled canonical package. Scientific tests could not run; no physics-validation claim is made.
- Reviewed notebook source as JSON without executing or rewriting it. No simulations, protected inputs, source code or existing notebook outputs were modified.
- No remote GitHub interactions or pushes occurred.

## Follow-up

Implementation is outside this review request. All 12 backlog entries remain proposed. Execute them in a configured project environment and archive their implementation milestones separately.
